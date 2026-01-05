#!/usr/bin/env python3
"""Translate git commit messages in batches."""

import subprocess
import re
import sys
import os
import tempfile
from transformers import MarianMTModel, MarianTokenizer
import torch

def has_russian_text(text):
    return bool(re.search(r'[А-Яа-яЁё]', text))

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
        if len(parts) == 2 and has_russian_text(parts[1]):
            commits.append((parts[0], parts[1]))
    
    return commits

def translate_commit_message(msg, model, tokenizer):
    """Translate commit message."""
    # Extract prefix (feat:, fix:, etc.)
    prefix_match = re.match(r'^([a-z]+:\s*)', msg)
    prefix = prefix_match.group(1) if prefix_match else ''
    rest = msg[len(prefix):] if prefix else msg
    
    if not has_russian_text(rest):
        return msg
    
    # Translate
    try:
        inputs = tokenizer(rest, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        return prefix + translated_text
    except Exception as e:
        print(f"  ⚠ Translation error: {e}", flush=True)
        return msg

def main():
    print("=" * 80)
    print("TRANSLATING GIT COMMIT MESSAGES")
    print("=" * 80)
    print()
    
    commits = get_commits_with_russian()
    print(f"Found {len(commits)} commits with Russian text\n")
    
    if not commits:
        print("No commits to translate.")
        return
    
    # Load model
    print("Loading translation model...", flush=True)
    model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
    tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
    model.eval()
    print("✓ Model loaded\n", flush=True)
    
    # Translate in batches
    batch_size = 10
    translation_map = {}
    
    print(f"Translating commits in batches of {batch_size}...\n")
    
    for batch_start in range(0, len(commits), batch_size):
        batch_end = min(batch_start + batch_size, len(commits))
        batch = commits[batch_start:batch_end]
        
        print(f"Batch {batch_start // batch_size + 1}/{(len(commits) + batch_size - 1) // batch_size}")
        print("-" * 80)
        
        for i, (hash_val, msg) in enumerate(batch, 1):
            total_i = batch_start + i
            print(f"[{total_i}/{len(commits)}] {hash_val[:8]}: {msg[:60]}...", flush=True)
            
            translated = translate_commit_message(msg, model, tokenizer)
            translation_map[hash_val] = translated
            
            print(f"  → {translated[:60]}...\n", flush=True)
    
    if not translation_map:
        print("No translations to apply.")
        return
    
    # Create filter script
    print(f"\nApplying translations to git history...\n")
    
    filter_lines = ['#!/bin/bash']
    for hash_val, translated in translation_map.items():
        translated_escaped = translated.replace("'", "'\"'\"'")
        filter_lines.append(f'if [ "$GIT_COMMIT" = "{hash_val}" ]; then')
        filter_lines.append(f"  echo '{translated_escaped}'")
        filter_lines.append('else')
        filter_lines.append('  cat')
        filter_lines.append('fi')
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
        f.write('\n'.join(filter_lines))
        filter_file = f.name
    
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
    
    os.unlink(filter_file)
    
    if result.returncode == 0:
        print(f"✓ Successfully translated {len(translation_map)} commits!")
    else:
        print(f"⚠ Warning: {result.stderr}")

if __name__ == '__main__':
    main()

