# -*- coding: utf-8 -*-
# tests/eda/test_data_overview.py

import unittest
import pandas as pd
import numpy as np
import os
from src.eda.data_overview import (
    show_basic_info,
    show_head,
    check_missing_values,
    check_duplicates,
    get_column_types,
    get_nan_columns,
    get_summary,
    load_data
)

class TestDataOverview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a sample dataframe
        cls.df = pd.DataFrame({
            'a': [1, 2, 3, np.nan, 5],
            'b': [5, 5, 5, 5, 5],
            'c': [1, 2, 2, 2, 3],
            'd': ['2022-01-01', '2022-01-02', None, '2022-01-04', '2022-01-05']
        })
        # Save as parquet and csv for testing load_data
        cls.parquet_path = "test_tmp.parquet"
        cls.csv_path = "test_tmp.csv"
        cls.df.to_parquet(cls.parquet_path)
        cls.df.to_csv(cls.csv_path, index=False)

    @classmethod
    def tearDownClass(cls):
        # Remove temporary files after tests
        if os.path.exists(cls.parquet_path):
            os.remove(cls.parquet_path)
        if os.path.exists(cls.csv_path):
            os.remove(cls.csv_path)

    def test_load_data_parquet(self):
        df_loaded = load_data(self.parquet_path, file_type="parquet")
        self.assertEqual(df_loaded.shape, self.df.shape)

    def test_load_data_csv(self):
        df_loaded = load_data(self.csv_path, file_type="csv")
        self.assertEqual(df_loaded.shape, self.df.shape)

    def test_show_basic_info(self):
        # Should not raise exception
        show_basic_info(self.df)

    def test_show_head(self):
        # Should not raise exception
        show_head(self.df, n=3)

    def test_check_missing_values(self):
        missing = check_missing_values(self.df)
        self.assertIn('a', missing.index)
        self.assertEqual(missing['a'], 1)

    def test_check_duplicates(self):
        # Add a duplicate row
        df_dup = pd.concat([self.df, self.df.iloc[[0]]], ignore_index=True)
        num_dup = check_duplicates(df_dup)
        self.assertEqual(num_dup, 1)

    def test_get_column_types(self):
        types = get_column_types(self.df)
        self.assertIn('a', types.index)

    def test_get_nan_columns(self):
        nan_cols = get_nan_columns(self.df)
        self.assertIn('a', nan_cols)

    def test_get_summary(self):
        # Should not raise exception
        get_summary(self.df)

if __name__ == '__main__':
    unittest.main()