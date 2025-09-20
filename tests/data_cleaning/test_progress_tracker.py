"""
Tests for Progress Tracker Module

This module contains comprehensive unit tests for the ProgressTracker classes.
"""

import pytest
import time
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from data_cleaning.progress_tracker import ProgressTracker, DetailedProgressTracker, BatchProgressTracker


class TestProgressTracker:
    """Test cases for ProgressTracker class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tracker = ProgressTracker(bar_width=20)
    
    def test_initialization(self):
        """Test tracker initialization."""
        assert self.tracker.bar_width == 20
        assert self.tracker.start_time is None
        assert self.tracker.current_step == 0
        assert self.tracker.total_steps == 0
        assert self.tracker.step_name == ""
    
    def test_format_time(self):
        """Test time formatting."""
        # Test seconds only
        assert self.tracker._format_time(30) == "00:30"
        
        # Test minutes and seconds
        assert self.tracker._format_time(90) == "01:30"
        
        # Test hours, minutes and seconds
        assert self.tracker._format_time(3661) == "01:01:01"
        
        # Test zero time
        assert self.tracker._format_time(0) == "00:00"
    
    def test_start_operation(self):
        """Test starting an operation."""
        self.tracker.start_operation(5, "Test Operation")
        
        assert self.tracker.total_steps == 5
        assert self.tracker.current_step == 0
        assert self.tracker.step_name == "Test Operation"
        assert self.tracker.start_time is not None
        assert not self.tracker._stop_event.is_set()
    
    def test_update_step(self):
        """Test updating step."""
        self.tracker.start_operation(5, "Test Operation")
        
        # Test incrementing step
        self.tracker.update_step("Step 1")
        assert self.tracker.current_step == 1
        assert self.tracker.step_name == "Step 1"
        
        # Test setting specific step
        self.tracker.update_step("Step 3", 3)
        assert self.tracker.current_step == 3
        assert self.tracker.step_name == "Step 3"
    
    def test_finish_operation(self):
        """Test finishing operation."""
        self.tracker.start_operation(5, "Test Operation")
        
        with patch('sys.stdout.write') as mock_write:
            self.tracker.finish_operation()
            
            # Should clear progress line and show completion
            assert mock_write.call_count >= 2
    
    def test_run_with_progress(self):
        """Test running function with progress tracking."""
        def test_func(x, y):
            time.sleep(0.1)  # Simulate work
            return x + y
        
        with patch('sys.stdout.write') as mock_write:
            result = self.tracker.run_with_progress(test_func, 2, 3)
            
            assert result == 5
            # Should have written progress updates
            assert mock_write.call_count > 0
    
    def test_run_with_progress_exception(self):
        """Test running function with progress tracking when exception occurs."""
        def test_func():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError):
            self.tracker.run_with_progress(test_func)
        
        # Should stop progress display even on exception
        assert self.tracker._stop_event.is_set()


class TestDetailedProgressTracker:
    """Test cases for DetailedProgressTracker class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.data = pd.DataFrame({
            'value': range(100)
        })
        self.tracker = DetailedProgressTracker(self.data, "Test Operation", 20)
    
    def test_initialization(self):
        """Test detailed tracker initialization."""
        assert self.tracker.data is self.data
        assert self.tracker.operation_name == "Test Operation"
        assert self.tracker.bar_width == 20
        assert self.tracker.total_rows == 100
        assert self.tracker.processed_rows == 0
        assert self.tracker.start_time is not None
    
    def test_update(self):
        """Test progress update."""
        with patch('sys.stdout.write') as mock_write:
            self.tracker.update(50)
            
            assert self.tracker.processed_rows == 50
            # Should have written progress update
            assert mock_write.call_count > 0
    
    def test_finish(self):
        """Test finishing detailed progress."""
        with patch('sys.stdout.write') as mock_write, \
             patch('builtins.print') as mock_print:
            
            self.tracker.finish()
            
            assert self.tracker.processed_rows == 100
            # Should have written final progress and completion message
            assert mock_write.call_count > 0
            assert mock_print.call_count > 0
    
    def test_format_time(self):
        """Test time formatting."""
        # Test seconds only
        assert self.tracker._format_time(30) == "00:30"
        
        # Test minutes and seconds
        assert self.tracker._format_time(90) == "01:30"
        
        # Test hours, minutes and seconds
        assert self.tracker._format_time(3661) == "01:01:01"
    
    def test_display_progress_zero_rows(self):
        """Test progress display with zero rows."""
        empty_data = pd.DataFrame({'value': []})
        tracker = DetailedProgressTracker(empty_data, "Empty Operation")
        
        with patch('sys.stdout.write') as mock_write:
            tracker._display_progress()
            
            # Should not write anything for zero rows
            assert mock_write.call_count == 0


