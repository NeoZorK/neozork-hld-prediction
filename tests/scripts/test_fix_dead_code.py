#!/usr/bin/env python3
"""
Tests for dead code fixer functionality.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "analysis" / "dead-code"))

from fix_dead_code import DeadCodeFixer


class TestDeadCodeFixer:
    """Test cases for DeadCodeFixer class."""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project structure for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            
            # Create project structure
            src_dir = project_root / "src"
            src_dir.mkdir()
            
            # Create test files
            (src_dir / "main.py").write_text("""
import pandas as pd
import numpy as np
import unused_module

def used_function():
    return pd.DataFrame()

def unused_function():
    return "unused"

if __name__ == "__main__":
    used_function()
""")
            
            # Create requirements.txt
            (project_root / "requirements.txt").write_text("""
pandas==2.2.3
numpy==2.2.4
unused-package==1.0.0
""")
            
            yield project_root
    
    def test_init(self, temp_project):
        """Test fixer initialization."""
        fixer = DeadCodeFixer(temp_project)
        
        assert fixer.project_root == temp_project
        assert fixer.backup_dir.exists()
        assert "dead_code_fix_" in str(fixer.backup_dir)
        assert len(fixer.fixes_applied) == 0
    
    def test_init_with_custom_backup_dir(self, temp_project):
        """Test fixer initialization with custom backup directory."""
        custom_backup = temp_project / "custom_backup"
        fixer = DeadCodeFixer(temp_project, custom_backup)
        
        assert fixer.backup_dir == custom_backup
        assert fixer.backup_dir.exists()
    
    def test_backup_file(self, temp_project):
        """Test file backup functionality."""
        fixer = DeadCodeFixer(temp_project)
        test_file = temp_project / "src" / "main.py"
        
        backup_path = fixer.backup_file(test_file)
        
        assert backup_path.exists()
        assert backup_path != test_file
        assert backup_path.read_text() == test_file.read_text()
    
    def test_remove_unused_imports(self, temp_project):
        """Test removing unused imports."""
        fixer = DeadCodeFixer(temp_project)
        test_file = temp_project / "src" / "main.py"
        
        # Create a file with unused imports
        test_file.write_text("""
import pandas as pd
import numpy as np
import unused_module

def test_function():
    return pd.DataFrame()
""")
        
        result = fixer.remove_unused_imports(test_file)
        
        assert result == True
        assert len(fixer.fixes_applied) == 1
        assert "unused imports" in fixer.fixes_applied[0]
        
        # Check that unused import was removed
        content = test_file.read_text()
        assert "import unused_module" not in content
        assert "import pandas as pd" in content  # Should remain
    
    def test_remove_unused_imports_no_unused(self, temp_project):
        """Test removing unused imports when none exist."""
        fixer = DeadCodeFixer(temp_project)
        test_file = temp_project / "src" / "main.py"
        
        # Create a file with only used imports
        test_file.write_text("""
import pandas as pd

def test_function():
    return pd.DataFrame()
""")
        
        result = fixer.remove_unused_imports(test_file)
        
        assert result == False
        assert len(fixer.fixes_applied) == 0
    
    def test_remove_dead_functions(self, temp_project):
        """Test removing dead functions."""
        fixer = DeadCodeFixer(temp_project)
        test_file = temp_project / "src" / "main.py"
        
        # Create a file with dead functions
        test_file.write_text("""
def used_function():
    return "used"

def unused_function():
    return "unused"

def another_unused_function():
    return "also unused"

if __name__ == "__main__":
    used_function()
""")
        
        dead_functions = ["unused_function", "another_unused_function"]
        result = fixer.remove_dead_functions(test_file, dead_functions)
        
        assert result == True
        assert len(fixer.fixes_applied) == 1
        assert "dead functions" in fixer.fixes_applied[0]
        
        # Check that dead functions were removed
        content = test_file.read_text()
        assert "def unused_function" not in content
        assert "def another_unused_function" not in content
        assert "def used_function" in content  # Should remain
    
    def test_update_requirements(self, temp_project):
        """Test updating requirements.txt."""
        fixer = DeadCodeFixer(temp_project)
        req_file = temp_project / "requirements.txt"
        
        # Create requirements.txt with unused packages
        req_file.write_text("""
pandas==2.2.3
numpy==2.2.4
unused-package==1.0.0
another-unused==2.0.0
""")
        
        unused_packages = ["unused-package", "another-unused"]
        result = fixer.update_requirements(unused_packages)
        
        assert result == True
        assert len(fixer.fixes_applied) == 1
        assert "unused packages" in fixer.fixes_applied[0]
        
        # Check that unused packages were removed
        content = req_file.read_text()
        assert "unused-package==1.0.0" not in content
        assert "another-unused==2.0.0" not in content
        assert "pandas==2.2.3" in content  # Should remain
        assert "numpy==2.2.4" in content  # Should remain
    
    def test_update_requirements_no_unused(self, temp_project):
        """Test updating requirements.txt when no unused packages."""
        fixer = DeadCodeFixer(temp_project)
        req_file = temp_project / "requirements.txt"
        
        # Create requirements.txt with only used packages
        req_file.write_text("""
