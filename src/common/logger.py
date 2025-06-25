# src/logger.py

"""
Console logging utility with colors using colorama.
All comments are in English.
"""

import colorama
from colorama import Fore, Style

# Initialize colorama once when the module is imported.
# autoreset=True automatically adds Style.RESET_ALL after each color print,
# simplifying usage as we don't need to manually reset color.
colorama.init(autoreset=True)

# Define color constants for different message types for better readability
INFO_COLOR = Fore.CYAN
WARNING_COLOR = Fore.YELLOW
ERROR_COLOR = Fore.RED
DEBUG_COLOR = Fore.MAGENTA  # Or Fore.BLUE, Fore.WHITE etc.
SUCCESS_COLOR = Fore.GREEN
HIGHLIGHT_COLOR = Fore.LIGHTBLUE_EX # For highlighting parts like keys in summary

# Reset style manually if needed (though autoreset should handle it)
RESET_ALL = Style.RESET_ALL

def print_info(message: str):
    """Prints an informational message (e.g., status, steps)."""
    print(f"{INFO_COLOR}{message}")

def print_warning(message: str):
    """Prints a warning message."""
    # Automatically adds "Warning: " prefix for clarity
    print(f"{WARNING_COLOR}Warning: {message}")

def print_error(message: str):
    """Prints an error message."""
     # Automatically adds "Error: " prefix
    print(f"{ERROR_COLOR}Error: {message}")

def print_debug(message: str):
    """Prints a debug message."""
    # Output debug message with color and "Debug:" prefix
    pass

def print_success(message: str):
    """Prints a success message."""
    print(f"{SUCCESS_COLOR}{message}")

def format_summary_line(key: str, value: str, key_width: int = 25) -> str:
     """Formats a line for the final summary with highlighted key."""
     # Pad the key string to align values
     padded_key = f"{key+':':<{key_width}}"
     # Apply highlight color to the key part
     colored_key = f"{HIGHLIGHT_COLOR}{padded_key}{RESET_ALL}"
     # Combine colored key and value
     return f"{colored_key} {value}"

# Note: For more complex logging needs (levels, file output, etc.),
# consider integrating Python's built-in 'logging' module in the future.
# This logger provides basic colored console output.