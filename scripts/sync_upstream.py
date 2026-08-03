import os
import urllib.request
import zipfile
import shutil
import tempfile

# Конфигурация
REPO_ZIP_URL = "https://github.com/glyphix-os/web-docs/archive/refs/heads/main.zip"
TARGET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "original_docs"))

def sync_chinese_docs():
    """
    Скачивает актуальные исходники Glyphix, фильтрует VuePress/i18n мусор 
    и обновляет локальную директорию original_docs.
    """
    print("[*] Запуск синхронизации с Upstream репозиторием...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "web-docs.zip")
        
        # 1. Скачивание актуального среза
        print(f"[*] Скачивание архива: {REPO_ZIP_URL}")
        try:
            urllib.request.urlretrieve(REPO_ZIP_URL, zip_path)
        except Exception as e:
            print(f"[!] Ошибка скачивания: {e}")
            return

        # 2. Распаковка во временную директорию
        print("[*] Распаковка архива...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            
        # Папка внутри архива по умолчанию имеет постфикс -main
        extracted_src = os.path.join(temp_dir, "web-docs-main", "src")
        
        if not os.path.exists(extracted_src):
            print("[!] Ошибка: директория 'src' не найдена в архиве.")
            return

        # 3. Очистка текущей директории original_docs (если существует)
        if os.path.exists(TARGET_DIR):
            print(f"[*] Очистка локальной директории {TARGET_DIR}...")
            shutil.rmtree(TARGET_DIR)
            
        # 4. Копирование только папки src (игнорируем корень с i18n и package.json)
        print("[*] Копирование документации...")
        shutil.copytree(extracted_src, TARGET_DIR)
        
        # 5. Принудительное удаление .vuepress из новых данных
        vuepress_path = os.path.join(TARGET_DIR, ".vuepress")
        if os.path.exists(vuepress_path):
            shutil.rmtree(vuepress_path)
            print("[*] Директория .vuepress удалена (оптимизация контекста LLM).")

        print("[+] Синхронизация успешно завершена.")

if __name__ == "__main__":
    sync_chinese_docs()