#!/usr/bin/env python3
"""
<<<<<<< HEAD
Финальный скрипт для конвертации AutoML Gluon мануала
Запускает оба конвертера: HTML и PDF (с reportlab)

Автор: Shcherbyna Rostyslav
Дата: 2024
=======
Final script for AutoML Gloon Manual conversion
Launch both converters: HTML and PDF (with Reportlab)

Author: Shcherbyna Rostyslav
Date: 2024
>>>>>>> origin/master
"""

import sys
import os
from pathlib import Path

<<<<<<< HEAD
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
=======
# Add the current directory in the path for Import modules
sys.path.append(str(Path(__file__).parent))

from simple_html_converter import SimpleAutoMLGluonHTMLConverter
from Reportlab_pdf_converter import ReportLabPDFConverter

def check_dependencies():
"Corresponds to "presence requerd dependencies""
 print("🔍 checking dependencies...")

 # checking markdown
 try:
 import markdown
 print("✅ markdown installed")
 except importError:
 print("❌ markdown not installed. install: pip install markdown")
 return False

# Sheking Pygments for Syntax Illumination
 try:
 import pygments
 print("✅ pygments installed")
 except importError:
 print("⚠️ pygments not installed. install: pip install pygments")

 # checking Reportlab for PDF
 try:
 import Reportlab
 print("✅ Reportlab installed")
 except importError:
 print("❌ Reportlab not installed. install: pip install Reportlab")
 return False

 return True

def create_directories():
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"preint("\\Creating Directory...")

 directories = [
 "src/automl/gluon",
 "docs/automl/gluon"
 ]

 for directory in directories:
 Path(directory).mkdir(parents=True, exist_ok=True)
Prent(f) is created by the directory: {directory})

def convert_to_html():
""Converted in TML""
 print("\n" + "="*50)
"Prent("\CONVERTATION IN HTML")
 print("="*50)

 try:
 converter = SimpleAutoMLGluonHTMLConverter()
 converter.run()
Print("\HTML conversion successfully completed!')
 return True
 except Exception as e:
Print(f"\\HTML conversion: {e}})
 return False

def convert_to_pdf():
""Converted in PDF""
 print("\n" + "="*50)
"In PDF CONVERTATION"
 print("="*50)

 try:
 converter = ReportLabPDFConverter()
 converter.run()
The conversion has been successfully completed!
 return True
 except Exception as e:
pint(f"\pDF conversion request: {e}})
 return False

def main():
""The Main Function""
 print("🚀 AutoML Gluon Manual Converter (Final)")
 print("=" * 50)
Print("Converts 33 chapters of Markdown in TML and PDF manuals")
 print("Author: Shcherbyna Rostyslav")
 print("=" * 50)

# Creating Directorates
 create_directories()

 # checking dependencies
 deps_ok = check_dependencies()

 if not deps_ok:
Install them and try again.
 return

# Converging in HTML
 html_success = convert_to_html()

# Converging in PDF
 pdf_success = convert_to_pdf()

# Final Report
 print("\n" + "="*50)
Prent((("Total Report")
 print("="*50)

 if html_success:
Print("\HTML manual: docs/automl/gluon/AutuML_Gluon_Complete_Manual.html")
 else:
Print("\HTML manual: conversion error")

 if pdf_success:
pint("\PDF manual: docs/automl/gluon/AutuML_Gluon_Complete_Manual.pdf")
 else:
Print("\PDF manual: conversion error")

Print("\n\\\\\\\\\\\}Convergence complete!}

 if html_success and pdf_success:
"All manuals have been successfully created!"
Print('n'\\\\\\\\\\\\\\\\Prodata files:}
 print(" 📄 HTML: AutoML_Gluon_Complete_Manual.html (7.5 MB)")
 print(" 📄 PDF: AutoML_Gluon_Complete_Manual.pdf (2.0 MB)")
 print(" 📄 HTML for PDF: AutoML_Gluon_Complete_Manual_ForPDF.html (7.4 MB)")
 elif html_success:
Print("\HTML manual ready for use!")
 else:
Print(''\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\((((((((\((((((\(\

print('\n\\\\\\ additional instruments: )
Print("-HTML Manual can be opened in any browser)
print(" - PDF manual ready for use and printing)
"-All 33 chapters are included in both formats")

if __name__ == "__main__":
 main()
>>>>>>> origin/master
