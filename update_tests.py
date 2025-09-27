#!/usr/bin/env python3
"""
Script to update all test files to remove @pytest.mark.skip decorators.
"""

import os
import re
from pathlib import Path

def update_test_file(file_path):
    """Update a test file to remove @pytest.mark.skip decorators."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove @pytest.mark.skip lines
    content = re.sub(r'    @pytest\.mark\.skip\([^)]*\)\n', '', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {file_path}")

def main():
    """Update all test files."""
    test_dir = Path("src/automl/gluon/tests/")
    
    for test_file in test_dir.glob("test_*.py"):
        update_test_file(test_file)
    
    print("All test files updated!")

if __name__ == "__main__":
    main()
