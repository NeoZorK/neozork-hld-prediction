#!/usr/bin/env python3
"""Simple script to translate commit messages using git filter-branch."""

import subprocess
import re
import sys
import os
import tempfile

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

def translate_simple(msg):
    """Simple translation using common patterns."""
    translations = {
        'обновление документации по': 'update documentation on',
        'добавление зависимости': 'add dependency',
        'обновление зависимостей': 'update dependencies',
        'в проект': 'to project',
        'до new versions': 'to new versions',
        'зависимостей': 'dependencies',
        'для достижения 100% прибыли': 'for achieving 100% profit',
        'по метрикам и мониторингу': 'on metrics and monitoring',
        'по анализу': 'on analysis',
        'по Монте-Карло симуляции': 'on Monte Carlo simulation',
        'и управлению рисками': 'and risk management',
        'по инженерии признаков': 'on feature engineering',
        'и обучению моделей': 'and model training',
        'для финансовых данных': 'for financial data',
        'по подготовке данных': 'on data preparation',
        'и созданию признаков': 'and feature creation',
        'для ML-систем': 'for ML systems',
        'по основам робастных систем': 'on fundamentals of robust systems',
        'в ML': 'in ML',
        'по установке и настройке': 'on installation and configuration',
        'для Apple Silicon': 'for Apple Silicon',
        'исключения и включения': 'exclusion and inclusion',
        'для исключения и включения документации': 'for exclusion and inclusion of documentation',
        'по детальным компонентам': 'on detailed components',
        'системы': 'system',
        'по системе мониторинга': 'on monitoring system',
        'и метрик': 'and metrics',
        'по полной системе заработка': 'on complete earning system',
        '100%+ в месяц': '100%+ per month',
        'по блокчейн-системам': 'on blockchain systems',
        'и автоматическому переобучению': 'and automatic retraining',
        'концепции и стратегии': 'concepts and strategies',
        'высокодоходных ML systems': 'high-yield ML systems',
        'на основе': 'based on',
        'blockchain integration': 'blockchain integration',
    }
    
    result = msg
    for ru, en in translations.items():
        result = result.replace(ru, en)
    
    # Clean up any remaining Russian words in quotes
    result = re.sub(r'"([А-Яа-яЁё]+)"', lambda m: f'"{m.group(1)}" (translated)', result)
    
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

