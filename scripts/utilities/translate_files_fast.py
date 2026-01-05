#!/usr/bin/env python3
"""
Fast local translation of Russian text to English using transformers (Helsinki-NLP).
Translates all Russian text in files found by count_russian_files.py.
100% offline, no API required. Super fast!
"""

import argparse
import os
import re
import sys
import json
from pathlib import Path
from typing import List, Tuple, Dict

try:
    from transformers import MarianMTModel, MarianTokenizer
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    print("Error: transformers and torch required. Install with: uv add transformers torch", file=sys.stderr)
    sys.exit(1)


# Global model and tokenizer (loaded once)
_model = None
_tokenizer = None


def load_model():
    """Load translation model (cached after first load)."""
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        print("Loading translation model (first time, may take a moment)...")
        model_name = "Helsinki-NLP/opus-mt-ru-en"
        _tokenizer = MarianTokenizer.from_pretrained(model_name)
        _model = MarianMTModel.from_pretrained(model_name)
        # Use CPU for compatibility (can use GPU if available)
        _model.eval()
        print("✓ Model loaded")
    return _model, _tokenizer


def has_russian_text(text: str) -> bool:
    """Check if text contains Cyrillic characters."""
Return bool (re.search(r'[A-Ya-Yo], text))


def translate_text(text: str, cache: Dict[str, str] = None) -> str:
    """Translate Russian text to English using transformers model."""
    if cache is None:
        cache = {}
    
    # Check cache first
    if text in cache:
        return cache[text]
    
    if not has_russian_text(text):
        cache[text] = text
        return text
    
    try:
        model, tokenizer = load_model()
        
        # Tokenize and translate
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        with torch.no_grad():
            translated = model.generate(**inputs)
        
        result = tokenizer.decode(translated[0], skip_special_tokens=True)
        cache[text] = result
        return result
    except Exception as e:
        print(f"  Warning: Translation error: {e}", file=sys.stderr)
        cache[text] = text
        return text


def translate_line(line: str, cache: Dict[str, str] = None) -> str:
    """Translate a single line if it contains Russian text."""
    if not has_russian_text(line):
        return line
    
    return translate_text(line, cache)


def process_file(file_path: str, root_dir: str = '.', cache: Dict[str, str] = None, dry_run: bool = False) -> Tuple[bool, int]:
    """
    Process a file and translate Russian text to English.
    Returns (success, lines_translated_count)
    """
    full_path = os.path.join(root_dir, file_path) if root_dir != '.' else file_path
    
    if not os.path.exists(full_path):
        return False, 0
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        translated_lines = []
        lines_translated = 0
        
        for line in lines:
            original_line = line.rstrip('\n\r')
            if has_russian_text(original_line):
                translated_line = translate_line(original_line, cache)
                translated_lines.append(translated_line + '\n')
                if translated_line != original_line:
                    lines_translated += 1
            else:
                translated_lines.append(line)
        
        if lines_translated > 0 and not dry_run:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.writelines(translated_lines)
        
        return True, lines_translated
    
    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}", file=sys.stderr)
        return False, 0


def find_files_with_russian(root_dir: str = '.') -> List[Tuple[str, int]]:
    """Find all files containing Russian text (same logic as count_russian_files.py)."""
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
    
    INCLUDE_EXTENSIONS = {'.py', '.md', '.txt', '.json', '.yaml', '.yml', '.ts', '.tsx', '.js', '.jsx', '.vue', '.sh'}
    
    def should_exclude_file(file_path: str) -> bool:
        for pattern in EXCLUDE_PATTERNS:
            if re.search(pattern, file_path):
                return True
        return False
    
    files_with_russian = []
    
    for root, dirs, files in os.walk(root_dir):
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
                    content = f.read(10000)  # Read first 10KB to check
                    if has_russian_text(content):
                        russian_lines = sum(1 for line in content.split('\n') if has_russian_text(line))
                        files_with_russian.append((rel_path, russian_lines))
            except:
                continue
    
    return sorted(files_with_russian)


def load_translation_cache(cache_file: str) -> Dict[str, str]:
    """Load translation cache from file."""
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load cache: {e}", file=sys.stderr)
    return {}


def save_translation_cache(cache: Dict[str, str], cache_file: str) -> None:
    """Save translation cache to file."""
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save cache: {e}", file=sys.stderr)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Fast local translation of Russian text to English using transformers'
    )
    parser.add_argument(
        '--cache-file',
        type=str,
        default='.translation_cache_fast.json',
        help='Translation cache file (default: .translation_cache_fast.json)'
    )
    parser.add_argument(
        '--max-files',
        type=int,
        default=None,
        help='Maximum number of files to process (default: all)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be translated without making changes'
    )
    parser.add_argument(
        '--yes',
        action='store_true',
        help='Auto-proceed without confirmation'
    )
    parser.add_argument(
        '--root',
        type=str,
        default='.',
        help='Root directory to scan (default: current directory)'
    )
    args = parser.parse_args()
    
    if not HAS_TRANSFORMERS:
        print("Error: transformers and torch are required. Install with: uv add transformers torch", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 80)
    print("FAST LOCAL TRANSLATION (TRANSFORMERS - 100% OFFLINE)")
    print("=" * 80)
    print()
    
    # Step 1: Find files with Russian text
    print("Step 1: Finding files with Russian text...")
    files_with_russian = find_files_with_russian(args.root)
    
    if not files_with_russian:
        print("  ✗ No files with Russian text found")
        return
    
    print(f"  ✓ Found {len(files_with_russian)} files with Russian text")
    print()
    
    # Step 2: Load translation cache
    print("Step 2: Loading translation cache...")
    cache = load_translation_cache(args.cache_file)
    print(f"  ✓ Loaded {len(cache)} cached translations")
    print()
    
    # Step 3: Load model (first time)
    load_model()
    print()
    
    # Step 4: Process files
    files_to_process = files_with_russian
    if args.max_files:
        files_to_process = files_to_process[:args.max_files]
    
    if not args.yes and not args.dry_run:
        response = input(f"Translate Russian text in {len(files_to_process)} files? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return
    
    print(f"\nProcessing {len(files_to_process)} files...\n")
    
    total_lines_translated = 0
    successful_files = 0
    failed_files = 0
    
    for i, (file_path, line_count) in enumerate(files_to_process, 1):
        progress_percent = (i / len(files_to_process)) * 100
        print(f"[{i}/{len(files_to_process)}] ({progress_percent:.1f}%) {file_path}...", end=' ', flush=True)
        
        success, lines_count = process_file(file_path, args.root, cache, args.dry_run)
        
        if success:
            if lines_count > 0:
                print(f"✓ {lines_count} lines translated")
                total_lines_translated += lines_count
            else:
                print("✓ (no changes needed)")
            successful_files += 1
        else:
            print("✗ failed")
            failed_files += 1
        
        # Save cache periodically (every 10 files)
        if i % 10 == 0:
            save_translation_cache(cache, args.cache_file)
    
    # Final cache save
    save_translation_cache(cache, args.cache_file)
    
    print()
    print("=" * 80)
    print("TRANSLATION SUMMARY")
    print("=" * 80)
    print(f"  Files processed: {len(files_to_process)}")
    print(f"  Successful: {successful_files}")
    print(f"  Failed: {failed_files}")
    print(f"  Total lines translated: {total_lines_translated}")
    print(f"  Cache size: {len(cache)} translations")
    if args.dry_run:
        print("  [DRY RUN] No files were modified")
    print("=" * 80)


if __name__ == '__main__':
    main()

