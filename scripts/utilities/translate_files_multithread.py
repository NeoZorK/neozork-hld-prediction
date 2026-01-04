#!/usr/bin/env python3
"""
Fast multithreaded local translation of Russian text to English using transformers.
Translates all Russian text in files found by count_russian_files.py.
100% offline, no API required. Super fast with multithreading!
"""

import argparse
import os
import re
import sys
import json
import threading
from pathlib import Path
from typing import List, Tuple, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

try:
    from transformers import MarianMTModel, MarianTokenizer
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    print("Error: transformers and torch required. Install with: uv add transformers torch", file=sys.stderr)
    sys.exit(1)


# Thread-safe model loading
_model_lock = threading.Lock()
_model = None
_tokenizer = None


def load_model():
    """Load translation model (thread-safe, cached after first load)."""
    global _model, _tokenizer
    with _model_lock:
        if _model is None or _tokenizer is None:
            print("Loading translation model (first time, may take a moment)...", flush=True)
            model_name = "Helsinki-NLP/opus-mt-ru-en"
            _tokenizer = MarianTokenizer.from_pretrained(model_name)
            _model = MarianMTModel.from_pretrained(model_name)
            _model.eval()
            print("✓ Model loaded", flush=True)
    return _model, _tokenizer


def has_russian_text(text: str) -> bool:
    """Check if text contains Cyrillic characters."""
    return bool(re.search(r'[А-Яа-яЁё]', text))


def translate_text(text: str, cache: Dict[str, str] = None, cache_lock: threading.Lock = None) -> str:
    """Translate Russian text to English using transformers model (thread-safe)."""
    if cache is None:
        cache = {}
    
    # Check cache first (thread-safe)
    if cache_lock:
        with cache_lock:
            if text in cache:
                return cache[text]
    else:
        if text in cache:
            return cache[text]
    
    if not has_russian_text(text):
        if cache_lock:
            with cache_lock:
                cache[text] = text
        else:
            cache[text] = text
        return text
    
    try:
        # Use model lock to prevent concurrent model access
        with _model_lock:
            model, tokenizer = load_model()
            
            # Tokenize and translate
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            
            with torch.no_grad():
                translated = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
            
            result = tokenizer.decode(translated[0], skip_special_tokens=True)
        
        # Save to cache (thread-safe)
        if cache_lock:
            with cache_lock:
                cache[text] = result
        else:
            cache[text] = result
        
        return result
    except Exception as e:
        print(f"  Warning: Translation error for text (first 50 chars): '{text[:50]}...': {e}", file=sys.stderr, flush=True)
        result = text
        if cache_lock:
            with cache_lock:
                cache[text] = result
        else:
            cache[text] = result
        return result


def translate_line(line: str, cache: Dict[str, str] = None, cache_lock: threading.Lock = None) -> str:
    """Translate a single line if it contains Russian text."""
    if not has_russian_text(line):
        return line
    
    return translate_text(line, cache, cache_lock)


def process_file(file_path: str, root_dir: str = '.', cache: Dict[str, str] = None, 
                 cache_lock: threading.Lock = None, dry_run: bool = False) -> Tuple[bool, int, str]:
    """
    Process a file and translate Russian text to English.
    Returns (success, lines_translated_count, file_path)
    """
    full_path = os.path.join(root_dir, file_path) if root_dir != '.' else file_path
    
    if not os.path.exists(full_path):
        return False, 0, file_path
    
    try:
        # Read file with timeout protection
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Limit file size to prevent memory issues
        if len(lines) > 10000:
            print(f"  ⚠ Skipping {file_path}: too large ({len(lines)} lines)", file=sys.stderr, flush=True)
            return False, 0, file_path
        
        translated_lines = []
        lines_translated = 0
        lines_processed = 0
        
        for line in lines:
            lines_processed += 1
            original_line = line.rstrip('\n\r')
            
            # Skip very long lines
            if len(original_line) > 2000:
                translated_lines.append(line)
                continue
            
            if has_russian_text(original_line):
                translated_line = translate_line(original_line, cache, cache_lock)
                translated_lines.append(translated_line + '\n')
                if translated_line != original_line:
                    lines_translated += 1
            else:
                translated_lines.append(line)
            
            # Progress indicator for large files
            if lines_processed % 100 == 0:
                print(f"    Processing {file_path}: {lines_processed}/{len(lines)} lines...", file=sys.stderr, flush=True)
        
        if lines_translated > 0 and not dry_run:
            # Write with backup
            backup_path = full_path + '.bak'
            try:
                import shutil
                shutil.copy2(full_path, backup_path)
            except:
                pass
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.writelines(translated_lines)
        
        return True, lines_translated, file_path
    
    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc()
        return False, 0, file_path


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


