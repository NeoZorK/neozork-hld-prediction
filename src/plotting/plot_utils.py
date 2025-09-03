"""
Plot utilities for automatic display mode detection.

This module provides utilities to automatically determine whether to show plots
or close them based on the environment (tests vs. interactive usage).
"""

import os
import matplotlib
import matplotlib.pyplot as plt
import sys
import time


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


def smart_plot_display(show_plot=True, block=None, pause_time=None):
    """
    Smart plot display function that automatically determines whether to show or close plots.
    
    Args:
        show_plot (bool): Whether to show the plot (overrides automatic detection)
        block (bool): Whether to block execution while showing the plot. If None, uses PLOT_BLOCK_MODE env var
        pause_time (float): Time to pause before closing (in seconds) if not blocking. If None, uses PLOT_PAUSE_TIME env var
    """
    # Check environment variable for block mode if not explicitly specified
    if block is None:
        block_env = os.environ.get('PLOT_BLOCK_MODE', 'true').lower()
        block = block_env in ('true', '1', 'yes', 'on')
    
    # Check environment variable for pause time if not explicitly specified
    if pause_time is None:
        pause_time = float(os.environ.get('PLOT_PAUSE_TIME', '5.0'))
    
    if show_plot and should_show_plot():
        if block:
            plt.show(block=True)
        else:
            plt.show(block=False)
            # Give user time to see the plot before it closes
            print(f"\nPlot displayed. Closing in {pause_time} seconds...")
            time.sleep(pause_time)
            plt.close()
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
