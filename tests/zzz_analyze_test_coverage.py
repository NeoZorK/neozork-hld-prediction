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
    
    # If test is in tests/src/..., look for source in src/... with similar structure
    if relative_path.parts[0] == "src":
        src_subpath = Path(*relative_path.parts[1:-1])
        src_path = Path("src") / src_subpath / f"{module_name}.py"
        return [src_path]

    # If test is in tests/..., look for source in src/... with similar structure
    src_path = Path("src") / relative_path.parent / f"{module_name}.py"
    # Also look for tests in tests/src/... for this source file
    src_test_path = Path("tests/src") / relative_path.parent / f"test_{module_name}.py"
    if src_test_path.exists():
        return [src_path]
    return [src_path]

def analyze_coverage():
    """Analyze test coverage"""
    src_files = get_src_files()
    test_files = get_test_files()

    covered_files = set()
    missing_tests = []

    for src_file in src_files:
        try:
            rel = src_file.relative_to("src")
            test_path1 = Path("tests") / rel.parent / f"test_{rel.stem}.py"
            test_path2 = Path("tests/src") / rel.parent / f"test_{rel.stem}.py"
        except ValueError:
            # File not in src/, look for tests in tests/ root and tests/src/
            test_path1 = Path("tests") / f"test_{src_file.stem}.py"
            test_path2 = Path("tests/src") / f"test_{src_file.stem}.py"
        if test_path1.exists() or test_path2.exists():
            covered_files.add(src_file.resolve())
        else:
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