import os
import sys
import struct
import zlib
import lzma
import argparse

# Константы структур
AOTA_MAGIC = b'AOTA'
ACT_BOOT_MAGIC = b'ACTHHTCA'
ACT_LZMA_MAGIC = b'LZMA\x10\x00\x00\x00'

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
            
        # Извлечение метаданных (актуально для внешнего и внутреннего контейнера)
        build_ver = header[0x40:0x60].split(b'\x00')[0].decode('ascii', errors='ignore')
        platform_id = header[0x60:0x7E].split(b'\x00')[0].decode('ascii', errors='ignore')

        with open(os.path.join(output_dir, "version.txt"), "w", encoding="utf-8") as vf:
            vf.write(f"build_ver={build_ver}\n")
            vf.write(f"platform_id={platform_id}\n")
            
        print(f"    [+] Версия: {build_ver} | Платформа: {platform_id}")
        
        # Парсинг FAT
        f.seek(fat_offset)
        extracted_files = []
        for i in range(file_count):
            fat_entry = f.read(32)
            if len(fat_entry) < 32: break
                
            name_b, file_offset, file_size, _, file_crc = struct.unpack('<16sIIII', fat_entry)
            filename = name_b.split(b'\x00')[0].decode('ascii')
            
            # Чтение полезной нагрузки файла
            current_pos = f.tell()
            f.seek(file_offset)
            payload = f.read(file_size)
            
            # Проверка целостности
            actual_crc = zlib.crc32(payload) & 0xFFFFFFFF
            status = "OK" if actual_crc == file_crc else "CRC_ERR"
            
            out_path = os.path.join(output_dir, filename)
            with open(out_path, 'wb') as out_f:
                out_f.write(payload)
                
            print(f"    [->] Извлечен: {filename:<14} | Размер: {file_size:<7} B | Статус: {status}")
            extracted_files.append(out_path)
            
            f.seek(current_pos)
            
    return extracted_files

def parse_temp_boot_image(temp_path, output_dir):
    """
    Парсер загрузочного образа Stage-2 (TEMP.bin).
    Разбирает заголовки, вырезает загрузчик и клеит XZ-чанки в памяти.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    with open(temp_path, 'rb') as f:
        # Чтение Boot Header
        header_data = f.read(40)
        if header_data[:8] != ACT_BOOT_MAGIC:
            raise ValueError("Неверная сигнатура TEMP.bin (ожидается ACTHHTCA)")
            
        with open(os.path.join(output_dir, "actions_boot_header.bin"), 'wb') as hf:
            hf.write(header_data)
            
        # Чтение Boot Stub (включая padding и IVT)
        f.seek(0x28)
        boot_stub_data = f.read(0x111E0 - 0x28)
        with open(os.path.join(output_dir, "boot_stub.bin"), 'wb') as bf:
            bf.write(boot_stub_data)
            
        print(f"    [+] Извлечены 'actions_boot_header.bin' и 'boot_stub.bin'")
        
        # Чтение сжатой зоны
        f.seek(0x111E0)
        compressed_payload = f.read()

    offset = 0
    chunk_index = 0
    unpacked_chunks = []
    
    while offset < len(compressed_payload):
        if offset + 16 > len(compressed_payload):
            break
            
        magic, header_sz, comp_sz, uncomp_sz = struct.unpack('<4sIII', compressed_payload[offset:offset+16])
        
        # Строгая проверка сигнатуры LZMA
        if compressed_payload[offset:offset+8] != ACT_LZMA_MAGIC:
            break
            
        xz_start = offset + 16
        xz_end = xz_start + comp_sz
        chunk_data = compressed_payload[xz_start:xz_end]
        
        try:
            unpacked = lzma.decompress(chunk_data)
            unpacked_chunks.append(unpacked)
            print(f"    [+] XZ Чанк #{chunk_index}: {comp_sz} B -> {len(unpacked)} B")
        except Exception as e:
            print(f"    [-] Ошибка декомпрессии XZ блока #{chunk_index}: {e}")
            
        offset = xz_end
        chunk_index += 1

    if not unpacked_chunks:
        raise ValueError("Сжатые данные не найдены внутри TEMP.bin")

    # Склейка внутреннего AOTA
    inner_container = b''.join(unpacked_chunks)
    inner_path = os.path.join(output_dir, "inner_aota_container.bin")
    
    with open(inner_path, 'wb') as out_f:
        out_f.write(inner_container)
        
    print(f"    [+] Сформирован внутренний монолит: {len(inner_container)} байт")
    return inner_path

def main():
    parser = argparse.ArgumentParser(description="Полная рекурсивная распаковка прошивки Actions ATS3085S")
    parser.add_argument("input_file", help="Путь к оригинальному файлу OTA (.bin)")
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
    inner_aota_path = parse_temp_boot_image(temp_bin_path, layer2_dir)

    layer3_dir = os.path.join(layer2_dir, "inner_aota_extracted")
    
    print("\n" + "="*50)
    print(f"[*] ЭТАП 3: Распаковка внутреннего контейнера AOTA (Layer 3)")
    print("="*50)
    layer3_files = parse_aota_container(inner_aota_path, layer3_dir)
    
    app_bin_path = next((f for f in layer3_files if f.lower().endswith("app.bin")), None)
    
    print("\n" + "="*50)
    print("[SUCCESS] Полная распаковка успешно завершена!")
    if app_bin_path:
        print(f"[*] Целевой файл для IDA/Ghidra: {app_bin_path}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()