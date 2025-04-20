# tests/data/fetchers/test_csv_fetcher.py

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
# Assumes tests are run from the project root directory
from src.data.fetchers.csv_fetcher import fetch_csv_data


# Definition of the TestCsvFetcher class
class TestCsvFetcher(unittest.TestCase):
    """
    Test suite for the fetch_csv_data function.
    """

    # setUp method to create temporary files before each test
    def setUp(self):
        """
        Set up temporary directory and file for testing.
        """
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
            # Add a row with infinity to test replacement
            "2023.01.01 10:03,103,inf,102,104,1300,jkl,101,inf\n"
        )
        with open(self.valid_csv_path, "w", encoding="utf-8") as f:
            f.write(self.valid_data_content)
        self.valid_file_size = os.path.getsize(self.valid_csv_path)

        # Create an empty file (with headers only, simulating MT5 export structure)
        self.empty_data_content = (
             "File Info Header Line\n"
             "DateTime,Open,High,Low,Close,TickVolume,ExtraCol,PredictLow,PredictHigh\n"
        )
        with open(self.empty_csv_path, "w", encoding="utf-8") as f:
            f.write(self.empty_data_content)
        self.empty_file_size = os.path.getsize(self.empty_csv_path)

        # Create a file missing a required column (e.g., 'Close')
        self.missing_col_content = (
            "File Info Header Line\n"
            "DateTime,Open,High,Low,TickVolume\n"
            "2023.01.01 10:00,100,105,99,1000\n"
        )
        with open(self.missing_col_path, "w", encoding="utf-8") as f:
             f.write(self.missing_col_content)
        self.missing_col_file_size = os.path.getsize(self.missing_col_path)

        # Create a file with bad formatting (e.g., wrong delimiter)
        self.bad_format_content = (
             "File Info Header Line\n"
             "DateTime;Open;High;Low;Close;TickVolume\n"
             "2023.01.01 10:00;100;105;99;101;1000\n"
        )
        with open(self.bad_format_path, "w", encoding="utf-8") as f:
             f.write(self.bad_format_content)
        self.bad_format_file_size = os.path.getsize(self.bad_format_path)

        # Create a file with invalid date format
        self.invalid_date_content = (
            "File Info Header Line\n"
            "DateTime,Open,High,Low,Close,TickVolume\n"
            "01-01-2023 10:00,100,105,99,101,1000\n" # Wrong format
            "2023.01.01 10:01,101,106,100,102,1100\n"
        )
        with open(self.invalid_date_path, "w", encoding="utf-8") as f:
            f.write(self.invalid_date_content)
        self.invalid_date_file_size = os.path.getsize(self.invalid_date_path)


    # tearDown method to clean up temporary files after each test
    def tearDown(self):
        """
        Clean up the temporary directory.
        """
        self.test_dir.cleanup()

    # Test case for successful data fetching
    def test_fetch_csv_data_success(self):
        """
        Test successfully fetching and processing data from a valid CSV file.
        Checks returned DataFrame structure, index, columns, and metrics.
        """
        # Call the function under test
        result = fetch_csv_data(self.valid_csv_path)

        # Assert the result is a tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack the tuple
        df, metrics = result

        # Assert DataFrame is not None and has expected shape
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 4) # Number of data rows
        # Check columns (TickVolume renamed to Volume, ExtraCol kept)
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'ExtraCol', 'PredictLow', 'PredictHigh']
        self.assertListEqual(sorted(df.columns.tolist()), sorted(expected_cols))

        # Assert index is DatetimeIndex
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertEqual(df.index.name, 'DateTime')

        # Assert basic data types (OHLCV should be numeric)
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            self.assertTrue(pd.api.types.is_numeric_dtype(df[col]))

        # Assert inf was replaced with NaN (High column, last row)
        # Note: iloc uses integer position
        self.assertTrue(pd.isna(df['High'].iloc[3]))
        self.assertTrue(pd.isna(df['PredictHigh'].iloc[3]))

        # Assert metrics dictionary
        self.assertIsInstance(metrics, dict)
        self.assertIn('file_size_bytes', metrics)
        self.assertEqual(metrics['file_size_bytes'], self.valid_file_size)

    # Test case for file not found
    def test_fetch_csv_data_file_not_found(self):
        """
        Test behavior when the specified CSV file does not exist.
        Expects (None, {'file_size_bytes': None}).
        """
        non_existent_path = os.path.join(self.test_dir.name, "non_existent.csv")
        result = fetch_csv_data(non_existent_path)

        # Assert the result is a tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack the tuple
        df, metrics = result

        # Assert DataFrame is None
        self.assertIsNone(df)
        # Assert metrics contain None for file size
        self.assertIsInstance(metrics, dict)
        self.assertIn('file_size_bytes', metrics)
        self.assertIsNone(metrics['file_size_bytes'])

    # Test case for empty file (only headers)
    def test_fetch_csv_data_empty_file(self):
        """
        Test behavior when the CSV file contains only header lines.
        Expects (None, {'file_size_bytes': size}).
        """
        result = fetch_csv_data(self.empty_csv_path)

        # Assert the result is a tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack the tuple
        df, metrics = result

        # Assert DataFrame is None (as no data rows)
        self.assertIsNone(df) # Changed: should return None if empty after processing
        # Assert metrics contain the file size
        self.assertIsInstance(metrics, dict)
        self.assertIn('file_size_bytes', metrics)
        self.assertEqual(metrics['file_size_bytes'], self.empty_file_size)

    # Test case for missing required column
    def test_fetch_csv_data_missing_column(self):
        """
        Test behavior when a required OHLCV column is missing.
        Expects (None, {'file_size_bytes': size}).
        """
        result = fetch_csv_data(self.missing_col_path)

        # Assert the result is a tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack the tuple
        df, metrics = result

        # Assert DataFrame is None
        self.assertIsNone(df)
        # Assert metrics contain the file size
        self.assertIsInstance(metrics, dict)
        self.assertIn('file_size_bytes', metrics)
        self.assertEqual(metrics['file_size_bytes'], self.missing_col_file_size)

    # Test case for badly formatted CSV (should raise ParserError handled internally)
    def test_fetch_csv_data_bad_format(self):
        """
        Test behavior with a file that pandas cannot parse correctly (e.g., wrong delimiter).
        Expects (None, {'file_size_bytes': size}).
        """
        result = fetch_csv_data(self.bad_format_path)

        # Assert the result is a tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack the tuple
        df, metrics = result

        # Assert DataFrame is None
        self.assertIsNone(df)
        # Assert metrics contain the file size
        self.assertIsInstance(metrics, dict)
        self.assertIn('file_size_bytes', metrics)
        self.assertEqual(metrics['file_size_bytes'], self.bad_format_file_size)

    # Test case for invalid date format
    def test_fetch_csv_data_invalid_date_format(self):
        """
        Test behavior when dates cannot be parsed, leading to dropped rows.
        It should return the valid rows or None if all rows are dropped.
        Expects (df with valid rows, {'file_size_bytes': size}) or (None, {...})
        """
        result = fetch_csv_data(self.invalid_date_path)

        # Assert the result is a tuple
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        # Unpack the tuple
        df, metrics = result

        # In this specific case, one row has a valid date, one doesn't.
        # The function drops rows with invalid dates.
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 1) # Only the valid row remains
        self.assertEqual(df.index[0], pd.Timestamp('2023-01-01 10:01:00'))

        # Assert metrics contain the file size
        self.assertIsInstance(metrics, dict)
        self.assertIn('file_size_bytes', metrics)
        self.assertEqual(metrics['file_size_bytes'], self.invalid_date_file_size)


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()