pandas==2.2.3
numpy==2.2.4
""")
        
        unused_packages = []
        result = fixer.update_requirements(unused_packages)
        
        assert result == False
        assert len(fixer.fixes_applied) == 0
    
    def test_delete_dead_files(self, temp_project):
        """Test deleting dead files."""
        fixer = DeadCodeFixer(temp_project)
        
        # Create a dead file
        dead_file = temp_project / "src" / "dead_file.py"
        dead_file.write_text("# This file is dead")
        
        dead_files = ["src/dead_file.py"]
        result = fixer.delete_dead_files(dead_files)
        
        assert result == True
        assert len(fixer.fixes_applied) == 1
        assert "dead file" in fixer.fixes_applied[0]
        
        # Check that file was deleted
        assert not dead_file.exists()
        
        # Check that backup exists
        backup_files = list(fixer.backup_dir.rglob("*.py"))
        assert len(backup_files) == 1
        assert backup_files[0].read_text() == "# This file is dead"
    
    def test_apply_fixes_from_analysis(self, temp_project):
        """Test applying fixes from analysis results."""
        fixer = DeadCodeFixer(temp_project)
        
        # Create analysis results file
        analysis_file = temp_project / "analysis.json"
        analysis_results = {
            "dead_libraries": [
                {
                    "package_name": "unused-package",
                    "import_name": "unused_package",
                    "usage_count": 0,
                    "files_used_in": [],
                    "is_optional": False
                }
            ],
            "dead_files": [
                {
                    "file_path": "src/dead_file.py",
                    "file_type": "python",
                    "size_bytes": 1024,
                    "last_modified": "2024-01-15T10:30:00",
                    "potential_reason": "Not imported anywhere"
                }
            ],
            "dead_code": [
                {
                    "name": "unused_function",
                    "type": "function",
                    "file_path": "src/main.py",
                    "line_number": 10,
                    "context": "def unused_function():",
                    "severity": "high"
                }
            ]
        }
        
        with open(analysis_file, 'w') as f:
            json.dump(analysis_results, f)
        
        # Create the files mentioned in analysis
        (temp_project / "src" / "dead_file.py").write_text("# Dead file")
        (temp_project / "src" / "main.py").write_text("""
def used_function():
    return "used"

def unused_function():
    return "unused"
""")
        
        # Update requirements.txt
        (temp_project / "requirements.txt").write_text("""
pandas==2.2.3
unused-package==1.0.0
""")
        
        # Apply fixes
        fixes_summary = fixer.apply_fixes_from_analysis(analysis_file, dry_run=False)
        
        assert fixes_summary['dead_libraries_fixed'] == 1
        assert fixes_summary['dead_files_fixed'] == 1
        assert fixes_summary['dead_code_fixed'] == 1
        assert len(fixer.fixes_applied) == 3
    
    def test_apply_fixes_from_analysis_dry_run(self, temp_project, capsys):
        """Test applying fixes from analysis results in dry run mode."""
        fixer = DeadCodeFixer(temp_project)
        
        # Create analysis results file
        analysis_file = temp_project / "analysis.json"
        analysis_results = {
            "dead_libraries": [
                {
                    "package_name": "unused-package",
                    "import_name": "unused_package",
                    "usage_count": 0,
                    "files_used_in": [],
                    "is_optional": False
                }
            ]
        }
        
        with open(analysis_file, 'w') as f:
            json.dump(analysis_results, f)
        
        # Apply fixes in dry run mode
        fixes_summary = fixer.apply_fixes_from_analysis(analysis_file, dry_run=True)
        
        captured = capsys.readouterr()
        assert "DRY RUN MODE" in captured.out
        assert "Would remove 1 unused packages" in captured.out
        assert len(fixer.fixes_applied) == 0  # No actual fixes applied
    
    def test_print_summary(self, temp_project, capsys):
        """Test printing summary of applied fixes."""
        fixer = DeadCodeFixer(temp_project)
        
        # Add some mock fixes
        fixer.fixes_applied = [
            "Removed 2 unused imports from src/main.py",
            "Removed 1 unused package from requirements.txt"
        ]
        
        fixer.print_summary()
        captured = capsys.readouterr()
        
        assert "FIXES APPLIED (2 total)" in captured.out
        assert "Removed 2 unused imports" in captured.out
        assert "Removed 1 unused package" in captured.out
        assert "Backup directory" in captured.out
    
    def test_print_summary_no_fixes(self, temp_project, capsys):
        """Test printing summary when no fixes were applied."""
        fixer = DeadCodeFixer(temp_project)
        
        fixer.print_summary()
        captured = capsys.readouterr()
        
        assert "No fixes were applied" in captured.out


if __name__ == "__main__":
    pytest.main([__file__])
