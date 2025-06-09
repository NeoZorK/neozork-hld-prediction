#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple Dependency Analyzer

A lightweight tool to analyze Python project dependencies without recursion issues.
This script scans Python files for import statements and compares them with
the dependencies listed in requirements.txt or pyproject.toml.

Author: GitHub Copilot
Date: June 9, 2025
"""

import os
import re
import sys
import shutil
import subprocess
import importlib.util
from pathlib import Path
from collections import defaultdict


def get_module_from_import(import_statement):
    """Extract module name from import statement."""
    # Handle 'import x' or 'import x as y'
    if import_statement.startswith('import '):
        # Remove 'import ' prefix
        line = import_statement[7:].strip()
        # Handle multiple imports on one line (import x, y, z)
        modules = []
        for part in line.split(','):
            # Remove 'as y' if present
            if ' as ' in part:
                part = part.split(' as ')[0]
            # Get top-level module
            modules.append(part.strip().split('.')[0])
        return modules

    # Handle 'from x import y'
    elif import_statement.startswith('from '):
        # Extract module name after 'from ' and before ' import'
        match = re.match(r'from\s+([\w\.]+)\s+import', import_statement)
        if match:
            # Get top-level module
            return [match.group(1).split('.')[0]]

    return []


def scan_file_for_imports(file_path):
    """Scan a Python file for import statements without using AST."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                # Look for import statements
                if line.startswith('import ') or line.startswith('from '):
                    # Handle multi-line imports
                    if '(' in line and ')' not in line:
                        multi_line = line
                        for next_line in f:
                            multi_line += next_line.strip()
                            if ')' in next_line:
                                break
                        line = multi_line

                    # Extract module names
                    modules = get_module_from_import(line)
                    imports.update(modules)
    except Exception as e:
        print(f"Error scanning {file_path}: {e}")

    return imports


def scan_project(project_path, max_depth=10):
    """Scan a project directory for imports with depth limit."""
    all_imports = set()
    file_count = 0

    for root, dirs, files in os.walk(project_path):
        # Calculate current depth from project root
        rel_path = os.path.relpath(root, project_path)
        current_depth = len(rel_path.split(os.sep)) if rel_path != '.' else 0

        # Skip if max depth reached
        if current_depth > max_depth:
            print(f"Skipping {root} (max depth reached)")
            continue

        # Skip virtual environments, __pycache__ and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and
                  d != '__pycache__' and d != '.venv' and d != 'venv']

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = scan_file_for_imports(file_path)
                all_imports.update(imports)
                file_count += 1

    return all_imports, file_count


def parse_requirements_txt(file_path):
    """Parse requirements.txt file."""
    packages = set()
    raw_requirements = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                original_line = line.strip()
                raw_requirements.append(original_line)

                if not original_line or original_line.startswith('#'):
                    continue

                # Handle various formats
                if original_line.startswith('-e') or original_line.startswith('git+'):
                    continue

                # Extract package name (before version specifiers)
                package = re.split(r'[=<>~\[\]]', original_line)[0].strip().lower()
                if package:
                    packages.add(package)
    except Exception as e:
        print(f"Error parsing requirements.txt: {e}")

    return packages, raw_requirements


def parse_pyproject_toml(file_path):
    """Parse dependencies from pyproject.toml file using regex instead of TOML parser."""
    packages = set()
    raw_content = ""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()

        # Find dependencies section using regex
        dependencies_match = re.search(r'dependencies\s*=\s*\[(.*?)\]', raw_content, re.DOTALL)
        if dependencies_match:
            deps_text = dependencies_match.group(1)
            # Extract package names from quoted strings
            for match in re.finditer(r'[\"\']([^\'\"]+?)[\"\']', deps_text):
                dep_line = match.group(1)
                # Extract package name (before version specifiers)
                package = re.split(r'[=<>~\[\]]', dep_line)[0].strip().lower()
                if package:
                    packages.add(package)
    except Exception as e:
        print(f"Error parsing pyproject.toml: {e}")

    return packages, raw_content


def get_known_aliases():
    """Return dictionary of known package aliases."""
    return {
        'bs4': 'beautifulsoup4',
        'yaml': 'pyyaml',
        'PIL': 'pillow',
        'sklearn': 'scikit-learn',
        'dotenv': 'python-dotenv',
        'cv2': 'opencv-python',
        'matplotlib.pyplot': 'matplotlib',
        'matplotlib': 'matplotlib',
        'np': 'numpy',
        'pd': 'pandas',
    }


def get_standard_library_modules():
    """Get a set of standard library module names."""
    std_lib = set()

    # Add builtin module names
    std_lib.update(sys.builtin_module_names)

    # Add modules from standard library paths
    for path in sys.path:
        if path.endswith(('site-packages', 'dist-packages')):
            continue  # Skip installed packages

        if os.path.isdir(path):
            for name in os.listdir(path):
                # Skip hidden files and directories
                if name.startswith('.'):
                    continue

                # Add modules and packages
                if name.endswith('.py'):
                    std_lib.add(name[:-3])
                elif os.path.isdir(os.path.join(path, name)) and not name.startswith('_'):
                    std_lib.add(name)

    # Add common standard library modules manually
    common_std_lib = {
        'os', 'sys', 're', 'math', 'json', 'datetime', 'time', 'random',
        'collections', 'functools', 'itertools', 'pathlib', 'typing',
        'io', 'csv', 'uuid', 'copy', 'string', 'logging', 'tempfile',
        'urllib', 'socket', 'traceback', 'argparse', 'shutil', 'pickle',
        'inspect', 'ast', 'sqlite3', 'base64', 'hashlib', 'signal', 'select',
    }
    std_lib.update(common_std_lib)

    return std_lib


