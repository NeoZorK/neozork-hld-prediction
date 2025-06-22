#!/usr/bin/env python3
"""
Скрипт для исправления импортов в тестовых файлах.
Заменяет относительные импорты на абсолютные.
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Исправляет импорты в одном файле."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем относительные импорты на абсолютные
    # from ...src. -> from src.
    # from ....src. -> from src.
    content = re.sub(r'from \.\.\.\.src\.', 'from src.', content)
    content = re.sub(r'from \.\.\.src\.', 'from src.', content)
    content = re.sub(r'from \.\.src\.', 'from src.', content)
    content = re.sub(r'from \.src\.', 'from src.', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Исправлен файл: {file_path}")

def main():
    """Основная функция для исправления всех файлов."""
    test_dir = Path("tests/calculation/indicators")
    
    if not test_dir.exists():
        print(f"Директория {test_dir} не найдена")
        return
    
    # Находим все Python файлы в директории тестов
    python_files = list(test_dir.rglob("*.py"))
    
    print(f"Найдено {len(python_files)} Python файлов для исправления")
    
    for file_path in python_files:
        fix_imports_in_file(file_path)
    
    print("Все импорты исправлены!")

if __name__ == "__main__":
    main() 