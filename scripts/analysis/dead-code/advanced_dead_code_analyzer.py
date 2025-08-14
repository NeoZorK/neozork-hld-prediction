#!/usr/bin/env python3
"""
Advanced Dead Code and Duplicate Code Analyzer

This script provides comprehensive analysis with accurate algorithms:
1. Dead Code: Functions/classes that are never called (not just text search)
2. Dead Libraries: Unused dependencies with proper import analysis
3. Duplicate Code: Code duplication detection
4. Interactive Menu: Choose what to analyze

Features:
- AST-based analysis for accurate function call detection
- Import tracking across the entire codebase
- Duplicate code detection using similarity algorithms
- Interactive menu for selective analysis
- Detailed reporting with confidence scores
"""

import os
import sys
import ast
import re
import json
import argparse
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Any, Optional
import datetime
from dataclasses import dataclass, asdict
import difflib
from enum import Enum

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x, **kwargs: x

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

class AnalysisType(Enum):
    """Types of analysis available"""
    DEAD_CODE = "dead_code"
    DEAD_LIBRARIES = "dead_libraries"
    DUPLICATE_CODE = "duplicate_code"
    ALL = "all"

@dataclass
class DeadCodeItem:
    """Represents a dead code item with detailed analysis"""
    name: str
    type: str  # function, class, method
    file_path: str
    line_number: int
    context: str
    severity: str  # high, medium, low
    confidence: float  # 0.0 to 1.0
    reason: str
    potential_uses: List[str]  # Where it might be used
    is_public_api: bool = False

@dataclass
class DeadLibraryItem:
    """Represents a dead library with detailed analysis"""
    package_name: str
    import_name: str
    usage_count: int
    files_used_in: List[str]
    is_optional: bool = False
    confidence: float = 1.0
    reason: str = ""

@dataclass
class DuplicateCodeItem:
    """Represents duplicate code"""
    file1: str
    file2: str
    line1_start: int
    line1_end: int
    line2_start: int
    line2_end: int
    similarity: float
    code_snippet: str
    size_lines: int

