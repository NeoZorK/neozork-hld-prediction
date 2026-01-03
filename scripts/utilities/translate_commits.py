#!/usr/bin/env python3
"""
Script to translate all git commit messages from Russian to English.

This script Uses git filter-branch to rewrite commit history.
WARNING: This will rewrite git history. Make sure you have a backup!
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Translation dictionary for common Russian phrases in commit messages
# Order matters: longer, more specific phrases should come first
TRANSLATIONS = {
 # Long specific phrases (must come first)
 r'\bобновление документации on полной системе заработка 100%\+ in месяц\b': 'update documentation on complete earning system 100%+ per month',
 r'\bобновление документации on системе Monitoringа and метрик for достижения 100% прибыли\b': 'update documentation on Monitoring system and metrics for achieving 100% profit',
 r'\bобновление документации on метрикам and Monitoringу for достижения 100% прибыли\b': 'update documentation on metrics and Monitoring for achieving 100% profit',
 r'\bобновление документации on детальным components системы NeoZorK\b': 'update documentation on Detailed components of NeoZorK system',
 r'\bобновление документации on установке and настройке MLX and Jupyter for Apple Silicon\b': 'update documentation on installation and configuration of MLX and Jupyter for Apple Silicon',
 r'\bобновление документации on основам робастных систем in ML\b': 'update documentation on basics of robust systems in ML',
 r'\bобновление документации on подготовке данных and созданию признаков for ML-систем\b': 'update documentation on data preparation and feature creation for ML systems',
 r'\bобновление документации on инженерии признаков and обучению моделей for финансовых данных\b': 'update documentation on feature engineering and model training for financial data',
 r'\bобновление документации on Монте-Карло симуляции and управлению рисками\b': 'update documentation on Monte Carlo simulation and risk Management',
 r'\bобновление документации on анализу SCHR Levels and SCHR SHORT3\b': 'update documentation on SCHR Levels and SCHR SHORT3 Analysis',
 r'\bобновление files \.dockerignore and \.gitignore for\b': 'update .dockerignore and .gitignore files for',
 r'\bобновление files \.dockerignore and \.gitignore for исключения and включения документации\b': 'update .dockerignore and .gitignore files for exclusion and inclusion of documentation',
 r'\bобновление files \.dockerignore and \.gitignore for декомпозиции\b': 'update .dockerignore and .gitignore files for decomposition',
 r'\bобновление functions экспорта метаданных in декомпозиции временных рядов\b': 'update metadata export function in time series decomposition',
 r'\bдобавление новых функций for визуализации результатов CEEMDAN\b': 'add new functions for CEEMDAN visualization results',
 r'\bдобавление новых функций for декомпозиции временных рядов\b': 'add new functions for time series decomposition',
 r'\bдобавление модуля декомпозиции временных рядов\b': 'add time series decomposition module',
 r'\bдобавление патча for исправления уязвимости SSRF in пакете ip\b': 'add patch to fix SSRF vulnerability in ip package',
 r'\bдобавление руководства on безопасности for уязвимости API отправки заданий Ray\b': 'add security guide for Ray job submission API vulnerability',
 r'\bдобавление документации on уязвимости CVE-2025-53000 in nbconvert\b': 'add documentation on CVE-2025-53000 vulnerability in nbconvert',
 r'\bуточнение спецификатора dependencies urllib3\b': 'clarify urllib3 dependency specifier',
 r'\bобновление временных меток in документации and скриптах\b': 'update timestamps in documentation and scripts',

 # Common phrases
 r'\bдобавление dependencies\b': 'add dependency',
 r'\bобновление dependencies\b': 'update dependency',
 r'\bдобавление документации\b': 'add documentation',
 r'\bобновление документации\b': 'update documentation',
 r'\bдобавление патча\b': 'add patch',
 r'\bдобавление новых функций\b': 'add new functions',
 r'\bобновление functions\b': 'update function',
 r'\bдобавление модуля\b': 'add module',
 r'\bобновление files\b': 'update files',
 r'\bдобавление новых dependencies\b': 'add new dependencies',

 # Common verbs
 r'\bобновление\b': 'update',
 r'\bдобавление\b': 'add',
 r'\bуточнение\b': 'clarify',
 r'\bисправление\b': 'fix',
 r'\bудаление\b': 'remove',
 r'\bулучшение\b': 'improve',
 r'\bрефакторинг\b': 'refactor',
 r'\bизменение\b': 'change',
 r'\bсоздание\b': 'create',
 r'\bнастройка\b': 'configure',

 # Specific phrases
 r'\bдо версии\b': 'to version',
 r'\bв package\.json\b': 'to package.json',
 r'\bв pyproject\.toml\b': 'to pyproject.toml',
 r'\bв requirements\.txt\b': 'to requirements.txt',
 r'\bв документации\b': 'in documentation',
 r'\bв скриптах\b': 'in scripts',
 r'\bдля\b': 'for',
 r'\bпо\b': 'on',
 r'\bс добавлением\b': 'with addition of',
 r'\bи\b': 'and',

 # Documentation specific
 r'\bруководства on\b': 'guide on',
 r'\bруководство on\b': 'guide on',
 r'\bуязвимости\b': 'vulnerability',
 r'\bуязвимость\b': 'vulnerability',
 r'\bбезопасности\b': 'security',
 r'\bвременных меток\b': 'timestamps',
 r'\bвременных рядов\b': 'time series',
 r'\bдекомпозиции\b': 'decomposition',
 r'\bэкспорта метаданных\b': 'metadata export',
 r'\bвизуализации результатов\b': 'visualization results',
 r'\bметрикам and Monitoringу\b': 'metrics and Monitoring',
 r'\bдля достижения 100% прибыли\b': 'for achieving 100% profit',
 r'\bанализу\b': 'Analysis',
 r'\bМонте-Карло симуляции\b': 'Monte Carlo simulation',
 r'\bуправлению рисками\b': 'risk Management',
 r'\bинженерии признаков\b': 'feature engineering',
 r'\bобучению моделей\b': 'model training',
 r'\bфинансовых данных\b': 'financial data',
 r'\bподготовке данных\b': 'data preparation',
 r'\bсозданию признаков\b': 'feature creation',
 r'\bML-систем\b': 'ML systems',
 r'\bосновам робастных систем\b': 'basics of robust systems',
 r'\bустановке and настройке\b': 'installation and configuration',
 r'\bдетальным components\b': 'Detailed components',
 r'\bсистеме Monitoringа\b': 'Monitoring system',
 r'\bполной системе заработка\b': 'complete earning system',
 r'\bблокчейн-системам\b': 'blockchain systems',
 r'\bавтоматическому переобучению\b': 'automatic retraining',
 r'\bконцепции and стратегии\b': 'Concepts and strategies',
 r'\bвысокодоходных ML-систем\b': 'high-yield ML systems',
 r'\bторговых систем\b': 'trading systems',
 r'\bблокчейн-интеграции\b': 'blockchain integration',
 r'\bметрикам Analysis производительности\b': 'performance Analysis metrics',
 r'\bпродвинутым практикам\b': 'advanced practices',
 r'\bоптимизации Portfolio\b': 'Portfolio optimization',
 r'\bтеоретическим обоснованиям\b': 'theoretical foundations',
 r'\bуровней поддержки and сопротивления\b': 'support and resistance levels',
 r'\bмашинному обучению\b': 'machine learning',
 r'\bструктуре документации\b': 'documentation Structure',
 r'\bновых разделов\b': 'new sections',
 r'\bисключения and включения\b': 'exclusion and inclusion',

 # More specific translations
 r'\bспецификатора dependencies\b': 'dependency specifier',
 r'\bновых версий\b': 'new versions',
 r'\bSSRF\b': 'SSRF', # Keep acronyms
 r'\bCEEMDAN\b': 'CEEMDAN', # Keep acronyms
 r'\bSCHR\b': 'SCHR', # Keep acronyms
 r'\bMLX\b': 'MLX', # Keep acronyms
 r'\bJupyter\b': 'Jupyter', # Keep names
 r'\bApple Silicon\b': 'Apple Silicon', # Keep names
 r'\bNeoZorK\b': 'NeoZorK', # Keep names
 r'\bCVE-\d+-\d+\b': lambda m: m.group(0), # Keep CVE numbers
}

# Direct translations for specific commit messages
DIRECT_TRANSLATIONS = {
 'chore: update dependencies h11 and httpcore to new versions':
 'chore: update dependencies h11 and httpcore to new versions',
 'feat: add new dependencies in проект':
 'feat: add new dependencies to project',
 'fix: update .dockerignore and .gitignore files for исключения and включения документации':
 'fix: update .dockerignore and .gitignore files for exclusion and inclusion of documentation',
 'feat: update documentation on концепции and стратегии высокодоходных ML systems':
 'feat: update documentation on Concepts and strategies of high-yield ML systems',
 'feat: update documentation on примерам trading systems on basis WAVE2, SCHR Levels and blockchain integration':
 'feat: update documentation on examples of trading systems based on WAVE2, SCHR Levels and blockchain integration',
 'feat: update documentation SCHR SHORT3 with addition of теоретических обоснований and Analysis':
 'feat: update documentation SCHR SHORT3 with addition of theoretical foundations and Analysis',
 'feat: update documentation SCHR Levels with addition of new sections on Analysis уровней поддержки and сопротивления':
 'feat: update documentation SCHR Levels with addition of new sections on Analysis of support and resistance levels',
 'feat: update структуры документации NeoZorK with addition of new sections':
 'feat: update NeoZorK documentation Structure with addition of new sections',
 'feat: добавлены новые разделы on data preparation, feature engineering, model training, бэктестингу and risk Management':
 'feat: add new sections on data preparation, feature engineering, model training, backtesting and risk Management',
 'feat: update руководства NeoZorK with установкой окружения for macOS M1 Pro':
 'feat: update NeoZorK guide with installation of environment for macOS M1 Pro',
 'feat: добавлен HTML-interface for учебника':
 'feat: add HTML interface for tutorial',
 'feat: добавлена полная система заработка 100%+ in месяц - Создана детальная система with рабочим кодом from идеи to деплоя - Добавлены все components: модели, индикаторы, блокчейн-integration - Реализована система автоматического переобучения - Добавлен полный Monitoring and система алертов - Создана documentation on Launch and использованию - Система готова for тестирования on блокчейн testnet':
 'feat: add complete earning system 100%+ per month - Created Detailed system with Working code from idea to deployment - Added all components: models, indicators, blockchain integration - Implemented automatic retraining system - Added full Monitoring and alert system - Created documentation on Launch and usage - system ready for testing on blockchain testnet',
 'feat: создан полный учебник on созданию робастных прибыльных ML systems':
 'feat: create complete tutorial on Creating robust profitable ML systems',
 'Add simple and advanced production examples to AutoML Gluon documentation - Introduced two new sections: "Простой example" and "Сложный example" showcasing the development and deployment of robust ML models Using AutoML Gluon. - included Detailed code examples, architecture diagrams, and performance metrics for both approaches. - Updated the AutoML Gluon manual and README to reference the new examples, enhancing the documentation\'s comprehensiveness and usability. - Added a script for generating graphics related to the production examples, improving visual representation. These additions provide Users with practical insights into building and deploying ML models, catering to both novice and advanced Users.':
 'Add simple and advanced production examples to AutoML Gluon documentation - Introduced two new sections: "Simple Example" and "Advanced Example" showcasing the development and deployment of robust ML models Using AutoML Gluon. - included Detailed code examples, architecture diagrams, and performance metrics for both approaches. - Updated the AutoML Gluon manual and README to reference the new examples, enhancing the documentation\'s comprehensiveness and usability. - Added a script for generating graphics related to the production examples, improving visual representation. These additions provide Users with practical insights into building and deploying ML models, catering to both novice and advanced Users.',
 'fix dual charts for -d fastest and MACD ок with scale date':
 'fix dual charts for -d fastest and MACD OK with scale date',
 'fix dual charts for -d fastest and MACD ок':
 'fix dual charts for -d fastest and MACD OK',
 'feat: Улучшить фильтрацию данных on дате in CSV and JSON файлах':
 'feat: improve data filtering by date in CSV and JSON files',
 'add dask datashader bokeh in requirments':
 'add dask datashader bokeh to requirements',
}


def translate_commit_message(message: str) -> str:
 """Translate Russian commit message to English."""
 # check for direct translation first
 message_stripped = message.strip()
 if message_stripped in DIRECT_TRANSLATIONS:
 return DIRECT_TRANSLATIONS[message_stripped]

 translated = message

 # Apply translations in order
 for pattern, replacement in TRANSLATIONS.items():
 if callable(replacement):
 translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)
 else:
 translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)

 # clean up multiple spaces
 translated = re.sub(r'\s+', ' ', translated)
 translated = translated.strip()

 return translated


def check_git_repo():
 """check if we're in a git repository."""
 result = subprocess.run(
 ['git', 'rev-parse', '--git-dir'],
 capture_output=True,
 text=True
 )
 return result.returncode == 0


