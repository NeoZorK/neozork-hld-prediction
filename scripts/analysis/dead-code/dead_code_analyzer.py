#!/usr/bin/env python3
"""
Dead Code and Dead Libraries Analyzer

This script performs comprehensive analysis to find:
1. Dead code (unused functions, classes, variables)
2. Dead libraries (unused dependencies)
3. Unused imports
4. Dead files (files not imported anywhere)

Usage:
    python dead_code_analyzer.py [options]
    uv run python dead_code_analyzer.py [options]

Options:
    --dead-code          Analyze dead code (functions, classes, variables)
    --dead-libraries     Analyze dead libraries (unused dependencies)
    --dead-files         Analyze dead files (unused modules)
    --all                Run all analyses
    --fix-imports        Remove unused imports automatically
    --fix-requirements   Update requirements.txt to remove unused packages
    --output-format      Output format: text, json, html (default: text)
    --verbose            Verbose output
"""

import os
import sys
import ast
import re
import json
import argparse
import subprocess
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Any, Optional
import datetime
from dataclasses import dataclass, asdict

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x, **kwargs: x

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

@dataclass
class DeadCodeItem:
    """Represents a dead code item"""
    name: str
    type: str  # function, class, variable, import
    file_path: str
    line_number: int
    context: str
    severity: str  # high, medium, low

@dataclass
class DeadLibraryItem:
    """Represents a dead library"""
    package_name: str
    import_name: str
    usage_count: int
    files_used_in: List[str]
    is_optional: bool = False

@dataclass
class DeadFileItem:
    """Represents a dead file"""
    file_path: str
    file_type: str
    size_bytes: int
    last_modified: str
    potential_reason: str

