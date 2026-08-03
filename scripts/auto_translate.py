import os
import glob
import hashlib
import time
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
    exit(1)

client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-2.5-flash"

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
                temperature=0.1
            )
        )
        return response.text
    except Exception as e:
        print(f"\n[!] Ошибка API при переводе на {target_lang}: {e}")
        return None

def process_translation():
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
    
    # Предварительный проход: определяем, какие файлы действительно нуждаются в переводе
    files_to_translate = []
    new_hashes = {}
    
    for filepath in md_files:
        if "\\en\\" in filepath or "/en/" in filepath:
            continue
            
        rel_path = os.path.relpath(filepath, SRC_DIR).replace("\\", "/")
        current_hash = get_file_hash(filepath)
        
        if rel_path in processed_hashes and processed_hashes[rel_path] == current_hash:
            new_hashes[rel_path] = current_hash
            continue
            
        files_to_translate.append((filepath, rel_path, current_hash))

    total_files = len(files_to_translate)
    
    if total_files == 0:
        print("[*] Все файлы уже переведены. Обновление не требуется.")
        return

    print(f"[*] Найдено файлов для перевода: {total_files}")
    
    files_translated = 0

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
        if en_content:
            out_filepath = os.path.join(TRANSL_DIR, "EN", rel_path)
            os.makedirs(os.path.dirname(out_filepath), exist_ok=True)
            with open(out_filepath, "w", encoding="utf-8") as out_f:
                out_f.write(en_content)
            print("OK", end="", flush=True)
        
        time.sleep(4) # Rate limit
        
        print(" | Перевод RU: ", end="", flush=True)
        ru_content = translate_text(content, "RU")
        if ru_content:
            out_filepath = os.path.join(TRANSL_DIR, "RU", rel_path)
            os.makedirs(os.path.dirname(out_filepath), exist_ok=True)
            with open(out_filepath, "w", encoding="utf-8") as out_f:
                out_f.write(ru_content)
            print("OK", flush=True)
            
        time.sleep(4) # Rate limit
            
        new_hashes[rel_path] = current_hash
        files_translated += 1

    # Сохраняем новые хеши
    with open(hash_db_path, "w", encoding="utf-8") as f:
        for path, fhash in new_hashes.items():
            f.write(f"{path}:{fhash}\n")
            
    print(f"\n[+] Процесс завершен. Успешно переведено: {files_translated}/{total_files} файлов.")

if __name__ == "__main__":
    process_translation()