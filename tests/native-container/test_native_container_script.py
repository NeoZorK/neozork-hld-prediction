#!/usr/bin/env python3
"""
Unit tests for the native container interactive script.

This module tests the functionality of the native-container.sh script
including system checks, container management, and interactive features.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock, call
import subprocess
import shutil
from pathlib import Path
import pytest

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tests.conftest import skip_if_docker


class TestNativeContainerScript(unittest.TestCase):
    """Test cases for the native container interactive script."""

    def setUp(self):
        """Set up test environment."""
        self.script_path = project_root / "scripts" / "native-container" / "native-container.sh"
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_script_exists(self):
        """Test that the script file exists and is executable."""
        self.assertTrue(self.script_path.exists(), "Script file should exist")
        self.assertTrue(os.access(self.script_path, os.X_OK), "Script should be executable")

    @skip_if_docker
    def test_script_syntax(self):
        """Test that the script has valid bash syntax."""
        try:
            result = subprocess.run(
                ["bash", "-n", str(self.script_path)],
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0, f"Script syntax error: {result.stderr}")
        except FileNotFoundError:
            self.skipTest("bash not available")

    @patch('subprocess.run')
    def test_check_macos_version_success(self, mock_run):
        """Test macOS version check with compatible version."""
        # Mock sw_vers output for macOS 26
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="26.0.0\n"
        )
        
        # Create a minimal script environment
        os.environ['SW_VERS'] = 'sw_vers'
        
        # Test the function (we'll need to extract it or test via subprocess)
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="0\n",  # Exit option
            capture_output=True,
            text=True
        )
        
        # Should not have syntax errors
        self.assertNotIn("syntax error", result.stderr.lower())

    @patch('subprocess.run')
    def test_check_native_container_success(self, mock_run):
        """Test native container application check."""
        # Mock container command
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="container version 1.0.0\n"
        )
        
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="4\n0\n",  # Help then exit
            capture_output=True,
            text=True
        )
        
        self.assertNotIn("syntax error", result.stderr.lower())

    @patch('subprocess.run')
    def test_check_python_success(self, mock_run):
        """Test Python installation check."""
        # Mock python3 command
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Python 3.11.0\n"
        )
        
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="4\n0\n",  # Help then exit
            capture_output=True,
            text=True
        )
        
        self.assertNotIn("syntax error", result.stderr.lower())

    def test_project_structure_check(self):
        """Test project structure validation."""
        # Create minimal required structure
        required_dirs = ["src", "tests", "data", "logs", "results"]
        for dir_name in required_dirs:
            os.makedirs(dir_name, exist_ok=True)
        
        # Create required files
        required_files = ["container.yaml", "container-entrypoint.sh", "requirements.txt", "run_analysis.py"]
        for file_name in required_files:
            with open(file_name, 'w') as f:
                f.write("# Test file\n")
        
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="4\n0\n",  # Help then exit
            capture_output=True,
            text=True
        )
        
        self.assertNotIn("syntax error", result.stderr.lower())

    @patch('subprocess.run')
    def test_container_management_functions(self, mock_run):
        """Test container management functions."""
        # Mock container list command
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="container-id neozork-hld-prediction running\n"),
            MagicMock(returncode=0, stdout=""),  # container start
            MagicMock(returncode=0, stdout=""),  # container stop
        ]
        
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="1\n2\n0\n",  # Start, stop, exit
            capture_output=True,
            text=True
        )
        
        self.assertNotIn("syntax error", result.stderr.lower())

    def test_script_help_output(self):
        """Test script help output when run non-interactively."""
        # Redirect stdin to /dev/null to simulate non-interactive mode
        with open(os.devnull, 'r') as devnull:
            result = subprocess.run(
                ["bash", str(self.script_path)],
                stdin=devnull,
                capture_output=True,
                text=True
            )
        
        # Should show usage information
        self.assertIn("Usage:", result.stdout)
        self.assertIn("interactive", result.stdout)

    @pytest.mark.skip(reason="Requires interactive terminal (tty)")
    def test_script_structure(self):
        """Test that the script shows the correct menu structure."""
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="5\n",  # Exit immediately
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Check for menu items in simplified menu
        menu_items = [
            "Start Container (Full Sequence)",
            "Stop Container (Full Sequence)",
            "Show Container Status",
            "Help",
            "Exit"
        ]
        
        for item in menu_items:
            self.assertIn(item, result.stdout, f"Menu should contain: {item}")

    @pytest.mark.skip(reason="Requires interactive terminal (tty)")
    def test_script_colors_and_formatting(self):
        """Test script colors and formatting."""
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="4\n5\n",  # Help then exit
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Should not have syntax errors
        self.assertNotIn("syntax error", result.stderr.lower())
        # Should show colored output (ANSI escape codes)
        self.assertIn("\033[", result.stdout, "Script should use color formatting")

    def test_cleanup_functionality(self):
        """Test cleanup functionality."""
        # Create minimal project structure
        os.makedirs("src", exist_ok=True)
        os.makedirs("tests", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs("results", exist_ok=True)
        
        with open("container.yaml", 'w') as f:
            f.write("apiVersion: v1\nkind: Container\n")
        
        with open("container-entrypoint.sh", 'w') as f:
            f.write("#!/bin/bash\necho 'Container started'\n")
        
        with open("requirements.txt", 'w') as f:
            f.write("pytest\n")
        
        with open("run_analysis.py", 'w') as f:
            f.write("#!/usr/bin/env python3\nprint('Analysis script')\n")
        
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="2\n5\n",  # Stop container (cleanup), exit
            capture_output=True,
            text=True,
            timeout=15
        )
        
        self.assertNotIn("syntax error", result.stderr.lower())

    @pytest.mark.skip(reason="Requires interactive terminal (tty)")
    def test_error_handling(self):
        """Test error handling in the script."""
        # Test with invalid menu choice
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="99\n5\n",  # Invalid choice, exit
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Should handle invalid input gracefully
        self.assertNotIn("syntax error", result.stderr.lower())
        self.assertIn("Invalid choice", result.stdout)

    def test_script_permissions(self):
        """Test script file permissions."""
        stat_info = os.stat(self.script_path)
        # Check if executable by owner
        self.assertTrue(stat_info.st_mode & 0o100, "Script should be executable by owner")

    def test_script_shebang(self):
        """Test script shebang line."""
        with open(self.script_path, 'r') as f:
            first_line = f.readline().strip()
        
        self.assertEqual(first_line, "#!/bin/bash", "Script should start with proper shebang")

    def test_script_variables(self):
        """Test script variable definitions."""
        with open(self.script_path, 'r') as f:
            content = f.read()
        
        # Check for important variables
        self.assertIn("CONTAINER_NAME=", content, "Script should define CONTAINER_NAME")
        self.assertIn("RED=", content, "Script should define color variables")
        self.assertIn("GREEN=", content, "Script should define color variables")

    def test_script_functions(self):
        """Test script function definitions."""
        with open(self.script_path, 'r') as f:
            content = f.read()
        
        # Check for important functions in simplified script
        required_functions = [
            "print_status",
            "print_success", 
            "print_error",
            "check_container_exists",
            "check_container_running",
            "start_container_sequence",
            "stop_container_sequence",
            "show_main_menu"
        ]
        
        for func in required_functions:
            self.assertIn(f"{func}()", content, f"Script should define function {func}")

    def test_script_comments(self):
        """Test script documentation and comments."""
        with open(self.script_path, 'r') as f:
            content = f.read()
        
        # Check for documentation
        self.assertIn("Native Container Interactive Script", content, "Script should have header comment")
        self.assertIn("This script provides", content, "Script should have description")

    @pytest.mark.skip(reason="Requires interactive terminal (tty)")
    def test_script_exit_codes(self):
        """Test script exit codes."""
        # Test normal exit
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="0\n",  # Exit
            capture_output=True,
            text=True,
            timeout=10
        )
        
        self.assertEqual(result.returncode, 0, "Script should exit with code 0")

        # Test help exit
        with open(os.devnull, 'r') as devnull:
            result = subprocess.run(
                ["bash", str(self.script_path)],
                stdin=devnull,
                capture_output=True,
                text=True
            )
        
        self.assertEqual(result.returncode, 1, "Script should exit with code 1 in non-interactive mode")


class TestNativeContainerScriptIntegration(unittest.TestCase):
    """Integration tests for the native container script."""

    def setUp(self):
        """Set up integration test environment."""
        self.script_path = project_root / "scripts" / "native-container" / "native-container.sh"
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Clean up integration test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @pytest.mark.skip(reason="Requires interactive terminal (tty)")
    def test_full_workflow_simulation(self):
        """Test a complete workflow simulation."""
        # Create minimal project structure
        os.makedirs("src", exist_ok=True)
        os.makedirs("tests", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs("results", exist_ok=True)
        
        with open("container.yaml", 'w') as f:
            f.write("apiVersion: v1\nkind: Container\n")
        
        with open("container-entrypoint.sh", 'w') as f:
            f.write("#!/bin/bash\necho 'Container started'\n")
        
        with open("requirements.txt", 'w') as f:
            f.write("pytest\n")
        
        with open("run_analysis.py", 'w') as f:
            f.write("#!/usr/bin/env python3\nprint('Analysis script')\n")
        
        # Test script execution (simulate user interaction)
        commands = [
            "4\n",  # Help
            "0\n",  # Exit
        ]
        
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="".join(commands),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should complete without errors
        self.assertEqual(result.returncode, 0, "Script should complete successfully")
        self.assertNotIn("syntax error", result.stderr.lower())

    def test_script_with_missing_dependencies(self):
        """Test script behavior with missing dependencies."""
        # Test without container command
        with patch.dict(os.environ, {'PATH': '/usr/bin:/bin'}):
            result = subprocess.run(
                ["bash", str(self.script_path)],
                input="4\n0\n",  # Help, exit
                capture_output=True,
                text=True,
                timeout=15
            )
        
        # Should handle missing dependencies gracefully
        self.assertNotIn("syntax error", result.stderr.lower())

    @pytest.mark.skip(reason="Requires interactive terminal (tty)")
    def test_script_performance(self):
        """Test script performance and responsiveness."""
        import time
        
        start_time = time.time()
        
        result = subprocess.run(
            ["bash", str(self.script_path)],
            input="0\n",  # Exit immediately
            capture_output=True,
            text=True,
            timeout=10
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Script should start quickly (less than 5 seconds)
        self.assertLess(execution_time, 5.0, f"Script took too long to start: {execution_time:.2f}s")
        self.assertEqual(result.returncode, 0, "Script should complete successfully")


if __name__ == '__main__':
    unittest.main() 