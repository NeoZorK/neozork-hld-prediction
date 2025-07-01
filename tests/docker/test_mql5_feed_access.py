"""
Test module for checking mql5_feed folder access in Docker container.
"""
import os
import pytest
from pathlib import Path


class TestMQL5FeedAccess:
    """Test class for mql5_feed folder access and functionality."""
    
    def test_mql5_feed_folder_exists(self):
        """Test that mql5_feed folder exists in the container."""
        mql5_feed_path = Path("/app/mql5_feed")
        assert mql5_feed_path.exists(), f"mql5_feed folder not found at {mql5_feed_path}"
        assert mql5_feed_path.is_dir(), f"mql5_feed path is not a directory: {mql5_feed_path}"
    
    def test_mql5_feed_indicators_folder_exists(self):
        """Test that indicators subfolder exists in mql5_feed."""
        indicators_path = Path("/app/mql5_feed/indicators")
        assert indicators_path.exists(), f"indicators folder not found at {indicators_path}"
        assert indicators_path.is_dir(), f"indicators path is not a directory: {indicators_path}"
    
    def test_vwap_indicator_file_exists(self):
        """Test that VWAP indicator file exists."""
        vwap_file = Path("/app/mql5_feed/indicators/SCHR_VWAP.mq5")
        assert vwap_file.exists(), f"SCHR_VWAP.mq5 not found at {vwap_file}"
        assert vwap_file.is_file(), f"SCHR_VWAP.mq5 is not a file: {vwap_file}"
    
    def test_vwap_indicator_file_content(self):
        """Test that VWAP indicator file has correct content."""
        vwap_file = Path("/app/mql5_feed/indicators/SCHR_VWAP.mq5")
        assert vwap_file.exists(), f"SCHR_VWAP.mq5 not found at {vwap_file}"
        
        # Try different encodings for MQL5 files
        try:
            content = vwap_file.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                content = vwap_file.read_text(encoding='utf-16')
            except UnicodeDecodeError:
                content = vwap_file.read_text(encoding='cp1251')
        
        # Check for essential MQL5 elements
        assert "#property indicator_chart_window" in content, "Missing chart window property"
        assert "OnCalculate" in content, "Missing OnCalculate function"
        assert "VWAP" in content, "Missing VWAP reference"
        assert "ENUM_APPLIED_PRICE" in content, "Missing price type enum"
    
    def test_mql5_feed_folder_permissions(self):
        """Test that mql5_feed folder has correct permissions."""
        mql5_feed_path = Path("/app/mql5_feed")
        assert mql5_feed_path.exists(), f"mql5_feed folder not found at {mql5_feed_path}"
        
        # Check if folder is readable
        assert os.access(mql5_feed_path, os.R_OK), f"mql5_feed folder is not readable: {mql5_feed_path}"
        
        # Check if folder is executable (for directory access)
        assert os.access(mql5_feed_path, os.X_OK), f"mql5_feed folder is not executable: {mql5_feed_path}"
    
    def test_indicators_folder_permissions(self):
        """Test that indicators folder has correct permissions."""
        indicators_path = Path("/app/mql5_feed/indicators")
        assert indicators_path.exists(), f"indicators folder not found at {indicators_path}"
        
        # Check if folder is readable
        assert os.access(indicators_path, os.R_OK), f"indicators folder is not readable: {indicators_path}"
        
        # Check if folder is executable (for directory access)
        assert os.access(indicators_path, os.X_OK), f"indicators folder is not executable: {indicators_path}"
    
    def test_vwap_file_permissions(self):
        """Test that VWAP indicator file has correct permissions."""
        vwap_file = Path("/app/mql5_feed/indicators/SCHR_VWAP.mq5")
        assert vwap_file.exists(), f"SCHR_VWAP.mq5 not found at {vwap_file}"
        
        # Check if file is readable
        assert os.access(vwap_file, os.R_OK), f"SCHR_VWAP.mq5 is not readable: {vwap_file}"
    
    def test_mql5_feed_folder_structure(self):
        """Test the complete folder structure of mql5_feed."""
        mql5_feed_path = Path("/app/mql5_feed")
        assert mql5_feed_path.exists(), f"mql5_feed folder not found at {mql5_feed_path}"
        
        # List all items in mql5_feed
        items = list(mql5_feed_path.iterdir())
        item_names = [item.name for item in items]
        
        # Check that indicators folder exists
        assert "indicators" in item_names, f"indicators folder not found in mql5_feed: {item_names}"
        
        # Check indicators folder content
        indicators_path = mql5_feed_path / "indicators"
        indicator_files = list(indicators_path.iterdir())
        indicator_file_names = [f.name for f in indicator_files if f.is_file()]
        
        # Check that VWAP indicator exists
        assert "SCHR_VWAP.mq5" in indicator_file_names, f"SCHR_VWAP.mq5 not found in indicators: {indicator_file_names}"
    
    def test_mql5_feed_mount_point(self):
        """Test that mql5_feed is properly mounted from host."""
        # This test checks if the folder is accessible and contains expected content
        mql5_feed_path = Path("/app/mql5_feed")
        assert mql5_feed_path.exists(), f"mql5_feed folder not found at {mql5_feed_path}"
        
        # Check if we can list contents
        try:
            items = list(mql5_feed_path.iterdir())
            assert len(items) > 0, "mql5_feed folder is empty"
        except PermissionError:
            pytest.fail("Permission denied when accessing mql5_feed folder")
        except OSError as e:
            pytest.fail(f"OS error when accessing mql5_feed folder: {e}")


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"]) 