#!/usr/bin/env python3
"""
Advanced translation script using free translation API for complex sentences.
Uses pattern-based translation first, then API for remaining Russian text.
"""

import argparse
import os
import re
import time
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from collections import OrderedDict

# Try to import translation libraries
try:
    from googletrans import Translator
    HAS_GOOGLETRANS = True
except ImportError:
    HAS_GOOGLETRANS = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    try:
        # Try with uv run
        import subprocess
        result = subprocess.run(['uv', 'run', 'python3', '-c', 'import requests'], 
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            HAS_REQUESTS = True
        else:
            HAS_REQUESTS = False
    except:
        HAS_REQUESTS = False

# Pattern-based translations (for simple phrases)
PATTERN_TRANSLATIONS = OrderedDict([
    (r'File not found', 'File not found'),
    (r'Missing columns', 'Missing columns'),
    (r'Setting index', 'Setting index'),
    (r'Creating temporary index', 'Creating temporary index'),
    (r'Loading data', 'Loading data'),
    (r'Checking presence', 'Checking presence'),
    (r'Using', 'Using'),
    (r'specific file', 'specific file'),
    (r'if specified', 'if specified'),
    (r'not found', 'not found'),
    (r'required', 'required'),
    (r'columns', 'columns'),
    (r'presence', 'presence'),
    (r'Checking', 'Checking'),
    (r'Loading', 'Loading'),
    (r'data', 'data'),
])

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
    """Check if file should be excluded from translation."""
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def has_russian_text(text: str) -> bool:
    """Check if text contains Cyrillic characters."""
    return bool(re.search(r'[А-Яа-яЁё]', text))


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


def translate_with_googletrans(text: str) -> Optional[str]:
    """Translate text using googletrans library."""
    if not HAS_GOOGLETRANS:
        return None
    
    try:
        translator = Translator()
        result = translator.translate(text, src='ru', dest='en')
        return result.text
    except Exception as e:
        print(f"  Warning: Google Translate error: {e}", file=sys.stderr)
        return None


def translate_text_advanced(text: str, use_api: bool = True) -> str:
    """Translate Russian text using patterns first, then API for remaining text."""
    if not has_russian_text(text):
        return text
    
    # First, apply pattern-based translations
    translated = text
    for pattern, replacement in PATTERN_TRANSLATIONS.items():
        translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)
    
    # If still has Russian text and API is enabled, use API
    if use_api and has_russian_text(translated):
        # Extract Russian sentences
        lines = translated.split('\n')
        translated_lines = []
        
        for line in lines:
            if has_russian_text(line):
                # Try to translate with API
                api_translated = None
                
                # Try MyMemory first (more reliable)
                try:
                    import requests
                    api_translated = translate_with_mymemory(line.strip())
                    if api_translated:
                        translated_lines.append(api_translated)
                        time.sleep(0.3)  # Rate limiting
                        continue
                except:
                    pass
                
                # Fallback to googletrans
                if not api_translated and HAS_GOOGLETRANS:
                    try:
                        api_translated = translate_with_googletrans(line.strip())
                        if api_translated:
                            translated_lines.append(api_translated)
                            time.sleep(0.3)  # Rate limiting
                            continue
                    except:
                        pass
                
                # If API failed, keep original
                if not api_translated:
                    translated_lines.append(line)
            else:
                translated_lines.append(line)
        
        translated = '\n'.join(translated_lines)
    
    return translated


def find_files_with_russian(root_dir: str = '.') -> List[Tuple[str, int]]:
    """Find all files containing Russian text."""
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
                    content = f.read()
                    if has_russian_text(content):
                        russian_lines = sum(1 for line in content.split('\n') if has_russian_text(line))
                        files_with_russian.append((rel_path, russian_lines))
            except Exception as e:
                print(f"Warning: Could not read {rel_path}: {e}", file=sys.stderr)
    
    return sorted(files_with_russian)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Translate Russian text using free translation API')
    parser.add_argument('--dry-run', action='store_true', help='Show files without making changes')
    parser.add_argument('--file', type=str, help='Translate specific file only')
    parser.add_argument('--yes', '-y', action='store_true', help='Auto-proceed without confirmation')
    parser.add_argument('--no-api', action='store_true', help='Disable API translation, use patterns only')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between API calls in seconds')
    args = parser.parse_args()
    
    # Check available translation methods
    if not args.no_api:
        # Try to import requests dynamically
        try:
            import requests
            has_requests = True
        except ImportError:
            has_requests = False
        
        if not has_requests and not HAS_GOOGLETRANS:
            print("Warning: No translation API libraries found.")
            print("Install: uv pip install requests  (for MyMemory API)")
            print("Or run with: uv run python3 scripts/utilities/translate_with_api.py")
            print("Continuing with pattern-based translation only...")
            print()
            use_api = False
        else:
            use_api = True
            if has_requests:
                print("✓ Using MyMemory Translation API (free)")
            if HAS_GOOGLETRANS:
                print("✓ Using Google Translate (googletrans)")
    else:
        use_api = False
        print("Using pattern-based translation only (API disabled)")
    
    print("Scanning project for files with Russian text...")
    print("Excluding: russian/ directories, *-ru.md files, and data/logs/models directories")
    print()
    
    if args.file:
        files_to_process = [(args.file, 0)]
    else:
        files_to_process = find_files_with_russian()
    
    if not files_to_process:
        print("No files with Russian text found (excluding Russian-specific files).")
        return
    
    print(f"Found {len(files_to_process)} files with Russian text:")
    print()
    
    total_lines = 0
    for file_path, line_count in files_to_process[:30]:
        print(f"  {file_path} ({line_count} lines)")
        total_lines += line_count
    
    if len(files_to_process) > 30:
        print(f"  ... and {len(files_to_process) - 30} more files")
    
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
    print("Starting translation...")
    if use_api:
        print("Using pattern-based translation + free API for complex sentences")
    else:
        print("Using pattern-based translation only")
    print()
    
    translated_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, (file_path, line_count) in enumerate(files_to_process, 1):
        full_path = os.path.join('.', file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            if not has_russian_text(original_content):
                skipped_count += 1
                continue
            
            print(f"[{i}/{len(files_to_process)}] Translating {file_path}...")
            translated_content = translate_text_advanced(original_content, use_api=use_api)
            
            if translated_content != original_content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(translated_content)
                translated_count += 1
                print(f"  ✓ Translated: {file_path}")
            else:
                skipped_count += 1
                print(f"  - No changes: {file_path}")
            
            # Rate limiting
            if use_api and i < len(files_to_process):
                time.sleep(args.delay)
                
        except Exception as e:
            error_count += 1
            print(f"  ✗ Error: {file_path}: {e}")
    
    print()
    print("=" * 60)
    print("Translation Summary:")
    print(f"  Translated: {translated_count} files")
    print(f"  Skipped: {skipped_count} files")
    print(f"  Errors: {error_count} files")
    print("=" * 60)
    print()
    print("Note: Please review translated files for accuracy.")


if __name__ == '__main__':
    main()

