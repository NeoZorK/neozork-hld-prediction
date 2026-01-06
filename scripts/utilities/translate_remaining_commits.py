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
'feat: add new preferences in project':
 'feat: add new dependencies to project',
'fix: update .dockerignore and .gitignore profiles for deletion and inclusion of documentation':
 'fix: update .dockerignore and .gitignore files for exclusion and inclusion of documentation',
'feat: up-date documentation on the ML systems' concept and strategy:
 'feat: update documentation on Concepts and strategies of high-yield ML systems',
'feat: up-date documentation on examples of trafficking systems on basic WAVE2, SCHR Movements and blockchain integration':
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
(r'bto new versionsb', 'to new versions'),
(r'b by project b', 'to project'),
(r'b `b', 'exclusion'),
(r'bclusion,b', 'inclusion'),
(r'b Concepts `b', 'Concepts'),
(r'b strategy `b', 'Strategies'),
(r' high-income, b', 'high-yeld'),
(r'b's examples `b', 'examples'),
 (r'\\bbased on\\b', 'based on'),
(r'btheoretical justifications `b', 'theoretical foundations'),
 (r'\\bAnalysis\\b', 'Analysis'),
(r'by-level support `b', 'support relief'),
(r'b Resistance',b', 'resistance'),
(r'bstructure of documentation `b', 'documentation Structure'),
(r'b' adds new sections `b', 'add new sections'),
(r'backtesting, b', 'backtesting'),
(r'brotherbook'b', 'guid'),
(r'`b with installation `b', 'with installation'),
(r'conditions `b', 'environment'),
(r'branded HTML-interface'b, 'add HTML interface'),
(r'b for textbook `b', 'for tutorial'),
(r'b' complete system of earnings added,b','add complete development system'),
(r'b in month `b', 'per month'),
(r'b The detailed system `b', 'Created Detailed System')
(r'`b with working code from ideas to deb', 'with Working code from idea to definition'),
(r'b Added all components b', 'Added all components'),
(r'b models `b', 'models'),
(r'bindicators `b', 'indicators'),
(r'blockchin-integration'b', 'blockchain integration'),
(r'`b Automatic retraining system implemented,b', 'implemented automatic retraining system'),
(r'b Added full Monitoringb', 'Added Full Monitoring'),
(r'b's allernet of `b', 'alert system'),
(r'b Created document'b', 'Created document'),
(r'bna Launch'b', 'on Launch'),
(r'buse,b', 'usage'),
(r'b System ready `b', 'system ready'),
(r'btest 'b', 'testing'),
(r'r'blockchin testnet'b', 'blockchain testnet'),
(r'b's created the full textbook `b', 'created complete tutorial'),
(r'bna create 'b', 'on Creation'),
(r'brobrobatic profit-making,b', 'robus profitable'),
(r'b Simple exampleb', 'Simple example'),
(r'b Complex exampleb', 'Advanced example'),
(r'bMACD okay,b', 'MACD OK'),
(r'b Improve data filtering `b', 'Improve data filtering'),
(r'b', 'by date'),
(r'b of CSV'b', 'in CSV'),
(r'bJSON files `b', 'JSON files'),
(r'b'b' notes'b', 'to requests'),
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
print("2. check for remating Russian text: git log --format='%s' grep-E'[A-Ya-Yo]')
 print("3. If everything looks good, Push: git Push --force origin v0.5.8")
 else:
 print(f"\n✗ Error during filter-branch:", file=sys.stderr)
 print(result.stderr, file=sys.stderr)
 sys.exit(1)


if __name__ == '__main__':
 main()

