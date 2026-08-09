import os
import sys
import struct
import zlib
import argparse
import re

SECTOR_SIZE = 512
CANONICAL_ORDER = ["ota.xml", "TEMP.bin", "sdfs_a.bin", "sdfs_k.bin"]
SERVICE_FILES = ["version.txt"]

def align_offset(offset):
    """Выравнивание смещения вверх до границы 512-байтового сектора."""
    return (offset + SECTOR_SIZE - 1) & ~(SECTOR_SIZE - 1)

def patch_ota_xml(xml_content, build_ver, platform_id, file_metadata):
    """
    Безопасное обновление ota.xml с сохранением оригинального форматирования
    и исходных символов переноса строк (CRLF / LF).
    """
    # 1. Обновляем версию и платформу
    xml_content = re.sub(r'<version_name>.*?</version_name>', f'<version_name>{build_ver}</version_name>', xml_content)
    xml_content = re.sub(r'<board_name>.*?</board_name>', f'<board_name>{platform_id}</board_name>', xml_content)

    # 2. Изолированная обработка каждого блока <partition>
    def partition_replacer(match):
        block = match.group(0)
        
        name_match = re.search(r'<file_name>(.*?)</file_name>', block)
        if not name_match:
            return block
            
        fname = name_match.group(1)
        
        if fname in file_metadata:
            meta = file_metadata[fname]
            physical_size = meta['size']
            physical_crc = meta['crc']
            
            # Извлекаем старый физический размер из XML
            old_size_match = re.search(r'<file_size>(.*?)</file_size>', block)
            if old_size_match:
                old_file_size = int(old_size_match.group(1), 16)
                
                # Если физический размер совпадает, сохраняем оригинальный блок (включая orig_size и checksum)
                if physical_size == old_file_size:
                    return block
            
            size_hex = hex(physical_size)
            crc_hex = f"0x{physical_crc:08x}"
            
            block = re.sub(r'<file_size>.*?</file_size>', f'<file_size>{size_hex}</file_size>', block)
            block = re.sub(r'<orig_size>.*?</orig_size>', f'<orig_size>{size_hex}</orig_size>', block)
            block = re.sub(r'<checksum>.*?</checksum>', f'<checksum>{crc_hex}</checksum>', block)
                
        return block

    xml_content = re.sub(r'<partition>.*?</partition>', partition_replacer, xml_content, flags=re.DOTALL)

    return xml_content
