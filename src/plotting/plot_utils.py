# -*- coding: utf-8 -*-
# src/plotting/plot_utils.py
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


def setup_interactive_backend():
    """
    Setup matplotlib for interactive plotting if not in test environment.
    """
    if not is_test_environment():
        try:
            # Use Agg backend for reliable plotting, then save and open files
            matplotlib.use('Agg')
            print(f"Matplotlib backend set to: {matplotlib.get_backend()}")
            print("Using file-based plot display for reliability")
        except Exception as e:
            print(f"Warning: Could not set Agg backend: {e}")
            # Fallback to default backend
            pass


def smart_plot_display(show_plot=True, block=None, pause_time=None, plot_type="plot"):
    """
    Smart plot display function that automatically determines whether to show or close plots.
    
    Args:
        show_plot (bool): Whether to show the plot (overrides automatic detection)
        block (bool): Whether to block execution while showing the plot. If None, uses PLOT_BLOCK_MODE env var
        pause_time (float): Time to pause before closing (in seconds) if not blocking. If None, uses PLOT_PAUSE_TIME env var
        plot_type (str): Type of plot to look for (e.g., "mplfinance", "seaborn")
    """
    # Setup backend
    setup_interactive_backend()
    
    # Check environment variable for block mode if not explicitly specified
    if block is None:
        block_env = os.environ.get('PLOT_BLOCK_MODE', 'true').lower()
        block = block_env in ('true', '1', 'yes', 'on')
    
    # Check environment variable for pause time if not explicitly specified
    if pause_time is None:
        pause_time = float(os.environ.get('PLOT_PAUSE_TIME', '10.0'))
    
    if show_plot and should_show_plot():
        if block:
            # Open the most recent plot file (since plot is already saved)
            open_latest_plot_file(plot_type)
        else:
            # Open the most recent plot file with auto-close
            open_latest_plot_file(plot_type)
            if pause_time > 0:
                print(f"Plot will remain open for {pause_time} seconds...")
                time.sleep(pause_time)
    else:
        plt.close()


def open_latest_plot_file(plot_type="plot"):
    """
    Open the most recently created plot file in the plots directory.
    
    Args:
        plot_type (str): Type of plot to look for (e.g., "mplfinance", "seaborn")
    """
    try:
        import os
        import subprocess
        import platform
        import glob
        
        plots_dir = os.path.join(os.getcwd(), 'plots')
        if not os.path.exists(plots_dir):
            print(f"Plots directory not found: {plots_dir}")
            return
        
        # Find the most recent plot file
        pattern = os.path.join(plots_dir, f"{plot_type}_plot_*.png")
        plot_files = glob.glob(pattern)
        
        if not plot_files:
            print(f"No {plot_type} plot files found in {plots_dir}")
            return
        
        # Get the most recent file
        latest_file = max(plot_files, key=os.path.getctime)
        print(f"Opening latest {plot_type} plot: {latest_file}")
        
        # Open plot with system default viewer
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', latest_file])
        elif platform.system() == 'Linux':
            subprocess.run(['xdg-open', latest_file])
        elif platform.system() == 'Windows':
            subprocess.run(['start', latest_file], shell=True)
        
        print("Plot opened with system default viewer")
        
    except Exception as e:
        print(f"Warning: Could not open plot file: {e}")


def file_based_plot_display(auto_close=False, pause_time=10.0):
    """
    Display plot by saving to file and opening with system default viewer.
    
    Args:
        auto_close (bool): Whether to automatically close the plot after pause
        pause_time (float): Time to pause before closing (in seconds)
    """
    try:
        import tempfile
        import subprocess
        import platform
        import os
        
        # Create temporary file in plots directory if it exists
        plots_dir = os.path.join(os.getcwd(), 'plots')
        if os.path.exists(plots_dir):
            temp_dir = plots_dir
        else:
            temp_dir = tempfile.gettempdir()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir=temp_dir) as tmp_file:
            plot_file = tmp_file.name
        
        # Save current plot to file
        plt.savefig(plot_file, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Plot saved to: {plot_file}")
        
        # Open plot with system default viewer
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', plot_file])
        elif platform.system() == 'Linux':
            subprocess.run(['xdg-open', plot_file])
        elif platform.system() == 'Windows':
            subprocess.run(['start', plot_file], shell=True)
        
        print("Plot opened with system default viewer")
        
        if auto_close:
            print(f"Plot will auto-close in {pause_time} seconds...")
            time.sleep(pause_time)
            # Try to close the file
            try:
                os.unlink(plot_file)
                print("Temporary plot file removed")
            except:
                pass
        else:
            print("Plot file will remain open. Close the viewer when done.")
            print(f"Plot file location: {plot_file}")
        
    except Exception as e:
        print(f"Warning: Could not save/open plot: {e}")
        print("Falling back to interactive display")
        try:
            # Try to use interactive backend as fallback
            matplotlib.use('TkAgg')
            plt.ion()
            plt.show(block=True)
        except:
            print("Could not display plot interactively either")
            plt.close()
