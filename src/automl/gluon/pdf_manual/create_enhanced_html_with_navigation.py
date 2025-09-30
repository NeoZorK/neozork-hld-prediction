#!/usr/bin/env python3
"""
Создание улучшенной HTML версии с полной навигацией
Автор: NeoZorK (Shcherbyna Rostyslav)
Дата: 2025
Местоположение: Ukraine, Zaporizhzhya
"""

import os
import re
from pathlib import Path

def create_enhanced_html_with_navigation():
    """Создание улучшенной HTML версии с полной навигацией"""
    
    print("=== Создание улучшенной HTML версии с навигацией ===")
    print("Автор: NeoZorK (Shcherbyna Rostyslav)")
    print("Дата: 2025")
    print("Местоположение: Ukraine, Zaporizhzhya")
    
    # Определение путей
    project_root = Path(__file__).parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    if not docs_dir.exists():
        docs_dir = Path("/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon")
        print(f"Используем абсолютный путь: {docs_dir}")
        print(f"Docs dir exists: {docs_dir.exists()}")
    
    html_file = docs_dir / "AutoML_Gluon_Complete_Manual.html"
    enhanced_html_file = docs_dir / "AutoML_Gluon_Complete_Manual_Reading_Friendly.html"
    
    print("=== Создание улучшенной HTML версии с навигацией ===")
    print(f"Исходный HTML: {html_file}")
    print(f"Улучшенный HTML: {enhanced_html_file}")
    
    if not html_file.exists():
        print("✗ HTML файл не найден")
        return False
    
    # Чтение исходного HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Создание улучшенного HTML с навигацией
    enhanced_html = create_enhanced_html_content(html_content)
    
    # Сохранение улучшенного HTML
    with open(enhanced_html_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_html)
    
    print(f"✓ Улучшенная HTML версия с навигацией создана: {enhanced_html_file}")
    return True

