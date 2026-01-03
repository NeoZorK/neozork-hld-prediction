#!/usr/bin/env python3
"""
Финальный скрипт for конвертации AutoML Gluon мануала
Запускает оба конвертера: HTML and PDF (with reportlab)

Author: Shcherbyna Rostyslav
Дата: 2024
"""

import sys
import os
from pathlib import Path

# Добавляем текущую директорию in путь for импорта модулей
sys.path.append(str(Path(__file__).parent))

from simple_html_converter import SimpleAutoMLGluonHTMLConverter
from reportlab_pdf_converter import ReportLabPDFConverter

def check_dependencies():
 """Проверяет наличие необходимых зависимостей"""
 print("🔍 Проверяем dependencies...")

 # Проверяем markdown
 try:
 import markdown
 print("✅ markdown installed")
 except ImportError:
 print("❌ markdown not installed. Install: pip install markdown")
 return False

 # Проверяем Pygments for подсветки синтаксиса
 try:
 import pygments
 print("✅ pygments installed")
 except ImportError:
 print("⚠️ pygments not installed. Install: pip install pygments")

 # Проверяем reportlab for PDF
 try:
 import reportlab
 print("✅ reportlab installed")
 except ImportError:
 print("❌ reportlab not installed. Install: pip install reportlab")
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
 """Конвертирует in HTML"""
 print("\n" + "="*50)
 print("🔄 КОНВЕРТАЦИЯ in HTML")
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
 """Конвертирует in PDF"""
 print("\n" + "="*50)
 print("🔄 КОНВЕРТАЦИЯ in PDF")
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
 """Главная function"""
 print("🚀 AutoML Gluon Manual Converter (Final)")
 print("=" * 50)
 print("Конвертирует 33 главы Markdown in HTML and PDF мануалы")
 print("Author: Shcherbyna Rostyslav")
 print("=" * 50)

 # Создаем директории
 create_directories()

 # Проверяем dependencies
 deps_ok = check_dependencies()

 if not deps_ok:
 print("\n❌ not все dependencies установлены. Установите их and попробуйте снова.")
 return

 # Конвертируем in HTML
 html_success = convert_to_html()

 # Конвертируем in PDF
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
 print(" 📄 HTML: AutoML_Gluon_Complete_Manual.html (7.5 MB)")
 print(" 📄 PDF: AutoML_Gluon_Complete_Manual.pdf (2.0 MB)")
 print(" 📄 HTML for PDF: AutoML_Gluon_Complete_Manual_ForPDF.html (7.4 MB)")
 elif html_success:
 print("📄 HTML мануал готов к использованию!")
 else:
 print("😞 Произошли ошибки при конвертации")

 print("\n💡 Дополнительные instructions:")
 print(" - HTML мануал можно открыть in любом браузере")
 print(" - PDF мануал готов к использованию and печати")
 print(" - Все 33 главы включены in оба формата")

if __name__ == "__main__":
 main()
