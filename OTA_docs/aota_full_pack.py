import os
import sys
import struct
import zlib
import lzma
import argparse
import re

SECTOR_SIZE = 512
CANONICAL_ORDER = ["ota.xml", "TEMP.bin", "sdfs_a.bin", "sdfs_k.bin", "app.bin"]
SERVICE_FILES = ["version.txt", "TEMP_extracted"]

# C-структуры заголовков (Little-Endian)
ACTIONS_BOOT_HEADER_FMT = '<8sIIIIIIII'
ACTIONS_BOOT_HEADER_SIZE = struct.calcsize(ACTIONS_BOOT_HEADER_FMT)

ACTIONS_LZMA_HEADER_FMT = '<4sIII'
ACTIONS_LZMA_HEADER_SIZE = struct.calcsize(ACTIONS_LZMA_HEADER_FMT)

ACTIONS_BOOT_MAGIC = b'ACTHHTCA'
ACTIONS_LZMA_MAGIC = b'LZMA\x10\x00\x00\x00'

CHUNK_SIZE_LIMIT = 0x200000

def align_offset(offset):
    """Выравнивание смещения вверх до границы 512-байтового сектора."""
    return (offset + SECTOR_SIZE - 1) & ~(SECTOR_SIZE - 1)

def patch_ota_xml(xml_content, build_ver, platform_id, file_metadata):
    """
    Безопасное обновление ota.xml с сохранением оригинального форматирования
    и исходных символов переноса строк (CRLF / LF).
    """
    xml_content = re.sub(r'<version_name>.*?</version_name>', f'<version_name>{build_ver}</version_name>', xml_content)
    xml_content = re.sub(r'<board_name>.*?</board_name>', f'<board_name>{platform_id}</board_name>', xml_content)

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
            
            old_size_match = re.search(r'<file_size>(.*?)</file_size>', block)
            if old_size_match:
                old_file_size = int(old_size_match.group(1), 16)
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
        return False

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

    print(f"    [*] Используется версия   : {build_ver}")
    print(f"    [*] Используется платформа: {platform_id}")

    all_files = os.listdir(input_dir)
    file_list = []
    
    for f in all_files:
        is_service = any(f.lower() == sf.lower() for sf in SERVICE_FILES)
        if not is_service and os.path.isfile(os.path.join(input_dir, f)):
            file_list.append(f)

    files_data = {}
    file_metadata = {}

    for filename in file_list:
        if filename.lower() == "ota.xml":
            continue
            
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'rb') as f:
            data = f.read()
            
        files_data[filename] = data
        file_metadata[filename] = {
            'size': len(data),
            'crc': zlib.crc32(data) & 0xFFFFFFFF
        }

    ota_xml_name = next((f for f in file_list if f.lower() == "ota.xml"), None)
    if not ota_xml_name:
        print(f"[!] Ошибка: ota.xml не найден в каталоге {input_dir}.")
        return False

    with open(os.path.join(input_dir, ota_xml_name), 'r', encoding='utf-8', newline='') as f:
        xml_content = f.read()

    xml_content = patch_ota_xml(xml_content, build_ver, platform_id, file_metadata)
    ota_data = xml_content.encode('utf-8')
    files_data[ota_xml_name] = ota_data

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
        
        print(f"        -> {filename:<12} | Off: 0x{current_offset:08X} | Size: {file_size:<7} B | Pad: {pad_size:<3} B | CRC32: 0x{file_crc:08X}")
        current_offset += aligned_sz

    total_file_size = current_offset
    fat_sector = fat_entries.ljust(SECTOR_SIZE, b'\x00')

    payload_checksum = zlib.crc32(payload) & 0xFFFFFFFF

    header = bytearray(SECTOR_SIZE)
    header[0:4]   = b'AOTA'
    header[4:8]   = b'\x00\x00\x00\x00'
    header[8:12]  = b'\x00\x01\x00\x04'
    header[12:16] = struct.pack('<I', len(final_file_list))
    header[16:18] = b'\x00\x02'
    header[18:20] = b'\x00\x04'
    header[20:24] = struct.pack('<I', total_file_size)
    header[24:28] = struct.pack('<I', payload_checksum)
    
    header[0x40:0x60] = build_ver.encode('ascii').ljust(32, b'\x00')[:32]
    header[0x60:0x7E] = platform_id.encode('ascii').ljust(30, b'\x00')[:30]
    
    header[0x7E:0x80] = b'\x01\x00'
    header[0x80:0x84] = b'\x00\x00\x00\x01'

    crc_data_block = header[8:] + fat_sector
    header_checksum = zlib.crc32(crc_data_block) & 0xFFFFFFFF
    header[4:8] = struct.pack('<I', header_checksum)

    with open(output_file, 'wb') as out_f:
        out_f.write(header)
        out_f.write(fat_sector)
        out_f.write(payload)

    return True

