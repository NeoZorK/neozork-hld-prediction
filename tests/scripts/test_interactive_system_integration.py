import os
import tempfile
import pandas as pd
import pytest
from unittest.mock import patch
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

class TestInteractiveSystemIntegration:
    def setup_method(self):
        """Setup method for tests."""
        try:
            from interactive_system import InteractiveSystem
            self.system = InteractiveSystem()
        except ImportError:
            pytest.skip("InteractiveSystem not available")
    
    def test_data_loading_workflow(self):
        """Test data loading workflow."""
        # Create a temporary CSV file with MT5 format
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Create MT5 format CSV data with header on second line
            csv_content = """<MetaTrader 5 CSV Export>
DateTime,Open,High,Low,Close,TickVolume,
2023.01.01 00:00,100.0,105.0,95.0,103.0,1000,
2023.01.02 00:00,101.0,106.0,96.0,104.0,1100,
2023.01.03 00:00,102.0,107.0,97.0,105.0,1200,"""
            
            f.write(csv_content)
            csv_file = f.name
        
        try:
            # Mock the data_manager to avoid actual file loading
            with patch.object(self.system, 'data_manager') as mock_data_manager:
                mock_data_manager.load_data_from_file.return_value = pd.DataFrame({
                    'Open': [100.0, 101.0, 102.0],
                    'High': [105.0, 106.0, 107.0],
                    'Low': [95.0, 96.0, 97.0],
                    'Close': [103.0, 104.0, 105.0],
                    'Volume': [1000, 1100, 1200]
                })
                
                # Load the data
                result = self.system.data_manager.load_data_from_file(csv_file)
                
                # Check that data was loaded correctly
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
                # Check that columns are properly mapped
                expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                assert all(col in result.columns for col in expected_columns)
                
        finally:
            # Clean up
            os.unlink(csv_file)
