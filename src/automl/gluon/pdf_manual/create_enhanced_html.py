#!/usr/bin/env python3
"""
Создание улучшенной HTML версии учебника
С крупным шрифтом, центрированием и удобным чтением

Автор: Shcherbyna Rostyslav
Дата: 2024
"""

import os
from pathlib import Path

def create_enhanced_html():
    """Создание улучшенной HTML версии"""
    
    # Пути к файлам
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    # Если путь неправильный, используем абсолютный путь
    if not docs_dir.exists():
        docs_dir = Path("/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon")
        print(f"Используем абсолютный путь: {docs_dir}")
        print(f"Docs dir exists: {docs_dir.exists()}")
    
    html_file = docs_dir / "AutoML_Gluon_Complete_Manual_Enhanced.html"
    enhanced_html_file = docs_dir / "AutoML_Gluon_Complete_Manual_Reading_Friendly.html"
    
    print("=== Создание улучшенной HTML версии ===")
    print(f"Исходный HTML: {html_file}")
    print(f"Улучшенный HTML: {enhanced_html_file}")
    
    if not html_file.exists():
        print(f"✗ HTML файл не найден: {html_file}")
        return False
    
    try:
        # Читаем исходный HTML
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Создаем улучшенную версию
        enhanced_html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoML Gluon - Полное руководство пользователя</title>
    <style>
        /* Улучшенные стили для удобного чтения */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 18px;
            line-height: 1.8;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header .subtitle {{
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 10px;
        }}
        
        .header .author {{
            font-size: 1.1em;
            opacity: 0.8;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin: 30px 0 20px 0;
            font-weight: bold;
        }}
        
        h1 {{
            font-size: 2.2em;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
        }}
        
        h2 {{
            font-size: 1.8em;
            color: #2980b9;
            border-left: 5px solid #3498db;
            padding-left: 20px;
            margin: 40px 0 25px 0;
        }}
        
        h3 {{
            font-size: 1.5em;
            color: #27ae60;
            margin: 30px 0 15px 0;
        }}
        
        h4 {{
            font-size: 1.3em;
            color: #e67e22;
            margin: 25px 0 10px 0;
        }}
        
        p {{
            margin: 15px 0;
            text-align: justify;
            font-size: 1.1em;
        }}
        
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
            font-size: 1.05em;
        }}
        
        code {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            border: 1px solid #34495e;
        }}
        
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            font-size: 0.95em;
            border: 1px solid #34495e;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        pre code {{
            background: transparent;
            color: inherit;
            padding: 0;
            border: none;
            border-radius: 0;
        }}
        
        /* Стили для ссылок внутри кода */
        code a, pre a {{
            color: #f39c12 !important;  /* Оранжевый цвет для ссылок в коде */
            text-decoration: underline;
        }}
        
        code a:hover, pre a:hover {{
            color: #e67e22 !important;  /* Темнее при наведении */
        }}
        
        /* Стили для ключевых слов в коде */
        code .keyword, pre .keyword {{
            color: #e74c3c;  /* Красный для ключевых слов */
            font-weight: bold;
        }}
        
        code .string, pre .string {{
            color: #2ecc71;  /* Зеленый для строк */
        }}
        
        code .number, pre .number {{
            color: #9b59b6;  /* Фиолетовый для чисел */
        }}
        
        code .boolean, pre .boolean {{
            color: #f39c12;  /* Оранжевый для булевых значений */
            font-weight: bold;
        }}
        
        blockquote {{
            border-left: 5px solid #3498db;
            background: #f8f9fa;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
            font-style: italic;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        th {{
            background: #3498db;
            color: white;
            font-weight: bold;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 20px 0;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .toc {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 8px;
            margin: 30px 0;
        }}
        
        .toc h2 {{
            color: #2c3e50;
            border: none;
            padding: 0;
            margin-bottom: 20px;
        }}
        
        .toc ul {{
            list-style: none;
            padding: 0;
        }}
        
        .toc li {{
            margin: 10px 0;
        }}
        
        .toc a {{
            color: #3498db;
            text-decoration: none;
            font-size: 1.1em;
            padding: 8px 15px;
            display: block;
            border-radius: 5px;
            transition: all 0.3s ease;
        }}
        
        .toc a:hover {{
            background: #3498db;
            color: white;
            transform: translateX(5px);
        }}
        
        .highlight {{
            background: #fff3cd;
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #ffc107;
            margin: 20px 0;
        }}
        
        .warning {{
            background: #f8d7da;
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #dc3545;
            margin: 20px 0;
        }}
        
        .success {{
            background: #d4edda;
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #28a745;
            margin: 20px 0;
        }}
        
        .navigation {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            z-index: 1000;
        }}
        
        .navigation h3 {{
            margin-bottom: 15px;
            color: #2c3e50;
        }}
        
        .navigation a {{
            display: block;
            color: #3498db;
            text-decoration: none;
            margin: 5px 0;
            padding: 5px 10px;
            border-radius: 5px;
            transition: background 0.3s ease;
        }}
        
        .navigation a:hover {{
            background: #f8f9fa;
        }}
        
        @media (max-width: 768px) {{
            body {{
                font-size: 16px;
                padding: 10px;
            }}
            
            .container {{
                margin: 0;
                border-radius: 0;
            }}
            
            .header {{
                padding: 20px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .navigation {{
                position: static;
                margin: 20px 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AutoML Gluon</h1>
            <div class="subtitle">Полное руководство пользователя</div>
            <div class="author">Автор: Shcherbyna Rostyslav | Дата: 2024</div>
        </div>
        
        <div class="content">
            {html_content}
        </div>
    </div>
    
    <div class="navigation">
        <h3>Навигация</h3>
        <a href="#installation">Установка</a>
        <a href="#basic-usage">Базовое использование</a>
        <a href="#metrics">Метрики</a>
        <a href="#validation">Валидация</a>
        <a href="#production">Продакшен</a>
        <a href="#apple-silicon">Apple Silicon</a>
    </div>
    
    <script>
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
        
        // Подсветка текущего раздела
        window.addEventListener('scroll', function() {{
            const sections = document.querySelectorAll('h1, h2, h3');
            const navLinks = document.querySelectorAll('.navigation a');
            
            let current = '';
            sections.forEach(section => {{
                const sectionTop = section.offsetTop;
                if (scrollY >= sectionTop - 200) {{
                    current = section.getAttribute('id') || section.textContent.toLowerCase().replace(/\\s+/g, '-');
                }}
            }});
            
            navLinks.forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {{
                    link.classList.add('active');
                }}
            }});
        }});
        
        // Улучшение читаемости кода
        function improveCodeReadability() {{
            // Находим все блоки кода, но только те, которые еще не обработаны
            const codeBlocks = document.querySelectorAll('code:not(.processed), pre:not(.processed)');
            
            codeBlocks.forEach(block => {{
                // Проверяем, что это простой текстовый блок кода
                if (block.children.length === 0 || block.textContent === block.innerText) {{
                    let text = block.textContent;
                    let html = '';
                    let i = 0;
                    
                    while (i < text.length) {{
                        // Проверяем комментарии
                        if (text[i] === '#') {{
                            let commentEnd = text.indexOf('\\n', i);
                            if (commentEnd === -1) commentEnd = text.length;
                            html += '<span style="color: #95a5a6; font-style: italic;">' + text.substring(i, commentEnd) + '</span>';
                            i = commentEnd;
                        }}
                        // Проверяем строки в кавычках
                        else if (text[i] === '"' || text[i] === "'") {{
                            let quote = text[i];
                            let stringEnd = i + 1;
                            while (stringEnd < text.length && text[stringEnd] !== quote) {{
                                if (text[stringEnd] === '\\\\' && stringEnd + 1 < text.length) {{
                                    stringEnd += 2; // Пропускаем экранированные символы
                                }} else {{
                                    stringEnd++;
                                }}
                            }}
                            if (stringEnd < text.length) stringEnd++;
                            html += '<span class="string">' + text.substring(i, stringEnd) + '</span>';
                            i = stringEnd;
                        }}
                        // Проверяем ключевые слова и булевы значения
                        else if (/[a-zA-Z_]/.test(text[i])) {{
                            let wordEnd = i;
                            while (wordEnd < text.length && /[a-zA-Z0-9_]/.test(text[wordEnd])) {{
                                wordEnd++;
                            }}
                            let word = text.substring(i, wordEnd);
                            
                            // Ключевые слова Python
                            if (/^(def|class|if|else|elif|for|while|try|except|finally|with|import|from|as|return|yield|lambda|and|or|not|in|is|None)$/.test(word)) {{
                                html += '<span class="keyword">' + word + '</span>';
                            }}
                            // Булевы значения
                            else if (/^(True|False|true|false)$/.test(word)) {{
                                html += '<span class="boolean">' + word + '</span>';
                            }}
                            else {{
                                html += word;
                            }}
                            i = wordEnd;
                        }}
                        // Проверяем числа
                        else if (/[0-9]/.test(text[i])) {{
                            let numEnd = i;
                            while (numEnd < text.length && /[0-9.]/.test(text[numEnd])) {{
                                numEnd++;
                            }}
                            html += '<span class="number">' + text.substring(i, numEnd) + '</span>';
                            i = numEnd;
                        }}
                        else {{
                            html += text[i];
                            i++;
                        }}
                    }}
                    
                    block.innerHTML = html;
                    block.classList.add('processed');
                }}
            }});
        }}
        
        // Запускаем улучшение читаемости после загрузки
        document.addEventListener('DOMContentLoaded', improveCodeReadability);
        
        // Также запускаем при изменении содержимого
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', improveCodeReadability);
        }} else {{
            improveCodeReadability();
        }}
    </script>
</body>
</html>
"""
        
        # Сохраняем улучшенную версию
        with open(enhanced_html_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_html)
        
        print(f"✓ Улучшенная HTML версия создана: {enhanced_html_file}")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка при создании улучшенной HTML: {e}")
        return False

def main():
    print("=== Создание улучшенной HTML версии учебника ===")
    print("Автор: Shcherbyna Rostyslav")
    print("Дата: 2024")
    
    success = create_enhanced_html()
    
    if success:
        print("\n🎉 Улучшенная HTML версия создана!")
        print("Файл готов для удобного чтения.")
    else:
        print("\n⚠️  Не удалось создать улучшенную HTML версию.")

if __name__ == "__main__":
    main()
