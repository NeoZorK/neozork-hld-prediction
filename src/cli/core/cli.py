# -*- coding: utf-8 -*-
# src/cli/core/cli.py

"""
Main CLI module with core functionality.
"""

import sys
from colorama import init, Fore, Style

from .argument_parser import parse_arguments
from .argument_validator import validate_and_process_arguments

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def show_indicator_help(indicator_name: str):
    """
    Show help information for a specific indicator.
    
    Args:
        indicator_name (str): Name of the indicator
    """
    from .indicator_help import show_indicator_help as show_help
    show_help(indicator_name)


def main():
    """Main CLI entry point."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Validate and process arguments
        args = validate_and_process_arguments(args)
        
        # Return validated arguments for further processing
        return args
        
    except ValueError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
