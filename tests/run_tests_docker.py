#!/usr/bin/env python3
"""
Run tests for Docker environment
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_docker_tests():
    """Run all Docker-specific tests"""
    
    # Test files to run
    test_files = [
        "tests/docker/test_uv_only_mode.py",
        "tests/docker/test_docker_tests.py", 
        "tests/docker/test_docker_config.py",
        "tests/native-container/test_native_container_full_functionality.py",
        "tests/native-container/test_container_setup.py",
        "tests/native-container/test_native_container_features.py",
        "tests/native-container/test_enhanced_shell.py"
    ]
    
    # Debug scripts to test
    debug_scripts = [
        "scripts/debug/debug_yfinance.py",
        "scripts/debug/debug_binance.py", 
        "scripts/debug/debug_polygon.py",
        "scripts/debug/examine_parquet.py"
    ]
    
    # Debug script tests (unit tests instead of running scripts)
    debug_script_tests = [
        "tests/test_debug_yfinance.py"
    ]
    
    print("=== Running Docker Tests ===")
    
    # Run test files with compact output
    passed_tests = 0
    failed_tests = 0
    skipped_tests = 0
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"Running {test_file}...", end=" ")
            result = subprocess.run([
                sys.executable, "-m", "pytest", test_file, 
                "--tb=no", "-q", "--disable-warnings"
            ], capture_output=True, text=True)
            
            # Analyze error reason
            error_reason = None
            if result.returncode != 0:
                if "not found" in result.stdout or "not found" in result.stderr:
                    error_reason = "❗ Important file not found"
                elif "API_KEY" in result.stdout or "API_KEY" in result.stderr:
                    error_reason = "❗ No API keys in environment"
                elif "Permission denied" in result.stdout or "Permission denied" in result.stderr:
                    error_reason = "❗ No file permissions"
                elif "No such file or directory" in result.stdout or "No such file or directory" in result.stderr:
                    error_reason = "❗ Required file not found"
                elif "ModuleNotFoundError" in result.stdout or "ModuleNotFoundError" in result.stderr:
                    error_reason = "❗ Module import error"
                elif "AssertionError" in result.stdout or "AssertionError" in result.stderr:
                    error_reason = "❗ AssertionError (see logs)"
                elif result.stderr.strip():
                    error_reason = result.stderr.strip().split('\n')[-1]
            
            # Parse output to count results
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                # Look for lines like "19 passed in 12.54s" or "3 passed, 1 failed in 2.34s"
                if 'passed' in line and any(word in line for word in ['failed', 'skipped', 'in']):
                    # Extract numbers from line
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.isdigit():
                            if i + 1 < len(parts) and parts[i + 1] == 'passed':
                                passed_tests += int(part)
                            elif i + 1 < len(parts) and parts[i + 1] == 'failed':
                                failed_tests += int(part)
                            elif i + 1 < len(parts) and parts[i + 1] == 'skipped':
                                skipped_tests += int(part)
                    break
            
            if result.returncode == 0:
                print("✅")
            else:
                print(f"❌{f' ({error_reason})' if error_reason else ''}")
        else:
            print(f"❌ {test_file} - Not found")
    
    # Test debug scripts with detailed output like v0.4.3
    print("\n=== Testing Debug Scripts ===")
    
    # First run unit tests for debug scripts (faster and more reliable)
    print("Running debug script unit tests...")
    for test_file in debug_script_tests:
        if Path(test_file).exists():
            print(f"Running {test_file}...", end=" ")
            result = subprocess.run([
                sys.executable, "-m", "pytest", test_file, 
                "--tb=no", "-q", "--disable-warnings"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅")
            else:
                print(f"❌ (Unit test failed)")
        else:
            print(f"❌ {test_file} - Not found")
    
    # Test debug scripts (only for non-interactive ones)
    print("\nTesting debug script execution...")
    for script in debug_scripts:
        # Skip interactive scripts in Docker
        if "debug_yfinance.py" in script:
            print(f"Testing {script}... ⏭️ (Skipped - using unit tests instead)")
            continue
            
        start_time = time.time()
        try:
            result = subprocess.run(
                [sys.executable, script],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=project_root
            )
            elapsed = time.time() - start_time
            
            if result.returncode == 0:
                print(f"Testing {script}... ✅ ({elapsed:.2f}s)")
            else:
                # Analyze error reason
                error_reason = "❗ Unknown error"
                
                if "BINANCE_API_KEY" in result.stdout or "BINANCE_API_SECRET" in result.stdout:
                    error_reason = "❗ no API_KEY found on env file in path: /app/docker.env"
                elif "POLYGON_API_KEY" in result.stdout:
                    error_reason = "❗ no API_KEY found on env file in path: /app/docker.env"
                elif "No API keys" in result.stderr or "No API keys" in result.stdout:
                    error_reason = "❗ no API_KEY found on env file in path: /app/docker.env"
                elif "Permission denied" in result.stderr:
                    error_reason = "❗ No file permissions"
                elif "No such file" in result.stderr:
                    error_reason = "❗ Required file not found"
                elif "ImportError" in result.stderr:
                    error_reason = "❗ Module import error"
                elif "timeout" in result.stderr.lower():
                    error_reason = "⏰ (Rate Limit)"
                
                print(f"Testing {script}... ❌ ({error_reason})")
                
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            print(f"Testing {script}... ⏰ (Rate Limit)")
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"Testing {script}... ❌ (Error: {str(e)})")

if __name__ == "__main__":
    run_docker_tests() 