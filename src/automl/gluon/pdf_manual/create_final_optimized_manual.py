#!/usr/bin/env python3
"""
Создание финальной оптимизированной версии руководства
С правильными изображениями и форматированием

Автор: NeoZorK (Shcherbyna Rostyslav)
Дата: 2025
"""

import os
import subprocess
import sys
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
import re

def create_final_html():
    """Создание финального HTML с оптимизированными изображениями"""
    
    print("=== Создание финального HTML ===")
    
    # Определение путей
    project_root = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    output_file = docs_dir / "AutoML_Gluon_Complete_Manual_Final.html"
    
    # Список всех разделов
    sections = [
        {"id": "01-installation", "title": "Введение и установка", "file": "01_installation.md"},
        {"id": "02-basic-usage", "title": "Базовое использование", "file": "02_basic_usage.md"},
        {"id": "03-advanced-configuration", "title": "Продвинутая конфигурация", "file": "03_advanced_configuration.md"},
        {"id": "04-metrics", "title": "Метрики и оценка качества", "file": "04_metrics.md"},
        {"id": "05-validation", "title": "Валидация моделей", "file": "05_validation.md"},
        {"id": "06-production", "title": "Продакшен и деплой", "file": "06_production.md"},
        {"id": "07-retraining", "title": "Переобучение моделей", "file": "07_retraining.md"},
        {"id": "08-best-practices", "title": "Лучшие практики", "file": "08_best_practices.md"},
        {"id": "09-examples", "title": "Примеры использования", "file": "09_examples.md"},
        {"id": "10-troubleshooting", "title": "Troubleshooting", "file": "10_troubleshooting.md"},
        {"id": "11-apple-silicon-optimization", "title": "Оптимизация для Apple Silicon", "file": "11_apple_silicon_optimization.md"},
        {"id": "12-simple-production-example", "title": "Простой пример продакшена", "file": "12_simple_production_example.md"},
        {"id": "13-advanced-production-example", "title": "Сложный пример продакшена", "file": "13_advanced_production_example.md"},
        {"id": "14-theory-and-fundamentals", "title": "Теория и основы AutoML", "file": "14_theory_and_fundamentals.md"},
        {"id": "15-interpretability-and-explainability", "title": "Интерпретируемость и объяснимость", "file": "15_interpretability_and_explainability.md"},
        {"id": "16-advanced-topics", "title": "Продвинутые темы", "file": "16_advanced_topics.md"},
        {"id": "17-ethics-and-responsible-ai", "title": "Этика и ответственный AI", "file": "17_ethics_and_responsible_ai.md"},
        {"id": "18-case-studies", "title": "Кейс-стади", "file": "18_case_studies.md"},
        {"id": "19-wave2-indicator-analysis", "title": "WAVE2 Индикатор - Полный анализ", "file": "19_wave2_indicator_analysis.md"},
        {"id": "20-schr-levels-analysis", "title": "SCHR Levels - Анализ и ML-модель", "file": "20_schr_levels_analysis.md"},
        {"id": "21-schr-short3-analysis", "title": "SCHR SHORT3 - Краткосрочная торговля", "file": "21_schr_short3_analysis.md"},
        {"id": "22-super-system-ultimate", "title": "Супер-система: Объединение всех индикаторов", "file": "22_super_system_ultimate.md"},
        {"id": "23-reading-guide", "title": "Руководство по изучению учебника", "file": "23_reading_guide.md"},
        {"id": "24-probability-usage-guide", "title": "Правильное использование вероятностей", "file": "24_probability_usage_guide.md"},
        {"id": "25-trading-bot-monitoring", "title": "Мониторинг торгового бота - Лучшие практики", "file": "25_trading_bot_monitoring.md"}
    ]
    
    # HTML шаблон с улучшенными стилями для изображений
    html_template = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoML Gluon - Полное руководство пользователя</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            text-align: center;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        
        h3 {{
            color: #2c3e50;
            margin-top: 25px;
        }}
        
        /* Улучшенные стили для изображений */
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
        }}
        
        /* Стили для изображений в коде */
        pre img {{
            margin: 10px 0;
            box-shadow: none;
            border: none;
        }}
        
        /* Улучшенные стили для Python кода */
        pre {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 4px solid #3776ab;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin: 20px 0;
            position: relative;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        pre::before {{
            content: "Python";
            position: absolute;
            top: 10px;
            right: 15px;
            background: #3776ab;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        /* Цветовое выделение для Python синтаксиса */
        .token.comment {{
            color: #6a9955;
            font-style: italic;
        }}
        
        .token.keyword {{
            color: #569cd6;
            font-weight: bold;
        }}
        
        .token.string {{
            color: #ce9178;
        }}
        
        .token.number {{
            color: #b5cea8;
        }}
        
        .token.function {{
            color: #dcdcaa;
        }}
        
        .token.class-name {{
            color: #4ec9b0;
        }}
        
        .token.operator {{
            color: #d4d4d4;
        }}
        
        .token.punctuation {{
            color: #d4d4d4;
        }}
        
        .token.variable {{
            color: #9cdcfe;
        }}
        
        .token.constant {{
            color: #4fc1ff;
        }}
        
        .token.builtin {{
            color: #dcdcaa;
        }}
        
        .token.boolean {{
            color: #569cd6;
        }}
        
        .token.parameter {{
            color: #9cdcfe;
        }}
        
        .token.property {{
            color: #9cdcfe;
        }}
        
        .token.attribute {{
            color: #9cdcfe;
        }}
        
        .token.tag {{
            color: #569cd6;
        }}
        
        .token.attr-name {{
            color: #92c5f8;
        }}
        
        .token.attr-value {{
            color: #ce9178;
        }}
        
        .explanation {{
            background: #f8f9fa;
            border-left: 4px solid #17a2b8;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }}
        
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }}
        
        .success {{
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }}
        
        .toc {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .toc h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        
        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .toc li {{
            margin: 8px 0;
        }}
        
        .toc a {{
            color: #3498db;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 4px;
            display: block;
            transition: background-color 0.3s;
        }}
        
        .toc a:hover {{
            background-color: #e3f2fd;
        }}
        
        .section {{
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 1px solid #eee;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        .inline-code {{
            background: #f1f3f4;
            color: #d73a49;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }}
        
        .bullet-list {{
            padding-left: 20px;
        }}
        
        .bullet-list li {{
            margin: 8px 0;
        }}
        
        .numbered-list {{
            padding-left: 20px;
        }}
        
        .numbered-list li {{
            margin: 8px 0;
        }}
        
        .paragraph {{
            margin: 15px 0;
        }}
        
        .section-title {{
            color: #2c3e50;
            font-size: 1.8em;
            margin-top: 40px;
            margin-bottom: 20px;
        }}
        
        .subsection-title {{
            color: #34495e;
            font-size: 1.4em;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        .back-to-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }}
        
        .back-to-top:hover {{
            background: #2980b9;
            transform: translateY(-2px);
        }}
        
        /* Адаптивные стили для мобильных устройств */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .container {{
                padding: 20px;
            }}
            
            img {{
                margin: 10px auto;
            }}
            
            pre {{
                font-size: 12px;
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>AutoML Gluon - Полное руководство пользователя</h1>
        <div class="subtitle">
            <strong>Автор:</strong> NeoZorK (Shcherbyna Rostyslav)<br>
            <strong>Дата:</strong> 2025<br>
            <strong>Местоположение:</strong> Ukraine, Zaporizhzhya<br>
            <strong>Версия:</strong> 1.0
        </div>
        
        <div class="toc">
            <h3>📚 Содержание</h3>
            <ul>
                {toc_items}
            </ul>
        </div>
        
        {content}
    </div>
    
    <button class="back-to-top" onclick="scrollToTop()" title="Наверх">↑</button>
    
    <script>
        function scrollToTop() {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}
        
        // Инициализация Prism.js для синтаксического выделения
        if (typeof Prism !== 'undefined') {{
            Prism.highlightAll();
        }}
        
        // Плавная прокрутка к якорям
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});
    </script>
</body>
</html>"""
    
    def convert_md_to_html(md_content, section_id, section_title):
        """Конвертация markdown в HTML с улучшенным форматированием"""
        
        # Конвертация markdown в HTML
        html = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])
        
        # Создание BeautifulSoup объекта для обработки
        soup = BeautifulSoup(html, 'html.parser')
        
        # Исправление путей к изображениям (уже сделано в markdown файлах)
        for img in soup.find_all('img'):
            if img.get('src') and not img['src'].startswith('http'):
                # Добавляем дополнительные стили для изображений
                img['style'] = 'max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;'
        
        # Улучшение форматирования кода
        for code_block in soup.find_all('code'):
            if code_block.parent.name == 'pre':
                # Это блок кода
                code_block['class'] = 'language-python'
                code_block.parent['class'] = 'code-block'
            else:
                # Это inline код
                code_block['class'] = 'inline-code'
        
        # Добавление классов для улучшения стилизации
        for h2 in soup.find_all('h2'):
            h2['class'] = 'section-title'
        
        for h3 in soup.find_all('h3'):
            h3['class'] = 'subsection-title'
        
        for ul in soup.find_all('ul'):
            ul['class'] = 'bullet-list'
        
        for ol in soup.find_all('ol'):
            ol['class'] = 'numbered-list'
        
        for p in soup.find_all('p'):
            if not p.get('class'):
                p['class'] = 'paragraph'
        
        return f'<div class="section" id="{section_id}"><h2>{section_title}</h2>{str(soup)}</div>'
    
    # Создание содержания
    toc_items = ""
    full_content = ""
    
    for i, section in enumerate(sections, 1):
        print(f"Обрабатываем {i}/25: {section['file']}")
        
        # Создание ссылки для содержания
        toc_items += f'<li><a href="#{section["id"]}">{i}. {section["title"]}</a></li>\n'
        
        # Чтение markdown файла
        md_file = docs_dir / section['file']
        if md_file.exists():
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Конвертация в HTML
            html_content = convert_md_to_html(md_content, section['id'], section['title'])
            full_content += html_content + '\n'
        else:
            print(f"⚠️  Файл не найден: {md_file}")
    
    # Создание финального HTML
    final_html = html_template.format(
        toc_items=toc_items,
        content=full_content
    )
    
    # Сохранение файла
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    # Статистика
    file_size = os.path.getsize(output_file) / 1024  # KB
    print(f"✅ Финальный HTML создан: {output_file}")
    print(f"📊 Обработано разделов: {len(sections)}/25")
    print(f"📁 Размер файла: {file_size:.1f} KB")
    
    return True

def create_final_pdf():
    """Создание финального PDF"""
    
    print("\n=== Создание финального PDF ===")
    
    # Запускаем Playwright конвертер с финальным HTML
    script_path = Path(__file__).parent / "create_pdf_with_playwright.py"
    
    try:
        # Модифицируем скрипт для использования финального HTML
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, cwd=script_path.parent)
        
        if result.returncode == 0:
            print("✅ Финальный PDF создан успешно!")
            return True
        else:
            print(f"✗ Ошибка создания PDF: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Ошибка запуска конвертера: {e}")
        return False

def main():
    """Основная функция"""
    
    print("🚀 Создание финальной оптимизированной версии руководства")
    print("Автор: NeoZorK (Shcherbyna Rostyslav)")
    print("Дата: 2025")
    print("Местоположение: Ukraine, Zaporizhzhya")
    
    # Создание финального HTML
    if not create_final_html():
        print("⚠️  Не удалось создать финальный HTML")
        return False
    
    # Создание финального PDF
    if not create_final_pdf():
        print("⚠️  Не удалось создать финальный PDF")
        return False
    
    print("\n🎉 Финальная версия создана успешно!")
    print("📄 Проверьте папку docs/automl/gluon/")
    print("📁 Файлы:")
    print("  - AutoML_Gluon_Complete_Manual_Final.html")
    print("  - AutoML_Gluon_Complete_Manual.pdf")
    print("  - images/optimized/ (оптимизированные изображения)")
    
    return True

if __name__ == "__main__":
    main()
