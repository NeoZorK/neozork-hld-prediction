# tests/export/test_export_functionality.py

"""
Unit tests for export functionality (parquet, CSV, JSON).
Tests the new indicator export features.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.export.parquet_export import export_indicator_to_parquet
from src.export.csv_export import export_indicator_to_csv
from src.export.json_export import export_indicator_to_json
from src.common.constants import TradingRule


class TestExportFunctionality:
    """Test class for export functionality."""
    
    @pytest.fixture
    def sample_ohlcv_data(self):
        """Create sample OHLCV data with indicators for testing."""
        dates = pd.date_range('2024-01-01', periods=100, freq='H')
        
        # Generate realistic OHLCV data
        close_prices = 100 + np.cumsum(np.random.randn(100) * 0.1)
        high_prices = close_prices + np.random.uniform(0.1, 1.0, 100)
        low_prices = close_prices - np.random.uniform(0.1, 1.0, 100)
        open_prices = close_prices + np.random.uniform(-0.5, 0.5, 100)
        volumes = np.random.randint(1000, 10000, 100)
        
        df = pd.DataFrame({
            'open': open_prices,
            'high': high_prices,
            'low': low_prices,
            'close': close_prices,
            'volume': volumes,
            # Sample indicator columns
            'Pressure': np.random.uniform(-1, 1, 100),
            'PV': np.random.uniform(0, 100, 100),
            'Support': close_prices - np.random.uniform(1, 5, 100),
            'Resistance': close_prices + np.random.uniform(1, 5, 100)
        }, index=dates)
        
        return df
    
    @pytest.fixture
    def sample_data_info(self):
        """Create sample data info for testing."""
        return {
            "parquet_cache_file": None,
            "csv_file": None,
            "data_source_label": "Test Data",
            "mode": "test"
        }
    
    @pytest.fixture
    def sample_args_parquet(self):
        """Create sample args for parquet export."""
        args = Mock()
        args.export_parquet = True
        args.export_csv = False
        args.export_json = False
        args.mode = "test"
        args.ticker = "TESTPAIR"
        args.interval = "H1"
        return args
    
    @pytest.fixture
    def sample_args_csv(self):
        """Create sample args for CSV export."""
        args = Mock()
        args.export_parquet = False
        args.export_csv = True
        args.export_json = False
        args.mode = "test"
        args.ticker = "TESTPAIR"
        args.interval = "H1"
        return args
    
    @pytest.fixture
    def sample_args_json(self):
        """Create sample args for JSON export."""
        args = Mock()
        args.export_parquet = False
        args.export_csv = False
        args.export_json = True
        args.mode = "test"
        args.ticker = "TESTPAIR"
        args.interval = "H1"
        return args
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_path = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        os.chdir(temp_path)
        yield temp_path
        os.chdir(original_cwd)
        shutil.rmtree(temp_path)
    
    def test_parquet_export_success(self, sample_ohlcv_data, sample_data_info, sample_args_parquet, temp_dir):
        """Test successful parquet export."""
        selected_rule = TradingRule.Pressure_Vector
        
        result = export_indicator_to_parquet(
            sample_ohlcv_data, sample_data_info, selected_rule, sample_args_parquet
        )
        
        assert result["success"] is True
        assert result["output_file"] is not None
        assert "TESTPAIR_H1_PressureVector.parquet" in result["output_file"]
        
        # Check if file was actually created
        output_path = Path(result["output_file"])
        assert output_path.exists()
        
        # Check if we can read the file back
        df_loaded = pd.read_parquet(output_path)
        assert not df_loaded.empty
        assert 'open' in df_loaded.columns
        assert 'Pressure' in df_loaded.columns
    
    def test_csv_export_success(self, sample_ohlcv_data, sample_data_info, sample_args_csv, temp_dir):
        """Test successful CSV export."""
        selected_rule = TradingRule.Pressure_Vector
        
        result = export_indicator_to_csv(
            sample_ohlcv_data, sample_data_info, selected_rule, sample_args_csv
        )
        
        assert result["success"] is True
        assert result["output_file"] is not None
        assert "TESTPAIR_H1_PressureVector.csv" in result["output_file"]
        
        # Check if file was actually created
        output_path = Path(result["output_file"])
        assert output_path.exists()
        
        # Check if we can read the file back
        df_loaded = pd.read_csv(output_path)
        assert not df_loaded.empty
        assert 'open' in df_loaded.columns
        assert 'Pressure' in df_loaded.columns
    
    def test_json_export_success(self, sample_ohlcv_data, sample_data_info, sample_args_json, temp_dir):
        """Test successful JSON export."""
        selected_rule = TradingRule.Pressure_Vector
        
        result = export_indicator_to_json(
            sample_ohlcv_data, sample_data_info, selected_rule, sample_args_json
        )
        
        assert result["success"] is True
        assert result["output_file"] is not None
        assert "TESTPAIR_H1_PressureVector.json" in result["output_file"]
        
        # Check if file was actually created
        output_path = Path(result["output_file"])
        assert output_path.exists()
        
        # Check if we can read the file back
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert 'open' in data[0]
        assert 'Pressure' in data[0]
    
    def test_export_with_no_flag_set(self, sample_ohlcv_data, sample_data_info, temp_dir):
        """Test export when no export flag is set."""
        args = Mock()
        args.export_parquet = False
        args.export_csv = False
        args.export_json = False
        
        selected_rule = TradingRule.Pressure_Vector
        
        # Test all export functions return failure when flag not set
        result_parquet = export_indicator_to_parquet(sample_ohlcv_data, sample_data_info, selected_rule, args)
        result_csv = export_indicator_to_csv(sample_ohlcv_data, sample_data_info, selected_rule, args)
        result_json = export_indicator_to_json(sample_ohlcv_data, sample_data_info, selected_rule, args)
        
        assert result_parquet["success"] is False
        assert result_csv["success"] is False
        assert result_json["success"] is False
        
        assert "Export flag not set" in result_parquet["error_message"]
        assert "Export CSV flag not set" in result_csv["error_message"]
        assert "Export JSON flag not set" in result_json["error_message"]
    
    def test_export_with_empty_dataframe(self, sample_data_info, sample_args_parquet, temp_dir):
        """Test export with empty DataFrame."""
        empty_df = pd.DataFrame()
        selected_rule = TradingRule.Pressure_Vector
        
        result = export_indicator_to_parquet(empty_df, sample_data_info, selected_rule, sample_args_parquet)
        
        assert result["success"] is False
        assert "No data to export" in result["error_message"]
    
    def test_export_with_none_dataframe(self, sample_data_info, sample_args_parquet, temp_dir):
        """Test export with None DataFrame."""
        selected_rule = TradingRule.Pressure_Vector
        
        result = export_indicator_to_parquet(None, sample_data_info, selected_rule, sample_args_parquet)
        
        assert result["success"] is False
        assert "No data to export" in result["error_message"]
    
    def test_export_directory_creation(self, sample_ohlcv_data, sample_data_info, sample_args_parquet, temp_dir):
        """Test that export creates the necessary directories."""
        selected_rule = TradingRule.Support_Resistants
        
        # Make sure directories don't exist initially
        parquet_dir = Path("data/indicators/parquet")
        csv_dir = Path("data/indicators/csv") 
        json_dir = Path("data/indicators/json")
        
        assert not parquet_dir.exists()
        
        # Test parquet export creates directory
        result = export_indicator_to_parquet(sample_ohlcv_data, sample_data_info, selected_rule, sample_args_parquet)
        assert result["success"] is True
        assert parquet_dir.exists()
        
        # Test CSV export creates directory
        sample_args_parquet.export_parquet = False
        sample_args_parquet.export_csv = True
        result = export_indicator_to_csv(sample_ohlcv_data, sample_data_info, selected_rule, sample_args_parquet)
        assert result["success"] is True
        assert csv_dir.exists()
        
        # Test JSON export creates directory
        sample_args_parquet.export_csv = False
        sample_args_parquet.export_json = True
        result = export_indicator_to_json(sample_ohlcv_data, sample_data_info, selected_rule, sample_args_parquet)
        assert result["success"] is True
        assert json_dir.exists()
    
    def test_filename_generation_with_rule_enum(self, sample_ohlcv_data, sample_data_info, sample_args_parquet, temp_dir):
        """Test filename generation with different rule enums."""
        rules_to_test = [
            (TradingRule.Pressure_Vector, "PressureVector"),
            (TradingRule.Support_Resistants, "SupportResistants"),
            (TradingRule.Predict_High_Low_Direction, "PredictHighLowDirection")
        ]
        
        for rule_enum, expected_name in rules_to_test:
            result = export_indicator_to_parquet(sample_ohlcv_data, sample_data_info, rule_enum, sample_args_parquet)
            assert result["success"] is True
            assert expected_name in result["output_file"]


if __name__ == "__main__":
    pytest.main([__file__])
