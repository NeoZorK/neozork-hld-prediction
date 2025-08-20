#!/usr/bin/env python3
"""
Script to fix import statements across the project.
Replaces relative imports with absolute imports from src package.
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix imports in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix relative imports from common
        content = re.sub(
            r'from \.\.\.\.common import',
            'from src.common import',
            content
        )
        content = re.sub(
            r'from \.\.\.\.common\.constants import',
            'from src.common.constants import',
            content
        )
        content = re.sub(
            r'from \.\.\.common import',
            'from src.common import',
            content
        )
        content = re.sub(
            r'from \.\.\.common\.constants import',
            'from src.common.constants import',
            content
        )
        content = re.sub(
            r'from \.\.common import',
            'from src.common import',
            content
        )
        content = re.sub(
            r'from \.\.common\.constants import',
            'from src.common.constants import',
            content
        )
        
        # Fix relative imports from calculation
        content = re.sub(
            r'from \.\.\.calculation\.',
            'from src.calculation.',
            content
        )
        content = re.sub(
            r'from \.\.calculation\.',
            'from src.calculation.',
            content
        )
        content = re.sub(
            r'from calculation\.',
            'from src.calculation.',
            content
        )
        
        # Fix relative imports from cli
        content = re.sub(
            r'from \.\.\.cli\.',
            'from src.cli.',
            content
        )
        content = re.sub(
            r'from \.\.cli\.',
            'from src.cli.',
            content
        )
        
        # Fix relative imports from plotting
        content = re.sub(
            r'from \.\.\.plotting\.',
            'from src.plotting.',
            content
        )
        content = re.sub(
            r'from \.\.plotting\.',
            'from src.plotting.',
            content
        )
        
        # Fix relative imports from data
        content = re.sub(
            r'from \.\.\.data\.',
            'from src.data.',
            content
        )
        content = re.sub(
            r'from \.\.data\.',
            'from src.data.',
            content
        )
        
        # Fix relative imports from eda
        content = re.sub(
            r'from \.\.\.eda\.',
            'from src.eda.',
            content
        )
        content = re.sub(
            r'from \.\.eda\.',
            'from src.eda.',
            content
        )
        
        # Fix relative imports from export
        content = re.sub(
            r'from \.\.\.export\.',
            'from src.export.',
            content
        )
        content = re.sub(
            r'from \.\.export\.',
            'from src.export.',
            content
        )
        
        # Fix relative imports from workflow
        content = re.sub(
            r'from \.\.\.workflow\.',
            'from src.workflow.',
            content
        )
        content = re.sub(
            r'from \.\.workflow\.',
            'from src.workflow.',
            content
        )
        
        # Fix relative imports from utils
        content = re.sub(
            r'from \.\.\.utils\.',
            'from src.utils.',
            content
        )
        content = re.sub(
            r'from \.\.utils\.',
            'from src.utils.',
            content
        )
        
        # Fix relative imports from __version__
        content = re.sub(
            r'from \.\. import __version__',
            'from src import __version__',
            content
        )
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed imports in: {file_path}")
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix imports across the project."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src"
    
    if not src_dir.exists():
        print("Error: src directory not found!")
        return
    
    fixed_count = 0
    total_files = 0
    
    # Process all Python files in src directory
    for py_file in src_dir.rglob("*.py"):
        if py_file.is_file():
            total_files += 1
            if fix_imports_in_file(py_file):
                fixed_count += 1
    
    print(f"\nImport fixing completed!")
    print(f"Total Python files processed: {total_files}")
    print(f"Files with imports fixed: {fixed_count}")

if __name__ == "__main__":
    main() 