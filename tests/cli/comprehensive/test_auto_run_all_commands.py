"""
Automatic CLI Command Runner and Tester

This module automatically runs all possible command combinations for run_analysis.py
and generates comprehensive reports. It's designed to catch regressions and ensure
all CLI functionality works correctly.

Features:
- Automatic command generation
- Parallel execution
- Detailed reporting
- Performance monitoring
- Regression detection
- HTML report generation
"""

import subprocess
import sys
import os
import time
import json
import csv
from datetime import datetime
from typing import List, Dict, Any, Tuple, Set
from pathlib import Path
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from collections import defaultdict
import tempfile

# Project setup
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
PYTHON = sys.executable
SCRIPT = PROJECT_ROOT / 'run_analysis.py'
LOG_DIR = Path(tempfile.mkdtemp(prefix="cli_auto_tests_"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class CommandResult:
    """Result of a command execution"""
    command: List[str]
    return_code: int
    stdout: str
    stderr: str
    execution_time: float
    timestamp: str
    success: bool
    category: str
    subcategory: str
    expected_failure: bool
    error_type: str = ""
    performance_rating: str = "normal"

class AutoCommandRunner:
    """Automatic command runner and tester"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.results: List[CommandResult] = []
        self.lock = threading.Lock()
        
        # Command categories and their configurations
        self.command_categories = {
            'basic_flags': {
                'commands': [
                    ['--version'],
                    ['--help'],
                    ['--examples'],
                    ['--indicators'],
                    ['--interactive'],
                    ['-i']
                ],
                'expected_success': True
            },
            'indicators_search': {
                'commands': [
                    ['--indicators'],
                    ['--indicators', 'oscillators'],
                    ['--indicators', 'trend'],
                    ['--indicators', 'momentum'],
                    ['--indicators', 'volatility'],
                    ['--indicators', 'volume'],
                    ['--indicators', 'oscillators', 'rsi'],
                    ['--indicators', 'oscillators', 'ema'],
                    ['--indicators', 'trend', 'macd'],
                    ['--indicators', 'volatility', 'bollinger']
                ],
                'expected_success': True
            },
            'demo_mode': {
                'commands': self._generate_demo_commands(),
                'expected_success': True
            },
            'csv_mode': {
                'commands': self._generate_csv_commands(),
                'expected_success': False  # May fail if files don't exist
            },
            'show_mode': {
                'commands': self._generate_show_commands(),
                'expected_success': False  # May fail if no data
            },
            'error_cases': {
                'commands': self._generate_error_commands(),
                'expected_success': False
            },
            'performance_tests': {
                'commands': self._generate_performance_commands(),
                'expected_success': True
            },
            'integration_tests': {
                'commands': self._generate_integration_commands(),
                'expected_success': True
            }
        }
    
    def _generate_demo_commands(self) -> List[List[str]]:
        """Generate demo mode commands with various combinations"""
        commands = []
        
        # Basic demo commands
        rules = ['RSI', 'EMA', 'BB', 'MACD', 'OHLCV', 'AUTO']
        draw_modes = ['fastest', 'fast', 'plotly']
        export_flags = ['--export-parquet', '--export-csv', '--export-json', '--export-indicators-info']
        
        # Single rule commands
        for rule in rules:
            commands.append(['demo', '--rule', rule])
        
        # Rule + draw mode combinations
        for rule in rules[:3]:  # Limit to first 3 rules
            for draw in draw_modes:
                commands.append(['demo', '--rule', rule, '-d', draw])
        
        # Export combinations
        for export_flag in export_flags:
            commands.append(['demo', '--rule', 'RSI', export_flag])
        
        # Multiple export flags
        commands.append(['demo', '--rule', 'RSI', '--export-parquet', '--export-csv'])
        commands.append(['demo', '--rule', 'RSI', '--export-parquet', '--export-csv', '--export-json'])
        
        # Price type combinations
        commands.append(['demo', '--rule', 'RSI', '--price-type', 'open'])
        commands.append(['demo', '--rule', 'RSI', '--price-type', 'close'])
        
        # Test invalid draw mode
        commands.append(['demo', '-d', 'invalid_draw'])
        
        return commands
    
    def _generate_csv_commands(self) -> List[List[str]]:
        """Generate CSV mode commands"""
        commands = []
        
        csv_files = ['data/test_data.csv', 'data/mn1.csv', 'mql5_feed/CSVExport_AAPL.NAS_PERIOD_D1.csv']
        points = ['0.01', '0.00001']
        rules = ['RSI', 'EMA', 'BB']
        draw_modes = ['fastest', 'fast']
        
        for csv_file in csv_files:
            for point in points:
                # Basic CSV command
                commands.append(['csv', '--csv-file', csv_file, '--point', point])
                
                # With rules
                for rule in rules:
                    commands.append(['csv', '--csv-file', csv_file, '--point', point, '--rule', rule])
                
                # With draw modes
                for draw in draw_modes:
                    commands.append(['csv', '--csv-file', csv_file, '--point', point, '--draw', draw])
        
        return commands
    
    def _generate_show_commands(self) -> List[List[str]]:
        """Generate show mode commands"""
        commands = []
        
        sources = ['yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'ind']
        keywords = ['AAPL', '2024', 'BTCUSDT']
        rules = ['RSI', 'EMA', 'BB']
        
        # Basic show commands
        for source in sources:
            commands.append(['show', '--source', source])
        
        # Show with keywords
        for source in sources[:3]:
            for keyword in keywords:
                commands.append(['show', '--source', source, '--keywords', keyword])
        
        # Show with rules
        for source in sources[:3]:
            for rule in rules:
                commands.append(['show', '--source', source, '--show-rule', rule])
        
        # Show with date filters
        commands.append(['show', '--source', 'yfinance', '--show-start', '2024-01-01', '--show-end', '2024-04-01'])
        
        return commands
    
    def _generate_error_commands(self) -> List[List[str]]:
        """Generate error case commands"""
        commands = []
        
        # Invalid modes
        commands.extend([
            ['invalid_mode'],
            ['nonexistent'],
            ['wrong_mode']
        ])
        
        # Missing required parameters
        commands.extend([
            ['csv'],
            ['csv', '--csv-file', 'data/test.csv'],
            ['csv', '--point', '0.01'],
            ['yfinance', '--ticker', 'AAPL'],
            ['yfinance', '--ticker', 'AAPL', '--point', '0.01'],
            ['polygon', '--ticker', 'AAPL', '--start', '2024-01-01'],
            ['binance', '--ticker', 'BTCUSDT', '--end', '2024-04-01']
        ])
        
        # Invalid flag values
        commands.extend([
            ['demo', '--rule', 'INVALID_RULE'],
            ['demo', '--draw', 'invalid_draw'],
            ['demo', '--price-type', 'invalid_price'],
            ['demo', '--point', '-1'],
            ['demo', '--point', '0']
        ])
        
        # Conflicting flags
        commands.extend([
            ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--period', '1mo', '--start', '2024-01-01'],
            ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--period', '1mo', '--end', '2024-04-01'],
            ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--start', '2024-01-01'],
            ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--end', '2024-04-01']
        ])
        
        # Export flags in forbidden modes
        commands.extend([
            ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--period', '1mo', '--export-parquet'],
            ['csv', '--csv-file', 'data/test.csv', '--point', '0.01', '--export-csv']
        ])
        
        return commands
    
    def _generate_performance_commands(self) -> List[List[str]]:
        """Generate performance test commands"""
        commands = []
        
        # Different rule combinations
        rules = ['RSI', 'EMA', 'BB', 'MACD', 'AUTO']
        draw_modes = ['fastest', 'fast', 'plotly']
        
        for rule in rules:
            for draw in draw_modes:
                commands.append(['demo', '--rule', rule, '-d', draw])
        
        # Multiple export combinations
        commands.append(['demo', '--rule', 'RSI', '--export-parquet', '--export-csv', '--export-json', '--export-indicators-info'])
        
        return commands
    
    def _generate_integration_commands(self) -> List[List[str]]:
        """Generate integration test commands"""
        commands = []
        
        # Full workflow tests
        commands.extend([
            ['demo', '--rule', 'RSI', '-d', 'fastest', '--export-parquet'],
            ['demo', '--rule', 'EMA', '-d', 'fast', '--export-csv'],
            ['demo', '--rule', 'BB', '-d', 'plotly', '--export-json'],
            ['demo', '--rule', 'AUTO', '-d', 'fastest', '--export-parquet', '--export-csv']
        ])
        
        return commands
    
    def run_command(self, command: List[str], category: str, subcategory: str, 
                   expected_success: bool) -> CommandResult:
        """Run a single command and return result"""
        start_time = time.perf_counter()
        timestamp = datetime.now().isoformat()
        
        # Set environment variables for testing
        env = os.environ.copy()
        env['MPLBACKEND'] = 'Agg'
        env['NEOZORK_TEST'] = '1'
        
        full_command = [PYTHON, str(SCRIPT)] + command
        
        try:
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                env=env,
                timeout=60  # 60 second timeout
            )
            execution_time = time.perf_counter() - start_time
            
            # Determine success
            success = result.returncode == 0
            if expected_success:
                success = result.returncode == 0
            else:
                success = result.returncode != 0
            
            # Determine error type
            error_type = ""
            if result.returncode != 0:
                if "Traceback" in result.stdout or "Traceback" in result.stderr:
                    error_type = "exception"
                elif "error" in result.stderr.lower():
                    error_type = "argument_error"
                else:
                    error_type = "other_error"
            
            # Determine performance rating
            performance_rating = "normal"
            if execution_time > 30:
                performance_rating = "slow"
            elif execution_time < 5:
                performance_rating = "fast"
            
            return CommandResult(
                command=command,
                return_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                execution_time=execution_time,
                timestamp=timestamp,
                success=success,
                category=category,
                subcategory=subcategory,
                expected_failure=not expected_success,
                error_type=error_type,
                performance_rating=performance_rating
            )
            
        except subprocess.TimeoutExpired:
            execution_time = time.perf_counter() - start_time
            return CommandResult(
                command=command,
                return_code=-1,
                stdout="",
                stderr="Command timed out after 60 seconds",
                execution_time=execution_time,
                timestamp=timestamp,
                success=False,
                category=category,
                subcategory=subcategory,
                expected_failure=not expected_success,
                error_type="timeout",
                performance_rating="timeout"
            )
    
    def run_all_commands(self) -> Dict[str, Any]:
        """Run all command categories and return comprehensive results"""
        print("Starting automatic CLI command testing...")
        start_time = time.time()
        
        all_commands = []
        
        # Prepare all commands
        for category, config in self.command_categories.items():
            for i, command in enumerate(config['commands']):
                all_commands.append((command, category, f"test_{i}", config['expected_success']))
        
        print(f"Total commands to test: {len(all_commands)}")
        
        # Run commands in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self.run_command, cmd, cat, subcat, expected)
                for cmd, cat, subcat, expected in all_commands
            ]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    with self.lock:
                        self.results.append(result)
                except Exception as e:
                    print(f"Error in command execution: {e}")
        
        # Analyze results
        total_time = time.time() - start_time
        analysis = self._analyze_results()
        analysis['total_time'] = total_time
        
        # Save results
        self._save_results(analysis)
        
        return analysis
    
    def _analyze_results(self) -> Dict[str, Any]:
        """Analyze test results and generate statistics"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - passed_tests
        
        # Category statistics
        category_stats = defaultdict(lambda: {'total': 0, 'passed': 0, 'failed': 0, 'avg_time': 0})
        
        for result in self.results:
            cat = result.category
            category_stats[cat]['total'] += 1
            if result.success:
                category_stats[cat]['passed'] += 1
            else:
                category_stats[cat]['failed'] += 1
        
        # Calculate average times
        for cat in category_stats:
            cat_results = [r for r in self.results if r.category == cat]
            if cat_results:
                category_stats[cat]['avg_time'] = sum(r.execution_time for r in cat_results) / len(cat_results)
        
        # Error analysis
        error_types = defaultdict(int)
        for result in self.results:
            if result.error_type:
                error_types[result.error_type] += 1
        
        # Performance analysis
        performance_stats = defaultdict(int)
        for result in self.results:
            performance_stats[result.performance_rating] += 1
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'category_stats': dict(category_stats),
            'error_types': dict(error_types),
            'performance_stats': dict(performance_stats),
            'failed_commands': [
                {
                    'command': r.command,
                    'category': r.category,
                    'return_code': r.return_code,
                    'error_type': r.error_type,
                    'execution_time': r.execution_time
                }
                for r in self.results if not r.success
            ]
        }
    
    def _save_results(self, analysis: Dict[str, Any]):
        """Save test results to various formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        json_file = LOG_DIR / f"cli_test_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        # Save detailed CSV results
        csv_file = LOG_DIR / f"cli_test_details_{timestamp}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Command', 'Category', 'Subcategory', 'Return Code', 'Success',
                'Execution Time', 'Error Type', 'Performance Rating', 'Timestamp'
            ])
            
            for result in self.results:
                writer.writerow([
                    ' '.join(result.command),
                    result.category,
                    result.subcategory,
                    result.return_code,
                    result.success,
                    f"{result.execution_time:.3f}",
                    result.error_type,
                    result.performance_rating,
                    result.timestamp
                ])
        
        # Save HTML report
        html_file = LOG_DIR / f"cli_test_report_{timestamp}.html"
        self._generate_html_report(analysis, html_file)
        
        print(f"Results saved to:")
        print(f"  JSON: {json_file}")
        print(f"  CSV: {csv_file}")
        print(f"  HTML: {html_file}")
    
    def _generate_html_report(self, analysis: Dict[str, Any], html_file: Path):
        """Generate HTML report"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>CLI Test Report - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; }}
        .category {{ margin: 20px 0; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }}
        .success {{ color: green; }}
        .failure {{ color: red; }}
        .warning {{ color: orange; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .progress-bar {{ width: 100%; background-color: #f0f0f0; border-radius: 5px; }}
        .progress {{ height: 20px; background-color: #4CAF50; border-radius: 5px; text-align: center; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>CLI Test Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p>Total Tests: {analysis['total_tests']}</p>
        <p>Success Rate: {analysis['success_rate']:.1f}%</p>
        <div class="progress-bar">
            <div class="progress" style="width: {analysis['success_rate']}%">
                {analysis['success_rate']:.1f}%
            </div>
        </div>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total Tests</td><td>{analysis['total_tests']}</td></tr>
            <tr><td>Passed Tests</td><td class="success">{analysis['passed_tests']}</td></tr>
            <tr><td>Failed Tests</td><td class="failure">{analysis['failed_tests']}</td></tr>
            <tr><td>Success Rate</td><td>{analysis['success_rate']:.1f}%</td></tr>
        </table>
    </div>
    
    <div class="category">
        <h2>Category Statistics</h2>
        <table>
            <tr><th>Category</th><th>Total</th><th>Passed</th><th>Failed</th><th>Success Rate</th><th>Avg Time (s)</th></tr>
"""
        
        for category, stats in analysis['category_stats'].items():
            success_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            html_content += f"""
            <tr>
                <td>{category}</td>
                <td>{stats['total']}</td>
                <td class="success">{stats['passed']}</td>
                <td class="failure">{stats['failed']}</td>
                <td>{success_rate:.1f}%</td>
                <td>{stats['avg_time']:.3f}</td>
            </tr>
"""
        
        html_content += """
        </table>
    </div>
    
    <div class="category">
        <h2>Error Analysis</h2>
        <table>
            <tr><th>Error Type</th><th>Count</th></tr>
"""
        
        for error_type, count in analysis['error_types'].items():
            html_content += f"""
            <tr><td>{error_type}</td><td class="failure">{count}</td></tr>
"""
        
        html_content += """
        </table>
    </div>
    
    <div class="category">
        <h2>Performance Analysis</h2>
        <table>
            <tr><th>Performance Rating</th><th>Count</th></tr>
"""
        
        for rating, count in analysis['performance_stats'].items():
            html_content += f"""
            <tr><td>{rating}</td><td>{count}</td></tr>
"""
        
        html_content += """
        </table>
    </div>
    
    <div class="category">
        <h2>Failed Commands</h2>
        <table>
            <tr><th>Command</th><th>Category</th><th>Return Code</th><th>Error Type</th><th>Time (s)</th></tr>
"""
        
        for failed in analysis['failed_commands'][:20]:  # Show first 20 failed commands
            html_content += f"""
            <tr>
                <td>{' '.join(failed['command'])}</td>
                <td>{failed['category']}</td>
                <td>{failed['return_code']}</td>
                <td>{failed['error_type']}</td>
                <td>{failed['execution_time']:.3f}</td>
            </tr>
"""
        
        if len(analysis['failed_commands']) > 20:
            html_content += f"""
            <tr><td colspan="5">... and {len(analysis['failed_commands']) - 20} more failed commands</td></tr>
"""
        
        html_content += """
        </table>
    </div>
</body>
</html>
"""
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

def main():
    """Main function to run all tests"""
    print("🚀 Starting Auto Command Runner...")
    
    runner = AutoCommandRunner(max_workers=4)
    results = runner.run_all_commands()
    
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