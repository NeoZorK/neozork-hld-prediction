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

def test_auto_start_mcp_still_exists():
    """Test that auto_start_mcp.py still exists in scripts/"""
    # Check that the file still exists in the original location
    path = Path("scripts/auto_start_mcp.py")
    assert path.exists(), f"File should still exist at {path}"
    
    # Check that the file has the correct content (basic check)
    with open(path, 'r') as f:
        content = f.read()
        assert "MCPAutoStarter" in content, "File should contain MCPAutoStarter class"

def test_run_cursor_mcp_still_exists():
    """Test that run_cursor_mcp.py still exists in scripts/"""
    # Check that the file still exists in the original location
    path = Path("scripts/run_cursor_mcp.py")
    assert path.exists(), f"File should still exist at {path}"
    
    # Check that the file has the correct content (basic check)
    with open(path, 'r') as f:
        content = f.read()
        assert "PyCharmGitHubCopilotMCPServerRunner" in content, "File should contain PyCharmGitHubCopilotMCPServerRunner class"

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
            assert "/app/tests/run_tests.py" in content, "Docker entrypoint should reference new path"
            assert "/app/scripts/run_tests.py" not in content, "Docker entrypoint should not reference old path"

if __name__ == "__main__":
    # Run all tests
    pytest.main([__file__, "-v"]) 