# src/cli.py

"""
Command Line Interface setup using argparse and RichHelpFormatter for colored help.
Removed arguments related to LWMA, CORE1, etc.
All comments are in English.
"""
import argparse
import textwrap # Import textwrap for cleaner epilog formatting


try:
    from rich_argparse import RichHelpFormatter
except ImportError:
    try:
        from rich.argparse import RichHelpFormatter
    except ImportError:
        # If rich is not installed or rich-argparse is missing, fallback gracefully
        # Prints a warning if rich text formatting is unavailable.
        print("Warning: 'rich' or 'rich-argparse' not installed. Help formatting will be basic.")
        print("Install with: pip install rich")
        # Use the standard formatter as a fallback
        # Sets the formatter to the standard one if RichHelpFormatter is unavailable.
        RichHelpFormatter = argparse.ArgumentDefaultsHelpFormatter

# Use relative imports for constants and version within the src package
from ..common.constants import TradingRule
from .. import __version__

# Function to parse command-line arguments
def parse_arguments():
    """Sets up argument parser using RichHelpFormatter and returns the parsed arguments."""

    # --- Main description ---
    # Defines the main description shown in the help message.
    main_description = textwrap.dedent("""
       Calculate and plot Shcherbyna Pressure Vector indicator using demo data,
       fetching from Yahoo Finance, or reading from a CSV file.
       """) # Updated description slightly

    # --- Example epilog ---
    # Defines example usage strings for the help message epilog.
    example_lines = [
        "[bold]Examples:[/bold]",
        "",
        "  [dim]# Run with demo data and default rule[/]",
        "  [bold cyan]python run_analysis.py demo[/]",
        "",
        "  [dim]# Run with demo data and Pressure_Vector rule[/]",
        "  [bold cyan]python run_analysis.py demo --rule PV[/]",
        "",
         # ADDED CSV EXAMPLE
         "  [dim]# Run using data from a specific CSV file[/]",
         "  [bold cyan]python run_analysis.py csv --csv-file path/to/your/data.csv[/]", # Added CSV example
         "",
        "  [dim]# Fetch 1 year of Daily EUR/USD data, estimate point size, use PV_HighLow rule[/]",
        "  [bold cyan]python run_analysis.py yf --ticker \"EURUSD=X\" --period 1y --interval D1 --rule PV_HighLow[/]",
        "",
        "  [dim]# Fetch AAPL data for a specific date range, H1 interval, explicitly set point size[/]",
        "  [bold cyan]python run_analysis.py yfinance --ticker AAPL --interval H1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule PHLD[/]"
    ]
    # Join example lines with newlines for better formatting
    # Joins the list of example lines into a single string with newlines.
    examples_epilog = "\n".join(example_lines)

    #--- Argument Parser Setup ---
    # Initializes the ArgumentParser with description, formatter, and examples.
    parser = argparse.ArgumentParser(
        description=main_description,
        formatter_class=RichHelpFormatter,
        epilog=examples_epilog
    )

    # --- Arguments ---
    # The mode argument determines the data source
    # Adds the main positional 'mode' argument with updated choices.
    parser.add_argument('mode', choices=['demo', 'yfinance', 'yf', 'csv'], # ADDED 'csv' choice
                        help="Operating mode: 'demo' uses built-in data, 'yfinance'/'yf' fetches data, 'csv' reads from file.")

    # --- CSV Options --- ADDED THIS SECTION
    # Creates a separate group for CSV-specific options in the help message.
    csv_group = parser.add_argument_group('CSV Options (used if mode=csv)')
    # Adds the '--csv-file' argument to the CSV group.
    csv_group.add_argument('--csv-file',
                         help="Path to the input CSV file (required for csv mode).")

    # --- Yahoo Finance Options ---
    # Grouping arguments for better organization in help message
    # Creates a group for Yahoo Finance options.
    yf_group = parser.add_argument_group('Yahoo Finance Options (used if mode=yfinance/yf)')
    # Added rich markup [cyan]...[/] for examples in help strings
    # Adds the '--ticker' argument for yfinance mode.
    yf_group.add_argument('-t', '--ticker',
                          help="Ticker symbol for yfinance (e.g., [cyan]'EURUSD=X'[/], [cyan]'BTC-USD'[/], [cyan]'AAPL'[/]). Required for yfinance/yf mode.")
    # Default value 'D1' will be shown by the formatter
    # Adds the '--interval' argument with a default value.
    yf_group.add_argument('-i', '--interval', default='D1',
                          help="Timeframe (e.g., [cyan]'M1', 'H1', 'D1', 'W1', 'MN1'[/]). Will be mapped to yfinance interval.")
    # Adds the '--point' argument for explicitly setting point size.
    yf_group.add_argument('--point', type=float,
                          help="Instrument point size (e.g., [cyan]0.00001[/]). Overrides automatic estimation. Crucial for accuracy.")

    # --- History Selection (for Yahoo Finance) ---
    # Mutually exclusive group ensures only period or start/end is used
    # Creates a mutually exclusive group for period vs. start/end date selection.
    history_group = yf_group.add_mutually_exclusive_group()
    # Default value '1y' will be shown by the formatter
    # Adds the '--period' argument to the exclusive group.
    history_group.add_argument('-p', '--period', default='1y',
                               help="History period for yfinance (e.g., [cyan]'1mo', '6mo', '1y', '5y', 'max'[/]).")
    # Adds the '--start' argument to the exclusive group.
    history_group.add_argument('--start', help="Start date for yfinance data (YYYY-MM-DD). Use with [bold]--end[/].")
    # --end is defined outside the exclusive group but logically belongs with --start
    # Adds the '--end' argument (logically paired with '--start').
    yf_group.add_argument('--end', help="End date for yfinance data (YYYY-MM-DD). Use with [bold]--start[/].")

    # --- Indicator Options (Simplified) ---
    # Creates a group for indicator-related options.
    indicator_group = parser.add_argument_group('Indicator Options')

    # Get available rules dynamically AFTER updating TradingRule enum
    # These are the only rules left after the removal step
    #rule_choices = list(TradingRule.__members__.keys())

    # Map rule choices to their corresponding TradingRule enum values
    # Defines aliases for shorter rule names.
    rule_aliases = {
        'PHLD': 'Predict_High_Low_Direction',
        'PV': 'Pressure_Vector',
        'SR': 'Support_Resistants'
    }

    # Add aliases to the rule choices
    # Gets the actual enum member names.
    rule_names = list(TradingRule.__members__.keys())

    # Create a list of all rule choices including aliases
    # Combines enum names and aliases for the 'choices' list.
    all_rule_choices = rule_names + list(rule_aliases.keys())

    # Set default rule to Predict_High_Low_Direction
    # Sets the default rule name based on the TradingRule enum.
    default_rule_name = TradingRule.Predict_High_Low_Direction.name

    # Add argument for rule selection
    # Adds the '--rule' argument with choices and default value.
    indicator_group.add_argument(
        '--rule',
        default=default_rule_name,
        choices=all_rule_choices,  # use all_rule_choices
        help=f"Trading rule to apply. Default: {default_rule_name}. "
             f"Aliases: PHLD=Predict_High_Low_Direction, PV=Pressure_Vector, SR=Support_Resistants." # Updated alias info slightly
    )

    # --- Version ---
    # Standard version argument, using rich markup for the version string output
    # Adds the standard '--version' argument.
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s [yellow]{__version__}[/]', # Added color markup
                        help="Show program's version number and exit.")

    # Parse arguments
    # Parses the actual command-line arguments provided by the user.
    args = parser.parse_args()

    # --- Post-parsing validation --- ADDED THIS BLOCK
    # Checks if the mode is 'csv' and if the required '--csv-file' argument was provided.
    if args.mode == 'csv' and not args.csv_file:
        # If mode is 'csv' but '--csv-file' is missing, print an error message and exit.
        # parser.error() is a clean way to exit with an argparse error.
        parser.error("argument --csv-file is required when mode is 'csv'")

    # Return parsed arguments if validation passes
    return args