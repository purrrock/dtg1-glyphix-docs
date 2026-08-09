import os
import sys
import struct
import zlib
import lzma
import argparse

# --- Константы структур ---
AOTA_MAGIC = b'AOTA'

# Actions Boot Header (40 байт / 0x28)
ACTIONS_BOOT_HEADER_FMT = '<8sIIIIIIII'
ACTIONS_BOOT_HEADER_SIZE = struct.calcsize(ACTIONS_BOOT_HEADER_FMT)

# Actions LZMA Header (16 байт / 0x10)
ACTIONS_LZMA_HEADER_FMT = '<4sIII'
ACTIONS_LZMA_HEADER_SIZE = struct.calcsize(ACTIONS_LZMA_HEADER_FMT)

ACTIONS_BOOT_MAGIC = b'ACTHHTCA'
# Строгая сигнатура: "LZMA" + header_size (0x00000010)
ACTIONS_LZMA_MAGIC_STRICT = b'LZMA\x10\x00\x00\x00'


def parse_aota_container(file_path, output_dir):
    """
    Универсальный парсер AOTA-контейнеров (подходит для внешнего и внутреннего).
    Извлекает файлы и сохраняет метаданные в version.txt.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    with open(file_path, 'rb') as f:
        header = f.read(512)
        magic, checksum_main, flags, file_count, fat_offset, data_offset = struct.unpack('<4sIIIHH', header[:20])
        
        if magic != AOTA_MAGIC:
            raise ValueError(f"Неверная сигнатура {magic}. Ожидается 'AOTA'.")
            
        build_ver = header[0x40:0x60].split(b'\x00')[0].decode('ascii', errors='ignore')
        platform_id = header[0x60:0x7E].split(b'\x00')[0].decode('ascii', errors='ignore')

        with open(os.path.join(output_dir, "version.txt"), "w", encoding="utf-8") as vf:
            vf.write(f"build_ver={build_ver}\n")
            vf.write(f"platform_id={platform_id}\n")
            
        print(f"    [+] Версия: {build_ver} | Платформа: {platform_id}")
        
        f.seek(fat_offset)
        extracted_files = []
        for i in range(file_count):
            fat_entry = f.read(32)
            if len(fat_entry) < 32: break
                
            name_b, file_offset, file_size, _, file_crc = struct.unpack('<16sIIII', fat_entry)
            filename = name_b.split(b'\x00')[0].decode('ascii')
            
            current_pos = f.tell()
            f.seek(file_offset)
            payload = f.read(file_size)
            
            actual_crc = zlib.crc32(payload) & 0xFFFFFFFF
            status = "OK" if actual_crc == file_crc else "CRC_ERR"
            
            out_path = os.path.join(output_dir, filename)
            with open(out_path, 'wb') as out_f:
                out_f.write(payload)
                
            print(f"    [->] Извлечен: {filename:<14} | Размер: {file_size:<7} B | Статус: {status}")
            extracted_files.append(out_path)
            
            f.seek(current_pos)
            
    return extracted_files


def parse_temp_boot_image(temp_path, output_dir, save_chunks=False):
    """
    Распаковывает загрузочный контейнер TEMP.bin (v1.6):
    - Парсит 40-байтный заголовок ACTHHTCA
    - Извлекает Boot Stub (включая заполнитель и IVT)
    - Извлекает и декомпрессирует сжатые XZ-чанки в памяти (In-Memory)
    - Склеивает разжатые блоки в единый inner_aota_container.bin
    """
    os.makedirs(output_dir, exist_ok=True)
    
    with open(temp_path, 'rb') as f:
        data = f.read()

    # 1. Чтение и валидация Boot Header
    if data[:8] != ACTIONS_BOOT_MAGIC:
        raise ValueError("Неверная сигнатура Boot Header (ожидается ACTHHTCA)")

    with open(os.path.join(output_dir, "actions_boot_header.bin"), 'wb') as hf:
        hf.write(data[:ACTIONS_BOOT_HEADER_SIZE])
    print(f"    [+] Извлечен 'actions_boot_header.bin'")

    # 2. Динамический поиск начала сжатых XZ-чанков
    lzma_offset = data.find(ACTIONS_LZMA_MAGIC_STRICT)
    if lzma_offset == -1:
        raise ValueError("Сжатые данные (LZMA) не найдены внутри TEMP.bin")

    # 3. Извлечение Boot Stub (от конца заголовка до начала первого LZMA-блока)
    boot_stub_data = data[ACTIONS_BOOT_HEADER_SIZE:lzma_offset]
    with open(os.path.join(output_dir, "boot_stub.bin"), 'wb') as bf:
        bf.write(boot_stub_data)
        
    print(f"    [+] Извлечен 'boot_stub.bin' (размер: {len(boot_stub_data)} байт)")
    print(f"    [+] Начало сжатых блоков LZMA: 0x{lzma_offset:08X}")
    
    # 4. Чтение и декомпрессия XZ-чанков
    offset = lzma_offset
    chunk_index = 0
    unpacked_chunks = []
    
    while offset < len(data):
        if offset + ACTIONS_LZMA_HEADER_SIZE > len(data):
            break
            
        # Проверка строгой сигнатуры LZMA для текущего чанка
        if data[offset:offset+8] != ACTIONS_LZMA_MAGIC_STRICT:
            break
            
        magic, header_sz, comp_sz, uncomp_sz = struct.unpack(ACTIONS_LZMA_HEADER_FMT, data[offset:offset+ACTIONS_LZMA_HEADER_SIZE])
        
        xz_start = offset + ACTIONS_LZMA_HEADER_SIZE
        xz_end = xz_start + comp_sz
        chunk_data = data[xz_start:xz_end]
        
        try:
            unpacked = lzma.decompress(chunk_data)
            
            if save_chunks:
                chunk_path = os.path.join(output_dir, f"chunk_{chunk_index}_unpacked.bin")
                with open(chunk_path, 'wb') as cf:
                    cf.write(unpacked)
                    
            unpacked_chunks.append(unpacked)
            print(f"    [+] XZ Чанк #{chunk_index}: Сжато {comp_sz} B -> Разжато {len(unpacked)} B (Ожидалось {uncomp_sz})")
        except Exception as e:
            print(f"    [-] Ошибка декомпрессии XZ блока #{chunk_index}: {e}")
            
        offset = xz_end
        chunk_index += 1

    if not unpacked_chunks:
        raise ValueError("Сжатые данные не найдены или повреждены")

    # 5. Склейка внутреннего AOTA
    inner_container = b''.join(unpacked_chunks)
    inner_path = os.path.join(output_dir, "inner_aota_container.bin")
    
    with open(inner_path, 'wb') as out_f:
        out_f.write(inner_container)
        
    print(f"    [+] Сформирован внутренний монолит (inner_aota_container.bin): {len(inner_container)} байт")
    return inner_path


def main():
    parser = argparse.ArgumentParser(description="Полная рекурсивная распаковка прошивки Actions ATS3085S")
    parser.add_argument("input_file", help="Путь к оригинальному файлу OTA (.bin)")
    parser.add_argument("--save-chunks", action="store_true", help="Опционально: сохранить промежуточные XZ-чанки на диск")
    args = parser.parse_args()

    base_name = os.path.splitext(os.path.basename(args.input_file))[0]
    layer1_dir = f"{base_name}_extracted"
    
    print("\n" + "="*50)
    print(f"[*] ЭТАП 1: Распаковка внешнего контейнера (Layer 1)")
    print("="*50)
    layer1_files = parse_aota_container(args.input_file, layer1_dir)
    
    temp_bin_path = next((f for f in layer1_files if f.lower().endswith("temp.bin")), None)
    if not temp_bin_path:
        print("\n[!] TEMP.bin не найден. Распаковка внутренних слоев не требуется.")
        sys.exit(0)

    layer2_dir = os.path.join(layer1_dir, "TEMP_extracted")
    
    print("\n" + "="*50)
    print(f"[*] ЭТАП 2: Анализ ядра и декомпрессия TEMP.bin (Layer 2)")
    print("="*50)
    inner_aota_path = parse_temp_boot_image(temp_bin_path, layer2_dir, save_chunks=args.save_chunks)

    layer3_dir = os.path.join(layer2_dir, "inner_aota_extracted")
    
    print("\n" + "="*50)
    print(f"[*] ЭТАП 3: Распаковка внутреннего контейнера AOTA (Layer 3)")
    print("="*50)
    layer3_files = parse_aota_container(inner_aota_path, layer3_dir)
    
    app_bin_path = next((f for f in layer3_files if f.lower().endswith("app.bin")), None)
    
    print("\n" + "="*50)
    print("[SUCCESS] Полная распаковка успешно завершена!")
    if app_bin_path:
        print(f"[*] Целевой файл для реверс-инжиниринга: {app_bin_path}")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()