#!/usr/bin/env python3
"""
Финальный скрипт для создания PDF учебника AutoML Gluon
Создает PDF с рабочими ссылками и навигацией

Автор: Shcherbyna Rostyslav
Дата: 2024
"""

import os
import subprocess
import sys
from pathlib import Path
import webbrowser
import time

def check_dependencies():
    """Проверка зависимостей"""
    
    print("=== Проверка зависимостей ===")
    
    # Проверка pandoc
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        print(f"✓ Pandoc: {result.stdout.split()[1]}")
    except FileNotFoundError:
        print("✗ Pandoc не найден")
        return False
    
    # Проверка LaTeX
    latex_engines = ['pdflatex', 'xelatex', 'lualatex']
    latex_found = False
    
    for engine in latex_engines:
        try:
            result = subprocess.run([engine, '--version'], capture_output=True, text=True)
            print(f"✓ {engine}: найден")
            latex_found = True
            break
        except FileNotFoundError:
            continue
    
    if not latex_found:
        print("✗ LaTeX не найден")
        print("  Установите LaTeX: brew install --cask mactex")
        return False
    
    return True

def create_combined_markdown():
    """Создание объединенного Markdown файла"""
    
    docs_dir = Path(__file__).parent.parent.parent.parent.parent / "docs" / "automl" / "gluon"
    
    # Порядок файлов
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
        "11_apple_silicon_optimization.md",
        "12_simple_production_example.md",
        "13_advanced_production_example.md",
        "14_theory_and_fundamentals.md",
        "15_interpretability_and_explainability.md",
        "16_advanced_topics.md",
        "17_ethics_and_responsible_ai.md",
        "18_case_studies.md",
        "19_wave2_indicator_analysis.md",
        "20_schr_levels_analysis.md",
        "21_schr_short3_analysis.md"
    ]
    
    combined_content = []
    
    for filename in files_order:
        file_path = docs_dir / filename
        
        if file_path.exists():
            print(f"Добавляем: {filename}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if combined_content:
                    combined_content.append("\n\n---\n\n")
                
                combined_content.append(content)
        else:
            print(f"Файл не найден: {filename}")
    
    # Сохранение
    combined_file = docs_dir / "AutoML_Gluon_Complete_Manual.md"
    
    with open(combined_file, 'w', encoding='utf-8') as f:
        f.write(''.join(combined_content))
    
    print(f"Создан объединенный файл: {combined_file}")
    return combined_file

def create_pdf_with_latex(markdown_file):
    """Создание PDF с LaTeX"""
    
    print("=== Создание PDF с LaTeX ===")
    
    # Команда pandoc с LaTeX
    cmd = [
        'pandoc',
        str(markdown_file),
        '-o', 'AutoML_Gluon_Complete_Manual.pdf',
        '--toc',
        '--number-sections',
        '--standalone',
        '--pdf-engine=pdflatex',
        '--variable', 'geometry:margin=2cm',
        '--variable', 'fontsize=11pt',
        '--variable', 'documentclass=book',
        '--variable', 'colorlinks=true',
        '--variable', 'linkcolor=blue',
        '--variable', 'urlcolor=blue',
        '--variable', 'toccolor=blue',
        '--variable', 'papersize=a4',
        '--variable', 'linestretch=1.2'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ PDF создан успешно с LaTeX!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка LaTeX: {e}")
        return False

def create_pdf_with_xelatex(markdown_file):
    """Создание PDF с XeLaTeX"""
    
    print("=== Создание PDF с XeLaTeX ===")
    
    cmd = [
        'pandoc',
        str(markdown_file),
        '-o', 'AutoML_Gluon_Complete_Manual.pdf',
        '--toc',
        '--number-sections',
        '--standalone',
        '--pdf-engine=xelatex',
        '--variable', 'geometry:margin=2cm',
        '--variable', 'fontsize=11pt',
        '--variable', 'documentclass=book',
        '--variable', 'colorlinks=true',
        '--variable', 'linkcolor=blue',
        '--variable', 'urlcolor=blue',
        '--variable', 'toccolor=blue',
        '--variable', 'papersize=a4',
        '--variable', 'linestretch=1.2'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ PDF создан успешно с XeLaTeX!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка XeLaTeX: {e}")
        return False

def create_html_version(markdown_file):
    """Создание HTML версии"""
    
    print("=== Создание HTML версии ===")
    
    cmd = [
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
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ HTML создан успешно!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка HTML: {e}")
        return False

def create_enhanced_html():
    """Создание улучшенного HTML с навигацией"""
    
    html_file = Path("AutoML_Gluon_Complete_Manual.html")
    
    if not html_file.exists():
        print("HTML файл не найден!")
        return False
    
    # Чтение HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Добавление JavaScript для навигации
    enhanced_html = html_content.replace(
        '</head>',
        '''
        <script>
        // Плавная прокрутка к якорям
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
        
        // Функция печати в PDF
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
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
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
    
    print(f"✓ Создан улучшенный HTML: {enhanced_file}")
    return enhanced_file

def open_in_browser(html_file):
    """Открытие HTML в браузере"""
    
    try:
        webbrowser.open(f"file://{html_file.absolute()}")
        print(f"✓ HTML открыт в браузере: {html_file.absolute()}")
        return True
    except Exception as e:
        print(f"✗ Ошибка открытия в браузере: {e}")
        return False

def main():
    """Основная функция"""
    
    print("=== Создание PDF учебника AutoML Gluon ===")
    
    # Проверка зависимостей
    if not check_dependencies():
        print("\n⚠️  Некоторые зависимости отсутствуют, но продолжаем...")
    
    # Создание объединенного Markdown
    markdown_file = create_combined_markdown()
    
    if not markdown_file.exists():
        print("✗ Ошибка создания объединенного файла")
        return False
    
    # Попытка создания PDF с LaTeX
    if create_pdf_with_latex(markdown_file):
        print("\n🎉 PDF успешно создан с LaTeX!")
        return True
    
    # Попытка создания PDF с XeLaTeX
    if create_pdf_with_xelatex(markdown_file):
        print("\n🎉 PDF успешно создан с XeLaTeX!")
        return True
    
    # Создание HTML версии
    if create_html_version(markdown_file):
        # Создание улучшенного HTML
        enhanced_file = create_enhanced_html()
        
        if enhanced_file:
            print("\n📄 HTML версия создана успешно!")
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
            
            # Открытие в браузере
            open_in_browser(enhanced_file)
            
            return True
    
    print("\n❌ Не удалось создать PDF автоматически")
    print("Используйте HTML версию для создания PDF через браузер")
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
