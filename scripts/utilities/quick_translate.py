#!/usr/bin/env python3
"""
Quick translation script without API - Uses comprehensive pattern matching.
"""

import os
import re
from pathlib import Path
from collections import OrderedDict

# Comprehensive Russian to English translations
TRANSLATIONS = OrderedDict([
    # Common Russian words and phrases
    (r'File not found', 'File not found'),
    (r'Missing columns', 'Missing columns'),
    (r'Setting index', 'Setting index'),
    (r'Creating temporary index', 'Creating temporary index'),
    (r'Loading data', 'Loading data'),
    (r'checking presence', 'checking presence'),
    (r'Using', 'Using'),
    (r'specific file', 'specific file'),
    (r'if specified', 'if specified'),
    (r'not found', 'not found'),
    (r'required', 'required'),
    (r'columns', 'columns'),
    (r'presence', 'presence'),
    (r'checking', 'checking'),
    (r'Loading', 'Loading'),
    (r'data', 'data'),
    (r'not available', 'not available'),
    (r'symbol', 'symbol'),
    (r'Timeframe', 'Timeframe'),
    (r'Authentication Management', 'Authentication Management'),
    (r'HTTP client', 'HTTP client'),
    (r'Style constants', 'Style constants'),
    (r'services', 'services'),
    (r'installation check', 'installation check'),
    (r'reinstall dependencies', 'reinstall dependencies'),
    (r'dependencies', 'dependencies'),
    (r'import', 'import'),
    (r'ports', 'ports'),
    (r'with ports', 'with ports'),
    (r'View networks', 'View networks'),
    (r'clean networks', 'clean networks'),
    (r'create network', 'create network'),
    (r'health check', 'health check'),
    (r'mobile API', 'mobile API'),
    (r'Data for main screen', 'Data for main screen'),
    (r'User Portfolio', 'User Portfolio'),
    (r'List of funds', 'List of funds'),
    (r'Investment Management', 'Investment Management'),
    (r'Run all tests', 'Run all tests'),
    (r'CLI interface', 'CLI interface'),
    (r'team Structure', 'team Structure'),
    (r'commercialization for', 'commercialization for'),
    (r'SaaS platform', 'SaaS platform'),
    (r'Use specific file if specified', 'Use specific file if specified'),
    (r'File not found', 'File not found'),
    (r'for specified symbol', 'for specified symbol'),
    (r'symbol and', 'symbol and'),
    (r'will be Used sequential', 'will be Used sequential'),
    (r'not available -', 'not available -'),
    (r'Use standard path', 'Use standard path'),
    (r'standard path', 'standard path'),
    (r'checking presence of required', 'checking presence of required'),
    (r'as datetime if present', 'as datetime if present'),
    (r'if not present', 'if not present'),
    (r'Data Synchronization', 'Data Synchronization'),
    (r'Push notifications', 'Push notifications'),
    (r'Technical details', 'Technical details'),
    (r'File Structure', 'File Structure'),
    (r'Analysis', 'Analysis'),
    (r'Timeframes', 'Timeframes'),
    (r'Timeframes', 'Timeframes'),
    (r'What components are included in the system', 'What components are included in the system'),
    (r'Detailed guide on all components', 'Detailed guide on all components'),
    (r'Launch', 'Launch'),
    (r'Calculations', 'Calculations'),
    (r'Working with data', 'Working with data'),
    (r'included in', 'included in'),
    (r'components', 'components'),
    (r'What', 'What'),
    (r'included', 'included'),
    (r'system', 'system'),
    (r'Detailed', 'Detailed'),
    (r'all', 'all'),
    (r'components', 'components'),
    (r'Working', 'Working'),
    (r'interface', 'interface'),
    (r'team', 'team'),
    (r'Structure', 'Structure'),
    (r'organization', 'organization'),
    (r'Missing', 'Missing'),
    (r'Setting', 'Setting'),
    (r'index', 'index'),
    (r'as datetime', 'as datetime'),
    (r'if present', 'if present'),
    (r'Creating', 'Creating'),
    (r'temporary', 'temporary'),
    (r'not present', 'not present'),
    (r'if it', 'if it'),
    (r'Synchronization', 'Synchronization'),
    (r'notifications', 'notifications'),
    (r'Push', 'Push'),
    (r'Technical', 'Technical'),
    (r'details', 'details'),
    (r'Structure', 'Structure'),
    (r'files', 'files'),
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
    (r'Launch', 'Launch'),
    (r'all tests', 'all tests'),
    (r'all', 'all'),
    (r'tests', 'tests'),
    # Common single words
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
    # Additional common phrases
    (r'installation', 'installation'),
    (r'package installation', 'package installation'),
    (r'check', 'check'),
    (r'installation check', 'installation check'),
    (r'clean', 'clean'),
    (r'cache', 'cache'),
    (r'reinstall', 'reinstall'),
    (r'Launch', 'Launch'),
    (r'start', 'start'),
    (r'coverage', 'coverage'),
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
    (r'including', 'including'),
    (r'messages', 'messages'),
    (r'execute', 'execute'),
    (r'Informing about', 'Informing about'),
    (r'training mode', 'training mode'),
    (r'acceleration', 'acceleration'),
    (r'install', 'install'),
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
    # Additional phrases from troubleshooting
    (r'View events', 'View events'),
    (r'pod Logs', 'pod Logs'),
    (r'with services', 'with services'),
    (r'service issues', 'service issues'),
    (r'View services', 'View services'),
    (r'describe service', 'describe service'),
    (r'with deployment', 'with deployment'),
    (r'deployment issues', 'deployment issues'),
    (r'View deployments', 'View deployments'),
    (r'describe deployment', 'describe deployment'),
    (r'Rollback deployment', 'Rollback deployment'),
    (r'events', 'events'),
    (r'Logs', 'Logs'),
    (r'pod', 'pod'),
    (r'services', 'services'),
    (r'services', 'services'),
    (r'describe', 'describe'),
    (r'service', 'service'),
    (r'deployment', 'deployment'),
    (r'deployments', 'deployments'),
    (r'deployment', 'deployment'),
    (r'Rollback', 'Rollback'),
    (r'deployment', 'deployment'),
    # Documentation phrases
    (r'environment installation', 'environment installation'),
    (r'Create optimal environment', 'Create optimal environment'),
    (r'for development', 'for development'),
    (r'robust ML systems', 'robust ML systems'),
    (r'ideal for', 'ideal for'),
    (r'chip revolutionized', 'chip revolutionized'),
    (r'Theory:', 'Theory:'),
    (r'UMA allows', 'UMA allows'),
    (r'use shared memory', 'Use shared memory'),
    (r'without copying data', 'without copying data'),
    (r'between devices', 'between devices'),
    (r'This is critical for', 'This is critical for'),
    (r'ML work', 'ML work'),
    (r'where large datasets', 'where large datasets'),
    (r'require fast access', 'require fast access'),
    (r'to memory', 'to memory'),
    (r'Practical advantages', 'Practical advantages'),
    (r'Speed:', 'Speed:'),
    (r'data are not copied', 'data are not copied'),
    (r'which speeds up processing', 'which speeds up processing'),
    (r'by 3-5 times', 'by 3-5 times'),
    (r'Memory efficiency', 'Memory efficiency'),
    (r'One dataset', 'One dataset'),
    (r'is used by both CPU and GPU', 'is Used by both CPU and GPU'),
    (r'Scalability:', 'Scalability:'),
    (r'up to 32GB shared memory', 'up to 32GB shared memory'),
    (r'for large models', 'for large models'),
    (r'Programming simplicity', 'Programming simplicity'),
    (r'no need to manage', 'no need to manage'),
    (r'data transfer', 'data transfer'),
    (r'Disadvantages:', 'Disadvantages:'),
    (r'Limited memory', 'Limited memory'),
    (r'compared to', 'compared to'),
    (r'discrete GPUs', 'discrete GPUs'),
    (r'Lower performance', 'lower performance'),
    (r'for very large models', 'for very large models'),
    (r'Specialized', 'Specialized'),
    (r'processor for', 'processor for'),
    (r'machine learning', 'machine learning'),
    (r'optimized for', 'optimized for'),
    (r'operations with', 'operations with'),
    (r'matrices', 'matrices'),
    (r'neural networks', 'neural networks'),
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
    r'^\./Logs/.*',
    r'^\./models/.*',
    r'^\./results/.*',
]

INCLUDE_EXTENSIONS = {'.py', '.md', '.txt'}


def should_exclude_file(file_path: str) -> bool:
    """check if file should be excluded."""
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def has_russian(text: str) -> bool:
    """check if text contains Russian."""
 return bool(re.search(r'[А-Яа-яЁё]', text))


def translate_text(text: str) -> str:
    """Translate Russian text."""
    if not has_russian(text):
        return text
    
    translated = text
    for pattern, replacement in TRANSLATIONS.items():
        translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)
    
    return translated


def main():
    """main function."""
    print("Quick translation (pattern-based, no API)...")
    
    files_processed = 0
    files_changed = 0
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not should_exclude_file(os.path.join(root, d))]
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, '.')
            
            if should_exclude_file(rel_path):
                continue
            
            if Path(file).suffix not in INCLUDE_EXTENSIONS:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not has_russian(content):
                    continue
                
                translated = translate_text(content)
                
                if translated != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(translated)
                    files_changed += 1
                    print(f"✓ {rel_path}")
                
                files_processed += 1
            except Exception as e:
                print(f"✗ {rel_path}: {e}")
    
    print(f"\nProcessed: {files_processed}, Changed: {files_changed}")


if __name__ == '__main__':
    main()

