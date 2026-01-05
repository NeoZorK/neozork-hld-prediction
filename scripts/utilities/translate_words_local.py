#!/usr/bin/env python3
"""
Fast local translation script for Russian words without API.
Uses translate library for local translation.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATE = True
except ImportError:
    HAS_TRANSLATE = False
    print("Warning: deep-translator library not available", file=sys.stderr)


def has_russian_text(text: str) -> bool:
    """Check if text contains Cyrillic characters."""
Return bool (re.search(r'[A-Ya-Yo], text))


def translate_word_local(word: str, translator, cache: Dict[str, str] = None) -> str:
    """Translate a single word using local translator."""
    if cache is None:
        cache = {}
    
    # Check cache first
    if word in cache:
        return cache[word]
    
    # Skip if not Russian
    if not has_russian_text(word):
        return word
    
    try:
        # Translate word
        translated = translator.translate(word)
        if translated:
            result = translated.strip()
            # For single words, take only first word
            result = result.split()[0] if result.split() else result
            cache[word] = result
            return result
    except Exception as e:
        print(f"  Warning: Translation error for '{word}': {e}", file=sys.stderr)
    
    # Return original if translation failed
    cache[word] = word
    return word


def translate_words_batch_local(words: List[str], cache: Dict[str, str] = None) -> Dict[str, str]:
    """Translate a batch of words using local translator."""
    if not HAS_TRANSLATE:
        print("Error: deep-translator library not available", file=sys.stderr)
        return {}
    
    if cache is None:
        cache = {}
    
    # Initialize translator
    translator = GoogleTranslator(source='ru', target='en')
    
    translations = {}
    total = len(words)
    
    for i, word in enumerate(words, 1):
        if word not in cache:
            translated = translate_word_local(word, translator, cache)
            translations[word] = translated
            cache[word] = translated
            
            # Show progress for every 100 words
            if i % 100 == 0:
                progress = (i * 100) // total
                print(f"    Progress: {i}/{total} words translated ({progress}%)", file=sys.stderr)
        else:
            translations[word] = cache[word]
    
    if total > 100:
        print("", file=sys.stderr)  # New line after progress
    
    return translations


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


def parse_words_file(words_file: str) -> Tuple[Dict[str, List[str]], Set[str]]:
    """
    Parse words file from count_russian_files.py output.
    Returns (file_words_dict, all_words_set)
    """
    file_words_dict = {}
    all_words = set()
    
    if not os.path.exists(words_file):
        return file_words_dict, all_words
    
    with open(words_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse format:
    # # All unique Russian words found:
    # word1,word2,word3,...
    # # Words by file:
    # file_path:word1,word2,word3,...
    
    lines = content.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            if 'All unique' in line:
                current_section = 'all'
            elif 'Words by file' in line:
                current_section = 'files'
            continue
        
        if current_section == 'all':
            # Parse all words
            words = [w.strip() for w in line.split(',') if w.strip()]
            all_words.update(words)
        elif current_section == 'files':
            # Parse file:words
            if ':' in line:
                file_path, words_str = line.split(':', 1)
                words = [w.strip() for w in words_str.split(',') if w.strip()]
                file_words_dict[file_path] = words
                all_words.update(words)
    
    return file_words_dict, all_words


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Fast local translation of Russian words without API'
    )
    parser.add_argument(
        '--words-file',
        type=str,
        required=True,
        help='File with Russian words (from count_russian_files.py --words-output)'
    )
    parser.add_argument(
        '--cache-file',
        type=str,
        default='.translation_cache.json',
        help='Translation cache file (default: .translation_cache.json)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=1000,
        help='Number of words to translate in one batch (default: 1000)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file for translations (JSON format)'
    )
    args = parser.parse_args()
    
    if not HAS_TRANSLATE:
        print("Error: deep-translator library is required. Install with: uv add deep-translator", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 80)
    print("FAST LOCAL TRANSLATION (NO API)")
    print("=" * 80)
    print()
    
    # Step 1: Parse words file
    print("Step 1: Parsing words file...")
    file_words_dict, all_words = parse_words_file(args.words_file)
    
    if not all_words:
        print("  ✗ No words found in file")
        return
    
    print(f"  ✓ Found {len(all_words)} unique Russian words")
    print(f"  ✓ Found {len(file_words_dict)} files with Russian words")
    print()
    
    # Step 2: Load translation cache
    print("Step 2: Loading translation cache...")
    cache = load_translation_cache(args.cache_file)
    print(f"  ✓ Loaded {len(cache)} cached translations")
    print()
    
    # Step 3: Translate words
    print("Step 3: Translating words (local, no API)...")
    words_to_translate = [w for w in all_words if w not in cache]
    
    if words_to_translate:
        print(f"  Translating {len(words_to_translate)} new words...")
        
        # Translate in batches
        word_map = cache.copy()
        for i in range(0, len(words_to_translate), args.batch_size):
            batch = words_to_translate[i:i + args.batch_size]
            batch_num = i // args.batch_size + 1
            total_batches = (len(words_to_translate) + args.batch_size - 1) // args.batch_size
            print(f"    Batch {batch_num}/{total_batches}: {len(batch)} words...")
            translations = translate_words_batch_local(batch, cache)
            word_map.update(translations)
            print(f"      ✓ Translated {len(translations)} words")
            
            # Save cache after each batch
            save_translation_cache(cache, args.cache_file)
        
        print(f"  ✓ Saved {len(cache)} translations to cache")
    else:
        print("  ✓ All words already translated (using cache)")
        word_map = cache.copy()
    
    print()
    
    # Step 4: Save translations if output file specified
    if args.output:
        print(f"Step 4: Saving translations to {args.output}...")
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(word_map, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved {len(word_map)} translations")
        print()
    
    print("=" * 80)
    print("TRANSLATION SUMMARY")
    print("=" * 80)
    print(f"  Total unique words: {len(all_words)}")
    print(f"  Translated words: {len(word_map)}")
    print(f"  Cache size: {len(cache)}")
    print("=" * 80)


if __name__ == '__main__':
    main()

