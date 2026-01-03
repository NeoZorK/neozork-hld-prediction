#!/usr/bin/env python3
"""
Script to translate remaining Russian commit messages to English.
Uses git filter-branch to rewrite specific commit messages.
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Direct translations for the remaining 18 commits
COMMIT_TRANSLATIONS = {
 'aacca191844e5ca4eea78c85395ac36388db810f':
 'chore: update dependencies h11 and httpcore to new versions',
 'b5809d69d1bdc21f5a85c01b136e38649571e720':
 'feat: add new dependencies to project',
 'eff2e35fd9d0de9cfde9ea64aa3098b5ea7c9ff5':
 'fix: update .dockerignore and .gitignore files for exclusion and inclusion of documentation',
 '9e8622e7705e1e1bd23ec9e78dfec5295d4f7633':
 'feat: update documentation on Concepts and strategies of high-yield ML systems',
 '9b017bf1ef6595f0f185154d14463f12bcf5767a':
 'feat: update documentation on examples of trading systems based on WAVE2, SCHR Levels and blockchain integration',
 '6d64c7d15d954062e9e5e946b602e3fdb4ba3249':
 'feat: update documentation SCHR SHORT3 with addition of theoretical foundations and Analysis',
 '85f504bb3f669c0d1b572831997f56f325f82c0a':
 'feat: update documentation SCHR Levels with addition of new sections on Analysis of support and resistance levels',
 'b7c2a933339cb74d1a3e0dbc25c9f088cd0a6cdd':
 'feat: update NeoZorK documentation Structure with addition of new sections',
 'd2ecdf5e5b88598ce92255b4a8d84b0b65a48457':
 'feat: add new sections on data preparation, feature engineering, model training, backtesting and risk Management',
 '16acadd1567d2839f767b0df7ccde5a31ca84de3':
 'feat: update NeoZorK guide with installation of environment for macOS M1 Pro',
 'f6a8260c649bf2e9f75b3bb990ee7681dc56974e':
 'feat: add HTML interface for tutorial',
 'c67140eb0ec3b33369c97fd972d371f6fdd20416':
 'feat: add complete earning system 100%+ per month - Created Detailed system with Working code from idea to deployment - Added all components: models, indicators, blockchain integration - Implemented automatic retraining system - Added full Monitoring and alert system - Created documentation on Launch and usage - system ready for testing on blockchain testnet',
 '02ec3296859726ca6f6026281a1496e64ea3b6e1':
 'feat: create complete tutorial on Creating robust profitable ML systems',
 '619544aef875fc061c16e143436fdd6b940bc2b5':
 'Add simple and advanced production examples to AutoML Gluon documentation - Introduced two new sections: "Simple Example" and "Advanced Example" showcasing the development and deployment of robust ML models Using AutoML Gluon. - included Detailed code examples, architecture diagrams, and performance metrics for both approaches. - Updated the AutoML Gluon manual and README to reference the new examples, enhancing the documentation\'s comprehensiveness and usability. - Added a script for generating graphics related to the production examples, improving visual representation. These additions provide Users with practical insights into building and deploying ML models, catering to both novice and advanced Users.',
 '877585aab0c1d60842bd7dc938175011d3892c67':
 'fix dual charts for -d fastest and MACD OK with scale date',
 '816bc990ee2430c7a06c59fecb72225178f74913':
 'fix dual charts for -d fastest and MACD OK',
 '32cfdef4eff2927cf7fa2b769a0df24669ecda93':
 'feat: improve data filtering by date in CSV and JSON files',
 '3f22dcc00126592105b0b8b4fb78c871769185b8':
 'add dask datashader bokeh to requirements',
}


def create_msg_filter_script():
 """Create a msg-filter script for git filter-branch."""
 # Also create message-based translations
 message_translations = {
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
 }

 script_content = f'''#!/usr/bin/env python3
import sys
import os
import re

COMMIT_TRANSLATIONS = {{
'''

 for commit_hash, translated_msg in COMMIT_TRANSLATIONS.items():
 # Escape quotes and newlines
 translated_escaped = translated_msg.replace("'", "\\'").replace("\\", "\\\\").replace("\\n", " ")
 script_content += f" '{commit_hash}': '{translated_escaped}',\n"

 script_content += '''}

MESSAGE_TRANSLATIONS = {
'''

 for original_msg, translated_msg in message_translations.items():
 original_escaped = original_msg.replace("'", "\\'").replace("\\", "\\\\")
 translated_escaped = translated_msg.replace("'", "\\'").replace("\\", "\\\\")
 script_content += f" '{original_escaped}': '{translated_escaped}',\n"

 script_content += '''}

def translate_message(message):
 message_stripped = message.strip()

 # check by commit hash first
 commit_hash = os.environ.get('GIT_COMMIT', '')
 if commit_hash and commit_hash in COMMIT_TRANSLATIONS:
 return COMMIT_TRANSLATIONS[commit_hash]

 # check by message content
 if message_stripped in MESSAGE_TRANSLATIONS:
 return MESSAGE_TRANSLATIONS[message_stripped]

 # Pattern-based translation for remaining cases
 translated = message_stripped

 # Replace common Russian words
 replacements = [
 (r'\\bdependencies\\b', 'dependencies'),
 (r'\\bдо new versions\\b', 'to new versions'),
 (r'\\bв проект\\b', 'to project'),
 (r'\\bисключения\\b', 'exclusion'),
 (r'\\bвключения\\b', 'inclusion'),
 (r'\\bконцепции\\b', 'Concepts'),
 (r'\\bстратегии\\b', 'strategies'),
 (r'\\bвысокодоходных\\b', 'high-yield'),
 (r'\\bпримерам\\b', 'examples'),
 (r'\\bbased on\\b', 'based on'),
 (r'\\bтеоретических обоснований\\b', 'theoretical foundations'),
 (r'\\bAnalysis\\b', 'Analysis'),
 (r'\\bуровней поддержки\\b', 'support levels'),
 (r'\\bсопротивления\\b', 'resistance'),
 (r'\\bструктуры документации\\b', 'documentation Structure'),
 (r'\\bдобавлены новые разделы\\b', 'add new sections'),
 (r'\\bбэктестингу\\b', 'backtesting'),
 (r'\\bруководства\\b', 'guide'),
 (r'\\bс установкой\\b', 'with installation'),
 (r'\\bокружения\\b', 'environment'),
 (r'\\bдобавлен HTML-interface\\b', 'add HTML interface'),
 (r'\\bдля учебника\\b', 'for tutorial'),
 (r'\\bдобавлена полная система заработка\\b', 'add complete earning system'),
 (r'\\bв месяц\\b', 'per month'),
 (r'\\bСоздана детальная система\\b', 'Created Detailed system'),
 (r'\\bс рабочим кодом from идеи to деплоя\\b', 'with Working code from idea to deployment'),
 (r'\\bДобавлены все components\\b', 'Added all components'),
 (r'\\bмодели\\b', 'models'),
 (r'\\bиндикаторы\\b', 'indicators'),
 (r'\\bблокчейн-integration\\b', 'blockchain integration'),
 (r'\\bРеализована система автоматического retraining\\b', 'Implemented automatic retraining system'),
 (r'\\bДобавлен полный Monitoring\\b', 'Added full Monitoring'),
 (r'\\bсистема алертов\\b', 'alert system'),
 (r'\\bСоздана documentation\\b', 'Created documentation'),
 (r'\\bна Launch\\b', 'on Launch'),
 (r'\\bиспользованию\\b', 'usage'),
 (r'\\bСистема готова\\b', 'system ready'),
 (r'\\bтестирования\\b', 'testing'),
 (r'\\bблокчейн testnet\\b', 'blockchain testnet'),
 (r'\\bсоздан полный учебник\\b', 'created complete tutorial'),
 (r'\\bна созданию\\b', 'on Creating'),
 (r'\\bробастных прибыльных\\b', 'robust profitable'),
 (r'\\bПростой example\\b', 'Simple example'),
 (r'\\bСложный example\\b', 'Advanced example'),
 (r'\\bMACD ок\\b', 'MACD OK'),
 (r'\\bУлучшить фильтрацию данных\\b', 'Improve data filtering'),
 (r'\\bна дате\\b', 'by date'),
 (r'\\bв CSV\\b', 'in CSV'),
 (r'\\bJSON файлах\\b', 'JSON files'),
 (r'\\bв requirments\\b', 'to requirements'),
 ]

 for pattern, replacement in replacements:
 translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)

 # clean up
 translated = re.sub(r'\\s+', ' ', translated)
 translated = translated.strip()

 return translated if translated != message_stripped else message

if __name__ == '__main__':
 message = sys.stdin.read()
 translated = translate_message(message)
 print(translated, end='')
'''

 script_path = Path('/tmp/git-msg-filter-remaining.py')
 with open(script_path, 'w') as f:
 f.write(script_content)

 script_path.chmod(0o755)
 return script_path


def main():
 """main function."""
 parser = argparse.ArgumentParser(describe='Translate remaining Russian commit messages')
 parser.add_argument('--yes', '-y', action='store_true', help='Automatically proceed without confirmation')
 args = parser.parse_args()

 print("Translating remaining 18 commits with Russian text...")
 print(f"found {len(COMMIT_TRANSLATIONS)} commits to translate")
 print()

 # Show preView
 print("PreView of translations:")
 for i, (commit_hash, translated) in enumerate(COMMIT_TRANSLATIONS.items(), 1):
 result = subprocess.run(
 ['git', 'log', '--format=%s', '-1', commit_hash],
 capture_output=True,
 text=True
 )
 original = result.stdout.strip()
 print(f"\n{i}. {commit_hash[:8]}")
 print(f" Original: {original[:80]}...")
 print(f" Translated: {translated[:80]}...")

 print()
 if not args.yes:
 response = input("Proceed with rewriting git history? (yes/no): ")
 if response.lower() != 'yes':
 print("Aborted.")
 return
 else:
 print("Proceeding with git history rewrite (--yes flag set)...")

 # Create msg-filter script
 script_path = create_msg_filter_script()
 print(f"\nCreated msg-filter script: {script_path}")

 # Run git filter-branch
 print("\nRunning git filter-branch...")
 print("This may take a while...")

 result = subprocess.run(
 [
 'git', 'filter-branch',
 '--msg-filter', f'python3 {script_path}',
 '--force',
 '--tag-name-filter', 'cat',
 '--', 'v0.5.8'
 ],
 capture_output=True,
 text=True
 )

 if result.returncode == 0:
 print("\n✓ Successfully translated all remaining commit messages!")
 print("\nNext steps:")
 print("1. ReView the changes: git log --oneline -20")
 print("2. check for remaining Russian text: git log --format='%s' | grep -E '[А-Яа-яЁё]'")
 print("3. If everything looks good, Push: git Push --force origin v0.5.8")
 else:
 print(f"\n✗ Error during filter-branch:", file=sys.stderr)
 print(result.stderr, file=sys.stderr)
 sys.exit(1)


if __name__ == '__main__':
 main()

