#!/usr/bin/env python3
"""
Создание PDF через браузер (простой способ)
Автоматически открывает HTML и создает PDF

Автор: NeoZorK (Shcherbyna Rostyslav)
Дата: 2025
"""

import os
import subprocess
import webbrowser
import time
from pathlib import Path

def create_pdf_via_browser():
    """Создание PDF через браузер"""
    
    print("=== Создание PDF через браузер ===")
    print("Автор: NeoZorK (Shcherbyna Rostyslav)")
    print("Дата: 2025")
    
    # Определение путей
    project_root = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    html_file = docs_dir / "AutoML_Gluon_Complete_Manual_Enhanced.html"
    pdf_file = docs_dir / "AutoML_Gluon_Complete_Manual.pdf"
    
    print(f"HTML файл: {html_file}")
    print(f"Выходной PDF: {pdf_file}")
    
    if not html_file.exists():
        print(f"✗ HTML файл не найден: {html_file}")
        return False
    
    # Открываем HTML в браузере
    print("🌐 Открываем HTML в браузере...")
    webbrowser.open(f"file://{html_file.absolute()}")
    
    print("\n" + "="*60)
    print("📋 ИНСТРУКЦИЯ ПО СОЗДАНИЮ PDF:")
    print("="*60)
    print("1. В открывшемся браузере нажмите Cmd+P (Mac) или Ctrl+P (Windows/Linux)")
    print("2. В настройках печати выберите 'Сохранить как PDF'")
    print("3. Настройте параметры:")
    print("   - Размер: A4")
    print("   - Поля: Стандартные")
    print("   - Масштаб: 100%")
    print("   - Включить фон: ✅")
    print("   - Включить заголовки и колонтитулы: ❌")
    print("4. Сохраните как: AutoML_Gluon_Complete_Manual.pdf")
    print("5. Сохраните в папку: docs/automl/gluon/")
    print("="*60)
    
    # Ждем немного
    print("\n⏳ Ждем 3 секунды...")
    time.sleep(3)
    
    print("\n✅ HTML файл открыт в браузере!")
    print("📄 Следуйте инструкции выше для создания PDF")
    
    return True

def create_pdf_with_chrome_headless():
    """Создание PDF с помощью Chrome в headless режиме"""
    
    print("\n=== Альтернативный способ: Chrome Headless ===")
    
    # Проверяем наличие Chrome
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "google-chrome",
        "chromium-browser"
    ]
    
    chrome_cmd = None
    for path in chrome_paths:
        if os.path.exists(path) or subprocess.run(['which', path.split('/')[-1]], capture_output=True).returncode == 0:
            chrome_cmd = path
            break
    
    if not chrome_cmd:
        print("✗ Chrome не найден")
        return False
    
    # Определение путей
    project_root = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    html_file = docs_dir / "AutoML_Gluon_Complete_Manual_Enhanced.html"
    pdf_file = docs_dir / "AutoML_Gluon_Complete_Manual.pdf"
    
    print(f"Chrome: {chrome_cmd}")
    print(f"HTML: {html_file}")
    print(f"PDF: {pdf_file}")
    
    # Команда для создания PDF
    cmd = [
        chrome_cmd,
        "--headless",
        "--disable-gpu",
        "--print-to-pdf=" + str(pdf_file.absolute()),
        "--print-to-pdf-no-header",
        f"file://{html_file.absolute()}"
    ]
    
    print("🔄 Создание PDF с помощью Chrome...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ PDF создан успешно!")
            print(f"📄 Файл: {pdf_file}")
            return True
        else:
            print(f"✗ Ошибка: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Таймаут при создании PDF")
        return False
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Создание PDF руководства AutoML Gluon")
    print("Автор: NeoZorK (Shcherbyna Rostyslav)")
    print("Дата: 2025")
    print("Местоположение: Ukraine, Zaporizhzhya")
    
    # Пробуем Chrome headless сначала
    if create_pdf_with_chrome_headless():
        print("\n🎉 PDF создан автоматически!")
    else:
        print("\n🔄 Переходим к ручному способу...")
        create_pdf_via_browser()
