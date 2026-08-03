import os
import glob

# =====================================================================
# Конфигурация путей
# =====================================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
OUTPUT_DIR = os.path.join(BASE_DIR, "ai_context")
RE_DELTAS_DIR = os.path.join(SRC_DIR, "re_deltas")

# Маршрутизация исходных текстов по языкам
LANGUAGES = {
    "ZH": os.path.join(SRC_DIR, "original_docs", "src"),
    "EN": os.path.join(SRC_DIR, "transl", "EN"),
    "RU": os.path.join(SRC_DIR, "transl", "RU")
}

# Маппинг целевых файлов контекста на поддиректории с Markdown
MAPPING = {
    "01_glyphix_framework_core": ["framework"],
    "02_glyphix_ui_components": ["components"],                   # Только строгие спецификации UI-атомов
    "03_glyphix_system_api": ["api"],
    "04_glyphix_CxxDev": ["cxxdev"],
    "05_glyphix_tutorials": ["tutorials", "cookbook"],            # Объединенная база обучающих примеров и рецептов
    # 06_glyphix_hardware_deltas_and_undoc_funcs собирается статично из re_deltas
    # 07_glyphix_toolchain_pkg может быть добавлен в маппинг при появлении исходников
}

SEPARATOR = "=" * 60 + "\nFILE_PATH: {file_path}\n\n"
SYSTEM_PROMPT = "# Context File: {filename}\nОграничения среды: MCU (No DOM), RTOS Zephyr, аппаратная платформа ATS3085S.\n\n"

def build_context():
    """
    Основной конвейер сборки контекста. Проходит по всем зарегистрированным
    языкам, собирает спецификации из поддиректорий и подмешивает результаты
    реверс-инжиниринга.
    """
    for lang_code, lang_src_dir in LANGUAGES.items():
        lang_out_dir = os.path.join(OUTPUT_DIR, lang_code)
        os.makedirs(lang_out_dir, exist_ok=True)
        
        # Если папки с переводами пока нет (например, RU пуста), пропускаем
        if not os.path.exists(lang_src_dir):
            continue

        print(f"[*] Сборка контекста для локали: {lang_code}")

        # Шаг 1: Агрегация документации фреймворка (Файлы 01 - 05)
        for out_prefix, src_subdirs in MAPPING.items():
            out_filename = f"{out_prefix}_{lang_code}.md"
            out_filepath = os.path.join(lang_out_dir, out_filename)
            
            with open(out_filepath, "w", encoding="utf-8") as outfile:
                outfile.write(SYSTEM_PROMPT.format(filename=out_filename))
                
                for subdir in src_subdirs:
                    target_scan_dir = os.path.join(lang_src_dir, subdir)
                    if not os.path.exists(target_scan_dir):
                        continue
                        
                    # Рекурсивный поиск .md файлов
                    search_pattern = os.path.join(target_scan_dir, "**", "*.md")
                    for filepath in glob.glob(search_pattern, recursive=True):
                        # Фильтр: Игнорируем старый английский перевод в ветке ZH
                        if lang_code == "ZH" and "original_docs\\src\\en" in filepath:
                            continue
                            
                        append_file_to_context(filepath, outfile, BASE_DIR)

        # Шаг 2: Безусловная инъекция файлов реверс-инжиниринга (Файл 06)
        build_hardware_deltas(lang_out_dir, lang_code)

def build_hardware_deltas(out_dir, lang_code):
    """
    Формирует 06_glyphix_hardware_deltas_and_undoc_funcs_*.md
    Эти данные критически важны для AI и добавляются во все языковые ветки.
    """
    out_filename = f"06_glyphix_hardware_deltas_and_undoc_funcs_{lang_code}.md"
    out_filepath = os.path.join(out_dir, out_filename)
    
    if not os.path.exists(RE_DELTAS_DIR):
        print(f"[!] Директория {RE_DELTAS_DIR} не найдена. Пропуск дельт.")
        return

    print(f"  -> Сборка аппаратных дельт: {out_filename}")
    with open(out_filepath, "w", encoding="utf-8") as outfile:
        outfile.write(SYSTEM_PROMPT.format(filename=out_filename))
        outfile.write("> [REVERSE ENGINEERING FACTS]\n")
        
        search_pattern = os.path.join(RE_DELTAS_DIR, "**", "*.md")
        for filepath in glob.glob(search_pattern, recursive=True):
            append_file_to_context(filepath, outfile, BASE_DIR)

def append_file_to_context(filepath, outfile, base_dir):
    """
    Читает файл, нормализует путь и записывает его в итоговый дескриптор.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as infile:
            content = infile.read()
            
        if not content.strip():
            return
            
        # Нормализация пути для контекста (относительно корня репозитория)
        rel_path = os.path.relpath(filepath, base_dir).replace("\\", "/")
        outfile.write(SEPARATOR.format(file_path=rel_path))
        outfile.write(content)
        outfile.write("\n\n")
    except Exception as e:
        print(f"[!] Ошибка чтения {filepath}: {e}")

if __name__ == "__main__":
    build_context()
    print("[+] Генерация AI-контекста успешно завершена.")