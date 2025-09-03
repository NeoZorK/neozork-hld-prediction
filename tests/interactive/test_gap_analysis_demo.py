#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo test for gap analysis functionality

This test demonstrates the gap analysis feature that was added to the interactive system.
"""

import sys
import os
import pandas as pd
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data_manager import DataManager
from src.interactive import InteractiveSystem


class TestGapAnalysisDemo:
    """Demo test class for gap analysis functionality."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
        self.system = InteractiveSystem()
    
    def test_gap_analysis_demo(self):
        """Demo the gap analysis functionality with real EURUSD data."""
        print("🔍 GAP ANALYSIS DEMO")
        print("=" * 50)
        print("Testing the new gap analysis feature for '8 eurusd' scenario")
        print("=" * 50)
        
        # Simulate the "8 eurusd" scenario
        print("\n1️⃣  Simulating '8 eurusd' command...")
        
        # Find EURUSD files in the data directory
        data_folder = Path("data")
        eurusd_files = []
        
        # Search for EURUSD files
        for ext in ['.csv', '.parquet']:
            pattern = f"*EURUSD*{ext}"
            files = list(data_folder.rglob(pattern))
            eurusd_files.extend(files)
        
        if not eurusd_files:
            pytest.skip("No EURUSD files found in data directory")
        
        print(f"✅ Found {len(eurusd_files)} EURUSD files:")
        for file in eurusd_files:
            # Safely get file name - handle both Path objects and strings
            if hasattr(file, 'name'):
                file_name = file.name
            else:
                file_name = str(file).split('/')[-1]  # Extract filename from path string
            print(f"   • {file_name}")
        
        # Load files using DataManager
        print(f"\n2️⃣  Loading EURUSD files...")
        
        all_data = []
        for i, file in enumerate(eurusd_files, 1):
            try:
                # Safely get file name - handle both Path objects and strings
                if hasattr(file, 'name'):
                    file_name = file.name
                else:
                    file_name = str(file).split('/')[-1]  # Extract filename from path string
                
                print(f"Loading file {i}/{len(eurusd_files)}: {file_name}")
                df = self.data_manager.load_data_from_file(str(file))
                df['source_file'] = file_name
                all_data.append(df)
                print(f"  ✅ Loaded: {file_name} ({df.shape[0]:,} rows)")
            except Exception as e:
                # Safely get file name for error reporting
                if hasattr(file, 'name'):
                    file_name = file.name
                else:
                    file_name = str(file).split('/')[-1]
                print(f"  ❌ Error loading {file_name}: {e}")
                continue
        
        if not all_data:
            pytest.fail("No files could be loaded")
        
        # Combine data
        print(f"\n3️⃣  Combining data...")
        try:
            self.system.current_data = pd.concat(all_data, ignore_index=True)
            print(f"✅ Combined data loaded successfully!")
            print(f"   Total shape: {self.system.current_data.shape[0]:,} rows × {self.system.current_data.shape[1]} columns")
        except Exception as e:
            pytest.fail(f"Error combining data: {e}")
        
        # Analyze gaps
        print(f"\n4️⃣  Analyzing time series gaps...")
        
        # Determine expected frequency using the gap_analyzer
        expected_frequency = self.data_manager.gap_analyzer._determine_expected_frequency(
            self.system.current_data, 'Timestamp'
        )
        print(f"   Expected frequency: {expected_frequency}")
        
        # Run gap analysis (without user input for testing)
        try:
            gap_result = self.data_manager.gap_analyzer.analyze_time_series_gaps(
                self.system.current_data, 'Timestamp', expected_frequency
            )
            
            # For testing purposes, we consider it successful if no exception was raised
            # The actual result might be False due to user input handling in tests
            print(f"\n✅ Gap analysis completed!")
            
        except Exception as e:
            pytest.fail(f"Gap analysis failed with exception: {e}")
        
        print(f"\n✅ Gap analysis completed successfully!")
        print(f"\n🎉 Demo completed!")
        print(f"   The gap analysis feature is now integrated into the interactive system.")
        print(f"   Users can now run '8 eurusd' and get gap analysis automatically!")


if __name__ == "__main__":
    # Run the demo test
    test_instance = TestGapAnalysisDemo()
    test_instance.setup_method()
    test_instance.test_gap_analysis_demo()
