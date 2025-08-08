#!/usr/bin/env python3
"""
Safe Test Runner for Apple Native Container

This script provides a safe way to run tests in Apple native container
with fixes for segmentation faults, memory issues, and path problems.
"""

import os
import sys
import subprocess
import signal
import time
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import multiprocessing

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AppleContainerTestRunner:
    """Safe test runner for Apple native container"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.logs_dir = self.project_root / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        # Container-specific settings
        self.is_container = self._detect_container()
        self.max_workers = self._get_safe_worker_count()
        self.memory_limit = "2G" if self.is_container else "4G"
        
        # Test categories to run safely
        self.safe_test_categories = [
            "unit",
            "basic", 
            "indicators",
            "data",
            "export"
        ]
        
        # Test categories to skip in container
        self.skip_in_container = [
            "slow",
            "performance",
            "integration"
        ]
        
    def _detect_container(self) -> bool:
        """Detect if running in Apple native container"""
        return (
            os.path.exists('/.dockerenv') or 
            os.environ.get('NATIVE_CONTAINER') == 'true' or
            os.environ.get('DOCKER_CONTAINER') == 'true'
        )
    
    def _get_safe_worker_count(self) -> int:
        """Get safe number of workers for container"""
        if self.is_container:
            # Reduce workers in container to prevent memory issues
            return min(2, multiprocessing.cpu_count())
        return multiprocessing.cpu_count()
    
    def _setup_environment(self):
        """Setup environment for safe testing"""
        logger.info("Setting up environment for Apple native container...")
        
        # Set environment variables
        os.environ['PYTHONUNBUFFERED'] = '1'
        os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
        os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib-cache'
        os.environ['OMP_NUM_THREADS'] = '1'  # Prevent OpenMP issues
        os.environ['MKL_NUM_THREADS'] = '1'   # Prevent MKL issues
        
        # Create necessary directories
        dirs_to_create = [
            '/tmp/matplotlib-cache',
            '/tmp/pytest-cache',
            str(self.logs_dir)
        ]
        
        for dir_path in dirs_to_create:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        logger.info("Environment setup completed")
    
    def _get_test_command(self, test_path: str = "tests", 
                         categories: Optional[List[str]] = None,
                         exclude_categories: Optional[List[str]] = None) -> List[str]:
        """Generate safe pytest command"""
        
        cmd = [
            "uv", "run", "pytest",
            test_path,
            "-v",
            "--tb=short", 
            "--disable-warnings",
            "--color=yes",
            f"-n {self.max_workers}",
            "--maxfail=5",
            "--durations=10",
            "--junitxml=logs/test-results.xml",
            "--html=logs/test-report.html",
            "--self-contained-html"
        ]
        
        # Add markers for safe categories
        if categories:
            markers = " or ".join([f"mark.{cat}" for cat in categories])
            cmd.extend(["-m", markers])
        
        # Exclude problematic categories in container
        if self.is_container and exclude_categories:
            exclude_markers = " and ".join([f"not mark.{cat}" for cat in exclude_categories])
            cmd.extend(["-m", exclude_markers])
        
        # Additional safety options for container
        if self.is_container:
            cmd.extend([
                "--disable-pytest-warnings",
                "--no-header",
                "--no-summary",
                "--strict-markers"
            ])
        
        return cmd
    
    def _run_tests_with_timeout(self, cmd: List[str], timeout: int = 600) -> Dict[str, Any]:
        """Run tests with timeout and error handling"""
        
        logger.info(f"Running tests with command: {' '.join(cmd)}")
        
        try:
            # Set up process with timeout
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=os.environ.copy()
            )
            
            # Wait for completion with timeout
            stdout, stderr = process.communicate(timeout=timeout)
            
            return {
                'return_code': process.returncode,
                'stdout': stdout,
                'stderr': stderr,
                'success': process.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"Tests timed out after {timeout} seconds")
            process.kill()
            return {
                'return_code': -1,
                'stdout': '',
                'stderr': f'Tests timed out after {timeout} seconds',
                'success': False
            }
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            return {
                'return_code': -1,
                'stdout': '',
                'stderr': str(e),
                'success': False
            }
    
    def run_safe_tests(self) -> Dict[str, Any]:
        """Run tests safely in Apple native container"""
        
        logger.info("Starting safe test execution for Apple native container")
        
        # Setup environment
        self._setup_environment()
        
        # Run tests in stages to prevent memory issues
        results = {}
        
        # Stage 1: Basic tests
        logger.info("Stage 1: Running basic tests...")
        basic_cmd = self._get_test_command(
            categories=["basic", "unit"],
            exclude_categories=self.skip_in_container
        )
        results['basic'] = self._run_tests_with_timeout(basic_cmd, timeout=300)
        
        if not results['basic']['success']:
            logger.error("Basic tests failed, stopping execution")
            return results
        
        # Stage 2: Core functionality tests
        logger.info("Stage 2: Running core functionality tests...")
        core_cmd = self._get_test_command(
            categories=["indicators", "data", "export"],
            exclude_categories=self.skip_in_container
        )
        results['core'] = self._run_tests_with_timeout(core_cmd, timeout=400)
        
        # Stage 3: CLI tests (if not in container)
        if not self.is_container:
            logger.info("Stage 3: Running CLI tests...")
            cli_cmd = self._get_test_command(
                categories=["cli"],
                exclude_categories=self.skip_in_container
            )
            results['cli'] = self._run_tests_with_timeout(cli_cmd, timeout=300)
        
        # Stage 4: Plotting tests (with reduced parallelism)
        logger.info("Stage 4: Running plotting tests...")
        plotting_cmd = self._get_test_command(
            categories=["plotting"],
            exclude_categories=self.skip_in_container
        )
        # Reduce workers for plotting tests to prevent matplotlib issues
        plotting_cmd[plotting_cmd.index("-n") + 1] = "1"
        results['plotting'] = self._run_tests_with_timeout(plotting_cmd, timeout=500)
        
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate test execution report"""
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'container': self.is_container,
            'max_workers': self.max_workers,
            'results': results,
            'summary': {
                'total_stages': len(results),
                'successful_stages': sum(1 for r in results.values() if r['success']),
                'failed_stages': sum(1 for r in results.values() if not r['success'])
            }
        }
        
        # Save report
        report_path = self.logs_dir / f"apple_container_test_report_{int(time.time())}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return str(report_path)
    
    def cleanup(self):
        """Cleanup temporary files and processes"""
        logger.info("Cleaning up...")
        
        # Close matplotlib figures
        try:
            import matplotlib.pyplot as plt
            plt.close('all')
        except:
            pass
        
        # Clean temporary directories
        temp_dirs = ['/tmp/matplotlib-cache', '/tmp/pytest-cache']
        for temp_dir in temp_dirs:
            try:
                import shutil
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except:
                pass

def main():
    """Main entry point"""
    
    runner = AppleContainerTestRunner()
    
    try:
        logger.info("Starting Apple native container test runner...")
        
        # Run tests
        results = runner.run_safe_tests()
        
        # Generate report
        report_path = runner.generate_report(results)
        logger.info(f"Test report saved to: {report_path}")
        
        # Print summary
        successful = sum(1 for r in results.values() if r['success'])
        total = len(results)
        
        logger.info(f"Test execution completed: {successful}/{total} stages successful")
        
        if successful == total:
            logger.info("✅ All test stages passed!")
            return 0
        else:
            logger.error("❌ Some test stages failed!")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Test execution interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    finally:
        runner.cleanup()

if __name__ == "__main__":
    sys.exit(main())
