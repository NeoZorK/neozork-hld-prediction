#!/usr/bin/env python3
"""
Dependency Test Analyzer

This tool automatically tests dependencies by temporarily disabling them and running tests
to determine which packages are actually needed. It works by:

1. Commenting out packages in requirements.txt
2. Running tests to see if they fail
3. Re-enabling packages that cause test failures
4. Reporting truly unused packages

Features:
- Automatic dependency testing
- Docker and container support
- MCP server testing
- Comprehensive error analysis
- Safe rollback mechanism
"""

import os
import sys
import re
import json
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional
from dataclasses import dataclass, asdict
import time
import logging
from enum import Enum

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x, **kwargs: x

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

class TestEnvironment(Enum):
    """Test environments"""
    NATIVE = "native"
    DOCKER = "docker"
    CONTAINER = "container"

class TestType(Enum):
    """Types of tests to run"""
    PYTEST = "pytest"
    MCP = "mcp"
    ALL = "all"

@dataclass
class DependencyTestResult:
    """Result of testing a dependency"""
    package_name: str
    is_required: bool
    test_environment: str
    test_type: str
    error_message: str = ""
    test_duration: float = 0.0
    confidence: float = 1.0

@dataclass
class TestSummary:
    """Summary of dependency testing"""
    total_packages: int
    required_packages: int
    unused_packages: int
    test_duration: float
    environment: str
    test_type: str
    results: List[DependencyTestResult]

