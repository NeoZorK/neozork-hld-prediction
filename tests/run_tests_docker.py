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
            
            # Parsing results
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'passed' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.isdigit() and i < len(parts) - 1 and parts[i+1] == 'passed':
                            passed_tests += int(part)
                        elif part.isdigit() and i < len(parts) - 1 and parts[i+1] == 'failed':
                            failed_tests += int(part)
                        elif part.isdigit() and i < len(parts) - 1 and parts[i+1] == 'skipped':
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
    
    # Test debug scripts
    for script in debug_scripts:
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
                if "No API keys" in result.stderr or "No API keys" in result.stdout:
                    error_reason = "❗ No API keys in environment"
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