def get_all_commits():
 """Get all commit hashes and messages."""
 result = subprocess.run(
 ['git', 'log', '--format=%H|%s', '--all'],
 capture_output=True,
 text=True,
 check=True
 )

 commits = []
 for line in result.stdout.strip().split('\n'):
 if '|' in line:
 commit_hash, message = line.split('|', 1)
 commits.append((commit_hash, message))

 return commits


def has_russian_text(text: str) -> bool:
 """check if text contains Cyrillic characters."""
 return bool(re.search(r'[А-Яа-яЁё]', text))


def main():
 """main function to translate commit messages."""
 parser = argparse.ArgumentParser(
 describe='Translate git commit messages from Russian to English'
 )
 parser.add_argument(
 '--yes', '-y',
 action='store_true',
 help='Automatically proceed without confirmation'
 )
 parser.add_argument(
 '--dry-run',
 action='store_true',
 help='Show translations without modifying git history'
 )
 args = parser.parse_args()

 if not check_git_repo():
 print("Error: Not in a git repository", file=sys.stderr)
 sys.exit(1)

 print("Fetching all commits...")
 commits = get_all_commits()

 # Find commits with Russian text
 russian_commits = []
 for commit_hash, message in commits:
 if has_russian_text(message):
 translated = translate_commit_message(message)
 if translated != message:
 russian_commits.append((commit_hash, message, translated))

 print(f"found {len(russian_commits)} commits with Russian text")

 if not russian_commits:
 print("No commits to translate.")
 return

 # Show first 10 translations as preView
 print("\nPreView of translations (first 10):")
 for i, (commit_hash, original, translated) in enumerate(russian_commits[:10], 1):
 print(f"\n{i}. {commit_hash[:8]}")
 print(f" Original: {original}")
 print(f" Translated: {translated}")

 if len(russian_commits) > 10:
 print(f"\n... and {len(russian_commits) - 10} more commits")

 if args.dry_run:
 print("\n[DRY RUN] No changes will be made to git history.")
 return

 # Ask for confirmation unless --yes flag is set
 if not args.yes:
 response = input("\nProceed with rewriting git history? (yes/no): ")
 if response.lower() != 'yes':
 print("Aborted.")
 return
 else:
 print("\nProceeding with git history rewrite (--yes flag set)...")

 # Create a Python script for git filter-branch msg-filter
 # This script will be called for each commit message
 msg_filter_script = Path('/tmp/git-msg-filter.py')

 # Create a dictionary mapping commit hashes to translated messages
 commit_translations = {hash_val: trans for hash_val, _, trans in russian_commits}

 with open(msg_filter_script, 'w') as f:
 f.write("#!/usr/bin/env python3\n")
 f.write("import sys\n")
 f.write("import re\n\n")

 # Write the translation function
 f.write("TRANSLATIONS = {\n")
 for pattern, replacement in TRANSLATIONS.items():
 if not callable(replacement):
 # Escape quotes in pattern and replacement
 pattern_escaped = pattern.replace('\\', '\\\\').replace("'", "\\'")
 replacement_escaped = replacement.replace("'", "\\'")
 f.write(f" r'{pattern_escaped}': '{replacement_escaped}',\n")
 f.write("}\n\n")

 # Write commit hash to translation mapping
 f.write("COMMIT_TRANSLATIONS = {\n")
 for commit_hash, translated in commit_translations.items():
 translated_escaped = translated.replace("'", "\\'").replace("\\", "\\\\")
 f.write(f" '{commit_hash}': '{translated_escaped}',\n")
 f.write("}\n\n")

 f.write("""
import os

def translate_commit_message(message):
 # check if we have a direct translation for this commit
 commit_hash = os.environ.get('GIT_COMMIT', '')
 if commit_hash and commit_hash in COMMIT_TRANSLATIONS:
 return COMMIT_TRANSLATIONS[commit_hash]

 # Otherwise, apply pattern-based translation
 translated = message
 for pattern, replacement in TRANSLATIONS.items():
 translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)

 translated = re.sub(r'\\s+', ' ', translated)
 return translated.strip()

if __name__ == '__main__':
 message = sys.stdin.read()
 translated = translate_commit_message(message)
 print(translated, end='')
""")

 msg_filter_script.chmod(0o755)

 print("\nRunning git filter-branch...")
 print("This may take a while...")

 # Run git filter-branch with Python script
 # GIT_COMMIT is available as environment variable in msg-filter
 result = subprocess.run(
 [
 'git', 'filter-branch',
 '--msg-filter', f'python3 {msg_filter_script}',
 '--force',
 '--tag-name-filter', 'cat',
 '--', '--all'
 ],
 capture_output=True,
 text=True
 )

 if result.returncode == 0:
 print("\n✓ Successfully translated all commit messages!")
 print("\nNext steps:")
 print("1. ReView the changes: git log --oneline -20")
 print("2. If everything looks good, force Push: git Push --force --all")
 print("3. If something went wrong, restore: git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch -r .' --prune-empty --tag-name-filter cat -- --all")
 else:
 print(f"\n✗ Error during filter-branch:", file=sys.stderr)
 print(result.stderr, file=sys.stderr)
 sys.exit(1)


if __name__ == '__main__':
 main()

