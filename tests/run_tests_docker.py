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
    
    # Run test files
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"\nRunning {test_file}...")
            result = subprocess.run([sys.executable, "-m", "pytest", test_file, "-v"], 
                                  capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"Errors: {result.stderr}")
        else:
            print(f"Test file not found: {test_file}")
    
    # Test debug scripts
    print("\n=== Testing Debug Scripts ===")
    for script in debug_scripts:
        if Path(script).exists():
            print(f"\nTesting {script}...")
            try:
                result = subprocess.run([sys.executable, script, "--help"], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"✅ {script} - OK")
                else:
                    print(f"❌ {script} - Failed: {result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"⏰ {script} - Timeout")
            except Exception as e:
                print(f"❌ {script} - Error: {e}")
        else:
            print(f"❌ {script} - Not found")

if __name__ == "__main__":
    run_docker_tests() 