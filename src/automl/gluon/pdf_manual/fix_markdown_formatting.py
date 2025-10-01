#!/usr/bin/env python3
"""
Исправление форматирования в markdown файлах
Исправление проблем с отображением списков и параметров

Автор: NeoZorK (Shcherbyna Rostyslav)
Дата: 2025
"""

import os
import re
from pathlib import Path

def fix_parameter_formatting(content):
    """Исправление форматирования параметров"""
    
    # Исправляем форматирование параметров
    # Ищем паттерн "**Параметр `name`:**" и исправляем следующие списки
    
    # Паттерн для поиска параметров
    param_pattern = r'\*\*Параметр `([^`]+)`:\*\*'
    
    # Разбиваем контент на части
    parts = re.split(param_pattern, content)
    
    if len(parts) < 2:
        return content
    
    result = []
    i = 0
    
    while i < len(parts):
        if i == 0:
            # Первая часть (до первого параметра)
            result.append(parts[i])
        elif i % 2 == 1:
            # Название параметра
            param_name = parts[i]
            result.append(f"**Параметр `{param_name}`:**")
        else:
            # Описание параметра
            param_desc = parts[i]
            
            # Исправляем форматирование списков в описании
            param_desc = fix_list_formatting(param_desc)
            result.append(param_desc)
        
        i += 1
    
    return ''.join(result)

def fix_list_formatting(text):
    """Исправление форматирования списков"""
    
    # Исправляем списки, которые начинаются с "- **Что означает**:"
    # Заменяем на правильное markdown форматирование
    
    lines = text.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Исправляем строки с параметрами
        if line.strip().startswith('- **Что означает**:'):
            fixed_lines.append(f"\n- **Что означает**: {line.split('**: ', 1)[1] if '**: ' in line else line.split('**:')[1]}")
        elif line.strip().startswith('- **Зачем нужен**:'):
            fixed_lines.append(f"- **Зачем нужен**: {line.split('**: ', 1)[1] if '**: ' in line else line.split('**:')[1]}")
        elif line.strip().startswith('- **Рекомендуемые значения**:'):
            fixed_lines.append(f"- **Рекомендуемые значения**:")
        elif line.strip().startswith('- **Что происходит при превышении**:'):
            fixed_lines.append(f"- **Что происходит при превышении**: {line.split('**: ', 1)[1] if '**: ' in line else line.split('**:')[1]}")
        elif line.strip().startswith('- **Практический пример**:'):
            fixed_lines.append(f"- **Практический пример**: {line.split('**: ', 1)[1] if '**: ' in line else line.split('**:')[1]}")
        elif line.strip().startswith('- **Детальная настройка'):
            fixed_lines.append(f"- **{line.split('- **')[1].split('**:')[0]}**:")
        elif line.strip().startswith('- **Влияние на качество модели**:'):
            fixed_lines.append(f"- **Влияние на качество модели**:")
        elif line.strip().startswith('- **Оптимизация по ресурсам**:'):
            fixed_lines.append(f"- **Оптимизация по ресурсам**:")
        elif line.strip().startswith('- **Мониторинг'):
            fixed_lines.append(f"- **{line.split('- **')[1].split('**:')[0]}**:")
        elif line.strip().startswith('- **Выбор типа усреднения**:'):
            fixed_lines.append(f"- **Выбор типа усреднения**:")
        elif line.strip().startswith('- **Параметр `'):
            # Это подпараметры, добавляем правильное форматирование
            fixed_lines.append(f"\n- **{line.split('- **')[1].split('**:')[0]}**:")
        elif line.strip().startswith('  - **'):
            # Вложенные списки
            fixed_lines.append(f"  - **{line.split('  - **')[1].split('**:')[0]}**: {line.split('**: ', 1)[1] if '**: ' in line else ''}")
        elif line.strip().startswith('  - `'):
            # Значения параметров
            fixed_lines.append(line)
        elif line.strip().startswith('- **'):
            # Другие параметры
            if '**:' in line:
                param_name = line.split('- **')[1].split('**:')[0]
                param_value = line.split('**: ', 1)[1] if '**: ' in line else ''
                fixed_lines.append(f"- **{param_name}**: {param_value}")
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_markdown_file(file_path):
    """Исправление markdown файла"""
    
    print(f"Исправляем: {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Исправляем форматирование параметров
        content = fix_parameter_formatting(content)
        
        # Дополнительные исправления
        # Исправляем проблемы с отображением списков
        content = re.sub(r'-\s*\*\*([^*]+)\*\*:\s*([^\n]+)', r'- **\1**: \2', content)
        
        # Исправляем вложенные списки
        content = re.sub(r'^  -\s*\*\*([^*]+)\*\*:\s*([^\n]+)', r'  - **\1**: \2', content, flags=re.MULTILINE)
        
        # Исправляем пустые строки между параметрами
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # Сохраняем исправленный файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Исправлен: {file_path.name}")
        return True
        
    except Exception as e:
        print(f"  ✗ Ошибка исправления {file_path.name}: {e}")
        return False

def main():
    """Основная функция"""
    
    print("🔧 Исправление форматирования в markdown файлах")
    print("Автор: NeoZorK (Shcherbyna Rostyslav)")
    print("Дата: 2025")
    
    # Определение путей
    project_root = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    # Список всех markdown файлов
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
    
    fixed_count = 0
    for md_file in md_files:
        md_path = docs_dir / md_file
        if md_path.exists():
            if fix_markdown_file(md_path):
                fixed_count += 1
        else:
            print(f"  ⚠️  Файл не найден: {md_file}")
    
    print(f"\n✅ Исправлено файлов: {fixed_count}/{len(md_files)}")
    
    if fixed_count > 0:
        print("\n🔄 Теперь пересоздадим HTML и PDF с исправленным форматированием...")
        
        # Пересоздаем HTML
        from create_final_optimized_manual import create_final_html
        if create_final_html():
            print("✅ HTML пересоздан с исправленным форматированием")
        
        # Пересоздаем PDF
        from create_pdf_with_playwright import create_pdf_with_playwright
        if create_pdf_with_playwright():
            print("✅ PDF пересоздан с исправленным форматированием")
    
    print("\n🎉 Форматирование исправлено!")
    return True

if __name__ == "__main__":
    main()
