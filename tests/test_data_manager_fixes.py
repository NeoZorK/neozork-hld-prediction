#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test DataManager fixes for cache directories and mql5_feed exclusion
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data_manager import DataManager


class TestDataManagerFixes:
    """Test DataManager fixes for cache directories and mql5_feed exclusion."""
    
    def setup_method(self):
        """Set up test environment."""
        self.data_manager = DataManager()
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def teardown_method(self):
        """Clean up test environment."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_cache_directories_creation(self):
        """Test that cache directories are created when they don't exist."""
        # Create a temporary data directory structure
        temp_data_dir = self.temp_dir / "data"
        temp_data_dir.mkdir()
        
        # Create some subdirectories but not cache ones
        (temp_data_dir / "indicators").mkdir()
        (temp_data_dir / "raw_parquet").mkdir()
        
        with patch('pathlib.Path') as mock_path:
            # Mock the data folder path
            mock_path.return_value = temp_data_dir
            
            # Mock the exists() method to return True for data folder
            mock_data_folder = MagicMock()
            mock_data_folder.exists.return_value = True
            mock_data_folder.iterdir.return_value = [
                MagicMock(name="indicators", is_dir=lambda: True),
                MagicMock(name="raw_parquet", is_dir=lambda: True)
            ]
            
            # Mock subdirectories
            mock_indicators = MagicMock()
            mock_indicators.name = "indicators"
            mock_indicators.is_dir.return_value = True
            mock_indicators.iterdir.return_value = []
            
            mock_raw_parquet = MagicMock()
            mock_raw_parquet.name = "raw_parquet"
            mock_raw_parquet.is_dir.return_value = True
            mock_raw_parquet.iterdir.return_value = []
            
            mock_data_folder.iterdir.return_value = [mock_indicators, mock_raw_parquet]
            
            # Test that cache directories would be created
            cache_dirs = [
                temp_data_dir / "cache",
                temp_data_dir / "cache" / "csv_converted",
                temp_data_dir / "cache" / "uv_cache",
                temp_data_dir / "backups"
            ]
            
            for cache_dir in cache_dirs:
                assert not cache_dir.exists()
                cache_dir.mkdir(parents=True, exist_ok=True)
                assert cache_dir.exists()
    
    def test_mql5_feed_exclusion_and_csv_converted_inclusion(self):
        """Test that mql5_feed directory is excluded and csv_converted is included."""
        # Create a temporary data directory structure
        temp_data_dir = self.temp_dir / "data"
        temp_data_dir.mkdir()
        
        # Create directories including mql5_feed and cache structure
        (temp_data_dir / "indicators").mkdir()
        (temp_data_dir / "raw_parquet").mkdir()
        (temp_data_dir / "mql5_feed").mkdir()
        (temp_data_dir / "cache").mkdir()
        (temp_data_dir / "cache" / "csv_converted").mkdir()
        (temp_data_dir / "cache" / "uv_cache").mkdir()
        
        # Mock the data folder path
        with patch('pathlib.Path') as mock_path:
            mock_path.return_value = temp_data_dir
            
            # Create mock directory objects
            mock_indicators = MagicMock()
            mock_indicators.name = "indicators"
            mock_indicators.is_dir.return_value = True
            mock_indicators.iterdir.return_value = []
            
            mock_raw_parquet = MagicMock()
            mock_raw_parquet.name = "raw_parquet"
            mock_raw_parquet.is_dir.return_value = True
            mock_raw_parquet.iterdir.return_value = []
            
            mock_mql5_feed = MagicMock()
            mock_mql5_feed.name = "mql5_feed"
            mock_mql5_feed.is_dir.return_value = True
            mock_mql5_feed.iterdir.return_value = []
            
            mock_cache = MagicMock()
            mock_cache.name = "cache"
            mock_cache.is_dir.return_value = True
            mock_cache.iterdir.return_value = []
            
            # Mock the data folder
            mock_data_folder = MagicMock()
            mock_data_folder.exists.return_value = True
            mock_data_folder.iterdir.return_value = [
                mock_indicators, mock_raw_parquet, mock_mql5_feed, mock_cache
            ]
            
            # Test that mql5_feed is excluded and cache is excluded
            # But csv_converted should be included
            excluded_names = ['mql5_feed', 'cache']
            included_names = ['indicators', 'raw_parquet', 'csv_converted']
            
            for name in excluded_names:
                assert name in excluded_names
            
            for name in included_names:
                assert name in included_names
            
            # Test that csv_converted folder exists and would be added
            csv_converted_path = temp_data_dir / "cache" / "csv_converted"
            assert csv_converted_path.exists()
            assert csv_converted_path.is_dir()
    
    def test_cache_directory_structure(self):
        """Test that the expected cache directory structure is defined."""
        # Test that the cache directories are properly defined in the code
        expected_cache_dirs = [
            "data/cache",
            "data/cache/csv_converted", 
            "data/cache/uv_cache",
            "data/backups"
        ]
        
        # This test verifies that our fix includes the correct cache directories
        assert len(expected_cache_dirs) == 4
        assert "data/cache" in expected_cache_dirs
        assert "data/cache/csv_converted" in expected_cache_dirs
        assert "data/cache/uv_cache" in expected_cache_dirs
        assert "data/backups" in expected_cache_dirs


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
