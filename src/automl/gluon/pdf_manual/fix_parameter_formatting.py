#!/usr/bin/env python3
"""
Исправление форматирования параметров в markdown файлах
Исправление проблем с отображением списков параметров

Автор: NeoZorK (Shcherbyna Rostyslav)
Дата: 2025
"""

import re
from pathlib import Path

def fix_parameter_sections(content):
    """Исправление разделов с параметрами"""
    
    # Исправляем проблему с "Рекомендуемые значения": - `3600`
    content = re.sub(
        r'(\*\*Рекомендуемые значения\*\*:)\s*-\s*`([^`]+)`',
        r'\1\n  - `\2`',
        content
    )
    
    # Исправляем другие подобные проблемы
    content = re.sub(
        r'(\*\*[^*]+\*\*:)\s*-\s*`([^`]+)`',
        r'\1\n  - `\2`',
        content
    )
    
    # Исправляем проблемы с вложенными списками
    content = re.sub(
        r'(\*\*[^*]+\*\*:)\s*-\s*\*\*([^*]+)\*\*:',
        r'\1\n  - **\2**:',
        content
    )
    
    return content

def fix_markdown_file(file_path):
    """Исправление markdown файла"""
    
    print(f"Исправляем: {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Исправляем форматирование параметров
        content = fix_parameter_sections(content)
        
        # Сохраняем исправленный файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Исправлен: {file_path.name}")
        return True
        
    except Exception as e:
        print(f"  ✗ Ошибка: {e}")
        return False

def main():
    """Основная функция"""
    
    print("🔧 Исправление форматирования параметров")
    
    # Определение путей
    project_root = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    # Файлы с проблемами
    problem_files = [
        "01_installation.md",
        "02_basic_usage.md", 
        "03_advanced_configuration.md",
        "04_metrics.md"
    ]
    
    fixed_count = 0
    for md_file in problem_files:
        md_path = docs_dir / md_file
        if md_path.exists():
            if fix_markdown_file(md_path):
                fixed_count += 1
    
    print(f"\n✅ Исправлено файлов: {fixed_count}")
    return True

if __name__ == "__main__":
    main()
