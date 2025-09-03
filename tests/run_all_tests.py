#!/usr/bin/env python3
"""
Main test runner for Neozork HLD Prediction system.

This script runs all tests with proper configuration and reporting.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_tests_with_uv(test_type="all", parallel=True, coverage=True, verbose=False):
    """
    Run tests using uv with specified configuration.
    
    Args:
        test_type (str): Type of tests to run (all, unit, integration, performance)
        parallel (bool): Whether to run tests in parallel
        coverage (bool): Whether to generate coverage report
        verbose (bool): Whether to run with verbose output
    
    Returns:
        bool: True if all tests passed, False otherwise
    """
    # Base command
    cmd = ["uv", "run", "pytest"]
    
    # Add test type
    if test_type == "unit":
        cmd.append("tests/unit")
    elif test_type == "integration":
        cmd.append("tests/integration")
    elif test_type == "performance":
        cmd.append("tests/performance")
    else:
        cmd.append("tests")
    
    # Add parallel execution
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Add coverage
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])
    
    # Add verbose output
    if verbose:
        cmd.append("-v")
    
    # Add additional pytest options
    cmd.extend([
        "--tb=short",
        "--strict-markers",
        "--disable-warnings"
    ])
    
    print(f"Running tests with command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with return code: {e.returncode}")
        return False
    except FileNotFoundError:
        print("Error: uv command not found. Please install uv first.")
        return False


def run_specific_test_pattern(pattern, parallel=True, verbose=False):
    """
    Run tests matching a specific pattern.
    
    Args:
        pattern (str): Test pattern to match
        parallel (bool): Whether to run tests in parallel
        verbose (bool): Whether to run with verbose output
    
    Returns:
        bool: True if all tests passed, False otherwise
    """
    cmd = ["uv", "run", "pytest", pattern]
    
    if parallel:
        cmd.extend(["-n", "auto"])
    
    if verbose:
        cmd.append("-v")
    
    print(f"Running tests matching pattern: {pattern}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with return code: {e.returncode}")
        return False


def run_cli_tests():
    """Run CLI-specific tests to verify all flags work correctly."""
    print("Running CLI tests to verify all flags work...")
    
    cli_tests = [
        # Basic help and version
        (["--help"], "Help should be displayed"),
        (["--version"], "Version should be displayed"),
        
        # Command help
        (["analyze", "--help"], "Analyze command help should be displayed"),
        (["train", "--help"], "Train command help should be displayed"),
        (["predict", "--help"], "Predict command help should be displayed"),
        (["data", "--help"], "Data command help should be displayed"),
        (["help", "--help"], "Help command help should be displayed"),
        
        # Invalid commands
        (["invalid_command"], "Invalid command should show error"),
        (["analyze"], "Analyze without required args should show error"),
        (["train"], "Train without required args should show error"),
        (["predict"], "Predict without required args should show error"),
    ]
    
    all_passed = True
    
    for args, description in cli_tests:
        print(f"Testing: {description}")
        print(f"Command: neozork {' '.join(args)}")
        
        try:
            # Import and test CLI
            from src.cli.core.cli import CLI
            cli = CLI("test-cli")
            
            # Run with test arguments
            result = cli.run(args)
            
            if result == 0:
                print("✓ PASSED")
            else:
                print("✗ FAILED")
                all_passed = False
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
            all_passed = False
        
        print("-" * 50)
    
    return all_passed


def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description="Run Neozork HLD Prediction tests")
    
    parser.add_argument(
        "--type", 
        choices=["all", "unit", "integration", "performance"],
        default="all",
        help="Type of tests to run"
    )
    
    parser.add_argument(
        "--no-parallel",
        action="store_true",
        help="Disable parallel test execution"
    )
    
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Disable coverage reporting"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--cli-only",
        action="store_true",
        help="Run only CLI tests"
    )
    
    parser.add_argument(
        "--pattern",
        type=str,
        help="Run tests matching specific pattern"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Neozork HLD Prediction - Test Runner")
    print("=" * 60)
    
    if args.cli_only:
        print("Running CLI tests only...")
        success = run_cli_tests()
    elif args.pattern:
        print(f"Running tests matching pattern: {args.pattern}")
        success = run_specific_test_pattern(
            args.pattern,
            parallel=not args.no_parallel,
            verbose=args.verbose
        )
    else:
        print(f"Running {args.type} tests...")
        success = run_tests_with_uv(
            test_type=args.type,
            parallel=not args.no_parallel,
            coverage=not args.no_coverage,
            verbose=args.verbose
        )
    
    print("=" * 60)
    if success:
        print("✓ All tests PASSED successfully!")
        sys.exit(0)
    else:
        print("✗ Some tests FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main()
