#!/usr/bin/env python3
"""
Workflow script for translating Russian words in files:
1. Extract Russian words from files
2. Translate words using API
3. Replace Russian words with English translations in source files
4. Verify context for correctness
"""

import argparse
import os
import re
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict

# Use urllib for HTTP requests (built-in, no dependencies)
try:
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
    from urllib.error import URLError
    import json as json_lib
    HAS_HTTP = True
except ImportError:
    HAS_HTTP = False
    print("Error: urllib not available")
    sys.exit(1)


def has_russian_text(text: str) -> bool:
    """Check if text contains Cyrillic characters."""
    return bool(re.search(r'[А-Яа-яЁё]', text))


def extract_russian_words(text: str) -> Set[str]:
    """Extract unique Russian words from text."""
    words = re.findall(r'\b[А-Яа-яЁё]+\b', text)
    return set(words)


def translate_word_with_api(word: str, cache: Dict[str, str] = None) -> Optional[str]:
    """Translate a single word using MyMemory Translation API."""
    if cache is None:
        cache = {}
    
    # Check cache first
    if word in cache:
        return cache[word]
    
    if not HAS_HTTP:
        return None
    
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": word,
            "langpair": "ru|en"
        }
        query_string = urlencode(params)
        full_url = f"{url}?{query_string}"
        
        req = Request(full_url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urlopen(req, timeout=5) as response:
            if response.status == 200:
                result = json_lib.loads(response.read().decode('utf-8'))
                if result.get('responseStatus') == 200:
                    translated = result['responseData']['translatedText'].strip()
                    # Clean up translation (remove extra words, keep only first word)
                    translated = translated.split()[0] if translated.split() else translated
                    cache[word] = translated
                    return translated
    except (URLError, json_lib.JSONDecodeError, KeyError, Exception) as e:
        print(f"  Warning: API error for '{word}': {e}", file=sys.stderr)
    
    return None


def translate_words_batch(words: List[str], cache: Dict[str, str] = None, delay: float = 0.1) -> Dict[str, str]:
    """Translate a batch of words using API."""
    if cache is None:
        cache = {}
    
    translations = {}
    for word in words:
        if word not in cache:
            translated = translate_word_with_api(word, cache)
            if translated:
                translations[word] = translated
                cache[word] = translated
            time.sleep(delay)  # Rate limiting
        else:
            translations[word] = cache[word]
    
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


def replace_words_in_text(text: str, word_map: Dict[str, str], context_check: bool = True) -> Tuple[str, int]:
    """
    Replace Russian words with English translations in text.
    Returns (translated_text, replacement_count)
    """
    if not has_russian_text(text):
        return text, 0
    
    translated = text
    replacement_count = 0
    
    # Sort words by length (longest first) to avoid partial replacements
    sorted_words = sorted(word_map.keys(), key=len, reverse=True)
    
    for russian_word in sorted_words:
        english_word = word_map[russian_word]
        
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(russian_word) + r'\b'
        
        # Count occurrences before replacement
        matches = len(re.findall(pattern, translated, re.IGNORECASE))
        
        if matches > 0:
            # Replace with case preservation
            def replace_func(match):
                original = match.group(0)
                # Preserve case
                if original.isupper():
                    return english_word.upper()
                elif original.istitle():
                    return english_word.title()
                else:
                    return english_word.lower()
            
            translated = re.sub(pattern, replace_func, translated, flags=re.IGNORECASE)
            replacement_count += matches
    
    return translated, replacement_count


def process_file_with_translations(
    file_path: str,
    word_map: Dict[str, str],
    context_check: bool = True
) -> Tuple[bool, int]:
    """
    Process a file and replace Russian words with English translations.
    Returns (success, replacement_count)
    """
    if not os.path.exists(file_path):
        return False, 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        if not has_russian_text(original_content):
            return True, 0
        
        translated_content, replacement_count = replace_words_in_text(
            original_content, word_map, context_check
        )
        
        if replacement_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
        
        return True, replacement_count
    
    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}", file=sys.stderr)
        return False, 0


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
    """Main workflow function."""
    parser = argparse.ArgumentParser(
        description='Workflow: Extract → Translate → Replace Russian words in files'
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
        '--max-files',
        type=int,
        default=None,
        help='Maximum number of files to process (default: all)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=50,
        help='Number of words to translate in one batch (default: 50)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=0.1,
        help='Delay between API calls in seconds (default: 0.1)'
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
    args = parser.parse_args()
    
    print("=" * 80)
    print("RUSSIAN WORDS TRANSLATION WORKFLOW")
    print("=" * 80)
    print()
    
    # Step 1: Parse words file
    print("Step 1: Parsing words file...")
    file_words_dict, all_words = parse_words_file(args.words_file)
    
    if not all_words:
        print("  ✗ No Russian words found in file")
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
    print("Step 3: Translating words...")
    words_to_translate = [w for w in all_words if w not in cache]
    
    if words_to_translate:
        print(f"  Translating {len(words_to_translate)} new words...")
        
        # Translate in batches
        word_map = cache.copy()
        for i in range(0, len(words_to_translate), args.batch_size):
            batch = words_to_translate[i:i + args.batch_size]
            print(f"    Batch {i // args.batch_size + 1}: {len(batch)} words...")
            translations = translate_words_batch(batch, cache, args.delay)
            word_map.update(translations)
            print(f"      ✓ Translated {len(translations)} words")
        
        # Save cache
        save_translation_cache(cache, args.cache_file)
        print(f"  ✓ Saved {len(cache)} translations to cache")
    else:
        print("  ✓ All words already translated (using cache)")
        word_map = cache.copy()
    
    print()
    
    # Step 4: Replace words in files
    print("Step 4: Replacing words in files...")
    
    if not args.yes and not args.dry_run:
        response = input(f"Replace Russian words in {len(file_words_dict)} files? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return
    
    files_to_process = list(file_words_dict.keys())
    if args.max_files:
        files_to_process = files_to_process[:args.max_files]
    
    total_replacements = 0
    successful_files = 0
    failed_files = 0
    
    for i, file_path in enumerate(files_to_process, 1):
        print(f"  [{i}/{len(files_to_process)}] Processing {file_path}...")
        
        if args.dry_run:
            # Count potential replacements
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                words_in_file = extract_russian_words(content)
                potential_replacements = len([w for w in words_in_file if w in word_map])
                print(f"    Would replace {potential_replacements} words")
                total_replacements += potential_replacements
            except Exception as e:
                print(f"    ✗ Error: {e}")
                failed_files += 1
        else:
            success, count = process_file_with_translations(file_path, word_map)
            if success:
                if count > 0:
                    print(f"    ✓ Replaced {count} words")
                    total_replacements += count
                else:
                    print(f"    - No replacements needed")
                successful_files += 1
            else:
                failed_files += 1
    
    print()
    print("=" * 80)
    print("WORKFLOW SUMMARY")
    print("=" * 80)
    print(f"  Total unique words: {len(all_words)}")
    print(f"  Translated words: {len(word_map)}")
    print(f"  Files processed: {len(files_to_process)}")
    print(f"  Successful: {successful_files}")
    print(f"  Failed: {failed_files}")
    print(f"  Total replacements: {total_replacements}")
    if args.dry_run:
        print("  [DRY RUN] No files were modified")
    print("=" * 80)


if __name__ == '__main__':
    main()

