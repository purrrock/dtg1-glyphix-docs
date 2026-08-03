import os
import glob
import hashlib
import time
import sys
from google import genai
from google.genai import types

# Конфигурация путей
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src", "original_docs")
TRANSL_DIR = os.path.join(BASE_DIR, "src", "transl")

# Настройка API Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("[!] Ошибка: Переменная окружения GEMINI_API_KEY не задана.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-3.5-flash-lite"

SYSTEM_PROMPTS = {
    "EN": "You are a technical documentation translator. Translate the following Markdown text from Chinese to English. Preserve all Markdown formatting, code blocks, URLs, and tables exactly as they are. Do not translate code variables or API function names.",
    "RU": "Ты профессиональный технический переводчик. Переведи следующий Markdown текст с китайского на русский язык. Сохрани всё форматирование Markdown, блоки кода, ссылки и таблицы. Не переводи названия переменных, функций API и системные пути."
}

def get_file_hash(filepath):
    """Вычисляет MD5 хеш файла."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def translate_text(text, target_lang, max_retries=3):
    """Отправляет запрос к Gemini API с механизмом повторных попыток (Retry)."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPTS[target_lang],
                    temperature=0.1
                )
            )
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            
            # Принудительный дамп сырого ответа API для отладки
            print(f"\n[RAW API ERROR DUMP - {target_lang}]:\n{error_msg}")
            
            # Обработка ошибки лимита запросов (Rate Limit / Quota)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                wait_time = 30 * (attempt + 1)
                print(f"[*] Перехват 429. Ожидание {wait_time} сек. (Попытка {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
                
            print(f"[!] Непредвиденная ошибка API ({target_lang}). Отмена для файла.")
            return None
            
    print(f"\n[!] Исчерпаны попытки перевода для языка {target_lang}.")
    return None

def process_translation():
    hash_db_path = os.path.join(BASE_DIR, "scripts", ".translation_hashes.txt")
    processed_hashes = {}
    
    # Загрузка старых хешей
    if os.path.exists(hash_db_path):
        with open(hash_db_path, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    path, fhash = line.strip().split(":", 1)
                    processed_hashes[path] = fhash

    # Инициализируем новую базу хешей копией старой (чтобы не потерять уже переведенное при сбое)
    new_hashes = processed_hashes.copy()

    search_pattern = os.path.join(SRC_DIR, "**", "*.md")
    md_files = glob.glob(search_pattern, recursive=True)
    
    files_to_translate = []
    
    for filepath in md_files:
        if "\\en\\" in filepath or "/en/" in filepath:
            continue
            
        rel_path = os.path.relpath(filepath, SRC_DIR).replace("\\", "/")
        current_hash = get_file_hash(filepath)
        
        if rel_path in processed_hashes and processed_hashes[rel_path] == current_hash:
            continue
            
        files_to_translate.append((filepath, rel_path, current_hash))

    total_files = len(files_to_translate)
    
    if total_files == 0:
        print("[*] Все файлы уже переведены. Обновление не требуется.")
        return

    print(f"[*] Найдено файлов для перевода: {total_files}")
    files_translated = 0
    has_critical_error = False

    for idx, (filepath, rel_path, current_hash) in enumerate(files_to_translate, 1):
        print(f"[{idx}/{total_files}] Чтение: {rel_path}...", end=" ", flush=True)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        if not content.strip():
            print("Пустой файл. Пропуск.")
            new_hashes[rel_path] = current_hash
            continue

        print("\n  -> Перевод EN: ", end="", flush=True)
        en_content = translate_text(content, "EN")
        if not en_content:
            has_critical_error = True
            break
            
        out_filepath_en = os.path.join(TRANSL_DIR, "EN", rel_path)
        os.makedirs(os.path.dirname(out_filepath_en), exist_ok=True)
        with open(out_filepath_en, "w", encoding="utf-8") as out_f:
            out_f.write(en_content)
        print("OK", end="", flush=True)
        
        time.sleep(6) # Увеличенный Rate limit
        
        print(" | Перевод RU: ", end="", flush=True)
        ru_content = translate_text(content, "RU")
        if not ru_content:
            has_critical_error = True
            break
            
        out_filepath_ru = os.path.join(TRANSL_DIR, "RU", rel_path)
        os.makedirs(os.path.dirname(out_filepath_ru), exist_ok=True)
        with open(out_filepath_ru, "w", encoding="utf-8") as out_f:
            out_f.write(ru_content)
        print("OK", flush=True)
            
        time.sleep(6) # Увеличенный Rate limit
            
        # Записываем хеш ТОЛЬКО если обе транзакции (EN и RU) прошли успешно
        new_hashes[rel_path] = current_hash
        files_translated += 1

    # Сохраняем хеши на диск (включая старые успешные и новые переведенные до момента ошибки)
    with open(hash_db_path, "w", encoding="utf-8") as f:
        for path, fhash in new_hashes.items():
            f.write(f"{path}:{fhash}\n")
            
    print(f"\n[+] Процесс завершен. Успешно переведено: {files_translated}/{total_files} файлов.")

    # Если скрипт прервался с ошибкой API, крашим CI/CD
    if has_critical_error:
        print("[!] Конвейер прерван из-за ошибок API. Прогресс сохранен.")
        sys.exit(1)

if __name__ == "__main__":
    process_translation()