def uninstall_unused_packages(unused_packages):
    """Uninstall unused packages using pip or uv."""
    if not unused_packages:
        print("No unused packages to uninstall.")
        return True

    print(f"\nUninstalling {len(unused_packages)} unused packages...")

    # Check if uv is available
    use_uv = False
    try:
        subprocess.run(['uv', '--version'], capture_output=True, text=True)
        use_uv = True
        print("Using 'uv' for package management")
    except FileNotFoundError:
        print("Using 'pip' for package management (uv not found)")

    success = True
    for package in unused_packages:
        try:
            if use_uv:
                # For uv, need to use the correct syntax (without --yes flag)
                cmd = ['uv', 'pip', 'uninstall', package]
                # Make the command interactive and automatically answer 'y' to the prompt
                print(f"Uninstalling {package}...")
                result = subprocess.run(cmd, input=b'y\n', text=True)
            else:
                cmd = ['pip', 'uninstall', '-y', package]
                print(f"Uninstalling {package}...")
                result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"  Error uninstalling {package}")
                success = False
            else:
                print(f"  Successfully uninstalled {package}")
        except Exception as e:
            print(f"  Error uninstalling {package}: {str(e)}")
            success = False

    return success


def update_requirements_txt(file_path, used_packages, raw_requirements):
    """Update requirements.txt to only include used packages."""
    if not file_path or not os.path.exists(file_path):
        print("requirements.txt not found, skipping update.")
        return False

    # Create backup
    backup_path = file_path + '.bak'
    shutil.copy2(file_path, backup_path)
    print(f"Created backup of requirements.txt at {backup_path}")

    # Convert used packages to lowercase for case-insensitive comparison
    used_packages_lower = {pkg.lower() for pkg in used_packages}

    # Filter out lines for unused packages
    new_requirements = []
    for line in raw_requirements:
        line = line.strip()
        if not line or line.startswith('#'):
            new_requirements.append(line)
            continue

        if line.startswith('-e') or line.startswith('git+'):
            new_requirements.append(line)
            continue

        # Extract package name
        package = re.split(r'[=<>~\[\]]', line)[0].strip().lower()
        if not package or package in used_packages_lower:
            new_requirements.append(line)

    # Write updated requirements.txt
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in new_requirements:
                f.write(line + '\n')
        print(f"Updated {file_path} with only used packages")
        return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        print(f"Restoring from backup...")
        shutil.copy2(backup_path, file_path)
        return False


def update_pyproject_toml(file_path, used_packages, raw_content):
    """Update pyproject.toml to only include used packages."""
    if not file_path or not os.path.exists(file_path):
        print("pyproject.toml not found, skipping update.")
        return False

    # Create backup
    backup_path = file_path + '.bak'
    shutil.copy2(file_path, backup_path)
    print(f"Created backup of pyproject.toml at {backup_path}")

    # Convert used packages to lowercase for case-insensitive comparison
    used_packages_lower = {pkg.lower() for pkg in used_packages}

    # Find the dependencies section
    deps_pattern = r'(dependencies\s*=\s*\[)(.*?)(\])'
    deps_match = re.search(deps_pattern, raw_content, re.DOTALL)

    if not deps_match:
        print("Could not find dependencies section in pyproject.toml")
        return False

    # Extract dependency lines
    deps_start = deps_match.group(1)
    deps_content = deps_match.group(2)
    deps_end = deps_match.group(3)

    # Process each dependency line
    dep_lines = []
    section_header = None

    for line in deps_content.split('\n'):
        line = line.strip()
        if not line:
            dep_lines.append(line)  # Keep empty lines
            continue

        # Keep comments and section headers
        if line.startswith('#'):
            section_header = line
            continue

        # Extract package name from the line
        match = re.search(r'[\"\']([^\'\"]+?)[\"\']', line)
        if not match:
            continue  # Skip if no package name found

        dep_spec = match.group(1)
        package = re.split(r'[=<>~\[\]]', dep_spec)[0].strip().lower()

        # Keep the dependency if it's used
        if package in used_packages_lower:
            # Add section header if it exists and wasn't added yet
            if section_header and section_header not in dep_lines:
                dep_lines.append(section_header)
                section_header = None
            dep_lines.append(line)

    # Build the new dependencies section
    new_deps_content = '\n'.join(dep_lines)
    new_content = raw_content.replace(deps_match.group(0), f"{deps_start}{new_deps_content}{deps_end}")

    # Write updated pyproject.toml
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path} with only used packages")
        return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        print(f"Restoring from backup...")
        shutil.copy2(backup_path, file_path)
        return False


