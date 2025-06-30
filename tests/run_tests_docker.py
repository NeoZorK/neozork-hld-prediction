#!/usr/bin/env python3
"""
Run tests for Docker environment
"""

import os
import sys
import subprocess
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
            
            # Parse output to count results
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'passed' in line:
                    # Simple parsing: look for "X passed" pattern
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
                print("❌")
                if result.stderr:
                    print(f"  Error: {result.stderr.strip()}")
        else:
            print(f"❌ {test_file} - Not found")
    
    # Test debug scripts
    print("\n=== Testing Debug Scripts ===")
    debug_passed = 0
    debug_failed = 0
    
    for script in debug_scripts:
        if Path(script).exists():
            print(f"Testing {script}...", end=" ")
            try:
                result = subprocess.run([sys.executable, script, "--help"], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print("✅")
                    debug_passed += 1
                else:
                    print("❌")
                    debug_failed += 1
            except subprocess.TimeoutExpired:
                print("⏰")
                debug_failed += 1
            except Exception as e:
                print("❌")
                debug_failed += 1
        else:
            print(f"❌ {script} - Not found")
            debug_failed += 1
    
    # Summary
    print(f"\n=== Test Summary ===")
    print(f"Tests: {passed_tests} passed, {failed_tests} failed, {skipped_tests} skipped")
    print(f"Debug scripts: {debug_passed} passed, {debug_failed} failed")
    
    if failed_tests == 0 and debug_failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(run_docker_tests()) 