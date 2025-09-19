"""
Progress Tracker Module

This module provides progress tracking functionality with progress bars and ETA calculations.
It supports both simple progress tracking and complex operations with multiple steps.
"""

import time
import sys
from typing import Callable, Any, Optional, List
from datetime import datetime, timedelta
import threading
import pandas as pd


class ProgressTracker:
    """Handles progress tracking with visual progress bars and ETA calculations."""
    
    def __init__(self, bar_width: int = 50):
        """
        Initialize the progress tracker.
        
        Args:
            bar_width: Width of the progress bar in characters
        """
        self.bar_width = bar_width
        self.start_time = None
        self.current_step = 0
        self.total_steps = 0
        self.step_name = ""
        self._stop_event = threading.Event()
    
    def run_with_progress(self, func: Callable, *args, **kwargs) -> Any:
        """
        Run a function with progress tracking.
        
        Args:
            func: Function to run
            *args: Arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Result of the function execution
        """
        # Extract progress info from kwargs if available
        progress_info = kwargs.pop('progress_info', {})
        step_name = progress_info.get('step_name', 'Processing')
        
        self.start_time = time.time()
        self.step_name = step_name
        
        # Start progress display in a separate thread
        progress_thread = threading.Thread(target=self._display_progress)
        progress_thread.daemon = True
        progress_thread.start()
        
        try:
            # Run the function
            result = func(*args, **kwargs)
            return result
        finally:
            # Stop progress display
            self._stop_event.set()
            progress_thread.join(timeout=1)
            self._clear_progress_line()
    
    def _display_progress(self):
        """Display progress bar in a separate thread."""
        while not self._stop_event.is_set():
            elapsed = time.time() - self.start_time
            progress_text = self._create_progress_text(elapsed)
            
            # Clear line and print progress
            sys.stdout.write('\r' + ' ' * 100 + '\r')  # Clear line
            sys.stdout.write(progress_text)
            sys.stdout.flush()
            
            time.sleep(0.1)  # Update every 100ms
    
    def _create_progress_text(self, elapsed: float) -> str:
        """Create progress text with bar and ETA."""
        # Create animated progress bar
        bar_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        spinner = bar_chars[int(elapsed * 10) % len(bar_chars)]
        
        # Create progress bar
        filled_width = int(self.bar_width * (elapsed % 2))  # Animated fill
        bar = '█' * filled_width + '░' * (self.bar_width - filled_width)
        
        # Format elapsed time
        elapsed_str = self._format_time(elapsed)
        
        # Create ETA (simplified - just show elapsed time for now)
        eta_str = f"ETA: {elapsed_str}"
        
        return f"{spinner} {self.step_name} [{bar}] {elapsed_str} {eta_str}"
    
    def _format_time(self, seconds: float) -> str:
        """Format time in HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def _clear_progress_line(self):
        """Clear the progress line."""
        sys.stdout.write('\r' + ' ' * 100 + '\r')
        sys.stdout.flush()
    
    def start_operation(self, total_steps: int, operation_name: str = "Operation"):
        """
        Start a multi-step operation.
        
        Args:
            total_steps: Total number of steps
            operation_name: Name of the operation
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.step_name = operation_name
        self.start_time = time.time()
        self._stop_event.clear()
    
    def update_step(self, step_name: str, step_number: Optional[int] = None):
        """
        Update current step.
        
        Args:
            step_name: Name of the current step
            step_number: Step number (if None, increments current step)
        """
        if step_number is not None:
            self.current_step = step_number
        else:
            self.current_step += 1
        
        self.step_name = step_name
    
    def finish_operation(self):
        """Finish the current operation."""
        self._stop_event.set()
        self._clear_progress_line()
        
        if self.start_time:
            total_time = time.time() - self.start_time
            print(f"✓ Operation completed in {self._format_time(total_time)}")
    
    def create_detailed_progress(self, data: pd.DataFrame, operation_name: str) -> 'DetailedProgressTracker':
        """
        Create a detailed progress tracker for data operations.
        
        Args:
            data: DataFrame being processed
            operation_name: Name of the operation
            
        Returns:
            DetailedProgressTracker instance
        """
        return DetailedProgressTracker(data, operation_name, self.bar_width)


