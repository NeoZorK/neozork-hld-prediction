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
    cmd = ["docker", "run", "--rm"]

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
    """Ask user which tests to run."""
    selected_tests = []

    print_header("Test Selection")
    print("Available test categories:")

    for i, (category, info) in enumerate(TEST_CATEGORIES.items(), 1):
        print(f"{i}. {category} - {info['description']}")

    print("\nFor each category, indicate if you want to run it (y/n):")

    for category, info in TEST_CATEGORIES.items():
        while True:
            response = input(f"Run {category} tests? (y/n): ").strip().lower()
            if response in ('y', 'n'):
                if response == 'y':
                    selected_tests.append(category)
                break
            else:
                print("Please enter 'y' or 'n'")

    return selected_tests

def prompt_for_tests_with_docker() -> List[Tuple[str, bool]]:
    """Ask user which tests to run and whether to use Docker for each."""
    selected_tests = []

    print_header("Test Selection")
    print("Available test categories:")

    for i, (category, info) in enumerate(TEST_CATEGORIES.items(), 1):
        print(f"{i}. {category} - {info['description']}")

    print("\nFor each category, indicate if you want to run it and whether to use Docker:")

    for category, info in TEST_CATEGORIES.items():
        while True:
            response = input(f"Run {category} tests? (y/n): ").strip().lower()
            if response in ('y', 'n'):
                if response == 'y':
                    use_docker = False
                    docker_response = input(f"Use Docker for {category}? (y/n): ").strip().lower()
                    if docker_response in ('y', 'n'):
                        use_docker = docker_response == 'y'
                    else:
                        print("Invalid response. Defaulting to not using Docker.")

                    selected_tests.append((category, use_docker))
                break
            else:
                print("Please enter 'y' or 'n'")

    return selected_tests

def run_selected_tests(categories: List[str]) -> Dict[str, bool]:
    """Run tests for selected categories."""
    results = {}

    for category in categories:
        if category in TEST_CATEGORIES:
            print_header(f"Running {category} Tests")

            category_success = True
            for script in TEST_CATEGORIES[category]["scripts"]:
                print_colored(f"Executing: {script}", 'yellow')
                success = run_script(script)
                if not success:
                    category_success = False

            results[category] = category_success

    return results

def run_selected_tests_with_docker(categories: List[Tuple[str, bool]]) -> Dict[str, bool]:
    """Run tests for selected categories, with optional Docker usage."""
    results = {}

    for category, use_docker in categories:
        if category in TEST_CATEGORIES:
            print_header(f"Running {category} Tests (Docker: {'Yes' if use_docker else 'No'})")

            category_success = True
            for script in TEST_CATEGORIES[category]["scripts"]:
                if use_docker:
                    print_colored(f"Executing in Docker: {script}", 'yellow')
                    success = run_docker_container(TEST_CATEGORIES[category]["docker_image"], script)
                else:
                    print_colored(f"Executing: {script}", 'yellow')
                    success = run_script(script)

                if not success:
                    category_success = False

            results[category] = category_success

    return results

def run_tests_in_docker() -> Dict[str, bool]:
    """Run all tests in their respective Docker containers."""
    results = {}

    for category, info in TEST_CATEGORIES.items():
        print_header(f"Running {category} Tests in Docker")

        docker_image = info.get("docker_image")
        if not docker_image:
            logger.warning(f"No Docker image defined for {category}, skipping")
            continue

        category_success = True
        for script in info["scripts"]:
            print_colored(f"Executing in Docker: {script}", 'yellow')
            success = run_docker_container(docker_image, script)
            if not success:
                category_success = False

        results[category] = category_success

    return results

def print_summary(results: Dict[str, bool]) -> None:
    """Print a summary of test results."""
    print_header("Test Summary")

    if not results:
        print_colored("No tests were run.", 'yellow')
        return

    for category, success in results.items():
        status = "PASSED" if success else "FAILED"
        color = 'green' if success else 'red'
        print_colored(f"{category}: {status}", color)

    # Overall result
    all_passed = all(results.values())
    overall = "All tests passed!" if all_passed else "Some tests failed!"
    color = 'green' if all_passed else 'red'
    print("\n" + "=" * 60)
    print_colored(overall, color)

def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description='Run data source tests')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--yfinance', action='store_true', help='Run Yahoo Finance tests')
    parser.add_argument('--binance', action='store_true', help='Run Binance API tests')
    parser.add_argument('--polygon', action='store_true', help='Run Polygon.io tests')
    parser.add_argument('--parquet', action='store_true', help='Run Parquet file tests')
    parser.add_argument('--docker', action='store_true', help='Run tests in Docker')
    parser.add_argument('--docker-only', action='store_true', help='Run tests only in Docker without local execution')
    args = parser.parse_args()

    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    # Check if we're in Docker environment
    in_docker = os.environ.get('DOCKER_CONTAINER', False) or os.path.exists('/.dockerenv')

    # Determine which tests to run
    selected_categories = []

    # If specific test flags are provided, use them
    if args.yfinance:
        selected_categories.append("yfinance")
    if args.binance:
        selected_categories.append("binance")
    if args.polygon:
        selected_categories.append("polygon")
    if args.parquet:
        selected_categories.append("parquet")
    if args.all:
        selected_categories = list(TEST_CATEGORIES.keys())

    # If Docker only mode is enabled, skip local execution
    if args.docker_only:
        print_colored("Running tests only in Docker containers", 'cyan')
        results_docker = run_tests_in_docker()
        print_summary(results_docker)
        return

    # If we're already in a Docker container, just run the local tests
    if in_docker:
        print_colored("Running in Docker environment", 'cyan')

        # If no specific categories selected, run all tests
        if not selected_categories:
            selected_categories = list(TEST_CATEGORIES.keys())

        if selected_categories:
            print_colored(f"Running tests for: {', '.join(selected_categories)}", 'cyan')
            results = run_selected_tests(selected_categories)
            print_summary(results)
        return

    # If no command line args specified and not in Docker, prompt interactively
    if not selected_categories and not args.docker_only:
        selected_categories = prompt_for_tests()

    # Run the selected tests locally if any
    if selected_categories and not args.docker_only:
        print_colored(f"Running tests for: {', '.join(selected_categories)}", 'cyan')
        results = run_selected_tests(selected_categories)
        print_summary(results)
    elif not args.docker_only:
        print_colored("No tests selected for local execution.", 'yellow')

    # Run tests in Docker if --docker flag is set or if we're using --docker-only
    if args.docker or args.docker_only:
        print_colored("Running all tests in Docker containers", 'cyan')
        results_docker = run_tests_in_docker()
        print_summary(results_docker)
    elif not args.docker_only and not in_docker:
        # If not running in Docker, prompt if Docker is not explicitly requested
        docker_prompt = input("Do you want to run tests in Docker containers? (y/n/all): ").strip().lower()
        if docker_prompt == 'y':
            selected_categories_docker = prompt_for_tests_with_docker()
            if selected_categories_docker:
                print_colored(f"Running tests for: {', '.join([cat[0] for cat in selected_categories_docker])} (in Docker)", 'cyan')
                results_docker = run_selected_tests_with_docker(selected_categories_docker)
                print_summary(results_docker)
        elif docker_prompt == 'all':
            print_colored("Running all tests in Docker containers", 'cyan')
            results_docker = run_tests_in_docker()
            print_summary(results_docker)

if __name__ == "__main__":
    main()
