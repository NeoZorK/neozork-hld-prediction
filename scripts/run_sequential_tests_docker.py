#!/usr/bin/env python3
"""
Sequential Docker Test Runner for NeoZork HLD Prediction

This script runs tests in Docker environment sequentially by folder
to avoid worker crashes and resource issues. Tests are run in a specific order
to ensure dependencies are met and resources are properly managed.
"""

import os
import sys
import subprocess
import logging
import time
import yaml
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SequentialTestRunner:
    """Sequential test runner for Docker environment."""
    
    def __init__(self, config_path: Optional[str] = None):
        # Detect if we're in Docker or local environment
        if os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER', False):
            self.project_root = Path('/app')
        else:
            # Local environment - use current directory
            self.project_root = Path(__file__).parent.parent
        
        self.tests_root = self.project_root / 'tests'
        self.results = {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'errors': 0,
            'total_time': 0
        }
        
        # Load configuration
        self.config = self.load_config(config_path)
        self.test_folders = self.config.get('test_folders', [])
        self.global_settings = self.config.get('global_settings', {})
        self.folder_overrides = self.config.get('folder_overrides', {})
        self.dependencies = self.config.get('dependencies', {})
        
        # Extract folder names for backward compatibility
        self.folder_names = [folder['name'] for folder in self.test_folders]
    
    def load_config(self, config_path: Optional[str] = None) -> Dict:
        """Load test execution configuration from YAML file."""
        if config_path is None:
            config_path = self.tests_root / 'test_execution_order.yaml'
        
        config_file = Path(config_path)
        
        if not config_file.exists():
            logger.warning(f"Config file {config_path} not found, using default configuration")
            return self.get_default_config()
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading config file {config_path}: {e}")
            logger.info("Using default configuration")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Get default configuration if YAML file is not available."""
        return {
            'test_folders': [
                {'name': 'common', 'description': 'Basic utilities', 'timeout': 30, 'required': True},
                {'name': 'unit', 'description': 'Unit tests', 'timeout': 60, 'required': True},
                {'name': 'utils', 'description': 'Utility functions', 'timeout': 45, 'required': True},
                {'name': 'data', 'description': 'Data processing', 'timeout': 90, 'required': True},
                {'name': 'calculation', 'description': 'Calculations', 'timeout': 120, 'required': True},
                {'name': 'cli', 'description': 'CLI tests', 'timeout': 90, 'required': True},
                {'name': 'plotting', 'description': 'Plotting tests', 'timeout': 90, 'required': True},
                {'name': 'export', 'description': 'Export tests', 'timeout': 45, 'required': True},
                {'name': 'eda', 'description': 'EDA tests', 'timeout': 60, 'required': True},
                {'name': 'interactive', 'description': 'Interactive tests', 'timeout': 60, 'required': True},
                {'name': 'integration', 'description': 'Integration tests', 'timeout': 120, 'required': True},
                {'name': 'mcp', 'description': 'MCP tests', 'timeout': 90, 'required': True},
                {'name': 'ml', 'description': 'ML tests', 'timeout': 180, 'required': True},
                {'name': 'docker', 'description': 'Docker tests', 'timeout': 120, 'required': True},
                {'name': 'native-container', 'description': 'Native container tests', 'timeout': 150, 'required': True},
                {'name': 'pocket_hedge_fund', 'description': 'Pocket hedge fund tests', 'timeout': 180, 'required': True},
                {'name': 'saas', 'description': 'SaaS tests', 'timeout': 120, 'required': True},
                {'name': 'scripts', 'description': 'Script tests', 'timeout': 90, 'required': True},
                {'name': 'workflow', 'description': 'Workflow tests', 'timeout': 60, 'required': True},
                {'name': 'e2e', 'description': 'E2E tests', 'timeout': 300, 'required': False}
            ],
            'global_settings': {
                'max_total_time': 3600,
                'stop_on_failure': True,
                'skip_empty_folders': True,
                'retry_failed': False,
                'cleanup_between_folders': True,
                'environment': {
                    'PYTHONPATH': '/app',
                    'PYTHONUNBUFFERED': '1',
                    'DOCKER_CONTAINER': 'true',
                    'MPLBACKEND': 'Agg',
                    'DISPLAY': '',
                    'UV_SYSTEM_PYTHON': '1'
                }
            },
            'folder_overrides': {},
            'dependencies': {}
        }
        
    def check_docker_environment(self) -> bool:
        """Check if we're running in Docker environment."""
        return (
            os.path.exists('/.dockerenv') or 
            os.environ.get('DOCKER_CONTAINER', False) or
            os.path.exists('/app')
        )
    
    def setup_environment(self):
        """Setup environment variables for Docker testing."""
        env = os.environ.copy()
        
        # Get environment variables from config
        config_env = self.global_settings.get('environment', {})
        env.update(config_env)
        
        return env
    
    def get_test_files_in_folder(self, folder_path: Path) -> List[Path]:
        """Get all test files in a folder."""
        if not folder_path.exists() or not folder_path.is_dir():
            return []
        
        test_files = []
        for file_path in folder_path.rglob('test_*.py'):
            if file_path.is_file():
                test_files.append(file_path)
        
        return sorted(test_files)
    
    def run_tests_in_folder(self, folder_config: Dict, env: Dict[str, str]) -> Tuple[bool, Dict]:
        """Run all tests in a specific folder."""
        folder_name = folder_config['name']
        folder_path = self.tests_root / folder_name
        
        if not folder_path.exists():
            if folder_config.get('required', True):
                logger.warning(f"Required test folder {folder_name} does not exist, skipping...")
            else:
                logger.info(f"Optional test folder {folder_name} does not exist, skipping...")
            return True, {'passed': 0, 'failed': 0, 'skipped': 0, 'errors': 0}
        
        test_files = self.get_test_files_in_folder(folder_path)
        
        if not test_files and self.global_settings.get('skip_empty_folders', True):
            logger.info(f"Test folder {folder_name} is empty, skipping...")
            return True, {'passed': 0, 'failed': 0, 'skipped': 0, 'errors': 0}
        
        logger.info(f"Running tests in folder: {folder_name} ({len(test_files)} files)")
        logger.info(f"Description: {folder_config.get('description', 'No description')}")
        
        # Get folder-specific settings
        folder_timeout = folder_config.get('timeout', 60)
        folder_maxfail = folder_config.get('maxfail', 1)
        
        # Apply folder overrides
        if folder_name in self.folder_overrides:
            overrides = self.folder_overrides[folder_name]
            folder_timeout = overrides.get('timeout', folder_timeout)
            folder_maxfail = overrides.get('maxfail', folder_maxfail)
        
        # Build pytest command for this folder
        cmd = [
            'uv', 'run', 'pytest',
            str(folder_path),
            '-c', 'pytest-docker.ini',
            '--tb=short',
            '--disable-warnings',
            '--no-header',
            '--no-summary',
            f'--maxfail={folder_maxfail}',
            f'--timeout={folder_timeout}',
            '--timeout-method=thread',
            '-v'
        ]
        
        logger.info(f"Command: {' '.join(cmd)}")
        logger.info(f"Timeout: {folder_timeout}s, Max failures: {folder_maxfail}")
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                env=env,
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=folder_timeout + 30  # Add 30s buffer to folder timeout
            )
            
            elapsed_time = time.time() - start_time
            
            # Parse results
            folder_results = self.parse_pytest_output(result.stdout, result.stderr)
            folder_results['time'] = elapsed_time
            
            if result.returncode == 0:
                logger.info(f"✅ Folder {folder_name} completed successfully in {elapsed_time:.2f}s")
                logger.info(f"   Passed: {folder_results['passed']}, "
                          f"Failed: {folder_results['failed']}, "
                          f"Skipped: {folder_results['skipped']}")
                return True, folder_results
            else:
                logger.error(f"❌ Folder {folder_name} failed in {elapsed_time:.2f}s")
                logger.error(f"   Passed: {folder_results['passed']}, "
                           f"Failed: {folder_results['failed']}, "
                           f"Skipped: {folder_results['skipped']}")
                if result.stderr:
                    logger.error(f"Error output: {result.stderr[:500]}...")
                return False, folder_results
                
        except subprocess.TimeoutExpired:
            elapsed_time = time.time() - start_time
            logger.error(f"⏰ Folder {folder_name} timed out after {elapsed_time:.2f}s")
            return False, {'passed': 0, 'failed': 0, 'skipped': 0, 'errors': 1, 'time': elapsed_time}
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"💥 Folder {folder_name} crashed: {str(e)}")
            return False, {'passed': 0, 'failed': 0, 'skipped': 0, 'errors': 1, 'time': elapsed_time}
    
    def parse_pytest_output(self, stdout: str, stderr: str) -> Dict:
        """Parse pytest output to extract test results."""
        results = {'passed': 0, 'failed': 0, 'skipped': 0, 'errors': 0}
        
        # Look for pytest summary line
        lines = stdout.split('\n')
        for line in lines:
            if 'passed' in line or 'failed' in line or 'skipped' in line:
                # Parse lines like "5 passed, 2 failed, 1 skipped"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.isdigit() and i < len(parts) - 1:
                        next_part = parts[i + 1]
                        if 'passed' in next_part:
                            results['passed'] += int(part)
                        elif 'failed' in next_part:
                            results['failed'] += int(part)
                        elif 'skipped' in next_part:
                            results['skipped'] += int(part)
        
        # Count errors from stderr
        if stderr and ('ERROR' in stderr or 'CRITICAL' in stderr):
            results['errors'] = 1
        
        return results
    
    def run_all_tests(self) -> bool:
        """Run all tests sequentially by folder."""
        if not self.check_docker_environment():
            logger.error("Not running in Docker environment!")
            return False
        
        logger.info("Starting sequential test execution in Docker environment")
        logger.info(f"Test folders to run: {', '.join(self.folder_names)}")
        
        env = self.setup_environment()
        overall_success = True
        start_time = time.time()
        
        # Check for maximum total time
        max_total_time = self.global_settings.get('max_total_time', 3600)
        stop_on_failure = self.global_settings.get('stop_on_failure', True)
        
        for i, folder_config in enumerate(self.test_folders, 1):
            folder_name = folder_config['name']
            
            # Check if we've exceeded maximum time
            elapsed_time = time.time() - start_time
            if elapsed_time > max_total_time:
                logger.warning(f"Maximum total time ({max_total_time}s) exceeded, stopping execution")
                break
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Running folder {i}/{len(self.test_folders)}: {folder_name}")
            logger.info(f"Description: {folder_config.get('description', 'No description')}")
            logger.info(f"Timeout: {folder_config.get('timeout', 60)}s")
            logger.info(f"{'='*60}")
            
            success, folder_results = self.run_tests_in_folder(folder_config, env)
            
            # Update overall results
            self.results['passed'] += folder_results['passed']
            self.results['failed'] += folder_results['failed']
            self.results['skipped'] += folder_results['skipped']
            self.results['errors'] += folder_results['errors']
            self.results['total_time'] += folder_results.get('time', 0)
            
            if not success:
                overall_success = False
                if stop_on_failure:
                    logger.error(f"Folder {folder_name} failed - stopping execution")
                    break
                else:
                    logger.warning(f"Folder {folder_name} failed - continuing with next folder")
            
            # Cleanup between folders if configured
            if self.global_settings.get('cleanup_between_folders', True):
                self.cleanup_between_folders()
        
        total_elapsed = time.time() - start_time
        self.results['total_time'] = total_elapsed
        
        # Print final summary
        self.print_summary(overall_success)
        
        return overall_success
    
    def cleanup_between_folders(self):
        """Perform cleanup between test folder executions."""
        try:
            # Clear pytest cache
            cache_dir = Path('/tmp/.pytest_cache')
            if cache_dir.exists():
                import shutil
                shutil.rmtree(cache_dir, ignore_errors=True)
            
            # Clear any temporary files
            temp_files = [
                '/tmp/test_*.py',
                '/tmp/*.log',
                '/tmp/*.tmp'
            ]
            
            for pattern in temp_files:
                for temp_file in Path('/tmp').glob(pattern.split('/')[-1]):
                    try:
                        temp_file.unlink()
                    except:
                        pass
                        
        except Exception as e:
            logger.debug(f"Cleanup warning: {e}")
    
    def print_summary(self, success: bool):
        """Print final test execution summary."""
        logger.info(f"\n{'='*60}")
        logger.info("FINAL TEST EXECUTION SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Total time: {self.results['total_time']:.2f}s")
        logger.info(f"Tests passed: {self.results['passed']}")
        logger.info(f"Tests failed: {self.results['failed']}")
        logger.info(f"Tests skipped: {self.results['skipped']}")
        logger.info(f"Errors: {self.results['errors']}")
        
        if success:
            logger.info("🎉 All test folders completed successfully!")
        else:
            logger.error("💥 Test execution failed!")
        
        logger.info(f"{'='*60}")

def main():
    """Main entry point."""
    runner = SequentialTestRunner()
    
    try:
        success = runner.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
