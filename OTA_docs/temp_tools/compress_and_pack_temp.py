import os
import sys
import struct
import lzma
import argparse

# C-структуры заголовков (Little-Endian)
ACTIONS_BOOT_HEADER_FMT = '<8sIIIIIIII'
ACTIONS_BOOT_HEADER_SIZE = struct.calcsize(ACTIONS_BOOT_HEADER_FMT)

ACTIONS_LZMA_HEADER_FMT = '<4sIII'
ACTIONS_LZMA_HEADER_SIZE = struct.calcsize(ACTIONS_LZMA_HEADER_FMT)

ACTIONS_BOOT_MAGIC = b'ACTHHTCA'
ACTIONS_LZMA_MAGIC = b'LZMA'

# Размер разжатого среза монолита (2 MiB / 0x200000 байт)
CHUNK_SIZE_LIMIT = 0x200000

def compress_and_pack_temp(input_dir="TEMP_extracted", output_file="TEMP_new.bin"):
    """
    Универсальный автоматический сборщик загрузочного контейнера TEMP.bin (v1.6):
    - Строго сохраняет ВСЕ оригинальные значения из actions_boot_header.bin 
      (включая entry_point, load_addr и заводские сигнатуры).
    - Нарезает inner_aota_container.bin на блоки по 2 MiB и сжимает в XZ/LZMA.
    """
    if not os.path.exists(input_dir):
        print(f"[-] Ошибка: Входной каталог '{input_dir}' не найден.")
        return False

    print(f"[*] Универсальная сборка '{output_file}' из каталога '{input_dir}'...")

    # 1. Загрузка оригинального заголовка ТЕКУЩЕЙ прошивки
    hdr_path = os.path.join(input_dir, "actions_boot_header.bin")
    if not os.path.exists(hdr_path):
        print(f"[-] Ошибка: Заголовок '{hdr_path}' не найден. (Убедитесь, что распаковали нужную прошивку)")
        return False

    with open(hdr_path, 'rb') as f_hdr:
        boot_hdr = bytearray(f_hdr.read())

    # Восстанавливаем размер до 40 байт для старых дампов
    if len(boot_hdr) == 36:
        boot_hdr += struct.pack('<I', 0x00000200) # ivt_offset = 0x200
    elif len(boot_hdr) != ACTIONS_BOOT_HEADER_SIZE:
        print(f"[-] Ошибка: Некорректный размер заголовка ({len(boot_hdr)} байт, ожидалось 40).")
        return False

    # 2. Загрузка Boot Stub
    stub_path = os.path.join(input_dir, "boot_stub.bin")
    if not os.path.exists(stub_path):
        print(f"[-] Ошибка: Файл '{stub_path}' не найден.")
        return False

    with open(stub_path, 'rb') as f_stub:
        boot_stub = f_stub.read()

    # Отрезаем дубликат заголовка из начала boot_stub, если он туда попал
    if boot_stub.startswith(ACTIONS_BOOT_MAGIC):
        boot_stub = boot_stub[ACTIONS_BOOT_HEADER_SIZE:]

    boot_stub_size = len(boot_stub)
    print(f"[+] Прочитан Boot Header (40 байт) и Boot Stub ({boot_stub_size} байт).")

    # Декодируем оригинальный заголовок ТОЛЬКО для вывода в лог (МЫ ЕГО НЕ МЕНЯЕМ!)
    magic, load_addr, block_size, pad, exec_addr, entry_point, header_sig, payload_sig, ivt_offset = struct.unpack(
        ACTIONS_BOOT_HEADER_FMT, boot_hdr
    )

    print(f"\n[+] Сохранены оригинальные параметры Boot Header:")
    print(f"    - Load / Exec Address (0x08 / 0x14): 0x{load_addr:08X}")
    print(f"    - Entry Point Offset  (0x18):        0x{entry_point:08X} (Оригинал)")
    print(f"    - Header Signature    (0x1C):        0x{header_sig:08X} (Оригинал)")
    print(f"    - Payload Signature   (0x20):        0x{payload_sig:08X} (Оригинал)")
    print(f"    - IVT Offset          (0x24):        0x{ivt_offset:08X}")

    # 3. Загрузка монолитного образа и его нарезка (Chunking)
    monolith_path = os.path.join(input_dir, "inner_aota_container.bin")
    if not os.path.exists(monolith_path):
        print(f"[-] Ошибка: Файл монолита '{monolith_path}' не найден.")
        return False

    with open(monolith_path, 'rb') as f_mono:
        monolith_data = f_mono.read()

    monolith_size = len(monolith_data)
    print(f"\n[+] Обработка inner_aota_container.bin ({monolith_size} байт)...")

    payload_blocks = b''
    offset = 0
    chunk_index = 1

    while offset < monolith_size:
        # Нарезаем монолит кусками не более 2 МБ
        chunk_slice = monolith_data[offset : offset + CHUNK_SIZE_LIMIT]
        uncomp_size = len(chunk_slice)

        # Сжимаем кусок в XZ
        xz_compressed = lzma.compress(chunk_slice, format=lzma.FORMAT_XZ)
        comp_size = len(xz_compressed)

        print(f"    [+] Сжат чанк #{chunk_index}: RAM 0x{uncomp_size:X} -> XZ 0x{comp_size:X} байт")

        # Добавляем 16-байтный проприетарный заголовок
        lzma_hdr = struct.pack(
            ACTIONS_LZMA_HEADER_FMT,
            ACTIONS_LZMA_MAGIC,
            ACTIONS_LZMA_HEADER_SIZE,
            comp_size,
            uncomp_size
        )

        payload_blocks += lzma_hdr + xz_compressed
        offset += uncomp_size
        chunk_index += 1

    # 4. Сборка итогового файла
    final_data = bytes(boot_hdr) + boot_stub + payload_blocks

    with open(output_file, 'wb') as f_out:
        f_out.write(final_data)

    print(f"\n[!] Файл '{output_file}' успешно собран. Размер: {len(final_data)} байт.")
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Универсальный перепаковщик TEMP.bin для Actions ATS3085S")
    parser.add_argument("input_dir", nargs="?", default="TEMP_extracted", help="Каталог с распакованными файлами")
    parser.add_argument("output_file", nargs="?", default="TEMP_new.bin", help="Имя итогового файла")
    args = parser.parse_args()
    compress_and_pack_temp(args.input_dir, args.output_file)