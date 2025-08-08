"""
Pytest-based Comprehensive CLI Flags Testing

This module provides pytest-based testing for all command line flags and their combinations
in the run_analysis.py script. It uses pytest fixtures and parametrization for efficient testing.

Features:
- Parametrized tests for all flags
- Fixtures for common test data
- Parallel execution support
- Detailed test reporting
- Integration with pytest-xdist for parallel testing
"""

import pytest
import subprocess
import sys
import os
import time
import json
from typing import List, Dict, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
import tempfile

# Project setup
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
PYTHON = sys.executable
SCRIPT = PROJECT_ROOT / 'run_analysis.py'
LOG_DIR = Path(tempfile.mkdtemp(prefix="cli_tests_pytest_"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Container detection
def is_container():
    """Check if running in container environment"""
    return (
        os.path.exists('/.dockerenv') or 
        os.environ.get('NATIVE_CONTAINER') == 'true' or
        os.environ.get('DOCKER_CONTAINER') == 'true'
    )

@dataclass
class CLITestCase:
    """Test case data structure for CLI testing"""
    name: str
    command: List[str]
    expected_return_code: int
    expected_output_contains: List[str] = None
    expected_error_contains: List[str] = None
    timeout: int = 30
    category: str = "general"

@pytest.fixture(scope="session")
def test_data():
    """Fixture providing test data for CLI tests"""
    return {
        'csv_file': 'data/test_data.csv',
        'ticker': 'AAPL',
        'point': '0.01',
        'interval': 'D1',
        'start_date': '2024-01-01',
        'end_date': '2024-04-01',
        'period': '1mo'
    }

@pytest.fixture(scope="session")
def all_flags():
    """Fixture providing all available CLI flags"""
    return {
        # Basic flags
        '--version': [],
        '--help': [],
        '--examples': [],
        '--indicators': [],
        '--interactive': [],
        '-i': [],
        
        # Data source flags
        '--csv-file': ['data/test_data.csv'],
        '--ticker': ['AAPL'],
        '--interval': ['M1', 'H1', 'D1', 'W1', 'MN1'],
        '--point': ['0.00001', '0.01', '1.0'],
        '--period': ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
        '--start': ['2024-01-01'],
        '--end': ['2024-04-01'],
        
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
        '--show-start': ['2024-01-01'],
        '--show-end': ['2024-04-01'],
        '--show-rule': ['RSI', 'EMA', 'BB'],
        
        # Plotting flags
        '-d': ['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'],
        '--draw-mode': ['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'],
        
        # Export flags
        '--export-parquet': [],
        '--export-csv': [],
        '--export-json': [],
        '--export-indicators-info': [],
        
        # Additional flags
        '--verbose': [],
        '--quiet': [],
        '--debug': [],
        '--no-cache': [],
        '--force': []
    }

@pytest.fixture(scope="session")
def modes_config():
    """Fixture providing mode configurations"""
    return {
        'demo': {
            'description': 'Demo mode with sample data',
            'required_flags': [],
            'optional_flags': ['--rule', '-d', '--export-parquet', '--export-csv', '--export-json']
        },
        'csv': {
            'description': 'CSV file processing mode',
            'required_flags': ['--csv-file', '--point'],
            'optional_flags': ['--rule', '-d', '--export-parquet', '--export-csv', '--export-json']
        },
        'yfinance': {
            'description': 'Yahoo Finance data mode',
            'required_flags': ['--ticker', '--point'],
            'optional_flags': ['--period', '--start', '--end', '--rule', '-d', '--export-parquet', '--export-csv', '--export-json']
        },
        'polygon': {
            'description': 'Polygon API data mode',
            'required_flags': ['--ticker', '--point'],
            'optional_flags': ['--period', '--start', '--end', '--rule', '-d', '--export-parquet', '--export-csv', '--export-json']
        },
        'binance': {
            'description': 'Binance API data mode',
            'required_flags': ['--ticker', '--point'],
            'optional_flags': ['--period', '--start', '--end', '--rule', '-d', '--export-parquet', '--export-csv', '--export-json']
        },
        'show': {
            'description': 'Show mode for data display',
            'required_flags': ['--source'],
            'optional_flags': ['--keywords', '--show-start', '--show-end', '--show-rule']
        }
    }

def run_cli_command(cmd: List[str], timeout: int = 30) -> Tuple[int, str, str, float]:
    """Run CLI command and return results"""
    start_time = time.time()
    
    try:
        # Use uv run for consistent environment
        full_cmd = ['uv', 'run', 'python', str(SCRIPT)] + cmd
        
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=PROJECT_ROOT,
            env=os.environ.copy()
        )
        
        execution_time = time.time() - start_time
        
        return (
            result.returncode,
            result.stdout,
            result.stderr,
            execution_time
        )
        
    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        return (1, "", f"Command timed out after {timeout}s", execution_time)
    except Exception as e:
        execution_time = time.time() - start_time
        return (1, "", str(e), execution_time)

@pytest.mark.basic
@pytest.mark.parametrize("flag", [
    '--version',
    '--help', 
    '--examples',
    '--indicators'
])
def test_basic_flags(flag):
    """Test basic CLI flags"""
    return_code, stdout, stderr, execution_time = run_cli_command([flag])
    
    assert return_code == 0, f"Flag {flag} failed with return code {return_code}"
    assert stdout, f"Flag {flag} produced no output"
    assert execution_time < 10, f"Flag {flag} took too long: {execution_time}s"

@pytest.mark.basic
def test_interactive_flag():
    """Test interactive flag"""
    return_code, stdout, stderr, execution_time = run_cli_command(['--interactive'])
    
    assert return_code == 0, f"Interactive flag failed with return code {return_code}"
    assert execution_time < 10, f"Interactive flag took too long: {execution_time}s"

@pytest.mark.basic
def test_short_interactive_flag():
    """Test short interactive flag"""
    return_code, stdout, stderr, execution_time = run_cli_command(['-i'])
    
    assert return_code == 0, f"Short interactive flag failed with return code {return_code}"
    assert execution_time < 10, f"Short interactive flag took too long: {execution_time}s"

@pytest.mark.basic
def test_version_flag():
    """Test version flag"""
    return_code, stdout, stderr, execution_time = run_cli_command(['--version'])
    
    assert return_code == 0, f"Version flag failed with return code {return_code}"
    assert 'version' in stdout.lower() or 'neozork' in stdout.lower(), f"Version output not found: {stdout}"
    assert execution_time < 5, f"Version flag took too long: {execution_time}s"

@pytest.mark.basic
def test_help_flag():
    """Test help flag"""
    return_code, stdout, stderr, execution_time = run_cli_command(['--help'])
    
    assert return_code == 0, f"Help flag failed with return code {return_code}"
    assert 'usage' in stdout.lower() or 'help' in stdout.lower(), f"Help output not found: {stdout}"
    assert execution_time < 5, f"Help flag took too long: {execution_time}s"

@pytest.mark.basic
def test_examples_flag():
    """Test examples flag"""
    return_code, stdout, stderr, execution_time = run_cli_command(['--examples'])
    
    assert return_code == 0, f"Examples flag failed with return code {return_code}"
    assert 'example' in stdout.lower() or 'usage' in stdout.lower(), f"Examples output not found: {stdout}"
    assert execution_time < 5, f"Examples flag took too long: {execution_time}s"

@pytest.mark.basic
@pytest.mark.parametrize("category", [
    'oscillators',
    'trend', 
    'momentum',
    'volatility',
    'volume'
])
def test_indicators_category_search(category):
    """Test indicators flag with category search"""
    return_code, stdout, stderr, execution_time = run_cli_command(['--indicators', category])
    
    assert return_code == 0, f"Indicators category {category} failed with return code {return_code}"
    assert category in stdout.lower(), f"Category {category} not found in output: {stdout}"
    assert execution_time < 10, f"Indicators category {category} took too long: {execution_time}s"

@pytest.mark.basic
@pytest.mark.parametrize("indicator", [
    'rsi',
    'ema', 
    'macd',
    'bollinger'
])
def test_indicators_specific_search(indicator):
    """Test indicators flag with specific indicator search"""
    return_code, stdout, stderr, execution_time = run_cli_command(['--indicators', indicator])
    
    assert return_code == 0, f"Indicators search {indicator} failed with return code {return_code}"
    assert indicator in stdout.lower(), f"Indicator {indicator} not found in output: {stdout}"
    assert execution_time < 10, f"Indicators search {indicator} took too long: {execution_time}s"

@pytest.mark.flag_combinations
@pytest.mark.parametrize("rule", [
    'RSI',
    'EMA', 
    'BB',
    'MACD',
    'OHLCV',
    'AUTO'
])
def test_demo_mode_rules(rule):
    """Test demo mode with different rules"""
    return_code, stdout, stderr, execution_time = run_cli_command(['demo', '--rule', rule])
    
    assert return_code == 0, f"Demo mode with rule {rule} failed with return code {return_code}"
    assert execution_time < 30, f"Demo mode with rule {rule} took too long: {execution_time}s"

@pytest.mark.flag_combinations
@pytest.mark.parametrize("draw_mode", [
    'fastest',
    'fast',
    'plotly'
])
def test_demo_mode_draw_modes(draw_mode):
    """Test demo mode with different draw modes"""
    return_code, stdout, stderr, execution_time = run_cli_command(['demo', '-d', draw_mode])
    
    assert return_code == 0, f"Demo mode with draw mode {draw_mode} failed with return code {return_code}"
    assert execution_time < 30, f"Demo mode with draw mode {draw_mode} took too long: {execution_time}s"

@pytest.mark.flag_combinations
@pytest.mark.parametrize("export_flag", [
    '--export-parquet',
    '--export-csv',
    '--export-json',
    '--export-indicators-info'
])
def test_demo_export_flags(export_flag):
    """Test demo mode with export flags"""
    return_code, stdout, stderr, execution_time = run_cli_command(['demo', export_flag])
    
    assert return_code == 0, f"Demo mode with export flag {export_flag} failed with return code {return_code}"
    assert execution_time < 30, f"Demo mode with export flag {export_flag} took too long: {execution_time}s"

@pytest.mark.flag_combinations
def test_csv_mode_valid(test_data):
    """Test CSV mode with valid parameters"""
    cmd = ['csv', '--csv-file', test_data['csv_file'], '--point', test_data['point']]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"CSV mode failed with return code {return_code}"
    assert execution_time < 30, f"CSV mode took too long: {execution_time}s"

@pytest.mark.error
@pytest.mark.parametrize("invalid_mode", [
    'invalid_mode',
    'nonexistent',
    'wrong'
])
def test_invalid_modes(invalid_mode):
    """Test invalid modes"""
    return_code, stdout, stderr, execution_time = run_cli_command([invalid_mode])
    
    assert return_code != 0, f"Invalid mode {invalid_mode} should have failed"
    assert execution_time < 10, f"Invalid mode {invalid_mode} took too long: {execution_time}s"

@pytest.mark.error
@pytest.mark.parametrize("test_case", [
    # Missing required parameters
    (['csv'], "Missing --csv-file and --point"),
    (['csv', '--csv-file', 'data/test.csv'], "Missing --point"),
    (['csv', '--point', '0.01'], "Missing --csv-file"),
    (['yfinance', '--ticker', 'AAPL'], "Missing --point and period/start-end"),
    (['yfinance', '--ticker', 'AAPL', '--point', '0.01'], "Missing period/start-end"),
    
    # Invalid flag values
    (['demo', '--rule', 'INVALID_RULE'], "Invalid rule"),
    (['demo', '-d', 'invalid_draw'], "Invalid draw mode"),
    (['demo', '--point', '-1'], "Negative point value"),
    (['demo', '--point', '0'], "Zero point value"),
])
def test_error_cases(test_case):
    """Test error cases"""
    cmd, expected_error = test_case
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code != 0, f"Error case should have failed: {cmd}"
    assert execution_time < 10, f"Error case took too long: {execution_time}s"

@pytest.mark.error
@pytest.mark.parametrize("conflicting_cmd", [
    ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--period', '1mo', '--start', '2024-01-01'],
    ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--period', '1mo', '--end', '2024-04-01'],
    ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--start', '2024-01-01'],
    ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--end', '2024-04-01'],
])
def test_conflicting_flags(conflicting_cmd):
    """Test conflicting flag combinations"""
    return_code, stdout, stderr, execution_time = run_cli_command(conflicting_cmd)
    
    assert return_code != 0, f"Conflicting flags should have failed: {conflicting_cmd}"
    assert execution_time < 10, f"Conflicting flags took too long: {execution_time}s"

@pytest.mark.flag_combinations
@pytest.mark.parametrize("source", [
    'yfinance',
    'yf',
    'csv',
    'polygon',
    'binance',
    'exrate',
    'ind'
])
def test_show_mode_sources(source):
    """Test show mode with different sources"""
    return_code, stdout, stderr, execution_time = run_cli_command(['show', '--source', source])
    
    assert return_code == 0, f"Show mode with source {source} failed with return code {return_code}"
    assert execution_time < 20, f"Show mode with source {source} took too long: {execution_time}s"

@pytest.mark.performance
def test_demo_mode_performance():
    """Test demo mode performance"""
    return_code, stdout, stderr, execution_time = run_cli_command(['demo'])
    
    assert return_code == 0, f"Demo mode failed with return code {return_code}"
    assert execution_time < 60, f"Demo mode took too long: {execution_time}s"

@pytest.mark.integration
def test_full_workflow_demo():
    """Test full workflow in demo mode"""
    cmd = ['demo', '--rule', 'RSI', '-d', 'fastest', '--export-csv']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Full workflow demo failed with return code {return_code}"
    assert execution_time < 60, f"Full workflow demo took too long: {execution_time}s"

@pytest.mark.performance
@pytest.mark.parametrize("rule", ['RSI', 'EMA', 'BB'])
@pytest.mark.parametrize("draw", ['fastest', 'fast'])
def test_multiple_combinations(rule, draw):
    """Test multiple flag combinations"""
    cmd = ['demo', '--rule', rule, '-d', draw]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Combination {rule}+{draw} failed with return code {return_code}"
    assert execution_time < 45, f"Combination {rule}+{draw} took too long: {execution_time}s"

@pytest.mark.slow
@pytest.mark.performance
def test_slow_operations():
    """Test slow operations"""
    cmd = ['demo', '--rule', 'AUTO', '-d', 'plotly']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd, timeout=120)
    
    assert return_code == 0, f"Slow operations failed with return code {return_code}"
    assert execution_time < 120, f"Slow operations took too long: {execution_time}s"

@pytest.mark.integration
def test_integration_with_export():
    """Test integration with export functionality"""
    cmd = ['demo', '--rule', 'RSI', '--export-parquet', '--export-csv', '--export-json']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Integration with export failed with return code {return_code}"
    assert execution_time < 60, f"Integration with export took too long: {execution_time}s"

@pytest.fixture
def validate_test_data(test_data):
    """Validate test data exists"""
    csv_file = Path(test_data['csv_file'])
    if not csv_file.exists():
        pytest.skip(f"Test data file not found: {csv_file}")
    return test_data

@pytest.mark.flag_combinations
def test_csv_mode_with_validation(validate_test_data):
    """Test CSV mode with data validation"""
    cmd = ['csv', '--csv-file', validate_test_data['csv_file'], '--point', validate_test_data['point']]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"CSV mode with validation failed with return code {return_code}"
    assert execution_time < 30, f"CSV mode with validation took too long: {execution_time}s"

def main():
    """Main function for standalone execution"""
    pytest.main([__file__, '-v', '--tb=short'])

if __name__ == "__main__":
    main() 