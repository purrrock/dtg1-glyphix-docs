import os
import sys
import struct
import lzma
import argparse

# C-структуры заголовков (Little-Endian)
# Actions Boot Header (40 байт / 0x28)
ACTIONS_BOOT_HEADER_FMT = '<8sIIIIIIII'
ACTIONS_BOOT_HEADER_SIZE = struct.calcsize(ACTIONS_BOOT_HEADER_FMT)

# Actions LZMA Header (16 байт / 0x10)
ACTIONS_LZMA_HEADER_FMT = '<4sIII'
ACTIONS_LZMA_HEADER_SIZE = struct.calcsize(ACTIONS_LZMA_HEADER_FMT)

ACTIONS_BOOT_MAGIC = b'ACTHHTCA'
# Строгая сигнатура: "LZMA" + header_size (0x00000010)
ACTIONS_LZMA_MAGIC_STRICT = b'LZMA\x10\x00\x00\x00'

def unpack_temp(input_file, output_dir="TEMP_extracted", save_chunks=False):
    """
    Распаковывает загрузочный контейнер TEMP.bin:
    - Парсит 40-байтный заголовок ACTHHTCA
    - Извлекает Boot Stub (включая заполнитель и IVT)
    - Извлекает и декомпрессирует сжатые XZ-чанки в памяти (In-Memory)
    - Склеивает разжатые блоки в единый inner_aota_container.bin
    - Сохраняет промежуточные chunk* файлы только если save_chunks == True
    """
    if not os.path.exists(input_file):
        print(f"[-] Ошибка: Входной файл '{input_file}' не найден.")
        return False

    with open(input_file, 'rb') as f:
        data = f.read()

    file_size = len(data)
    print(f"[*] Чтение файла: {input_file} (Размер: {file_size} байт / {hex(file_size)})")

    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] Каталог выгрузки: {output_dir}/")

    # 1. Разбор главного загрузочного заголовка ACTHHTCA (40 байт)
    if data.startswith(ACTIONS_BOOT_MAGIC):
        boot_hdr = data[:ACTIONS_BOOT_HEADER_SIZE]
        (magic, load_addr, block_size, pad, 
         exec_addr, entry_point, hdr_crc, payload_crc, ivt_offset) = struct.unpack(
            ACTIONS_BOOT_HEADER_FMT, boot_hdr
        )
        print("\n[+] Обнаружен Actions Boot Header ('ACTHHTCA', 40 байт):")
        print(f"    - Load Address:   0x{load_addr:08X}")
        print(f"    - Block Size:     0x{block_size:08X}")
        print(f"    - Exec Address:   0x{exec_addr:08X}")
        print(f"    - Entry Point:    0x{entry_point:08X}")
        print(f"    - Header Sig:     0x{hdr_crc:08X}")
        print(f"    - Payload Sig:    0x{payload_crc:08X}")
        print(f"    - IVT Offset:     0x{ivt_offset:08X}")

        hdr_path = os.path.join(output_dir, "actions_boot_header.bin")
        with open(hdr_path, 'wb') as f_hdr:
            f_hdr.write(boot_hdr)
        print(f"    [->] Сохранен заголовок: {hdr_path}")
    else:
        print("[!] Внимание: Заголовок ACTHHTCA не обнаружен в начале файла.")

    # 2. Поиск первой СТРОГОЙ сигнатуры LZMA для определения границ Boot Stub
    first_lzma_offset = data.find(ACTIONS_LZMA_MAGIC_STRICT)
    if first_lzma_offset != -1:
        # Извлекаем данные со смещения 0x28 (сразу после 40-байтного заголовка) до начала LZMA
        boot_stub_data = data[ACTIONS_BOOT_HEADER_SIZE:first_lzma_offset]
        boot_stub_path = os.path.join(output_dir, "boot_stub.bin")
        with open(boot_stub_path, 'wb') as f_stub:
            f_stub.write(boot_stub_data)
        print(f"\n[+] Извлечен Boot Stub (0x{ACTIONS_BOOT_HEADER_SIZE:08X} - 0x{first_lzma_offset:08X}):")
        print(f"    - Размер: {len(boot_stub_data)} байт")
        print(f"    [->] Сохранен файл: {boot_stub_path}")
    else:
        print("[-] Критическая ошибка: Строгая сигнатура контейнеров LZMA не найдена!")
        return False

    # 3. Итеративный разбор всех сжатых блоков Actions LZMA
    offset = first_lzma_offset
    chunk_index = 1
    unpacked_chunks = []

    print("\n[*] Начало In-Memory разбора сжатых блоков LZMA/XZ...")

    while True:
        offset = data.find(ACTIONS_LZMA_MAGIC_STRICT, offset)
        if offset == -1:
            break

        header_bytes = data[offset : offset + ACTIONS_LZMA_HEADER_SIZE]
        magic, header_size, comp_size, uncomp_size = struct.unpack(
            ACTIONS_LZMA_HEADER_FMT, header_bytes
        )

        xz_start = offset + header_size
        xz_end = xz_start + comp_size

        if xz_end > file_size:
            print(f"[-] Ошибка: Чанк #{chunk_index} по смещению 0x{offset:08X} выходит за пределы файла.")
            break

        print(f"\n[+] Чанк #{chunk_index} (Смещение 0x{offset:08X}):")
        print(f"    - Сжатый размер: {comp_size} байт (0x{comp_size:X})")
        print(f"    - Размер в RAM:  {uncomp_size} байт (0x{uncomp_size:X})")

        xz_data = data[xz_start:xz_end]

        # Выгрузка сырого XZ-потока на диск только при включенном флаге отладки
        if save_chunks:
            xz_path = os.path.join(output_dir, f"chunk_{chunk_index}.xz")
            with open(xz_path, 'wb') as f_xz:
                f_xz.write(xz_data)
            print(f"    [->] Сохранен сырой поток: {xz_path}")

        # Декомпрессия XZ в оперативной памяти
        try:
            unpacked_bytes = lzma.decompress(xz_data)
            actual_size = len(unpacked_bytes)
            
            if save_chunks:
                unpacked_path = os.path.join(output_dir, f"chunk_{chunk_index}_unpacked.bin")
                with open(unpacked_path, 'wb') as f_unp:
                    f_unp.write(unpacked_bytes)
                print(f"    [->] Сохранен распакованный дамп: {unpacked_path} ({actual_size} байт)")
            else:
                print(f"    [+] Успешно разжат в RAM ({actual_size} байт)")

            if actual_size != uncomp_size:
                print(f"    [!] Внимание: Фактический размер ({actual_size}) не совпадает с заявленным ({uncomp_size})")

            unpacked_chunks.append(unpacked_bytes)
        except Exception as e:
            print(f"    [-] Ошибка декомпрессии XZ блока #{chunk_index}: {e}")

        offset = xz_end
        chunk_index += 1

    # 4. Склеивание всех блоков из RAM в единый образ внутреннего AOTA-контейнера
    if unpacked_chunks:
        concatenated_data = b''.join(unpacked_chunks)
        concat_path = os.path.join(output_dir, "inner_aota_container.bin")
        with open(concat_path, 'wb') as f_cat:
            f_cat.write(concatenated_data)
        print(f"\n[+] Склейка распакованных блоков завершена:")
        print(f"    - Итоговый размер образа: {len(concatenated_data)} байт")
        print(f"    [->] Сохранен монолитный образ: {concat_path}")

    print(f"\n[*] Распаковка TEMP.bin в каталог '{output_dir}/' успешно завершена.")
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Распаковщик прошивки Actions Semiconductor TEMP.bin")
    parser.add_argument("input_file", nargs="?", default="TEMP.bin", help="Путь к файлу TEMP.bin (по умолчанию: TEMP.bin)")
    parser.add_argument("-d", "--dir", default="TEMP_extracted", help="Каталог для выгрузки (по умолчанию: TEMP_extracted)")
    parser.add_argument("-s", "--save-chunks", action="store_true", help="Сохранять промежуточные отладочные файлы chunk_*.xz и chunk_*_unpacked.bin")
    
    args = parser.parse_args()
    unpack_temp(args.input_file, args.dir, args.save_chunks)