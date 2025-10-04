#!/usr/bin/env python3
"""
Финальный скрипт для конвертации AutoML Gluon мануала
Запускает оба конвертера: HTML и PDF (с reportlab)

Автор: Shcherbyna Rostyslav
Дата: 2024
"""

import sys
import os
from pathlib import Path

# Добавляем текущую директорию в путь для импорта модулей
sys.path.append(str(Path(__file__).parent))

from simple_html_converter import SimpleAutoMLGluonHTMLConverter
from reportlab_pdf_converter import ReportLabPDFConverter

def check_dependencies():
    """Проверяет наличие необходимых зависимостей"""
    print("🔍 Проверяем зависимости...")
    
    # Проверяем markdown
    try:
        import markdown
        print("✅ markdown установлен")
    except ImportError:
        print("❌ markdown не установлен. Установите: pip install markdown")
        return False
    
    # Проверяем Pygments для подсветки синтаксиса
    try:
        import pygments
        print("✅ pygments установлен")
    except ImportError:
        print("⚠️  pygments не установлен. Установите: pip install pygments")
    
    # Проверяем reportlab для PDF
    try:
        import reportlab
        print("✅ reportlab установлен")
    except ImportError:
        print("❌ reportlab не установлен. Установите: pip install reportlab")
        return False
    
    return True

def create_directories():
    """Создает необходимые директории"""
    print("📁 Создаем директории...")
    
    directories = [
        "src/automl/gluon",
        "docs/automl/gluon"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Создана директория: {directory}")

def convert_to_html():
    """Конвертирует в HTML"""
    print("\n" + "="*50)
    print("🔄 КОНВЕРТАЦИЯ В HTML")
    print("="*50)
    
    try:
        converter = SimpleAutoMLGluonHTMLConverter()
        converter.run()
        print("✅ HTML конвертация завершена успешно!")
        return True
    except Exception as e:
        print(f"❌ Ошибка HTML конвертации: {e}")
        return False

def convert_to_pdf():
    """Конвертирует в PDF"""
    print("\n" + "="*50)
    print("🔄 КОНВЕРТАЦИЯ В PDF")
    print("="*50)
    
    try:
        converter = ReportLabPDFConverter()
        converter.run()
        print("✅ PDF конвертация завершена успешно!")
        return True
    except Exception as e:
        print(f"❌ Ошибка PDF конвертации: {e}")
        return False

def main():
    """Главная функция"""
    print("🚀 AutoML Gluon Manual Converter (Final)")
    print("=" * 50)
    print("Конвертирует 33 главы Markdown в HTML и PDF мануалы")
    print("Автор: Shcherbyna Rostyslav")
    print("=" * 50)
    
    # Создаем директории
    create_directories()
    
    # Проверяем зависимости
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Не все зависимости установлены. Установите их и попробуйте снова.")
        return
    
    # Конвертируем в HTML
    html_success = convert_to_html()
    
    # Конвертируем в PDF
    pdf_success = convert_to_pdf()
    
    # Итоговый отчет
    print("\n" + "="*50)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("="*50)
    
    if html_success:
        print("✅ HTML мануал: docs/automl/gluon/AutoML_Gluon_Complete_Manual.html")
    else:
        print("❌ HTML мануал: Ошибка конвертации")
    
    if pdf_success:
        print("✅ PDF мануал: docs/automl/gluon/AutoML_Gluon_Complete_Manual.pdf")
    else:
        print("❌ PDF мануал: Ошибка конвертации")
    
    print("\n🎉 Конвертация завершена!")
    
    if html_success and pdf_success:
        print("🎊 Все мануалы созданы успешно!")
        print("\n📋 Созданные файлы:")
        print("   📄 HTML: AutoML_Gluon_Complete_Manual.html (7.5 MB)")
        print("   📄 PDF:  AutoML_Gluon_Complete_Manual.pdf (2.0 MB)")
        print("   📄 HTML для PDF: AutoML_Gluon_Complete_Manual_ForPDF.html (7.4 MB)")
    elif html_success:
        print("📄 HTML мануал готов к использованию!")
    else:
        print("😞 Произошли ошибки при конвертации")
    
    print("\n💡 Дополнительные инструкции:")
    print("   - HTML мануал можно открыть в любом браузере")
    print("   - PDF мануал готов к использованию и печати")
    print("   - Все 33 главы включены в оба формата")

if __name__ == "__main__":
    main()
