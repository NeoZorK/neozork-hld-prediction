# tests/data/fetchers/test_csv_fetcher.py
# -*- coding: utf-8 -*-

"""
Unit tests for the CSV data fetcher.
All comments are in English.
"""

import unittest
import tempfile
import os
import pandas as pd
import numpy as np # Import numpy
from pathlib import Path

# Adjust the import path based on the project structure
from src.data.fetchers.csv_fetcher import fetch_csv_data


# Definition of the TestCsvFetcher class
class TestCsvFetcher(unittest.TestCase):
    """ Test suite for the fetch_csv_data function. """

    def setUp(self):
        """ Set up temporary directory and file for testing. """
        self.test_dir = tempfile.TemporaryDirectory()
        self.valid_csv_path = os.path.join(self.test_dir.name, "valid_data.csv")
        self.empty_csv_path = os.path.join(self.test_dir.name, "empty_data.csv")
        self.missing_col_path = os.path.join(self.test_dir.name, "missing_col.csv")
        self.bad_format_path = os.path.join(self.test_dir.name, "bad_format.csv")
        self.invalid_date_path = os.path.join(self.test_dir.name, "invalid_date.csv")

        # Create a valid CSV file (MT5 style with info line and header with trailing commas/tabs)
        # Using simple comma separation here for simplicity in test file creation
        # The fetcher should handle cleaning. Use TickVolume, DateTime.
        self.valid_data_content = (
            "File Info Header Line\n"
            "DateTime,Open,High,Low,Close,TickVolume,ExtraCol,PredictLow,PredictHigh\n"
            "2023.01.01 10:00,100,105,99,101,1000,abc,98,106\n"
            "2023.01.01 10:01,101,106,100,102,1100,def,99,107\n"
            "2023.01.01 10:02,102,107,101,103,1200,ghi,100,108\n"
            "2023.01.01 10:03,103,inf,102,104,1300,jkl,101,inf\n" # Row with inf
        )
        with open(self.valid_csv_path, "w", encoding="utf-8") as f: f.write(self.valid_data_content)

        # Create other files
        self.empty_data_content = (
             "File Info Header Line\n"
             "DateTime,Open,High,Low,Close,TickVolume,ExtraCol,PredictLow,PredictHigh\n"
        )
        with open(self.empty_csv_path, "w", encoding="utf-8") as f: f.write(self.empty_data_content)

        self.missing_col_content = (
            "File Info Header Line\n"
            "DateTime,Open,High,Low,TickVolume\n" # Missing Close
            "2023.01.01 10:00,100,105,99,1000\n"
        )
        with open(self.missing_col_path, "w", encoding="utf-8") as f: f.write(self.missing_col_content)

        self.bad_format_content = (
             "File Info Header Line\n"
             "DateTime;Open;High;Low;Close;TickVolume\n" # Wrong separator
             "2023.01.01 10:00;100;105;99;101;1000\n"
        )
        with open(self.bad_format_path, "w", encoding="utf-8") as f: f.write(self.bad_format_content)

        self.invalid_date_content = (
            "File Info Header Line\n"
            "DateTime,Open,High,Low,Close,TickVolume\n"
            "01-01-2023 10:00,100,105,99,101,1000\n" # Invalid date format for default parser
            "2023.01.01 10:01,101,106,100,102,1100\n" # Valid date
        )
        with open(self.invalid_date_path, "w", encoding="utf-8") as f: f.write(self.invalid_date_content)

        # Define the expected column mapping for these test files
        self.test_ohlc_map = {
             'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close',
             'Volume': 'TickVolume' # Map internal 'Volume' to CSV's 'TickVolume'
        }
        self.test_dt_col = 'DateTime'

    def tearDown(self):
        """ Clean up the temporary directory. """
        self.test_dir.cleanup()

    def test_fetch_csv_data_success(self):
        """ Test successfully fetching and processing data from a valid CSV file. """
        # Pass the specific mapping and datetime column used in the test file
        result = fetch_csv_data(
            self.valid_csv_path,
            ohlc_columns=self.test_ohlc_map,
            datetime_column=self.test_dt_col,
            skiprows=1 # Standard skip for MT5 format
        )
        # --- FIXED ASSERTIONS ---
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        # Expect all 4 rows, as inf doesn't cause drop based on OHLC NaN check
        self.assertEqual(result.shape[0], 4)
        # Check expected columns after standard renaming + others found
        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'ExtraCol', 'PredictLow', 'PredictHigh']
        self.assertListEqual(sorted(result.columns.tolist()), sorted(expected_cols))
        self.assertIsInstance(result.index, pd.DatetimeIndex)
        self.assertEqual(result.index.name, 'Timestamp') # Check standard index name
        # Check types (should be float after latest changes)
        for col in ['Open', 'High', 'Low', 'Close', 'Volume', 'PredictLow', 'PredictHigh']:
            self.assertTrue(pd.api.types.is_numeric_dtype(result[col]))
        # Check inf was handled correctly (became np.inf, which is numeric)
        self.assertTrue(np.isinf(result.loc[pd.Timestamp('2023-01-01 10:03:00'), 'High']))
        self.assertTrue(np.isinf(result.loc[pd.Timestamp('2023-01-01 10:03:00'), 'PredictHigh']))
        # --- END FIXED ASSERTIONS ---

    def test_fetch_csv_data_file_not_found(self):
        """ Test behavior when the specified CSV file does not exist. """
        non_existent_path = os.path.join(self.test_dir.name, "non_existent.csv")
        result = fetch_csv_data(non_existent_path)
        # --- FIXED ASSERTIONS ---
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty) # Expect empty dataframe on error
        # --- END FIXED ASSERTIONS ---

    def test_fetch_csv_data_empty_file(self):
        """ Test behavior when the CSV file contains only header lines. """
        result = fetch_csv_data(
            self.empty_csv_path,
            ohlc_columns=self.test_ohlc_map,
            datetime_column=self.test_dt_col,
            skiprows=1
            )
        # --- FIXED ASSERTIONS ---
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty) # Expect empty dataframe if no data rows
         # --- END FIXED ASSERTIONS ---

    def test_fetch_csv_data_missing_column(self):
        """ Test behavior when a required OHLC column is missing. """
        # Expect ValueError internally, resulting in empty DataFrame
        result = fetch_csv_data(
            self.missing_col_path,
             ohlc_columns=self.test_ohlc_map, # Mapping still includes 'Close'
             datetime_column=self.test_dt_col,
             skiprows=1
        )
         # --- FIXED ASSERTIONS ---
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty) # Expect empty dataframe on error
         # --- END FIXED ASSERTIONS ---

    def test_fetch_csv_data_bad_format(self):
        """ Test behavior with a file that pandas cannot parse correctly (wrong separator). """
        # Expect pandas error internally, resulting in empty DataFrame
        result = fetch_csv_data(
            self.bad_format_path,
            ohlc_columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close', 'Volume':'TickVolume'}, # Use ; names? No, map std to expected bad ones
            datetime_column='DateTime', # Expect this name
            skiprows=1,
            separator=',' # Force comma separator to cause failure
            )
         # --- FIXED ASSERTIONS ---
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty) # Expect empty dataframe on error
         # --- END FIXED ASSERTIONS ---

    def test_fetch_csv_data_invalid_date_format(self):
        """ Test behavior when dates cannot be parsed, leading to dropped rows. """
        result = fetch_csv_data(
             self.invalid_date_path,
             ohlc_columns=self.test_ohlc_map,
             datetime_column=self.test_dt_col,
             skiprows=1
             )
        # --- FIXED ASSERTIONS ---
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        # Only the second row with the valid date format should remain
        self.assertEqual(result.shape[0], 1)
        self.assertEqual(result.index[0], pd.Timestamp('2023-01-01 10:01:00'))
        # --- END FIXED ASSERTIONS ---

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()