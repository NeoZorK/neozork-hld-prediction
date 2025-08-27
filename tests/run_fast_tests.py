#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fast test runner for Docker environment.

This script runs only fast tests that are optimized for Docker environments
with limited resources and time constraints.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_fast_tests():
    """Run fast tests optimized for Docker environment."""
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Define fast test patterns
    fast_test_patterns = [
        "tests/eda/test_time_series_analysis_fast.py",
        "tests/test_visualization_manager_fast.py", 
        "tests/interactive/test_core_fast.py",
        "tests/eda/test_time_series_analysis.py::TestTimeSeriesAnalyzer::test_analyze_volatility",
        "tests/eda/test_time_series_analysis.py::TestTimeSeriesAnalyzer::test_comprehensive_analysis_basic",
        "tests/eda/test_time_series_analysis.py::TestTimeSeriesAnalyzer::test_comprehensive_analysis_no_data",
        "tests/eda/test_time_series_analysis.py::TestTimeSeriesAnalyzer::test_comprehensive_analysis_small_dataset",
        "tests/test_visualization_manager.py::TestVisualizationManager::test_create_statistics_plots_many_columns_basic",
        "tests/interactive/test_core.py::TestInteractiveSystem::test_run_feature_engineering_analysis"
    ]
    
    # Build pytest command with optimized settings for Docker
    cmd = [
        "uv", "run", "pytest",
        "-v",
        "--tb=short",
        "--disable-warnings",
        "--timeout=15",  # Reduced timeout for faster execution
        "--timeout-method=thread",
        "-n", "4",  # Limit to 4 parallel processes
        "--dist=worksteal",
        "--max-worker-restart=3",
        "--maxfail=5",
        "-W", "ignore"
    ]
    
    # Add test patterns
    cmd.extend(fast_test_patterns)
    
    print("Running fast tests optimized for Docker environment...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 80)
    
    try:
        # Run the tests
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print("\n" + "=" * 80)
            print("✅ All fast tests passed!")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("❌ Some fast tests failed!")
            print("=" * 80)
            
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error running tests: {e}")
        return 1


def run_specific_fast_tests():
    """Run specific fast tests that were failing in Docker."""
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Define the specific failing tests with optimizations
    specific_tests = [
        # Time series analysis tests
        "tests/eda/test_time_series_analysis_fast.py::TestTimeSeriesAnalyzerFast::test_analyze_volatility_fast",
        "tests/eda/test_time_series_analysis_fast.py::TestTimeSeriesAnalyzerFast::test_comprehensive_analysis_fast",
        
        # Visualization manager tests
        "tests/test_visualization_manager_fast.py::TestVisualizationManagerFast::test_create_statistics_plots_few_columns_basic_fast",
        
        # Interactive core tests
        "tests/interactive/test_core_fast.py::TestInteractiveSystemFast::test_run_feature_engineering_analysis_fast"
    ]
    
    # Build pytest command with very conservative settings
    cmd = [
        "uv", "run", "pytest",
        "-v",
        "--tb=short",
        "--disable-warnings",
        "--timeout=10",  # Very short timeout
        "--timeout-method=thread",
        "-n", "2",  # Very limited parallelism
        "--dist=worksteal",
        "--max-worker-restart=2",
        "--maxfail=3",
        "-W", "ignore"
    ]
    
    # Add test patterns
    cmd.extend(specific_tests)
    
    print("Running specific fast tests that were failing in Docker...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 80)
    
    try:
        # Run the tests
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print("\n" + "=" * 80)
            print("✅ All specific fast tests passed!")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("❌ Some specific fast tests failed!")
            print("=" * 80)
            
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error running tests: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--specific":
        exit_code = run_specific_fast_tests()
    else:
        exit_code = run_fast_tests()
    
    sys.exit(exit_code)
