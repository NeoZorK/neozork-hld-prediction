#!/usr/bin/env python3
"""
Translate specific lines in files using line numbers from count_russian_files.py output.
Format: file_path:line1,line2,line3
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from collections import OrderedDict

# Check for requests library
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Comprehensive translation patterns (expanded from translate_files_advanced.py)
# Order matters: longer, more specific phrases first
TRANSLATIONS = OrderedDict([
    # Image alt text and common phrases
 (r'architecture\s+([A-Z][a-zA-Z\s]+)', r'Architecture \1'),
 (r'architecture\s+([a-z][a-zA-Z\s]+)', r'architecture \1'),
 (r'comparison\s+([а-яА-Я\s]+)', r'Comparison \1'),
 (r'comparison\s+([а-яА-Я\s]+)', r'comparison \1'),
 (r'methods\s+([а-яА-Я\s]+)', r'Methods \1'),
 (r'methods\s+([а-яА-Я\s]+)', r'methods \1'),
 (r'workflow\s+process\s+([а-яА-Я\s]+)', r'Workflow \1'),
 (r'workflow\s+process\s+([а-яА-Я\s]+)', r'workflow \1'),
 (r'metrics\s+([а-яА-Я\s]+)', r'Metrics \1'),
 (r'metrics\s+([а-яА-Я\s]+)', r'metrics \1'),
    
    # Common documentation phrases
 (r'\bобновление\b', 'update'),
 (r'\bдобавление\b', 'add'),
 (r'\bудаление\b', 'remove'),
 (r'\bисправление\b', 'fix'),
 (r'\bулучшение\b', 'improve'),
 (r'\bсоздание\b', 'create'),
 (r'\bнастройка\b', 'configuration'),
 (r'\bустановка\b', 'installation'),
 (r'\bруководство\b', 'guide'),
 (r'\bдокументация\b', 'documentation'),
 (r'\bпример\b', 'example'),
 (r'\bпримеры\b', 'examples'),
 (r'\bописание\b', 'description'),
 (r'\bинструкция\b', 'instruction'),
 (r'\bинструкции\b', 'instructions'),
 (r'\bзависимость\b', 'dependency'),
 (r'\bзависимости\b', 'dependencies'),
 (r'\bмодуль\b', 'module'),
 (r'\bмодули\b', 'modules'),
 (r'\bфункция\b', 'function'),
 (r'\bфункции\b', 'functions'),
 (r'\bпараметр\b', 'parameter'),
 (r'\bпараметры\b', 'parameters'),
 (r'\bконфигурация\b', 'configuration'),
 (r'\bнастройки\b', 'settings'),
 (r'\bиндикаторов\b', 'indicators'),
 (r'\bпроверка\b', 'check'),
 (r'\bочистка\b', 'clean'),
 (r'\bкэша\b', 'cache'),
 (r'\bпереустановка\b', 'reinstall'),
 (r'\bпроизводительности\b', 'performance'),
 (r'\bпроизводительность\b', 'performance'),
 (r'\bархитектура\b', 'architecture'),
 (r'\bАрхитектура\b', 'Architecture'),
 (r'\bсравнение\b', 'comparison'),
 (r'\bСравнение\b', 'Comparison'),
 (r'\bметоды\b', 'methods'),
 (r'\bМетоды\b', 'Methods'),
 (r'\bпроцесс\b', 'process'),
 (r'\bПроцесс\b', 'Process'),
 (r'\bрабочий\b', 'workflow'),
 (r'\bРабочий\b', 'Workflow'),
 (r'\bметрики\b', 'metrics'),
 (r'\bМетрики\b', 'Metrics'),
 (r'\bвалидации\b', 'validation'),
 (r'\bвалидация\b', 'validation'),
 (r'\bВалидация\b', 'Validation'),
 (r'\bпереобучения\b', 'retraining'),
 (r'\bпереобучение\b', 'retraining'),
 (r'\bПереобучение\b', 'Retraining'),
    
    # Common words
 (r'\bдля\b', 'for'),
 (r'\bпо\b', 'on'),
 (r'\bс\b', 'with'),
 (r'\bи\b', 'and'),
 (r'\bили\b', 'or'),
 (r'\bв\b', 'in'),
 (r'\bна\b', 'on'),
 (r'\bот\b', 'from'),
 (r'\bдо\b', 'to'),
 (r'\bне\b', 'not'),
])


def has_russian_text(text: str) -> bool:
    """Check if text contains Cyrillic characters."""
 return bool(re.search(r'[А-Яа-яЁё]', text))


def translate_text_pattern_based(text: str) -> str:
    """Translate Russian text to English using comprehensive patterns."""
    if not has_russian_text(text):
        return text

    translated = text
    # Apply translations in order (longer patterns first)
    for pattern, replacement in TRANSLATIONS.items():
        translated = re.sub(pattern, replacement, translated, flags=re.MULTILINE | re.IGNORECASE)

    # Clean up multiple spaces but preserve structure
    lines = translated.split('\n')
    cleaned_lines = []
    for line in lines:
        if (line.strip().startswith('#') or
            line.strip().startswith('*') or
            line.strip().startswith('-') or
            line.strip().startswith('```') or
            line.strip().startswith('`')):
            cleaned_lines.append(re.sub(r'[ \t]+', ' ', line.rstrip()))
        else:
            cleaned_lines.append(re.sub(r'[ \t]+', ' ', line.rstrip()))
    return '\n'.join(cleaned_lines)


def translate_with_mymemory(text: str, max_length: int = 500) -> Optional[str]:
    """Translate text using MyMemory Translation API (free)."""
    if not HAS_REQUESTS:
        return None

    if len(text) > max_length:
        # Split long text into chunks
        chunks = []
        sentences = re.split(r'([.!?]\s+)', text)
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        translated_chunks = []
        for chunk in chunks:
            translated = translate_with_mymemory(chunk, max_length)
            if translated:
                translated_chunks.append(translated)
                import time
                time.sleep(0.5)  # Rate limiting
            else:
                translated_chunks.append(chunk)

        return ''.join(translated_chunks)

    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": "ru|en"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('responseStatus') == 200:
                return result['responseData']['translatedText']
    except Exception as e:
        print(f"  Warning: MyMemory API error: {e}", file=sys.stderr)

    return None


def translate_text(text: str, use_api: bool = True) -> str:
    """Translate Russian text to English."""
    if not has_russian_text(text):
        return text

    # Try API first for better quality
    if use_api and HAS_REQUESTS:
        api_translated = translate_with_mymemory(text)
        if api_translated and api_translated != text:
            # Clean up the API translation
            translated = api_translated.strip()
            # Apply pattern-based fixes for common issues
            for pattern, replacement in TRANSLATIONS.items():
                translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)
            return translated

    # Fallback to pattern-based translation
    return translate_text_pattern_based(text)


def parse_line_numbers(line_nums_str: str) -> List[int]:
    """Parse comma-separated line numbers."""
    try:
        return [int(ln.strip()) for ln in line_nums_str.split(',') if ln.strip()]
    except ValueError:
        return []


def translate_file_lines(file_path: str, line_numbers: List[int], use_api: bool = True) -> Tuple[int, int]:
    """Translate specific lines in a file. Returns (translated_count, total_count)."""
    if not os.path.exists(file_path):
        print(f"  ✗ File not found: {file_path}")
        return (0, 0)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        translated_count = 0
        total_count = len(line_numbers)

        for line_num in line_numbers:
            if line_num < 1 or line_num > len(lines):
                continue

            original_line = lines[line_num - 1]
            if not has_russian_text(original_line):
                continue

            # Translate the line
            if use_api:
                translated_line = translate_text(original_line.rstrip('\n\r'), use_api=True)
            else:
                translated_line = translate_text_pattern_based(original_line.rstrip('\n\r'))
            
            # Preserve trailing newline if it existed
            if original_line.endswith('\n'):
                translated_line += '\n'
            elif original_line.endswith('\r'):
                translated_line += '\r'

            # Only update if translation changed something
            if translated_line != original_line:
                lines[line_num - 1] = translated_line
                translated_count += 1

        # Write back if any changes were made
        if translated_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

        return (translated_count, total_count)

    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}", file=sys.stderr)
        return (0, 0)


def process_lines_file(lines_file: str, max_files: int = 10, use_api: bool = True) -> None:
    """Process lines file and translate files."""
    if not os.path.exists(lines_file):
        print(f"Error: File not found: {lines_file}")
        return

    print(f"Reading line numbers from: {lines_file}")
    print(f"Processing up to {max_files} files...")
    print()

    files_processed = 0
    total_translated = 0
    total_lines = 0

    with open(lines_file, 'r', encoding='utf-8') as f:
        for line in f:
            if files_processed >= max_files:
                break

            line = line.strip()
            if not line:
                continue

            # Parse format: file_path:line1,line2,line3
            if ':' not in line:
                continue

            file_path, line_nums_str = line.split(':', 1)
            line_numbers = parse_line_numbers(line_nums_str)

            if not line_numbers:
                continue

            print(f"[{files_processed + 1}/{max_files}] Processing {file_path} ({len(line_numbers)} lines)...")

            translated, total = translate_file_lines(file_path, line_numbers, use_api=use_api)
            
            if translated > 0:
                print(f"  ✓ Translated {translated}/{total} lines")
                total_translated += translated
                total_lines += total
            else:
                print(f"  - No changes needed")

            files_processed += 1

            # Small delay to avoid rate limiting
            if use_api and HAS_REQUESTS:
                import time
                time.sleep(0.3)

    print()
    print("=" * 60)
    print(f"Summary: Processed {files_processed} files")
    print(f"  Translated: {total_translated} lines")
    print(f"  Total lines checked: {total_lines}")
    print("=" * 60)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Translate specific lines in files using line numbers from count_russian_files.py'
    )
    parser.add_argument(
        '--lines-file',
        type=str,
        required=True,
        help='File with line numbers (format: file_path:line1,line2,line3)'
    )
    parser.add_argument(
        '--max-files',
        type=int,
        default=10,
        help='Maximum number of files to process (default: 10)'
    )
    parser.add_argument(
        '--no-api',
        action='store_true',
        help='Disable API translation, use pattern-based only'
    )
    args = parser.parse_args()

    if args.no_api:
        print("Using pattern-based translation only")
    elif HAS_REQUESTS:
        print("✓ Using MyMemory Translation API (free)")
    else:
        print("Warning: 'requests' library not found. Using pattern-based translation only.")
        print("Install it with: pip install requests")

    print()

    process_lines_file(args.lines_file, args.max_files, use_api=not args.no_api)


if __name__ == '__main__':
    main()

