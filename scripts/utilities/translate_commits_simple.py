#!/usr/bin/env python3
"""Simple script to translate commit messages using git filter-branch."""

import subprocess
import re
import sys
import os
import tempfile

def has_russian_text(text):
Return bool (re.search(r'[A-Ya-Yo], text))

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

def translate_simple(msg):
    """Simple translation using common patterns."""
    translations = {
'update documentation on',
'Addition of dependency': 'add dependency',
'Renewal of addictions': 'update dependencies'
'in project': 'to project',
'To new versions',
'dependent': 'dependences',
'to achieve 100% profit': 'for achieving 100% profit',
'by metrics and monitoring': 'on metrics and monitoring',
'analyzing': 'on anallysis'
'Monte Carlo simulations': 'on Monte Carlo simulation',
'and risk management': 'and risk management',
'In the engineering of the signs': 'on feature engineering',
'and model learning': 'and modeling',
'for financial data': 'for financial data'
'data production': 'on data preparation',
'and the creation of signs': 'and fear creation',
'for ML systems': 'for ML systems',
'on fundamentals of robot systems',
'in ML',
'On installation and setting': 'on installation and conference',
'For Apple Silicon': 'for Apple Silicon'
'Exception and inclusion': 'exclusion and inclusion',
'for deletion and inclusion of documentation': 'for exception and inclusion of documentation',
'on detailed components': 'on detailed components',
'systems': 'system',
'on monitoring system',
'and metric': 'and metrics',
'In a full-time pay system': 'on complete learning system',
'100 per cent+ per month': '100 per cent+ per month',
'on block systems': 'on blockchain systems',
'and automatic retraining',
Concepts and strategies: 'Concepts and strategies',
'high-income ML systems': 'high-yeld ML systems',
'based on': 'based on',
        'blockchain integration': 'blockchain integration',
    }
    
    result = msg
    for ru, en in translations.items():
        result = result.replace(ru, en)
    
    # Clean up any remaining Russian words in quotes
Result = re.sub(r'"([A-Ya-Yyo]+)"", Lambda m: f'" {m.group(1)}" (translated)', results)
    
    return result

def main():
    commits = get_commits_with_russian()
    print(f"Found {len(commits)} commits with Russian text\n")
    
    if not commits:
        print("No commits to translate.")
        return
    
    # Create translation map
    translation_map = {}
    print("Translating commit messages...\n")
    
    for i, (hash_val, msg) in enumerate(commits[:20], 1):  # Limit to 20 for now
        print(f"[{i}/{min(20, len(commits))}] {hash_val[:8]}: {msg[:60]}...", flush=True)
        translated = translate_simple(msg)
        translation_map[hash_val] = translated
        print(f"  → {translated[:60]}...\n", flush=True)
    
    if not translation_map:
        print("No translations to apply.")
        return
    
    # Create filter script
    filter_lines = []
    for hash_val, translated in translation_map.items():
        # Escape for bash
        translated_escaped = translated.replace("'", "'\"'\"'")
        filter_lines.append(f'if [ "$GIT_COMMIT" = "{hash_val}" ]; then')
        filter_lines.append(f"  echo '{translated_escaped}'")
        filter_lines.append('else')
        filter_lines.append('  cat')
        filter_lines.append('fi')
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
        f.write('#!/bin/bash\n')
        f.write('\n'.join(filter_lines))
        filter_file = f.name
    
    os.chmod(filter_file, 0o755)
    
    print(f"\nApplying translations using git filter-branch...\n")
    
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
        print(f"✓ Translated {len(translation_map)} commits successfully!")
    else:
        print(f"⚠ Warning: {result.stderr}")

if __name__ == '__main__':
    main()