def save_translation_cache(cache: Dict[str, str], cache_file: str, cache_lock: threading.Lock = None) -> None:
    """Save translation cache to file (thread-safe)."""
    try:
        if cache_lock:
            with cache_lock:
                cache_copy = cache.copy()
        else:
            cache_copy = cache.copy()
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_copy, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save cache: {e}", file=sys.stderr)


def process_file_wrapper(args_tuple):
    """Wrapper for process_file to work with ThreadPoolExecutor."""
    file_path, root_dir, cache, cache_lock, dry_run = args_tuple
    return process_file(file_path, root_dir, cache, cache_lock, dry_run)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Fast multithreaded local translation of Russian text to English using transformers'
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
        '--batch-size',
        type=int,
        default=5,
        help='Number of files to process in one batch (default: 5)'
    )
    parser.add_argument(
        '--threads',
        type=int,
        default=10,
        help='Number of threads to use (default: 10)'
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
    print("FAST MULTITHREADED LOCAL TRANSLATION (TRANSFORMERS - 100% OFFLINE)")
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
        response = input(f"Translate Russian text in {len(files_to_process)} files using {args.threads} threads? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return
    
    print(f"\nProcessing {len(files_to_process)} files in batches of {args.batch_size} using {args.threads} threads...\n")
    
    # Thread-safe cache
    cache_lock = threading.Lock()
    total_lines_translated = 0
    successful_files = 0
    failed_files = 0
    processed_count = 0
    
    # Process in batches
    for batch_start in range(0, len(files_to_process), args.batch_size):
        batch_end = min(batch_start + args.batch_size, len(files_to_process))
        batch = files_to_process[batch_start:batch_end]
        batch_num = batch_start // args.batch_size + 1
        total_batches = (len(files_to_process) + args.batch_size - 1) // args.batch_size
        
        print(f"\n{'='*80}")
        print(f"Batch {batch_num}/{total_batches} ({len(batch)} files)")
        print(f"{'='*80}\n")
        
        # Prepare arguments for threads
        file_args = [
            (file_path, args.root, cache, cache_lock, args.dry_run)
            for file_path, _ in batch
        ]
        
        # Process batch with ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(process_file_wrapper, args): args[0]
                for args in file_args
            }
            
            # Process completed tasks with progress
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                processed_count += 1
                progress_percent = (processed_count / len(files_to_process)) * 100
                
                try:
                    success, lines_count, _ = future.result()
                    
                    if success:
                        if lines_count > 0:
                            print(f"[{processed_count}/{len(files_to_process)}] ({progress_percent:.1f}%) ✓ {file_path}: {lines_count} lines translated", flush=True)
                            total_lines_translated += lines_count
                        else:
                            print(f"[{processed_count}/{len(files_to_process)}] ({progress_percent:.1f}%) ✓ {file_path}: (no changes)", flush=True)
                        successful_files += 1
                    else:
                        print(f"[{processed_count}/{len(files_to_process)}] ({progress_percent:.1f}%) ✗ {file_path}: failed", flush=True)
                        failed_files += 1
                except Exception as e:
                    print(f"[{processed_count}/{len(files_to_process)}] ({progress_percent:.1f}%) ✗ {file_path}: error - {e}", flush=True)
                    failed_files += 1
        
        # Save cache after each batch
        save_translation_cache(cache, args.cache_file, cache_lock)
        print(f"\n✓ Batch {batch_num} completed. Cache saved.")
    
    # Final cache save
    save_translation_cache(cache, args.cache_file, cache_lock)
    
    print()
    print("=" * 80)
    print("TRANSLATION SUMMARY")
    print("=" * 80)
    print(f"  Files processed: {len(files_to_process)}")
    print(f"  Successful: {successful_files}")
    print(f"  Failed: {failed_files}")
    print(f"  Total lines translated: {total_lines_translated}")
    print(f"  Cache size: {len(cache)} translations")
    print(f"  Threads used: {args.threads}")
    if args.dry_run:
        print("  [DRY RUN] No files were modified")
    print("=" * 80)


if __name__ == '__main__':
    main()

