#!/usr/bin/env python3
"""
Script to translate Russian text in project files to English.
Excludes files in russian/ directories and files with -ru.md suffix.
"""

import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import List, Tuple

# Comprehensive translation patterns for Russian phrases
# Order matters: longer phrases first
TRANSLATION_PATTERNS = {
 # Long specific phrases (must come first)
 r'AutoML Gluon installation': 'AutoML Gluon installation',
 r'Why Proper installation is Critical': 'Why Proper installation is Critical',
 r'Real Consequences of Incorrect installation': 'Real Consequences of Incorrect installation',
 r'Что происходит при неправильной установке\?': 'What Happens with Incorrect installation?',
 r'Конфликты dependencies': 'Dependency Conflicts',
 r'Issues with производительностью': 'Performance Issues',
 r'Ошибки компиляции': 'Compilation Errors',
 r'Issues with GPU': 'GPU Issues',
 r'Troubleshooting': 'Troubleshooting',
 r'Common Issues': 'Common Issues',
 r'installation Issues': 'installation Issues',
 r'Launch Issues': 'Launch Issues',
 r'import Errors': 'import Errors',
 r'Port Issues': 'Port Issues',
 r'Frequently Asked Questions': 'Frequently Asked Questions',
 r'Project Structure': 'Project Structure',
 r'Run and Test Guides': 'Run and Test Guides',
 r'Russian Version': 'Russian Version',
 r'English Version': 'English Version',
 r'Common Resources': 'Common Resources',

 # Common documentation phrases
 r'\bобновление\b': 'update',
 r'\bдобавление\b': 'add',
 r'\bудаление\b': 'remove',
 r'\bисправление\b': 'fix',
 r'\bулучшение\b': 'improve',
 r'\bсоздание\b': 'create',
 r'\bнастройка\b': 'configuration',
 r'\bустановка\b': 'installation',
 r'\bруководство\b': 'guide',
 r'\bдокументация\b': 'documentation',
 r'\bпример\b': 'example',
 r'\bпримеры\b': 'examples',
 r'\bописание\b': 'describe',
 r'\bинструкция\b': 'instruction',
 r'\bинструкции\b': 'instructions',
 r'\bзависимость\b': 'dependency',
 r'\bзависимости\b': 'dependencies',
 r'\bмодуль\b': 'module',
 r'\bмодули\b': 'modules',
 r'\bфункция\b': 'function',
 r'\bфункции\b': 'functions',
 r'\bпараметр\b': 'parameter',
 r'\bпараметры\b': 'parameters',
 r'\bконфигурация\b': 'configuration',
 r'\bнастройки\b': 'Settings',

 # Code comments and docstrings
 r'Comprehensive solution for': 'Comprehensive solution for',
 r'Решает \d+ основные задачи': lambda m: f'Solves {m.group(1)} main tasks',
 r'Prediction': 'Prediction',
 r'Author:': 'Author:',
 r'Version:': 'Version:',

 # Common words (lower priority)
 r'\bдля\b': 'for',
 r'\bпо\b': 'on',
 r'\bс\b': 'with',
 r'\bи\b': 'and',
 r'\bили\b': 'or',
 r'\bв\b': 'in',
 r'\bна\b': 'on',
 r'\bот\b': 'from',
 r'\bдо\b': 'to',
}

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
 r'^\./Logs/.*',
 r'^\./models/.*',
 r'^\./results/.*',
 r'^\./\.venv/.*',
 r'^\./venv/.*',
 r'^\./\.uv/.*',
 r'^\./uv_cache/.*',
]

# File extensions to process
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
 # Count Russian lines
 russian_lines = sum(1 for line in content.split('\n') if has_russian_text(line))
 files_with_russian.append((rel_path, russian_lines))
 except Exception as e:
 print(f"Warning: Could not read {rel_path}: {e}")

 return sorted(files_with_russian)


def translate_text(text: str) -> str:
 """Translate Russian text to English Using patterns."""
 if not has_russian_text(text):
 return text

 translated = text

 # Apply translation patterns (longer patterns first)
 for pattern, replacement in TRANSLATION_PATTERNS.items():
 if callable(replacement):
 translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)
 else:
 translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)

 # clean up multiple spaces (but preserve newlines in markdown)
 lines = translated.split('\n')
 cleaned_lines = []
 for line in lines:
 # Preserve markdown Structure
 if line.strip().startswith('#') or line.strip().startswith('*') or line.strip().startswith('-'):
 cleaned_lines.append(re.sub(r'[ \t]+', ' ', line))
 else:
 cleaned_lines.append(re.sub(r'[ \t]+', ' ', line))

 translated = '\n'.join(cleaned_lines)

 return translated


def main():
 """main function."""
 parser = argparse.ArgumentParser(describe='Translate Russian text in project files to English')
 parser.add_argument('--dry-run', action='store_true', help='Show files that would be translated without making changes')
 parser.add_argument('--file', type=str, help='Translate specific file only')
 parser.add_argument('--yes', '-y', action='store_true', help='Automatically proceed without confirmation')
 args = parser.parse_args()

 print("Scanning project for files with Russian text...")
 print("Excluding: russian/ directories, *-ru.md files, and data/Logs/models directories")
 print()

 if args.file:
 files_to_process = [(args.file, 0)]
 else:
 files_to_process = find_files_with_russian()

 if not files_to_process:
 print("No files with Russian text found (excluding Russian-specific files).")
 return

 print(f"found {len(files_to_process)} files with Russian text:")
 print()

 total_lines = 0
 for file_path, line_count in files_to_process[:20]:
 print(f" {file_path} ({line_count} lines with Russian text)")
 total_lines += line_count

 if len(files_to_process) > 20:
 print(f" ... and {len(files_to_process) - 20} more files")

 print()
 print(f"Total: {len(files_to_process)} files, {total_lines} lines with Russian text")
 print()

 if args.dry_run:
 print("[DRY RUN] No changes will be made.")
 return

 if not args.yes:
 response = input("Proceed with translation? This will modify files. (yes/no): ")
 if response.lower() != 'yes':
 print("Aborted.")
 return

 print()
 print("starting translation...")
 print("Note: This script Uses pattern-based translation.")
 print("Complex sentences may require manual reView.")
 print()

 translated_count = 0
 skipped_count = 0

 for file_path, line_count in files_to_process:
 full_path = os.path.join('.', file_path)

 try:
 with open(full_path, 'r', encoding='utf-8') as f:
 original_content = f.read()

 if not has_russian_text(original_content):
 skipped_count += 1
 continue

 # Translate content
 translated_content = translate_text(original_content)

 # Only write if content changed
 if translated_content != original_content:
 with open(full_path, 'w', encoding='utf-8') as f:
 f.write(translated_content)
 translated_count += 1
 print(f"✓ Translated: {file_path}")
 else:
 skipped_count += 1

 except Exception as e:
 print(f"✗ Error processing {file_path}: {e}")

 print()
 print(f"Translation complete!")
 print(f" Translated: {translated_count} files")
 print(f" Skipped: {skipped_count} files")
 print()
 print("Note: Please reView translated files for accuracy.")
 print("Complex sentences may need manual correction.")


if __name__ == '__main__':
 main()

