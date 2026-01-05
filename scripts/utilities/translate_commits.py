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
r'\updating documentation on the full pay system 100%\+in month\b': 'update documentation on completing system 100%+ per month',
r' re-update documentation on Monitoring system and metrics for achieving 100% profit `b': 'update documentation on Monitoring system and metrics for Achieving 100% profit',
r'update documentation on metrics and monitoring for achievement 100% profit/b': 'update documentation on metrics and Monitoring for processing 100% benefit',
r'update documentation on detailed components of NeoZorK\b': 'update documentation on Detailed components of NeoZorK system',
r'\update documentation on installation and installation of MLX and Jupiter for Apple Silicon\b': 'update documentation on installation and negotiation of MLX and Jupiter for Apple Silicon',
r'\update documentation on basic robotic systems in ML\b': 'update documentation on basics of Robst systems in ML',
r' `update documentation on data production and data creation for ML systems',
r'update documentation on evidence engineering and training models for financial data_b': 'update documentation on finance engineering and method training for financial data',
r'\update documentation on Monte Carlo simulation and risk management /b': 'update documentation on Monte Carlo simulation and Risk Management',
r'\update of SCHR Analysis Documents and SCHR SHORT3\b': `update documentation on SCHR Movements and SCHR SHORT3 Analysis',
r' rejuvenation of files ..dockerignore and ..gitignore for\b': 'update .dockerignore and .gitignore profiles for',
r'update files ..dockerignore and ..gitignore for deletion and inclusion of documentation .b': 'update .dockerignore and .gitignore profiles for graduation and incorporation of documentation',
r' rejuvenation of files ..dockerignore and ..gitignore for statement .b': 'update .dockerignore and .gitignore profiles for decomposition',
r'\renewal of data exports of metadata in the time series decomposite \b': 'update metadata export finance in time series decomposition',
r'\baddition of new functions for visualizing the results of CEMEDAN\b': 'add new findings for CEEMDAN visualization results',
r'\bbaddition of new functions for decomposition of time series \b': 'add new findings for time series decomposition',
r'baddition of the time-series decomposite module 'b': 'add time series decomposition modeule',
r'\baddition of the SSRF vulnerability correction patch in the ip\b' package: 'add patch to fix SSRF vulnerability in ip package',
r'\addition of the security manual for API vulnerability sending Ray\b': 'add security guide for Ray jab submission API vulnerability',
r'\addition of documentation on vulnerability CVE 2025-53000 in nbconvert\b': 'add documentation on CVE 2025-53000 vulnerability in nbconvert',
r'=Background specification of dependencies urllib3\b': 'clarify urllib3 dependency specifier',
r'\update time tags in documentation and scripts 'b': 'update timeamps in documentation and scripts',

 # Common phrases
r'badditiondependencies 'b': 'add dependency',
r' rejuvenation dependencies 'b': 'update dependency',
r'\baddition of documentation_b': 'add documentation',
r'\updating documentation_b': 'update documentation',
r''baddition of patch 'b': 'add patch',
r'\bbaddition of new functions_b': 'add new functions',
r'\renewal functions\b': 'update function',
r'\baddition module 'b': 'add module',
r'_update file sheets',
r'\baddition of new dependencies\b': 'add new dependencies',

 # Common verbs
r'\update 'b': 'update',
r'\bbb': 'add',
r'\b': 'clarify',
r'·b' correction /b': 'fix',
r'b': 'remove',
r'\b': 'improve',
r'\brefector',
r'·b' change 'b': 'change',
r'`b' creation 'b': 'create',
r'\bd': 'configure',

 # Specific phrases
r'\b before version `b': 'to version',
r'b in paperage\.json\b': 'to package.json',
r'b in pyproject /.toml\b': 'to pyproject.toml',
r'\b in statements\.txt\b': 'to requests.txt',
r'\b in documentation_b': 'in documentation',
r'\b in scripts 'b': 'in scripts',
r'\b for\b': 'for',
r'\bpo\b': 'on',
r'\b with the addition 'b': 'with extension of',
r'bi'b': 'and',

 # Documentation specific
