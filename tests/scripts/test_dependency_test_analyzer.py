#!/usr/bin/env python3
"""
Tests for Dependency Test Analyzer

Tests the dependency testing functionality that disables packages and runs tests.
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "analysis" / "dead-code"))

from dependency_test_analyzer import (
    DependencyTestAnalyzer, 
    DependencyTestResult, 
    TestSummary,
    TestEnvironment,
    TestType
)

class TestDependencyTestAnalyzer:
    """Test cases for DependencyTestAnalyzer"""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project structure for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create requirements.txt
            requirements_content = """numpy==1.21.0
pandas==1.3.0
matplotlib==3.4.0
requests==2.25.1
beautifulsoup4==4.9.3
"""
            (temp_path / "requirements.txt").write_text(requirements_content)
            
            yield temp_path
    
    def test_initialization(self, temp_project):
        """Test analyzer initialization"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        assert analyzer.project_root == temp_project
        assert analyzer.requirements_file == temp_project / "requirements.txt"
        assert len(analyzer.exclude_packages) > 0
        assert len(analyzer.test_configs) == 3  # native, docker, container
    
    def test_detect_environment(self, temp_project):
        """Test environment detection"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Check if we're in Docker environment
        is_docker = os.path.exists('/.dockerenv')
        
        # Test environment detection
        env = analyzer.detect_environment()
        
        if is_docker:
            # In Docker environment, should return DOCKER
            assert env == TestEnvironment.DOCKER
        else:
            # In native environment, should return NATIVE
            assert env == TestEnvironment.NATIVE
        
        # Test Docker environment detection with mock
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            env = analyzer.detect_environment()
            assert env == TestEnvironment.DOCKER
    
    def test_parse_requirements(self, temp_project):
        """Test requirements parsing"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        packages = analyzer.parse_requirements()
        
        # Should find packages from requirements.txt
        assert "numpy" in packages
        assert "pandas" in packages
        assert "matplotlib" in packages
        assert "requests" in packages
        assert "beautifulsoup4" in packages
        
        # Should not include excluded packages
        assert "uv" not in packages
        assert "pytest" not in packages
    
    def test_create_backup(self, temp_project):
        """Test backup creation"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Create backup
        success = analyzer.create_backup()
        assert success == True
        
        # Check backup file exists
        assert analyzer.backup_file.exists()
        assert analyzer.backup_file.suffix == '.backup'
        
        # Check backup content matches original
        original_content = (temp_project / "requirements.txt").read_text()
        backup_content = analyzer.backup_file.read_text()
        assert original_content == backup_content
    
    def test_restore_backup(self, temp_project):
        """Test backup restoration"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Create backup first
        analyzer.create_backup()
        
        # Modify requirements.txt
        (temp_project / "requirements.txt").write_text("modified content")
        
        # Restore backup
        success = analyzer.restore_backup()
        assert success == True
        
        # Check content is restored
        content = (temp_project / "requirements.txt").read_text()
        assert "numpy==1.21.0" in content
        assert "modified content" not in content
    
    def test_disable_package(self, temp_project):
        """Test package disabling"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Disable a package
        success = analyzer.disable_package("numpy")
        assert success == True
        
        # Check package is commented out
        content = (temp_project / "requirements.txt").read_text()
        assert "# DISABLED FOR TESTING: numpy==1.21.0" in content
        # The original line is still there but commented out
    
    def test_enable_package(self, temp_project):
        """Test package enabling"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Disable a package first
        analyzer.disable_package("numpy")
        
        # Enable the package
        success = analyzer.enable_package("numpy")
        assert success == True
        
        # Check package is uncommented
        content = (temp_project / "requirements.txt").read_text()
        assert "numpy==1.21.0" in content
        assert "# DISABLED FOR TESTING: numpy==1.21.0" not in content
    
    def test_run_command(self, temp_project):
        """Test command execution"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Test successful command
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "success"
            mock_result.stderr = ""
            mock_run.return_value = mock_result
            
            exit_code, stdout, stderr = analyzer.run_command(['echo', 'test'])
            
            assert exit_code == 0
            assert stdout == "success"
            assert stderr == ""
    
    def test_analyze_test_output(self, temp_project):
        """Test test output analysis"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Test successful output
        success, reason = analyzer.analyze_test_output("passed", "")
        assert success == True
        assert "passed successfully" in reason
        
        # Test failed output
        success, reason = analyzer.analyze_test_output("", "ModuleNotFoundError")
        assert success == False
        assert "ModuleNotFoundError" in reason
        
        # Test failed output with different patterns
        success, reason = analyzer.analyze_test_output("", "ImportError: No module named 'numpy'")
        assert success == False
        assert "ImportError" in reason
    
    @patch('dependency_test_analyzer.DependencyTestAnalyzer.install_dependencies')
    @patch('dependency_test_analyzer.DependencyTestAnalyzer.run_pytest')
    def test_test_package_required(self, mock_run_pytest, mock_install, temp_project):
        """Test package testing when package is required"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Mock dependencies
        mock_install.return_value = True
        mock_run_pytest.return_value = (1, "", "ModuleNotFoundError")
        
        # Test package
        result = analyzer.test_package("numpy", TestEnvironment.NATIVE, TestType.PYTEST)
        
        assert result.package_name == "numpy"
        assert result.is_required == True
        assert result.test_environment == "native"
        assert result.test_type == "pytest"
        assert "ModuleNotFoundError" in result.error_message
        assert result.confidence > 0.8
    
    @patch('dependency_test_analyzer.DependencyTestAnalyzer.install_dependencies')
    @patch('dependency_test_analyzer.DependencyTestAnalyzer.run_pytest')
    def test_test_package_unused(self, mock_run_pytest, mock_install, temp_project):
        """Test package testing when package is unused"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Mock dependencies
        mock_install.return_value = True
        mock_run_pytest.return_value = (0, "passed", "")
        
        # Test package
        result = analyzer.test_package("numpy", TestEnvironment.NATIVE, TestType.PYTEST)
        
        assert result.package_name == "numpy"
        assert result.is_required == False
        assert result.test_environment == "native"
        assert result.test_type == "pytest"
        assert result.error_message == ""
        assert result.confidence > 0.9
    
    @patch('dependency_test_analyzer.DependencyTestAnalyzer.create_backup')
    @patch('dependency_test_analyzer.DependencyTestAnalyzer.test_package')
    @patch('dependency_test_analyzer.DependencyTestAnalyzer.restore_backup')
    def test_run_analysis(self, mock_restore, mock_test_package, mock_backup, temp_project):
        """Test complete analysis run"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Mock dependencies
        mock_backup.return_value = True
        mock_restore.return_value = True
        
        # Mock test results
        mock_result1 = DependencyTestResult(
            package_name="numpy",
            is_required=True,
            test_environment="native",
            test_type="pytest",
            error_message="ModuleNotFoundError",
            test_duration=10.0,
            confidence=0.9
        )
        mock_result2 = DependencyTestResult(
            package_name="pandas",
            is_required=False,
            test_environment="native",
            test_type="pytest",
            error_message="",
            test_duration=8.0,
            confidence=0.95
        )
        mock_test_package.side_effect = [mock_result1, mock_result2]
        
        # Run analysis
        summary = analyzer.run_analysis(
            environment=TestEnvironment.NATIVE,
            test_type=TestType.PYTEST,
            packages=["numpy", "pandas"]
        )
        
        assert summary.total_packages == 2
        assert summary.required_packages == 1
        assert summary.unused_packages == 1
        assert summary.environment == "native"
        assert summary.test_type == "pytest"
        assert len(summary.results) == 2
    
    def test_run_analysis_dry_run(self, temp_project):
        """Test analysis dry run"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        summary = analyzer.run_analysis(
            environment=TestEnvironment.NATIVE,
            test_type=TestType.PYTEST,
            packages=["numpy", "pandas"],
            dry_run=True
        )
        
        assert summary.total_packages == 2
        assert summary.required_packages == 0
        assert summary.unused_packages == 2
        assert summary.test_duration == 0.0
    
    def test_run_analysis_no_packages(self, temp_project):
        """Test analysis with no packages"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        summary = analyzer.run_analysis(
            environment=TestEnvironment.NATIVE,
            test_type=TestType.PYTEST,
            packages=[]
        )
        
        assert summary.total_packages == 0
        assert summary.required_packages == 0
        assert summary.unused_packages == 0
    
    def test_print_results(self, temp_project, capsys):
        """Test results printing"""
        analyzer = DependencyTestAnalyzer(temp_project)
        
        # Create sample results
        results = [
            DependencyTestResult(
                package_name="numpy",
                is_required=True,
                test_environment="native",
                test_type="pytest",
                error_message="ModuleNotFoundError",
                test_duration=10.0,
                confidence=0.9
            ),
            DependencyTestResult(
                package_name="pandas",
                is_required=False,
                test_environment="native",
                test_type="pytest",
                error_message="",
                test_duration=8.0,
                confidence=0.95
            )
        ]
        
        summary = TestSummary(
            total_packages=2,
            required_packages=1,
            unused_packages=1,
            test_duration=18.0,
            environment="native",
            test_type="pytest",
            results=results
        )
        
        analyzer.print_results(summary)
        captured = capsys.readouterr()
        
        assert "DEPENDENCY TEST ANALYSIS RESULTS" in captured.out
        assert "numpy" in captured.out
        assert "pandas" in captured.out
        assert "SUMMARY" in captured.out
        assert "REQUIRED PACKAGES" in captured.out
        assert "UNUSED PACKAGES" in captured.out

class TestTestEnvironment:
    """Test TestEnvironment enum"""
    
    def test_enum_values(self):
        """Test enum values"""
        assert TestEnvironment.NATIVE.value == "native"
        assert TestEnvironment.DOCKER.value == "docker"
        assert TestEnvironment.CONTAINER.value == "container"

class TestTestType:
    """Test TestType enum"""
    
    def test_enum_values(self):
        """Test enum values"""
        assert TestType.PYTEST.value == "pytest"
        assert TestType.MCP.value == "mcp"
        assert TestType.ALL.value == "all"

if __name__ == "__main__":
    pytest.main([__file__])
