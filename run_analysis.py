# /run_analysis.py (in NeoZorK HLD/ root folder)

# Standard library imports
import sys
import time

# Imports from the src package using new paths
from src import __version__
from src.cli.cli import parse_arguments
from src.workflow.workflow import run_indicator_workflow
from src.reporting.reporting import print_summary
from src.common.logger import logger


# --- Main Execution Function ---
def main():
    """Main entry point script."""

    # Print version information using the logger
    logger.print_info(f"Shcherbyna Pressure Vector Indicator - Version: {__version__}")

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