def analyze_dependencies(project_path, requirements_path=None, pyproject_path=None, max_depth=10):
    """Analyze which dependencies are used and which are not."""
    print(f"Analyzing dependencies in {project_path}")
    print(f"Maximum directory depth: {max_depth}")

    # Get standard library modules
    std_lib = get_standard_library_modules()
    print(f"Identified {len(std_lib)} standard library modules")

    # Get known package aliases
    aliases = get_known_aliases()

    # Load declared dependencies
    declared_packages = set()
    raw_requirements = []
    raw_pyproject = ""

    if requirements_path and os.path.exists(requirements_path):
        req_packages, raw_requirements = parse_requirements_txt(requirements_path)
        declared_packages.update(req_packages)
        print(f"Found {len(req_packages)} packages in {requirements_path}")

    if pyproject_path and os.path.exists(pyproject_path):
        pyproject_packages, raw_pyproject = parse_pyproject_toml(pyproject_path)
        declared_packages.update(pyproject_packages)
        print(f"Found {len(pyproject_packages)} packages in {pyproject_path}")

    if not declared_packages:
        print("No dependencies found in the specified files.")
        return None

    # Scan project for imports
    print(f"Scanning Python files in {project_path}...")
    imports, file_count = scan_project(project_path, max_depth)
    print(f"Scanned {file_count} Python files and found {len(imports)} unique imports")

    # Filter out standard library imports
    non_std_imports = set()
    for imp in imports:
        if imp not in std_lib:
            non_std_imports.add(imp)

    print(f"After filtering standard library: {len(non_std_imports)} imports")

    # Map imports to package names
    used_packages = set()
    unmapped_imports = set()

    for imp in non_std_imports:
        # Check if the import name matches a package directly
        if imp.lower() in declared_packages:
            used_packages.add(imp.lower())
        # Check if the import has a known alias
        elif imp in aliases and aliases[imp].lower() in declared_packages:
            used_packages.add(aliases[imp].lower())
        else:
            unmapped_imports.add(imp)

    unused_packages = declared_packages - used_packages

    # Display results
    print("\n=== RESULTS ===")

    print("\nUsed packages:")
    for pkg in sorted(used_packages):
        print(f"  ✓ {pkg}")

    print("\nUnused packages:")
    for pkg in sorted(unused_packages):
        print(f"  ✗ {pkg}")

    print("\nImports not mapped to declared packages:")
    for imp in sorted(unmapped_imports):
        if imp in aliases:
            print(f"  ? {imp} (alias for {aliases[imp]})")
        else:
            print(f"  ? {imp}")

    # Summary
    print("\n=== SUMMARY ===")
    print(f"Total declared packages: {len(declared_packages)}")
    print(f"Used packages: {len(used_packages)} ({len(used_packages)/len(declared_packages)*100:.1f}%)")
    print(f"Unused packages: {len(unused_packages)} ({len(unused_packages)/len(declared_packages)*100:.1f}%)")
    print(f"Unmapped imports: {len(unmapped_imports)}")

    # Ask user if they want to uninstall unused packages and update files
    if unused_packages:
        print("\nWould you like to uninstall unused packages and update dependency files? (y/n)")
        response = input().strip().lower()

        if response == 'y' or response == 'yes':
            # Uninstall unused packages
            success = uninstall_unused_packages(unused_packages)

            if success:
                # Update requirements.txt
                if requirements_path and os.path.exists(requirements_path):
                    update_requirements_txt(requirements_path, used_packages, raw_requirements)

                # Update pyproject.toml
                if pyproject_path and os.path.exists(pyproject_path):
                    update_pyproject_toml(pyproject_path, used_packages, raw_pyproject)

            print("\nDependency cleanup completed!")

    return {
        'used_packages': sorted(used_packages),
        'unused_packages': sorted(unused_packages),
        'unmapped_imports': sorted(unmapped_imports)
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python simple_dep_analyzer.py <project_directory> [--requirements=path] [--pyproject=path] [--max-depth=10]")
        sys.exit(1)

    project_path = sys.argv[1]
    requirements_path = None
    pyproject_path = None
    max_depth = 10

    # Parse command line arguments
    for arg in sys.argv[2:]:
        if arg.startswith('--requirements='):
            requirements_path = arg.split('=', 1)[1]
        elif arg.startswith('--pyproject='):
            pyproject_path = arg.split('=', 1)[1]
        elif arg.startswith('--max-depth='):
            try:
                max_depth = int(arg.split('=', 1)[1])
            except ValueError:
                print(f"Invalid value for max-depth: {arg}")
                sys.exit(1)

    # If no specific files provided, look for them in the project directory
    if not requirements_path and not pyproject_path:
        default_requirements = os.path.join(project_path, 'requirements.txt')
        default_pyproject = os.path.join(project_path, 'pyproject.toml')

        if os.path.exists(default_requirements):
            requirements_path = default_requirements

        if os.path.exists(default_pyproject):
            pyproject_path = default_pyproject

    analyze_dependencies(project_path, requirements_path, pyproject_path, max_depth)
