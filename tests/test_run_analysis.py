#!/usr/bin/env python3
"""
Unit tests for run_analysis.py
"""

import pytest
import os
import sys

def test_run_analysis_import():
    """Test that run_analysis can be imported"""
    try:
        # Add project root to path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        
        # Try to import the main module
        import run_analysis
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import run_analysis: {e}")

def test_run_analysis_file_exists():
    """Test that the run_analysis file exists"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    analysis_file = os.path.join(project_root, "run_analysis.py")
    assert os.path.exists(analysis_file), f"run_analysis file not found: {analysis_file}"

def test_run_analysis_basic_functionality():
    """Test basic run_analysis functionality"""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        
        # Test that the file can be executed as a module
        import subprocess
        result = subprocess.run([sys.executable, "-c", "import run_analysis"], 
                              capture_output=True, text=True, cwd=project_root)
        assert result.returncode == 0, f"Failed to import module: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Basic functionality test failed: {e}") 