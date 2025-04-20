# tests/data/fetchers/test_csv_fetcher.py (Исправления v2)

"""
Unit tests for the CSV data fetcher.
All comments are in English.
"""

import unittest
import tempfile
import os
import pandas as pd
from pathlib import Path

# Adjust the import path based on the project structure
from src.data.fetchers.csv_fetcher import fetch_csv_data


# Definition of the TestCsvFetcher class
class TestCsvFetcher(unittest.TestCase):
    """ Test suite for the fetch_csv_data function. """

    # setUp method (no changes needed)
    def setUp(self):
        """ Set up temporary directory and file for testing. """
        self.test_dir = tempfile.TemporaryDirectory()
        self.valid_csv_path = os.path.join(self.test_dir.name, "valid_data.csv")
        self.empty_csv_path = os.path.join(self.test_dir.name, "empty_data.csv")
        self.missing_col_path = os.path.join(self.test_dir.name, "missing_col.csv")
        self.bad_format_path = os.path.join(self.test_dir.name, "bad_format.csv")
        self.invalid_date_path = os.path.join(self.test_dir.name, "invalid_date.csv")
        # Create a valid CSV file
        self.valid_data_content = (
            "File Info Header Line\n"
            "DateTime,Open,High,Low,Close,TickVolume,ExtraCol,PredictLow,PredictHigh\n"
            "2023.01.01 10:00,100,105,99,101,1000,abc,98,106\n"
            "2023.01.01 10:01,101,106,100,102,1100,def,99,107\n"
            "2023.01.01 10:02,102,107,101,103,1200,ghi,100,108\n"
            "2023.01.01 10:03,103,inf,102,104,1300,jkl,101,inf\n" # Row with inf
        )
        with open(self.valid_csv_path, "w", encoding="utf-8") as f: f.write(self.valid_data_content)
        self.valid_file_size = os.path.getsize(self.valid_csv_path)
        # Create other files... (rest of setUp is unchanged)
        self.empty_data_content = (
             "File Info Header Line\n"
             "DateTime,Open,High,Low,Close,TickVolume,ExtraCol,PredictLow,PredictHigh\n"
        )
        with open(self.empty_csv_path, "w", encoding="utf-8") as f: f.write(self.empty_data_content)
        self.empty_file_size = os.path.getsize(self.empty_csv_path)
        self.missing_col_content = (
            "File Info Header Line\n"
            "DateTime,Open,High,Low,TickVolume\n"
            "2023.01.01 10:00,100,105,99,1000\n"
        )
        with open(self.missing_col_path, "w", encoding="utf-8") as f: f.write(self.missing_col_content)
        self.missing_col_file_size = os.path.getsize(self.missing_col_path)
        self.bad_format_content = (
             "File Info Header Line\n"
             "DateTime;Open;High;Low;Close;TickVolume\n"
             "2023.01.01 10:00;100;105;99;101;1000\n"
        )
        with open(self.bad_format_path, "w", encoding="utf-8") as f: f.write(self.bad_format_content)
        self.bad_format_file_size = os.path.getsize(self.bad_format_path)
        self.invalid_date_content = (
            "File Info Header Line\n"
            "DateTime,Open,High,Low,Close,TickVolume\n"
            "01-01-2023 10:00,100,105,99,101,1000\n"
            "2023.01.01 10:01,101,106,100,102,1100\n"
        )
        with open(self.invalid_date_path, "w", encoding="utf-8") as f: f.write(self.invalid_date_content)
        self.invalid_date_file_size = os.path.getsize(self.invalid_date_path)

    # tearDown method (no changes needed)
    def tearDown(self):
        """ Clean up the temporary directory. """
        self.test_dir.cleanup()

    # Test case for successful data fetching
    def test_fetch_csv_data_success(self):
        """ Test successfully fetching and processing data from a valid CSV file. """
        result = fetch_csv_data(self.valid_csv_path)
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNotNone(df); self.assertIsInstance(df, pd.DataFrame)

        # FIX: Expect 3 rows after dropping the row with NaN from 'inf'
        self.assertEqual(df.shape[0], 3)

        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'ExtraCol', 'PredictLow', 'PredictHigh']
        self.assertListEqual(sorted(df.columns.tolist()), sorted(expected_cols))
        self.assertIsInstance(df.index, pd.DatetimeIndex); self.assertEqual(df.index.name, 'DateTime')
        for col in ['Open', 'Low', 'Close', 'Volume']: # Check cols that didn't have inf
            self.assertTrue(pd.api.types.is_numeric_dtype(df[col]))
        # 'High' and 'PredictHigh' are tricky because the inf row was dropped.
        # Check the remaining values are numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(df['High']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['PredictHigh']))
        # Check metrics
        self.assertIsInstance(metrics, dict); self.assertIn('file_size_bytes', metrics)
        self.assertEqual(metrics['file_size_bytes'], self.valid_file_size)

    # Test case for file not found (No changes needed)
    def test_fetch_csv_data_file_not_found(self):
        """ Test behavior when the specified CSV file does not exist. """
        non_existent_path = os.path.join(self.test_dir.name, "non_existent.csv")
        result = fetch_csv_data(non_existent_path)
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        self.assertIsInstance(metrics, dict); self.assertIn('file_size_bytes', metrics)
        self.assertIsNone(metrics['file_size_bytes'])

    # Test case for empty file (No changes needed)
    def test_fetch_csv_data_empty_file(self):
        """ Test behavior when the CSV file contains only header lines. """
        result = fetch_csv_data(self.empty_csv_path)
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df) # Changed: fetcher returns None if df is empty after read
        self.assertIsInstance(metrics, dict); self.assertIn('file_size_bytes', metrics)
        self.assertEqual(metrics['file_size_bytes'], self.empty_file_size)

    # Test case for missing required column (No changes needed)
    def test_fetch_csv_data_missing_column(self):
        """ Test behavior when a required OHLCV column is missing. """
        result = fetch_csv_data(self.missing_col_path)
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        self.assertIsInstance(metrics, dict); self.assertIn('file_size_bytes', metrics)
        self.assertEqual(metrics['file_size_bytes'], self.missing_col_file_size)

    # Test case for badly formatted CSV (No changes needed)
    def test_fetch_csv_data_bad_format(self):
        """ Test behavior with a file that pandas cannot parse correctly. """
        result = fetch_csv_data(self.bad_format_path)
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNone(df)
        self.assertIsInstance(metrics, dict); self.assertIn('file_size_bytes', metrics)
        self.assertEqual(metrics['file_size_bytes'], self.bad_format_file_size)

    # Test case for invalid date format (No changes needed)
    def test_fetch_csv_data_invalid_date_format(self):
        """ Test behavior when dates cannot be parsed, leading to dropped rows. """
        result = fetch_csv_data(self.invalid_date_path)
        self.assertIsNotNone(result); self.assertIsInstance(result, tuple); self.assertEqual(len(result), 2)
        df, metrics = result
        self.assertIsNotNone(df); self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 1) # Only the valid row remains
        self.assertEqual(df.index[0], pd.Timestamp('2023-01-01 10:01:00'))
        self.assertIsInstance(metrics, dict); self.assertIn('file_size_bytes', metrics)
        self.assertEqual(metrics['file_size_bytes'], self.invalid_date_file_size)


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()