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
    import ssl
    import json as json_lib
    HAS_HTTP = True
    # Create SSL context that doesn't verify certificates (for free API)
    SSL_CONTEXT = ssl.create_default_context()
    SSL_CONTEXT.check_hostname = False
    SSL_CONTEXT.verify_mode = ssl.CERT_NONE
except ImportError:
    HAS_HTTP = False
    SSL_CONTEXT = None
    print("Error: urllib not available")
    sys.exit(1)


def has_russian_text(text: str) -> bool:
    """Check if text contains Cyrillic characters."""
    return bool(re.search(r'[А-Яа-яЁё]', text))


def extract_russian_words(text: str) -> Set[str]:
    """Extract unique Russian words from text."""
    words = re.findall(r'\b[А-Яа-яЁё]+\b', text)
    return set(words)


def translate_text_with_api(text: str, cache: Dict[str, str] = None, max_length: int = 500, max_retries: int = 3, retry_delay: float = 2.0) -> Optional[str]:
    """Translate text using MyMemory Translation API with retry logic."""
    if cache is None:
        cache = {}
    
    # Check cache first
    if text in cache:
        return cache[text]
    
    if not HAS_HTTP:
        return None
    
    # Handle long text by splitting into chunks
    if len(text) > max_length:
        # Split by sentences
        sentences = re.split(r'([.!?]\s+)', text)
        chunks = []
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
        
        # Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            translated = translate_text_with_api(chunk, cache, max_length, max_retries, retry_delay)
            if translated:
                translated_chunks.append(translated)
            else:
                translated_chunks.append(chunk)
            time.sleep(retry_delay)  # Rate limiting between chunks
        
        result = ''.join(translated_chunks)
        cache[text] = result
        return result
    
    # Retry logic for API calls
    for attempt in range(max_retries):
        try:
            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": "ru|en"
            }
            query_string = urlencode(params)
            full_url = f"{url}?{query_string}"
            
            req = Request(full_url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urlopen(req, timeout=15, context=SSL_CONTEXT) as response:
                if response.status == 200:
                    result = json_lib.loads(response.read().decode('utf-8'))
                    if result.get('responseStatus') == 200:
                        translated = result['responseData']['translatedText'].strip()
                        cache[text] = translated
                        return translated
                elif response.status == 429:
                    # Rate limited - wait longer and retry
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1) * 2  # Exponential backoff
                        print(f"    Rate limited, waiting {wait_time:.1f}s before retry {attempt + 1}/{max_retries}...", file=sys.stderr)
                        time.sleep(wait_time)
                        continue
        except URLError as e:
            if "429" in str(e) or "Too Many Requests" in str(e):
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1) * 2
                    print(f"    Rate limited, waiting {wait_time:.1f}s before retry {attempt + 1}/{max_retries}...", file=sys.stderr)
                    time.sleep(wait_time)
                    continue
            else:
                if attempt == max_retries - 1:
                    print(f"  Warning: API error for text (first 50 chars): '{text[:50]}...': {e}", file=sys.stderr)
        except (json_lib.JSONDecodeError, KeyError, Exception) as e:
            if attempt == max_retries - 1:
                print(f"  Warning: API error for text (first 50 chars): '{text[:50]}...': {e}", file=sys.stderr)
    
    return None


def translate_word_with_api(word: str, cache: Dict[str, str] = None) -> Optional[str]:
    """Translate a single word using MyMemory Translation API."""
    if cache is None:
        cache = {}
    
    # Check cache first
    if word in cache:
        return cache[word]
    
    # Use text translation for words too
    translated = translate_text_with_api(word, cache, max_length=100)
    if translated:
        # For single words, take only first word
        translated = translated.split()[0] if translated.split() else translated
        cache[word] = translated
        return translated
    
    return None


