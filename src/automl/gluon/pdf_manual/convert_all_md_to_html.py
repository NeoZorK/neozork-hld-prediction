#!/usr/bin/env python3
"""
Конвертер всех markdown файлов в единый HTML с форматированием кода
Автор: NeoZorK (Shcherbyna Rostyslav)
Дата: 2025
"""

import os
import re
from pathlib import Path

def convert_md_to_html(md_content):
    """Конвертация markdown в HTML с базовым форматированием"""
    
    # Заголовки
    md_content = re.sub(r'^# (.*)', r'<h1>\1</h1>', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^## (.*)', r'<h2>\1</h2>', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^### (.*)', r'<h3>\1</h3>', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^#### (.*)', r'<h4>\1</h4>', md_content, flags=re.MULTILINE)
    
    # Жирный текст
    md_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', md_content)
    
    # Курсив
    md_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', md_content)
    
    # Код
    md_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', md_content)
    
    # Блоки кода
    md_content = re.sub(r'```python\n(.*?)\n```', r'<pre><code class="language-python">\1</code></pre>', md_content, flags=re.DOTALL)
    md_content = re.sub(r'```bash\n(.*?)\n```', r'<pre><code class="language-bash">\1</code></pre>', md_content, flags=re.DOTALL)
    md_content = re.sub(r'```\n(.*?)\n```', r'<pre><code>\1</code></pre>', md_content, flags=re.DOTALL)
    
    # Списки
    md_content = re.sub(r'^- (.*)', r'<li>\1</li>', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^(\d+)\. (.*)', r'<li>\2</li>', md_content, flags=re.MULTILINE)
    
    # Параграфы
    paragraphs = md_content.split('\n\n')
    html_paragraphs = []
    
    for para in paragraphs:
        if para.strip():
            if not para.startswith('<'):
                para = f'<p>{para}</p>'
            html_paragraphs.append(para)
    
    return '\n\n'.join(html_paragraphs)

def create_complete_html_manual():
    """Создание полного HTML руководства из всех markdown файлов"""
    
    print("=== Создание полного HTML руководства ===")
    print("Автор: NeoZorK (Shcherbyna Rostyslav)")
    print("Дата: 2025")
    
    # Пути
    docs_dir = Path("/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon")
    output_file = docs_dir / "AutoML_Gluon_Complete_Manual_Full.html"
    
    # Список всех markdown файлов в правильном порядке
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
    
    # HTML шаблон с форматированием в стиле Python_Formatting_Example.html
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
        
        /* Улучшенные стили для Python кода */
        pre {
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
        }
        
        pre::before {
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
        }
        
        /* Цветовое выделение для Python синтаксиса */
        .token.comment {
            color: #6a9955;
            font-style: italic;
        }
        
        .token.keyword {
            color: #569cd6;
            font-weight: bold;
        }
        
        .token.string {
            color: #ce9178;
        }
        
        .token.number {
            color: #b5cea8;
        }
        
        .token.function {
            color: #dcdcaa;
        }
        
        .token.class-name {
            color: #4ec9b0;
        }
        
        .token.operator {
            color: #d4d4d4;
        }
        
        .token.punctuation {
            color: #d4d4d4;
        }
        
        .token.variable {
            color: #9cdcfe;
        }
        
        .token.constant {
            color: #4fc1ff;
        }
        
        .token.builtin {
            color: #dcdcaa;
        }
        
        .token.boolean {
            color: #569cd6;
        }
        
        .explanation {
            background: #f8f9fa;
            border-left: 4px solid #17a2b8;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }
        
        .warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }
        
        .success {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }
        
        .toc {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .toc h3 {
            margin-top: 0;
            color: #2c3e50;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 8px 0;
        }
        
        .toc a {
            color: #3498db;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 4px;
            display: block;
            transition: background-color 0.2s;
        }
        
        .toc a:hover {
            background-color: #e3f2fd;
        }
        
        .section {
            margin: 40px 0;
            padding: 20px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
        }
        
        .author-info {
            background: #e8f4fd;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AutoML Gluon - Полное руководство пользователя</h1>
        
        <div class="author-info">
            <strong>Автор:</strong> NeoZorK (Shcherbyna Rostyslav)<br>
            <strong>Дата:</strong> 2025<br>
            <strong>Местоположение:</strong> Ukraine, Zaporizhzhya<br>
            <strong>Версия:</strong> 1.0
        </div>
        
        <div class="explanation">
            <strong>🎯 О руководстве:</strong><br>
            Это исчерпывающее руководство по AutoML Gluon - мощному инструменту автоматизированного машинного обучения от Amazon. Руководство содержит все необходимые знания для эффективного использования AutoML Gluon в реальных проектах.
        </div>
        
        <div class="toc">
            <h3>Содержание</h3>
            <ul>
                <li><a href="#installation">1. Установка AutoML Gluon</a></li>
                <li><a href="#basic-usage">2. Базовое использование</a></li>
                <li><a href="#advanced-configuration">3. Продвинутая конфигурация</a></li>
                <li><a href="#metrics">4. Метрики и оценка качества</a></li>
                <li><a href="#validation">5. Валидация моделей</a></li>
                <li><a href="#production">6. Продакшен и деплой</a></li>
                <li><a href="#retraining">7. Переобучение моделей</a></li>
                <li><a href="#best-practices">8. Лучшие практики</a></li>
                <li><a href="#examples">9. Примеры использования</a></li>
                <li><a href="#troubleshooting">10. Troubleshooting</a></li>
                <li><a href="#apple-silicon">11. Оптимизация для Apple Silicon</a></li>
                <li><a href="#simple-production">12. Простой пример продакшена</a></li>
                <li><a href="#advanced-production">13. Сложный пример продакшена</a></li>
                <li><a href="#theory">14. Теория и основы AutoML</a></li>
                <li><a href="#interpretability">15. Интерпретируемость и объяснимость</a></li>
                <li><a href="#advanced-topics">16. Продвинутые темы</a></li>
                <li><a href="#ethics">17. Этика и ответственный AI</a></li>
                <li><a href="#case-studies">18. Кейс-стади</a></li>
                <li><a href="#wave2-analysis">19. WAVE2 Индикатор - Полный анализ</a></li>
                <li><a href="#schr-levels">20. SCHR Levels - Анализ и ML-модель</a></li>
                <li><a href="#schr-short3">21. SCHR SHORT3 - Краткосрочная торговля</a></li>
                <li><a href="#super-system">22. Супер-система: Объединение всех индикаторов</a></li>
                <li><a href="#reading-guide">23. Руководство по изучению учебника</a></li>
                <li><a href="#probability-usage">24. Правильное использование вероятностей</a></li>
                <li><a href="#monitoring">25. Мониторинг торгового бота</a></li>
            </ul>
        </div>
        
        {content}
    </div>
    
    <script>
        // Инициализация Prism.js для синтаксического выделения
        if (typeof Prism !== 'undefined') {
            Prism.highlightAll();
        }
        
        // Плавная прокрутка к якорям
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    </script>
</body>
</html>"""
    
    # Чтение и конвертация всех markdown файлов
    all_content = []
    
    for i, md_file in enumerate(md_files, 1):
        md_path = docs_dir / md_file
        if md_path.exists():
            print(f"Обрабатываем {i}/25: {md_file}")
            
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Конвертация в HTML
            html_content = convert_md_to_html(md_content)
            
            # Добавление ID для навигации
            section_id = md_file.replace('.md', '').replace('_', '-')
            html_content = f'<div class="section" id="{section_id}">\n{html_content}\n</div>'
            
            all_content.append(html_content)
        else:
            print(f"⚠️ Файл не найден: {md_file}")
    
    # Объединение всего контента
    full_content = '\n\n'.join(all_content)
    
    # Создание финального HTML
    final_html = html_template.format(content=full_content)
    
    # Сохранение файла
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"\n✅ Полное HTML руководство создано: {output_file}")
    print(f"📊 Обработано разделов: {len(all_content)}/25")
    print(f"📁 Размер файла: {os.path.getsize(output_file) / 1024:.1f} KB")
    
    return True

if __name__ == "__main__":
    success = create_complete_html_manual()
    if success:
        print("\n🎉 Полное HTML руководство создано успешно!")
        print("Файл готов для использования.")
    else:
        print("\n❌ Ошибка при создании HTML руководства.")
