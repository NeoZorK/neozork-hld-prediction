#!/usr/bin/env python3
"""
Script to count files with Russian text requiring translation to English.
Includes Russian text in code comments.
Excludes files in russian/ directories, files with -ru.md suffix, and files with both RU and ENG versions.
"""

import argparse
import os
import re
from pathlib import Path
from typing import List, Tuple, Dict, Set
from collections import defaultdict


# files and directories to exclude
EXCLUDE_PATTERNS = [
 r'.*/russian/.*',
 r'.*-ru\.md$',
 r'.*_ru\.md$',
 r'.*\.ru\..*',
 r'^\./\.git/.*',
 r'^\./node_modules/.*',
 r'^\./__pycache__/.*',
 r'^\./data/.*',
 r'^\./logs/.*',
 r'^\./models/.*',
 r'^\./results/.*',
 r'^\./\.venv/.*',
 r'^\./venv/.*',
 r'^\./\.uv/.*',
 r'^\./uv_cache/.*',
]

INCLUDE_EXTENSIONS = {'.py', '.md', '.txt', '.json', '.yaml', '.yml', '.ts', '.tsx', '.js', '.jsx', '.vue', '.sh'}


def should_exclude_file(file_path: str) -> bool:
    """check if file should be excluded from translation."""
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def has_russian_text(text: str) -> bool:
 """check if text contains Cyrillic characters."""
 return bool(re.search(r'[А-Яа-яЁё]', text))


def get_base_filename(file_path: str) -> str:
 """Get base filename without language suffixes."""
 path = Path(file_path)
 name = path.stem

 # Remove language suffixes
 name = re.sub(r'[-_]ru$', '', name)
 name = re.sub(r'[-_]en$', '', name)

 return name


def find_english_version(file_path: str, root_dir: str = '.') -> bool:
 """
 check if file has corresponding English Version.
 Returns True if English Version exists, False otherwise.
 """
 path = Path(file_path)
 dir_path = path.parent
 base_name = get_base_filename(file_path)
 ext = path.suffix

 # check various patterns for English Version
 possible_english_names = [
 f"{base_name}-en{ext}",
 f"{base_name}_en{ext}",
 f"{base_name}-en.md",
 f"{base_name}_en.md",
 f"{base_name}{ext}", # Same name without suffix
 ]

 # check in same directory
 for eng_name in possible_english_names:
 eng_path = dir_path / eng_name
 if eng_path.exists() and eng_path != Path(file_path):
 return True

 # check in english/ directory (if file is in russian/)
 if 'russian' in str(dir_path):
 english_dir = str(dir_path).replace('russian', 'english')
 if os.path.exists(english_dir):
 for eng_name in possible_english_names:
 eng_path = Path(english_dir) / eng_name
 if eng_path.exists():
 return True

 # check if there's an english/ directory at the same level
 parent_dir = dir_path.parent
 english_dir = parent_dir / 'english'
 if english_dir.exists() and english_dir.is_dir():
 for eng_name in possible_english_names:
 eng_path = english_dir / eng_name
 if eng_path.exists():
 return True

 # For files without suffix, check if there's a -en.md or _en.md version
 if not re.search(r'[-_]ru', str(path)):
 # check for -en.md or _en.md versions
 for eng_name in [f"{base_name}-en.md", f"{base_name}_en.md"]:
 eng_path = dir_path / eng_name
 if eng_path.exists():
 return True

 return False


def find_files_with_russian(root_dir: str = '.') -> List[Tuple[str, int]]:
 """Find all files containing Russian text."""
 files_with_russian = []

 for root, dirs, files in os.walk(root_dir):
 # Skip excluded directories
 dirs[:] = [d for d in dirs if not should_exclude_file(os.path.join(root, d))]

 for file in files:
 file_path = os.path.join(root, file)
 rel_path = os.path.relpath(file_path, root_dir)

 if should_exclude_file(rel_path):
 continue

 ext = Path(file).suffix
 if ext not in INCLUDE_EXTENSIONS:
 continue

 try:
 with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
 content = f.read()
 if has_russian_text(content):
 russian_lines = sum(1 for line in content.split('\n') if has_russian_text(line))
 files_with_russian.append((rel_path, russian_lines))
 except Exception as e:
 print(f"Warning: Could not read {rel_path}: {e}")

 return sorted(files_with_russian)


def filter_files_requiring_translation(files_with_russian: List[Tuple[str, int]], root_dir: str = '.') -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]:
 """
 Filter files requiring translation, excluding those with both RU and ENG versions.
 Returns: (files_requiring_translation, files_with_both_versions)
 """
 files_requiring = []
 files_with_both = []

 for file_path, line_count in files_with_russian:
 if find_english_version(file_path, root_dir):
 files_with_both.append((file_path, line_count))
 else:
 files_requiring.append((file_path, line_count))

 return files_requiring, files_with_both


