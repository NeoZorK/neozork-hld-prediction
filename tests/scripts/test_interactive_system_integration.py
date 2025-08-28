import os
import tempfile
import pandas as pd

class TestInteractiveSystemIntegration:
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
