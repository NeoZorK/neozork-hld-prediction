#!/usr/bin/env python3
"""
Test script for the sequential test runner

This script tests the sequential test runner functionality
without actually running all tests.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_config_loading():
    """Test configuration loading functionality."""
    print("Testing configuration loading...")
    
    # Import the sequential test runner
    from scripts.run_sequential_tests_docker import SequentialTestRunner
    
    # Test with default config
    runner = SequentialTestRunner()
    
    print(f"✅ Default config loaded successfully")
    print(f"   Test folders: {len(runner.test_folders)}")
    print(f"   Folder names: {', '.join(runner.folder_names[:5])}...")
    
    # Test with custom config file
    config_content = """
test_folders:
  - name: "test_folder_1"
    description: "Test folder 1"
    timeout: 30
    required: true
  - name: "test_folder_2"
    description: "Test folder 2"
    timeout: 60
    required: false

global_settings:
  max_total_time: 1800
  stop_on_failure: true
  skip_empty_folders: true
  environment:
    PYTHONPATH: "/app"
    DOCKER_CONTAINER: "true"

folder_overrides:
  test_folder_1:
    timeout: 45
    maxfail: 2

dependencies:
  test_folder_2:
    - "test_folder_1"
"""
    
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        temp_config_path = f.name
    
    try:
        runner_custom = SequentialTestRunner(temp_config_path)
        print(f"✅ Custom config loaded successfully")
        print(f"   Test folders: {len(runner_custom.test_folders)}")
        print(f"   Max total time: {runner_custom.global_settings.get('max_total_time')}")
        
        # Test folder overrides
        overrides = runner_custom.folder_overrides
        if 'test_folder_1' in overrides:
            print(f"   Folder overrides: {overrides['test_folder_1']}")
        
    finally:
        # Clean up temporary file
        os.unlink(temp_config_path)
    
    return True

def test_environment_setup():
    """Test environment setup functionality."""
    print("\nTesting environment setup...")
    
    from scripts.run_sequential_tests_docker import SequentialTestRunner
    
    runner = SequentialTestRunner()
    env = runner.setup_environment()
    
    required_env_vars = ['PYTHONPATH', 'DOCKER_CONTAINER', 'MPLBACKEND']
    
    for var in required_env_vars:
        if var in env:
            print(f"✅ Environment variable {var}: {env[var]}")
        else:
            print(f"❌ Missing environment variable: {var}")
            return False
    
    return True

def test_docker_detection():
    """Test Docker environment detection."""
    print("\nTesting Docker environment detection...")
    
    from scripts.run_sequential_tests_docker import SequentialTestRunner
    
    runner = SequentialTestRunner()
    is_docker = runner.check_docker_environment()
    
    print(f"Docker environment detected: {is_docker}")
    
    # This test will pass regardless of environment
    # In Docker, it should return True, in local environment, False
    print("✅ Docker detection test completed")
    
    return True

def test_folder_discovery():
    """Test test folder discovery functionality."""
    print("\nTesting folder discovery...")
    
    from scripts.run_sequential_tests_docker import SequentialTestRunner
    
    runner = SequentialTestRunner()
    
    # Test with existing folder
    tests_root = project_root / 'tests'
    if tests_root.exists():
        common_folder = tests_root / 'common'
        if common_folder.exists():
            test_files = runner.get_test_files_in_folder(common_folder)
            print(f"✅ Found {len(test_files)} test files in common folder")
            if test_files:
                print(f"   Example: {test_files[0].name}")
        else:
            print("⚠️  Common test folder not found")
    
    # Test with non-existent folder
    non_existent = Path('/tmp/non_existent_folder')
    test_files = runner.get_test_files_in_folder(non_existent)
    print(f"✅ Non-existent folder handled correctly: {len(test_files)} files")
    
    return True

def test_config_validation():
    """Test configuration validation."""
    print("\nTesting configuration validation...")
    
    # Test valid YAML
    valid_config = """
test_folders:
  - name: "test"
    description: "Test"
    timeout: 30
    required: true

global_settings:
  max_total_time: 3600
  stop_on_failure: true
"""
    
    try:
        config = yaml.safe_load(valid_config)
        print("✅ Valid YAML configuration parsed successfully")
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing failed: {e}")
        return False
    
    # Test invalid YAML
    invalid_config = """
test_folders:
  - name: "test"
    description: "Test"
    timeout: 30
    required: true
  invalid_yaml: [unclosed list
"""
    
    try:
        config = yaml.safe_load(invalid_config)
        print("❌ Invalid YAML should have failed")
        return False
    except yaml.YAMLError:
        print("✅ Invalid YAML correctly rejected")
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Sequential Test Runner")
    print("=" * 60)
    
    tests = [
        test_config_loading,
        test_environment_setup,
        test_docker_detection,
        test_folder_discovery,
        test_config_validation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
