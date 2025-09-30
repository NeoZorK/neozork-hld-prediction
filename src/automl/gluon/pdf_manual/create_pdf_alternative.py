#!/usr/bin/env python3
"""
Альтернативный скрипт для создания PDF учебника AutoML Gluon
Использует HTML как промежуточный формат
"""

import os
import subprocess
import sys
from pathlib import Path
import webbrowser

def create_html_with_links():
    """Создание HTML с рабочими ссылками"""
    
    docs_dir = Path(__file__).parent
    markdown_file = docs_dir / "AutoML_Gluon_Complete_Manual.md"
    
    if not markdown_file.exists():
        print("Файл AutoML_Gluon_Complete_Manual.md не найден!")
        return False
    
    # Создание HTML с улучшенными ссылками
    html_cmd = [
        'pandoc',
        str(markdown_file),
        '-o', 'AutoML_Gluon_Complete_Manual.html',
        '--toc',
        '--number-sections',
        '--standalone',
        '--css', 'style.css',
        '--metadata', 'title="AutoML Gluon - Полное руководство"',
        '--metadata', 'author="AutoML Gluon Manual"',
        '--metadata', 'date="2024"',
        '--toc-depth=3',
        '--section-divs',
        '--id-prefix=section-'
    ]
    
    print("Создание HTML с рабочими ссылками...")
    
    try:
        result = subprocess.run(html_cmd, check=True, capture_output=True, text=True)
        print("HTML успешно создан!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании HTML: {e}")
        return False

def create_enhanced_html():
    """Создание улучшенного HTML с JavaScript для навигации"""
    
    html_file = Path("AutoML_Gluon_Complete_Manual.html")
    
    if not html_file.exists():
        print("HTML файл не найден!")
        return False
    
    # Чтение HTML файла
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Добавление JavaScript для улучшенной навигации
    enhanced_html = html_content.replace(
        '</head>',
        '''
        <script>
        // Функция для плавной прокрутки к якорям
        function smoothScrollTo(target) {
            const element = document.querySelector(target);
            if (element) {
                element.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
        
        // Обработка кликов по ссылкам
        document.addEventListener('DOMContentLoaded', function() {
            const links = document.querySelectorAll('a[href^="#"]');
            links.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = this.getAttribute('href');
                    smoothScrollTo(target);
                });
            });
        });
        
        // Функция для печати в PDF
        function printToPDF() {
            window.print();
        }
        
        // Добавление кнопки печати
        document.addEventListener('DOMContentLoaded', function() {
            const printButton = document.createElement('button');
            printButton.innerHTML = '🖨️ Печать в PDF';
            printButton.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1000;
                background: #3498db;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
            `;
            printButton.onclick = printToPDF;
            document.body.appendChild(printButton);
        });
        </script>
        <style>
        @media print {
            body { font-size: 12pt; line-height: 1.4; }
            h1, h2, h3, h4, h5, h6 { page-break-after: avoid; }
            pre, code { page-break-inside: avoid; }
            a { color: #000; text-decoration: none; }
            a[href^="http"]:after { content: " (" attr(href) ")"; font-size: 0.8em; color: #666; }
        }
        </style>
        </head>
        '''
    )
    
    # Сохранение улучшенного HTML
    enhanced_file = Path("AutoML_Gluon_Complete_Manual_Enhanced.html")
    with open(enhanced_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_html)
    
    print(f"Создан улучшенный HTML: {enhanced_file}")
    return enhanced_file

def create_pdf_via_browser():
    """Создание PDF через браузер (инструкция)"""
    
    print("\n=== Инструкция по созданию PDF ===")
    print("1. Откройте файл AutoML_Gluon_Complete_Manual_Enhanced.html в браузере")
    print("2. Нажмите Ctrl+P (или Cmd+P на Mac)")
    print("3. В настройках печати выберите 'Сохранить как PDF'")
    print("4. Настройте параметры:")
    print("   - Размер: A4")
    print("   - Поля: Стандартные")
    print("   - Масштаб: 100%")
    print("   - Включить фон")
    print("5. Сохраните как AutoML_Gluon_Complete_Manual.pdf")
    
    # Попытка открыть файл в браузере
    try:
        enhanced_file = Path("AutoML_Gluon_Complete_Manual_Enhanced.html")
        if enhanced_file.exists():
            webbrowser.open(f"file://{enhanced_file.absolute()}")
            print(f"\nФайл открыт в браузере: {enhanced_file.absolute()}")
    except Exception as e:
        print(f"Не удалось открыть файл в браузере: {e}")

def create_simple_pdf():
    """Попытка создать простой PDF"""
    
    markdown_file = Path("AutoML_Gluon_Complete_Manual.md")
    
    if not markdown_file.exists():
        print("Markdown файл не найден!")
        return False
    
    # Простая команда pandoc
    cmd = [
        'pandoc',
        str(markdown_file),
        '-o', 'AutoML_Gluon_Complete_Manual.pdf',
        '--toc',
        '--number-sections',
        '--standalone'
    ]
    
    print("Попытка создания простого PDF...")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("PDF создан успешно!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании PDF: {e}")
        return False

def main():
    """Основная функция"""
    
    print("=== Альтернативное создание PDF учебника AutoML Gluon ===")
    
    # Создание HTML с ссылками
    if not create_html_with_links():
        print("Ошибка при создании HTML!")
        return False
    
    # Создание улучшенного HTML
    enhanced_file = create_enhanced_html()
    
    if enhanced_file:
        print(f"Создан улучшенный HTML файл: {enhanced_file}")
        
        # Инструкция по созданию PDF
        create_pdf_via_browser()
        
        return True
    
    # Попытка создать простой PDF
    if create_simple_pdf():
        print("PDF создан успешно!")
        return True
    
    print("Не удалось создать PDF автоматически.")
    print("Используйте HTML версию для создания PDF через браузер.")
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
