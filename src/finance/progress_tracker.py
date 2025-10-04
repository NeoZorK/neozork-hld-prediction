"""
Financial Analysis Progress Tracker

This module provides progress tracking functionality for financial analysis operations.
It follows the same patterns as existing progress trackers in the project.
"""

import time
import sys
from typing import Dict, Any, Optional
from .color_utils import ColorUtils


class FinanceProgressTracker:
    """Tracks progress of financial analysis operations."""
    
    def __init__(self, total_files: int = 1, verbose: bool = True):
        """
        Initialize progress tracker.
        
        Args:
            total_files: Total number of files to process
            verbose: Whether to show verbose output
        """
        self.total_files = total_files
        self.verbose = verbose
        self.current_file = 0
        self.successful_files = 0
        self.failed_files = 0
        self.start_time = None
        self.file_start_time = None
        self.current_filename = None
        
    def start_file(self, filename: str) -> None:
        """
        Start tracking a new file.
        
        Args:
            filename: Name of the file being processed
        """
        self.current_filename = filename
        self.file_start_time = time.time()
        
        if self.verbose:
            print(f"\n{ColorUtils.progress(f'Processing file {self.current_file + 1}/{self.total_files}: {filename}')}")
            print("=" * 80)
    
    def complete_file(self, success: bool = True, error_message: str = None) -> None:
        """
        Mark current file as completed.
        
        Args:
            success: Whether the file was processed successfully
            error_message: Error message if processing failed
        """
        if self.file_start_time:
            file_time = time.time() - self.file_start_time
            
            if success:
                self.successful_files += 1
                if self.verbose:
                    print(f"{ColorUtils.success(f'Completed in {file_time:.2f}s')}")
            else:
                self.failed_files += 1
                if self.verbose and error_message:
                    print(f"{ColorUtils.error(f'Failed: {error_message}')}")
        
        self.current_file += 1
        self.file_start_time = None
        self.current_filename = None
    
    def display_progress(self) -> None:
        """Display current progress."""
        if not self.verbose:
            return
        
        progress_percentage = (self.current_file / self.total_files) * 100 if self.total_files > 0 else 0
        progress_bar = ColorUtils.create_progress_bar(self.current_file, self.total_files)
        
        print(f"\n{ColorUtils.progress('Overall Progress:')} {progress_bar}")
        print(f"{ColorUtils.info(f'Files processed: {self.current_file}/{self.total_files}')}")
        print(f"{ColorUtils.success(f'Successful: {self.successful_files}')}")
        print(f"{ColorUtils.error(f'Failed: {self.failed_files}')}")
        
        if self.current_file < self.total_files:
            print(f"{ColorUtils.warning(f'Remaining: {self.total_files - self.current_file}')}")
    
    def display_final_summary(self) -> None:
        """Display final summary of processing."""
        if not self.verbose:
            return
        
        total_time = time.time() - self.start_time if self.start_time else 0
        
        print(f"\n{ColorUtils.header('FINANCIAL ANALYSIS COMPLETE')}")
        print("=" * 80)
        print(f"{ColorUtils.info(f'Total files processed: {self.total_files}')}")
        print(f"{ColorUtils.success(f'Successful: {self.successful_files}')}")
        print(f"{ColorUtils.error(f'Failed: {self.failed_files}')}")
        
        if self.total_files > 0:
            success_rate = (self.successful_files / self.total_files) * 100
            print(f"{ColorUtils.metric(f'Success rate: {success_rate:.1f}%')}")
        
        print(f"{ColorUtils.metric(f'Total processing time: {total_time:.2f}s')}")
        
        if self.successful_files > 0:
            avg_time = total_time / self.successful_files
            print(f"{ColorUtils.metric(f'Average time per file: {avg_time:.2f}s')}")
        
        print("=" * 80)
    
    def start_analysis(self) -> None:
        """Start the overall analysis."""
        self.start_time = time.time()
        if self.verbose:
            print(f"{ColorUtils.header('Starting Financial Analysis')}")
            print(f"{ColorUtils.info(f'Total files to process: {self.total_files}')}")
            print("=" * 80)
    
    def update_analysis_step(self, step: str, current: int, total: int) -> None:
        """
        Update analysis step progress.
        
        Args:
            step: Current analysis step
            current: Current step number
            total: Total number of steps
        """
        if not self.verbose:
            return
        
        progress_bar = ColorUtils.create_progress_bar(current, total)
        print(f"{ColorUtils.progress(f'{step}:')} {progress_bar}")


class ColumnProgressTracker:
    """Tracks progress for individual column analysis."""
    
    def __init__(self, column_name: str, analysis_type: str, total_steps: int):
        """
        Initialize column progress tracker.
        
        Args:
            column_name: Name of the column being analyzed
            analysis_type: Type of analysis being performed
            total_steps: Total number of steps in the analysis
        """
        self.column_name = column_name
        self.analysis_type = analysis_type
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = None
        
    def start_analysis(self) -> None:
        """Start tracking column analysis."""
        self.start_time = time.time()
        print(f"{ColorUtils.analysis(f'Analyzing {self.analysis_type} for column: {self.column_name}')}")
    
    def update_step(self, step_name: str) -> None:
        """
        Update current analysis step.
        
        Args:
            step_name: Name of the current step
        """
        self.current_step += 1
        progress_bar = ColorUtils.create_progress_bar(self.current_step, self.total_steps)
        print(f"  {ColorUtils.progress(f'{step_name}:')} {progress_bar}")
    
    def complete_analysis(self) -> None:
        """Mark analysis as completed."""
        if self.start_time:
            analysis_time = time.time() - self.start_time
            print(f"  {ColorUtils.success(f'Completed in {analysis_time:.2f}s')}")