def group_by_extension(files: List[Tuple[str, int]]) -> Dict[str, List[Tuple[str, int]]]:
 """Group files by extension."""
 grouped = defaultdict(List)
 for file_path, line_count in files:
 ext = Path(file_path).suffix or '(no extension)'
 grouped[ext].append((file_path, line_count))
 return dict(grouped)


def group_by_directory(files: List[Tuple[str, int]]) -> Dict[str, List[Tuple[str, int]]]:
 """Group files by top-level directory."""
 grouped = defaultdict(List)
 for file_path, line_count in files:
 parts = Path(file_path).parts
 top_dir = parts[0] if len(parts) > 1 else '.'
 grouped[top_dir].append((file_path, line_count))
 return dict(grouped)


def print_statistics(
 all_files: List[Tuple[str, int]],
 files_requiring: List[Tuple[str, int]],
 files_with_both: List[Tuple[str, int]],
 summary_only: bool = False
) -> None:
 """Print statistics about files with Russian text."""
 total_files = len(all_files)
 requiring_count = len(files_requiring)
 both_versions_count = len(files_with_both)

 total_lines_all = sum(count for _, count in all_files)
 total_lines_requiring = sum(count for _, count in files_requiring)
 total_lines_both = sum(count for _, count in files_with_both)

 print("=" * 80)
 print("files WITH RUSSIAN TEXT - STATISTICS")
 print("=" * 80)
 print()
 print(f"Total files with Russian text: {total_files} ({total_lines_all} lines)")
 print(f"files requiring translation: {requiring_count} ({total_lines_requiring} lines)")
 print(f"files with both RU and ENG versions (excluded): {both_versions_count} ({total_lines_both} lines)")
 print()

 if summary_only:
 return

 # Group by extension
 print("=" * 80)
 print("BREAKDOWN BY FILE TYPE")
 print("=" * 80)
 print()

 grouped_by_ext = group_by_extension(files_requiring)
 for ext in sorted(grouped_by_ext.keys()):
 files_List = grouped_by_ext[ext]
 total_lines = sum(count for _, count in files_List)
 print(f"{ext:15} {len(files_List):4} files, {total_lines:5} lines")

 print()

 # Group by directory
 print("=" * 80)
 print("BREAKDOWN BY DIRECTORY")
 print("=" * 80)
 print()

 grouped_by_dir = group_by_directory(files_requiring)
 for dir_name in sorted(grouped_by_dir.keys()):
 files_List = grouped_by_dir[dir_name]
 total_lines = sum(count for _, count in files_List)
 print(f"{dir_name:30} {len(files_List):4} files, {total_lines:5} lines")

 print()

 # Detailed List
 print("=" * 80)
 print("Detailed List OF files REQUIRING TRANSLATION")
 print("=" * 80)
 print()

 for file_path, line_count in files_requiring:
 print(f" {file_path:60} ({line_count:4} lines)")

 if files_with_both:
 print()
 print("=" * 80)
 print("files WITH BOTH RU AND ENG VERSIONS (EXCLUDED FROM TRANSLATION)")
 print("=" * 80)
 print()

 for file_path, line_count in files_with_both:
 print(f" {file_path:60} ({line_count:4} lines)")


def main():
 """main function."""
 parser = argparse.ArgumentParser(
 description='Count files with Russian text requiring translation to English'
 )
 parser.add_argument(
 '--output', '-o',
 type=str,
 help='Save Report to file'
 )
 parser.add_argument(
 '--summary-only',
 action='store_true',
 help='Show only summary statistics without Detailed List'
 )
 parser.add_argument(
 '--root',
 type=str,
 default='.',
 help='Root directory to scan (default: current directory)'
 )
 args = parser.parse_args()

 print("Scanning project for files with Russian text...")
 print("Excluding: russian/ directories, *-ru.md files, and files with both RU and ENG versions")
 print()

 files_with_russian = find_files_with_russian(args.root)

 if not files_with_russian:
 print("No files with Russian text found (excluding Russian-specific files).")
 return

 files_requiring, files_with_both = filter_files_requiring_translation(files_with_russian, args.root)

 # Print to console
 print_statistics(files_with_russian, files_requiring, files_with_both, args.summary_only)

 # Save to file if requested
 if args.output:
 import sys
 original_stdout = sys.stdout
 try:
 with open(args.output, 'w', encoding='utf-8') as f:
 sys.stdout = f
 print_statistics(files_with_russian, files_requiring, files_with_both, args.summary_only)
 sys.stdout = original_stdout
 print(f"\nReport saved to: {args.output}")
 except Exception as e:
 sys.stdout = original_stdout
 print(f"Error saving Report to {args.output}: {e}")


if __name__ == '__main__':
 main()