def pack_aota(input_dir, output_file, build_ver=None, platform_id=None):
    if not os.path.isdir(input_dir):
        print(f"[!] Ошибка: Каталог {input_dir} не существует.")
        sys.exit(1)

    # --- ЧТЕНИЕ КОНФИГУРАЦИИ ---
    ver_file_path = os.path.join(input_dir, "version.txt")
    file_build_ver, file_platform_id = None, None

    if os.path.exists(ver_file_path):
        with open(ver_file_path, "r", encoding="utf-8") as vf:
            for line in vf:
                line = line.strip()
                if line.startswith("build_ver="):
                    file_build_ver = line.split("=", 1)[1]
                elif line.startswith("platform_id="):
                    file_platform_id = line.split("=", 1)[1]

    build_ver = build_ver or file_build_ver or "1.00_2602281703"
    platform_id = platform_id or file_platform_id or "A5S10GLY"

    print(f"[*] Используется версия   : {build_ver}")
    print(f"[*] Используется платформа: {platform_id}")

    # --- ПОДГОТОВКА СПИСКА ФАЙЛОВ ---
    all_files = os.listdir(input_dir)
    file_list = []
    
    for f in all_files:
        is_service = any(f.lower() == sf.lower() for sf in SERVICE_FILES)
        if not is_service and os.path.isfile(os.path.join(input_dir, f)):
            file_list.append(f)

    # --- ЭТАП 1: ЗАГРУЗКА PAYLOAD В ПАМЯТЬ И РАСЧЕТ ДАННЫХ ---
    files_data = {}
    file_metadata = {}

    for filename in file_list:
        if filename.lower() == "ota.xml":
            continue # Пропускаем ota.xml, обработаем его позже
            
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'rb') as f:
            data = f.read()
            
        files_data[filename] = data
        file_metadata[filename] = {
            'size': len(data),
            'crc': zlib.crc32(data) & 0xFFFFFFFF
        }

    # --- ЭТАП 2: ДИНАМИЧЕСКИЙ ПАТЧИНГ ota.xml ---
    ota_xml_name = next((f for f in file_list if f.lower() == "ota.xml"), None)
    if not ota_xml_name:
        print("[!] Ошибка: ota.xml не найден в каталоге.")
        sys.exit(1)

    # Открытие с newline='' предотвращает автоматическую конвертацию \r\n в \n
    with open(os.path.join(input_dir, ota_xml_name), 'r', encoding='utf-8', newline='') as f:
        xml_content = f.read()

    print("[*] Динамическое обновление ota.xml...")
    xml_content = patch_ota_xml(xml_content, build_ver, platform_id, file_metadata)
    
    # Кодирование сохраняет исходную байтовую структуру CRLF
    ota_data = xml_content.encode('utf-8')
    files_data[ota_xml_name] = ota_data

    # --- ЭТАП 3: СБОРКА ТАБЛИЦЫ FAT И ВЫРАВНИВАНИЕ PAYLOAD ---
    final_file_list = []
    for c_file in CANONICAL_ORDER:
        for f in file_list:
            if f.lower() == c_file.lower():
                final_file_list.append(f)
                break
    for f in sorted(file_list):
        if f not in final_file_list:
            final_file_list.append(f)

    fat_entries = bytearray()
    payload = bytearray()
    current_offset = 0x0400

    print(f"\n[*] Структура контейнера:")
    for filename in final_file_list:
        data = files_data[filename]
        file_size = len(data)
        file_crc = zlib.crc32(data) & 0xFFFFFFFF
        
        filename_b = filename.encode('ascii').ljust(16, b'\x00')[:16]
        fat_entries += struct.pack('<16sIIII', filename_b, current_offset, file_size, 0, file_crc)
        
        payload += data
        aligned_sz = align_offset(file_size)
        pad_size = aligned_sz - file_size
        payload += b'\x00' * pad_size
        
        print(f" -> {filename:<12} | Off: 0x{current_offset:08X} | Size: {file_size:<7} B | Pad: {pad_size:<3} B | CRC32: 0x{file_crc:08X}")
        current_offset += aligned_sz

    total_file_size = current_offset
    fat_sector = fat_entries.ljust(SECTOR_SIZE, b'\x00')

    # --- ЭТАП 4: ФИНАЛЬНЫЕ КОНТРОЛЬНЫЕ СУММЫ И СБОРКА ---
    payload_checksum = zlib.crc32(payload) & 0xFFFFFFFF

    header = bytearray(SECTOR_SIZE)
    header[0:4]   = b'AOTA'
    header[4:8]   = b'\x00\x00\x00\x00'                 # Placeholder
    header[8:12]  = b'\x00\x01\x00\x04'                 # Flags
    header[12:16] = struct.pack('<I', len(final_file_list)) # File Count
    header[16:18] = b'\x00\x02'                         # FAT Offset
    header[18:20] = b'\x00\x04'                         # Data Offset
    header[20:24] = struct.pack('<I', total_file_size)  # Total Size
    header[24:28] = struct.pack('<I', payload_checksum) # Payload Checksum
    
    header[0x40:0x60] = build_ver.encode('ascii').ljust(32, b'\x00')[:32]
    header[0x60:0x7E] = platform_id.encode('ascii').ljust(30, b'\x00')[:30]
    
    header[0x7E:0x80] = b'\x01\x00'
    header[0x80:0x84] = b'\x00\x00\x00\x01'

    # Точный расчет CRC32 для заголовка
    crc_data_block = header[8:] + fat_sector
    header_checksum = zlib.crc32(crc_data_block) & 0xFFFFFFFF
    header[4:8] = struct.pack('<I', header_checksum)

    with open(output_file, 'wb') as out_f:
        out_f.write(header)
        out_f.write(fat_sector)
        out_f.write(payload)

    print(f"\n[SUCCESS] Сборка успешно завершена: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Каталог с извлеченными файлами")
    parser.add_argument("output_file", help="Итоговый файл .bin")
    parser.add_argument("--ver", default=None, help="Переопределить версию")
    parser.add_argument("--platform", default=None, help="Переопределить платформу")

    args = parser.parse_args()
    pack_aota(args.input_dir, args.output_file, args.ver, args.platform)