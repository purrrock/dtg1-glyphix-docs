import os
import sys
import struct
import zlib

def unpack_aota(file_path):
    """
    Парсер и распаковщик главного контейнера Actions OTA (AOTA).
    Извлекает файлы и сохраняет метаданные версии в version.txt.
    """
    if not os.path.exists(file_path):
        print(f"[!] Ошибка: Файл {file_path} не найден.")
        return

    # Формирование имени целевого каталога
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = f"{base_name}_extracted"
    
    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] Целевая директория: {output_dir}")

    with open(file_path, 'rb') as f:
        # 1. Чтение Root Header (512 байт)
        header = f.read(512)
        magic, checksum_main, flags, file_count, fat_offset, data_offset = struct.unpack('<4sIIIHH', header[:20])
        
        if magic != b'AOTA':
            print(f"[!] Критическая ошибка: Неверная сигнатура {magic}. Ожидается 'AOTA'.")
            sys.exit(1)
            
        # ------------------------------------------------------------------
        # Извлечение метаданных версии и платформы из заголовка
        # 0x40..0x5F: build_ver (32 байта, null-terminated)
        # 0x60..0x7D: platform_id (30 байт, null-terminated)
        # ------------------------------------------------------------------
        build_ver_raw = header[0x40:0x60].split(b'\x00')[0]
        platform_id_raw = header[0x60:0x7E].split(b'\x00')[0]
        
        build_ver = build_ver_raw.decode('ascii', errors='ignore')
        platform_id = platform_id_raw.decode('ascii', errors='ignore')

        # Запись метаданных в version.txt внутри созданного каталога
        ver_file_path = os.path.join(output_dir, "version.txt")
        with open(ver_file_path, "w", encoding="utf-8") as vf:
            vf.write(f"build_ver={build_ver}\n")
            vf.write(f"platform_id={platform_id}\n")
            
        print(f"[*] Версия прошивки: {build_ver}")
        print(f"[*] Идентификатор платформы: {platform_id}")
        print(f"[*] Метаданные сохранены в: {ver_file_path}\n")
        # ------------------------------------------------------------------

        print(f"[*] AOTA Контейнер обнаружен (Flags: 0x{flags:08X})")
        print(f"[*] Количество файлов (FAT): {file_count}")
        print(f"[*] Смещение FAT: 0x{fat_offset:04X} | Начало данных: 0x{data_offset:04X}\n")

        # 2. Парсинг File Allocation Table (FAT)
        f.seek(fat_offset)
        for i in range(file_count):
            fat_entry = f.read(32)
            if len(fat_entry) < 32:
                print(f"[!] Ошибка: Неожиданный конец FAT-таблицы на записи {i}")
                break
                
            name_b, file_offset, file_size, _, file_crc = struct.unpack('<16sIIII', fat_entry)
            filename = name_b.split(b'\x00')[0].decode('ascii')
            
            print(f" -> {filename:<12} | Offset: 0x{file_offset:08X} | Size: {file_size:<7} байт |", end="")
            
            current_fat_pos = f.tell()
            
            # 3. Переход к данным и извлечение
            f.seek(file_offset)
            payload = f.read(file_size)
            
            actual_crc = zlib.crc32(payload) & 0xFFFFFFFF
            if actual_crc != file_crc:
                print(f" [CRC ERROR: Ожидался 0x{file_crc:08X}, получен 0x{actual_crc:08X}]")
            else:
                print(" [CRC OK]")
                
            out_path = os.path.join(output_dir, filename)
            with open(out_path, 'wb') as out_f:
                out_f.write(payload)
            
            f.seek(current_fat_pos)
            
    print("\n[SUCCESS] Распаковка и генерация version.txt завершены.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python aota_unpacker.py <путь_к_файлу.bin>")
        sys.exit(1)
        
    unpack_aota(sys.argv[1])