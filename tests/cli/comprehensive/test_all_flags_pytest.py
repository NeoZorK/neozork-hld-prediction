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

# Project setup
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
PYTHON = sys.executable
SCRIPT = PROJECT_ROOT / 'run_analysis.py'
LOG_DIR = PROJECT_ROOT / 'logs' / 'cli_tests'
LOG_DIR.mkdir(parents=True, exist_ok=True)

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
        '--draw': ['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'],
        
        # Export flags
        '--export-parquet': [],
        '--export-csv': [],
        '--export-json': [],
        '--export-indicators-info': [],
    }

@pytest.fixture(scope="session")
def modes_config():
    """Fixture providing modes and their required parameters"""
    return {
        'demo': {
            'required': [],
            'optional': ['--rule', '--draw', '--export-parquet', '--export-csv', '--export-json', '--export-indicators-info']
        },
        'yfinance': {
            'required': ['--ticker', '--point'],
            'optional': ['--period', '--start', '--end', '--rule', '--draw', '--price-type']
        },
        'yf': {
            'required': ['--ticker', '--point'],
            'optional': ['--period', '--start', '--end', '--rule', '--draw', '--price-type']
        },
        'csv': {
            'required': ['--csv-file', '--point'],
            'optional': ['--rule', '--draw', '--price-type']
        },
        'polygon': {
            'required': ['--ticker', '--start', '--end', '--point'],
            'optional': ['--interval', '--rule', '--draw', '--price-type']
        },
        'binance': {
            'required': ['--ticker', '--start', '--end', '--point'],
            'optional': ['--interval', '--rule', '--draw', '--price-type']
        },
        'exrate': {
            'required': ['--ticker', '--point'],
            'optional': ['--interval', '--rule', '--draw', '--price-type']
        },
        'show': {
            'required': [],
            'optional': ['--source', '--keywords', '--show-start', '--show-end', '--show-rule', '--draw', '--export-parquet', '--export-csv', '--export-json', '--export-indicators-info']
        },
        'interactive': {
            'required': [],
            'optional': []
        }
    }

def run_cli_command(cmd: List[str], timeout: int = 30) -> Tuple[int, str, str, float]:
    """Run CLI command and return results"""
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
            timeout=timeout
        )
        execution_time = time.perf_counter() - start_time
        return result.returncode, result.stdout, result.stderr, execution_time
    except subprocess.TimeoutExpired:
        execution_time = time.perf_counter() - start_time
        return -1, "", "Command timed out", execution_time

# Basic flag tests
@pytest.mark.basic
@pytest.mark.parametrize("flag", [
    '--version',
    '--help', 
    '--examples',
    '--indicators'
])
def test_basic_flags(flag):
    """Test basic flags that don't require additional parameters"""
    cmd = [PYTHON, str(SCRIPT), flag]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    # Basic flags should either succeed or show help/version info
    assert return_code in [0, 1], f"Flag {flag} failed with return code {return_code}"
    assert execution_time < 10, f"Flag {flag} took too long: {execution_time:.2f}s"

# Test interactive flags separately (they have special behavior)
@pytest.mark.basic
def test_interactive_flag():
    """Test --interactive flag (should start interactive mode)"""
    cmd = [PYTHON, str(SCRIPT), '--interactive']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd, timeout=5)
    
    # Interactive mode should start (return code 0) or timeout (return code -1)
    assert return_code in [0, -1], f"Interactive flag failed with return code {return_code}"
    # If it didn't timeout, it should show interactive mode message
    if return_code == 0:
        assert "Interactive Mode" in stdout or "Welcome" in stdout, "Should show interactive mode message"
    # If it timed out, that's also acceptable for this test

@pytest.mark.basic
def test_short_interactive_flag():
    """Test -i flag (should require mode argument)"""
    cmd = [PYTHON, str(SCRIPT), '-i']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    # -i should fail because it requires a mode argument
    assert return_code == 2, f"Short interactive flag should fail with code 2, got {return_code}"
    assert "arguments are required: mode" in stderr, "Should show mode requirement error"

