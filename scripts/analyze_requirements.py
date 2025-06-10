#!/usr/bin/env python3
"""
Requirements Analyzer

This script analyzes Python imports across the project and compares them
with the requirements.txt file to identify unused dependencies.
Uses grep for efficient import detection and tqdm for progress tracking.
"""

import os
import sys
import re
import ast
import shutil
import datetime
import subprocess
from pathlib import Path
from collections import defaultdict, Counter
try:
    from tqdm import tqdm
except ImportError:
    # We'll handle this in main()
    pass

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"

# Standard library modules
STDLIB_MODULES = {
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

# Mapping of package names to import names and vice versa
PACKAGE_TO_IMPORT = {
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
    # Add common mappings for trading APIs
    'python-binance': 'binance',
    'polygon-api-client': 'polygon'
}

# Reverse mapping for import to package name
IMPORT_TO_PACKAGE = {v: k for k, v in PACKAGE_TO_IMPORT.items()}

# Well-known third-party libraries that might be installed differently
WELL_KNOWN_LIBRARIES = {
    'binance': 'python-binance',
    'polygon': 'polygon-api-client'
}


def find_python_files(start_dir):
    """
    Find all Python files in the project.

    Args:
        start_dir (str or Path): The directory to start searching from

    Returns:
        list: List of paths to Python files
    """
    python_files = []
    for root, _, files in os.walk(start_dir):
        # Skip virtual environments, hidden directories, and __pycache__
        if any(part.startswith('.') or part == '__pycache__' or part == 'venv' or part == 'env'
               for part in Path(root).parts):
            continue

        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    return python_files


def extract_imports_using_grep():
    """
    Extract all import statements from Python files using grep command.

    Returns:
        tuple: (file_imports, all_imports) where:
            - file_imports is a defaultdict mapping filenames to sets of imports
            - all_imports is a set of all unique imports
    """
    # Use grep to find all import statements
    try:
        print("Searching for imports using grep...")
        grep_command = ["grep", "-r", "--include=*.py", "-E", "^(import|from) ", str(PROJECT_ROOT)]
        grep_output = subprocess.check_output(grep_command, text=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:  # grep returns 1 if no matches found
            print("No import statements found in the project.")
            return defaultdict(set), set()
        else:
            print(f"Error running grep command: {e}")
            return defaultdict(set), set()

    # Process grep output
    lines = grep_output.splitlines()
    file_imports = defaultdict(set)
    all_imports = set()

    print(f"Processing {len(lines)} import statements...")

    # Get tqdm from global scope to avoid issues if it was just installed
    progress_func = globals().get('tqdm', lambda x, **kwargs: x)

    for line in progress_func(lines, desc="Processing imports", unit="imports"):
        # Extract filename and import statement
        parts = line.split(':', 1)
        if len(parts) < 2:
            continue

        filename, import_statement = parts

        # Parse the import statement
        import_statement = import_statement.strip()

        # Handle "import X" or "import X as Y" or "import X, Y, Z"
        if import_statement.startswith('import '):
            import_parts = import_statement[7:].split(',')
            for part in import_parts:
                part = part.strip()
                if ' as ' in part:
                    module = part.split(' as ')[0].strip()
                else:
                    module = part

                # Get the top-level package
                if module:  # Make sure module isn't empty
                    top_package = module.split('.')[0]
                    file_imports[filename].add(top_package)
                    all_imports.add(top_package)

        # Handle "from X import Y" or "from X.Z import Y"
        elif import_statement.startswith('from '):
            # Extract the module being imported from
            match = re.match(r'from\s+(\S+)\s+import', import_statement)
            if match:
                module = match.group(1)
                # Get the top-level package
                top_package = module.split('.')[0]
                file_imports[filename].add(top_package)
                all_imports.add(top_package)

    return file_imports, all_imports


def extract_imports_from_file(file_path):
    """
    Extract all import statements from a Python file using ast module.

    Args:
        file_path (str or Path): Path to the Python file

    Returns:
        set: Set of imported module names
    """
    imports = set()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            # Handle regular imports: import X, import X.Y
            if isinstance(node, ast.Import):
                for name in node.names:
                    # Get the top-level package
                    top_package = name.name.split('.')[0]
                    imports.add(top_package)

            # Handle from imports: from X import Y, from X.Y import Z
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Get the top-level package
                    top_package = node.module.split('.')[0]
                    imports.add(top_package)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

    return imports


def parse_requirements_txt(req_path):
    """
    Parse requirements.txt and extract package names.

    Args:
        req_path (str or Path): Path to requirements.txt file

    Returns:
        dict: Dictionary mapping package names to their requirement lines
    """
    requirements = {}

    with open(req_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#') or line.startswith('//'):
                continue

            # Remove inline comments
            if '#' in line:
                line = line.split('#', 1)[0].strip()

            # Process the requirement line
            if line:
                # Extract package name (remove version specifiers)
                match = re.match(r'^([a-zA-Z0-9_\-]+)', line)
                if match:
                    package_name = match.group(1).lower()
                    requirements[package_name] = line

    return requirements


def map_package_to_import(package_name):
    """
    Map package names to their corresponding import names.
    Some packages have different names when imported.

    Args:
        package_name (str): The package name to map

    Returns:
        str: The corresponding import name
    """
    return PACKAGE_TO_IMPORT.get(package_name.lower(), package_name.lower())


def map_import_to_package(import_name):
    """
    Map import names back to their package names.

    Args:
        import_name (str): The import name to map

    Returns:
        str: The corresponding package name
    """
    return IMPORT_TO_PACKAGE.get(import_name.lower(), import_name.lower())


def analyze_project_imports():
    """
    Analyze all Python files in the project and collect imports.

    Returns:
        tuple: (third_party_imports, import_counts, total_files) where:
            - third_party_imports is a set of third-party imports
            - import_counts is a Counter mapping imports to their occurrence counts
            - total_files is the number of files analyzed
    """
    # Use grep-based approach for finding imports
    file_imports, all_imports = extract_imports_using_grep()

    # If grep fails or finds nothing, fall back to Python-based parsing
    if not all_imports:
        print("Falling back to Python-based import analysis...")
        python_files = find_python_files(PROJECT_ROOT)

        if not python_files:
            print("No Python files found in the project.")
            return set(), Counter(), 0

        file_imports = defaultdict(set)
        all_imports = set()

        # Get tqdm from global scope to avoid issues if it was just installed
        progress_func = globals().get('tqdm', lambda x, **kwargs: x)

        for py_file in progress_func(python_files, desc="Analyzing files", unit="files"):
            imports = extract_imports_from_file(py_file)
            file_imports[py_file] = imports
            all_imports.update(imports)

    # Filter out standard library modules
    std_lib_modules = set(sys.builtin_module_names)
    std_lib_modules.update(STDLIB_MODULES)

    # Try to use stdlib_list if available, otherwise continue with our predefined set
    stdlib_list_modules = set()
    try:
        # Import in try block to avoid issues if it's not installed
        import stdlib_list
        stdlib_list_modules = set(stdlib_list.stdlib_list("3.11"))
    except ImportError:
        # If stdlib_list is not available, we're already using our predefined set
        pass

    # Add any modules from stdlib_list to our standard library set
    std_lib_modules.update(stdlib_list_modules)

    third_party_imports = all_imports - std_lib_modules

    # Count occurrences in files for each import
    import_counts = Counter()
    for file_path, imports in file_imports.items():
        for imp in imports:
            if imp in third_party_imports:
                import_counts[imp] += 1

    return third_party_imports, import_counts, len(file_imports)


def display_results(third_party_imports, import_counts, total_files, requirements,
                   used_requirements, unused_requirements, missing_requirements):
    """
    Display the analysis results in a structured format.

    Args:
        third_party_imports (set): Set of third-party imports found
        import_counts (Counter): Counter mapping imports to their occurrence counts
        total_files (int): Number of files analyzed
        requirements (dict): Dictionary mapping package names to their requirement lines
        used_requirements (set): Set of used requirement packages
        unused_requirements (set): Set of unused requirement packages
        missing_requirements (set): Set of imports not in requirements
    """
    print("\n=== Analysis Results ===")
    print(f"\nTotal Python files analyzed: {total_files}")
    print(f"Total third-party imports found: {len(third_party_imports)}")
    print(f"Total packages in requirements.txt: {len(requirements)}")

    print(f"\n✅ Used packages ({len(used_requirements)}):")
    for pkg in sorted(used_requirements):
        import_name = map_package_to_import(pkg)
        count = import_counts.get(import_name, 0)
        print(f"  - {pkg} (used in {count} files)")

    print(f"\n❌ Unused packages ({len(unused_requirements)}):")
    for pkg in sorted(unused_requirements):
        print(f"  - {pkg}")

    if missing_requirements:
        print(f"\n⚠️ Imports without requirements ({len(missing_requirements)}):")
        print("   These are imports found in your code that aren't in requirements.txt")

        # Group by importance
        trading_apis = []
        other_missing = []

        for pkg in sorted(missing_requirements):
            import_name = map_import_to_package(pkg)
            count = import_counts.get(pkg, 0)
            package_info = f"  - {pkg}"
            if pkg in WELL_KNOWN_LIBRARIES:
                suggested_pkg = WELL_KNOWN_LIBRARIES[pkg]
                package_info += f" (install as: {suggested_pkg}, used in {count} files)"
                trading_apis.append((pkg, package_info))
            else:
                package_info += f" (used in {count} files)"
                other_missing.append((pkg, package_info))

        # Show trading APIs first as they're specifically mentioned by the user
        if trading_apis:
            print("\n   Trading APIs:")
            for _, info in trading_apis:
                print(info)

        if other_missing:
            if trading_apis:
                print("\n   Other missing packages:")
            for _, info in other_missing:
                print(info)

        print("\n   To add these to requirements.txt, use:")
        for pkg, _ in trading_apis:
            suggested_pkg = WELL_KNOWN_LIBRARIES[pkg]
            print(f"   pip install {suggested_pkg}")

        if other_missing:
            other_pkgs = [pkg for pkg, _ in other_missing]
            if len(other_pkgs) <= 5:
                for pkg in other_pkgs:
                    print(f"   pip install {pkg}")
            else:
                print(f"   pip install {' '.join(other_pkgs[:5])} ...")
