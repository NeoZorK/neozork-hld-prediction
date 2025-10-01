#!/usr/bin/env python3
"""
Скрипт для генерации HTML из всех расширенных .md файлов
"""

import os
import markdown
import re
from pathlib import Path

def create_html_from_md():
    """Создание HTML из всех .md файлов"""
    
    # Путь к папке с .md файлами
    md_dir = Path("docs/automl/gluon")
    output_file = md_dir / "AutoML_Gluon_Complete_Manual_Reading_Friendly.html"
    
    # Список всех .md файлов в правильном порядке
    md_files = [
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
        "21_schr_short3_analysis.md",
        "22_super_system_ultimate.md",
        "23_reading_guide.md",
        "24_probability_usage_guide.md",
        "25_trading_bot_monitoring.md"
    ]
    
    # HTML шаблон
    html_template = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoML Gluon - Полное руководство</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }
        h3 {
            color: #2c3e50;
            margin-top: 25px;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }
        pre code {
            background: none;
            padding: 0;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #f8f9fa;
            font-style: italic;
        }
        ul, ol {
            padding-left: 25px;
        }
        li {
            margin-bottom: 5px;
        }
        .toc {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        .toc h2 {
            margin-top: 0;
            border: none;
            padding: 0;
        }
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        .toc li {
            margin-bottom: 8px;
        }
        .toc a {
            text-decoration: none;
            color: #3498db;
            font-weight: 500;
        }
        .toc a:hover {
            text-decoration: underline;
        }
        .highlight {
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }
        .warning {
            background-color: #f8d7da;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
            margin: 20px 0;
        }
        .success {
            background-color: #d4edda;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AutoML Gluon - Полное руководство</h1>
        <p><strong>Автор:</strong> Shcherbyna Rostyslav<br>
        <strong>Дата:</strong> 2024<br>
        <strong>Версия:</strong> 2.0 (Расширенная с детальными объяснениями)</p>
        
        <div class="toc">
            <h2>Содержание</h2>
            <ul>
                <li><a href="#установка-automl-gluon">1. Установка AutoML Gluon</a></li>
                <li><a href="#базовое-использование">2. Базовое использование</a></li>
                <li><a href="#продвинутая-конфигурация">3. Продвинутая конфигурация</a></li>
                <li><a href="#метрики-и-оценка-качества">4. Метрики и оценка качества</a></li>
                <li><a href="#валидация-моделей">5. Валидация моделей</a></li>
                <li><a href="#продакшен-и-деплой">6. Продакшен и деплой</a></li>
                <li><a href="#переобучение-моделей">7. Переобучение моделей</a></li>
                <li><a href="#лучшие-практики">8. Лучшие практики</a></li>
                <li><a href="#примеры-использования">9. Примеры использования</a></li>
                <li><a href="#решение-проблем">10. Решение проблем</a></li>
                <li><a href="#оптимизация-для-apple-silicon">11. Оптимизация для Apple Silicon</a></li>
                <li><a href="#простой-пример-продакшена">12. Простой пример продакшена</a></li>
                <li><a href="#продвинутый-пример-продакшена">13. Продвинутый пример продакшена</a></li>
                <li><a href="#теория-и-основы-automl">14. Теория и основы AutoML</a></li>
                <li><a href="#интерпретируемость-моделей">15. Интерпретируемость моделей</a></li>
                <li><a href="#продвинутые-темы">16. Продвинутые темы</a></li>
                <li><a href="#этика-и-ответственный-ai">17. Этика и ответственный AI</a></li>
                <li><a href="#кейс-стади">18. Кейс-стади</a></li>
                <li><a href="#wave2-индикатор">19. WAVE2 Индикатор</a></li>
                <li><a href="#schr-levels-индикатор">20. SCHR Levels Индикатор</a></li>
                <li><a href="#schr-short3-индикатор">21. SCHR SHORT3 Индикатор</a></li>
                <li><a href="#супер-система">22. Супер-система</a></li>
                <li><a href="#руководство-по-изучению">23. Руководство по изучению</a></li>
                <li><a href="#использование-вероятностей">24. Использование вероятностей</a></li>
                <li><a href="#мониторинг-торгового-бота">25. Мониторинг торгового бота</a></li>
            </ul>
        </div>
        
        {content}
    </div>
</body>
</html>"""
    
    # Настройка markdown
    md = markdown.Markdown(extensions=['toc', 'codehilite', 'tables', 'fenced_code'])
    
    # Сбор содержимого всех .md файлов
    all_content = []
    
    for md_file in md_files:
        file_path = md_dir / md_file
        if file_path.exists():
            print(f"Обрабатываем {md_file}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Добавляем разделитель между главами
            all_content.append(f"\n\n---\n\n")
            all_content.append(content)
        else:
            print(f"Файл {md_file} не найден!")
    
    # Объединяем весь контент
    full_content = ''.join(all_content)
    
    # Конвертируем в HTML
    html_content = md.convert(full_content)
    
    # Создаем финальный HTML
    final_html = html_template.replace('{content}', html_content)
    
    # Сохраняем файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ HTML файл создан: {output_file}")
    print(f"📄 Размер файла: {len(final_html)} символов")
    
    return output_file

if __name__ == "__main__":
    create_html_from_md()