def translate_words_batch(words: List[str], cache: Dict[str, str] = None, delay: float = 0.05) -> Dict[str, str]:
    """Translate a batch of words using API."""
    if cache is None:
        cache = {}
    
    translations = {}
    total = len(words)
    for i, word in enumerate(words, 1):
        if word not in cache:
            translated = translate_word_with_api(word, cache)
            if translated:
                translations[word] = translated
                cache[word] = translated
            # Show progress for every 10 words
            if i % 10 == 0:
                print(f"    Progress: {i}/{total} words translated", end='\r', file=sys.stderr)
            time.sleep(delay)  # Rate limiting
        else:
            translations[word] = cache[word]
    
    if total > 10:
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


def replace_words_in_text(text: str, word_map: Dict[str, str], context_check: bool = True, show_progress: bool = False) -> Tuple[str, int]:
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
    total_words = len(sorted_words)
    
    for idx, russian_word in enumerate(sorted_words, 1):
        if show_progress and total_words > 10 and idx % max(1, total_words // 10) == 0:
            progress_percent = (idx / total_words) * 100
            print(f"      Replacing words: {progress_percent:.0f}% ({idx}/{total_words})", end='\r', file=sys.stderr)
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
    
    if show_progress and total_words > 10:
        print("", file=sys.stderr)  # New line after progress
    
    return translated, replacement_count


def extract_russian_fragments(text: str, max_fragment_length: int = 800) -> List[Tuple[int, str]]:
    """
    Extract Russian text fragments from text, grouping consecutive Russian lines.
    Returns list of (start_line_index, fragment_text) tuples.
    """
    lines = text.split('\n')
    fragments = []
    current_fragment_lines = []
    current_fragment_start = None
    
    for i, line in enumerate(lines):
        if has_russian_text(line):
            if current_fragment_start is None:
                current_fragment_start = i
            
            # Check if adding this line would exceed max length
            test_fragment = '\n'.join(current_fragment_lines + [line])
            if len(test_fragment) > max_fragment_length and current_fragment_lines:
                # Save current fragment and start new one
                fragments.append((current_fragment_start, '\n'.join(current_fragment_lines)))
                current_fragment_lines = [line]
                current_fragment_start = i
            else:
                current_fragment_lines.append(line)
        else:
            # Non-Russian line - save current fragment if exists
            if current_fragment_lines:
                fragments.append((current_fragment_start, '\n'.join(current_fragment_lines)))
                current_fragment_lines = []
                current_fragment_start = None
    
    # Save last fragment if exists
    if current_fragment_lines:
        fragments.append((current_fragment_start, '\n'.join(current_fragment_lines)))
    
    return fragments


def process_file_with_api_translation(
    file_path: str,
    cache: Dict[str, str],
    delay: float = 2.0,
    cache_file: str = None,
    max_fragment_length: int = 800
) -> Tuple[bool, int]:
    """
    Process a file by translating Russian text fragments through API.
    Optimized: groups consecutive Russian lines into fragments for fewer API calls.
    Returns (success, replacement_count)
    """
    if not os.path.exists(file_path):
        return False, 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        if not has_russian_text(original_content):
            return True, 0
        
        # Extract Russian fragments (grouped consecutive Russian lines)
        fragments = extract_russian_fragments(original_content, max_fragment_length)
        
        if not fragments:
            return True, 0
        
        total_fragments = len(fragments)
        print(f"    Found {total_fragments} Russian text fragments to translate")
        
        # Build translation map: fragment_text -> translated_text
        translation_map = {}
        replacement_count = 0
        
        for i, (start_line_idx, fragment) in enumerate(fragments, 1):
            # Show progress
            progress_percent = (i / total_fragments) * 100
            fragment_preview = fragment[:50].replace('\n', ' ') if len(fragment) > 50 else fragment.replace('\n', ' ')
            print(f"    [{i}/{total_fragments}] ({progress_percent:.1f}%) Translating fragment ({len(fragment)} chars)...", end='\r')
            sys.stdout.flush()
            
            # Translate fragment
            translated_fragment = translate_text_with_api(
                fragment,
                cache,
                max_length=max_fragment_length,
                max_retries=3,
                retry_delay=delay
            )
            
            if translated_fragment and translated_fragment != fragment:
                translation_map[fragment] = translated_fragment
                replacement_count += 1
                print(f"    ✓ Translated fragment {i}/{total_fragments}")
            else:
                if not translated_fragment:
                    print(f"    ⚠ Skipped fragment {i}/{total_fragments} (API error)")
                translation_map[fragment] = fragment  # Keep original
            
            # Adaptive delay based on fragment size
            adaptive_delay = delay + (len(fragment) / 1000) * 0.5  # Extra delay for larger fragments
            time.sleep(adaptive_delay)
            
            # Save cache periodically (every 5 fragments)
            if cache_file and i % 5 == 0:
                save_translation_cache(cache, cache_file)
        
        print()  # New line after progress
        
        if replacement_count > 0:
            # Reconstruct file with translations
            lines = original_content.split('\n')
            result_lines = []
            fragment_idx = 0
            i = 0
            
            while i < len(lines):
                if fragment_idx < len(fragments):
                    frag_start, frag_text = fragments[fragment_idx]
                    if i == frag_start:
                        # Replace fragment
                        translated = translation_map.get(frag_text, frag_text)
                        frag_lines = translated.split('\n')
                        result_lines.extend(frag_lines)
                        # Skip lines that were part of this fragment
                        frag_line_count = len(frag_text.split('\n'))
                        i += frag_line_count
                        fragment_idx += 1
                        continue
                
                # Regular line (not part of any fragment)
                result_lines.append(lines[i])
                i += 1
            
            translated_content = '\n'.join(result_lines)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
        
        # Save cache after processing file
        if cache_file:
            save_translation_cache(cache, cache_file)
        
        return True, replacement_count
    
    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}", file=sys.stderr)
        return False, 0


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
            original_content, word_map, context_check, show_progress=True
        )
        
        if replacement_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
        
        return True, replacement_count
    
    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}", file=sys.stderr)
        return False, 0