class DetailedProgressTracker:
    """Detailed progress tracker for data operations with row-by-row progress."""
    
    def __init__(self, data: pd.DataFrame, operation_name: str, bar_width: int = 50):
        """
        Initialize detailed progress tracker.
        
        Args:
            data: DataFrame being processed
            operation_name: Name of the operation
            bar_width: Width of the progress bar
        """
        self.data = data
        self.operation_name = operation_name
        self.bar_width = bar_width
        self.total_rows = len(data)
        self.processed_rows = 0
        self.start_time = time.time()
        self._stop_event = threading.Event()
    
    def update(self, processed_rows: int):
        """
        Update progress.
        
        Args:
            processed_rows: Number of rows processed so far
        """
        self.processed_rows = processed_rows
        self._display_progress()
    
    def _display_progress(self):
        """Display detailed progress."""
        if self.total_rows == 0:
            return
        
        progress = self.processed_rows / self.total_rows
        filled_width = int(self.bar_width * progress)
        bar = '█' * filled_width + '░' * (self.bar_width - filled_width)
        
        elapsed = time.time() - self.start_time
        
        # Calculate ETA
        if self.processed_rows > 0:
            rate = self.processed_rows / elapsed
            remaining_rows = self.total_rows - self.processed_rows
            eta_seconds = remaining_rows / rate if rate > 0 else 0
            eta_str = f"ETA: {self._format_time(eta_seconds)}"
        else:
            eta_str = "ETA: --:--"
        
        percentage = progress * 100
        elapsed_str = self._format_time(elapsed)
        
        progress_text = (
            f"🔄 {self.operation_name} [{bar}] "
            f"{percentage:5.1f}% ({self.processed_rows:,}/{self.total_rows:,}) "
            f"{elapsed_str} {eta_str}"
        )
        
        sys.stdout.write('\r' + ' ' * 100 + '\r')
        sys.stdout.write(progress_text)
        sys.stdout.flush()
    
    def _format_time(self, seconds: float) -> str:
        """Format time in HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def finish(self):
        """Finish the detailed progress tracking."""
        self.processed_rows = self.total_rows
        self._display_progress()
        
        total_time = time.time() - self.start_time
        print(f"\n✓ {self.operation_name} completed in {self._format_time(total_time)}")
        print(f"  Processed {self.total_rows:,} rows at {self.total_rows/total_time:.0f} rows/sec")


class BatchProgressTracker:
    """Progress tracker for batch operations."""
    
    def __init__(self, total_batches: int, batch_name: str = "Batch"):
        """
        Initialize batch progress tracker.
        
        Args:
            total_batches: Total number of batches
            batch_name: Name of the batch operation
        """
        self.total_batches = total_batches
        self.current_batch = 0
        self.batch_name = batch_name
        self.start_time = time.time()
    
    def start_batch(self, batch_number: int, batch_info: str = ""):
        """
        Start a new batch.
        
        Args:
            batch_number: Batch number
            batch_info: Additional batch information
        """
        self.current_batch = batch_number
        elapsed = time.time() - self.start_time
        
        if batch_number > 0:
            # Calculate ETA
            avg_time_per_batch = elapsed / batch_number
            remaining_batches = self.total_batches - batch_number
            eta_seconds = remaining_batches * avg_time_per_batch
            eta_str = f"ETA: {self._format_time(eta_seconds)}"
        else:
            eta_str = "ETA: --:--"
        
        progress_text = (
            f"📦 {self.batch_name} {batch_number + 1}/{self.total_batches} "
            f"({self._format_time(elapsed)}) {eta_str}"
        )
        
        if batch_info:
            progress_text += f" - {batch_info}"
        
        print(progress_text)
    
    def _format_time(self, seconds: float) -> str:
        """Format time in HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def finish(self):
        """Finish batch processing."""
        total_time = time.time() - self.start_time
        print(f"✓ All {self.total_batches} batches completed in {self._format_time(total_time)}")
