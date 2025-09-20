# -*- coding: utf-8 -*-
"""
Progress Tracker for NeoZork Interactive ML Trading Strategy Development.

This module provides progress tracking with percentage and ETA calculations.
"""

import time
import sys
from typing import Optional, Callable
from datetime import datetime, timedelta
from src.common.logger import print_info, print_warning, print_error, print_debug


class ProgressTracker:
    """
    Progress tracker with percentage and ETA calculations.
    
    Features:
    - Real-time progress updates
    - ETA calculation
    - Single-line progress display
    - Smooth progress bars
    - Time tracking
    """
    
    def __init__(self, total_items: int, description: str = "Processing"):
        """
        Initialize the progress tracker.
        
        Args:
            total_items: Total number of items to process
            description: Description of the process
        """
        self.total_items = total_items
        self.description = description
        self.current_item = 0
        self.start_time = None
        self.last_update_time = None
        self.update_interval = 0.1  # Update every 100ms
        self.last_progress = 0
        
    def start(self):
        """Start the progress tracking."""
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.current_item = 0
        self.last_progress = 0
        print_info(f"🚀 Starting {self.description}...")
    
    def update(self, current_item: int, custom_message: str = ""):
        """
        Update progress.
        
        Args:
            current_item: Current item number (0-based)
            custom_message: Custom message to display
        """
        self.current_item = current_item
        current_time = time.time()
        
        # Only update if enough time has passed
        if current_time - self.last_update_time < self.update_interval:
            return
        
        self.last_update_time = current_time
        
        # Calculate progress
        progress = (current_item / self.total_items) * 100 if self.total_items > 0 else 0
        
        # Only update if progress has changed significantly
        if abs(progress - self.last_progress) < 0.1:
            return
        
        self.last_progress = progress
        
        # Calculate ETA
        eta = self._calculate_eta(current_time)
        
        # Create progress bar
        progress_bar = self._create_progress_bar(progress)
        
        # Create status message
        status_message = self._create_status_message(
            progress, eta, custom_message
        )
        
        # Display progress (single line)
        self._display_progress(progress_bar, status_message)
    
    def finish(self, success_message: str = "Completed"):
        """
        Finish the progress tracking.
        
        Args:
            success_message: Success message to display
        """
        if self.start_time:
            total_time = time.time() - self.start_time
            print_info(f"✅ {success_message} in {total_time:.2f} seconds")
        else:
            print_info(f"✅ {success_message}")
    
    def _calculate_eta(self, current_time: float) -> str:
        """
        Calculate estimated time of arrival.
        
        Args:
            current_time: Current timestamp
            
        Returns:
            ETA string
        """
        try:
            if self.current_item == 0 or self.start_time is None:
                return "Calculating..."
            
            elapsed_time = current_time - self.start_time
            items_per_second = self.current_item / elapsed_time
            remaining_items = self.total_items - self.current_item
            
            if items_per_second > 0:
                eta_seconds = remaining_items / items_per_second
                eta_delta = timedelta(seconds=int(eta_seconds))
                
                if eta_delta.total_seconds() < 60:
                    return f"ETA: {int(eta_seconds)}s"
                elif eta_delta.total_seconds() < 3600:
                    minutes = int(eta_delta.total_seconds() / 60)
                    return f"ETA: {minutes}m"
                else:
                    hours = int(eta_delta.total_seconds() / 3600)
                    minutes = int((eta_delta.total_seconds() % 3600) / 60)
                    return f"ETA: {hours}h{minutes}m"
            else:
                return "ETA: Unknown"
                
        except Exception as e:
            print_debug(f"Error calculating ETA: {e}")
            return "ETA: Calculating..."
    
    def _create_progress_bar(self, progress: float, width: int = 30) -> str:
        """
        Create a visual progress bar.
        
        Args:
            progress: Progress percentage (0-100)
            width: Width of the progress bar
            
        Returns:
            Progress bar string
        """
        try:
            filled_width = int((progress / 100) * width)
            empty_width = width - filled_width
            
            # Create progress bar with Unicode characters
            bar = "█" * filled_width + "░" * empty_width
            
            return f"[{bar}]"
            
        except Exception as e:
            print_debug(f"Error creating progress bar: {e}")
            return "[░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]"
    
    def _create_status_message(self, progress: float, eta: str, custom_message: str) -> str:
        """
        Create status message.
        
        Args:
            progress: Progress percentage
            eta: ETA string
            custom_message: Custom message
            
        Returns:
            Status message string
        """
        try:
            # Format progress with 1 decimal place
            progress_str = f"{progress:.1f}%"
            
            # Create status message
            if custom_message:
                status = f"{self.description}: {custom_message} | {progress_str} | {eta}"
            else:
                status = f"{self.description}: {progress_str} | {eta}"
            
            return status
            
        except Exception as e:
            print_debug(f"Error creating status message: {e}")
            return f"{self.description}: {progress:.1f}% | {eta}"
    
    def _display_progress(self, progress_bar: str, status_message: str):
        """
        Display progress on a single line.
        
        Args:
            progress_bar: Progress bar string
            status_message: Status message string
        """
        try:
            # Clear the line and move cursor to beginning
            sys.stdout.write('\r')
            sys.stdout.write(' ' * 120)  # Clear line
            sys.stdout.write('\r')
            
            # Write progress
            full_message = f"{progress_bar} {status_message}"
            sys.stdout.write(full_message)
            sys.stdout.flush()
            
        except Exception as e:
            print_debug(f"Error displaying progress: {e}")
    
    def create_callback(self) -> Callable[[int, int, str], None]:
        """
        Create a callback function for use with other modules.
        
        Returns:
            Callback function
        """
        def callback(current: int, total: int, message: str = ""):
            self.update(current, message)
        
        return callback


class MultiProgressTracker:
    """
    Multi-level progress tracker for complex operations.
    
    Features:
    - Multiple progress levels
    - Nested progress tracking
    - Overall progress calculation
    """
    
    def __init__(self, total_phases: int, description: str = "Multi-phase Processing"):
        """
        Initialize the multi-progress tracker.
        
        Args:
            total_phases: Total number of phases
            description: Description of the process
        """
        self.total_phases = total_phases
        self.description = description
        self.current_phase = 0
        self.phase_trackers = {}
        self.start_time = None
        
    def start(self):
        """Start the multi-progress tracking."""
        self.start_time = time.time()
        self.current_phase = 0
        print_info(f"🚀 Starting {self.description}...")
    
    def start_phase(self, phase_name: str, total_items: int) -> ProgressTracker:
        """
        Start a new phase.
        
        Args:
            phase_name: Name of the phase
            total_items: Total items in this phase
            
        Returns:
            ProgressTracker for this phase
        """
        self.current_phase += 1
        phase_tracker = ProgressTracker(total_items, f"{phase_name} (Phase {self.current_phase}/{self.total_phases})")
        self.phase_trackers[phase_name] = phase_tracker
        phase_tracker.start()
        return phase_tracker
    
    def finish_phase(self, phase_name: str, success_message: str = "Phase completed"):
        """
        Finish a phase.
        
        Args:
            phase_name: Name of the phase
            success_message: Success message
        """
        if phase_name in self.phase_trackers:
            self.phase_trackers[phase_name].finish(success_message)
    
    def finish_all(self, success_message: str = "All phases completed"):
        """
        Finish all phases.
        
        Args:
            success_message: Success message
        """
        if self.start_time:
            total_time = time.time() - self.start_time
            print_info(f"✅ {success_message} in {total_time:.2f} seconds")
        else:
            print_info(f"✅ {success_message}")
