#!/usr/bin/env python3
"""
Tests for dead code analyzer functionality.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "scripts" / "analysis" / "dead-code"))

from dead_code_analyzer import DeadCodeAnalyzer, DeadCodeItem, DeadLibraryItem, DeadFileItem


class TestDeadCodeAnalyzer:
    """Test cases for DeadCodeAnalyzer class."""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project structure for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            
            # Create project structure
            src_dir = project_root / "src"
            src_dir.mkdir()
            
            tests_dir = project_root / "tests"
            tests_dir.mkdir()
            
            scripts_dir = project_root / "scripts"
            scripts_dir.mkdir()
            
            # Create test files
            (src_dir / "main.py").write_text("""
import pandas as pd
import numpy as np

def used_function():
    return pd.DataFrame()

def unused_function():
    return "unused"

class UsedClass:
    pass

class UnusedClass:
    pass

if __name__ == "__main__":
    used_function()
""")
            
            (src_dir / "utils.py").write_text("""
import os

def utility_function():
    return os.getcwd()

def another_unused_function():
    return "unused"
""")
            
            (tests_dir / "test_main.py").write_text("""
import pytest
from src.main import used_function, UsedClass

def test_used_function():
    assert used_function() is not None

def test_used_class():
    instance = UsedClass()
    assert instance is not None
""")
            
            # Create requirements.txt
            (project_root / "requirements.txt").write_text("""
pandas==2.2.3
numpy==2.2.4
matplotlib==3.10.1
unused-package==1.0.0
""")
            
            yield project_root
    
    def test_init(self, temp_project):
        """Test analyzer initialization."""
        analyzer = DeadCodeAnalyzer(temp_project)
        
        assert analyzer.project_root == temp_project
        assert analyzer.src_dir == temp_project / "src"
        assert analyzer.tests_dir == temp_project / "tests"
        assert analyzer.scripts_dir == temp_project / "scripts"
        assert len(analyzer.stdlib_modules) > 0
        assert len(analyzer.package_to_import) > 0
    
    def test_find_python_files(self, temp_project):
        """Test finding Python files."""
        analyzer = DeadCodeAnalyzer(temp_project)
        python_files = analyzer.find_python_files(temp_project)
        
        # Should find our test files
        file_paths = [str(f.relative_to(temp_project)) for f in python_files]
        assert "src/main.py" in file_paths
        assert "src/utils.py" in file_paths
        assert "tests/test_main.py" in file_paths
    
    def test_analyze_file_imports(self, temp_project):
        """Test analyzing imports in a file."""
        analyzer = DeadCodeAnalyzer(temp_project)
        main_file = temp_project / "src" / "main.py"
        
        imports = analyzer.analyze_file_imports(main_file)
        
        assert "pandas" in imports['imports']
        assert "numpy" in imports['imports']
        assert "used_function" in imports['functions']
        assert "unused_function" in imports['functions']
        assert "UsedClass" in imports['classes']
        assert "UnusedClass" in imports['classes']
    
    def test_analyze_dead_code(self, temp_project):
        """Test dead code analysis."""
        analyzer = DeadCodeAnalyzer(temp_project)
        
        with patch.object(analyzer, '_count_usage', return_value=1):
            dead_items = analyzer.analyze_dead_code()
        
        # Should find unused functions and classes
        dead_names = [item.name for item in dead_items]
        assert "unused_function" in dead_names
        assert "UnusedClass" in dead_names
        assert "another_unused_function" in dead_names
    
    def test_analyze_dead_libraries(self, temp_project):
        """Test dead libraries analysis."""
        analyzer = DeadCodeAnalyzer(temp_project)
        
        dead_libraries = analyzer.analyze_dead_libraries()
        
        # Should find unused package
        dead_packages = [item.package_name for item in dead_libraries]
        assert "unused-package" in dead_packages
    
    def test_analyze_dead_files(self, temp_project):
        """Test dead files analysis."""
        analyzer = DeadCodeAnalyzer(temp_project)
        
        # Create an unused file
        unused_file = temp_project / "src" / "unused.py"
        unused_file.write_text("# This file is not imported anywhere")
        
        dead_files = analyzer.analyze_dead_files()
        
        # Should find the unused file
        dead_file_paths = [item.file_path for item in dead_files]
        assert "src/unused.py" in dead_file_paths
    
    def test_run_analysis(self, temp_project):
        """Test running complete analysis."""
        analyzer = DeadCodeAnalyzer(temp_project)
        
        with patch.object(analyzer, 'analyze_dead_code', return_value=[]):
            with patch.object(analyzer, 'analyze_dead_libraries', return_value=[]):
                with patch.object(analyzer, 'analyze_dead_files', return_value=[]):
                    results = analyzer.run_analysis()
        
        assert 'dead_code' in results
        assert 'dead_libraries' in results
        assert 'dead_files' in results
    
    def test_print_results(self, temp_project, capsys):
        """Test printing results."""
        analyzer = DeadCodeAnalyzer(temp_project)
        
        # Create mock results
        results = {
            'dead_code': [
                {
                    'name': 'test_function',
                    'type': 'function',
                    'file_path': 'src/test.py',
                    'line_number': 10,
                    'context': 'def test_function():',
                    'severity': 'high'
                }
            ],
            'dead_libraries': [
                {
                    'package_name': 'test-package',
                    'import_name': 'test_package',
                    'usage_count': 0,
                    'files_used_in': [],
                    'is_optional': False
                }
            ],
            'dead_files': []
        }
        
        analyzer.print_results(results)
        captured = capsys.readouterr()
        
        assert "DEAD CODE AND LIBRARIES ANALYSIS RESULTS" in captured.out
        assert "test_function" in captured.out
        assert "test-package" in captured.out


class TestDeadCodeItem:
    """Test cases for DeadCodeItem dataclass."""
    
    def test_dead_code_item_creation(self):
        """Test creating DeadCodeItem."""
        item = DeadCodeItem(
            name="test_function",
            type="function",
            file_path="src/test.py",
            line_number=10,
            context="def test_function():",
            severity="high"
        )
        
        assert item.name == "test_function"
        assert item.type == "function"
        assert item.file_path == "src/test.py"
        assert item.line_number == 10
        assert item.severity == "high"


class TestDeadLibraryItem:
    """Test cases for DeadLibraryItem dataclass."""
    
    def test_dead_library_item_creation(self):
        """Test creating DeadLibraryItem."""
        item = DeadLibraryItem(
            package_name="test-package",
            import_name="test_package",
            usage_count=0,
            files_used_in=[],
            is_optional=False
        )
        
        assert item.package_name == "test-package"
        assert item.import_name == "test_package"
        assert item.usage_count == 0
        assert item.is_optional == False


class TestDeadFileItem:
    """Test cases for DeadFileItem dataclass."""
    
    def test_dead_file_item_creation(self):
        """Test creating DeadFileItem."""
        item = DeadFileItem(
            file_path="src/unused.py",
            file_type="python",
            size_bytes=1024,
            last_modified="2024-01-15T10:30:00",
            potential_reason="Not imported anywhere"
        )
        
        assert item.file_path == "src/unused.py"
        assert item.file_type == "python"
        assert item.size_bytes == 1024
        assert item.potential_reason == "Not imported anywhere"


if __name__ == "__main__":
    pytest.main([__file__])
