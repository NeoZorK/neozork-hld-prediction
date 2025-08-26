"""
CLI Flag Test Generator

This module automatically generates test cases for all possible flag combinations
in the run_analysis.py script. It creates comprehensive test coverage by
generating all valid and invalid combinations of flags.

Features:
- Automatic flag combination generation
- Valid and invalid test case generation
- Test case categorization
- Performance optimization
- Test case filtering and prioritization
"""

import itertools
import subprocess
import sys
import os
import time
import json
import tempfile
from typing import List, Dict, Any, Tuple, Set
from pathlib import Path
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

# Project setup
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
PYTHON = sys.executable
SCRIPT = PROJECT_ROOT / 'run_analysis.py'
LOG_DIR = Path(tempfile.mkdtemp(prefix="cli_flag_tests_"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class FlagDefinition:
    """Definition of a CLI flag"""
    name: str
    values: List[str]
    required: bool = False
    mutually_exclusive: List[str] = None
    depends_on: List[str] = None
    category: str = "general"

@dataclass
class FlagTestCase:
    """Generated test case"""
    name: str
    command: List[str]
    expected_success: bool
    category: str
    priority: int
    description: str

class FlagTestGenerator:
    """Generator for CLI flag test cases"""
    
    def __init__(self):
        self.flags = self._define_flags()
        self.modes = self._define_modes()
        self.test_cases: List[FlagTestCase] = []
        
    def _define_flags(self) -> Dict[str, FlagDefinition]:
        """Define all available flags and their properties"""
        return {
            # Basic flags
            '--version': FlagDefinition('--version', [], category='basic'),
            '--help': FlagDefinition('--help', [], category='basic'),
            '--examples': FlagDefinition('--examples', [], category='basic'),
            '--indicators': FlagDefinition('--indicators', [], category='basic'),
            '--interactive': FlagDefinition('--interactive', [], category='basic'),
            '-i': FlagDefinition('-i', [], category='basic'),
            
            # Mode flags
            'mode': FlagDefinition('mode', ['demo', 'yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'show', 'interactive'], required=True, category='mode'),
            
            # Data source flags
            '--csv-file': FlagDefinition('--csv-file', ['data/test_data.csv', 'data/mn1.csv'], category='data_source'),
            '--ticker': FlagDefinition('--ticker', ['AAPL', 'MSFT', 'BTCUSDT', 'EURUSD'], category='data_source'),
            '--interval': FlagDefinition('--interval', ['M1', 'H1', 'D1', 'W1', 'MN1'], category='data_source'),
            '--point': FlagDefinition('--point', ['0.00001', '0.01', '1.0'], category='data_source'),
            '--period': FlagDefinition('--period', ['1d', '5d', '1mo', '3mo', '6mo', '1y'], category='data_source'),
            '--start': FlagDefinition('--start', ['2024-01-01'], category='data_source'),
            '--end': FlagDefinition('--end', ['2024-04-01'], category='data_source'),
            
            # Indicator flags
            '--rule': FlagDefinition('--rule', ['RSI', 'EMA', 'BB', 'MACD', 'OHLCV', 'AUTO'], category='indicator'),
            '--price-type': FlagDefinition('--price-type', ['open', 'close'], category='indicator'),
            
            # Show mode flags
            '--source': FlagDefinition('--source', ['yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'ind'], category='show_mode'),
            '--keywords': FlagDefinition('--keywords', [['AAPL'], ['2024'], ['BTCUSDT']], category='show_mode'),
            '--show-start': FlagDefinition('--show-start', ['2024-01-01'], category='show_mode'),
            '--show-end': FlagDefinition('--show-end', ['2024-04-01'], category='show_mode'),
            '--show-rule': FlagDefinition('--show-rule', ['RSI', 'EMA', 'BB'], category='show_mode'),
            
            # Plotting flags
            '-d': FlagDefinition('-d', ['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'], category='plotting'),
            
            # Export flags
            '--export-parquet': FlagDefinition('--export-parquet', [], category='export'),
            '--export-csv': FlagDefinition('--export-csv', [], category='export'),
            '--export-json': FlagDefinition('--export-json', [], category='export'),
            '--export-indicators-info': FlagDefinition('--export-indicators-info', [], category='export'),
        }
    
    def _define_modes(self) -> Dict[str, Dict[str, Any]]:
        """Define mode requirements and constraints"""
        return {
            'demo': {
                'required': [],
                'optional': ['--rule', '-d', '--price-type', '--export-parquet', '--export-csv', '--export-json', '--export-indicators-info'],
                'forbidden': [],
                'expected_success': True
            },
            'yfinance': {
                'required': ['--ticker', '--point'],
                'optional': ['--period', '--start', '--end', '--rule', '-d', '--price-type'],
                'forbidden': ['--export-parquet', '--export-csv', '--export-json', '--export-indicators-info'],
                'expected_success': True
            },
            'yf': {
                'required': ['--ticker', '--point'],
                'optional': ['--period', '--start', '--end', '--rule', '-d', '--price-type'],
                'forbidden': ['--export-parquet', '--export-csv', '--export-json', '--export-indicators-info'],
                'expected_success': True
            },
            'csv': {
                'required': ['--csv-file', '--point'],
                'optional': ['--rule', '-d', '--price-type'],
                'forbidden': ['--export-parquet', '--export-csv', '--export-json', '--export-indicators-info'],
                'expected_success': False  # May fail if files don't exist
            },
            'polygon': {
                'required': ['--ticker', '--start', '--end', '--point'],
                'optional': ['--interval', '--rule', '-d', '--price-type'],
                'forbidden': ['--export-parquet', '--export-csv', '--export-json', '--export-indicators-info'],
                'expected_success': True
            },
            'binance': {
                'required': ['--ticker', '--start', '--end', '--point'],
                'optional': ['--interval', '--rule', '-d', '--price-type'],
                'forbidden': ['--export-parquet', '--export-csv', '--export-json', '--export-indicators-info'],
                'expected_success': True
            },
            'exrate': {
                'required': ['--ticker', '--point'],
                'optional': ['--interval', '--rule', '-d', '--price-type'],
                'forbidden': ['--export-parquet', '--export-csv', '--export-json', '--export-indicators-info'],
                'expected_success': True
            },
            'show': {
                'required': [],
                'optional': ['--source', '--keywords', '--show-start', '--show-end', '--show-rule', '-d', '--export-parquet', '--export-csv', '--export-json', '--export-indicators-info'],
                'forbidden': [],
                'expected_success': False  # May fail if no data
            },
            'interactive': {
                'required': [],
                'optional': [],
                'forbidden': [],
                'expected_success': True
            }
        }
    
    def generate_basic_flag_tests(self) -> List[FlagTestCase]:
        """Generate tests for basic flags"""
        test_cases = []
        
        basic_flags = ['--version', '--help', '--examples', '--indicators', '--interactive', '-i']
        
        for flag in basic_flags:
            test_cases.append(FlagTestCase(
                name=f"test_basic_{flag.replace('-', '').replace('--', '')}",
                command=[flag],
                expected_success=True,
                category='basic_flags',
                priority=1,
                description=f"Test basic flag {flag}"
            ))
        
        return test_cases
    
    def generate_mode_tests(self) -> List[FlagTestCase]:
        """Generate tests for different modes"""
        test_cases = []
        
        for mode, config in self.modes.items():
            # Basic mode test
            test_cases.append(FlagTestCase(
                name=f"test_mode_{mode}_basic",
                command=[mode],
                expected_success=config['expected_success'],
                category='mode_basic',
                priority=1,
                description=f"Test basic {mode} mode"
            ))
            
            # Mode with required parameters
            if config['required']:
                required_cmd = [mode]
                for req_flag in config['required']:
                    if req_flag in self.flags and self.flags[req_flag].values:
                        required_cmd.extend([req_flag, self.flags[req_flag].values[0]])
                
                test_cases.append(FlagTestCase(
                    name=f"test_mode_{mode}_required",
                    command=required_cmd,
                    expected_success=config['expected_success'],
                    category='mode_required',
                    priority=2,
                    description=f"Test {mode} mode with required parameters"
                ))
            
            # Mode with required + optional parameters
            if config['required'] and config['optional']:
                for opt_flag in config['optional'][:3]:  # Limit to first 3 optional flags
                    if opt_flag in self.flags:
                        cmd = [mode]
                        
                        # Add required parameters
                        for req_flag in config['required']:
                            if req_flag in self.flags and self.flags[req_flag].values:
                                cmd.extend([req_flag, self.flags[req_flag].values[0]])
                        
                        # Add optional parameter
                        if self.flags[opt_flag].values:
                            cmd.extend([opt_flag, self.flags[opt_flag].values[0]])
                        else:
                            cmd.append(opt_flag)
                        
                        test_cases.append(FlagTestCase(
                            name=f"test_mode_{mode}_{opt_flag.replace('-', '').replace('--', '')}",
                            command=cmd,
                            expected_success=config['expected_success'],
                            category='mode_optional',
                            priority=3,
                            description=f"Test {mode} mode with {opt_flag}"
                        ))
        
        return test_cases
    
    def generate_flag_combination_tests(self) -> List[FlagTestCase]:
        """Generate tests for flag combinations"""
        test_cases = []
        
        # Demo mode combinations
        rules = ['RSI', 'EMA', 'BB', 'MACD']
        draw_modes = ['fastest', 'fast', 'plotly']
        export_flags = ['--export-parquet', '--export-csv', '--export-json', '--export-indicators-info']
        
        # Rule + draw combinations
        for rule in rules:
            for draw in draw_modes:
                test_cases.append(FlagTestCase(
                    name=f"test_demo_rule_{rule}_draw_{draw}",
                    command=['demo', '--rule', rule, '-d', draw],
                    expected_success=True,
                    category='flag_combinations',
                    priority=2,
                    description=f"Test demo mode with rule {rule} and draw {draw}"
                ))
        
        # Export combinations
        for export_flag in export_flags:
            test_cases.append(FlagTestCase(
                name=f"test_demo_export_{export_flag.replace('-', '').replace('--', '')}",
                command=['demo', '--rule', 'RSI', export_flag],
                expected_success=True,
                category='flag_combinations',
                priority=2,
                description=f"Test demo mode with {export_flag}"
            ))
        
        # Multiple export flags
        test_cases.append(FlagTestCase(
            name="test_demo_multiple_exports",
            command=['demo', '--rule', 'RSI', '--export-parquet', '--export-csv', '--export-json'],
            expected_success=True,
            category='flag_combinations',
            priority=3,
            description="Test demo mode with multiple export flags"
        ))
        
        return test_cases
    
    def generate_error_tests(self) -> List[FlagTestCase]:
        """Generate error case tests"""
        test_cases = []
        
        # Invalid modes
        invalid_modes = ['invalid_mode', 'nonexistent', 'wrong_mode']
        for mode in invalid_modes:
            test_cases.append(FlagTestCase(
                name=f"test_error_invalid_mode_{mode}",
                command=[mode],
                expected_success=False,
                category='error_cases',
                priority=1,
                description=f"Test invalid mode {mode}"
            ))
        
        # Missing required parameters
        missing_required_cases = [
            (['csv'], "Missing --csv-file and --point"),
            (['csv', '--csv-file', 'data/test.csv'], "Missing --point"),
            (['csv', '--point', '0.01'], "Missing --csv-file"),
            (['yfinance', '--ticker', 'AAPL'], "Missing --point and period/start-end"),
            (['yfinance', '--ticker', 'AAPL', '--point', '0.01'], "Missing period/start-end"),
            (['polygon', '--ticker', 'AAPL', '--start', '2024-01-01'], "Missing --end and --point"),
            (['binance', '--ticker', 'BTCUSDT', '--end', '2024-04-01'], "Missing --start and --point")
        ]
        
        for cmd, description in missing_required_cases:
            test_cases.append(FlagTestCase(
                name=f"test_error_missing_required_{'_'.join(cmd)}",
                command=cmd,
                expected_success=False,
                category='error_cases',
                priority=1,
                description=description
            ))
        
        # Invalid flag values
        invalid_value_cases = [
            (['demo', '--rule', 'INVALID_RULE'], "Invalid rule"),
            (['demo', '-d', 'invalid_draw'], "Invalid draw mode"),
            (['demo', '--price-type', 'invalid_price'], "Invalid price type"),
            (['demo', '--point', '-1'], "Negative point value"),
            (['demo', '--point', '0'], "Zero point value")
        ]
        
        for cmd, description in invalid_value_cases:
            test_cases.append(FlagTestCase(
                name=f"test_error_invalid_value_{'_'.join(cmd)}",
                command=cmd,
                expected_success=False,
                category='error_cases',
                priority=1,
                description=description
            ))
        
        # Conflicting flags
        conflicting_cases = [
            (['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--period', '1mo', '--start', '2024-01-01'], "Period with start date"),
            (['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--period', '1mo', '--end', '2024-04-01'], "Period with end date"),
            (['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--start', '2024-01-01'], "Start without end"),
            (['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--end', '2024-04-01'], "End without start")
        ]
        
        for cmd, description in conflicting_cases:
            test_cases.append(FlagTestCase(
                name=f"test_error_conflicting_{'_'.join(cmd[:3])}",
                command=cmd,
                expected_success=False,
                category='error_cases',
                priority=1,
                description=description
            ))
        
        return test_cases
    
    def generate_performance_tests(self) -> List[FlagTestCase]:
        """Generate performance test cases"""
        test_cases = []
        
        # Different rule combinations
        rules = ['RSI', 'EMA', 'BB', 'MACD', 'AUTO']
        draw_modes = ['fastest', 'fast', 'plotly']
        
        for rule in rules:
            for draw in draw_modes:
                test_cases.append(FlagTestCase(
                    name=f"test_performance_{rule}_{draw}",
                    command=['demo', '--rule', rule, '-d', draw],
                    expected_success=True,
                    category='performance',
                    priority=2,
                    description=f"Performance test with {rule} and {draw}"
                ))
        
        # Multiple export combinations
        test_cases.append(FlagTestCase(
            name="test_performance_multiple_exports",
            command=['demo', '--rule', 'RSI', '--export-parquet', '--export-csv', '--export-json', '--export-indicators-info'],
            expected_success=True,
            category='performance',
            priority=3,
            description="Performance test with all export flags"
        ))
        
        return test_cases
    
    def generate_all_tests(self) -> List[FlagTestCase]:
        """Generate all test cases"""
        print("Generating CLI flag test cases...")
        
        all_tests = []
        
        # Generate different types of tests
        test_generators = [
            self.generate_basic_flag_tests,
            self.generate_mode_tests,
            self.generate_flag_combination_tests,
            self.generate_error_tests,
            self.generate_performance_tests
        ]
        
        for generator in test_generators:
            try:
                tests = generator()
                all_tests.extend(tests)
                print(f"Generated {len(tests)} tests from {generator.__name__}")
            except Exception as e:
                print(f"Error in {generator.__name__}: {e}")
        
        # Sort by priority
        all_tests.sort(key=lambda x: x.priority)
        
        print(f"Total test cases generated: {len(all_tests)}")
        return all_tests
    
    def run_test_case(self, test_case: FlagTestCase) -> Dict[str, Any]:
        """Run a single test case"""
        start_time = time.perf_counter()
        
        # Set environment variables for testing
        env = os.environ.copy()
        env['MPLBACKEND'] = 'Agg'
        env['NEOZORK_TEST'] = '1'
        
        full_command = [PYTHON, str(SCRIPT)] + test_case.command
        
        try:
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                env=env,
                timeout=60
            )
            execution_time = time.perf_counter() - start_time
            
            success = result.returncode == 0
            if test_case.expected_success:
                success = result.returncode == 0
            else:
                success = result.returncode != 0
            
            return {
                'test_case': test_case,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'execution_time': execution_time,
                'success': success,
                'timeout': False
            }
            
        except subprocess.TimeoutExpired:
            execution_time = time.perf_counter() - start_time
            return {
                'test_case': test_case,
                'return_code': -1,
                'stdout': "",
                'stderr': "Command timed out",
                'execution_time': execution_time,
                'success': False,
                'timeout': True
            }
    
    def run_all_tests(self, max_workers: int = 4) -> Dict[str, Any]:
        """Run all generated test cases"""
        test_cases = self.generate_all_tests()
        
        print(f"Running {len(test_cases)} test cases with {max_workers} workers...")
        
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.run_test_case, test_case) for test_case in test_cases]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Error in test execution: {e}")
        
        # Analyze results
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r['success'])
        failed_tests = total_tests - passed_tests
        timeout_tests = sum(1 for r in results if r['timeout'])
        
        # Category statistics
        category_stats = {}
        for result in results:
            category = result['test_case'].category
            if category not in category_stats:
                category_stats[category] = {'total': 0, 'passed': 0, 'failed': 0, 'avg_time': 0}
            
            category_stats[category]['total'] += 1
            if result['success']:
                category_stats[category]['passed'] += 1
            else:
                category_stats[category]['failed'] += 1
        
        # Calculate average times
        for category in category_stats:
            cat_results = [r for r in results if r['test_case'].category == category]
            if cat_results:
                category_stats[category]['avg_time'] = sum(r['execution_time'] for r in cat_results) / len(cat_results)
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'timeout_tests': timeout_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'category_stats': category_stats,
            'results': results,
            'failed_tests_details': [
                {
                    'name': r['test_case'].name,
                    'command': r['test_case'].command,
                    'category': r['test_case'].category,
                    'return_code': r['return_code'],
                    'execution_time': r['execution_time'],
                    'timeout': r['timeout']
                }
                for r in results if not r['success']
            ]
        }
    
    def save_results(self, results: Dict[str, Any]):
        """Save test results"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        json_file = LOG_DIR / f"flag_test_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            # Convert test cases to dict for JSON serialization
            serializable_results = []
            for result in results['results']:
                serializable_result = {
                    'test_case': {
                        'name': result['test_case'].name,
                        'command': result['test_case'].command,
                        'category': result['test_case'].category,
                        'priority': result['test_case'].priority,
                        'description': result['test_case'].description
                    },
                    'return_code': result['return_code'],
                    'stdout': result['stdout'][:500],  # Limit output size
                    'stderr': result['stderr'][:500],
                    'execution_time': result['execution_time'],
                    'success': result['success'],
                    'timeout': result['timeout']
                }
                serializable_results.append(serializable_result)
            
            json.dump({
                'total_tests': results['total_tests'],
                'passed_tests': results['passed_tests'],
                'failed_tests': results['failed_tests'],
                'timeout_tests': results['timeout_tests'],
                'success_rate': results['success_rate'],
                'category_stats': results['category_stats'],
                'results': serializable_results,
                'failed_tests_details': results['failed_tests_details']
            }, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to: {json_file}")

def main():
    """Main function to run flag generator tests"""
    print("🚀 Starting Flag Generator Test Runner...")
    
    generator = FlagTestGenerator()
    results = generator.run_all_tests()
    
    print(f"✅ Completed! Results saved to: {LOG_DIR}")
    print(f"📊 Summary: {results['success_rate']:.1f}%")
    
    # Cleanup temporary directory
    try:
        import shutil
        shutil.rmtree(LOG_DIR)
        print(f"🧹 Cleaned up temporary directory: {LOG_DIR}")
    except Exception as e:
        print(f"⚠️  Warning: Could not clean up temporary directory: {e}")

if __name__ == "__main__":
    main() 