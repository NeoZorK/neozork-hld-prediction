#!/usr/bin/env python3
"""
Оптимизация изображений и исправление markdown файлов
Создание правильных .md файлов с оптимизированными изображениями

Автор: NeoZorK (Shcherbyna Rostyslav)
Дата: 2025
"""

import os
import subprocess
import sys
from pathlib import Path
from PIL import Image
import re

def install_pillow():
    """Установка Pillow если не установлен"""
    try:
        from PIL import Image
        return True
    except ImportError:
        print("📦 Устанавливаем Pillow...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'Pillow'], check=True)
        try:
            from PIL import Image
            return True
        except ImportError:
            print("✗ Не удалось установить Pillow")
            return False

def optimize_image(input_path, output_path, max_width=800, quality=85):
    """Оптимизация изображения"""
    
    try:
        with Image.open(input_path) as img:
            # Конвертируем в RGB если нужно
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Вычисляем новые размеры
            width, height = img.size
            if width > max_width:
                new_height = int((height * max_width) / width)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Сохраняем с оптимизацией
            img.save(output_path, 'PNG', optimize=True, quality=quality)
            
            # Получаем размеры файлов
            original_size = os.path.getsize(input_path)
            optimized_size = os.path.getsize(output_path)
            compression_ratio = (1 - optimized_size / original_size) * 100
            
            print(f"  ✓ {os.path.basename(input_path)}: {original_size//1024}KB → {optimized_size//1024}KB ({compression_ratio:.1f}% сжатие)")
            
            return True
            
    except Exception as e:
        print(f"  ✗ Ошибка оптимизации {input_path}: {e}")
        return False

def optimize_all_images():
    """Оптимизация всех изображений"""
    
    print("=== Оптимизация изображений ===")
    
    if not install_pillow():
        return False
    
    # Определение путей
    project_root = Path(__file__).parent.parent.parent.parent.parent
    images_dir = project_root / "docs" / "automl" / "gluon" / "images"
    optimized_dir = images_dir / "optimized"
    
    # Создаем папку для оптимизированных изображений
    optimized_dir.mkdir(exist_ok=True)
    
    # Находим все изображения
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(images_dir.glob(f'*{ext}'))
    
    print(f"Найдено изображений: {len(image_files)}")
    
    optimized_count = 0
    for img_path in image_files:
        output_path = optimized_dir / img_path.name
        
        if optimize_image(img_path, output_path):
            optimized_count += 1
    
    print(f"✅ Оптимизировано изображений: {optimized_count}/{len(image_files)}")
    return optimized_count > 0

def fix_markdown_images(md_file_path):
    """Исправление ссылок на изображения в markdown файле"""
    
    print(f"Исправляем изображения в: {md_file_path.name}")
    
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем пути к изображениям на оптимизированные
        content = re.sub(
            r'!\[([^\]]*)\]\(images/([^)]+)\)',
            r'![\1](images/optimized/\2)',
            content
        )
        
        # Добавляем размеры изображений для лучшего отображения
        content = re.sub(
            r'!\[([^\]]*)\]\(images/optimized/([^)]+)\)',
            r'<img src="images/optimized/\2" alt="\1" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">',
            content
        )
        
        # Сохраняем исправленный файл
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Исправлен: {md_file_path.name}")
        return True
        
    except Exception as e:
        print(f"  ✗ Ошибка исправления {md_file_path.name}: {e}")
        return False

def fix_all_markdown_files():
    """Исправление всех markdown файлов"""
    
    print("\n=== Исправление markdown файлов ===")
    
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
            if fix_markdown_images(md_path):
                fixed_count += 1
        else:
            print(f"  ⚠️  Файл не найден: {md_file}")
    
    print(f"✅ Исправлено файлов: {fixed_count}/{len(md_files)}")
    return fixed_count > 0

def create_optimized_html():
    """Создание оптимизированного HTML"""
    
    print("\n=== Создание оптимизированного HTML ===")
    
    # Запускаем наш улучшенный конвертер
    script_path = Path(__file__).parent / "convert_all_md_to_html_enhanced.py"
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, cwd=script_path.parent)
        
        if result.returncode == 0:
            print("✅ Оптимизированный HTML создан успешно!")
            return True
        else:
            print(f"✗ Ошибка создания HTML: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Ошибка запуска конвертера: {e}")
        return False

def create_optimized_pdf():
    """Создание оптимизированного PDF"""
    
    print("\n=== Создание оптимизированного PDF ===")
    
    # Запускаем Playwright конвертер
    script_path = Path(__file__).parent / "create_pdf_with_playwright.py"
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, cwd=script_path.parent)
        
        if result.returncode == 0:
            print("✅ Оптимизированный PDF создан успешно!")
            return True
        else:
            print(f"✗ Ошибка создания PDF: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Ошибка запуска конвертера: {e}")
        return False

def main():
    """Основная функция"""
    
    print("🚀 Оптимизация изображений и создание правильных файлов")
    print("Автор: NeoZorK (Shcherbyna Rostyslav)")
    print("Дата: 2025")
    print("Местоположение: Ukraine, Zaporizhzhya")
    
    # Шаг 1: Оптимизация изображений
    if not optimize_all_images():
        print("⚠️  Не удалось оптимизировать изображения")
        return False
    
    # Шаг 2: Исправление markdown файлов
    if not fix_all_markdown_files():
        print("⚠️  Не удалось исправить markdown файлы")
        return False
    
    # Шаг 3: Создание оптимизированного HTML
    if not create_optimized_html():
        print("⚠️  Не удалось создать HTML")
        return False
    
    # Шаг 4: Создание оптимизированного PDF
    if not create_optimized_pdf():
        print("⚠️  Не удалось создать PDF")
        return False
    
    print("\n🎉 Все файлы созданы успешно!")
    print("📄 Проверьте папку docs/automl/gluon/")
    
    return True

if __name__ == "__main__":
    main()
