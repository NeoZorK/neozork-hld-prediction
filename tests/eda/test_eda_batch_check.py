import unittest
import sys
import os
from unittest.mock import patch

# Добавляем корень проекта в sys.path для корректного импорта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.eda import eda_batch_check

class TestEdaBatchCheck(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test data
        self.test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/test_unittest'))
        os.makedirs(self.test_data_dir, exist_ok=True)

    def tearDown(self):
        # Delete the test data directory after tests
        import shutil
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)

    @patch('src.eda.eda_batch_check.file_info')
    @patch('src.eda.eda_batch_check.folder_stats')
    def test_main_basic(self, mock_folder_stats, mock_file_info):
        # Mocking the file_info and folder_stats functions
        mock_file_info.get_file_info.return_value = {
            'file_path': '/fake/path/file1.parquet',
            'file_name': 'file1.parquet',
            'file_size_mb': 1.23,
            'n_rows': 10,
            'n_cols': 2,
            'columns': ['a', 'b'],
            'dtypes': {'a': 'int64', 'b': 'float64'},
            'datetime_or_timestamp_fields': [],
            'datetime_columns': [],
            'timestamp_columns': []
        }
        mock_folder_stats.get_folder_stats.return_value = {
            'folder': '/fake/path',
            'total_size_mb': 1.23,
            'file_count': 1
        }
        # Mocking os.walk and glob.glob to simulate file system
        with patch('os.walk') as mock_walk, patch('glob.glob') as mock_glob:
            mock_walk.return_value = [('/fake/path', [], ['file1.parquet'])]
            mock_glob.return_value = ['/fake/path/file1.parquet']
            # Mocking pandas read_parquet to simulate reading a parquet file
            with patch('pandas.read_parquet') as mock_read_parquet:
                import pandas as pd
                mock_df = pd.DataFrame({'a': [1,2,3,4,5], 'b': [1.1,2.2,3.3,4.4,5.5]})
                mock_read_parquet.return_value = mock_df
                # Mocking tqdm to avoid actual progress bar
                with patch('builtins.print') as mock_print, \
                     patch.object(sys, 'argv', ['eda_batch_check.py', '--basic-stats']):
                    eda_batch_check.main()
                    self.assertTrue(mock_print.called)

    def test_script_runs(self):
        # Проверяем, что скрипт импортируется и main вызывается без ошибок
        with patch('builtins.print') as mock_print, \
             patch.object(sys, 'argv', ['eda_batch_check.py', '--basic-stats']):
            try:
                eda_batch_check.main()
            except SystemExit:
                # argparse can raise SystemExit if no arguments are provided
                pass
            self.assertTrue(mock_print.called)

# RUN TESTS
if __name__ == '__main__':
    unittest.main()

