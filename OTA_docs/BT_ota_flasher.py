import asyncio
import struct
import zlib
import os
import argparse
from bleak import BleakClient, BleakError

OTA_DATA_UUID = "e49a25e0-f69a-11e8-8eb2-f2801f1b9fd1"
OTA_NOTIFY_UUID = "e49a28e1-f69a-11e8-8eb2-f2801f1b9fd1"
OTA_CTRL_UUID = "26078ae1-dfe6-4657-9427-178458b911a1"

PRE_HANDSHAKE_CMDS = [
    bytes.fromhex("5500a400afbe010000000000"),
    bytes.fromhex("5500a500afbe010000000000"),
    bytes.fromhex("5500a600afbe010000000000"),
    bytes.fromhex("5500a7001680000000000000")
]

CMD_OTA_REQUEST = bytes.fromhex("0901804300012000312e30305f3236303232383137303300000000000000000000000000000000000202000000031000000000000000000000000000000000000401000009010001")
CMD_OTA_START = bytes.fromhex("0902800000")
CMD_OTA_SET_PARAMS = bytes.fromhex("090980040001010001")
CMD_OTA_END = bytes.fromhex("0906800000")

PAGE_SIZE = 1024
MAX_CHUNK = 230

# Глобальные примитивы синхронизации
init_event = asyncio.Event()
# Семафор на 5 пакетов (Размер скользящего окна AtkDfuController)
window_semaphore = asyncio.Semaphore(5)

def ota_notification_handler(sender, data):
    """
    Единый роутер входящих пакетов от часов.
    Распознает ответы на инициализацию и потоковые ACK.
    """
    if len(data) >= 2 and data[0] == 0x09:
        if data[1] in [0x01, 0x02, 0x09]:
            # Это ответ на REQUEST, START или SET_PARAMS
            init_event.set()
        else:
            # Это ответ на Data Chunk (часы обработали пакет).
            # Освобождаем место в скользящем окне для отправки следующего пакета.
            try:
                window_semaphore.release()
            except ValueError:
                pass # Защита от переполнения семафора

def build_ota_packets(firmware_bytes):
    packets = []
    total_size = len(firmware_bytes)
    for page_offset in range(0, total_size, PAGE_SIZE):
        page_data = firmware_bytes[page_offset : page_offset + PAGE_SIZE]
        seq_id = 0
        for chunk_offset in range(0, len(page_data), MAX_CHUNK):
            chunk_data = page_data[chunk_offset : chunk_offset + MAX_CHUNK]
            chunk_crc = zlib.crc32(chunk_data) & 0xFFFFFFFF
            crc_bytes = struct.pack('<I', chunk_crc)
            payload_len = 1 + 4 + len(chunk_data)
            header = struct.pack('<BBB H B', 0x09, 0x0b, 0x80, payload_len, seq_id)
            packets.append(header + crc_bytes + chunk_data)
            seq_id += 1
    return packets

async def flash_firmware(mac_address, file_path):
    if not os.path.exists(file_path):
        print(f"[-] Файл не найден: {file_path}")
        return

    with open(file_path, 'rb') as f:
        firmware_bytes = f.read()

    print(f"[*] Подготовка данных: {len(firmware_bytes)} байт...")
    packets = build_ota_packets(firmware_bytes)

    async with BleakClient(mac_address) as client:
        if not client.is_connected:
            print("[-] Ошибка подключения.")
            return

        print("[+] Подписка на канал Flow Control (e49a28e1)...")
        await client.start_notify(OTA_NOTIFY_UUID, ota_notification_handler)

        print("[+] Выполнение Pre-Handshake (Write Request)...")
        # Управляющие команды MAS отправляем надежным Write Request, как вы и сказали
        for cmd in PRE_HANDSHAKE_CMDS:
            await client.write_gatt_char(OTA_CTRL_UUID, cmd, response=True)

        print("[+] Инициализация AOTA сеанса (Ожидание ответов)...")
        
        # 1. REQUEST
        init_event.clear()
        await client.write_gatt_char(OTA_DATA_UUID, CMD_OTA_REQUEST, response=False)
        await asyncio.wait_for(init_event.wait(), timeout=5.0)
        
        # 2. START
        init_event.clear()
        await client.write_gatt_char(OTA_DATA_UUID, CMD_OTA_START, response=False)
        await asyncio.wait_for(init_event.wait(), timeout=5.0)

        # 3. SET_PARAMS
        init_event.clear()
        await client.write_gatt_char(OTA_DATA_UUID, CMD_OTA_SET_PARAMS, response=False)
        await asyncio.wait_for(init_event.wait(), timeout=5.0)

        print("[+] Начинаем заливку прошивки (Sliding Window = 5)...")
        total_packets = len(packets)
        
        try:
            for i, packet in enumerate(packets):
                # Блокируемся, если в полете уже 5 пакетов и нет подтверждений
                await window_semaphore.acquire()
                
                # Выстреливаем пакет в эфир
                await client.write_gatt_char(OTA_DATA_UUID, packet, response=False)
                
                # НИКАКИХ SLEEP! Скорость регулируется аппаратно часами.
                if i % 500 == 0 and i > 0:
                    percent = (i / total_packets) * 100
                    print(f"    Прогресс: {i}/{total_packets} пакетов ({percent:.1f}%)")
                    
        except BleakError as e:
            print(f"\n[-] Разрыв соединения на пакете {i}: {e}")
            return
        finally:
            await client.stop_notify(OTA_NOTIFY_UUID)

        print("[+] Передача завершена. Отправка Reboot...")
        await client.write_gatt_char(OTA_DATA_UUID, CMD_OTA_END, response=True)
        print("[*] Успешно! Прошивка записана.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mac", help="MAC-адрес смарт-часов")
    parser.add_argument("file", help="Путь к файлу прошивки (.bin)")
    args = parser.parse_args()
    asyncio.run(flash_firmware(args.mac, args.file))