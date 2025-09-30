#!/usr/bin/env python3
"""
Скрипт для создания PDF учебника AutoML Gluon с рабочими ссылками
"""

import os
import subprocess
import sys
from pathlib import Path

def create_combined_markdown():
    """Создание объединенного Markdown файла"""
    
    # Путь к директории с файлами
    docs_dir = Path(__file__).parent
    
    # Порядок файлов для объединения
    files_order = [
        "README.md",
        "01_installation.md", 
        "02_basic_usage.md",
        "03_advanced_configuration.md",
        "04_metrics.md",
        "05_validation.md",
        "06_production.md",
        "07_retraining.md",
        "08_best_practices.md",
        "09_examples.md",
        "10_troubleshooting.md",
        "11_apple_silicon_optimization.md"
    ]
    
    # Создание объединенного файла
    combined_content = []
    
    for filename in files_order:
        file_path = docs_dir / filename
        
        if file_path.exists():
            print(f"Добавляем файл: {filename}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Добавление разделителя между файлами
                if combined_content:
                    combined_content.append("\n\n---\n\n")
                
                # Добавление содержимого файла
                combined_content.append(content)
        else:
            print(f"Файл не найден: {filename}")
    
    # Сохранение объединенного файла
    combined_file = docs_dir / "AutoML_Gluon_Complete_Manual.md"
    
    with open(combined_file, 'w', encoding='utf-8') as f:
        f.write(''.join(combined_content))
    
    print(f"Создан объединенный файл: {combined_file}")
    return combined_file

def create_pdf_with_links(markdown_file):
    """Создание PDF с рабочими ссылками"""
    
    # Команда pandoc для создания PDF с ссылками
    cmd = [
        'pandoc',
        str(markdown_file),
        '-o', 'AutoML_Gluon_Complete_Manual.pdf',
        '--pdf-engine=xelatex',
        '--toc',  # Содержание
        '--toc-depth=3',  # Глубина содержания
        '--number-sections',  # Нумерация разделов
        '--linkcolor=blue',  # Цвет ссылок
        '--urlcolor=blue',
        '--toccolor=blue',
        '--geometry=margin=2cm',  # Отступы
        '--fontsize=11pt',
        '--documentclass=book',
        '--chapters',  # Разделение на главы
        '--variable', 'colorlinks=true',
        '--variable', 'linkcolor=blue',
        '--variable', 'urlcolor=blue',
        '--variable', 'toccolor=blue',
        '--variable', 'book=true',
        '--variable', 'documentclass=book',
        '--variable', 'geometry:margin=2cm',
        '--variable', 'fontsize=11pt',
        '--variable', 'linestretch=1.2',
        '--variable', 'papersize=a4',
        '--variable', 'colorlinks=true',
        '--variable', 'linkcolor=blue',
        '--variable', 'urlcolor=blue',
        '--variable', 'toccolor=blue',
        '--variable', 'book=true',
        '--variable', 'documentclass=book',
        '--variable', 'geometry:margin=2cm',
        '--variable', 'fontsize=11pt',
        '--variable', 'linestretch=1.2',
        '--variable', 'papersize=a4'
    ]
    
    print("Создание PDF с помощью pandoc...")
    print(f"Команда: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("PDF успешно создан!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании PDF: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def create_simple_pdf(markdown_file):
    """Создание простого PDF без сложных настроек"""
    
    # Простая команда pandoc
    cmd = [
        'pandoc',
        str(markdown_file),
        '-o', 'AutoML_Gluon_Complete_Manual.pdf',
        '--toc',
        '--number-sections',
        '--pdf-engine=wkhtmltopdf',
        '--css', 'style.css'
    ]
    
    print("Создание простого PDF...")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("PDF успешно создан!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании PDF: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def create_html_first(markdown_file):
    """Создание HTML версии сначала"""
    
    # Создание HTML
    html_cmd = [
        'pandoc',
        str(markdown_file),
        '-o', 'AutoML_Gluon_Complete_Manual.html',
        '--toc',
        '--number-sections',
        '--standalone',
        '--css', 'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-light.min.css',
        '--metadata', 'title="AutoML Gluon - Полное руководство"',
        '--metadata', 'author="AutoML Gluon Manual"',
        '--metadata', 'date="2024"'
    ]
    
    print("Создание HTML версии...")
    
    try:
        result = subprocess.run(html_cmd, check=True, capture_output=True, text=True)
        print("HTML успешно создан!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании HTML: {e}")
        return False

def main():
    """Основная функция"""
    
    print("=== Создание PDF учебника AutoML Gluon ===")
    
    # Создание объединенного Markdown файла
    markdown_file = create_combined_markdown()
    
    if not markdown_file.exists():
        print("Ошибка: не удалось создать объединенный файл")
        return False
    
    # Попытка создания PDF с разными методами
    print("\n=== Попытка 1: Создание PDF с XeLaTeX ===")
    if create_pdf_with_links(markdown_file):
        print("PDF создан успешно с XeLaTeX!")
        return True
    
    print("\n=== Попытка 2: Создание простого PDF ===")
    if create_simple_pdf(markdown_file):
        print("PDF создан успешно с wkhtmltopdf!")
        return True
    
    print("\n=== Попытка 3: Создание HTML версии ===")
    if create_html_first(markdown_file):
        print("HTML версия создана успешно!")
        print("Можно использовать браузер для печати в PDF")
        return True
    
    print("Не удалось создать PDF. Проверьте установку pandoc и LaTeX.")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
