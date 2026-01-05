#!/usr/bin/env python3
"""
Safe fast translation of Russian text to English using transformers.
Processes files sequentially but with progress tracking and caching.
100% offline, no API required.
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
    
    # Split long texts into sentences
    if len(text) > 500:
        # Split by sentence boundaries
        sentences = re.split(r'([.!?]\s+)', text)
        translated_parts = []
        current_chunk = ""
        
        for part in sentences:
            if len(current_chunk) + len(part) <= 500:
                current_chunk += part
            else:
                if current_chunk:
                    translated_parts.append(translate_text(current_chunk.strip(), cache))
                current_chunk = part
        
        if current_chunk:
            translated_parts.append(translate_text(current_chunk.strip(), cache))
        
        result = ''.join(translated_parts)
        cache[text] = result
        return result
    
    try:
        model, tokenizer = load_model()
        
        # Tokenize and translate
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        with torch.no_grad():
            translated = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
        
        result = tokenizer.decode(translated[0], skip_special_tokens=True)
        cache[text] = result
        return result
    except Exception as e:
        print(f"    ⚠ Translation error: {e}", file=sys.stderr, flush=True)
        cache[text] = text
        return text


def translate_line(line: str, cache: Dict[str, str] = None) -> str:
    """Translate a single line if it contains Russian text."""
    if not has_russian_text(line):
        return line
    
    return translate_text(line, cache)


def process_file(file_path: str, root_dir: str = '.', cache: Dict[str, str] = None, 
                 dry_run: bool = False) -> Tuple[bool, int, str]:
    """
    Process a file and translate Russian text to English.
    Returns (success, lines_translated_count, file_path)
    """
    full_path = os.path.join(root_dir, file_path) if root_dir != '.' else file_path
    
    if not os.path.exists(full_path):
        return False, 0, file_path
    
    try:
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Process large files in chunks
        is_large_file = len(lines) > 5000
        if is_large_file:
            print(f"    ⚠ Large file detected: {len(lines)} lines, processing in chunks...", file=sys.stderr, flush=True)
        
        translated_lines = []
        lines_translated = 0
        total_lines = len(lines)
        
        # Process in chunks for large files
        chunk_size = 1000 if is_large_file else total_lines
        chunks = [lines[i:i + chunk_size] for i in range(0, total_lines, chunk_size)]
        
        for chunk_num, chunk in enumerate(chunks, 1):
            if is_large_file:
                print(f"      Processing chunk {chunk_num}/{len(chunks)} ({len(chunk)} lines)...", flush=True)
            
            for i, line in enumerate(chunk):
                line_index = (chunk_num - 1) * chunk_size + i + 1
                original_line = line.rstrip('\n\r')
                
                # Skip very long lines
                if len(original_line) > 2000:
                    translated_lines.append(line)
                    continue
                
                if has_russian_text(original_line):
                    translated_line = translate_line(original_line, cache)
                    translated_lines.append(translated_line + '\n')
                    if translated_line != original_line:
                        lines_translated += 1
                else:
                    translated_lines.append(line)
                
                # Progress indicator
                if total_lines > 50:
                    if line_index % max(1, total_lines // 20) == 0 or line_index == total_lines:
                        progress = (line_index * 100) // total_lines
                        print(f"      [{progress}%] {line_index}/{total_lines} lines processed", flush=True)
        
        if lines_translated > 0 and not dry_run:
            # Create backup
            backup_path = full_path + '.bak'
            try:
                import shutil
                if not os.path.exists(backup_path):
                    shutil.copy2(full_path, backup_path)
            except:
                pass
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.writelines(translated_lines)
        
        return True, lines_translated, file_path
    
    except Exception as e:
        print(f"    ✗ Error: {e}", file=sys.stderr, flush=True)
        return False, 0, file_path


def find_files_with_russian(root_dir: str = '.') -> List[Tuple[str, int]]:
    """Find all files containing Russian text."""
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
                    content = f.read(10000)
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
        description='Safe fast translation of Russian text to English using transformers'
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
        default=3,
        help='Number of files to process in one batch (default: 3)'
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
    print("SAFE FAST TRANSLATION (TRANSFORMERS - 100% OFFLINE)")
    print("=" * 80)
    print()
    
    # Step 1: Find files
    print("Step 1: Finding files with Russian text...")
    files_with_russian = find_files_with_russian(args.root)
    
    if not files_with_russian:
        print("  ✗ No files with Russian text found")
        return
    
    print(f"  ✓ Found {len(files_with_russian)} files with Russian text")
    print()
    
    # Step 2: Load cache
    print("Step 2: Loading translation cache...")
    cache = load_translation_cache(args.cache_file)
    print(f"  ✓ Loaded {len(cache)} cached translations")
    print()
    
    # Step 3: Load model
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
    
    batch_size = args.batch_size if hasattr(args, 'batch_size') else 3
    total_batches = (len(files_to_process) + batch_size - 1) // batch_size
    
    print(f"\nProcessing {len(files_to_process)} files in batches of {batch_size}...\n")
    
    total_lines_translated = 0
    successful_files = 0
    failed_files = 0
    
    # Process in batches
    for batch_num in range(total_batches):
        batch_start = batch_num * batch_size
        batch_end = min(batch_start + batch_size, len(files_to_process))
        batch = files_to_process[batch_start:batch_end]
        
        print(f"{'='*80}")
        print(f"BATCH {batch_num + 1}/{total_batches} ({len(batch)} files)")
        print(f"{'='*80}\n")
        
        for i, (file_path, line_count) in enumerate(batch, 1):
            file_num = batch_start + i
            progress_percent = (file_num * 100) / len(files_to_process)
            print(f"[{file_num}/{len(files_to_process)}] ({progress_percent:.1f}%) {file_path}", flush=True)
            print(f"  Processing...", flush=True)
            
            success, lines_count, _ = process_file(file_path, args.root, cache, args.dry_run)
            
            if success:
                if lines_count > 0:
                    print(f"  ✓ {lines_count} lines translated\n", flush=True)
                    total_lines_translated += lines_count
                else:
                    print(f"  ✓ (no changes needed)\n", flush=True)
                successful_files += 1
            else:
                print(f"  ✗ failed\n", flush=True)
                failed_files += 1
        
        # Save cache after each batch
        save_translation_cache(cache, args.cache_file)
        print(f"💾 Batch {batch_num + 1} completed. Cache saved ({len(cache)} translations)\n", flush=True)
    
    # Final save
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

