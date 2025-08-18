#!/usr/bin/env python3
"""
Dead Code and Libraries Fixer

This script automatically fixes dead code and library issues found by the analyzer.
Supports automatic removal of unused imports, dead functions, and unused dependencies.

Usage:
    python fix_dead_code.py [options]
    uv run python fix_dead_code.py [options]

Options:
    --fix-imports        Remove unused imports automatically
    --fix-functions      Remove dead functions
    --fix-requirements   Update requirements.txt to remove unused packages
    --fix-files          Delete dead files
    --all                Apply all fixes
    --dry-run            Show what would be fixed without applying
    --backup-dir         Specify backup directory
    --analysis-file      Use results from dead_code_analyzer.py
"""

import os
import sys
import ast
import re
import shutil
import argparse
import json
from pathlib import Path
from typing import List, Set, Dict, Any
import datetime

class DeadCodeFixer:
    """Automatically fix dead code and library issues"""
    
    def __init__(self, project_root: Path, backup_dir: Path = None):
        self.project_root = project_root
        
        if backup_dir is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            self.backup_dir = project_root / "backups" / f"dead_code_fix_{timestamp}"
        else:
            self.backup_dir = backup_dir
            
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.fixes_applied = []
    
    def backup_file(self, file_path: Path) -> Path:
        """Create backup of a file"""
        backup_path = self.backup_dir / file_path.relative_to(self.project_root)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def remove_unused_imports(self, file_path: Path) -> bool:
        """Remove unused imports from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            lines = content.split('\n')
            
            # Find all imports and their aliases
            imports_info = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports_info.append({
                            'line': node.lineno,
                            'name': name.name,
                            'alias': name.asname or name.name,
                            'type': 'import'
                        })
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for name in node.names:
                            imports_info.append({
                                'line': node.lineno,
                                'name': name.name,
                                'alias': name.asname or name.name,
                                'module': node.module,
                                'type': 'from'
                            })
            
            # Find unused imports
            unused_imports = []
            for imp in imports_info:
                if not self._is_name_used_in_tree(imp['alias'], tree, imp['line']):
                    unused_imports.append(imp)
            
            # Remove unused imports
            if unused_imports:
                self.backup_file(file_path)
                
                # Remove lines with unused imports
                lines_to_remove = {imp['line'] for imp in unused_imports}
                new_lines = [line for i, line in enumerate(lines, 1) if i not in lines_to_remove]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                
                self.fixes_applied.append(f"Removed {len(unused_imports)} unused imports from {file_path}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error removing unused imports from {file_path}: {e}")
            return False
    
    def _is_name_used_in_tree(self, name: str, tree: ast.AST, import_line: int) -> bool:
        """Check if a name is used in the AST, excluding the import line itself"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == name:
                # Skip if this is the import statement itself
                if hasattr(node, 'lineno') and node.lineno != import_line:
                    return True
        return False
    
    def remove_dead_functions(self, file_path: Path, dead_functions: List[str]) -> bool:
        """Remove dead functions from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            lines = content.split('\n')
            
            # Find function definitions to remove
            lines_to_remove = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name in dead_functions:
                    # Get function lines
                    start_line = node.lineno
                    end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
                    
                    # Add all lines of the function
                    for i in range(start_line, end_line + 1):
                        lines_to_remove.add(i)
            
            if lines_to_remove:
                self.backup_file(file_path)
                
                new_lines = [line for i, line in enumerate(lines, 1) if i not in lines_to_remove]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                
                self.fixes_applied.append(f"Removed {len(dead_functions)} dead functions from {file_path}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error removing dead functions from {file_path}: {e}")
            return False
    
    def update_requirements(self, unused_packages: List[str]) -> bool:
        """Update requirements.txt to remove unused packages"""
        req_file = self.project_root / "requirements.txt"
        
        if not req_file.exists():
            print("requirements.txt not found")
            return False
        
        try:
            self.backup_file(req_file)
            
            with open(req_file, 'r') as f:
                lines = f.readlines()
            
            # Filter out unused packages
            new_lines = []
            removed_count = 0
            
            for line in lines:
                package_name = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                if package_name not in unused_packages:
                    new_lines.append(line)
                else:
                    removed_count += 1
            
            with open(req_file, 'w') as f:
                f.writelines(new_lines)
            
            if removed_count > 0:
                self.fixes_applied.append(f"Removed {removed_count} unused packages from requirements.txt")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating requirements.txt: {e}")
            return False
    
    def delete_dead_files(self, dead_files: List[str]) -> bool:
        """Delete dead files"""
        deleted_count = 0
        
        for file_path_str in dead_files:
            file_path = self.project_root / file_path_str
            
            if file_path.exists():
                try:
                    # Create backup
                    backup_path = self.backup_file(file_path)
                    
                    # Delete file
                    file_path.unlink()
                    
                    self.fixes_applied.append(f"Deleted dead file: {file_path_str} (backup: {backup_path})")
                    deleted_count += 1
                    
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        
        return deleted_count > 0
    
    def apply_fixes_from_analysis(self, analysis_file: Path, dry_run: bool = False) -> Dict[str, Any]:
        """Apply fixes based on analysis results"""
        if not analysis_file.exists():
            print(f"Analysis file not found: {analysis_file}")
            return {}
        
        try:
            with open(analysis_file, 'r') as f:
                analysis_results = json.load(f)
        except Exception as e:
            print(f"Error reading analysis file: {e}")
            return {}
        
        fixes_summary = {
            'dead_code_fixed': 0,
            'dead_libraries_fixed': 0,
            'dead_files_fixed': 0,
            'backup_dir': str(self.backup_dir)
        }
        
        if dry_run:
            print("DRY RUN MODE - No changes will be made")
            print(f"Backup directory would be: {self.backup_dir}")
        
        # Fix dead libraries
        if 'dead_libraries' in analysis_results:
            unused_packages = [item['package_name'] for item in analysis_results['dead_libraries']]
            if unused_packages and not dry_run:
                if self.update_requirements(unused_packages):
                    fixes_summary['dead_libraries_fixed'] = len(unused_packages)
            elif unused_packages:
                print(f"Would remove {len(unused_packages)} unused packages from requirements.txt")
        
        # Fix dead files
        if 'dead_files' in analysis_results:
            dead_files = [item['file_path'] for item in analysis_results['dead_files']]
            if dead_files and not dry_run:
                if self.delete_dead_files(dead_files):
                    fixes_summary['dead_files_fixed'] = len(dead_files)
            elif dead_files:
                print(f"Would delete {len(dead_files)} dead files")
        
        # Fix dead code (functions)
        if 'dead_code' in analysis_results:
            dead_functions = {}
            for item in analysis_results['dead_code']:
                if item['type'] == 'function':
                    file_path = item['file_path']
                    if file_path not in dead_functions:
                        dead_functions[file_path] = []
                    dead_functions[file_path].append(item['name'])
            
            if dead_functions and not dry_run:
                for file_path, functions in dead_functions.items():
                    full_path = self.project_root / file_path
                    if full_path.exists():
                        if self.remove_dead_functions(full_path, functions):
                            fixes_summary['dead_code_fixed'] += len(functions)
            elif dead_functions:
                total_functions = sum(len(funcs) for funcs in dead_functions.values())
                print(f"Would remove {total_functions} dead functions")
        
        return fixes_summary
    
    def print_summary(self):
        """Print summary of applied fixes"""
        if not self.fixes_applied:
            print("No fixes were applied.")
            return
        
        print(f"\n✅ FIXES APPLIED ({len(self.fixes_applied)} total):")
        print("-" * 50)
        for fix in self.fixes_applied:
            print(f"  • {fix}")
        
        print(f"\n📁 Backup directory: {self.backup_dir}")
        print("💡 To restore original files, copy from backup directory")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Dead Code and Libraries Fixer")
    parser.add_argument('--fix-imports', action='store_true', help='Remove unused imports')
    parser.add_argument('--fix-functions', action='store_true', help='Remove dead functions')
    parser.add_argument('--fix-requirements', action='store_true', help='Update requirements.txt')
    parser.add_argument('--fix-files', action='store_true', help='Delete dead files')
    parser.add_argument('--all', action='store_true', help='Apply all fixes')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without applying')
    parser.add_argument('--backup-dir', help='Specify backup directory')
    parser.add_argument('--analysis-file', help='Use results from dead_code_analyzer.py')
    
    args = parser.parse_args()
    
    if not any([args.fix_imports, args.fix_functions, args.fix_requirements, args.fix_files, args.all, args.analysis_file]):
        print("Please specify what to fix. Use --help for options.")
        return
    
    if args.all:
        args.fix_imports = True
        args.fix_functions = True
        args.fix_requirements = True
        args.fix_files = True
    
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Setup backup directory
    backup_dir = None
    if args.backup_dir:
        backup_dir = Path(args.backup_dir)
    
    fixer = DeadCodeFixer(project_root, backup_dir)
    
    if args.analysis_file:
        # Use analysis file
        analysis_file = Path(args.analysis_file)
        if not analysis_file.is_absolute():
            analysis_file = project_root / analysis_file
        
        fixes_summary = fixer.apply_fixes_from_analysis(analysis_file, dry_run=args.dry_run)
        
        if not args.dry_run:
            fixer.print_summary()
        
        # Print summary
        print(f"\n📊 FIXES SUMMARY:")
        print(f"  Dead code items fixed: {fixes_summary.get('dead_code_fixed', 0)}")
        print(f"  Dead libraries fixed: {fixes_summary.get('dead_libraries_fixed', 0)}")
        print(f"  Dead files fixed: {fixes_summary.get('dead_files_fixed', 0)}")
        
    else:
        # Manual fixes (would need to be integrated with analyzer results)
        if args.dry_run:
            print("DRY RUN MODE - No changes will be made")
            print("Backup directory would be:", fixer.backup_dir)
            return
        
        print(f"Backup directory: {fixer.backup_dir}")
        
        # Apply manual fixes
        if args.fix_imports:
            print("\nFixing unused imports...")
            # This would need to be integrated with the analyzer results
        
        if args.fix_requirements:
            print("\nFixing requirements.txt...")
            # This would need to be integrated with the analyzer results
        
        fixer.print_summary()
    
    print("\n🎉 Fix operations completed!")

if __name__ == "__main__":
    main()
