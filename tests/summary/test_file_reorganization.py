#!/usr/bin/env python3
"""
Test to verify that file reorganization was done correctly
"""

import os
import sys
from pathlib import Path
import pytest

def test_analyze_test_coverage_moved():
    """Test that analyze_test_coverage.py was moved to tests/ with zzz_ prefix"""
    # Check that the file exists in the new location
    new_path = Path("tests/zzz_analyze_test_coverage.py")
    assert new_path.exists(), f"File should exist at {new_path}"
    
    # Check that the file doesn't exist in the old location
    old_path = Path("scripts/analyze_test_coverage.py")
    assert not old_path.exists(), f"File should not exist at {old_path}"
    
    # Check that the file has the correct content (basic check)
    with open(new_path, 'r') as f:
        content = f.read()
        assert "analyze_coverage" in content, "File should contain analyze_coverage function"
        assert "This script runs as the last test" in content, "File should have updated description"

def test_run_tests_moved():
    """Test that run_tests.py was moved to tests/"""
    # Check that the file exists in the new location
    new_path = Path("tests/run_tests.py")
    assert new_path.exists(), f"File should exist at {new_path}"
    
    # Check that the file doesn't exist in the old location
    old_path = Path("scripts/run_tests.py")
    assert not old_path.exists(), f"File should not exist at {old_path}"
    
    # Check that the file has the correct content (basic check)
    with open(new_path, 'r') as f:
        content = f.read()
        assert "run_selected_tests" in content, "File should contain run_selected_tests function"
        assert "TEST_CATEGORIES" in content, "File should contain TEST_CATEGORIES"

def test_test_stdio_moved():
    """Test that test_stdio.py was moved to tests/"""
    # Check that the file exists in the new location
    new_path = Path("tests/test_stdio.py")
    assert new_path.exists(), f"File should exist at {new_path}"
    
    # Check that the file doesn't exist in the old location
    old_path = Path("scripts/test_stdio.py")
    assert not old_path.exists(), f"File should not exist at {old_path}"
    
    # Check that the file has the correct content (basic check)
    with open(new_path, 'r') as f:
        content = f.read()
        assert "test_stdio_mode" in content, "File should contain test_stdio_mode function"
        assert "PyCharm GitHub Copilot MCP Server" in content, "File should contain server reference"

def test_documentation_updated():
    """Test that documentation files were updated with new paths"""
    # Check docs/scripts.md
    scripts_doc = Path("docs/scripts.md")
    if scripts_doc.exists():
        with open(scripts_doc, 'r') as f:
            content = f.read()
            assert "tests/zzz_analyze_test_coverage.py" in content, "Documentation should reference new path"
            assert "scripts/analyze_test_coverage.py" not in content, "Documentation should not reference old path"
    
    # Check docs/testing.md
    testing_doc = Path("docs/testing.md")
    if testing_doc.exists():
        with open(testing_doc, 'r') as f:
            content = f.read()
            assert "tests/run_tests.py" in content, "Documentation should reference new path"
            assert "scripts/run_tests.py" not in content, "Documentation should not reference old path"
    
    # Check docs/mcp-servers/SETUP.md
    setup_doc = Path("docs/mcp-servers/SETUP.md")
    if setup_doc.exists():
        with open(setup_doc, 'r') as f:
            content = f.read()
            assert "tests/test_stdio.py" in content, "Documentation should reference new path"
            assert "scripts/test_stdio.py" not in content, "Documentation should not reference old path"

def test_docker_entrypoint_updated():
    """Test that docker-entrypoint.sh was updated with new path"""
    entrypoint = Path("docker-entrypoint.sh")
    if entrypoint.exists():
        with open(entrypoint, 'r') as f:
            content = f.read()
            # Check for run_tests_docker.py reference (used in the script)
            assert "run_tests_docker.py" in content, "Docker entrypoint should reference run_tests_docker.py"
            # Check that it doesn't reference the old path
            assert "/app/scripts/run_tests.py" not in content, "Docker entrypoint should not reference old path"

def test_init_files_exist():
    """Test that __init__.py files exist in all src/ and tests/ directories and subdirectories"""
    
    def check_init_files(directory: Path, context: str):
        """Check for __init__.py files in directory and all subdirectories"""
        missing_inits = []
        
        # Check the directory itself
        if not (directory / "__init__.py").exists():
            missing_inits.append(str(directory / "__init__.py"))
        
        # Check all subdirectories
        for subdir in directory.rglob("*/"):
            if subdir.is_dir() and "__pycache__" not in str(subdir) and "egg-info" not in str(subdir) and ".pytest_cache" not in str(subdir):
                if not (subdir / "__init__.py").exists():
                    missing_inits.append(str(subdir / "__init__.py"))
        
        return missing_inits
    
    # Check src/ directory
    src_dir = Path("src")
    assert src_dir.exists(), "src/ directory should exist"
    src_missing = check_init_files(src_dir, "src/")
    
    # Check tests/ directory
    tests_dir = Path("tests")
    assert tests_dir.exists(), "tests/ directory should exist"
    tests_missing = check_init_files(tests_dir, "tests/")
    
    # Report missing __init__.py files
    all_missing = src_missing + tests_missing
    if all_missing:
        missing_list = "\n".join(f"  - {path}" for path in all_missing)
        pytest.fail(f"Missing __init__.py files:\n{missing_list}")
    
    print(f"✅ All directories in src/ and tests/ have __init__.py files")

def test_neozork_mcp_server_exists():
    """Test that neozork_mcp_server.py exists in root directory"""
    # Check that the file exists in the root location
    path = Path("neozork_mcp_server.py")
    assert path.exists(), f"File should exist at {path}"
    
    # Check that the file has the correct content (basic check)
    with open(path, 'r') as f:
        content = f.read()
        assert "NeoZorKMCPServer" in content, "File should contain NeoZorKMCPServer class"

def test_neozork_mcp_manager_exists():
    """Test that neozork_mcp_manager.py exists in scripts/mcp/"""
    # Check that the file exists in the scripts/mcp location
    path = Path("scripts/mcp/neozork_mcp_manager.py")
    assert path.exists(), f"File should exist at {path}"
    
    # Check that the file has the correct content (basic check)
    with open(path, 'r') as f:
        content = f.read()
        assert "NeozorkMCPManager" in content, "File should contain NeozorkMCPManager class"

if __name__ == "__main__":
    # Run all tests
    pytest.main([__file__, "-v"]) 