class TestBatchProgressTracker:
    """Test cases for BatchProgressTracker class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tracker = BatchProgressTracker(5, "Test Batch")
    
    def test_initialization(self):
        """Test batch tracker initialization."""
        assert self.tracker.total_batches == 5
        assert self.tracker.current_batch == 0
        assert self.tracker.batch_name == "Test Batch"
        assert self.tracker.start_time is not None
    
    def test_start_batch(self):
        """Test starting a batch."""
        with patch('builtins.print') as mock_print:
            self.tracker.start_batch(0, "First batch")
            
            assert self.tracker.current_batch == 0
            assert mock_print.call_count == 1
            
            # Check printed content
            printed_text = mock_print.call_args[0][0]
            assert "Test Batch 1/5" in printed_text
            assert "First batch" in printed_text
    
    def test_start_batch_with_eta(self):
        """Test starting a batch with ETA calculation."""
        # Simulate some time passing
        time.sleep(0.1)
        
        with patch('builtins.print') as mock_print:
            self.tracker.start_batch(1, "Second batch")
            
            assert self.tracker.current_batch == 1
            assert mock_print.call_count == 1
            
            # Check that ETA is calculated
            printed_text = mock_print.call_args[0][0]
            assert "ETA:" in printed_text
    
    def test_finish(self):
        """Test finishing batch processing."""
        with patch('builtins.print') as mock_print:
            self.tracker.finish()
            
            assert mock_print.call_count == 1
            
            # Check printed content
            printed_text = mock_print.call_args[0][0]
            assert "All 5 batches completed" in printed_text
    
    def test_format_time(self):
        """Test time formatting."""
        # Test seconds only
        assert self.tracker._format_time(30) == "00:30"
        
        # Test minutes and seconds
        assert self.tracker._format_time(90) == "01:30"
        
        # Test hours, minutes and seconds
        assert self.tracker._format_time(3661) == "01:01:01"


class TestProgressTrackerIntegration:
    """Integration tests for progress tracking."""
    
    def test_create_detailed_progress(self):
        """Test creating detailed progress tracker."""
        data = pd.DataFrame({'value': range(50)})
        tracker = ProgressTracker()
        
        detailed_tracker = tracker.create_detailed_progress(data, "Integration Test")
        
        assert isinstance(detailed_tracker, DetailedProgressTracker)
        assert detailed_tracker.data is data
        assert detailed_tracker.operation_name == "Integration Test"
        assert detailed_tracker.bar_width == tracker.bar_width
    
    def test_progress_tracking_workflow(self):
        """Test complete progress tracking workflow."""
        tracker = ProgressTracker()
        
        # Start operation
        tracker.start_operation(3, "Test Workflow")
        
        # Update steps
        tracker.update_step("Step 1")
        assert tracker.current_step == 1
        
        tracker.update_step("Step 2")
        assert tracker.current_step == 2
        
        tracker.update_step("Step 3")
        assert tracker.current_step == 3
        
        # Finish operation
        with patch('sys.stdout.write') as mock_write, \
             patch('builtins.print') as mock_print:
            
            tracker.finish_operation()
            
            # Should clear progress and show completion
            assert mock_write.call_count > 0
            assert mock_print.call_count > 0
    
    def test_multiple_operations(self):
        """Test multiple operations with same tracker."""
        tracker = ProgressTracker()
        
        # First operation
        tracker.start_operation(2, "First Operation")
        tracker.update_step("Step 1")
        tracker.finish_operation()
        
        # Second operation
        tracker.start_operation(3, "Second Operation")
        tracker.update_step("Step 1")
        tracker.update_step("Step 2")
        tracker.update_step("Step 3")
        tracker.finish_operation()
        
        # Should work for both operations
        assert True  # If we get here without errors, test passes
