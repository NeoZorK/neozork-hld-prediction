#!/usr/bin/env python3
"""
Script for fixing imports in test files.
Replaces relative imports with absolute ones.
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fixes imports in a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace relative imports with absolute ones
    # from ...src. -> from src.
    # from ....src. -> from src.
    content = re.sub(r'from \.\.\.\.src\.', 'from src.', content)
    content = re.sub(r'from \.\.\.src\.', 'from src.', content)
    content = re.sub(r'from \.\.src\.', 'from src.', content)
    content = re.sub(r'from \.src\.', 'from src.', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed file: {file_path}")

def main():
    """Main function for fixing all files."""
    test_dir = Path("tests/calculation/indicators")
    
    if not test_dir.exists():
        print(f"Directory {test_dir} not found")
        return
    
    # Find all Python files in the test directory
    python_files = list(test_dir.rglob("*.py"))
    
    print(f"Found {len(python_files)} Python files to fix")
    
    for file_path in python_files:
        fix_imports_in_file(file_path)
    
    print("All imports fixed!")

if __name__ == "__main__":
    main() 