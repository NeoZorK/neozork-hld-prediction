"""
Progress Tracking Module for Time Series Analysis

This module provides progress tracking capabilities with ETA estimation
for batch processing operations in time series analysis.

Features:
- Progress bar with percentage completion
- ETA (Estimated Time of Arrival) calculation
- Memory usage tracking
- File processing statistics
- Real-time progress updates
"""

import time
import gc
import psutil
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import sys


class ProgressTracker:
    """Tracks progress and provides ETA for batch processing operations."""
    
    def __init__(self, total_files: int, verbose: bool = True):
        """
        Initialize progress tracker.
        
        Args:
            total_files: Total number of files to process
            verbose: Whether to show detailed progress information
        """
        self.total_files = total_files
        self.processed_files = 0
        self.failed_files = 0
        self.start_time = time.time()
        self.file_start_times = {}
        self.file_processing_times = []
        self.verbose = verbose
        self.current_file = None
        self.process = psutil.Process(os.getpid())
        
        # Initialize memory tracking
        self.initial_memory = self._get_memory_usage()
        self.peak_memory = self.initial_memory
        
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            memory_info = self.process.memory_info()
            return memory_info.rss / 1024 / 1024  # Convert to MB
        except:
            return 0.0
    
    def start_file(self, filename: str) -> None:
        """
        Start processing a new file.
        
        Args:
            filename: Name of the file being processed
        """
        self.current_file = filename
        self.file_start_times[filename] = time.time()
        
        if self.verbose:
            print(f"\n{'='*80}")
            print(f"📁 PROCESSING FILE {self.processed_files + self.failed_files + 1}/{self.total_files}: {filename}")
            print(f"{'='*80}")
            print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
            print(f"💾 Memory usage: {self._get_memory_usage():.1f} MB")
    
    def complete_file(self, success: bool = True, error_message: str = None) -> None:
        """
        Complete processing of current file.
        
        Args:
            success: Whether file processing was successful
            error_message: Error message if processing failed
        """
        if not self.current_file:
            return
            
        file_end_time = time.time()
        file_processing_time = file_end_time - self.file_start_times[self.current_file]
        self.file_processing_times.append(file_processing_time)
        
        if success:
            self.processed_files += 1
            status = "✅ Successfully processed"
        else:
            self.failed_files += 1
            status = "❌ Failed to process"
            if error_message:
                status += f": {error_message}"
        
        # Update peak memory
        current_memory = self._get_memory_usage()
        self.peak_memory = max(self.peak_memory, current_memory)
        
        if self.verbose:
            print(f"\n{status}: {self.current_file}")
            print(f"⏱️  File processing time: {file_processing_time:.2f} seconds")
            print(f"💾 Current memory usage: {current_memory:.1f} MB")
            print(f"📊 Peak memory usage: {self.peak_memory:.1f} MB")
        
        # Clear current file
        self.current_file = None
        
        # Force garbage collection to free memory
        gc.collect()
    
    def get_progress_info(self) -> Dict[str, Any]:
        """
        Get current progress information.
        
        Returns:
            Dictionary with progress statistics
        """
        total_processed = self.processed_files + self.failed_files
        progress_percentage = (total_processed / self.total_files) * 100 if self.total_files > 0 else 0
        
        # Calculate ETA
        elapsed_time = time.time() - self.start_time
        if total_processed > 0:
            avg_time_per_file = elapsed_time / total_processed
            remaining_files = self.total_files - total_processed
            eta_seconds = remaining_files * avg_time_per_file
            eta = datetime.now() + timedelta(seconds=eta_seconds)
        else:
            eta = None
            avg_time_per_file = 0
        
        # Calculate processing rate
        files_per_minute = (total_processed / elapsed_time) * 60 if elapsed_time > 0 else 0
        
        return {
            'total_files': self.total_files,
            'processed_files': self.processed_files,
            'failed_files': self.failed_files,
            'current_file': self.current_file,
            'progress_percentage': progress_percentage,
            'elapsed_time': elapsed_time,
            'eta': eta,
            'avg_time_per_file': avg_time_per_file,
            'files_per_minute': files_per_minute,
            'memory_usage': self._get_memory_usage(),
            'peak_memory': self.peak_memory,
            'memory_increase': self._get_memory_usage() - self.initial_memory
        }
    
    def display_progress(self) -> None:
        """Display current progress information."""
        info = self.get_progress_info()
        
        # Create visual progress bar
        progress_bar = self._create_progress_bar(info['progress_percentage'])
        
        print(f"\n{'='*60}")
        print(f"📊 BATCH PROCESSING PROGRESS")
        print(f"{'='*60}")
        print(f"📁 Files: {info['processed_files'] + info['failed_files']}/{info['total_files']} ({info['progress_percentage']:.1f}%)")
        print(f"📊 Progress: {progress_bar}")
        print(f"✅ Successful: {info['processed_files']}")
        print(f"❌ Failed: {info['failed_files']}")
        
        if info['current_file']:
            print(f"🔄 Current: {info['current_file']}")
        
        print(f"⏱️  Elapsed: {info['elapsed_time']:.1f} seconds")
        print(f"📈 Rate: {info['files_per_minute']:.1f} files/minute")
        
        if info['eta']:
            print(f"🎯 ETA: {info['eta'].strftime('%H:%M:%S')}")
        
        print(f"💾 Memory: {info['memory_usage']:.1f} MB (peak: {info['peak_memory']:.1f} MB)")
        if info['memory_increase'] > 0:
            print(f"📈 Memory increase: +{info['memory_increase']:.1f} MB")
        print(f"{'='*60}")
    
    def _create_progress_bar(self, percentage: float, width: int = 30) -> str:
        """Create a visual progress bar."""
        filled_width = int((percentage / 100) * width)
        bar = '█' * filled_width + '░' * (width - filled_width)
        return f"[{bar}] {percentage:.1f}%"
    
    def display_final_summary(self) -> None:
        """Display final processing summary."""
        info = self.get_progress_info()
        
        print(f"\n{'='*80}")
        print(f"🎉 BATCH PROCESSING COMPLETE")
        print(f"{'='*80}")
        print(f"📊 Total files: {info['total_files']}")
        print(f"✅ Successful: {info['processed_files']}")
        print(f"❌ Failed: {info['failed_files']}")
        print(f"📈 Success rate: {(info['processed_files']/info['total_files']*100):.1f}%")
        print(f"⏱️  Total time: {info['elapsed_time']:.1f} seconds")
        print(f"📈 Average time per file: {info['avg_time_per_file']:.2f} seconds")
        print(f"📈 Processing rate: {info['files_per_minute']:.1f} files/minute")
        print(f"💾 Peak memory usage: {info['peak_memory']:.1f} MB")
        print(f"📈 Memory increase: +{info['memory_increase']:.1f} MB")
        print(f"{'='*80}")
    
    def cleanup_memory(self) -> None:
        """Force memory cleanup."""
        gc.collect()
        if self.verbose:
            current_memory = self._get_memory_usage()
            print(f"🧹 Memory cleanup completed. Current usage: {current_memory:.1f} MB")


class ProgressBar:
    """Simple progress bar for console output."""
    
    def __init__(self, total: int, width: int = 50):
        """
        Initialize progress bar.
        
        Args:
            total: Total number of items
            width: Width of progress bar in characters
        """
        self.total = total
        self.width = width
        self.current = 0
    
    def update(self, current: int) -> None:
        """
        Update progress bar.
        
        Args:
            current: Current progress
        """
        self.current = current
        percentage = (current / self.total) * 100 if self.total > 0 else 0
        filled_width = int((current / self.total) * self.width) if self.total > 0 else 0
        
        bar = '█' * filled_width + '░' * (self.width - filled_width)
        
        print(f"\rProgress: [{bar}] {percentage:.1f}% ({current}/{self.total})", end='', flush=True)
    
    def complete(self) -> None:
        """Mark progress bar as complete."""
        self.update(self.total)
        print()  # New line after completion
