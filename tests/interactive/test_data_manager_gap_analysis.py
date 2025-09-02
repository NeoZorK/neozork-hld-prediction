#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for DataManager Gap Analysis Integration

This module tests the integration of time series gap analysis
with the DataManager class.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import tempfile
import os
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data_manager import DataManager
from src.interactive import InteractiveSystem


class TestDataManagerGapAnalysis:
    """Test cases for DataManager gap analysis integration."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
        self.system = InteractiveSystem()
    
    def test_analyze_time_series_gaps(self):
        """Test analyzing time series gaps in loaded files using EDA functionality."""
        # Create temporary files with gaps
        temp_files = []
        
        # File 1: With gaps
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Timestamp,value\n")
            f.write("2024-01-01 10:00:00,1\n")
            f.write("2024-01-01 11:00:00,2\n")
            f.write("2024-01-01 13:00:00,3\n")  # Gap of 2 hours
            f.write("2024-01-01 14:00:00,4\n")
            temp_files.append(Path(f.name))
        
        # File 2: Without gaps
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Timestamp,value\n")
            f.write("2024-01-01 15:00:00,5\n")
            f.write("2024-01-01 16:00:00,6\n")
            f.write("2024-01-01 17:00:00,7\n")
            temp_files.append(Path(f.name))
        
        try:
            # Test gap analysis using EDA functionality
            result = self.data_manager.analyze_time_series_gaps(
                temp_files, 'Timestamp', '1H'
            )
            
            assert result == True  # Method should return True on success
            
        finally:
            for temp_file in temp_files:
                os.unlink(temp_file)
    
    def test_determine_expected_frequency(self):
        """Test determining expected frequency from data."""
        # Test hourly data
        dates = pd.date_range('2024-01-01', periods=10, freq='1H')
        df = pd.DataFrame({'Timestamp': dates, 'value': range(10)})
        
        frequency = self.data_manager._determine_expected_frequency(df, 'Timestamp')
        assert frequency == '1H'
        
        # Test daily data
        dates = pd.date_range('2024-01-01', periods=10, freq='1D')
        df = pd.DataFrame({'Timestamp': dates, 'value': range(10)})
        
        frequency = self.data_manager._determine_expected_frequency(df, 'Timestamp')
        assert frequency == '1D'
        
        # Test minute data
        dates = pd.date_range('2024-01-01', periods=10, freq='1T')
        df = pd.DataFrame({'Timestamp': dates, 'value': range(10)})
        
        frequency = self.data_manager._determine_expected_frequency(df, 'Timestamp')
        assert frequency == '1T'
    
    def test_determine_expected_frequency_missing_column(self):
        """Test determining frequency with missing datetime column."""
        df = pd.DataFrame({'value': range(10)})
        
        frequency = self.data_manager._determine_expected_frequency(df, 'Timestamp')
        assert frequency == '1H'  # Default value
    
    def test_determine_expected_frequency_insufficient_data(self):
        """Test determining frequency with insufficient data."""
        df = pd.DataFrame({
            'Timestamp': pd.to_datetime(['2024-01-01 10:00:00']),
            'value': [1]
        })
        
        frequency = self.data_manager._determine_expected_frequency(df, 'Timestamp')
        assert frequency == '1H'  # Default value
    
    def test_gap_analysis_enabled(self):
        """Test that gap analysis is properly enabled."""
        assert hasattr(self.data_manager, 'gap_analysis_enabled')
        assert self.data_manager.gap_analysis_enabled == True
    
    def test_show_detailed_gap_info_from_eda(self):
        """Test showing detailed gap information using EDA results."""
        # Create mock gap summary
        gap_summary = [
            {
                'file': 'test1.csv',
                'column': 'Timestamp',
                'gaps_count': 2,
                'largest_gap': '2 hours',
                'method': 'direct',
                'from': '2024-01-01 11:00:00',
                'to': '2024-01-01 13:00:00',
                'delta': '2 hours'
            },
            {
                'file': 'test2.csv',
                'column': 'Timestamp',
                'gaps_count': 0,
                'method': 'direct'
            }
        ]
        
        # Import colorama for testing
        import colorama
        from colorama import Fore, Style
        colorama.init(autoreset=True)
        
        # Test that the method doesn't raise any exceptions
        try:
            self.data_manager._show_detailed_gap_info_from_eda(gap_summary, Fore, Style)
        except Exception as e:
            pytest.fail(f"Method raised unexpected exception: {e}")
    
    def test_real_user_scenario_with_gap_analysis(self):
        """Test the real user scenario with gap analysis integration."""
        print("🧪 Testing Real User Scenario with Gap Analysis...")
        print("=" * 60)
        print("Scenario: Load Data -> '8 eurusd' -> Gap Analysis")
        print("=" * 60)
        
        # Create test files simulating EURUSD data
        temp_files = []
        
        # File 1: EURUSD data with gaps
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Timestamp,Open,High,Low,Close,Volume\n")
            f.write("2024-01-01 10:00:00,1.1000,1.1005,1.0995,1.1002,1000\n")
            f.write("2024-01-01 11:00:00,1.1002,1.1008,1.1000,1.1005,1200\n")
            f.write("2024-01-01 13:00:00,1.1005,1.1010,1.1003,1.1008,1100\n")  # Gap
            f.write("2024-01-01 14:00:00,1.1008,1.1012,1.1006,1.1010,1300\n")
            temp_files.append(Path(f.name))
        
        # File 2: EURUSD data without gaps
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Timestamp,Open,High,Low,Close,Volume\n")
            f.write("2024-01-01 15:00:00,1.1010,1.1015,1.1008,1.1012,1400\n")
            f.write("2024-01-01 16:00:00,1.1012,1.1018,1.1010,1.1015,1500\n")
            f.write("2024-01-01 17:00:00,1.1015,1.1020,1.1012,1.1018,1600\n")
            temp_files.append(Path(f.name))
        
        try:
            # Step 1: Load files using DataManager
            print("\n1️⃣  Step 1: Loading EURUSD files...")
            
            all_data = []
            for i, file in enumerate(temp_files):
                try:
                    print(f"Loading file {i+1}/{len(temp_files)}: {file.name}")
                    df = self.data_manager.load_data_from_file(str(file))
                    df['source_file'] = file.name
                    all_data.append(df)
                    print(f"  ✅ Loaded: {file.name} ({df.shape[0]:,} rows)")
                except Exception as e:
                    print(f"  ❌ Error loading {file.name}: {e}")
                    continue
            
            if not all_data:
                pytest.fail("No files could be loaded")
            
            # Step 2: Combine data
            print(f"\n2️⃣  Step 2: Combining data...")
            
            try:
                self.system.current_data = pd.concat(all_data, ignore_index=True)
                print(f"✅ Combined data loaded successfully!")
                print(f"   Total shape: {self.system.current_data.shape[0]:,} rows × {self.system.current_data.shape[1]} columns")
            except Exception as e:
                pytest.fail(f"Error combining data: {e}")
            
            # Step 3: Analyze gaps
            print(f"\n3️⃣  Step 3: Analyzing time series gaps...")
            
            # Determine expected frequency
            expected_frequency = self.data_manager._determine_expected_frequency(
                self.system.current_data, 'Timestamp'
            )
            print(f"   Expected frequency: {expected_frequency}")
            
            # Analyze gaps
            gap_result = self.data_manager.analyze_time_series_gaps(
                temp_files, 'Timestamp', expected_frequency
            )
            
            assert gap_result == True, "Gap analysis should complete successfully"
            
            print(f"\n✅ Gap analysis completed successfully!")
            
        finally:
            for temp_file in temp_files:
                os.unlink(temp_file)


if __name__ == "__main__":
    # Run tests
    test_instance = TestDataManagerGapAnalysis()
    test_instance.setup_method()
    
    print("🧪 Testing DataManager Gap Analysis Integration...")
    print("=" * 60)
    
    # Test real user scenario with gap analysis
    print("\n1️⃣  Testing real user scenario with gap analysis...")
    test_instance.test_real_user_scenario_with_gap_analysis()
    print("✅ Real user scenario with gap analysis test completed")
    
    print("\n🎉 All tests completed!")