def compress_and_pack_temp(input_dir, output_file):
    if not os.path.exists(input_dir):
        print(f"[-] Ошибка: Входной каталог '{input_dir}' не найден.")
        return False

    hdr_path = os.path.join(input_dir, "actions_boot_header.bin")
    if not os.path.exists(hdr_path):
        print(f"[-] Ошибка: Заголовок '{hdr_path}' не найден.")
        return False

    with open(hdr_path, 'rb') as f_hdr:
        boot_hdr = bytearray(f_hdr.read())

    if len(boot_hdr) == 36:
        boot_hdr += struct.pack('<I', 0x00000200)
    elif len(boot_hdr) != ACTIONS_BOOT_HEADER_SIZE:
        print(f"[-] Ошибка: Некорректный размер заголовка.")
        return False

    stub_path = os.path.join(input_dir, "boot_stub.bin")
    if not os.path.exists(stub_path):
        print(f"[-] Ошибка: Файл '{stub_path}' не найден.")
        return False

    with open(stub_path, 'rb') as f_stub:
        boot_stub = f_stub.read()

    if boot_stub.startswith(ACTIONS_BOOT_MAGIC):
        boot_stub = boot_stub[ACTIONS_BOOT_HEADER_SIZE:]

    monolith_path = os.path.join(input_dir, "inner_aota_container.bin")
    if not os.path.exists(monolith_path):
        print(f"[-] Ошибка: Файл монолита '{monolith_path}' не найден.")
        return False

    with open(monolith_path, 'rb') as f_mono:
        monolith_data = f_mono.read()

    monolith_size = len(monolith_data)
    payload_blocks = b''
    offset = 0
    chunk_index = 1

    while offset < monolith_size:
        chunk_slice = monolith_data[offset : offset + CHUNK_SIZE_LIMIT]
        uncomp_size = len(chunk_slice)
        xz_compressed = lzma.compress(chunk_slice, format=lzma.FORMAT_XZ)
        comp_size = len(xz_compressed)

        print(f"    [+] Сжат чанк #{chunk_index}: RAM 0x{uncomp_size:X} -> XZ 0x{comp_size:X} байт")

        lzma_hdr = struct.pack(
            ACTIONS_LZMA_HEADER_FMT,
            b'LZMA',
            ACTIONS_LZMA_HEADER_SIZE,
            comp_size,
            uncomp_size
        )

        payload_blocks += lzma_hdr + xz_compressed
        offset += uncomp_size
        chunk_index += 1

    final_data = bytes(boot_hdr) + boot_stub + payload_blocks

    with open(output_file, 'wb') as f_out:
        f_out.write(final_data)

    return True

def main():
    parser = argparse.ArgumentParser(description="Полная сборка прошивки Actions ATS3085S (Outer + TEMP.bin + Inner)")
    parser.add_argument("input_dir", help="Корневой каталог извлеченной прошивки (например: firmware_extracted)")
    parser.add_argument("output_file", help="Имя итогового файла (например: custom_ota.bin)")
    args = parser.parse_args()

    base_dir = os.path.normpath(args.input_dir)
    layer2_dir = os.path.join(base_dir, "TEMP_extracted")
    layer3_dir = os.path.join(layer2_dir, "inner_aota_extracted")

    print(f"\n" + "="*60)
    print(f"[*] ЭТАП 1: Сборка внутреннего ядра (Layer 3 -> Layer 2)")
    print("="*60)
    
    if os.path.exists(layer3_dir):
        inner_container_path = os.path.join(layer2_dir, "inner_aota_container.bin")
        if pack_aota(layer3_dir, inner_container_path):
            print(f"[+] Внутренний контейнер успешно собран.")
        else:
            print(f"[-] Ошибка сборки внутреннего контейнера.")
            sys.exit(1)
    else:
        print("[!] Каталог Layer 3 не найден. Используем существующий inner_aota_container.bin")

    print(f"\n" + "="*60)
    print(f"[*] ЭТАП 2: Сжатие и сборка загрузчика TEMP.bin (Layer 2 -> Layer 1)")
    print("="*60)

    if os.path.exists(layer2_dir):
        temp_bin_path = os.path.join(base_dir, "TEMP.bin")
        if compress_and_pack_temp(layer2_dir, temp_bin_path):
            print(f"[+] Загрузочный образ TEMP.bin успешно обновлен.")
        else:
            print(f"[-] Ошибка сборки TEMP.bin.")
            sys.exit(1)
    else:
        print("[!] Каталог Layer 2 не найден. Используем существующий TEMP.bin")

    print(f"\n" + "="*60)
    print(f"[*] ЭТАП 3: Финальная сборка внешнего AOTA-контейнера (Layer 1)")
    print("="*60)

    if pack_aota(base_dir, args.output_file):
        print(f"\n[SUCCESS] Прошивка полностью собрана и готова к прошивке!")
        print(f"Файл: {os.path.abspath(args.output_file)}")
    else:
        print(f"\n[-] Ошибка финальной сборки.")
        sys.exit(1)

if __name__ == "__main__":
    main()