def create_enhanced_html_content(html_content):
    """Создание улучшенного HTML контента с навигацией"""
    
    # Список всех разделов
    sections = [
        {"id": "section-1", "title": "Введение и установка", "file": "01_installation.md"},
        {"id": "section-2", "title": "Базовое использование", "file": "02_basic_usage.md"},
        {"id": "section-3", "title": "Продвинутая конфигурация", "file": "03_advanced_configuration.md"},
        {"id": "section-4", "title": "Метрики и оценка качества", "file": "04_metrics.md"},
        {"id": "section-5", "title": "Валидация моделей", "file": "05_validation.md"},
        {"id": "section-6", "title": "Продакшен и деплой", "file": "06_production.md"},
        {"id": "section-7", "title": "Переобучение моделей", "file": "07_retraining.md"},
        {"id": "section-8", "title": "Лучшие практики", "file": "08_best_practices.md"},
        {"id": "section-9", "title": "Примеры использования", "file": "09_examples.md"},
        {"id": "section-10", "title": "Troubleshooting", "file": "10_troubleshooting.md"},
        {"id": "section-11", "title": "Оптимизация для Apple Silicon", "file": "11_apple_silicon_optimization.md"},
        {"id": "section-12", "title": "Простой пример продакшена", "file": "12_simple_production_example.md"},
        {"id": "section-13", "title": "Сложный пример продакшена", "file": "13_advanced_production_example.md"},
        {"id": "section-14", "title": "Теория и основы AutoML", "file": "14_theory_and_fundamentals.md"},
        {"id": "section-15", "title": "Интерпретируемость и объяснимость", "file": "15_interpretability_and_explainability.md"},
        {"id": "section-16", "title": "Продвинутые темы", "file": "16_advanced_topics.md"},
        {"id": "section-17", "title": "Этика и ответственный AI", "file": "17_ethics_and_responsible_ai.md"},
        {"id": "section-18", "title": "Кейс-стади", "file": "18_case_studies.md"},
        {"id": "section-19", "title": "WAVE2 Индикатор - Полный анализ", "file": "19_wave2_indicator_analysis.md"},
        {"id": "section-20", "title": "SCHR Levels - Анализ и ML-модель", "file": "20_schr_levels_analysis.md"},
        {"id": "section-21", "title": "SCHR SHORT3 - Краткосрочная торговля", "file": "21_schr_short3_analysis.md"},
        {"id": "section-22", "title": "Супер-система: Объединение всех индикаторов", "file": "22_super_system_ultimate.md"},
        {"id": "section-23", "title": "Руководство по изучению учебника", "file": "23_reading_guide.md"},
        {"id": "section-24", "title": "Правильное использование вероятностей", "file": "24_probability_usage_guide.md"}
    ]
    
    # Создание навигации
    navigation_html = create_navigation_html(sections)
    
    # Создание полного HTML
    enhanced_html = f"""<!DOCTYPE html>
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
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
        }}
        
        .sidebar {{
            width: 300px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            overflow-y: auto;
            max-height: 100vh;
            position: sticky;
            top: 0;
        }}
        
        .main-content {{
            flex: 1;
            padding: 40px;
            overflow-y: auto;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header .subtitle {{
            font-size: 1.3em;
            opacity: 0.9;
        }}
        
        .navigation {{
            margin-bottom: 30px;
        }}
        
        .navigation h3 {{
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #fff;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 10px;
        }}
        
        .nav-section {{
            margin-bottom: 20px;
        }}
        
        .nav-section h4 {{
            font-size: 1em;
            margin-bottom: 10px;
            color: #fff;
            opacity: 0.9;
        }}
        
        .nav-links {{
            list-style: none;
        }}
        
        .nav-links li {{
            margin-bottom: 8px;
        }}
        
        .nav-links a {{
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            padding: 8px 12px;
            border-radius: 5px;
            display: block;
            transition: all 0.3s ease;
            font-size: 0.9em;
        }}
        
        .nav-links a:hover {{
            background: rgba(255,255,255,0.2);
            color: white;
            transform: translateX(5px);
        }}
        
        .nav-links a.active {{
            background: rgba(255,255,255,0.3);
            color: white;
            font-weight: bold;
        }}
        
        .content {{
            font-size: 18px;
            line-height: 1.8;
            color: #2c3e50;
        }}
        
        .content h1, .content h2, .content h3, .content h4, .content h5, .content h6 {{
            color: #2c3e50;
            margin: 30px 0 20px 0;
            font-weight: bold;
        }}
        
        .content h1 {{
            font-size: 2.2em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .content h2 {{
            font-size: 1.8em;
            border-bottom: 2px solid #764ba2;
            padding-bottom: 8px;
        }}
        
        .content h3 {{
            font-size: 1.5em;
            color: #667eea;
        }}
        
        .content h4 {{
            font-size: 1.3em;
            color: #764ba2;
        }}
        
        .content p {{
            margin: 15px 0;
            text-align: justify;
        }}
        
        .content ul, .content ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        .content li {{
            margin: 8px 0;
        }}
        
        .content blockquote {{
            border-left: 4px solid #667eea;
            margin: 20px 0;
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 0 5px 5px 0;
        }}
        
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .content th, .content td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .content th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
        }}
        
        .content tr:hover {{
            background: #f8f9fa;
        }}
        
        .content code {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
            border: 1px solid #34495e;
        }}
        
        .content pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            border: 1px solid #34495e;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .content pre code {{
            background: none;
            padding: 0;
            border: none;
            color: #ecf0f1;
        }}
        
        .content code a, .content pre a {{
            color: #f39c12;
            text-decoration: none;
        }}
        
        .content code a:hover, .content pre a:hover {{
            text-decoration: underline;
        }}
        
        .content .keyword {{
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .content .string {{
            color: #27ae60;
        }}
        
        .content .number {{
            color: #f39c12;
        }}
        
        .content .boolean {{
            color: #9b59b6;
        }}
        
        .content .comment {{
            color: #7f8c8d;
            font-style: italic;
        }}
        
        .content img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        
        .content a {{
            color: #667eea;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: all 0.3s ease;
        }}
        
        .content a:hover {{
            color: #764ba2;
            border-bottom-color: #764ba2;
        }}
        
        .toc {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .toc h2 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        
        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .toc li {{
            margin: 8px 0;
        }}
        
        .toc a {{
            color: #667eea;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 4px;
            display: block;
            transition: all 0.3s ease;
        }}
        
        .toc a:hover {{
            background: #e9ecef;
            color: #764ba2;
        }}
        
        .back-to-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            font-size: 18px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            z-index: 1000;
        }}
        
        .back-to-top:hover {{
            background: #764ba2;
            transform: translateY(-2px);
        }}
        
        .progress-bar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            z-index: 1001;
            transition: width 0.3s ease;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                flex-direction: column;
            }}
            
            .sidebar {{
                width: 100%;
                max-height: 300px;
                position: relative;
            }}
            
            .main-content {{
                padding: 20px;
            }}
            
            .content {{
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="progress-bar" id="progressBar"></div>
    
    <div class="container">
        <div class="sidebar">
            <div class="navigation">
                <h3>📚 Навигация по учебнику</h3>
                
                <div class="nav-section">
                    <h4>🔰 Основы</h4>
                    <ul class="nav-links">
                        <li><a href="#section-1">1. Введение и установка</a></li>
                        <li><a href="#section-2">2. Базовое использование</a></li>
                        <li><a href="#section-3">3. Продвинутая конфигурация</a></li>
                        <li><a href="#section-4">4. Метрики и оценка качества</a></li>
                        <li><a href="#section-5">5. Валидация моделей</a></li>
                    </ul>
                </div>
                
                <div class="nav-section">
                    <h4>🚀 Продакшен</h4>
                    <ul class="nav-links">
                        <li><a href="#section-6">6. Продакшен и деплой</a></li>
                        <li><a href="#section-7">7. Переобучение моделей</a></li>
                        <li><a href="#section-8">8. Лучшие практики</a></li>
                        <li><a href="#section-9">9. Примеры использования</a></li>
                        <li><a href="#section-10">10. Troubleshooting</a></li>
                    </ul>
                </div>
                
                <div class="nav-section">
                    <h4>🍎 Специализация</h4>
                    <ul class="nav-links">
                        <li><a href="#section-11">11. Apple Silicon оптимизация</a></li>
                        <li><a href="#section-12">12. Простой пример продакшена</a></li>
                        <li><a href="#section-13">13. Сложный пример продакшена</a></li>
                    </ul>
                </div>
                
                <div class="nav-section">
                    <h4>🧠 Теория</h4>
                    <ul class="nav-links">
                        <li><a href="#section-14">14. Теория и основы AutoML</a></li>
                        <li><a href="#section-15">15. Интерпретируемость</a></li>
                        <li><a href="#section-16">16. Продвинутые темы</a></li>
                        <li><a href="#section-17">17. Этика и ответственный AI</a></li>
                    </ul>
                </div>
                
                <div class="nav-section">
                    <h4>📊 Кейс-стади</h4>
                    <ul class="nav-links">
                        <li><a href="#section-18">18. Кейс-стади</a></li>
                    </ul>
                </div>
                
                <div class="nav-section">
                    <h4>📈 Индикаторы</h4>
                    <ul class="nav-links">
                        <li><a href="#section-19">19. WAVE2 Индикатор</a></li>
                        <li><a href="#section-20">20. SCHR Levels</a></li>
                        <li><a href="#section-21">21. SCHR SHORT3</a></li>
                    </ul>
                </div>
                
                <div class="nav-section">
                    <h4>🌟 Продвинутое</h4>
                    <ul class="nav-links">
                        <li><a href="#section-22">22. Супер-система</a></li>
                        <li><a href="#section-23">23. Руководство по изучению</a></li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="header">
                <h1>AutoML Gluon - Полное руководство пользователя</h1>
                <div class="subtitle">
                    <strong>Автор:</strong> NeoZorK (Shcherbyna Rostyslav)<br>
                    <strong>Дата:</strong> 2025<br>
                    <strong>Местоположение:</strong> Ukraine, Zaporizhzhya<br>
                    <strong>Версия:</strong> 1.0
                </div>
            </div>
            
            <div class="content">
                {html_content}
            </div>
        </div>
    </div>
    
    <button class="back-to-top" onclick="scrollToTop()" title="Наверх">↑</button>
    
    <script>
        // Прогресс-бар
        window.addEventListener('scroll', function() {{
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById('progressBar').style.width = scrolled + '%';
        }});
        
        // Плавная прокрутка к началу
        function scrollToTop() {{
            window.scrollTo({{
                top: 0,
                behavior: 'smooth'
            }});
        }}
        
        // Подсветка активной ссылки в навигации
        window.addEventListener('scroll', function() {{
            const sections = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
            const navLinks = document.querySelectorAll('.nav-links a');
            
            let current = '';
            sections.forEach(section => {{
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (scrollY >= (sectionTop - 200)) {{
                    current = section.getAttribute('id');
                }}
            }});
            
            navLinks.forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {{
                    link.classList.add('active');
                }}
            }});
        }});
        
        // Подсветка синтаксиса для кода
        function highlightSyntax() {{
            const codeBlocks = document.querySelectorAll('pre code, code');
            codeBlocks.forEach(block => {{
                let code = block.textContent;
                
                // Подсветка ключевых слов Python
                code = code.replace(/\\b(def|class|if|else|elif|for|while|try|except|finally|with|import|from|as|return|yield|lambda|and|or|not|in|is|True|False|None)\\b/g, '<span class="keyword">$1</span>');
                
                // Подсветка строк
                code = code.replace(/(["'])((?:(?!\\1)[^\\\\]|\\\\.)*)(\\1)/g, '<span class="string">$1$2$3</span>');
                
                // Подсветка чисел
                code = code.replace(/\\b\\d+\\.?\\d*\\b/g, '<span class="number">$&</span>');
                
                // Подсветка булевых значений
                code = code.replace(/\\b(True|False|None)\\b/g, '<span class="boolean">$1</span>');
                
                // Подсветка комментариев
                code = code.replace(/(#.*$)/gm, '<span class="comment">$1</span>');
                
                block.innerHTML = code;
            }});
        }}
        
        // Запуск подсветки синтаксиса
        document.addEventListener('DOMContentLoaded', highlightSyntax);
        
        // Плавная прокрутка для якорных ссылок
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
    
    return enhanced_html

def create_navigation_html(sections):
    """Создание HTML навигации"""
    
    navigation_html = """
    <div class="navigation">
        <h3>📚 Навигация по учебнику</h3>
    """
    
    # Группировка разделов
    groups = {
        "🔰 Основы": sections[:5],
        "🚀 Продакшен": sections[5:10],
        "🍎 Специализация": sections[10:13],
        "🧠 Теория": sections[13:17],
        "📊 Кейс-стади": sections[17:18],
        "📈 Индикаторы": sections[18:21],
        "🌟 Продвинутое": sections[21:]
    }
    
    for group_name, group_sections in groups.items():
        navigation_html += f"""
        <div class="nav-section">
            <h4>{group_name}</h4>
            <ul class="nav-links">
        """
        
        for section in group_sections:
            navigation_html += f'<li><a href="#{section["id"]}">{section["title"]}</a></li>'
        
        navigation_html += """
            </ul>
        </div>
        """
    
    navigation_html += "</div>"
    
    return navigation_html

if __name__ == "__main__":
    success = create_enhanced_html_with_navigation()
    if success:
        print("🎉 Улучшенная HTML версия с навигацией создана!")
        print("Файл готов для удобного чтения.")
    else:
        print("❌ Ошибка при создании HTML версии.")
