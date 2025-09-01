#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for Timestamp NaN issue fix

This test verifies that the DataManager correctly handles DatetimeIndex
and preserves timestamp information without creating NaN values.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

from src.interactive.data_manager import DataManager


class TestTimestampFix:
    """Test class for Timestamp NaN issue fix."""
    
    @pytest.fixture
    def data_manager(self):
        """Create a DataManager instance for testing."""
        return DataManager()
    
    @pytest.fixture
    def sample_data_with_datetime_index(self):
        """Create sample data with DatetimeIndex for testing."""
        dates = pd.date_range('2023-01-01', periods=1000, freq='H')
        data = {
            'Low': np.random.uniform(1.0, 2.0, 1000),
            'Close': np.random.uniform(1.0, 2.0, 1000),
            'High': np.random.uniform(1.0, 2.0, 1000),
            'Open': np.random.uniform(1.0, 2.0, 1000),
            'Volume': np.random.randint(100, 1000, 1000),
            'predicted_low': np.random.uniform(0.0, 1.0, 1000),
            'predicted_high': np.random.uniform(0.0, 1.0, 1000),
            'pressure': np.random.uniform(0.0, 1.0, 1000),
            'pressure_vector': np.random.uniform(0.0, 1.0, 1000)
        }
        df = pd.DataFrame(data, index=dates)
        df.index.name = 'Timestamp'
        return df
    
    @pytest.fixture
    def sample_data_without_datetime_index(self):
        """Create sample data without DatetimeIndex for testing."""
        data = {
            'Timestamp': pd.date_range('2023-01-01', periods=1000, freq='H'),
            'Low': np.random.uniform(1.0, 2.0, 1000),
            'Close': np.random.uniform(1.0, 2.0, 1000),
            'High': np.random.uniform(1.0, 2.0, 1000),
            'Open': np.random.uniform(1.0, 2.0, 1000),
            'Volume': np.random.randint(100, 1000, 1000),
            'predicted_low': np.random.uniform(0.0, 1.0, 1000),
            'predicted_high': np.random.uniform(0.0, 1.0, 1000),
            'pressure': np.random.uniform(0.0, 1.0, 1000),
            'pressure_vector': np.random.uniform(0.0, 1.0, 1000)
        }
        df = pd.DataFrame(data)
        return df
    
    def test_handle_datetime_index_with_datetime_index(self, data_manager, sample_data_with_datetime_index):
        """Test _handle_datetime_index with DatetimeIndex."""
        df = sample_data_with_datetime_index.copy()
        
        # Process the DataFrame
        result = data_manager._handle_datetime_index(df)
        
        # Check that Timestamp column exists and has no NaN values
        assert 'Timestamp' in result.columns
        assert result['Timestamp'].isna().sum() == 0
        assert len(result) == 1000
        
        # Check that the original data is preserved
        assert all(col in result.columns for col in ['Low', 'Close', 'High', 'Open', 'Volume'])
    
    def test_handle_datetime_index_without_datetime_index(self, data_manager, sample_data_without_datetime_index):
        """Test _handle_datetime_index without DatetimeIndex."""
        df = sample_data_without_datetime_index.copy()
        
        # Process the DataFrame
        result = data_manager._handle_datetime_index(df)
        
        # Check that Timestamp column exists and has no NaN values
        assert 'Timestamp' in result.columns
        assert result['Timestamp'].isna().sum() == 0
        assert len(result) == 1000
        
        # Check that the original data is preserved
        assert all(col in result.columns for col in ['Low', 'Close', 'High', 'Open', 'Volume'])
    
    def test_load_parquet_with_datetime_index(self, data_manager, sample_data_with_datetime_index):
        """Test loading parquet file with DatetimeIndex."""
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file:
            # Save sample data to parquet
            sample_data_with_datetime_index.to_parquet(tmp_file.name)
            
            try:
                # Load the parquet file
                result = data_manager.load_data_from_file(tmp_file.name)
                
                # Check that Timestamp column exists and has no NaN values
                assert 'Timestamp' in result.columns
                assert result['Timestamp'].isna().sum() == 0
                assert len(result) == 1000
                
                # Check that the original data is preserved
                assert all(col in result.columns for col in ['Low', 'Close', 'High', 'Open', 'Volume'])
                
            finally:
                # Clean up
                os.unlink(tmp_file.name)
    
    def test_load_parquet_without_datetime_index(self, data_manager, sample_data_without_datetime_index):
        """Test loading parquet file without DatetimeIndex."""
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file:
            # Save sample data to parquet
            sample_data_without_datetime_index.to_parquet(tmp_file.name)
            
            try:
                # Load the parquet file
                result = data_manager.load_data_from_file(tmp_file.name)
                
                # Check that Timestamp column exists and has no NaN values
                assert 'Timestamp' in result.columns
                assert result['Timestamp'].isna().sum() == 0
                assert len(result) == 1000
                
                # Check that the original data is preserved
                assert all(col in result.columns for col in ['Low', 'Close', 'High', 'Open', 'Volume'])
                
            finally:
                # Clean up
                os.unlink(tmp_file.name)
    
    def test_mixed_data_concatenation(self, data_manager, sample_data_with_datetime_index, sample_data_without_datetime_index):
        """Test concatenation of mixed data structures."""
        # Create two DataFrames with different structures
        df1 = sample_data_with_datetime_index.copy()
        df2 = sample_data_without_datetime_index.copy()
        
        # Add source file info
        df1['source_file'] = 'file1.parquet'
        df2['source_file'] = 'file2.parquet'
        
        # Load both files using the data manager
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file1:
            with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file2:
                # Save sample data to parquet files
                df1.to_parquet(tmp_file1.name)
                df2.to_parquet(tmp_file2.name)
                
                try:
                    # Load both files
                    result1 = data_manager.load_data_from_file(tmp_file1.name)
                    result2 = data_manager.load_data_from_file(tmp_file2.name)
                    
                    # Add source file info
                    result1['source_file'] = 'file1.parquet'
                    result2['source_file'] = 'file2.parquet'
                    
                    # Simulate the concatenation logic from load_data method
                    all_data = [result1, result2]
                    
                    # Check if any DataFrames have DatetimeIndex
                    has_datetime_index = any(isinstance(df.index, pd.DatetimeIndex) for df in all_data)
                    
                    if has_datetime_index:
                        # Convert DatetimeIndex to 'Timestamp' column for consistent concatenation
                        processed_data = []
                        for df in all_data:
                            df_copy = df.copy()
                            if isinstance(df_copy.index, pd.DatetimeIndex):
                                # Reset index to make datetime a column
                                df_copy = df_copy.reset_index()
                                # Rename the index column if it's unnamed
                                if df_copy.columns[0] == 'index':
                                    df_copy = df_copy.rename(columns={'index': 'Timestamp'})
                            processed_data.append(df_copy)
                        
                        # Combine DataFrames with consistent column structure
                        combined_data = pd.concat(processed_data, ignore_index=True)
                    else:
                        # Check for mixed structures
                        has_timestamp_column = any('Timestamp' in df.columns for df in all_data)
                        missing_timestamp_column = any('Timestamp' not in df.columns for df in all_data)
                        
                        if has_timestamp_column and missing_timestamp_column:
                            # Process all DataFrames to ensure consistent structure
                            processed_data = []
                            for i, df in enumerate(all_data):
                                df_copy = df.copy()
                                
                                if 'Timestamp' not in df_copy.columns:
                                    # Create a dummy Timestamp column for files without it
                                    df_copy['Timestamp'] = pd.NaT
                                
                                processed_data.append(df_copy)
                            
                            # Combine DataFrames with consistent column structure
                            combined_data = pd.concat(processed_data, ignore_index=True)
                        else:
                            # All files have consistent structure, use standard concatenation
                            combined_data = pd.concat(all_data, ignore_index=True)
                    
                    # Check final result
                    assert 'Timestamp' in combined_data.columns
                    assert len(combined_data) == 2000  # 1000 + 1000
                    
                    # Check that there are no NaN values in Timestamp column
                    nan_count = combined_data['Timestamp'].isna().sum()
                    assert nan_count == 0, f"Found {nan_count} NaN values in Timestamp column"
                    
                    # Check source file distribution
                    source_files = combined_data['source_file'].value_counts()
                    assert source_files['file1.parquet'] == 1000
                    assert source_files['file2.parquet'] == 1000
                    
                finally:
                    # Clean up
                    os.unlink(tmp_file1.name)
                    os.unlink(tmp_file2.name)
    
    def test_real_eurusd_files(self, data_manager):
        """Test with real EURUSD files to ensure the fix works."""
        # Check if EURUSD files exist
        csv_converted_folder = Path("data/cache/csv_converted")
        eurusd_files = list(csv_converted_folder.glob("CSVExport_EURUSD_PERIOD_*.parquet"))
        
        if not eurusd_files:
            pytest.skip("No EURUSD files found for testing")
        
        # Test with a few EURUSD files
        test_files = eurusd_files[:3]  # Test first 3 files
        
        all_data = []
        for file in test_files:
            try:
                # Load file using data manager
                df = data_manager.load_data_from_file(str(file))
                df['source_file'] = file.name
                
                # Check that Timestamp column exists and has no NaN values
                if 'Timestamp' in df.columns:
                    nan_count = df['Timestamp'].isna().sum()
                    assert nan_count == 0, f"Found {nan_count} NaN values in {file.name}"
                
                all_data.append(df)
                
            except Exception as e:
                pytest.fail(f"Failed to load {file.name}: {e}")
        
        if all_data:
            # Test concatenation
            # Check if any DataFrames have DatetimeIndex
            has_datetime_index = any(isinstance(df.index, pd.DatetimeIndex) for df in all_data)
            
            if has_datetime_index:
                # Convert DatetimeIndex to 'Timestamp' column for consistent concatenation
                processed_data = []
                for df in all_data:
                    df_copy = df.copy()
                    if isinstance(df_copy.index, pd.DatetimeIndex):
                        # Reset index to make datetime a column
                        df_copy = df_copy.reset_index()
                        # Rename the index column if it's unnamed
                        if df_copy.columns[0] == 'index':
                            df_copy = df_copy.rename(columns={'index': 'Timestamp'})
                    processed_data.append(df_copy)
                
                # Combine DataFrames with consistent column structure
                combined_data = pd.concat(processed_data, ignore_index=True)
            else:
                # Check for mixed structures
                has_timestamp_column = any('Timestamp' in df.columns for df in all_data)
                missing_timestamp_column = any('Timestamp' not in df.columns for df in all_data)
                
                if has_timestamp_column and missing_timestamp_column:
                    # Process all DataFrames to ensure consistent structure
                    processed_data = []
                    for i, df in enumerate(all_data):
                        df_copy = df.copy()
                        
                        if 'Timestamp' not in df_copy.columns:
                            # Create a dummy Timestamp column for files without it
                            df_copy['Timestamp'] = pd.NaT
                        
                        processed_data.append(df_copy)
                    
                    # Combine DataFrames with consistent column structure
                    combined_data = pd.concat(processed_data, ignore_index=True)
                else:
                    # All files have consistent structure, use standard concatenation
                    combined_data = pd.concat(all_data, ignore_index=True)
            
            # Check final result
            assert 'Timestamp' in combined_data.columns
            nan_count = combined_data['Timestamp'].isna().sum()
            assert nan_count == 0, f"Found {nan_count} NaN values in Timestamp column after concatenation"
