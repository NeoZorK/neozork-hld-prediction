#!/usr/bin/env python3
"""
Optimized test runner with parallel execution and comprehensive reporting
"""

import os
import sys
import time
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class OptimizedTestRunner:
    """Optimized test runner with parallel execution"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.project_root = project_root
        self.test_dir = project_root / "tests"
        self.results = {
            'start_time': None,
            'end_time': None,
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'errors': 0,
            'execution_time': 0,
            'parallel_workers': 0,
            'test_categories': {}
        }
    
    def run_tests(self, categories: Optional[List[str]] = None, 
                  markers: Optional[List[str]] = None,
                  parallel: bool = True,
                  workers: str = "auto",
                  verbose: bool = False) -> Dict[str, Any]:
        """Run tests with specified configuration"""
        
        print("🚀 Starting Optimized Test Runner")
        print("=" * 60)
        
        self.results['start_time'] = time.time()
        
        # Build pytest command
        cmd = self._build_pytest_command(categories, markers, parallel, workers, verbose)
        
        # Run tests
        success, output = self._execute_tests(cmd)
        
        # Parse results
        self._parse_results(output)
        
        # Generate report
        self._generate_report()
        
        return self.results
    
    def _build_pytest_command(self, categories: Optional[List[str]], 
                             markers: Optional[List[str]],
                             parallel: bool, workers: str, verbose: bool) -> List[str]:
        """Build pytest command with specified options"""
        
        cmd = [sys.executable, "-m", "pytest"]
        
        # Add test paths
        if categories:
            for category in categories:
                category_path = self.test_dir / category
                if category_path.exists():
                    cmd.append(str(category_path))
                else:
                    print(f"⚠️  Warning: Test category '{category}' not found")
        else:
            cmd.append(str(self.test_dir))
        
        # Add markers
        if markers:
            for marker in markers:
                cmd.extend(["-m", marker])
        
        # Add parallel execution
        if parallel:
            cmd.extend(["-n", workers])
        
        # Add output options
        if verbose:
            cmd.append("-v")
        else:
            cmd.extend(["-q", "--tb=short"])
        
        # Add additional options
        cmd.extend([
            "--strict-markers",
            "--disable-warnings",
            "--color=yes",
            "--durations=10"
        ])
        
        return cmd
    
    def _execute_tests(self, cmd: List[str]) -> tuple[bool, str]:
        """Execute pytest command and capture output"""
        
        print(f"🔧 Running command: {' '.join(cmd)}")
        print("-" * 60)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=self.config.get('timeout', 600)  # 10 minutes timeout
            )
            
            output = result.stdout + result.stderr
            success = result.returncode == 0
            
            return success, output
            
        except subprocess.TimeoutExpired:
            print("⏰ Test execution timed out")
            return False, "Test execution timed out"
        except Exception as e:
            print(f"💥 Error executing tests: {e}")
            return False, str(e)
    
    def _parse_results(self, output: str):
        """Parse pytest output to extract results"""
        
        self.results['end_time'] = time.time()
        self.results['execution_time'] = self.results['end_time'] - self.results['start_time']
        
        # Extract test counts from output
        lines = output.split('\n')
        for line in lines:
            if 'passed' in line and 'failed' in line:
                # Parse summary line like "3 passed, 1 failed, 2 skipped in 10.5s"
                parts = line.split(',')
                for part in parts:
                    part = part.strip()
                    if 'passed' in part:
                        self.results['passed'] = int(part.split()[0])
                    elif 'failed' in part:
                        self.results['failed'] = int(part.split()[0])
                    elif 'skipped' in part:
                        self.results['skipped'] = int(part.split()[0])
                    elif 'error' in part:
                        self.results['errors'] = int(part.split()[0])
                
                self.results['total_tests'] = (
                    self.results['passed'] + 
                    self.results['failed'] + 
                    self.results['skipped'] + 
                    self.results['errors']
                )
                break
    
    def _generate_report(self):
        """Generate comprehensive test report"""
        
        print("\n" + "=" * 60)
        print("📊 OPTIMIZED TEST RUNNER REPORT")
        print("=" * 60)
        
        # Basic statistics
        print(f"⏱️  Execution Time: {self.results['execution_time']:.2f}s")
        print(f"📈 Total Tests: {self.results['total_tests']}")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"⏭️  Skipped: {self.results['skipped']}")
        print(f"💥 Errors: {self.results['errors']}")
        
        # Calculate success rate
        if self.results['total_tests'] > 0:
            success_rate = (self.results['passed'] / self.results['total_tests']) * 100
            print(f"🎯 Success Rate: {success_rate:.1f}%")
        
        # Performance metrics
        if self.results['total_tests'] > 0:
            tests_per_second = self.results['total_tests'] / self.results['execution_time']
            print(f"⚡ Tests/Second: {tests_per_second:.2f}")
        
        # Status summary
        if self.results['failed'] == 0 and self.results['errors'] == 0:
            print("\n🎉 All tests passed successfully!")
        else:
            print(f"\n⚠️  {self.results['failed'] + self.results['errors']} tests failed")
        
        print("=" * 60)
    
    def save_results(self, output_file: str = "test_results.json"):
        """Save test results to JSON file"""
        
        results_file = self.project_root / output_file
        
        # Convert to serializable format
        serializable_results = {
            'start_time': self.results['start_time'],
            'end_time': self.results['end_time'],
            'execution_time': self.results['execution_time'],
            'total_tests': self.results['total_tests'],
            'passed': self.results['passed'],
            'failed': self.results['failed'],
            'skipped': self.results['skipped'],
            'errors': self.results['errors'],
            'parallel_workers': self.results['parallel_workers'],
            'test_categories': self.results['test_categories']
        }
        
        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"💾 Results saved to: {results_file}")

def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(description="Optimized Test Runner")
    parser.add_argument("--categories", nargs="+", 
                       help="Test categories to run (e.g., cli calculation data)")
    parser.add_argument("--markers", nargs="+",
                       help="Pytest markers to filter tests")
    parser.add_argument("--no-parallel", action="store_true",
                       help="Disable parallel execution")
    parser.add_argument("--workers", default="auto",
                       help="Number of parallel workers (default: auto)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    parser.add_argument("--save-results", action="store_true",
                       help="Save results to JSON file")
    parser.add_argument("--timeout", type=int, default=600,
                       help="Test timeout in seconds (default: 600)")
    
    args = parser.parse_args()
    
    # Configuration
    config = {
        'timeout': args.timeout,
        'parallel': not args.no_parallel,
        'workers': args.workers,
        'verbose': args.verbose
    }
    
    # Create runner
    runner = OptimizedTestRunner(config)
    
    # Run tests
    results = runner.run_tests(
        categories=args.categories,
        markers=args.markers,
        parallel=not args.no_parallel,
        workers=args.workers,
        verbose=args.verbose
    )
    
    # Save results if requested
    if args.save_results:
        runner.save_results()
    
    # Exit with appropriate code
    if results['failed'] > 0 or results['errors'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main() 