"""Shcherbyna Pressure Vector Indicator Analysis Tool

This script performs analysis of pressure vector indicators based on provided data.

Description:
    The tool calculates and visualizes pressure vector indicators using the Shcherbyna
    method. It processes input data, performs necessary calculations, and generates
    visual representations of the results.

Usage:
    python run_analysis.py [options]
    ./nz [options]                    # Universal script (works in Docker/local)
    uv run ./nz [options]             # With uv dependency management

Options:
    --input-file PATH       Path to the input data file
    --output-dir PATH      Directory for saving output files
    --plot-type TYPE       Type of plot to generate (default: 'standard')
    --verbose             Enable detailed logging output
    --version            Show program's version number and exit
    --help               Show this help message and exit

Examples:
    # Basic usage with default settings
    python run_analysis.py --input-file data.csv
    ./nz --input-file data.csv

    # Generate specific plot type with custom output directory
    python run_analysis.py --input-file data.csv --output-dir ./results --plot-type detailed
    ./nz --input-file data.csv --output-dir ./results --plot-type detailed

    # Run with verbose logging
    python run_analysis.py --input-file data.csv --verbose
    ./nz --input-file data.csv --verbose

    # Show version information
    ./nz --version

    # Show help
    ./nz --help

    # Run demo analysis
    ./nz demo --rule PHLD

    # Analyze YFinance data
    ./nz yfinance MSFT --rule PHLD
    ./nz yfinance AAPL --period 1mo --rule PHLD

    # Analyze MQL5 data
    ./nz mql5 EURUSD --interval H4 --rule PHLD
    ./nz mql5 GBPUSD --interval D1 --rule PHLD

    # Analyze CSV data
    ./nz csv --csv-file data.csv --rule PHLD
    ./nz csv --csv-file data.csv --rule PHLD --plot-type detailed

    # Analyze Binance data
    ./nz binance BTCUSDT --interval 1h --rule PHLD
    ./nz binance ETHUSDT --interval 4h --rule PHLD

    # Analyze Polygon data
    ./nz polygon AAPL --interval 1 --rule PHLD
    ./nz polygon MSFT --interval 5 --rule PHLD

    # Run with specific parameters
    ./nz --input-file data.csv --output-dir ./results --plot-type detailed

    # Use with uv (recommended for native environment)
    uv run ./nz --version
    uv run ./nz demo --rule PHLD

Environment Detection:
    The nz script automatically detects whether it's running in a Docker container
    or native environment:
    - Docker Environment: Uses python run_analysis.py directly
    - Native Environment: Uses uv run python run_analysis.py (with fallback to direct Python)

Related Scripts:
    ./eda [options]                    # Data exploration and analysis script
    ./eda --help                       # Show EDA help
    ./eda --data-quality-checks        # Run data quality checks
    ./eda --nan-check                  # Check for NaN values
    ./eda --fix-files                  # Fix data quality issues
    ./eda --descriptive-stats          # Run statistical analysis

Notes:
    - Input file should be in CSV format with appropriate headers
    - Output directory will be created if it doesn't exist
    - Requires Python 3.8 or higher
    - For Docker usage, scripts work seamlessly inside containers
    - For native development, uv is recommended for dependency management
"""

# /run_analysis.py (in NeoZorK HLD/ root folder)

# Standard library imports
import sys
import time
import os

# Check if running in Docker environment and patch webbrowser if needed
IN_DOCKER = os.environ.get('DOCKER_CONTAINER', False) or os.path.exists('/.dockerenv')
if IN_DOCKER:
    try:
        # Import our Docker-friendly browser module
        from src.utils import docker_browser
        # Patch the webbrowser module in sys.modules to use our version
        sys.modules['webbrowser'] = docker_browser
        # Docker browser patching complete
    except ImportError:
        docker_browser = None
        print("Warning: Running in Docker but docker_browser module not found")

# Imports from the src package using new paths
from src import __version__
from src.cli.cli import parse_arguments
from src.workflow.workflow import run_indicator_workflow
from src.workflow.reporting import print_summary
from src.common import logger
# Importing rich for colored terminal output
from rich.console import Console


# Initialize rich console
console = Console()


# --- Main Execution Function ---
def main():
    """Main execution function for the Shcherbyna Pressure Vector Indicator analysis.

    This function orchestrates the entire workflow of the analysis:
    1. Displays version information
    2. Parses command line arguments
    3. Executes the analysis workflow
    4. Generates and displays the summary report

    The function handles errors gracefully and provides appropriate exit codes:
    - Exit code 0: Successful execution
    - Exit code 1: Error in argument parsing or workflow execution

    Returns:
        None
    """

    # Start overall timer for the entire script execution
    start_time_total = time.perf_counter()

    # Parse command line arguments using the function from cli.py
    try:
        args = parse_arguments()
    except Exception as e:
        logger.print_error(f"Failed to parse arguments: {e}")
        sys.exit(1) # Exit if argument parsing fails

    # --- Execute Workflow ---
    # Call the main workflow function from workflow.py, passing the parsed args.
    # This function now contains the logic for data acquisition, point size,
    # indicator calculation, and plotting generation.
    # It returns a dictionary containing results and metrics.
    workflow_results = run_indicator_workflow(args)

    # --- Print Summary Report ---
    # Stop the overall timer
    end_time_total = time.perf_counter()
    total_duration = end_time_total - start_time_total

    # Check if the workflow returned a result dictionary
    if workflow_results:
        # Call the summary printing function from reporting.py
        print_summary(workflow_results, total_duration, args)
    else:
        # Fallback message if workflow function failed catastrophically
        logger.print_error("Critical error: Workflow did not return results.")
        logger.print_info(f"Total Execution Time: {total_duration:.3f} seconds")

    # Exit with an error code if the workflow reported failure
    if not workflow_results or not workflow_results.get("success", False):
        logger.print_error("Exiting due to errors during workflow execution.")
        sys.exit(1)
    else:
        logger.print_success("Workflow finished successfully.")


# Standard Python entry point check
if __name__ == "__main__":
    main()
