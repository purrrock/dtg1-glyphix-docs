import os
import glob
import hashlib
import time
from google import genai
from google.genai import types

# Конфигурация путей
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src", "original_docs", "src")
TRANSL_DIR = os.path.join(BASE_DIR, "src", "transl")

# Настройка API Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("[!] Ошибка: Переменная окружения GEMINI_API_KEY не задана.")
    exit(1)

client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-3.6-flash"

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

def translate_text(text, target_lang):
    """Отправляет запрос к Gemini API."""
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPTS[target_lang],
                temperature=0.1 # Низкая температура для строгого перевода без фантазий
            )
        )
        return response.text
    except Exception as e:
        print(f"[!] Ошибка API при переводе на {target_lang}: {e}")
        return None

def process_translation():
    # Файл для хранения хешей уже переведенных файлов
    hash_db_path = os.path.join(BASE_DIR, "scripts", ".translation_hashes.txt")
    processed_hashes = {}
    
    if os.path.exists(hash_db_path):
        with open(hash_db_path, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    path, fhash = line.strip().split(":", 1)
                    processed_hashes[path] = fhash

    search_pattern = os.path.join(SRC_DIR, "**", "*.md")
    md_files = glob.glob(search_pattern, recursive=True)
    
    new_hashes = {}
    files_translated = 0

    for filepath in md_files:
        # Игнорируем старую папку 'en' в оригинальных исходниках
        if "\\en\\" in filepath or "/en/" in filepath:
            continue

        rel_path = os.path.relpath(filepath, SRC_DIR)
        current_hash = get_file_hash(filepath)
        
        # Проверка, изменился ли файл с прошлого перевода
        if rel_path in processed_hashes and processed_hashes[rel_path] == current_hash:
            new_hashes[rel_path] = current_hash
            continue

        print(f"[*] Перевод файла: {rel_path}")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        if not content.strip():
            new_hashes[rel_path] = current_hash
            continue

        # Перевод на оба языка
        for lang in ["EN", "RU"]:
            translated_content = translate_text(content, lang)
            
            if translated_content:
                out_filepath = os.path.join(TRANSL_DIR, lang, rel_path)
                os.makedirs(os.path.dirname(out_filepath), exist_ok=True)
                
                with open(out_filepath, "w", encoding="utf-8") as out_f:
                    out_f.write(translated_content)
                    
            # Rate limiting Google API (15 RPM для бесплатного тарифа)
            time.sleep(4) 
            
        new_hashes[rel_path] = current_hash
        files_translated += 1

    # Сохраняем новые хеши
    with open(hash_db_path, "w", encoding="utf-8") as f:
        for path, fhash in new_hashes.items():
            f.write(f"{path}:{fhash}\n")
            
    print(f"[+] Перевод завершен. Переведено файлов: {files_translated}")

if __name__ == "__main__":
    process_translation()