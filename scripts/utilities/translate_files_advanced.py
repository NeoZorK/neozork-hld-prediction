#!/usr/bin/env python3
"""
Advanced script to translate Russian text in project files to English.
Uses comprehensive translation dictionary and sentence-level processing.
Excludes files in russian/ directories and files with -ru.md suffix.
"""

import argparse
import os
import re
from pathlib import Path
from typing import List, Tuple
from collections import OrderedDict

# Comprehensive translation dictionary
# Order matters: longer, more specific phrases first
TRANSLATIONS = OrderedDict([
 # Documentation headers and titles
 (r'^# installation (.+)$', r'# installation \1'),
 (r'^## Почему (.+)$', r'## Why \1'),
 (r'^### (.+) последствия (.+)$', r'### \1 Consequences \2'),
 (r'^#### (.+) проблемы (.+)$', r'#### \1 Issues \2'),
 (r'^#### Ошибки (.+)$', r'#### \1 Errors'),
 (r'^#### Проблемы (.+)$', r'#### \1 Issues'),

 # Common documentation phrases
 (r'AutoML Gluon installation', 'AutoML Gluon installation'),
 (r'Why Proper installation is Critical', 'Why Proper installation is Critical'),
 (r'Real Consequences of Incorrect installation', 'Real Consequences of Incorrect installation'),
 (r'Что происходит при неправильной установке\?', 'What Happens with Incorrect installation?'),
 (r'Troubleshooting', 'Troubleshooting'),
 (r'Common Issues', 'Common Issues'),
 (r'installation Issues', 'installation Issues'),
 (r'Launch Issues', 'Launch Issues'),
 (r'import Errors', 'import Errors'),
 (r'Port Issues', 'Port Issues'),
 (r'Frequently Asked Questions', 'Frequently Asked Questions'),
 (r'Project Structure', 'Project Structure'),
 (r'Run and Test Guides', 'Run and Test Guides'),
 (r'Russian Version', 'Russian Version'),
 (r'English Version', 'English Version'),
 (r'Common Resources', 'Common Resources'),

 # Code comments
 (r'Comprehensive solution for', 'Comprehensive solution for'),
 (r'Решает (\d+) основные задачи', r'Solves \1 main tasks'),
 (r'Prediction', 'Prediction'),
 (r'Author:', 'Author:'),
 (r'Version:', 'Version:'),
 (r'Comprehensive solution', 'Comprehensive solution'),
 (r'Creating ML models', 'Creating ML models'),
 (r'based on', 'based on'),
 (r'sign', 'sign'),
 (r'price direction', 'price direction'),
 (r'on (\d+) periods', r'for \1 periods'),
 (r'breakthrough', 'breakthrough'),
 (r'holding', 'holding'),
 (r'between them', 'between them'),

 # Technical terms
 (r'\bобновление\b', 'update'),
 (r'\bдобавление\b', 'add'),
 (r'\bудаление\b', 'remove'),
 (r'\bисправление\b', 'fix'),
 (r'\bулучшение\b', 'improve'),
 (r'\bсоздание\b', 'create'),
 (r'\bнастройка\b', 'configuration'),
 (r'\bустановка\b', 'installation'),
 (r'\bруководство\b', 'guide'),
 (r'\bдокументация\b', 'documentation'),
 (r'\bпример\b', 'example'),
 (r'\bпримеры\b', 'examples'),
 (r'\bописание\b', 'describe'),
 (r'\bинструкция\b', 'instruction'),
 (r'\bинструкции\b', 'instructions'),
 (r'\bзависимость\b', 'dependency'),
 (r'\bзависимости\b', 'dependencies'),
 (r'\bмодуль\b', 'module'),
 (r'\bмодули\b', 'modules'),
 (r'\bфункция\b', 'function'),
 (r'\bфункции\b', 'functions'),
 (r'\bпараметр\b', 'parameter'),
 (r'\bпараметры\b', 'parameters'),
 (r'\bконфигурация\b', 'configuration'),
 (r'\bнастройки\b', 'Settings'),
 (r'\bиндикаторов\b', 'indicators'),
 (r'\bcheck\b', 'check'),
 (r'\bclean\b', 'clean'),
 (r'\bcache\b', 'cache'),
 (r'\breinstall\b', 'reinstall'),

 # Common words (lower priority)
 (r'\bдля\b', 'for'),
 (r'\bпо\b', 'on'),
 (r'\bс\b', 'with'),
 (r'\bи\b', 'and'),
 (r'\bили\b', 'or'),
 (r'\bв\b', 'in'),
 (r'\bна\b', 'on'),
 (r'\bот\b', 'from'),
 (r'\bдо\b', 'to'),
 (r'\bне\b', 'not'),
 (r'\bустановлен\b', 'installed'),

 # Additional phrases for mixed text
 (r'basis', 'basis'),
 (r'periods', 'periods'),
 (r'up/down', 'up/down'),
 (r'package installation', 'package installation'),
 (r'occupied ports', 'occupied ports'),
 (r'Free ports', 'Free ports'),
 (r'database', 'database'),
 (r'PostgreSQL connection', 'PostgreSQL connection'),
 (r'Restart PostgreSQL', 'Restart PostgreSQL'),
 (r'testing', 'testing'),
 (r'start', 'start'),
 (r'coverage', 'coverage'),
 (r'coverage cache', 'coverage cache'),
 (r'network', 'network'),
 (r'with debugging', 'with debugging'),
 (r'specific test', 'specific test'),
 (r'with timeout', 'with timeout'),
 (r'with limited threads', 'with limited threads'),
 (r'Containers do not start', 'Containers do not start'),
 (r'Rebuild containers', 'Rebuild containers'),
 (r'Restart Docker', 'Restart Docker'),
 (r'View volumes', 'View volumes'),
 (r'Suppresses output', 'Suppresses output'),
 (r'Restores standard output', 'Restores standard output'),
 (r'Filters messages', 'Filters messages'),
 (r'available', 'available'),
 (r'will be Used', 'will be Used'),
 (r'parallel training', 'parallel training'),
 (r'sequential training', 'sequential training'),
 (r'to install', 'to install'),
 (r'Pipeline initialization', 'Pipeline initialization'),
 (r'Path to folder', 'Path to folder'),
 (r'with data', 'with data'),
 (r'Specific data file', 'Specific data file'),
 (r'for Analysis', 'for Analysis'),
 (r'install:', 'install:'),
 (r'different tasks', 'different tasks'),
 (r'minutes', 'minutes'),
 (r'initialized', 'initialized'),

 # Additional Russian words and phrases
 (r'including', 'including'),
 (r'messages', 'messages'),
 (r'execute', 'execute'),
 (r'Comprehensive pipeline', 'Comprehensive pipeline'),
 (r'Informing about', 'Informing about'),
 (r'training mode', 'training mode'),
 (r'acceleration', 'acceleration'),
 (r'install', 'install'),
 (r'Loading data', 'Loading data'),
 (r'specified', 'specified'),
 (r'Trading symbol', 'Trading symbol'),
 (r'Timeframe', 'Timeframe'),
 (r'mobile application', 'mobile application'),
 (r'Report', 'Report'),
 (r'Status:', 'Status:'),
 (r'COMPLETED', 'COMPLETED'),
 (r'successfully created', 'successfully created'),
 (r'integrated', 'integrated'),
 (r'Implemented', 'Implemented'),
 (r'application Structure', 'application Structure'),
 (r'application', 'application'),
 (r'Navigation', 'Navigation'),
 (r'Authentication', 'Authentication'),
 (r'state Management', 'state Management'),
 (r'integration', 'integration'),
 (r'Application screens', 'Application screens'),
 (r'Login to system', 'Login to system'),
 (r'User registration', 'User registration'),
 (r'main screen', 'main screen'),
 (r'with greeting', 'with greeting'),
 (r'Loading screen', 'Loading screen'),
 (r'Plan', 'Plan'),
 (r'Goal', 'Goal'),
 (r'Create system', 'Create system'),
 (r'multiple Timeframes', 'multiple Timeframes'),
 (r'simultaneously', 'simultaneously'),
 (r'improving accuracy', 'improving accuracy'),
 (r'predictions', 'predictions'),
 (r'Concept', 'Concept'),
 (r'Timeframe hierarchy', 'Timeframe hierarchy'),
 (r'Base Timeframe', 'Base Timeframe'),
 (r'for trading', 'for trading'),
 (r'Medium Timeframe', 'Medium Timeframe'),
 (r'for trend', 'for trend'),
 (r'Long-term trend', 'Long-term trend'),
 (r'Macro trend', 'Macro trend'),
 (r'Fundamental trend', 'Fundamental trend'),
 (r'Analysis principles', 'Analysis principles'),
 (r'Synchronization', 'Synchronization'),
 (r'must be synchronized', 'must be synchronized'),
 (r'in time', 'in time'),
 (r'influence hierarchy', 'influence hierarchy'),
 (r'higher Timeframes', 'higher Timeframes'),
 (r'influence', 'influence'),
 (r'lower', 'lower'),
 (r'Conflict resolution', 'Conflict resolution'),
 (r'In case of conflict', 'In case of conflict'),
 (r'priority to', 'priority to'),
 (r'higher Timeframe', 'higher Timeframe'),
 (r'General questions', 'General questions'),
 (r'How to quickly', 'How to quickly'),
 (r'Launch the system', 'Launch the system'),
 (r'Use', 'Use'),
 (r'Quick start', 'Quick start'),
 (r'Launch main Analysis', 'Launch main Analysis'),
 (r'main page', 'main page'),
 (r'Complete guide', 'Complete guide'),
 (r'Quick start', 'Quick start'),
 (r'guide on', 'guide on'),
 (r'testing', 'testing'),
 (r'deployment', 'deployment'),
 (r'main Structure', 'main Structure'),
 (r'main code', 'main code'),
 (r'platform', 'platform'),
 (r'Hedge fund', 'Hedge fund'),
 (r'Monitoring', 'Monitoring'),
 (r'Comprehensive strategy', 'Comprehensive strategy'),
 (r'commercialization', 'commercialization'),
 (r'Market Analysis', 'Market Analysis'),
 (r'opportunity assessment', 'opportunity assessment'),
 (r'Business model', 'Business model'),
 (r'revenue streams', 'revenue streams'),
 (r'Go-to-market strategy', 'Go-to-market strategy'),
 (r'to market', 'to market'),
 (r'Roadmap', 'Roadmap'),
 (r'product development', 'product development'),
 (r'Issues with', 'Issues with'),
 (r'tests do not', 'tests do not'),
 (r'Safe mode', 'Safe mode'),
 (r'Launch', 'Launch'),
 (r'Slow tests', 'Slow tests'),
 (r'not available', 'not available'),
 (r'symbol', 'symbol'),
 (r'Timeframe', 'Timeframe'),
 (r'data File not found', 'data File not found'),
 (r'Authentication Management', 'Authentication Management'),
 (r'HTTP client', 'HTTP client'),
 (r'Style constants', 'Style constants'),
 (r'services', 'services'),
 (r'Use specific file', 'Use specific file'),
 (r'if specified', 'if specified'),
 (r'found', 'found'),
 (r'Use', 'Use'),
 (r'specific file', 'specific file'),
 (r'specified', 'specified'),
 (r'not found', 'not found'),
 (r'data file', 'data file'),
 (r'symbol and', 'symbol and'),
 (r'and Timeframe', 'and Timeframe'),
 (r'Loading data', 'Loading data'),
 (r'checking presence', 'checking presence'),
 (r'required columns', 'required columns'),
 (r'Analysis', 'Analysis'),
 (r'Timeframes', 'Timeframes'),
 (r'Timeframes', 'Timeframes'),
 (r'What components are included in the system', 'What components are included in the system'),
 (r'Detailed guide on all components', 'Detailed guide on all components'),
 (r'Launch', 'Launch'),
 (r'Calculations', 'Calculations'),
 (r'Working with data', 'Working with data'),
 (r'health check', 'health check'),
 (r'mobile API', 'mobile API'),
 (r'Data for main screen', 'Data for main screen'),
 (r'User Portfolio', 'User Portfolio'),
 (r'List of funds', 'List of funds'),
 (r'Investment Management', 'Investment Management'),
 (r'View networks', 'View networks'),
 (r'clean networks', 'clean networks'),
 (r'create network', 'create network'),
 (r'Run all tests', 'Run all tests'),
 (r'CLI interface', 'CLI interface'),
 (r'team Structure', 'team Structure'),
 (r'organization', 'organization'),
 (r'commercialization for', 'commercialization for'),
 (r'SaaS platform', 'SaaS platform'),
 (r'Use specific file if specified', 'Use specific file if specified'),
 (r'File not found', 'File not found'),
 (r'for specified symbol', 'for specified symbol'),
 (r'for specified', 'for specified'),
 (r'symbol and', 'symbol and'),
 (r'will be Used sequential', 'will be Used sequential'),
 (r'not available -', 'not available -'),
 (r'not available', 'not available'),
 (r'Use standard path', 'Use standard path'),
 (r'standard path', 'standard path'),
 (r'checking presence of required', 'checking presence of required'),
 (r'columns', 'columns'),
 (r'required', 'required'),
 (r'presence', 'presence'),
 (r'checking', 'checking'),
 (r'Loading', 'Loading'),
 (r'data', 'data'),
 (r'mobile', 'mobile'),
 (r'health', 'health'),
 (r'check', 'check'),
 (r'main screen', 'main screen'),
 (r'main', 'main'),
 (r'screen', 'screen'),
 (r'User', 'User'),
 (r'Portfolio', 'Portfolio'),
 (r'List', 'List'),
 (r'funds', 'funds'),
 (r'investments', 'investments'),
 (r'Management', 'Management'),
 (r'networks', 'networks'),
 (r'View', 'View'),
 (r'included in', 'included in'),
 (r'components', 'components'),
 (r'What', 'What'),
 (r'included', 'included'),
 (r'system', 'system'),
 (r'Detailed', 'Detailed'),
 (r'all', 'all'),
 (r'components', 'components'),
 (r'Calculations', 'Calculations'),
 (r'Working', 'Working'),
 (r'interface', 'interface'),
 (r'team', 'team'),
 (r'Structure', 'Structure'),
 (r'organization', 'organization'),
])

