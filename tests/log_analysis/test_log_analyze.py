# -*- coding: utf-8 -*-
# scripts/log_analysis/test_log_analyze.py

import unittest
import os
from scripts.log_analysis import log_analyze
from scripts.log_analysis import log_parse_utils

class TestLogAnalyze(unittest.TestCase):

    def setUp(self):
        # Prepare a sample log file content for testing
        self.sample_log = [
            "2025-05-02 13:11:05,861 | INFO | CHECKING: test_file.csv\n",
            "2025-05-02 13:11:05,861 | INFO | Shape: (324, 9)\n",
            "2025-05-02 13:11:05,866 | INFO | Number of duplicate rows: 2\n",
            "2025-05-02 13:11:05,867 | INFO | Columns with NaN values: ['col1', 'col2']\n",
            "2025-05-02 13:11:05,867 | INFO | Missing values:\n",
            "col1    1\n",
            "col2    2\n",
            "\n",
            "2025-05-02 13:11:05,867 | INFO | CHECKING: empty_file.csv\n",
            "2025-05-02 13:11:05,867 | INFO | Shape: (0, 0)\n",
        ]
        self.test_log_path = "test_eda_batch_check.log"
        with open(self.test_log_path, "w", encoding="utf-8") as f:
            f.writelines(self.sample_log)

    def tearDown(self):
        os.remove(self.test_log_path)

    def test_analyze_log(self):
        report = log_analyze.analyze_log(self.test_log_path)
        self.assertIn('test_file.csv', report['file_duplicates'])
        self.assertEqual(report['file_duplicates']['test_file.csv'], 2)
        self.assertIn('test_file.csv', report['file_nan_columns'])
        self.assertListEqual(report['file_nan_columns']['test_file.csv'], ['col1', 'col2'])
        self.assertIn('test_file.csv', report['file_missing'])
        self.assertIn('col1    1', report['file_missing']['test_file.csv'])
        self.assertIn('empty_file.csv', report['empty_files'])

    def test_parse_duplicate_count(self):
        self.assertEqual(log_parse_utils.parse_duplicate_count("INFO | Number of duplicate rows: 5"), 5)
        self.assertIsNone(log_parse_utils.parse_duplicate_count("INFO | Number of duplicate rows: None"))

    def test_parse_nan_columns(self):
        self.assertEqual(
            log_parse_utils.parse_nan_columns("INFO | Columns with NaN values: ['a', 'b']"),
            ['a', 'b']
        )
        self.assertEqual(
            log_parse_utils.parse_nan_columns("INFO | Columns with NaN values: []"),
            []
        )

    def test_parse_checking_file(self):
        self.assertEqual(
            log_parse_utils.parse_checking_file("INFO | CHECKING: path/to/file.csv"),
            "path/to/file.csv"
        )
        self.assertIsNone(
            log_parse_utils.parse_checking_file("Some other line")
        )

    def test_parse_error_line(self):
        self.assertEqual(
            log_parse_utils.parse_error_line("ERROR processing file.csv: File not found"),
            ("file.csv", "File not found")
        )
        self.assertIsNone(
            log_parse_utils.parse_error_line("INFO | All good")
        )

    def test_is_empty_shape(self):
        self.assertTrue(log_parse_utils.is_empty_shape("INFO | Shape: (0, 0)"))
        self.assertFalse(log_parse_utils.is_empty_shape("INFO | Shape: (1, 1)"))

    def test_is_missing_values_block_start(self):
        self.assertTrue(log_parse_utils.is_missing_values_block_start("INFO | Missing values:"))
        self.assertFalse(log_parse_utils.is_missing_values_block_start("INFO | Something else"))

    def test_parse_missing_lines(self):
        lines = [
            "INFO | Missing values:\n",
            "col1    1\n",
            "col2    2\n",
            "\n",
            "INFO | Number of duplicate rows: 0\n"
        ]
        missing, idx = log_parse_utils.parse_missing_lines(lines, 1)
        self.assertListEqual(missing, ['col1    1', 'col2    2'])

if __name__ == "__main__":
    unittest.main()