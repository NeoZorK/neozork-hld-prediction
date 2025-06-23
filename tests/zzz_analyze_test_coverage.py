#!/usr/bin/env python3
"""
Script for analyzing test coverage of modules in src/ and project root
This script runs as the last test to show a summary of test coverage
"""

import os
import sys
from pathlib import Path

def get_src_files():
    """Get all Python files from src/ and project root, excluding __init__.py files"""
    src_dir = Path("src")
    root_dir = Path(".")
    src_files = []
    # src/
    for py_file in src_dir.rglob("*.py"):
        if "__pycache__" in str(py_file) or "egg-info" in str(py_file) or py_file.name == "__init__.py":
            continue
        src_files.append(py_file)
    # root/
    for py_file in root_dir.glob("*.py"):
        if py_file.name == Path(__file__).name or py_file.name == "__init__.py":
            continue  # don't include the analyzer itself or __init__.py files
        src_files.append(py_file.resolve())
    return sorted(set(src_files))

def get_test_files():
    """Get all test files"""
    tests_dir = Path("tests")
    test_files = []
    for py_file in tests_dir.rglob("test_*.py"):
        test_files.append(py_file)
    return sorted(test_files)

def map_test_to_src(test_file):
    """Map test file to source file"""
    relative_path = test_file.relative_to(Path("tests"))
    module_name = relative_path.stem.replace("test_", "")
    
    # Handle special cases
    if module_name.endswith("_indicator"):
        module_name = module_name.replace("_indicator", "_ind")
    elif module_name.endswith("_fetcher"):
        module_name = module_name.replace("_fetcher", "_fetcher")
    
    # If test is in tests/src/, then source file is in src/
    if relative_path.parts[0] == "src":
        # Skip 'src' in relative path
        src_subpath = Path(*relative_path.parts[1:-1])
        src_path = Path("src") / src_subpath / f"{module_name}.py"
        return [src_path]
    
    # For tests in tests/ root (e.g., test_fix_imports.py for scripts/fix_imports.py)
    root_path = Path(f"{module_name}.py")
    src_path = Path("src") / relative_path.parent / f"{module_name}.py"
    return [src_path, root_path]

def analyze_coverage():
    """Analyze test coverage"""
    src_files = get_src_files()
    test_files = get_test_files()
    
    # Create mapping of tests to source files
    test_to_src = {}
    for test_file in test_files:
        src_paths = map_test_to_src(test_file)
        test_to_src[test_file] = src_paths
    
    # Analyze coverage
    covered_files = set()
    missing_tests = []
    
    for test_file, src_paths in test_to_src.items():
        found = False
        for src_file in src_paths:
            if src_file.exists():
                covered_files.add(src_file.resolve())
                found = True
        if not found:
            print(f"⚠️  Test {test_file} doesn't match source file")
    
    # Find files without tests
    for src_file in src_files:
        if src_file.resolve() not in covered_files:
            missing_tests.append(src_file)
    
    # Output results
    print(f"📊 TEST COVERAGE ANALYSIS")
    print(f"=" * 50)
    print(f"Total files in src/ and root: {len(src_files)}")
    print(f"Total tests: {len(test_files)}")
    print(f"Covered by tests: {len(covered_files)}")
    print(f"Not covered by tests: {len(missing_tests)}")
    print(f"Coverage: {len(covered_files)/len(src_files)*100:.1f}%")
    print()
    
    if missing_tests:
        print("📝 FILES WITHOUT TESTS:")
        print("-" * 30)
        for file in missing_tests:
            print(f"❌ {file}")
        print()
        
        # Group by modules
        modules = {}
        for file in missing_tests:
            module = file.parent.name
            if module not in modules:
                modules[module] = []
            modules[module].append(file.name)
        
        print("📁 GROUPING BY MODULES:")
        print("-" * 30)
        for module, files in sorted(modules.items()):
            print(f"\n🔸 {module}/ ({len(files)} files):")
            for file in files:
                print(f"   - {file}")
    
    return missing_tests

if __name__ == "__main__":
    missing_tests = analyze_coverage()
    sys.exit(1 if missing_tests else 0) 