"""
Comprehensive CLI Flags Testing Suite

This module provides comprehensive testing for all command line flags and their combinations
in the run_analysis.py script. It automatically tests all possible flag combinations and
validates their behavior.

Features:
- Tests all individual flags
- Tests flag combinations
- Validates error conditions
- Tests all modes and their required parameters
- Performance testing with timing
- Detailed logging and reporting
"""

import subprocess
import sys
import os
import time
import json
import pytest
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import tempfile

# Project setup
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
PYTHON = sys.executable
SCRIPT = PROJECT_ROOT / 'run_analysis.py'
LOG_DIR = Path(tempfile.mkdtemp(prefix="cli_tests_"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class CLITestResult:
    """Test result data structure"""
    command: List[str]
    return_code: int
    stdout: str
    stderr: str
    execution_time: float
    expected_failure: bool
    test_category: str
    test_name: str

class ComprehensiveCLITester:
    """Comprehensive CLI testing class for run_analysis.py"""
    
    def __init__(self):
        self.results: List[CLITestResult] = []
        self.test_data = {
            'csv_file': 'data/test_data.csv',
            'ticker': 'AAPL',
            'point': '0.01',
            'interval': 'D1',
            'start_date': '2024-01-01',
            'end_date': '2024-04-01',
            'period': '1mo'
        }
        
        # All available flags and their values
        self.all_flags = {
            # Basic flags
            '--version': [],
            '--help': [],
            '--examples': [],
            '--indicators': [],
            '--interactive': [],
            '-i': [],
            
            # Data source flags
            '--csv-file': [self.test_data['csv_file']],
            '--ticker': [self.test_data['ticker']],
            '--interval': ['M1', 'H1', 'D1', 'W1', 'MN1'],
            '--point': ['0.00001', '0.01', '1.0'],
            '--period': ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
            '--start': [self.test_data['start_date']],
            '--end': [self.test_data['end_date']],
            
            # Indicator flags
            '--rule': [
                'OHLCV', 'AUTO', 'PHLD', 'PV', 'SR', 'RSI', 'RSI_MOM', 'RSI_DIV', 
                'CCI', 'STOCH', 'EMA', 'BB', 'ATR', 'VWAP', 'PIVOT', 'MACD', 
                'STOCHOSC', 'HMA', 'TSF', 'MC', 'KELLY', 'FG', 'COT', 'PCR', 
                'DONCHAIN', 'FIBO', 'OBV', 'STDEV', 'ADX', 'SAR', 'SUPERTREND'
            ],
            '--price-type': ['open', 'close'],
            
            # Show mode flags
            '--source': ['yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'ind'],
            '--keywords': [['AAPL'], ['2024'], ['BTCUSDT']],
            '--show-start': [self.test_data['start_date']],
            '--show-end': [self.test_data['end_date']],
            '--show-rule': ['RSI', 'EMA', 'BB'],
            
            # Plotting flags
            '-d': ['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'],
            '--draw': ['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'],
            
            # Export flags
            '--export-parquet': [],
            '--export-csv': [],
            '--export-json': [],
            '--export-indicators-info': [],
        }
        
        # Modes and their required parameters
        self.modes = {
            'demo': {
                'required': [],
                'optional': ['--rule', '-d', '--export-parquet', '--export-csv', '--export-json', '--export-indicators-info']
            },
            'yfinance': {
                'required': ['--ticker', '--point'],
                'optional': ['--period', '--start', '--end', '--rule', '-d', '--price-type']
            },
            'yf': {
                'required': ['--ticker', '--point'],
                'optional': ['--period', '--start', '--end', '--rule', '-d', '--price-type']
            },
            'csv': {
                'required': ['--csv-file', '--point'],
                'optional': ['--rule', '-d', '--price-type']
            },
            'polygon': {
                'required': ['--ticker', '--start', '--end', '--point'],
                'optional': ['--interval', '--rule', '-d', '--price-type']
            },
            'binance': {
                'required': ['--ticker', '--start', '--end', '--point'],
                'optional': ['--interval', '--rule', '-d', '--price-type']
            },
            'exrate': {
                'required': ['--ticker', '--point'],
                'optional': ['--interval', '--rule', '-d', '--price-type']
            },
            'show': {
                'required': [],
                'optional': ['--source', '--keywords', '--show-start', '--show-end', '--show-rule', '-d', '--export-parquet', '--export-csv', '--export-json', '--export-indicators-info']
            },
            'interactive': {
                'required': [],
                'optional': []
            }
        }
        
        # Error test cases
        self.error_cases = [
            # Invalid modes
            ['invalid_mode'],
            ['nonexistent'],
            
            # Missing required parameters
            ['csv'],  # missing --csv-file and --point
            ['csv', '--csv-file', self.test_data['csv_file']],  # missing --point
            ['csv', '--point', self.test_data['point']],  # missing --csv-file
            ['yfinance', '--ticker', self.test_data['ticker']],  # missing --point and period/start-end
            ['yfinance', '--ticker', self.test_data['ticker'], '--point', self.test_data['point']],  # missing period/start-end
            ['polygon', '--ticker', self.test_data['ticker'], '--start', self.test_data['start_date']],  # missing --end and --point
            ['binance', '--ticker', self.test_data['ticker'], '--end', self.test_data['end_date']],  # missing --start and --point
            
            # Invalid flag values
            ['demo', '--rule', 'INVALID_RULE'],
            ['demo', '--draw', 'invalid_draw'],
            ['demo', '--price-type', 'invalid_price'],
            ['demo', '--point', '-1'],  # negative point
            ['demo', '--point', '0'],   # zero point
            
            # Conflicting flags
            ['yfinance', '--ticker', self.test_data['ticker'], '--point', self.test_data['point'], 
             '--period', '1mo', '--start', self.test_data['start_date']],  # period with start
            ['yfinance', '--ticker', self.test_data['ticker'], '--point', self.test_data['point'], 
             '--period', '1mo', '--end', self.test_data['end_date']],      # period with end
            ['yfinance', '--ticker', self.test_data['ticker'], '--point', self.test_data['point'], 
             '--start', self.test_data['start_date']],  # start without end
            ['yfinance', '--ticker', self.test_data['ticker'], '--point', self.test_data['point'], 
             '--end', self.test_data['end_date']],      # end without start
            
            # Export flags in forbidden modes
            ['yfinance', '--ticker', self.test_data['ticker'], '--point', self.test_data['point'], 
             '--period', '1mo', '--export-parquet'],
            ['csv', '--csv-file', self.test_data['csv_file'], '--point', self.test_data['point'], 
             '--export-csv'],
        ]

    def run_command(self, cmd: List[str], expected_failure: bool = False, 
                   test_category: str = "general", test_name: str = "") -> CLITestResult:
        """Run a single command and return test result"""
        start_time = time.perf_counter()
        
        # Set environment variables for testing
        env = os.environ.copy()
        env['MPLBACKEND'] = 'Agg'  # Non-interactive backend
        env['NEOZORK_TEST'] = '1'  # Test mode flag
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                env=env,
                timeout=30  # 30 second timeout
            )
        except subprocess.TimeoutExpired:
            return CLITestResult(
                command=cmd,
                return_code=-1,
                stdout="",
                stderr="Command timed out after 30 seconds",
                execution_time=30.0,
                expected_failure=expected_failure,
                test_category=test_category,
                test_name=test_name
            )
        
        execution_time = time.perf_counter() - start_time
        
        return CLITestResult(
            command=cmd,
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            execution_time=execution_time,
            expected_failure=expected_failure,
            test_category=test_category,
            test_name=test_name
        )

    def test_basic_flags(self) -> List[CLITestResult]:
        """Test basic flags that don't require additional parameters"""
        print("Testing basic flags...")
        results = []
        
        basic_flags = ['--version', '--help', '--examples', '--indicators', '--interactive', '-i']
        
        for flag in basic_flags:
            cmd = [PYTHON, str(SCRIPT), flag]
            result = self.run_command(cmd, test_category="basic_flags", test_name=f"test_{flag}")
            results.append(result)
            
        return results

    def test_mode_combinations(self) -> List[CLITestResult]:
        """Test all modes with their required and optional parameters"""
        print("Testing mode combinations...")
        results = []
        
        for mode, config in self.modes.items():
            # Test mode with only required parameters
            if config['required']:
                cmd = [PYTHON, str(SCRIPT), mode]
                for req_param in config['required']:
                    if req_param in self.all_flags:
                        cmd.extend([req_param, str(self.all_flags[req_param][0])])
                
                result = self.run_command(cmd, test_category="mode_required", test_name=f"test_{mode}_required")
                results.append(result)
            
            # Test mode with required + optional parameters
            if config['required'] and config['optional']:
                cmd = [PYTHON, str(SCRIPT), mode]
                
                # Add required parameters
                for req_param in config['required']:
                    if req_param in self.all_flags:
                        cmd.extend([req_param, str(self.all_flags[req_param][0])])
                
                # Add one optional parameter
                for opt_param in config['optional'][:3]:  # Limit to first 3 to avoid too many combinations
                    if opt_param in self.all_flags:
                        test_cmd = cmd + [opt_param, str(self.all_flags[opt_param][0])]
                        result = self.run_command(test_cmd, test_category="mode_optional", test_name=f"test_{mode}_{opt_param}")
                        results.append(result)
        
        return results

    def test_flag_combinations(self) -> List[CLITestResult]:
        """Test various flag combinations"""
        print("Testing flag combinations...")
        results = []
        
        # Test demo mode with different rule and draw combinations
        rules = ['RSI', 'EMA', 'BB', 'MACD']
        draw_modes = ['fastest', 'fast', 'plotly']
        
        for rule in rules:
            for draw in draw_modes:
                cmd = [PYTHON, str(SCRIPT), 'demo', '--rule', rule, '-d', draw]
                result = self.run_command(cmd, test_category="flag_combinations", test_name=f"test_demo_{rule}_{draw}")
                results.append(result)
        
        # Test export combinations
        export_flags = ['--export-parquet', '--export-csv', '--export-json', '--export-indicators-info']
        for export_flag in export_flags:
            cmd = [PYTHON, str(SCRIPT), 'demo', '--rule', 'RSI', export_flag]
            result = self.run_command(cmd, test_category="flag_combinations", test_name=f"test_demo_export_{export_flag}")
            results.append(result)
        
        # Test invalid draw mode
        cmd = [PYTHON, str(SCRIPT), 'demo', '-d', 'invalid_draw']
        result = self.run_command(cmd, test_category="flag_combinations", test_name="test_demo_invalid_draw")
        results.append(result)
        
        return results

    def test_error_cases(self) -> List[CLITestResult]:
        """Test error cases that should fail"""
        print("Testing error cases...")
        results = []
        
        for error_cmd in self.error_cases:
            cmd = [PYTHON, str(SCRIPT)] + error_cmd
            result = self.run_command(cmd, expected_failure=True, test_category="error_cases", test_name=f"test_error_{'_'.join(error_cmd)}")
            results.append(result)
        
        return results

    def test_indicators_search(self) -> List[CLITestResult]:
        """Test indicators search functionality"""
        print("Testing indicators search...")
        results = []
        
        # Test basic indicators listing
        cmd = [PYTHON, str(SCRIPT), '--indicators']
        result = self.run_command(cmd, test_category="indicators_search", test_name="test_indicators_list")
        results.append(result)
        
        # Test category search
        categories = ['oscillators', 'trend', 'momentum', 'volatility', 'volume']
        for category in categories:
            cmd = [PYTHON, str(SCRIPT), '--indicators', category]
            result = self.run_command(cmd, test_category="indicators_search", test_name=f"test_indicators_category_{category}")
            results.append(result)
        
        # Test specific indicator search
        indicators = ['rsi', 'ema', 'macd', 'bollinger']
        for indicator in indicators:
            cmd = [PYTHON, str(SCRIPT), '--indicators', 'oscillators', indicator]
            result = self.run_command(cmd, test_category="indicators_search", test_name=f"test_indicators_search_{indicator}")
            results.append(result)
        
        return results

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test categories and return comprehensive results"""
        print("Starting comprehensive CLI testing...")
        start_time = time.time()
        
        all_results = []
        
        # Run all test categories
        test_categories = [
            self.test_basic_flags,
            self.test_mode_combinations,
            self.test_flag_combinations,
            self.test_error_cases,
            self.test_indicators_search,
        ]
        
        for test_func in test_categories:
            try:
                results = test_func()
                all_results.extend(results)
            except Exception as e:
                print(f"Error in {test_func.__name__}: {e}")
        
        # Analyze results
        total_tests = len(all_results)
        passed_tests = 0
        failed_tests = 0
        error_tests = 0
        timeout_tests = 0
        
        category_stats = {}
        
        for result in all_results:
            # Categorize results
            if result.return_code == -1:
                timeout_tests += 1
            elif result.expected_failure and result.return_code != 0:
                passed_tests += 1
            elif not result.expected_failure and result.return_code == 0:
                passed_tests += 1
            else:
                failed_tests += 1
                if 'Traceback' in result.stdout or 'Traceback' in result.stderr:
                    error_tests += 1
            
            # Update category statistics
            if result.test_category not in category_stats:
                category_stats[result.test_category] = {'passed': 0, 'failed': 0, 'total': 0}
            
            category_stats[result.test_category]['total'] += 1
            if (result.expected_failure and result.return_code != 0) or (not result.expected_failure and result.return_code == 0):
                category_stats[result.test_category]['passed'] += 1
            else:
                category_stats[result.test_category]['failed'] += 1
        
        total_time = time.time() - start_time
        
        # Save detailed results
        self.save_results(all_results, category_stats, total_time)
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'error_tests': error_tests,
            'timeout_tests': timeout_tests,
            'total_time': total_time,
            'category_stats': category_stats,
            'results': all_results
        }

    def save_results(self, results: List[CLITestResult], category_stats: Dict, total_time: float):
        """Save test results to files"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save detailed log
        log_file = LOG_DIR / f"cli_test_detailed_{timestamp}.log"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"Comprehensive CLI Test Results - {timestamp}\n")
            f.write("=" * 60 + "\n\n")
            
            for result in results:
                f.write(f"Test: {result.test_name}\n")
                f.write(f"Category: {result.test_category}\n")
                f.write(f"Command: {' '.join(result.command)}\n")
                f.write(f"Return Code: {result.return_code}\n")
                f.write(f"Execution Time: {result.execution_time:.3f}s\n")
                f.write(f"Expected Failure: {result.expected_failure}\n")
                f.write(f"STDOUT: {result.stdout[:500]}\n")
                f.write(f"STDERR: {result.stderr[:500]}\n")
                f.write("-" * 40 + "\n\n")
        
        # Save summary
        summary_file = LOG_DIR / f"cli_test_summary_{timestamp}.json"
        summary = {
            'timestamp': timestamp,
            'total_tests': len(results),
            'category_stats': category_stats,
            'total_time': total_time,
            'failed_tests': [
                {
                    'name': r.test_name,
                    'category': r.test_category,
                    'command': r.command,
                    'return_code': r.return_code,
                    'stdout': r.stdout[:200],
                    'stderr': r.stderr[:200]
                }
                for r in results
                if (r.expected_failure and r.return_code == 0) or (not r.expected_failure and r.return_code != 0)
            ]
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"Detailed results saved to: {log_file}")
        print(f"Summary saved to: {summary_file}")

def main():
    """Main function to run all flag tests"""
    print("🚀 Starting Flag Test Runner...")
    
    runner = ComprehensiveCLITester()
    results = runner.run_all_tests()
    
    print(f"✅ Completed! Results saved to: {LOG_DIR}")
    print(f"📊 Summary: {results['summary']}")
    
    # Cleanup temporary directory
    try:
        import shutil
        shutil.rmtree(LOG_DIR)
        print(f"🧹 Cleaned up temporary directory: {LOG_DIR}")
    except Exception as e:
        print(f"⚠️  Warning: Could not clean up temporary directory: {e}")

if __name__ == "__main__":
    main() 