# files and directories to exclude
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
 """check if file should be excluded from translation."""
 for pattern in EXCLUDE_PATTERNS:
 if re.search(pattern, file_path):
 return True
 return False


def has_russian_text(text: str) -> bool:
 """check if text contains Cyrillic characters."""
 return bool(re.search(r'[А-Яа-яЁё]', text))


def find_files_with_russian(root_dir: str = '.') -> List[Tuple[str, int]]:
 """Find all files containing Russian text."""
 files_with_russian = []

 for root, dirs, files in os.walk(root_dir):
 # Skip excluded directories
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
 print(f"Warning: Could not read {rel_path}: {e}")

 return sorted(files_with_russian)


def translate_text(text: str) -> str:
 """Translate Russian text to English Using comprehensive patterns."""
 if not has_russian_text(text):
 return text

 translated = text

 # Apply translations in order (longer patterns first)
 for pattern, replacement in TRANSLATIONS.items():
 translated = re.sub(pattern, replacement, translated, flags=re.MULTILINE | re.IGNORECASE)

 # clean up multiple spaces but preserve Structure
 lines = translated.split('\n')
 cleaned_lines = []
 for line in lines:
 # Preserve markdown and code Structure
 if (line.strip().startswith('#') or
 line.strip().startswith('*') or
 line.strip().startswith('-') or
 line.strip().startswith('```') or
 line.strip().startswith('`')):
 cleaned_lines.append(re.sub(r'[ \t]+', ' ', line.rstrip()))
 else:
 cleaned_lines.append(re.sub(r'[ \t]+', ' ', line.rstrip()))

 return '\n'.join(cleaned_lines)


