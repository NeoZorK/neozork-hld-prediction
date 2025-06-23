#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
from typing import List, Dict, Optional, Tuple
import logging
import time

# Setup logging
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "test_runner_docker.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE)
    ]
)
logger = logging.getLogger('test_runner_docker')

# Define test categories and their scripts (for Docker environment)
TEST_CATEGORIES = {
    "yfinance": {
        "description": "Yahoo Finance API tests",
        "scripts": [
            "scripts/debug_scripts/debug_yfinance.py"
        ]
    },
    "binance": {
        "description": "Binance API tests",
        "scripts": [
            "scripts/debug_scripts/debug_binance.py"
        ]
    },
    "polygon": {
        "description": "Polygon.io API tests",
        "scripts": [
            "scripts/debug_scripts/debug_polygon.py"
        ]
    },
    "parquet": {
        "description": "Parquet file operations tests",
        "scripts": [
            "scripts/debug_scripts/examine_parquet.py"
        ]
    }
}

def print_colored(text: str, color_code: int = 0) -> None:
    """Print colored text to terminal."""
    colors = {
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
    }

    if isinstance(color_code, str) and color_code in colors:
        color_code = colors[color_code]

    print(f"\033[{color_code}m{text}\033[0m")

def print_header(title: str) -> None:
    """Print a formatted header."""
    separator = "=" * 60
    print("\n" + separator)
    print_colored(f"  {title.upper()}", 'cyan')
    print(separator + "\n")

def check_api_key(service: str) -> bool:
    """Check if API key for a service is present in environment."""
    env_vars = {
        'binance': ['BINANCE_API_KEY', 'BINANCE_API_SECRET'],
        'polygon': ['POLYGON_API_KEY', 'POLYGON_API_KEY_ID', 'POLYGON_API_SECRET'],
    }
    for var in env_vars.get(service, []):
        if os.environ.get(var):
            return True
    return False

def run_script(script_path: str, args: Optional[List[str]] = None, category: Optional[str] = None) -> bool:
    """
    Run a Python script with arguments.
    Args:
        script_path: Path to the script
        args: Optional arguments to pass to the script
        category: Optional test category (for API key check)
    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(script_path):
        logger.error(f"Script not found: {script_path}")
        if category in ("binance", "polygon"):
            if not check_api_key(category):
                print_colored(f"[INFO] {category.capitalize()} API key not found in environment. Please set the required API key(s) in your .env or docker.env file.", 'yellow')
        return False

    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)

    logger.info(f"Running: {' '.join(cmd)}")

    try:
        start_time = time.time()
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )

        # Print output in real-time
        for line in process.stdout:
            print(line, end='')

        # Wait for process to complete
        process.wait()
        elapsed_time = time.time() - start_time

        if process.returncode == 0:
            logger.info(f"Script completed successfully in {elapsed_time:.2f}s: {script_path}")
            return True
        else:
            # Collect stderr
            stderr_output = process.stderr.read()
            logger.error(f"Script failed with return code {process.returncode}: {script_path}")
            if stderr_output:
                logger.error(f"Error output: {stderr_output}")
            if category in ("binance", "polygon"):
                if not check_api_key(category):
                    print_colored(f"[INFO] {category.capitalize()} API key not found in environment. Please set the required API key(s) in your .env or docker.env file.", 'yellow')
            return False

    except Exception as e:
        logger.error(f"Error running script {script_path}: {str(e)}")
        if category in ("binance", "polygon"):
            if not check_api_key(category):
                print_colored(f"[INFO] {category.capitalize()} API key not found in environment. Please set the required API key(s) in your .env or docker.env file.", 'yellow')
        return False

def run_selected_tests(categories: List[str]) -> Dict[str, bool]:
    """Run selected test categories."""
    results = {}
    
    for category in categories:
        if category not in TEST_CATEGORIES:
            print(f"Warning: Unknown category '{category}'")
            continue
            
        info = TEST_CATEGORIES[category]
        print_header(f"Running {category} Tests")
        
        success = True
        for script in info['scripts']:
            if not run_script(script, category=category):
                success = False
                
        results[category] = success
        
        if success:
            print_colored(f"✅ {category} tests completed successfully", 'green')
        else:
            print_colored(f"❌ {category} tests failed", 'red')
    
    return results

def run_all_tests() -> Dict[str, bool]:
    """Run all tests."""
    results = {}
    
    for category, info in TEST_CATEGORIES.items():
        print_header(f"Running {category} Tests")
        
        success = True
        for script in info['scripts']:
            if not run_script(script, category=category):
                success = False
                
        results[category] = success
        
        if success:
            print_colored(f"✅ {category} tests completed successfully", 'green')
        else:
            print_colored(f"❌ {category} tests failed", 'red')
    
    return results

def print_summary(results: Dict[str, bool]) -> None:
    """Print test results summary."""
    print_header("Test Results Summary")
    
    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)
    failed_tests = total_tests - passed_tests
    
    print(f"Total test categories: {total_tests}")
    print_colored(f"Passed: {passed_tests}", 'green')
    print_colored(f"Failed: {failed_tests}", 'red')
    
    if failed_tests > 0:
        print("\nFailed test categories:")
        for category, success in results.items():
            if not success:
                print_colored(f"  - {category}", 'red')
    
    print(f"\nSuccess rate: {passed_tests/total_tests*100:.1f}%")

def main():
    """Main function for Docker environment."""
    parser = argparse.ArgumentParser(description="Run various test categories in Docker environment")
    parser.add_argument("--categories", nargs="+", help="Test categories to run")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    if args.all:
        results = run_all_tests()
        print_summary(results)
    elif args.categories:
        results = run_selected_tests(args.categories)
        print_summary(results)
    else:
        # Default: run all tests
        print_colored("Running all external data feed tests in Docker environment...", 'cyan')
        results = run_all_tests()
        print_summary(results)

if __name__ == "__main__":
    main() 