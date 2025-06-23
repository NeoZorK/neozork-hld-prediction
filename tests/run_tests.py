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
LOG_FILE = os.path.join(LOG_DIR, "test_runner.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE)
    ]
)
logger = logging.getLogger('test_runner')

# Define test categories and their scripts
TEST_CATEGORIES = {
    "yfinance": {
        "description": "Yahoo Finance API tests",
        "scripts": [
            "scripts/debug_scripts/debug_yfinance.py"
        ],
        "docker_image": "neozork-yfinance"
    },
    "binance": {
        "description": "Binance API tests",
        "scripts": [
            "scripts/debug_scripts/debug_binance.py"
        ],
        "docker_image": "neozork-binance"
    },
    "polygon": {
        "description": "Polygon.io API tests",
        "scripts": [
            "scripts/debug_scripts/debug_polygon.py"
        ],
        "docker_image": "neozork-polygon"
    },
    "parquet": {
        "description": "Parquet file operations tests",
        "scripts": [
            "scripts/debug_scripts/examine_parquet.py"
        ],
        "docker_image": "neozork-parquet"
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

def run_script(script_path: str, args: Optional[List[str]] = None) -> bool:
    """
    Run a Python script with arguments.

    Args:
        script_path: Path to the script
        args: Optional arguments to pass to the script

    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(script_path):
        logger.error(f"Script not found: {script_path}")
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
            return False

    except Exception as e:
        logger.error(f"Error running script {script_path}: {str(e)}")
        return False

def run_docker_container(docker_image: str, script_path: str, args: Optional[List[str]] = None) -> bool:
    """
    Run a script inside a Docker container.

    Args:
        docker_image: Docker image name
        script_path: Path to the script (relative to project root)
        args: Optional arguments to pass to the script

    Returns:
        bool: True if successful, False otherwise
    """
    # Construct the docker run command
    cmd = ["docker", "run", "--rm", "-it"]  # Add -it flag for interactive mode

    # Map current directory to /app in container
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cmd.extend(["-v", f"{project_root}:/app"])

    # Add image name
    cmd.append(docker_image)

    # Add command to run inside container
    cmd.append("python")
    cmd.append(script_path)

    # Add arguments if provided
    if args:
        cmd.extend(args)

    logger.info(f"Running docker: {' '.join(cmd)}")

    try:
        # For interactive scripts like examine_parquet.py, we need to use system call directly
        # instead of subprocess.Popen to ensure proper interactive mode
        if "examine_parquet.py" in script_path:
            # Use os.system for truly interactive processes
            cmd_str = " ".join(cmd)
            start_time = time.time()
            logger.info(f"Executing interactive command: {cmd_str}")
            return_code = os.system(cmd_str)
            elapsed_time = time.time() - start_time

            if return_code == 0:
                logger.info(f"Docker run completed successfully in {elapsed_time:.2f}s: {docker_image}")
                return True
            else:
                logger.error(f"Docker run failed with return code {return_code}: {docker_image}")
                return False
        else:
            # For non-interactive scripts, use subprocess as before
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
                logger.info(f"Docker run completed successfully in {elapsed_time:.2f}s: {docker_image}")
                return True
            else:
                # Collect stderr
                stderr_output = process.stderr.read()
                logger.error(f"Docker run failed with return code {process.returncode}: {docker_image}")
                if stderr_output:
                    logger.error(f"Error output: {stderr_output}")
                return False

    except Exception as e:
        logger.error(f"Error running docker container {docker_image}: {str(e)}")
        return False

def prompt_for_tests() -> List[str]:
    """Prompt user to select test categories."""
    print_header("Available Test Categories")
    
    for i, (category, info) in enumerate(TEST_CATEGORIES.items(), 1):
        print(f"{i}. {category} - {info['description']}")
    
    print("\nEnter test categories to run (comma-separated, or 'all' for all tests):")
    user_input = input().strip().lower()
    
    if user_input == 'all':
        return list(TEST_CATEGORIES.keys())
    
    selected_categories = []
    for category in user_input.split(','):
        category = category.strip()
        if category in TEST_CATEGORIES:
            selected_categories.append(category)
        else:
            print(f"Warning: Unknown category '{category}'")
    
    return selected_categories

def prompt_for_tests_with_docker() -> List[Tuple[str, bool]]:
    """Prompt user to select test categories with Docker options."""
    print_header("Available Test Categories with Docker Options")
    
    for i, (category, info) in enumerate(TEST_CATEGORIES.items(), 1):
        print(f"{i}. {category} - {info['description']}")
    
    print("\nEnter test categories to run with Docker option (format: category:docker, e.g., 'binance:true,polygon:false'):")
    user_input = input().strip().lower()
    
    selected_categories = []
    for item in user_input.split(','):
        item = item.strip()
        if ':' in item:
            category, docker_str = item.split(':', 1)
            category = category.strip()
            use_docker = docker_str.strip() in ['true', '1', 'yes', 'y']
            
            if category in TEST_CATEGORIES:
                selected_categories.append((category, use_docker))
            else:
                print(f"Warning: Unknown category '{category}'")
        else:
            category = item.strip()
            if category in TEST_CATEGORIES:
                selected_categories.append((category, False))
            else:
                print(f"Warning: Unknown category '{category}'")
    
    return selected_categories

def prompt_for_individual_tests() -> List[str]:
    """Prompt user to select individual test scripts."""
    print_header("Available Test Scripts")
    
    all_scripts = []
    for category, info in TEST_CATEGORIES.items():
        for script in info['scripts']:
            all_scripts.append(script)
            print(f"{len(all_scripts)}. {script}")
    
    print("\nEnter script numbers to run (comma-separated):")
    user_input = input().strip()
    
    selected_scripts = []
    for num_str in user_input.split(','):
        try:
            num = int(num_str.strip()) - 1
            if 0 <= num < len(all_scripts):
                selected_scripts.append(all_scripts[num])
            else:
                print(f"Warning: Invalid script number {num + 1}")
        except ValueError:
            print(f"Warning: Invalid number '{num_str}'")
    
    return selected_scripts

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
            if not run_script(script):
                success = False
                
        results[category] = success
        
        if success:
            print_colored(f"✅ {category} tests completed successfully", 'green')
        else:
            print_colored(f"❌ {category} tests failed", 'red')
    
    return results

def run_selected_tests_with_docker(categories: List[Tuple[str, bool]]) -> Dict[str, bool]:
    """Run selected test categories with Docker options."""
    results = {}
    
    for category, use_docker in categories:
        if category not in TEST_CATEGORIES:
            print(f"Warning: Unknown category '{category}'")
            continue
            
        info = TEST_CATEGORIES[category]
        print_header(f"Running {category} Tests {'(Docker)' if use_docker else '(Local)'}")
        
        success = True
        for script in info['scripts']:
            if use_docker:
                if not run_docker_container(info['docker_image'], script):
                    success = False
            else:
                if not run_script(script):
                    success = False
                    
        results[category] = success
        
        if success:
            print_colored(f"✅ {category} tests completed successfully", 'green')
        else:
            print_colored(f"❌ {category} tests failed", 'red')
    
    return results

def run_tests_in_docker() -> Dict[str, bool]:
    """Run all tests in Docker containers."""
    results = {}
    
    for category, info in TEST_CATEGORIES.items():
        print_header(f"Running {category} Tests in Docker")
        
        success = True
        for script in info['scripts']:
            if not run_docker_container(info['docker_image'], script):
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
    """Main function."""
    parser = argparse.ArgumentParser(description="Run various test categories")
    parser.add_argument("--categories", nargs="+", help="Test categories to run")
    parser.add_argument("--docker", action="store_true", help="Run tests in Docker containers")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--individual", action="store_true", help="Select individual test scripts")
    
    args = parser.parse_args()
    
    if args.interactive:
        if args.individual:
            scripts = prompt_for_individual_tests()
            if scripts:
                print_header("Running Individual Scripts")
                for script in scripts:
                    run_script(script)
        else:
            if args.docker:
                categories = prompt_for_tests_with_docker()
                if categories:
                    results = run_selected_tests_with_docker(categories)
                    print_summary(results)
            else:
                categories = prompt_for_tests()
                if categories:
                    results = run_selected_tests(categories)
                    print_summary(results)
    else:
        if args.categories:
            if args.docker:
                categories = [(cat, True) for cat in args.categories]
                results = run_selected_tests_with_docker(categories)
            else:
                results = run_selected_tests(args.categories)
            print_summary(results)
        elif args.docker:
            results = run_tests_in_docker()
            print_summary(results)
        else:
            print("Please specify test categories or use --interactive mode")
            parser.print_help()

if __name__ == "__main__":
    main() 