class AnalysisProgressTracker:
    """Tracks progress for specific analysis types."""
    
    def __init__(self, analysis_type: str, total_columns: int):
        """
        Initialize analysis progress tracker.
        
        Args:
            analysis_type: Type of analysis being performed
            total_columns: Total number of columns to analyze
        """
        self.analysis_type = analysis_type
        self.total_columns = total_columns
        self.current_column = 0
        self.start_time = None
        
    def start_analysis(self) -> None:
        """Start tracking analysis."""
        self.start_time = time.time()
        print(f"\n{ColorUtils.header(f'{self.analysis_type.upper()} ANALYSIS')}")
        print("=" * 80)
        print(f"{ColorUtils.info(f'Analyzing {self.total_columns} columns...')}")
    
    def update_column(self, column_name: str) -> None:
        """
        Update current column being analyzed.
        
        Args:
            column_name: Name of the current column
        """
        self.current_column += 1
        progress_bar = ColorUtils.create_progress_bar(self.current_column, self.total_columns)
        print(f"{ColorUtils.progress(f'Column {self.current_column}/{self.total_columns} ({column_name}):')} {progress_bar}")
    
    def complete_analysis(self) -> None:
        """Mark analysis as completed."""
        if self.start_time:
            analysis_time = time.time() - self.start_time
            print(f"{ColorUtils.success(f'{self.analysis_type.title()} analysis completed in {analysis_time:.2f}s')}")
            print("=" * 80)
    
    def display_analysis_progress(self, current: int, total: int, step: str) -> None:
        """
        Display progress for specific analysis step.
        
        Args:
            current: Current progress
            total: Total progress
            step: Current step name
        """
        progress_bar = ColorUtils.create_progress_bar(current, total)
        print(f"  {ColorUtils.progress(f'{step}:')} {progress_bar}")


class BatchProgressTracker:
    """Tracks progress for batch processing operations."""
    
    def __init__(self, total_directories: int, verbose: bool = True):
        """
        Initialize batch progress tracker.
        
        Args:
            total_directories: Total number of directories to process
            verbose: Whether to show verbose output
        """
        self.total_directories = total_directories
        self.verbose = verbose
        self.current_directory = 0
        self.successful_directories = 0
        self.failed_directories = 0
        self.start_time = None
        
    def start_batch(self) -> None:
        """Start batch processing."""
        self.start_time = time.time()
        if self.verbose:
            print(f"{ColorUtils.header('Starting Batch Financial Analysis')}")
            print(f"{ColorUtils.info(f'Total directories to process: {self.total_directories}')}")
            print("=" * 80)
    
    def start_directory(self, directory_name: str) -> None:
        """
        Start processing a directory.
        
        Args:
            directory_name: Name of the directory being processed
        """
        self.current_directory += 1
        if self.verbose:
            print(f"\n{ColorUtils.progress(f'Processing directory {self.current_directory}/{self.total_directories}: {directory_name}')}")
            print("=" * 60)
    
    def complete_directory(self, success: bool = True, files_processed: int = 0, files_successful: int = 0, files_failed: int = 0) -> None:
        """
        Mark directory as completed.
        
        Args:
            success: Whether the directory was processed successfully
            files_processed: Number of files processed
            files_successful: Number of files processed successfully
            files_failed: Number of files that failed
        """
        if success:
            self.successful_directories += 1
            if self.verbose:
                print(f"{ColorUtils.success(f'Directory completed: {files_successful}/{files_processed} files successful')}")
        else:
            self.failed_directories += 1
            if self.verbose:
                print(f"{ColorUtils.error(f'Directory failed: {files_failed}/{files_processed} files failed')}")
    
    def display_final_summary(self) -> None:
        """Display final batch processing summary."""
        if not self.verbose:
            return
        
        total_time = time.time() - self.start_time if self.start_time else 0
        
        print(f"\n{ColorUtils.header('BATCH FINANCIAL ANALYSIS COMPLETE')}")
        print("=" * 80)
        print(f"{ColorUtils.info(f'Total directories processed: {self.total_directories}')}")
        print(f"{ColorUtils.success(f'Successful: {self.successful_directories}')}")
        print(f"{ColorUtils.error(f'Failed: {self.failed_directories}')}")
        
        if self.total_directories > 0:
            success_rate = (self.successful_directories / self.total_directories) * 100
            print(f"{ColorUtils.metric(f'Success rate: {success_rate:.1f}%')}")
        
        print(f"{ColorUtils.metric(f'Total processing time: {total_time:.2f}s')}")
        print("=" * 80)