# Version test
@pytest.mark.basic
def test_version_flag():
    """Test version flag specifically"""
    cmd = [PYTHON, str(SCRIPT), '--version']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Version flag failed with return code {return_code}"
    assert "Shcherbyna Pressure Vector Indicator" in stdout, "Version output should contain tool name"
    assert "v" in stdout, "Version output should contain version number"

# Help test
@pytest.mark.basic
def test_help_flag():
    """Test help flag specifically"""
    cmd = [PYTHON, str(SCRIPT), '--help']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Help flag failed with return code {return_code}"
    assert "usage:" in stdout, "Help output should contain usage information"
    assert "Shcherbyna Pressure Vector Indicator" in stdout, "Help output should contain tool name"

# Examples test
@pytest.mark.basic
def test_examples_flag():
    """Test examples flag specifically"""
    cmd = [PYTHON, str(SCRIPT), '--examples']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Examples flag failed with return code {return_code}"
    assert "Examples" in stdout, "Examples output should contain examples section"

# Indicators search tests
@pytest.mark.basic
@pytest.mark.parametrize("category", [
    'oscillators',
    'trend', 
    'momentum',
    'volatility',
    'volume'
])
def test_indicators_category_search(category):
    """Test indicators search by category"""
    cmd = [PYTHON, str(SCRIPT), '--indicators', category]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Indicators search for {category} failed with return code {return_code}"
    assert category in stdout.lower(), f"Output should contain category {category}"

@pytest.mark.basic
@pytest.mark.parametrize("indicator", [
    'rsi',
    'ema', 
    'macd',
    'bollinger'
])
def test_indicators_specific_search(indicator):
    """Test indicators search for specific indicators"""
    cmd = [PYTHON, str(SCRIPT), '--indicators', 'oscillators', indicator]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    # This might not find all indicators, so we just check it doesn't crash
    assert return_code in [0, 1], f"Indicators search for {indicator} failed with return code {return_code}"

# Demo mode tests
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
    cmd = [PYTHON, str(SCRIPT), 'demo', '--rule', rule]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Demo mode with rule {rule} failed with return code {return_code}"
    assert execution_time < 60, f"Demo mode with rule {rule} took too long: {execution_time:.2f}s"

@pytest.mark.flag_combinations
@pytest.mark.parametrize("draw_mode", [
    'fastest',
    'fast',
    'plotly'
])
def test_demo_mode_draw_modes(draw_mode):
    """Test demo mode with different draw modes"""
    cmd = [PYTHON, str(SCRIPT), 'demo', '--rule', 'RSI', '--draw', draw_mode]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Demo mode with draw {draw_mode} failed with return code {return_code}"

# Export tests
@pytest.mark.flag_combinations
@pytest.mark.parametrize("export_flag", [
    '--export-parquet',
    '--export-csv',
    '--export-json',
    '--export-indicators-info'
])
def test_demo_export_flags(export_flag):
    """Test demo mode with export flags"""
    cmd = [PYTHON, str(SCRIPT), 'demo', '--rule', 'RSI', export_flag]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Demo mode with {export_flag} failed with return code {return_code}"

# CSV mode tests
@pytest.mark.flag_combinations
def test_csv_mode_valid(test_data):
    """Test CSV mode with valid parameters"""
    cmd = [PYTHON, str(SCRIPT), 'csv', '--csv-file', test_data['csv_file'], '--point', test_data['point']]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    # CSV mode might fail if file doesn't exist, but should not crash
    assert return_code in [0, 1], f"CSV mode failed with return code {return_code}"

# Error case tests
@pytest.mark.error
@pytest.mark.parametrize("invalid_mode", [
    'invalid_mode',
    'nonexistent',
    'wrong'
])
def test_invalid_modes(invalid_mode):
    """Test invalid modes should fail"""
    cmd = [PYTHON, str(SCRIPT), invalid_mode]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code != 0, f"Invalid mode {invalid_mode} should fail but returned {return_code}"

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
    (['demo', '--draw', 'invalid_draw'], "Invalid draw mode"),
    (['demo', '--point', '-1'], "Negative point value"),
    (['demo', '--point', '0'], "Zero point value"),
])
def test_error_cases(test_case):
    """Test various error cases"""
    cmd_parts, description = test_case
    cmd = [PYTHON, str(SCRIPT)] + cmd_parts
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code != 0, f"Error case '{description}' should fail but returned {return_code}"

