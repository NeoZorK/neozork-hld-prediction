"""
Plot utilities for automatic display mode detection.

This module provides utilities to automatically determine whether to show plots
or close them based on the environment (tests vs. interactive usage).
"""

import os
import matplotlib
import matplotlib.pyplot as plt
import sys


def is_test_environment():
    """
    Check if we're running in a test environment.
    
    Returns:
        bool: True if running in tests, False otherwise
    """
    # Check for pytest markers
    if 'pytest' in sys.modules:
        return True
    
    # Check for test environment variables
    if os.environ.get('PYTEST_CURRENT_TEST'):
        return True
    
    # Check for CI/CD environment
    if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
        return True
    
    # Check if matplotlib backend is set to non-interactive
    if matplotlib.get_backend() == 'Agg':
        return True
    
    return False


def should_show_plot():
    """
    Determine whether plots should be shown or closed.
    
    Returns:
        bool: True if plots should be shown, False if they should be closed
    """
    return not is_test_environment()


def smart_plot_display(show_plot=True):
    """
    Smart plot display function that automatically determines whether to show or close plots.
    
    Args:
        show_plot (bool): Whether to show the plot (overrides automatic detection)
    """
    if show_plot and should_show_plot():
        plt.show()
    else:
        plt.close()


def setup_interactive_backend():
    """
    Setup matplotlib for interactive plotting if not in test environment.
    """
    if not is_test_environment():
        try:
            # Try to use an interactive backend
            matplotlib.use('TkAgg')  # or 'Qt5Agg', 'MacOSX' depending on system
            plt.ion()  # Turn on interactive mode
        except Exception:
            # Fallback to default backend
            pass
