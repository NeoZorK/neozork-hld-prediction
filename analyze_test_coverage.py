#!/usr/bin/env python3
"""
Скрипт для анализа покрытия тестами модулей в src/ и в корне проекта
"""

import os
import sys
from pathlib import Path

def get_src_files():
    """Получить все Python файлы из src/ и из корня проекта"""
    src_dir = Path("src")
    root_dir = Path(".")
    src_files = []
    # src/
    for py_file in src_dir.rglob("*.py"):
        if "__pycache__" in str(py_file) or "egg-info" in str(py_file):
            continue
        src_files.append(py_file)
    # root/
    for py_file in root_dir.glob("*.py"):
        if py_file.name == Path(__file__).name:
            continue  # не включаем сам анализатор
        src_files.append(py_file.resolve())
    return sorted(set(src_files))

def get_test_files():
    """Получить все тестовые файлы"""
    tests_dir = Path("tests")
    test_files = []
    for py_file in tests_dir.rglob("test_*.py"):
        test_files.append(py_file)
    return sorted(test_files)

def map_test_to_src(test_file):
    """Сопоставить тестовый файл с исходным файлом"""
    relative_path = test_file.relative_to(Path("tests"))
    module_name = relative_path.stem.replace("test_", "")
    
    # Обрабатываем специальные случаи
    if module_name.endswith("_indicator"):
        module_name = module_name.replace("_indicator", "_ind")
    elif module_name.endswith("_fetcher"):
        module_name = module_name.replace("_fetcher", "_fetcher")
    
    # Если тест находится в tests/src/, то исходный файл в src/
    if relative_path.parts[0] == "src":
        # Пропускаем 'src' в относительном пути
        src_subpath = Path(*relative_path.parts[1:-1])
        src_path = Path("src") / src_subpath / f"{module_name}.py"
        return [src_path]
    
    # Для тестов в корне tests/ (например, test_fix_imports.py)
    root_path = Path(f"{module_name}.py")
    src_path = Path("src") / relative_path.parent / f"{module_name}.py"
    return [src_path, root_path]

def analyze_coverage():
    """Анализировать покрытие тестами"""
    src_files = get_src_files()
    test_files = get_test_files()
    
    # Создаем маппинг тестов к исходным файлам
    test_to_src = {}
    for test_file in test_files:
        src_paths = map_test_to_src(test_file)
        test_to_src[test_file] = src_paths
    
    # Анализируем покрытие
    covered_files = set()
    missing_tests = []
    
    for test_file, src_paths in test_to_src.items():
        found = False
        for src_file in src_paths:
            if src_file.exists():
                covered_files.add(src_file.resolve())
                found = True
        if not found:
            print(f"⚠️  Тест {test_file} не соответствует исходному файлу")
    
    # Находим файлы без тестов
    for src_file in src_files:
        if src_file.resolve() not in covered_files:
            missing_tests.append(src_file)
    
    # Выводим результаты
    print(f"📊 АНАЛИЗ ПОКРЫТИЯ ТЕСТАМИ")
    print(f"=" * 50)
    print(f"Всего файлов в src/ и root: {len(src_files)}")
    print(f"Всего тестов: {len(test_files)}")
    print(f"Покрыто тестами: {len(covered_files)}")
    print(f"Не покрыто тестами: {len(missing_tests)}")
    print(f"Покрытие: {len(covered_files)/len(src_files)*100:.1f}%")
    print()
    
    if missing_tests:
        print("📝 ФАЙЛЫ БЕЗ ТЕСТОВ:")
        print("-" * 30)
        for file in missing_tests:
            print(f"❌ {file}")
        print()
        
        # Группируем по модулям
        modules = {}
        for file in missing_tests:
            module = file.parent.name
            if module not in modules:
                modules[module] = []
            modules[module].append(file.name)
        
        print("📁 ГРУППИРОВКА ПО МОДУЛЯМ:")
        print("-" * 30)
        for module, files in sorted(modules.items()):
            print(f"\n🔸 {module}/ ({len(files)} файлов):")
            for file in files:
                print(f"   - {file}")
    
    return missing_tests

if __name__ == "__main__":
    missing_tests = analyze_coverage()
    sys.exit(1 if missing_tests else 0) 