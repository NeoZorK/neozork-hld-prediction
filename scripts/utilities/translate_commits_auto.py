#!/usr/bin/env python3
"""
Script to automatically translate git commit messages from Russian to English.
Uses transformers model for translation.
"""

import subprocess
import re
import sys
from transformers import MarianMTModel, MarianTokenizer

# Load translation model
_model = None
_tokenizer = None

def load_model():
    global _model, _tokenizer
    if _model is None:
        print("Loading translation model...", flush=True)
        _tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
        _model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
        _model.eval()
        print("✓ Model loaded", flush=True)
    return _model, _tokenizer

def translate_text(text: str) -> str:
    """Translate Russian text to English."""
    if not re.search(r'[А-Яа-яЁё]', text):
        return text
    
    model, tokenizer = load_model()
    
    # Split text into sentences for better translation
    sentences = re.split(r'([.!?]\s+)', text)
    translated_parts = []
    
    for part in sentences:
        if not part.strip():
            translated_parts.append(part)
            continue
        
        if not re.search(r'[А-Яа-яЁё]', part):
            translated_parts.append(part)
            continue
        
        # Translate
        try:
            inputs = tokenizer(part, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                translated = model.generate(**inputs)
            translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
            translated_parts.append(translated_text)
        except Exception as e:
            print(f"  ⚠ Translation error: {e}", flush=True)
            translated_parts.append(part)
    
    return ''.join(translated_parts)

def get_commits_with_russian():
    """Get all commits with Russian text."""
    result = subprocess.run(
        ['git', 'log', '--format=%H|%s', '--all'],
        capture_output=True, text=True, encoding='utf-8'
    )
    
    commits = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split('|', 1)
        if len(parts) == 2 and re.search(r'[А-Яа-яЁё]', parts[1]):
            commits.append((parts[0], parts[1]))
    
    return commits

def translate_commit_message(msg: str) -> str:
    """Translate commit message, preserving format."""
    # Extract prefix (feat:, fix:, etc.)
    prefix_match = re.match(r'^([a-z]+:\s*)', msg)
    prefix = prefix_match.group(1) if prefix_match else ''
    rest = msg[len(prefix):] if prefix else msg
    
    # Translate the rest
    translated_rest = translate_text(rest)
    
    return prefix + translated_rest

def main():
    import torch
    
    print("=" * 80)
    print("AUTOMATIC COMMIT MESSAGE TRANSLATION")
    print("=" * 80)
    print()
    
    commits = get_commits_with_russian()
    print(f"Found {len(commits)} commits with Russian text\n")
    
    if not commits:
        print("No commits to translate.")
        return
    
    # Create translation map
    translation_map = {}
    
    print("Translating commit messages...\n")
    for i, (hash_val, msg) in enumerate(commits, 1):
        print(f"[{i}/{len(commits)}] {hash_val[:8]}: {msg[:60]}...", flush=True)
        translated = translate_commit_message(msg)
        translation_map[hash_val] = translated
        print(f"  → {translated[:60]}...\n", flush=True)
    
    # Apply translations using git filter-branch
    print("\nApplying translations to git history...\n")
    
    # Create filter script
    filter_script = "#!/bin/bash\n"
    for hash_val, translated in translation_map.items():
        # Escape special characters
        translated_escaped = translated.replace("'", "'\\''")
        filter_script += f'if [ "$GIT_COMMIT" = "{hash_val}" ]; then\n'
        filter_script += f"  echo '{translated_escaped}'\n"
        filter_script += "else\n"
        filter_script += "  cat\n"
        filter_script += "fi\n"
    
    # Write filter script
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
        f.write(filter_script)
        filter_file = f.name
    
    import os
    os.chmod(filter_file, 0o755)
    
    # Run filter-branch
    env = os.environ.copy()
    env['FILTER_BRANCH_SQUELCH_WARNING'] = '1'
    
    result = subprocess.run(
        ['git', 'filter-branch', '-f', '--msg-filter', f'bash {filter_file}'],
        env=env,
        capture_output=True,
        text=True
    )
    
    # Clean up
    os.unlink(filter_file)
    
    if result.returncode == 0:
        print("✓ All commits translated successfully!")
    else:
        print(f"⚠ Warning: {result.stderr}")
    
    print(f"\nTranslated {len(translation_map)} commits")

if __name__ == '__main__':
    main()