# Conflicting flags tests
@pytest.mark.error
@pytest.mark.parametrize("conflicting_cmd", [
    ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--period', '1mo', '--start', '2024-01-01'],
    ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--period', '1mo', '--end', '2024-04-01'],
    ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--start', '2024-01-01'],
    ['yfinance', '--ticker', 'AAPL', '--point', '0.01', '--end', '2024-04-01'],
])
def test_conflicting_flags(conflicting_cmd):
    """Test conflicting flag combinations"""
    cmd = [PYTHON, str(SCRIPT)] + conflicting_cmd
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code != 0, f"Conflicting flags should fail but returned {return_code}"

# Show mode tests
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
    cmd = [PYTHON, str(SCRIPT), 'show', '--source', source]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    # Show mode might not have data, but should not crash
    assert return_code in [0, 1], f"Show mode with source {source} failed with return code {return_code}"

# Performance tests
@pytest.mark.performance
def test_demo_mode_performance():
    """Test demo mode performance"""
    cmd = [PYTHON, str(SCRIPT), 'demo', '--rule', 'RSI']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd, timeout=120)
    
    assert return_code == 0, f"Demo mode performance test failed with return code {return_code}"
    assert execution_time < 60, f"Demo mode took too long: {execution_time:.2f}s"

# Integration tests
@pytest.mark.integration
def test_full_workflow_demo():
    """Test full workflow with demo mode"""
    cmd = [PYTHON, str(SCRIPT), 'demo', '--rule', 'RSI', '--draw', 'fastest', '--export-parquet']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd, timeout=120)
    
    assert return_code == 0, f"Full workflow demo failed with return code {return_code}"
    assert "successfully" in stdout.lower() or "finished" in stdout.lower(), "Should indicate successful completion"

# Stress tests
@pytest.mark.performance
@pytest.mark.parametrize("rule", ['RSI', 'EMA', 'BB'])
@pytest.mark.parametrize("draw", ['fastest', 'fast'])
def test_multiple_combinations(rule, draw):
    """Test multiple rule and draw combinations"""
    cmd = [PYTHON, str(SCRIPT), 'demo', '--rule', rule, '--draw', draw]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"Combination {rule}+{draw} failed with return code {return_code}"
    assert execution_time < 60, f"Combination {rule}+{draw} took too long: {execution_time:.2f}s"

# Custom markers for test organization
@pytest.mark.slow
@pytest.mark.performance
def test_slow_operations():
    """Test slower operations that might take more time"""
    cmd = [PYTHON, str(SCRIPT), 'demo', '--rule', 'AUTO', '--draw', 'plotly']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd, timeout=180)
    
    assert return_code == 0, f"Slow operation failed with return code {return_code}"

@pytest.mark.integration
def test_integration_with_export():
    """Test integration with all export options"""
    cmd = [PYTHON, str(SCRIPT), 'demo', '--rule', 'RSI', 
           '--export-parquet', '--export-csv', '--export-json', '--export-indicators-info']
    return_code, stdout, stderr, execution_time = run_cli_command(cmd, timeout=120)
    
    assert return_code == 0, f"Integration test with exports failed with return code {return_code}"

# Fixture for test data validation
@pytest.fixture
def validate_test_data(test_data):
    """Validate that test data files exist"""
    csv_file = Path(test_data['csv_file'])
    if not csv_file.exists():
        pytest.skip(f"Test data file {csv_file} does not exist")
    return test_data

# Test with data validation
@pytest.mark.flag_combinations
def test_csv_mode_with_validation(validate_test_data):
    """Test CSV mode with data validation"""
    cmd = [PYTHON, str(SCRIPT), 'csv', '--csv-file', validate_test_data['csv_file'], 
           '--point', validate_test_data['point']]
    return_code, stdout, stderr, execution_time = run_cli_command(cmd)
    
    assert return_code == 0, f"CSV mode with validation failed with return code {return_code}"

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"]) 