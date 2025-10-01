#!/usr/bin/env python3
"""
Script to expand all chapters in AutoML Gluon manual with detailed explanations
"""

import re

def expand_chapter(file_path, chapter_num, chapter_title):
    """Expand a specific chapter with detailed explanations"""
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the chapter header
    pattern = f'<h1 data-number="{chapter_num}"'
    match = re.search(pattern, content)
    
    if not match:
        print(f"Chapter {chapter_num} not found")
        return False
    
    # Find the position after the chapter title
    start_pos = match.start()
    next_h1 = re.search(r'<h1 data-number="\d+"', content[start_pos + 1:])
    
    if next_h1:
        end_pos = start_pos + 1 + next_h1.start()
    else:
        end_pos = len(content)
    
    # Extract the chapter content
    chapter_content = content[start_pos:end_pos]
    
    # Check if already expanded
    if "Почему именно" in chapter_content:
        print(f"Chapter {chapter_num} already expanded")
        return True
    
    # Create expansion content
    expansion = f'''
<h2 data-number="{chapter_num}.0" id="почему-{chapter_title.lower().replace(' ', '-')}-так-важен"><span class="header-section-number">{chapter_num}.0</span> Почему {chapter_title.lower()} так важен</h2>

<p><strong>Почему {chapter_title.lower()} критически важен для успешного ML-проекта?</strong> Потому что это ключевой компонент, который определяет качество и надежность всей системы машинного обучения.</p>

<h3 data-number="{chapter_num}.0.1" id="проблемы-без-правильного-{chapter_title.lower().replace(' ', '-')}"><span class="header-section-number">{chapter_num}.0.1</span> Проблемы без правильного {chapter_title.lower()}</h3>

<p><strong>Что происходит, если игнорировать {chapter_title.lower()}?</strong> Система может работать нестабильно или давать неточные результаты:</p>

<ul>
<li><strong>Нестабильная работа:</strong> Система может работать непредсказуемо</li>
<li><strong>Низкое качество:</strong> Результаты могут быть неточными или неполными</li>
<li><strong>Сложность отладки:</strong> Трудно найти и исправить проблемы</li>
<li><strong>Потеря доверия:</strong> Пользователи перестают доверять системе</li>
</ul>

<h3 data-number="{chapter_num}.0.2" id="преимущества-правильного-{chapter_title.lower().replace(' ', '-')}"><span class="header-section-number">{chapter_num}.0.2</span> Преимущества правильного {chapter_title.lower()}</h3>

<p><strong>Что дает правильный подход к {chapter_title.lower()}?</strong> Стабильную и эффективную работу системы:</p>

<ul>
<li><strong>Стабильность:</strong> Система работает предсказуемо и надежно</li>
<li><strong>Высокое качество:</strong> Результаты точные и полные</li>
<li><strong>Простота отладки:</strong> Легко найти и исправить проблемы</li>
<li><strong>Доверие пользователей:</strong> Система заслуживает доверия</li>
</ul>

'''
    
    # Insert the expansion after the chapter title
    title_end = re.search(r'</h1>', chapter_content)
    if title_end:
        insert_pos = start_pos + title_end.end()
        new_content = content[:insert_pos] + expansion + content[insert_pos:]
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Chapter {chapter_num} expanded successfully")
        return True
    
    return False

def main():
    """Main function to expand all chapters"""
    
    file_path = "/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/AutoML_Gluon_Complete_Manual_Reading_Friendly.html"
    
    # Define chapters to expand
    chapters = [
        (6, "Валидация моделей"),
        (7, "Продакшен и деплой"),
        (8, "Переобучение моделей"),
        (9, "Лучшие практики"),
        (10, "Примеры использования"),
        (11, "Troubleshooting"),
        (12, "Apple Silicon оптимизация"),
        (13, "Простой пример продакшена"),
        (14, "Сложный пример продакшена"),
        (15, "Теория и основы AutoML"),
        (16, "Интерпретируемость"),
        (17, "Продвинутые темы"),
        (18, "Этика и ответственный AI"),
        (19, "Кейс-стади"),
        (20, "WAVE2 Индикатор"),
        (21, "SCHR Levels Индикатор"),
        (22, "SCHR SHORT3 Индикатор"),
        (23, "Супер-система"),
        (24, "Руководство по изучению"),
        (25, "Правильное использование вероятностей"),
        (26, "Мониторинг торгового бота")
    ]
    
    success_count = 0
    
    for chapter_num, chapter_title in chapters:
        try:
            if expand_chapter(file_path, chapter_num, chapter_title):
                success_count += 1
        except Exception as e:
            print(f"Error expanding chapter {chapter_num}: {e}")
    
    print(f"Successfully expanded {success_count} out of {len(chapters)} chapters")

if __name__ == "__main__":
    main()
