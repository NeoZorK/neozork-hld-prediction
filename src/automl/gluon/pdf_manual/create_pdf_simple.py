#!/usr/bin/env python3
"""
Простое создание PDF через браузер
Использует системные возможности для создания PDF

Автор: Shcherbyna Rostyslav
Дата: 2024
"""

import os
import subprocess
from pathlib import Path

def create_pdf_simple():
    """Создание PDF простым способом"""
    
    # Пути к файлам
    script_dir = Path(__file__).parent
    # Переходим к корню проекта
    project_root = script_dir.parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    # Отладочная информация
    print(f"Script dir: {script_dir}")
    print(f"Project root: {project_root}")
    print(f"Docs dir: {docs_dir}")
    print(f"Docs dir exists: {docs_dir.exists()}")
    
    # Если путь неправильный, используем абсолютный путь
    if not docs_dir.exists():
        docs_dir = Path("/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon")
        print(f"Используем абсолютный путь: {docs_dir}")
        print(f"Docs dir exists: {docs_dir.exists()}")
    
    html_file = docs_dir / "AutoML_Gluon_Complete_Manual_Enhanced.html"
    output_pdf = docs_dir / "AutoML_Gluon_Complete_Manual.pdf"
    
    print("=== Создание PDF простым способом ===")
    print(f"HTML файл: {html_file}")
    print(f"Выходной PDF: {output_pdf}")
    
    if not html_file.exists():
        print(f"✗ HTML файл не найден: {html_file}")
        return False
    
    try:
        # Попытка 1: Используем wkhtmltopdf если доступен
        print("Попытка 1: wkhtmltopdf...")
        try:
            result = subprocess.run([
                'wkhtmltopdf',
                '--page-size', 'A4',
                '--margin-top', '1cm',
                '--margin-right', '1cm',
                '--margin-bottom', '1cm',
                '--margin-left', '1cm',
                '--encoding', 'UTF-8',
                '--print-media-type',
                str(html_file),
                str(output_pdf)
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✓ PDF создан с wkhtmltopdf: {output_pdf}")
                return True
            else:
                print(f"wkhtmltopdf ошибка: {result.stderr}")
        except FileNotFoundError:
            print("wkhtmltopdf не найден")
        except subprocess.TimeoutExpired:
            print("wkhtmltopdf timeout")
        
        # Попытка 2: Используем Chrome/Chromium
        print("Попытка 2: Chrome/Chromium...")
        chrome_paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
            '/usr/bin/google-chrome',
            '/usr/bin/chromium-browser'
        ]
        
        chrome_path = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_path = path
                break
        
        if chrome_path:
            try:
                result = subprocess.run([
                    chrome_path,
                    '--headless',
                    '--disable-gpu',
                    '--print-to-pdf=' + str(output_pdf),
                    '--print-to-pdf-no-header',
                    '--run-all-compositor-stages-before-draw',
                    '--virtual-time-budget=5000',
                    str(html_file)
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0 and output_pdf.exists():
                    print(f"✓ PDF создан с Chrome: {output_pdf}")
                    return True
                else:
                    print(f"Chrome ошибка: {result.stderr}")
            except subprocess.TimeoutExpired:
                print("Chrome timeout")
        else:
            print("Chrome/Chromium не найден")
        
        # Попытка 3: Используем Safari (macOS)
        print("Попытка 3: Safari...")
        try:
            # Создаем AppleScript для Safari
            applescript = f'''
            tell application "Safari"
                activate
                open location "file://{html_file.absolute()}"
                delay 3
                tell application "System Events"
                    keystroke "p" using command down
                    delay 1
                    keystroke "s" using command down
                    delay 1
                    keystroke "{output_pdf.name}"
                    delay 1
                    keystroke return
                end tell
            end tell
            '''
            
            result = subprocess.run([
                'osascript', '-e', applescript
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✓ PDF создан с Safari: {output_pdf}")
                return True
            else:
                print(f"Safari ошибка: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("Safari timeout")
        
        print("✗ Не удалось создать PDF автоматически")
        return False
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False

def main():
    print("=== Создание PDF учебника AutoML Gluon (простой способ) ===")
    print("Автор: Shcherbyna Rostyslav")
    print("Дата: 2024")
    
    success = create_pdf_simple()
    
    if success:
        print("\n🎉 PDF учебник успешно создан!")
        print("Файл готов к использованию.")
    else:
        print("\n⚠️  Не удалось создать PDF автоматически.")
        print("Попробуйте:")
        print("1. Откройте HTML файл в браузере")
        print("2. Нажмите Cmd+P (печать)")
        print("3. Выберите 'Сохранить как PDF'")
        print("4. Настройте параметры и сохраните")

if __name__ == "__main__":
    main()