class DeadCodeAnalyzer:
    """Comprehensive dead code and library analyzer"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_dir = project_root / "src"
        self.tests_dir = project_root / "tests"
        self.scripts_dir = project_root / "scripts"
        
        # Standard library modules
        self.stdlib_modules = self._get_stdlib_modules()
        
        # Package mappings
        self.package_to_import = {
            'scikit-learn': 'sklearn',
            'python-dateutil': 'dateutil',
            'beautifulsoup4': 'bs4',
            'pyyaml': 'yaml',
            'plotext': 'plotext',
            'pillow': 'pil',
            'matplotlib-inline': 'matplotlib_inline',
            'ipython-pygments-lexers': 'ipython_pygments_lexers',
            'jupyter-core': 'jupyter_core',
            'jupyter-client': 'jupyter_client',
            'prometheus-client': 'prometheus_client',
            'send2trash': 'send2trash',
            'nest-asyncio': 'nest_asyncio',
            'python-json-logger': 'pythonjsonlogger',
            'notebook-shim': 'notebook_shim',
            'jupyterlab-pygments': 'jupyterlab_pygments',
            'rpds-py': 'rpds',
            'stack-data': 'stack_data',
            'async-lru': 'async_lru',
            'python-binance': 'binance',
            'polygon-api-client': 'polygon'
        }
        
        self.import_to_package = {v: k for k, v in self.package_to_import.items()}
        
        # Results storage
        self.dead_code_items: List[DeadCodeItem] = []
        self.dead_libraries: List[DeadLibraryItem] = []
        self.dead_files: List[DeadFileItem] = []
        self.import_usage: Dict[str, Set[str]] = defaultdict(set)
        self.function_usage: Dict[str, Set[str]] = defaultdict(set)
        self.class_usage: Dict[str, Set[str]] = defaultdict(set)
        
    def _get_stdlib_modules(self) -> Set[str]:
        """Get standard library modules"""
        stdlib_modules = {
            'os', 'sys', 're', 'math', 'datetime', 'time', 'random', 'json',
            'pathlib', 'collections', 'itertools', 'functools', 'types',
            'argparse', 'logging', 'io', 'pickle', 'csv', 'sqlite3', 'configparser',
            'ast', 'shutil', 'tempfile', 'glob', 'fnmatch', 'uuid', 'hashlib',
            'abc', 'array', 'asyncio', 'base64', 'binascii', 'bisect', 'builtins',
            'bz2', 'calendar', 'cgi', 'cgitb', 'cmd', 'code', 'codecs', 'codeop',
            'colorsys', 'compileall', 'concurrent', 'contextlib', 'copy', 'copyreg',
            'crypt', 'dataclasses', 'decimal', 'difflib', 'dis', 'distutils',
            'doctest', 'email', 'encodings', 'enum', 'filecmp', 'fileinput',
            'formatter', 'fractions', 'ftplib', 'getopt', 'getpass', 'gettext',
            'gzip', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp',
            'importlib', 'inspect', 'ipaddress', 'keyword', 'linecache', 'locale',
            'lzma', 'mailbox', 'mailcap', 'marshal', 'mimetypes', 'mmap', 'modulefinder',
            'multiprocessing', 'netrc', 'numbers', 'operator', 'optparse', 'os',
            'platform', 'poplib', 'posixpath', 'pprint', 'profile', 'pstats', 'pty',
            'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'runpy',
            'sched', 'secrets', 'selectors', 'shelve', 'signal', 'site', 'smtplib',
            'sndhdr', 'socket', 'socketserver', 'spwd', 'ssl', 'stat', 'statistics',
            'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable',
            'sys', 'sysconfig', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'test',
            'textwrap', 'threading', 'timeit', 'tkinter', 'token', 'tokenize', 'trace',
            'traceback', 'tracemalloc', 'tty', 'turtle', 'turtledemo', 'typing', 'unicodedata',
            'unittest', 'urllib', 'uu', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser',
            'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile', 'zipimport', 'zlib'
        }
        
        # Try to use stdlib_list if available
        try:
            import stdlib_list
            stdlib_modules.update(set(stdlib_list.stdlib_list("3.11")))
        except ImportError:
            pass
            
        return stdlib_modules
    
    def find_python_files(self, directory: Path) -> List[Path]:
        """Find all Python files in directory"""
        python_files = []
        for root, dirs, files in os.walk(directory):
            # Skip __pycache__ and .git directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.pytest_cache', '.venv']]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        return python_files
    
    def analyze_file_imports(self, file_path: Path) -> Dict[str, Any]:
        """Analyze imports in a single file"""
        imports = {
            'imports': set(),
            'from_imports': set(),
            'functions': set(),
            'classes': set(),
            'variables': set(),
            'unused_imports': set()
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Track defined items
            defined_items = set()
            
            for node in ast.walk(tree):
                # Handle imports
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports['imports'].add(name.name.split('.')[0])
                        
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports['from_imports'].add(node.module.split('.')[0])
                
                # Handle function definitions
                elif isinstance(node, ast.FunctionDef):
                    imports['functions'].add(node.name)
                    defined_items.add(node.name)
                
                # Handle class definitions
                elif isinstance(node, ast.ClassDef):
                    imports['classes'].add(node.name)
                    defined_items.add(node.name)
                
                # Handle variable assignments
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            imports['variables'].add(target.id)
                            defined_items.add(target.id)
            
            # Check for unused imports (simplified heuristic)
            all_imports = imports['imports'] | imports['from_imports']
            imports['unused_imports'] = all_imports - defined_items
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            
        return imports
    
    def analyze_dead_code(self) -> List[DeadCodeItem]:
        """Analyze dead code across the project"""
        print("Analyzing dead code...")
        
        python_files = self.find_python_files(self.project_root)
        dead_items = []
        
        for file_path in tqdm(python_files, desc="Analyzing files for dead code"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                # Find all function and class definitions
                defined_items = {}
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        defined_items[node.name] = {
                            'type': 'function' if isinstance(node, ast.FunctionDef) else 'class',
                            'line': node.lineno,
                            'context': self._get_context(content, node.lineno)
                        }
                
                # Check if items are used (simplified heuristic)
                for name, info in defined_items.items():
                    # Skip special methods and main functions
                    if (name.startswith('_') and name.endswith('_')) or name == 'main':
                        continue
                    
                    # Check if the item is used elsewhere
                    usage_count = self._count_usage(name, python_files)
                    
                    if usage_count <= 1:  # Only defined, not used elsewhere
                        dead_items.append(DeadCodeItem(
                            name=name,
                            type=info['type'],
                            file_path=str(file_path.relative_to(self.project_root)),
                            line_number=info['line'],
                            context=info['context'],
                            severity='medium' if usage_count == 1 else 'high'
                        ))
                        
            except Exception as e:
                print(f"Error analyzing dead code in {file_path}: {e}")
        
        return dead_items
    
    def _get_context(self, content: str, line_number: int) -> str:
        """Get context around a line number"""
        lines = content.split('\n')
        start = max(0, line_number - 2)
        end = min(len(lines), line_number + 2)
        return '\n'.join(lines[start:end])
    
    def _count_usage(self, name: str, python_files: List[Path]) -> int:
        """Count usage of a name across Python files"""
        count = 0
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                count += content.count(name)
            except:
                continue
        return count
    
    def analyze_dead_libraries(self) -> List[DeadLibraryItem]:
        """Analyze dead libraries (unused dependencies)"""
        print("Analyzing dead libraries...")
        
        # Get all imports from the project
        python_files = self.find_python_files(self.project_root)
        all_imports = defaultdict(set)
        
        for file_path in python_files:
            imports = self.analyze_file_imports(file_path)
            for imp in imports['imports'] | imports['from_imports']:
                all_imports[imp].add(str(file_path.relative_to(self.project_root)))
        
        # Parse requirements.txt
        requirements = self._parse_requirements()
        
        # Find unused packages
        dead_libraries = []
        for package_name, package_info in requirements.items():
            import_name = self.package_to_import.get(package_name, package_name)
            
            if import_name not in all_imports:
                dead_libraries.append(DeadLibraryItem(
                    package_name=package_name,
                    import_name=import_name,
                    usage_count=0,
                    files_used_in=[],
                    is_optional=self._is_optional_package(package_name)
                ))
            else:
                # Check if it's used in meaningful files (not just tests)
                meaningful_files = [f for f in all_imports[import_name] 
                                  if not f.startswith('tests/') and not f.startswith('scripts/')]
                
                if not meaningful_files:
                    dead_libraries.append(DeadLibraryItem(
                        package_name=package_name,
                        import_name=import_name,
                        usage_count=len(all_imports[import_name]),
                        files_used_in=list(all_imports[import_name]),
                        is_optional=self._is_optional_package(package_name)
                    ))
        
        return dead_libraries
    
    def _parse_requirements(self) -> Dict[str, str]:
        """Parse requirements.txt file"""
        requirements = {}
        req_file = self.project_root / "requirements.txt"
        
        if req_file.exists():
            with open(req_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Extract package name
                        package_name = line.split('==')[0].split('>=')[0].split('<=')[0]
                        requirements[package_name] = line
        
        return requirements
    
    def _is_optional_package(self, package_name: str) -> bool:
        """Check if a package is optional (development, testing, etc.)"""
        optional_keywords = ['test', 'pytest', 'dev', 'debug', 'lint', 'format']
        return any(keyword in package_name.lower() for keyword in optional_keywords)
    
    def analyze_dead_files(self) -> List[DeadFileItem]:
        """Analyze dead files (files not imported anywhere)"""
        print("Analyzing dead files...")
        
        python_files = self.find_python_files(self.project_root)
        imported_files = set()
        dead_files = []
        
        # Find all imported modules
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            module_name = name.name
                            # Try to find the corresponding file
                            module_file = self._find_module_file(module_name)
                            if module_file:
                                imported_files.add(str(module_file))
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            module_file = self._find_module_file(node.module)
                            if module_file:
                                imported_files.add(str(module_file))
                                
            except Exception as e:
                print(f"Error analyzing imports in {file_path}: {e}")
        
        # Find files that are not imported
        for file_path in python_files:
            rel_path = str(file_path.relative_to(self.project_root))
            
            # Skip special files
            if (file_path.name in ['__init__.py', '__main__.py'] or
                file_path.name.startswith('test_') or
                'test' in file_path.parts):
                continue
            
            if rel_path not in imported_files:
                try:
                    stat = file_path.stat()
                    dead_files.append(DeadFileItem(
                        file_path=rel_path,
                        file_type='python',
                        size_bytes=stat.st_size,
                        last_modified=datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        potential_reason='Not imported anywhere'
                    ))
                except Exception as e:
                    print(f"Error getting file info for {file_path}: {e}")
        
        return dead_files
    
    def _find_module_file(self, module_name: str) -> Optional[Path]:
        """Find the file corresponding to a module name"""
        # Convert module name to file path
        module_path = module_name.replace('.', '/')
        
        # Try different extensions
        for ext in ['.py', '/__init__.py']:
            file_path = self.project_root / 'src' / f"{module_path}{ext}"
            if file_path.exists():
                return file_path
        
        return None
    
    def run_analysis(self, analyze_dead_code: bool = True, 
                    analyze_dead_libraries: bool = True,
                    analyze_dead_files: bool = True) -> Dict[str, Any]:
        """Run comprehensive analysis"""
        results = {}
        
        if analyze_dead_code:
            self.dead_code_items = self.analyze_dead_code()
            results['dead_code'] = [asdict(item) for item in self.dead_code_items]
        
        if analyze_dead_libraries:
            self.dead_libraries = self.analyze_dead_libraries()
            results['dead_libraries'] = [asdict(item) for item in self.dead_libraries]
        
        if analyze_dead_files:
            self.dead_files = self.analyze_dead_files()
            results['dead_files'] = [asdict(item) for item in self.dead_files]
        
        return results
    
    def print_results(self, results: Dict[str, Any], verbose: bool = False):
        """Print analysis results"""
        print("\n" + "="*60)
        print("DEAD CODE AND LIBRARIES ANALYSIS RESULTS")
        print("="*60)
        
        # Dead Code Results
        if 'dead_code' in results:
            print(f"\n🔍 DEAD CODE ANALYSIS ({len(results['dead_code'])} items found)")
            print("-" * 40)
            
            if not results['dead_code']:
                print("✅ No dead code found!")
            else:
                for item in results['dead_code']:
                    print(f"❌ {item['type'].upper()}: {item['name']}")
                    print(f"   File: {item['file_path']}:{item['line_number']}")
                    print(f"   Severity: {item['severity']}")
                    if verbose:
                        print(f"   Context: {item['context']}")
                    print()
        
        # Dead Libraries Results
        if 'dead_libraries' in results:
            print(f"\n📦 DEAD LIBRARIES ANALYSIS ({len(results['dead_libraries'])} items found)")
            print("-" * 40)
            
            if not results['dead_libraries']:
                print("✅ No dead libraries found!")
            else:
                for item in results['dead_libraries']:
                    print(f"❌ Package: {item['package_name']}")
                    print(f"   Import: {item['import_name']}")
                    print(f"   Usage count: {item['usage_count']}")
                    if item['files_used_in']:
                        print(f"   Used in: {', '.join(item['files_used_in'][:3])}")
                    if item['is_optional']:
                        print(f"   Note: Optional package (dev/test)")
                    print()
        
        # Dead Files Results
        if 'dead_files' in results:
            print(f"\n📁 DEAD FILES ANALYSIS ({len(results['dead_files'])} items found)")
            print("-" * 40)
            
            if not results['dead_files']:
                print("✅ No dead files found!")
            else:
                for item in results['dead_files']:
                    print(f"❌ File: {item['file_path']}")
                    print(f"   Size: {item['size_bytes']} bytes")
                    print(f"   Last modified: {item['last_modified']}")
                    print(f"   Reason: {item['potential_reason']}")
                    print()
        
        # Summary
        total_issues = (len(results.get('dead_code', [])) + 
                       len(results.get('dead_libraries', [])) + 
                       len(results.get('dead_files', [])))
        
        print(f"\n📊 SUMMARY")
        print("-" * 40)
        print(f"Total issues found: {total_issues}")
        print(f"Dead code items: {len(results.get('dead_code', []))}")
        print(f"Dead libraries: {len(results.get('dead_libraries', []))}")
        print(f"Dead files: {len(results.get('dead_files', []))}")
        
        if total_issues > 0:
            print(f"\n💡 RECOMMENDATIONS:")
            print("- Consider removing unused functions and classes")
            print("- Remove unused dependencies from requirements.txt")
            print("- Delete or refactor unused files")
            print("- Review test coverage for removed code")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Dead Code and Libraries Analyzer")
    parser.add_argument('--dead-code', action='store_true', help='Analyze dead code')
    parser.add_argument('--dead-libraries', action='store_true', help='Analyze dead libraries')
    parser.add_argument('--dead-files', action='store_true', help='Analyze dead files')
    parser.add_argument('--all', action='store_true', help='Run all analyses')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--output-format', choices=['text', 'json', 'html'], 
                       default='text', help='Output format')
    parser.add_argument('--output-file', help='Output file path')
    
    args = parser.parse_args()
    
    # Default to all analyses if none specified
    if not any([args.dead_code, args.dead_libraries, args.dead_files, args.all]):
        args.all = True
    
    if args.all:
        args.dead_code = True
        args.dead_libraries = True
        args.dead_files = True
    
    # Initialize analyzer
    analyzer = DeadCodeAnalyzer(PROJECT_ROOT)
    
    # Run analysis
    results = analyzer.run_analysis(
        analyze_dead_code=args.dead_code,
        analyze_dead_libraries=args.dead_libraries,
        analyze_dead_files=args.dead_files
    )
    
    # Output results
    if args.output_format == 'json':
        output = json.dumps(results, indent=2)
    elif args.output_format == 'html':
        output = analyzer._generate_html_report(results)
    else:
        analyzer.print_results(results, verbose=args.verbose)
        return
    
    # Write to file or stdout
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(output)
        print(f"Results written to {args.output_file}")
    else:
        print(output)

if __name__ == "__main__":
    main()