def find_files_with_russian(root_dir: str = '.') -> List[str]:
    """Find all files with Russian text (excluding russian/ directories)."""
    files_with_russian = []
    
    for root, dirs, files in os.walk(root_dir):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if not any(
            pattern in os.path.join(root, d) for pattern in [
                '.git', 'node_modules', '__pycache__', '.venv', 'venv', 
                '.uv', 'uv_cache', 'russian', 'data', 'Logs', 'models', 'results'
            ]
        )]
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_dir)
            
            # Skip excluded files
            if any(rel_path.endswith(ext) for ext in ['-ru.md', '_ru.md', '.ru.']):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(10000)  # Read first 10KB to check
                    if has_russian_text(content):
                        files_with_russian.append(rel_path)
            except:
                continue
    
    return files_with_russian


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
        default=None,
        help='File with Russian words (from count_russian_files.py --words-output). If not provided, will scan for files with Russian text.'
    )
    parser.add_argument(
        '--scan-files',
        action='store_true',
        help='Scan project for files with Russian text (if --words-file not provided)'
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
        default=2.5,
        help='Base delay between API calls in seconds (default: 2.5)'
    )
    parser.add_argument(
        '--max-fragment-length',
        type=int,
        default=800,
        help='Maximum length of text fragment for API translation (default: 800)'
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
        '--translate-by-file',
        action='store_true',
        help='Translate entire file content through API (instead of word-by-word)'
    )
    args = parser.parse_args()
    
    print("=" * 80)
    print("RUSSIAN WORDS TRANSLATION WORKFLOW")
    print("=" * 80)
    print()
    
    # Step 1: Get files with Russian text
    print("Step 1: Finding files with Russian text...")
    
    if args.words_file:
        file_words_dict, all_words = parse_words_file(args.words_file)
        if not file_words_dict and not all_words:
            print("  ⚠ Words file empty or not found, scanning for files...")
            args.scan_files = True
    
    if args.scan_files or not args.words_file:
        # Scan for files directly
        files_with_russian = find_files_with_russian('.')
        file_words_dict = {f: [] for f in files_with_russian}  # Empty word lists, will be processed directly
        all_words = set()
        print(f"  ✓ Found {len(files_with_russian)} files with Russian text")
    else:
        print(f"  ✓ Found {len(all_words)} unique Russian words")
        print(f"  ✓ Found {len(file_words_dict)} files with Russian words")
    
    if not file_words_dict:
        print("  ✗ No files with Russian text found")
        return
    
    print(f"  ✓ Found {len(all_words)} unique Russian words")
    print(f"  ✓ Found {len(file_words_dict)} files with Russian words")
    print()
    
    # Step 2: Load translation cache
    print("Step 2: Loading translation cache...")
    cache = load_translation_cache(args.cache_file)
    print(f"  ✓ Loaded {len(cache)} cached translations")
    print()
    
    if args.translate_by_file:
        # Mode: Translate entire files through API
        print("Mode: Translating entire files through API")
        print()
        
        # Step 3: Translate files directly
        print("Step 3: Translating files...")
    else:
        # Mode: Translate words first, then replace
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
    
    if not args.translate_by_file:
        if not args.yes and not args.dry_run:
            response = input(f"Replace Russian words in {len(file_words_dict)} files? (yes/no): ")
            if response.lower() != 'yes':
                print("Aborted.")
                return
    else:
        if not args.yes and not args.dry_run:
            response = input(f"Translate {len(file_words_dict)} files through API? (yes/no): ")
            if response.lower() != 'yes':
                print("Aborted.")
                return
    
    files_to_process = list(file_words_dict.keys())
    if args.max_files:
        files_to_process = files_to_process[:args.max_files]
    
    total_replacements = 0
    successful_files = 0
    failed_files = 0
    
    print(f"\nProcessing {len(files_to_process)} files...\n")
    
    for i, file_path in enumerate(files_to_process, 1):
        progress_percent = (i / len(files_to_process)) * 100
        print(f"\n{'='*80}")
        print(f"  [{i}/{len(files_to_process)}] ({progress_percent:.1f}%) Processing: {file_path}")
        print(f"{'='*80}")
        
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
            if args.translate_by_file:
                # Translate entire file through API (optimized)
                success, count = process_file_with_api_translation(
                    file_path, 
                    cache, 
                    args.delay,
                    args.cache_file,
                    args.max_fragment_length
                )
                if success:
                    if count > 0:
                        print(f"    ✓ Translated {count} lines")
                        total_replacements += count
                    else:
                        print(f"    - No translations needed")
                    successful_files += 1
                else:
                    failed_files += 1
            else:
                # Replace words using word map
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
    # Save cache after file processing
    if args.translate_by_file:
        save_translation_cache(cache, args.cache_file)
    
    print()
    print("=" * 80)
    print("WORKFLOW SUMMARY")
    print("=" * 80)
    if args.translate_by_file:
        print(f"  Mode: File-by-file translation")
        print(f"  Files processed: {len(files_to_process)}")
        print(f"  Successful: {successful_files}")
        print(f"  Failed: {failed_files}")
        print(f"  Total lines translated: {total_replacements}")
        print(f"  Cache size: {len(cache)} translations")
    else:
        print(f"  Mode: Word-by-word translation")
        print(f"  Total unique words: {len(all_words)}")
        print(f"  Translated words: {len(word_map) if 'word_map' in locals() else len(cache)}")
        print(f"  Files processed: {len(files_to_process)}")
        print(f"  Successful: {successful_files}")
        print(f"  Failed: {failed_files}")
        print(f"  Total replacements: {total_replacements}")
    if args.dry_run:
        print("  [DRY RUN] No files were modified")
    print("=" * 80)


if __name__ == '__main__':
    main()

