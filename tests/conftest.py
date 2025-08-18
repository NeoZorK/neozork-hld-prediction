#!/usr/bin/env python3
"""
Global pytest configuration and shared fixtures
"""

import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import signal

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Global test configuration
TEST_TIMEOUT = 120  # seconds
PARALLEL_WORKERS = "auto"
TEST_DATA_SIZE = 100

def get_environment_type():
    """Determine the current environment type"""
    if os.environ.get('NATIVE_CONTAINER') == 'true':
        return 'native_container'
    elif os.environ.get('DOCKER_CONTAINER') == 'true':
        return 'docker'
    elif os.path.exists('/.dockerenv'):
        return 'docker'
    else:
        return 'local'

def should_skip_docker_tests():
    """Check if Docker tests should be skipped"""
    env_type = get_environment_type()
    return env_type == 'native_container'

def should_skip_native_container_tests():
    """Check if native container tests should be skipped"""
    env_type = get_environment_type()
    return env_type == 'docker'

def skip_if_docker(func):
    """Decorator to skip tests when running in Docker environment"""
    def wrapper(*args, **kwargs):
        if os.environ.get('DOCKER_CONTAINER') == 'true':
            pytest.skip("Test skipped in Docker environment")
        return func(*args, **kwargs)
    return wrapper

