#!/usr/bin/env python3
"""
Test runner script for Pocket Hedge Fund

This script provides a convenient way to run different types of tests
with proper configuration and reporting.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(command)}")
    print()
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ {description} failed with error: {e}")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run Pocket Hedge Fund tests")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "e2e", "all"], 
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Run tests with coverage reporting"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Run tests in verbose mode"
    )
    parser.add_argument(
        "--parallel", 
        action="store_true",
        help="Run tests in parallel"
    )
    parser.add_argument(
        "--pattern",
        help="Run tests matching pattern"
    )
    
    args = parser.parse_args()
    
    # Set up environment
    os.environ["PYTHONPATH"] = str(Path(__file__).parent.parent)
    os.environ["TESTING"] = "true"
    
    # Base pytest command
    base_cmd = ["python", "-m", "pytest"]
    
    # Add test type
    if args.type == "unit":
        base_cmd.extend(["unit/"])
    elif args.type == "integration":
        base_cmd.extend(["integration/"])
    elif args.type == "e2e":
        base_cmd.extend(["e2e/"])
    else:  # all
        base_cmd.extend(["."])
    
    # Add pattern if specified
    if args.pattern:
        base_cmd.extend(["-k", args.pattern])
    
    # Add coverage if requested
    if args.coverage:
        base_cmd.extend([
            "--cov=src.pocket_hedge_fund",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=80"
        ])
    
    # Add verbose mode
    if args.verbose:
        base_cmd.append("-v")
    
    # Add parallel execution
    if args.parallel:
        base_cmd.extend(["-n", "auto"])
    
    # Run tests
    success = run_command(base_cmd, f"Running {args.type} tests")
    
    if args.coverage and success:
        print(f"\n📊 Coverage report generated in htmlcov/index.html")
    
    # Summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