class AdvancedDeadCodeAnalyzer:
    """Advanced dead code and duplicate code analyzer"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_dir = project_root / "src"
        self.tests_dir = project_root / "tests"
        self.scripts_dir = project_root / "scripts"
        
        # Analysis results
        self.dead_code_items: List[DeadCodeItem] = []
        self.dead_libraries: List[DeadLibraryItem] = []
        self.duplicate_code_items: List[DuplicateCodeItem] = []
        
        # Internal tracking
        self.function_calls: Dict[str, Set[str]] = defaultdict(set)  # function -> files where called
        self.class_instantiations: Dict[str, Set[str]] = defaultdict(set)
        self.imports: Dict[str, Set[str]] = defaultdict(set)
        self.defined_functions: Dict[str, Dict] = {}
        self.defined_classes: Dict[str, Dict] = {}
        
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
    
    def analyze_function_calls(self, file_path: Path) -> Dict[str, Set[str]]:
        """Analyze function calls in a file using AST"""
        calls = defaultdict(set)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # Handle direct function calls
                    if isinstance(node.func, ast.Name):
                        calls[node.func.id].add(str(file_path.relative_to(self.project_root)))
                    
                    # Handle method calls (obj.method())
                    elif isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name):
                            calls[f"{node.func.value.id}.{node.func.attr}"].add(str(file_path.relative_to(self.project_root)))
                
                # Handle class instantiations
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    # This might be a class instantiation
                    calls[f"__init__:{node.func.id}"].add(str(file_path.relative_to(self.project_root)))
                
                # Handle imports
                elif isinstance(node, ast.Import):
                    for name in node.names:
                        calls[name.name.split('.')[0]].add(str(file_path.relative_to(self.project_root)))
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        calls[node.module.split('.')[0]].add(str(file_path.relative_to(self.project_root)))
                        
        except Exception as e:
            print(f"Error analyzing function calls in {file_path}: {e}")
        
        return calls
    
    def analyze_defined_items(self, file_path: Path) -> Tuple[Dict[str, Dict], Dict[str, Dict]]:
        """Analyze defined functions and classes in a file"""
        functions = {}
        classes = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions[node.name] = {
                        'file': str(file_path.relative_to(self.project_root)),
                        'line': node.lineno,
                        'is_public': not node.name.startswith('_'),
                        'is_main': node.name == 'main',
                        'is_test': node.name.startswith('test_'),
                        'context': self._get_context(content, node.lineno)
                    }
                
                elif isinstance(node, ast.ClassDef):
                    classes[node.name] = {
                        'file': str(file_path.relative_to(self.project_root)),
                        'line': node.lineno,
                        'is_public': not node.name.startswith('_'),
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                        'context': self._get_context(content, node.lineno)
                    }
                        
        except Exception as e:
            print(f"Error analyzing defined items in {file_path}: {e}")
        
        return functions, classes
    
    def _get_context(self, content: str, line_number: int) -> str:
        """Get context around a line number"""
        lines = content.split('\n')
        start = max(0, line_number - 2)
        end = min(len(lines), line_number + 2)
        return '\n'.join(lines[start:end])
    
    def analyze_dead_code_advanced(self) -> List[DeadCodeItem]:
        """Advanced dead code analysis using AST-based function call tracking"""
        print("Analyzing dead code with advanced AST-based detection...")
        
        python_files = self.find_python_files(self.project_root)
        dead_items = []
        
        # First pass: collect all defined functions and classes
        all_functions = {}
        all_classes = {}
        
        for file_path in tqdm(python_files, desc="Collecting defined items"):
            functions, classes = self.analyze_defined_items(file_path)
            all_functions.update(functions)
            all_classes.update(classes)
        
        # Second pass: collect all function calls
        all_calls = defaultdict(set)
        
        for file_path in tqdm(python_files, desc="Analyzing function calls"):
            calls = self.analyze_function_calls(file_path)
            for func_name, files in calls.items():
                all_calls[func_name].update(files)
        
        # Third pass: identify dead code
        for func_name, func_info in all_functions.items():
            # Skip special cases
            if (func_info['is_main'] or 
                func_info['is_test'] or 
                func_name.startswith('__') and func_name.endswith('__')):
                continue
            
            # Check if function is called
            called_files = all_calls.get(func_name, set())
            
            if not called_files:
                # Function is never called
                confidence = 0.9 if func_info['is_public'] else 0.7
                reason = "Function is never called anywhere in the codebase"
                
                dead_items.append(DeadCodeItem(
                    name=func_name,
                    type='function',
                    file_path=func_info['file'],
                    line_number=func_info['line'],
                    context=func_info['context'],
                    severity='high' if func_info['is_public'] else 'medium',
                    confidence=confidence,
                    reason=reason,
                    potential_uses=[],
                    is_public_api=func_info['is_public']
                ))
        
        # Check for dead classes
        for class_name, class_info in all_classes.items():
            # Skip special cases
            if class_name.startswith('__') and class_name.endswith('__'):
                continue
            
            # Check if class is instantiated
            instantiated_files = all_calls.get(f"__init__:{class_name}", set())
            
            if not instantiated_files:
                # Class is never instantiated
                confidence = 0.8 if class_info['is_public'] else 0.6
                reason = "Class is never instantiated anywhere in the codebase"
                
                dead_items.append(DeadCodeItem(
                    name=class_name,
                    type='class',
                    file_path=class_info['file'],
                    line_number=class_info['line'],
                    context=class_info['context'],
                    severity='high' if class_info['is_public'] else 'medium',
                    confidence=confidence,
                    reason=reason,
                    potential_uses=[],
                    is_public_api=class_info['is_public']
                ))
        
        return dead_items
    
    def analyze_dead_libraries_advanced(self) -> List[DeadLibraryItem]:
        """Advanced dead library analysis with proper import tracking"""
        print("Analyzing dead libraries with advanced import tracking...")
        
        python_files = self.find_python_files(self.project_root)
        all_imports = defaultdict(set)
        
        # Collect all imports
        for file_path in tqdm(python_files, desc="Analyzing imports"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            all_imports[name.name.split('.')[0]].add(str(file_path.relative_to(self.project_root)))
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            all_imports[node.module.split('.')[0]].add(str(file_path.relative_to(self.project_root)))
                            
            except Exception as e:
                print(f"Error analyzing imports in {file_path}: {e}")
        
        # Parse requirements.txt
        requirements = self._parse_requirements()
        
        # Find unused packages
        dead_libraries = []
        for package_name, package_info in requirements.items():
            import_name = self.package_to_import.get(package_name, package_name)
            
            if import_name not in all_imports:
                # Package is not imported anywhere
                dead_libraries.append(DeadLibraryItem(
                    package_name=package_name,
                    import_name=import_name,
                    usage_count=0,
                    files_used_in=[],
                    is_optional=self._is_optional_package(package_name),
                    confidence=0.95,
                    reason="Package is not imported anywhere in the codebase"
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
                        is_optional=self._is_optional_package(package_name),
                        confidence=0.8,
                        reason="Package is only used in test/script files"
                    ))
        
        return dead_libraries
    
    def analyze_duplicate_code(self, min_similarity: float = 0.8, min_lines: int = 5) -> List[DuplicateCodeItem]:
        """Analyze duplicate code using similarity detection"""
        print("Analyzing duplicate code...")
        
        python_files = self.find_python_files(self.project_root)
        duplicate_items = []
        
        # Read all files and create line-based representations
        file_contents = {}
        for file_path in tqdm(python_files, desc="Reading files"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    file_contents[str(file_path.relative_to(self.project_root))] = lines
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        # Compare files for duplicates
        file_list = list(file_contents.keys())
        
        for i in tqdm(range(len(file_list)), desc="Analyzing duplicates"):
            for j in range(i + 1, len(file_list)):
                file1, file2 = file_list[i], file_list[j]
                
                # Skip comparing test files with non-test files
                if (file1.startswith('tests/') != file2.startswith('tests/')):
                    continue
                
                duplicates = self._find_duplicates_in_files(
                    file1, file2, 
                    file_contents[file1], file_contents[file2],
                    min_similarity, min_lines
                )
                duplicate_items.extend(duplicates)
        
        return duplicate_items
    
    def _find_duplicates_in_files(self, file1: str, file2: str, lines1: List[str], 
                                 lines2: List[str], min_similarity: float, min_lines: int) -> List[DuplicateCodeItem]:
        """Find duplicate code between two files"""
        duplicates = []
        
        # Use difflib to find similar sequences
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        
        for block in matcher.get_matching_blocks():
            if block.size >= min_lines:
                # Calculate similarity
                similarity = self._calculate_similarity(lines1[block.a:block.a+block.size], 
                                                      lines2[block.b:block.b+block.size])
                
                if similarity >= min_similarity:
                    # Extract the duplicate code
                    code_snippet = ''.join(lines1[block.a:block.a+block.size])
                    
                    duplicates.append(DuplicateCodeItem(
                        file1=file1,
                        file2=file2,
                        line1_start=block.a + 1,
                        line1_end=block.a + block.size,
                        line2_start=block.b + 1,
                        line2_end=block.b + block.size,
                        similarity=similarity,
                        code_snippet=code_snippet,
                        size_lines=block.size
                    ))
        
        return duplicates
    
    def _calculate_similarity(self, lines1: List[str], lines2: List[str]) -> float:
        """Calculate similarity between two code blocks"""
        if len(lines1) != len(lines2):
            return 0.0
        
        # Normalize lines (remove whitespace, comments)
        def normalize_line(line: str) -> str:
            line = line.strip()
            # Remove comments
            if '#' in line:
                line = line.split('#')[0].strip()
            return line
        
        normalized1 = [normalize_line(line) for line in lines1]
        normalized2 = [normalize_line(line) for line in lines2]
        
        # Count identical lines
        identical = sum(1 for a, b in zip(normalized1, normalized2) if a == b and a)
        
        return identical / len(lines1) if lines1 else 0.0
    
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
        optional_keywords = ['test', 'pytest', 'dev', 'debug', 'lint', 'format', 'black']
        return any(keyword in package_name.lower() for keyword in optional_keywords)
    
    def run_analysis(self, analysis_types: List[AnalysisType]) -> Dict[str, Any]:
        """Run specified analyses"""
        results = {}
        
        if AnalysisType.DEAD_CODE in analysis_types or AnalysisType.ALL in analysis_types:
            self.dead_code_items = self.analyze_dead_code_advanced()
            results['dead_code'] = [asdict(item) for item in self.dead_code_items]
        
        if AnalysisType.DEAD_LIBRARIES in analysis_types or AnalysisType.ALL in analysis_types:
            self.dead_libraries = self.analyze_dead_libraries_advanced()
            results['dead_libraries'] = [asdict(item) for item in self.dead_libraries]
        
        if AnalysisType.DUPLICATE_CODE in analysis_types or AnalysisType.ALL in analysis_types:
            self.duplicate_code_items = self.analyze_duplicate_code()
            results['duplicate_code'] = [asdict(item) for item in self.duplicate_code_items]
        
        return results
    
    def print_results(self, results: Dict[str, Any], verbose: bool = False):
        """Print analysis results with detailed information"""
        print("\n" + "="*80)
        print("ADVANCED DEAD CODE AND DUPLICATE CODE ANALYSIS RESULTS")
        print("="*80)
        
        # Dead Code Results
        if 'dead_code' in results:
            print(f"\n🔍 DEAD CODE ANALYSIS ({len(results['dead_code'])} items found)")
            print("-" * 60)
            
            if not results['dead_code']:
                print("✅ No dead code found!")
            else:
                for item in results['dead_code']:
                    print(f"❌ {item['type'].upper()}: {item['name']}")
                    print(f"   File: {item['file_path']}:{item['line_number']}")
                    print(f"   Severity: {item['severity']}")
                    print(f"   Confidence: {item['confidence']:.2f}")
                    print(f"   Reason: {item['reason']}")
                    if item['is_public_api']:
                        print(f"   ⚠️  PUBLIC API - Review carefully!")
                    if verbose:
                        print(f"   Context: {item['context']}")
                    print()
        
        # Dead Libraries Results
        if 'dead_libraries' in results:
            print(f"\n📦 DEAD LIBRARIES ANALYSIS ({len(results['dead_libraries'])} items found)")
            print("-" * 60)
            
            if not results['dead_libraries']:
                print("✅ No dead libraries found!")
            else:
                for item in results['dead_libraries']:
                    print(f"❌ Package: {item['package_name']}")
                    print(f"   Import: {item['import_name']}")
                    print(f"   Confidence: {item['confidence']:.2f}")
                    print(f"   Reason: {item['reason']}")
                    if item['files_used_in']:
                        print(f"   Used in: {', '.join(item['files_used_in'][:3])}")
                    if item['is_optional']:
                        print(f"   Note: Optional package (dev/test)")
                    print()
        
        # Duplicate Code Results
        if 'duplicate_code' in results:
            print(f"\n🔄 DUPLICATE CODE ANALYSIS ({len(results['duplicate_code'])} items found)")
            print("-" * 60)
            
            if not results['duplicate_code']:
                print("✅ No duplicate code found!")
            else:
                for item in results['duplicate_code']:
                    print(f"🔄 Duplicate: {item['size_lines']} lines")
                    print(f"   File 1: {item['file1']}:{item['line1_start']}-{item['line1_end']}")
                    print(f"   File 2: {item['file2']}:{item['line2_start']}-{item['line2_end']}")
                    print(f"   Similarity: {item['similarity']:.2f}")
                    if verbose:
                        print(f"   Code: {item['code_snippet'][:200]}...")
                    print()
        
        # Summary
        total_issues = (len(results.get('dead_code', [])) + 
                       len(results.get('dead_libraries', [])) + 
                       len(results.get('duplicate_code', [])))
        
        print(f"\n📊 SUMMARY")
        print("-" * 60)
        print(f"Total issues found: {total_issues}")
        print(f"Dead code items: {len(results.get('dead_code', []))}")
        print(f"Dead libraries: {len(results.get('dead_libraries', []))}")
        print(f"Duplicate code: {len(results.get('duplicate_code', []))}")
        
        if total_issues > 0:
            print(f"\n💡 RECOMMENDATIONS:")
            print("- Review high-confidence dead code items first")
            print("- Check public API functions carefully before removal")
            print("- Consider refactoring duplicate code into shared functions")
            print("- Remove unused dependencies to reduce package size")

def interactive_menu() -> List[AnalysisType]:
    """Interactive menu for choosing analysis types"""
    print("\n🔍 Advanced Dead Code Analysis Menu")
    print("=" * 50)
    print("Choose what to analyze:")
    print("1. Dead Code (functions/classes never called)")
    print("2. Dead Libraries (unused dependencies)")
    print("3. Duplicate Code (code duplication)")
    print("4. All analyses")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                return [AnalysisType.DEAD_CODE]
            elif choice == '2':
                return [AnalysisType.DEAD_LIBRARIES]
            elif choice == '3':
                return [AnalysisType.DUPLICATE_CODE]
            elif choice == '4':
                return [AnalysisType.ALL]
            elif choice == '5':
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter 1-5.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

def main():
    """Main function with interactive menu"""
    parser = argparse.ArgumentParser(description="Advanced Dead Code and Duplicate Code Analyzer")
    parser.add_argument('--dead-code', action='store_true', help='Analyze dead code')
    parser.add_argument('--dead-libraries', action='store_true', help='Analyze dead libraries')
    parser.add_argument('--duplicate-code', action='store_true', help='Analyze duplicate code')
    parser.add_argument('--all', action='store_true', help='Run all analyses')
    parser.add_argument('--interactive', action='store_true', help='Use interactive menu')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--output-file', help='Output file path')
    
    args = parser.parse_args()
    
    # Determine analysis types
    analysis_types = []
    
    if args.interactive:
        analysis_types = interactive_menu()
    elif args.all:
        analysis_types = [AnalysisType.ALL]
    else:
        if args.dead_code:
            analysis_types.append(AnalysisType.DEAD_CODE)
        if args.dead_libraries:
            analysis_types.append(AnalysisType.DEAD_LIBRARIES)
        if args.duplicate_code:
            analysis_types.append(AnalysisType.DUPLICATE_CODE)
        
        # Default to all if none specified
        if not analysis_types:
            analysis_types = [AnalysisType.ALL]
    
    # Initialize analyzer
    analyzer = AdvancedDeadCodeAnalyzer(PROJECT_ROOT)
    
    # Run analysis
    results = analyzer.run_analysis(analysis_types)
    
    # Output results
    if args.output_format == 'json':
        output = json.dumps(results, indent=2)
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