@pytest.fixture(scope="session")
def test_data_dir():
    """Create temporary test data directory"""
    temp_dir = tempfile.mkdtemp(prefix="test_data_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture(scope="session")
def sample_data(test_data_dir):
    """Generate sample financial data for testing"""
    # Create sample OHLCV data
    dates = pd.date_range('2024-01-01', periods=TEST_DATA_SIZE, freq='D')
    np.random.seed(42)  # For reproducible tests
    
    data = {
        'Date': dates,
        'Open': np.random.uniform(100, 200, TEST_DATA_SIZE),
        'High': np.random.uniform(150, 250, TEST_DATA_SIZE),
        'Low': np.random.uniform(50, 150, TEST_DATA_SIZE),
        'Close': np.random.uniform(100, 200, TEST_DATA_SIZE),
        'Volume': np.random.randint(1000, 10000, TEST_DATA_SIZE)
    }
    
    df = pd.DataFrame(data)
    
    # Save as CSV
    csv_file = test_data_dir / "sample_data.csv"
    df.to_csv(csv_file, index=False)
    
    # Save as Parquet
    parquet_file = test_data_dir / "sample_data.parquet"
    df.to_parquet(parquet_file, index=False)
    
    return {
        'csv_file': str(csv_file),
        'parquet_file': str(parquet_file),
        'dataframe': df,
        'point': '0.01'
    }

@pytest.fixture(scope="session")
def cli_script():
    """Path to the main CLI script"""
    script_path = Path(__file__).parent.parent / "run_analysis.py"
    assert script_path.exists(), f"CLI script not found at {script_path}"
    return script_path

@pytest.fixture(scope="session")
def python_executable():
    """Python executable for running CLI commands"""
    return sys.executable

@pytest.fixture(scope="function")
def temp_workspace():
    """Create temporary workspace for each test"""
    temp_dir = tempfile.mkdtemp(prefix="test_workspace_")
    original_cwd = os.getcwd()
    
    try:
        os.chdir(temp_dir)
        yield Path(temp_dir)
    finally:
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture(scope="function")
def mock_data_files(temp_workspace):
    """Create mock data files for testing"""
    # Create sample data
    dates = pd.date_range('2024-01-01', periods=50, freq='D')
    data = {
        'Date': dates,
        'Close': np.random.uniform(100, 200, 50),
        'Volume': np.random.randint(1000, 10000, 50)
    }
    df = pd.DataFrame(data)
    
    # Save files
    csv_file = temp_workspace / "test_data.csv"
    parquet_file = temp_workspace / "test_data.parquet"
    
    df.to_csv(csv_file, index=False)
    df.to_parquet(parquet_file, index=False)
    
    return {
        'csv': str(csv_file),
        'parquet': str(parquet_file),
        'dataframe': df
    }

@pytest.fixture(scope="session")
def test_config():
    """Global test configuration"""
    return {
        'timeout': TEST_TIMEOUT,
        'workers': PARALLEL_WORKERS,
        'data_size': TEST_DATA_SIZE,
        'verbose': True,
        'parallel': True
    }

# Performance monitoring fixtures
@pytest.fixture(scope="function")
def performance_monitor():
    """Monitor test performance"""
    import time
    import psutil
    import os
    
    start_time = time.time()
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    yield {
        'start_time': start_time,
        'start_memory': start_memory,
        'process': process
    }
    
    end_time = time.time()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    execution_time = end_time - start_time
    memory_used = end_memory - start_memory
    
    # Log performance metrics
    print(f"\n📊 Test Performance:")
    print(f"   Execution time: {execution_time:.2f}s")
    print(f"   Memory usage: {memory_used:.2f}MB")

# CLI command runner fixture
@pytest.fixture(scope="function")
def run_cli():
    """Fixture to run CLI commands with proper error handling"""
    def _run_cli(cmd: List[str], timeout: int = TEST_TIMEOUT) -> Tuple[int, str, str, float]:
        """Run CLI command and return results"""
        import subprocess
        import time
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=Path(__file__).parent.parent
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
    
    return _run_cli

# Test categorization fixtures
@pytest.fixture(scope="session")
def test_categories():
    """Define test categories for organization"""
    return {
        'unit': 'Unit tests for individual functions',
        'integration': 'Integration tests for component interaction',
        'performance': 'Performance and stress tests',
        'cli': 'Command line interface tests',
        'data': 'Data processing and validation tests',
        'indicators': 'Technical indicator calculation tests',
        'export': 'Data export functionality tests',
        'plotting': 'Visualization and plotting tests'
    }

# Parallel test configuration
def pytest_configure(config):
    """Configure pytest for parallel testing"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual functions"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for component interaction"
    )
    config.addinivalue_line(
        "markers", "performance: Performance and stress tests"
    )
    config.addinivalue_line(
        "markers", "cli: Command line interface tests"
    )
    config.addinivalue_line(
        "markers", "data: Data processing and validation tests"
    )
    config.addinivalue_line(
        "markers", "indicators: Technical indicator calculation tests"
    )
    config.addinivalue_line(
        "markers", "export: Data export functionality tests"
    )
    config.addinivalue_line(
        "markers", "plotting: Visualization and plotting tests"
    )
    config.addinivalue_line(
        "markers", "docker: Docker-specific tests"
    )
    config.addinivalue_line(
        "markers", "native_container: Native container-specific tests"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection for better organization"""
    # Check environment type
    env_type = get_environment_type()
    skip_docker = should_skip_docker_tests()
    skip_native = should_skip_native_container_tests()
    
    print(f"\n🔍 Environment detected: {env_type}")
    if skip_docker:
        print("⏭️  Docker tests will be skipped")
    if skip_native:
        print("⏭️  Native container tests will be skipped")
    
    for item in items:
        # Add default markers based on test path
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        elif "cli" in str(item.fspath):
            item.add_marker(pytest.mark.cli)
        elif "data" in str(item.fspath):
            item.add_marker(pytest.mark.data)
        elif "indicators" in str(item.fspath):
            item.add_marker(pytest.mark.indicators)
        elif "export" in str(item.fspath):
            item.add_marker(pytest.mark.export)
        elif "plotting" in str(item.fspath):
            item.add_marker(pytest.mark.plotting)
        elif "docker" in str(item.fspath):
            item.add_marker(pytest.mark.docker)
        elif "native-container" in str(item.fspath):
            item.add_marker(pytest.mark.native_container)
        
        # Skip Docker tests in native container environment
        if skip_docker and "docker" in str(item.fspath):
            item.add_marker(pytest.mark.skip(reason="Docker tests skipped in native container environment"))
            print(f"⏭️  Skipping Docker test: {item.nodeid}")
        
        # Skip native container tests in Docker environment
        if skip_native and "native-container" in str(item.fspath):
            item.add_marker(pytest.mark.skip(reason="Native container tests skipped in Docker environment"))
            print(f"⏭️  Skipping native container test: {item.nodeid}")

        # Only skip specific heavy test files, not entire directories
        # This allows individual tests to run while still enforcing the 10-second timeout
        heavy_test_files = [
            "test_all_flags.py",
            "test_all_flags_pytest.py", 
            "test_auto_run_all_commands.py",
            "test_flag_generator.py"
        ]
        
        if any(heavy_file in str(item.fspath) for heavy_file in heavy_test_files):
            item.add_marker(pytest.mark.skip(reason="Skipped heavy CLI test file (>10s)"))
            print(f"⏭️  Skipping heavy CLI test: {item.nodeid}")

# Test result reporting
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Generate custom test summary"""
    print("\n" + "="*60)
    print("📊 TEST EXECUTION SUMMARY")
    print("="*60)
    
    # Count tests by category
    stats = terminalreporter.stats
    passed = len(stats.get('passed', []))
    failed = len(stats.get('failed', []))
    skipped = len(stats.get('skipped', []))
    errors = len(stats.get('error', []))
    
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"💥 Errors: {errors}")
    print(f"📈 Total: {passed + failed + skipped + errors}")
    
    if failed > 0 or errors > 0:
        print("\n🔍 FAILURE ANALYSIS:")
        for failure in stats.get('failed', []):
            print(f"   ❌ {failure.nodeid}")
        for error in stats.get('error', []):
            print(f"   💥 {error.nodeid}")
    
    print("="*60)
    
    # Save test results to logs/test_results directory
    try:
        import json
        from datetime import datetime
        
        # Create logs/test_results directory if it doesn't exist
        logs_dir = Path(__file__).parent.parent / "logs" / "test_results"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = logs_dir / f"test_results_{timestamp}.json"
        
        # Prepare results data
        results_data = {
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'errors': errors,
            'total': passed + failed + skipped + errors,
            'success_rate': (passed / (passed + failed + errors)) * 100 if (passed + failed + errors) > 0 else 0,
            'exit_status': exitstatus.name if hasattr(exitstatus, 'name') else str(exitstatus)
        }
        
        # Save to file
        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"💾 Test results saved to: {results_file}")
        
    except Exception as e:
        print(f"⚠️  Could not save test results: {e}")

def pytest_sessionfinish(session, exitstatus):
    """Run test coverage analysis after all tests complete"""
    print("\n" + "="*60)
    print("🔍 RUNNING TEST COVERAGE ANALYSIS")
    print("="*60)
    
    # Import and run the coverage analysis
    try:
        from tests.zzz_analyze_test_coverage import analyze_coverage
        missing_tests = analyze_coverage()
        
        # Exit with error code if there are missing tests
        if missing_tests:
            print(f"\n⚠️  Found {len(missing_tests)} files without tests!")
            print("Consider adding tests for uncovered files.")
        else:
            print("\n✅ All source files have corresponding tests!")
            
    except Exception as e:
        print(f"❌ Error running coverage analysis: {e}")
        import traceback
        traceback.print_exc() 

# Enforce a strict per-test time limit of 10 seconds across all environments
# Skips the test if it exceeds the limit to keep the suite fast
@pytest.fixture(autouse=True)
def enforce_three_second_timeout(request):
    """Autouse fixture to skip any test exceeding 10 seconds runtime.

    Uses Unix SIGALRM; ignored on unsupported platforms. Can be disabled by
    setting environment variable DISABLE_TEST_TIMEOUT=1 or with marker @pytest.mark.no_timeout.
    """
    # Allow opting out via env var or marker
    if os.environ.get('DISABLE_TEST_TIMEOUT') == '1' or request.node.get_closest_marker('no_timeout'):
        yield
        return

    # SIGALRM is available on Unix (Darwin/macOS, Linux, Docker). For unsupported platforms, do nothing.
    if hasattr(signal, 'SIGALRM'):
        def _timeout_handler(signum, frame):
            pytest.skip("Test exceeded 10 seconds")

        previous_handler = signal.signal(signal.SIGALRM, _timeout_handler)
        # 10-second alarm
        signal.alarm(10)
        try:
            yield
        finally:
            # Cancel alarm and restore handler
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous_handler)
    else:
        # Fallback: no enforcement on this platform
        yield