class DependencyTestAnalyzer:
    """Analyzer for testing dependencies by disabling them"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.requirements_file = project_root / "requirements.txt"
        self.backup_file = None
        self.temp_requirements = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Test configurations
        self.test_configs = {
            TestEnvironment.NATIVE: {
                'pytest_cmd': ['uv', 'run', 'pytest', 'tests', '-n', 'auto'],
                'mcp_cmd': ['uv', 'run', 'python', 'scripts/mcp/check_mcp_status.py'],
                'install_cmd': ['uv', 'pip', 'install', '-r', 'requirements.txt']
            },
            TestEnvironment.DOCKER: {
                'pytest_cmd': ['docker', 'exec', 'neozork-container', 'uv', 'run', 'pytest', 'tests', '-n', 'auto'],
                'mcp_cmd': ['docker', 'exec', 'neozork-container', 'uv', 'run', 'python', 'scripts/mcp/check_mcp_status.py'],
                'install_cmd': ['docker', 'exec', 'neozork-container', 'uv', 'pip', 'install', '-r', 'requirements.txt']
            },
            TestEnvironment.CONTAINER: {
                'pytest_cmd': ['podman', 'exec', 'neozork-container', 'uv', 'run', 'pytest', 'tests', '-n', 'auto'],
                'mcp_cmd': ['podman', 'exec', 'neozork-container', 'uv', 'run', 'python', 'scripts/mcp/check_mcp_status.py'],
                'install_cmd': ['podman', 'exec', 'neozork-container', 'uv', 'pip', 'install', '-r', 'requirements.txt']
            }
        }
        
        # Packages to exclude from testing (always required)
        self.exclude_packages = {
            'uv',  # Package manager itself
            'pytest',  # Testing framework
            'pytest-xdist',  # Parallel testing
            'pytest-cov',  # Coverage
            'coverage',  # Coverage
            'black',  # Code formatting
            'flake8',  # Linting
            'mypy',  # Type checking
            'pre-commit',  # Git hooks
            'tox',  # Testing automation
            'pip',  # Package installer
            'setuptools',  # Build tools
            'wheel',  # Build tools
            'build',  # Build tools
            'twine',  # Package upload
            'sphinx',  # Documentation
            'sphinx-rtd-theme',  # Documentation theme
            'myst-parser',  # Documentation
            'jupyter',  # Jupyter notebooks
            'ipython',  # Interactive Python
            'notebook',  # Jupyter notebook
            'jupyterlab',  # Jupyter lab
            'jupyter-client',  # Jupyter client
            'jupyter-core',  # Jupyter core
            'jupyterlab-pygments',  # Jupyter syntax highlighting
            'notebook-shim',  # Jupyter notebook shim
            'ipython-pygments-lexers',  # IPython syntax highlighting
            'matplotlib-inline',  # Matplotlib inline
            'nest-asyncio',  # Async support
            'stack-data',  # Stack data
            'async-lru',  # Async LRU cache
            'rpds-py',  # Rust-based data structures
            'python-json-logger',  # JSON logging
            'send2trash',  # File operations
            'prometheus-client',  # Metrics
            'python-binance',  # Binance API
            'polygon-api-client',  # Polygon API
        }
    
    def detect_environment(self) -> TestEnvironment:
        """Detect the current test environment"""
        if os.path.exists('/.dockerenv'):
            return TestEnvironment.DOCKER
        elif os.path.exists('/.container'):
            return TestEnvironment.CONTAINER
        else:
            return TestEnvironment.NATIVE
    
    def parse_requirements(self) -> List[str]:
        """Parse requirements.txt and return list of packages"""
        if not self.requirements_file.exists():
            self.logger.error(f"Requirements file not found: {self.requirements_file}")
            return []
        
        packages = []
        with open(self.requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name
                    package_name = line.split('==')[0].split('>=')[0].split('<=')[0]
                    if package_name not in self.exclude_packages:
                        packages.append(package_name)
        
        return packages
    
    def create_backup(self) -> bool:
        """Create backup of requirements.txt"""
        try:
            self.backup_file = self.requirements_file.with_suffix('.txt.backup')
            shutil.copy2(self.requirements_file, self.backup_file)
            self.logger.info(f"Backup created: {self.backup_file}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return False
    
    def restore_backup(self) -> bool:
        """Restore requirements.txt from backup"""
        if self.backup_file and self.backup_file.exists():
            try:
                shutil.copy2(self.backup_file, self.requirements_file)
                self.logger.info("Requirements.txt restored from backup")
                return True
            except Exception as e:
                self.logger.error(f"Failed to restore backup: {e}")
                return False
        return False
    
    def disable_package(self, package_name: str) -> bool:
        """Temporarily disable a package by commenting it out"""
        try:
            with open(self.requirements_file, 'r') as f:
                lines = f.readlines()
            
            modified = False
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#') and package_name in line:
                    lines[i] = f"# DISABLED FOR TESTING: {line}"
                    modified = True
            
            if modified:
                with open(self.requirements_file, 'w') as f:
                    f.writelines(lines)
                self.logger.info(f"Disabled package: {package_name}")
                return True
            else:
                self.logger.warning(f"Package not found in requirements.txt: {package_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to disable package {package_name}: {e}")
            return False
    
    def enable_package(self, package_name: str) -> bool:
        """Re-enable a package by uncommenting it"""
        try:
            with open(self.requirements_file, 'r') as f:
                lines = f.readlines()
            
            modified = False
            for i, line in enumerate(lines):
                if line.startswith(f"# DISABLED FOR TESTING: ") and package_name in line:
                    lines[i] = line.replace("# DISABLED FOR TESTING: ", "")
                    modified = True
            
            if modified:
                with open(self.requirements_file, 'w') as f:
                    f.writelines(lines)
                self.logger.info(f"Enabled package: {package_name}")
                return True
            else:
                self.logger.warning(f"Disabled package not found: {package_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to enable package {package_name}: {e}")
            return False
    
    def run_command(self, cmd: List[str], timeout: int = 300) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr"""
        try:
            self.logger.debug(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.project_root
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", f"Command timed out after {timeout} seconds"
        except Exception as e:
            return -1, "", str(e)
    
    def install_dependencies(self, environment: TestEnvironment) -> bool:
        """Install dependencies in the specified environment"""
        config = self.test_configs[environment]
        cmd = config['install_cmd']
        
        self.logger.info(f"Installing dependencies in {environment.value} environment...")
        exit_code, stdout, stderr = self.run_command(cmd, timeout=600)
        
        if exit_code == 0:
            self.logger.info("Dependencies installed successfully")
            return True
        else:
            self.logger.error(f"Failed to install dependencies: {stderr}")
            return False
    
    def run_pytest(self, environment: TestEnvironment) -> Tuple[int, str, str]:
        """Run pytest in the specified environment"""
        config = self.test_configs[environment]
        cmd = config['pytest_cmd']
        
        self.logger.info(f"Running pytest in {environment.value} environment...")
        return self.run_command(cmd, timeout=600)
    
    def run_mcp_test(self, environment: TestEnvironment) -> Tuple[int, str, str]:
        """Run MCP server test in the specified environment"""
        config = self.test_configs[environment]
        cmd = config['mcp_cmd']
        
        self.logger.info(f"Running MCP test in {environment.value} environment...")
        return self.run_command(cmd, timeout=300)
    
    def analyze_test_output(self, stdout: str, stderr: str) -> Tuple[bool, str]:
        """Analyze test output to determine if tests passed"""
        # Check for common error patterns
        error_patterns = [
            r'ModuleNotFoundError',
            r'ImportError',
            r'No module named',
            r'Failed:',
            r'ERROR:',
            r'FAILED',
            r'Traceback',
            r'Exception:',
        ]
        
        combined_output = stdout + stderr
        
        for pattern in error_patterns:
            if re.search(pattern, combined_output, re.IGNORECASE):
                return False, f"Error detected: {pattern}"
        
        # Check for successful test completion
        success_patterns = [
            r'passed',
            r'PASSED',
            r'✓',
            r'SUCCESS',
        ]
        
        for pattern in success_patterns:
            if re.search(pattern, combined_output, re.IGNORECASE):
                return True, "Tests passed successfully"
        
        # If no clear success/failure indicators, assume failure
        return False, "No clear success indicators found"
    
    def test_package(self, package_name: str, environment: TestEnvironment, test_type: TestType) -> DependencyTestResult:
        """Test a single package by disabling it and running tests"""
        start_time = time.time()
        
        self.logger.info(f"Testing package: {package_name}")
        
        # Disable the package
        if not self.disable_package(package_name):
            return DependencyTestResult(
                package_name=package_name,
                is_required=False,
                test_environment=environment.value,
                test_type=test_type.value,
                error_message="Failed to disable package",
                test_duration=time.time() - start_time,
                confidence=0.0
            )
        
        try:
            # Install dependencies
            if not self.install_dependencies(environment):
                return DependencyTestResult(
                    package_name=package_name,
                    is_required=True,  # Assume required if install fails
                    test_environment=environment.value,
                    test_type=test_type.value,
                    error_message="Failed to install dependencies",
                    test_duration=time.time() - start_time,
                    confidence=0.8
                )
            
            # Run tests based on test type
            if test_type == TestType.PYTEST:
                exit_code, stdout, stderr = self.run_pytest(environment)
            elif test_type == TestType.MCP:
                exit_code, stdout, stderr = self.run_mcp_test(environment)
            elif test_type == TestType.ALL:
                # Run both pytest and MCP tests
                pytest_exit, pytest_out, pytest_err = self.run_pytest(environment)
                mcp_exit, mcp_out, mcp_err = self.run_mcp_test(environment)
                
                exit_code = pytest_exit or mcp_exit
                stdout = pytest_out + "\n" + mcp_out
                stderr = pytest_err + "\n" + mcp_err
            
            # Analyze results
            tests_passed, reason = self.analyze_test_output(stdout, stderr)
            
            # If tests failed, package is required
            is_required = not tests_passed
            
            return DependencyTestResult(
                package_name=package_name,
                is_required=is_required,
                test_environment=environment.value,
                test_type=test_type.value,
                error_message=reason if is_required else "",
                test_duration=time.time() - start_time,
                confidence=0.9 if is_required else 0.95
            )
            
        finally:
            # Always re-enable the package
            self.enable_package(package_name)
    
    def run_analysis(self, environment: TestEnvironment = None, test_type: TestType = TestType.ALL, 
                    packages: List[str] = None, dry_run: bool = False) -> TestSummary:
        """Run dependency analysis"""
        if environment is None:
            environment = self.detect_environment()
        
        self.logger.info(f"Starting dependency analysis in {environment.value} environment")
        self.logger.info(f"Test type: {test_type.value}")
        
        # Parse packages to test
        if packages is None:
            packages = self.parse_requirements()
        
        if not packages:
            self.logger.error("No packages to test")
            return TestSummary(
                total_packages=0,
                required_packages=0,
                unused_packages=0,
                test_duration=0.0,
                environment=environment.value,
                test_type=test_type.value,
                results=[]
            )
        
        self.logger.info(f"Testing {len(packages)} packages")
        
        if dry_run:
            self.logger.info("DRY RUN: Would test the following packages:")
            for pkg in packages:
                self.logger.info(f"  - {pkg}")
            return TestSummary(
                total_packages=len(packages),
                required_packages=0,
                unused_packages=len(packages),
                test_duration=0.0,
                environment=environment.value,
                test_type=test_type.value,
                results=[]
            )
        
        # Create backup
        if not self.create_backup():
            self.logger.error("Failed to create backup, aborting")
            return TestSummary(
                total_packages=len(packages),
                required_packages=0,
                unused_packages=0,
                test_duration=0.0,
                environment=environment.value,
                test_type=test_type.value,
                results=[]
            )
        
        start_time = time.time()
        results = []
        
        try:
            # Test each package
            for package in tqdm(packages, desc=f"Testing packages in {environment.value}"):
                result = self.test_package(package, environment, test_type)
                results.append(result)
                
                # Log result
                status = "REQUIRED" if result.is_required else "UNUSED"
                self.logger.info(f"{package}: {status} ({result.test_duration:.1f}s)")
        
        finally:
            # Restore backup
            self.restore_backup()
        
        test_duration = time.time() - start_time
        required_count = sum(1 for r in results if r.is_required)
        unused_count = len(results) - required_count
        
        return TestSummary(
            total_packages=len(packages),
            required_packages=required_count,
            unused_packages=unused_count,
            test_duration=test_duration,
            environment=environment.value,
            test_type=test_type.value,
            results=results
        )
    
    def print_results(self, summary: TestSummary, verbose: bool = False):
        """Print analysis results"""
        print("\n" + "="*80)
        print("DEPENDENCY TEST ANALYSIS RESULTS")
        print("="*80)
        
        print(f"\n📊 SUMMARY")
        print("-" * 60)
        print(f"Environment: {summary.environment}")
        print(f"Test Type: {summary.test_type}")
        print(f"Total Packages: {summary.total_packages}")
        print(f"Required Packages: {summary.required_packages}")
        print(f"Unused Packages: {summary.unused_packages}")
        print(f"Test Duration: {summary.test_duration:.1f} seconds")
        
        if summary.unused_packages > 0:
            print(f"\n❌ UNUSED PACKAGES ({summary.unused_packages})")
            print("-" * 60)
            for result in summary.results:
                if not result.is_required:
                    print(f"  - {result.package_name}")
                    if verbose and result.error_message:
                        print(f"    Reason: {result.error_message}")
        
        if summary.required_packages > 0:
            print(f"\n✅ REQUIRED PACKAGES ({summary.required_packages})")
            print("-" * 60)
            for result in summary.results:
                if result.is_required:
                    print(f"  - {result.package_name}")
                    if verbose and result.error_message:
                        print(f"    Error: {result.error_message}")
        
        if summary.unused_packages > 0:
            print(f"\n💡 RECOMMENDATIONS:")
            print("- Review unused packages before removal")
            print("- Consider if packages might be used in the future")
            print("- Check for dynamic imports or conditional usage")
            print("- Test thoroughly after removing packages")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Dependency Test Analyzer")
    parser.add_argument('--environment', choices=['native', 'docker', 'container'], 
                       help='Test environment (auto-detected if not specified)')
    parser.add_argument('--test-type', choices=['pytest', 'mcp', 'all'], default='all',
                       help='Type of tests to run')
    parser.add_argument('--packages', nargs='+', help='Specific packages to test')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be tested without running')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--output-file', help='Output file path')
    
    args = parser.parse_args()
    
    # Determine environment
    if args.environment:
        environment = TestEnvironment(args.environment)
    else:
        environment = None  # Will be auto-detected
    
    # Determine test type
    test_type = TestType(args.test_type)
    
    # Initialize analyzer
    analyzer = DependencyTestAnalyzer(PROJECT_ROOT)
    
    # Run analysis
    summary = analyzer.run_analysis(
        environment=environment,
        test_type=test_type,
        packages=args.packages,
        dry_run=args.dry_run
    )
    
    # Output results
    if args.output_format == 'json':
        output = json.dumps(asdict(summary), indent=2)
    else:
        analyzer.print_results(summary, verbose=args.verbose)
        return
    
    # Write to file or stdout
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(output)
        print(f"Results written to {args.output_file}")
    else:
        print(output)

if __name__ == "__main__":
    main()