r'\b manuals on /b': 'guid on',
r'\bmouse on\b': 'guid on',
r' `vulnerability',
r'vulnerability 'b': 'vulnerability'
r'\b security_b': 'security',
r'time tags 'b': 'timestamps',
r'time rows 'b': 'time series',
r'\bdecomposite_b': 'decomposition',
r'\bexport metadata_b': 'metadata export',
r'\bvising results_b': 'visualization results',
r'\bmetricks and Monitoring_b': 'metrics and Monitoring',
r'\b to achieve 100% profit \b': 'for achieving 100% profit',
r'\banalysis',
r'\bMonte-Carlo simulations 'b': 'Monte carlo simulation',
r' risk management_b': 'risk Management',
r'·b': 'feature engineering',
r'\model learning \b': 'model training',
r'\bfinancial data_b': 'financial data',
r'\b data training \b': 'data preparation',
r'\bformation of signs 'b': 'feature creation',
r'\bML systems_b': 'ML systems',
r'brands of robotic systems 'b': 'baseics of Robist systems',
r'_place and setup 'b': 'installation and configration',
"R" is a "detained components",
r'\bsystem Monitoring_b': 'Monitoring system',
r' full system of earnings \b': 'complete development system',
r'\blockchin systems_b': 'lockchain systems',
r'\bautomatic retraining',
r'``b Concepts and strategies 'b': 'Concepts and strategies',
r' high-income ML systems 'b': 'high-yeld ML systems',
r'\btrade systems 'b': 'trading systems',
r'\blockchen integration_b': 'lockchain integration',
r'\bmetricks Analysis performance\b': 'Performance Analysis metrics',
r'&b advanced practitioners `b': 'advanced practices',
r'&boptimization of Portfolio\b': 'Porthfolio optimization',
r'`btheoretical justifications 'b': 'theoretical foundations',
r'&b levels of support and resistance `b': 'support and resistance movements',
r'\b' machine learning 'b': 'Machine learning'
r'\bstructural structure `b': 'documentation Structure',
r'\b': 'new sections',
r' `exclusion and inclusion',

 # More specific translations
r'\b of the Dependencies 'b': 'dependency specifier',
r'=new versions 'b': 'new versions',
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
'feat: add new preferences in project':
 'feat: add new dependencies to project',
'fix: update .dockerignore and .gitignore profiles for deletion and inclusion of documentation':
 'fix: update .dockerignore and .gitignore files for exclusion and inclusion of documentation',
'feat: up-date documentation on the ML systems' concept and strategy:
 'feat: update documentation on Concepts and strategies of high-yield ML systems',
'feat: up-date documentation on examples of trafficking systems on basic WAVE2, SCHR Movements and blockchain integration':
 'feat: update documentation on examples of trading systems based on WAVE2, SCHR Levels and blockchain integration',
'feat: up-to-date documentation SCHR SHORT3 with extension of theoretical reasoning and Analysis':
 'feat: update documentation SCHR SHORT3 with addition of theoretical foundations and Analysis',
'feat: up-to-date documentation SCHR Movements with extension of new sections on support and resistance levels':
 'feat: update documentation SCHR Levels with addition of new sections on Analysis of support and resistance levels',
'feat: predated documentation structure NeoZorK with extension of new sections':
 'feat: update NeoZorK documentation Structure with addition of new sections',
'feat: Added new sections on data prevention, management, model training, backtting and Risk Management':
 'feat: add new sections on data preparation, feature engineering, model training, backtesting and risk Management',
'feat: extradate of NeoZorK with setting environment for machos M1 Pro':
 'feat: update NeoZorK guide with installation of environment for macOS M1 Pro',
'feat: Added HTML-interface for textbook':
 'feat: add HTML interface for tutorial',
'feat: a complete system of earnings 100%+in month has been added - a detailed system with working code from ideas to fault has been created - all components added: models, indicators, block-integration - Automatic retraining has been implemented - A complete Monitoring and Alert System has been added - Documentation on Launch and use - System ready for testing on blocks testnet:
 'feat: add complete earning system 100%+ per month - Created Detailed system with Working code from idea to deployment - Added all components: models, indicators, blockchain integration - Implemented automatic retraining system - Added full Monitoring and alert system - Created documentation on Launch and usage - system ready for testing on blockchain testnet',
'feat: A complete textbook has been created on creating robotic profitable ML systems':
 'feat: create complete tutorial on Creating robust profitable ML systems',
"Add simplification and promotional activities to AutoML Gluon presentation - Introduced two new sections: "Simple example" and "Challenged exemplification" involving the development and development of the robin ML methodsUSING AutoML Gluon. - Including Detailed codes, architecture diagrams, and performance methods for other applications. - Update the AutoML Gluon manial and README to refuse the new experiences, reflecting the communication\'s compliance and enforcement.- Added a script for generating graphics related to the production examples, improving visual representation. These additions provide Users with practical insights into building and deploying ML models, catering to both novice and advanced Users.':
 'Add simple and advanced production examples to AutoML Gluon documentation - Introduced two new sections: "Simple Example" and "Advanced Example" showcasing the development and deployment of robust ML models Using AutoML Gluon. - included Detailed code examples, architecture diagrams, and performance metrics for both approaches. - Updated the AutoML Gluon manual and README to reference the new examples, enhancing the documentation\'s comprehensiveness and usability. - Added a script for generating graphics related to the production examples, improving visual representation. These additions provide Users with practical insights into building and deploying ML models, catering to both novice and advanced Users.',
'fix dual charters for -d present and MACD ok with scal data':
 'fix dual charts for -d fastest and MACD OK with scale date',
'fix dual charters for -d present and MACD ok':
 'fix dual charts for -d fastest and MACD OK',
'feat: Improve data filtering on date in CSV and JSON files ':
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
Return bool (re.search(r'[A-Ya-Yo], text))


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

