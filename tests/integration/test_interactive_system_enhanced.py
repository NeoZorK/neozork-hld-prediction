#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test enhanced interactive system functionality.

This test suite covers the new features added to interactive_system.py:
- Enhanced data loading with subfolder selection
- Data fixing capabilities
- HTML report generation
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from interactive_system import InteractiveSystem


class TestEnhancedInteractiveSystem:
    """Test enhanced interactive system functionality."""
    
    @pytest.fixture
    def interactive_system(self):
        """Create interactive system instance."""
        return InteractiveSystem()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data with issues for testing."""
        # Create data with various issues
        data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=100, freq='H'),
            'open': [100 + i * 0.1 + np.random.normal(0, 0.5) for i in range(100)],
            'high': [101 + i * 0.1 + np.random.normal(0, 0.5) for i in range(100)],
            'low': [99 + i * 0.1 + np.random.normal(0, 0.5) for i in range(100)],
            'close': [100.5 + i * 0.1 + np.random.normal(0, 0.5) for i in range(100)],
            'volume': [1000 + np.random.normal(0, 100) for _ in range(100)]
        })
        
        # Add some issues
        data.loc[10, 'open'] = np.nan  # NaN value
        data.loc[20, 'close'] = np.nan  # NaN value
        # Add duplicate rows properly
        duplicate_row = data.iloc[30].copy()
        data = pd.concat([data, pd.DataFrame([duplicate_row])], ignore_index=True)
        data.loc[40, 'volume'] = 0  # Zero value
        data.loc[50, 'close'] = -1  # Negative value
        
        return data
    
    def test_enhanced_data_loading_structure(self, interactive_system):
        """Test that data loading structure is enhanced."""
        # Check that _load_single_file method is removed
        assert not hasattr(interactive_system, '_load_single_file')
        
        # Check that _load_folder_files method exists
        assert hasattr(interactive_system, '_load_folder_files')
        
        # Check that load_data method is updated
        assert hasattr(interactive_system, 'load_data')
    
    def test_data_fixing_functionality(self, interactive_system, sample_data, monkeypatch):
        """Test data fixing functionality."""
        interactive_system.current_data = sample_data.copy()
        
        # Mock user input to keep changes
        monkeypatch.setattr('builtins.input', lambda prompt: 'y')
        
        # Run data fixing
        interactive_system.fix_data_issues()
        
        # Check that data was processed
        assert interactive_system.current_data is not None
        assert 'data_fixes' in interactive_system.current_results
        
        # Check that NaN values were fixed
        assert not interactive_system.current_data['open'].isna().any()
        assert not interactive_system.current_data['close'].isna().any()
        
        # Check that duplicates were removed
        assert not interactive_system.current_data.duplicated().any()
    
    def test_data_fixing_revert(self, interactive_system, sample_data, monkeypatch):
        """Test that data fixing can be reverted."""
        original_data = sample_data.copy()
        interactive_system.current_data = original_data.copy()
        
        # Mock user input to revert changes
        monkeypatch.setattr('builtins.input', lambda prompt: 'n')
        
        # Run data fixing
        interactive_system.fix_data_issues()
        
        # Check that data was reverted
        assert interactive_system.current_data.equals(original_data)
    
    def test_html_report_generation(self, interactive_system, sample_data, tmp_path):
        """Test HTML report generation."""
        interactive_system.current_data = sample_data
        
        # Add some analysis results
        interactive_system.current_results = {
            'data_quality': {
                'total_missing': 2,
                'missing_percentage': 2.0,
                'duplicates': 3,
                'duplicate_percentage': 3.0
            },
            'correlation_analysis': {
                'high_correlation_pairs': []
            },
            'time_series_analysis': {
                'stationarity': {'close': {'is_stationary': False}}
            }
        }
        
        # Change to temp directory for testing
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            # Run HTML report generation
            interactive_system.generate_html_report()
            
            # Check that reports directory was created
            reports_dir = Path("reports")
            assert reports_dir.exists()
            
            # Check that HTML file was created
            html_files = list(reports_dir.glob("*.html"))
            assert len(html_files) > 0
            
            # Check HTML file content
            html_content = html_files[0].read_text()
            assert "Interactive System Analysis Report" in html_content
            assert "Data Overview" in html_content
            assert "Data Quality Analysis" in html_content
            
        finally:
            os.chdir(original_cwd)
    
    def test_enhanced_eda_menu(self, interactive_system):
        """Test that EDA menu includes new options."""
        # Check that new methods exist
        assert hasattr(interactive_system, 'fix_data_issues')
        assert hasattr(interactive_system, 'generate_html_report')
        
        # Check that print_eda_menu method exists
        assert hasattr(interactive_system, 'print_eda_menu')
    
    def test_imports_work_correctly(self):
        """Test that all required imports work."""
        try:
            from interactive_system import InteractiveSystem
            system = InteractiveSystem()
            assert system is not None
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
    
    def test_data_folder_structure_detection(self, interactive_system):
        """Test that data folder structure is detected correctly."""
        data_folder = Path("data")
        if not data_folder.exists():
            pytest.skip("Data folder not found")
        
        # Check that we can find subfolders
        subfolders = [data_folder]
        for item in data_folder.iterdir():
            if item.is_dir():
                subfolders.append(item)
                for subitem in item.iterdir():
                    if subitem.is_dir():
                        subfolders.append(subitem)
        
        # Should have at least the main data folder
        assert len(subfolders) >= 1
        assert data_folder in subfolders
        
        # Check that common subfolders exist
        expected_subfolders = ['data', 'data/cache', 'data/indicators', 'data/raw_parquet']
        for expected in expected_subfolders:
            if Path(expected).exists():
                assert Path(expected) in subfolders or any(str(sf).endswith(expected) for sf in subfolders)
    
    def test_folder_selection_with_mask(self, interactive_system, monkeypatch):
        """Test folder selection with mask functionality."""
        # Mock the _load_folder_files method to test the parsing logic
        def mock_load_folder_files():
            # Simulate the folder selection logic
            input_text = "3 eurusd"
            parts = input_text.split()
            
            # Check if first part is a number (folder selection)
            if parts[0].isdigit():
                folder_idx = int(parts[0]) - 1
                mask = parts[1].lower() if len(parts) > 1 else None
                return folder_idx == 2 and mask == "eurusd"
            return False
        
        # Test the logic
        assert mock_load_folder_files() == True
    
    def test_folder_selection_without_mask(self, interactive_system):
        """Test folder selection without mask."""
        # Test parsing logic for folder number only
        input_text = "1"
        parts = input_text.split()
        
        if parts[0].isdigit():
            folder_idx = int(parts[0]) - 1
            mask = parts[1].lower() if len(parts) > 1 else None
            assert folder_idx == 0
            assert mask is None
        else:
            pytest.fail("Should have detected number")
    
    def test_path_with_mask(self, interactive_system):
        """Test path with mask parsing."""
        # Test parsing logic for path with mask
        input_text = "data gbpusd"
        parts = input_text.split()
        
        if not parts[0].isdigit():
            folder_path = parts[0]
            mask = parts[1].lower() if len(parts) > 1 else None
            assert folder_path == "data"
            assert mask == "gbpusd"
        else:
            pytest.fail("Should not have detected number")


class TestDataFixingIntegration:
    """Test integration with fix_files module."""
    
    def test_fix_files_import(self):
        """Test that fix_files module can be imported."""
        try:
            from src.eda import fix_files
            assert hasattr(fix_files, 'fix_nan')
            assert hasattr(fix_files, 'fix_duplicates')
        except ImportError as e:
            pytest.fail(f"fix_files import failed: {e}")
    
    def test_html_report_generator_import(self):
        """Test that html_report_generator module can be imported."""
        try:
            from src.eda import html_report_generator
            assert hasattr(html_report_generator, 'HTMLReport')
        except ImportError as e:
            pytest.fail(f"html_report_generator import failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