def main():
 """main function."""
 parser = argparse.ArgumentParser(describe='Translate Russian text in project files to English')
 parser.add_argument('--dry-run', action='store_true', help='Show files without making changes')
 parser.add_argument('--file', type=str, help='Translate specific file only')
 parser.add_argument('--yes', '-y', action='store_true', help='Auto-proceed without confirmation')
 parser.add_argument('--batch-size', type=int, default=10, help='Number of files to process in batch')
 args = parser.parse_args()

 print("Scanning project for files with Russian text...")
 print("Excluding: russian/ directories, *-ru.md files, and data/Logs/models directories")
 print()

 if args.file:
 files_to_process = [(args.file, 0)]
 else:
 files_to_process = find_files_with_russian()

 if not files_to_process:
 print("No files with Russian text found (excluding Russian-specific files).")
 return

 print(f"found {len(files_to_process)} files with Russian text:")
 print()

 total_lines = 0
 for file_path, line_count in files_to_process[:30]:
 print(f" {file_path} ({line_count} lines)")
 total_lines += line_count

 if len(files_to_process) > 30:
 print(f" ... and {len(files_to_process) - 30} more files")

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
 print("starting translation...")
 print("Note: This Uses pattern-based translation. Complex sentences may need reView.")
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

 translated_content = translate_text(original_content)

 if translated_content != original_content:
 with open(full_path, 'w', encoding='utf-8') as f:
 f.write(translated_content)
 translated_count += 1
 print(f"[{i}/{len(files_to_process)}] ✓ {file_path}")
 else:
 skipped_count += 1
 print(f"[{i}/{len(files_to_process)}] - {file_path} (no changes)")

 except Exception as e:
 error_count += 1
 print(f"[{i}/{len(files_to_process)}] ✗ {file_path}: {e}")

 print()
 print("=" * 60)
 print("Translation Summary:")
 print(f" Translated: {translated_count} files")
 print(f" Skipped: {skipped_count} files")
 print(f" Errors: {error_count} files")
 print("=" * 60)
 print()
 print("Note: Please reView translated files for accuracy.")
 print("Complex sentences and Technical terms may need manual correction.")


if __name__ == '__main__':
 main()
