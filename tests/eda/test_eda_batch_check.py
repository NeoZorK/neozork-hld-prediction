# -*- coding: utf-8 -*-
# tests/eda/test_eda_batch_check.py
import unittest
import os
import tempfile
import shutil
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from eda_batch_check import (
    setup_logger,
    find_data_files,
    log_file_info,
    suppress_warnings,
    check_file,
    process_folder
)

class TestEDABatchCheck(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, "test.log")
        self.csv_file = os.path.join(self.test_dir, "test.csv")
        self.parquet_file = os.path.join(self.test_dir, "test.parquet")
        df = pd.DataFrame({
            'timestamp': pd.date_range(start='2024-01-01', periods=5),
            'open': [1.0, 2.0, 3.0, 4.0, 5.0],
            'high': [1.1, 2.1, 3.1, 4.1, 5.1],
            'low': [0.9, 1.9, 2.9, 3.9, 4.9],
            'close': [1.05, 2.05, 3.05, 4.05, 5.05],
            'volume': [100, 200, 300, 400, 500]
        })
        df.to_csv(self.csv_file, index=False, sep='\t')
        df.to_parquet(self.parquet_file, index=False)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_main_verification_prompt_yes(self):
        with patch('argparse.ArgumentParser.parse_args') as mock_args, \
             patch('builtins.input', return_value='y'), \
             patch('src.eda.eda_data_cleaner.run_data_cleaner', return_value=True), \
             patch('eda_batch_check.analyze_log', return_value={'total_files': 2}), \
             patch('eda_batch_check.print_summary_diff'), \
             patch('eda_batch_check.setup_logger'), \
             patch('eda_batch_check.find_data_files', return_value=[self.csv_file, self.parquet_file]), \
             patch('eda_batch_check.process_folder'), \
             patch('eda_batch_check.tqdm'):
            mock_args.return_value = type('Args', (), {
                'clean': True,
                'output_dir': os.path.join(self.test_dir, 'cleaned'),
                'csv_delimiter': '\t',
                'csv_header': '0',
                'handle_nan': 'ffill',
                'skip_verification': False,
                'log_file': self.log_file,
                'target_folders': [self.test_dir]
            })
            from eda_batch_check import main
            main()
            from eda_batch_check import analyze_log
            assert analyze_log.call_count == 2


    def test_main_data_cleaning_failure(self):
        """Test: main() exits with code 2 if data cleaning fails"""
        with patch('argparse.ArgumentParser.parse_args') as mock_args, \
             patch('sys.exit') as mock_exit, \
             patch('src.eda.eda_data_cleaner.run_data_cleaner', return_value=False), \
             patch('eda_batch_check.setup_logger'), \
             patch('eda_batch_check.find_data_files', return_value=[self.csv_file, self.parquet_file]), \
             patch('eda_batch_check.process_folder'), \
             patch('eda_batch_check.tqdm'), \
             patch('eda_batch_check.analyze_log', return_value={'total_files': 2}):
            mock_args.return_value = type('Args', (), {
                'clean': True,
                'output_dir': os.path.join(self.test_dir, 'cleaned'),
                'csv_delimiter': '\t',
                'csv_header': '0',
                'handle_nan': 'ffill',
                'skip_verification': True,
                'log_file': self.log_file,
                'target_folders': [self.test_dir]
            })
            from eda_batch_check import main  # Import here, after patching
            main()
            mock_exit.assert_called_with(2)

    def test_main_no_files_found(self):
        empty_dir = tempfile.mkdtemp()
        try:
            with patch('argparse.ArgumentParser.parse_args') as mock_args, \
                 patch('sys.exit') as mock_exit:
                mock_args.return_value = type('Args', (), {
                    'clean': False,
                    'output_dir': os.path.join(empty_dir, 'cleaned'),
                    'csv_delimiter': '\t',
                    'csv_header': '0',
                    'handle_nan': 'ffill',
                    'skip_verification': True,
                    'log_file': os.path.join(empty_dir, 'test.log'),
                    'target_folders': [empty_dir]
                })
                from eda_batch_check import main
                main()
                mock_exit.assert_called_with(1)
        finally:
            shutil.rmtree(empty_dir)

    def test_setup_logger(self):
        logger = setup_logger(self.log_file)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        logger = setup_logger(self.log_file)
        self.assertIsNotNone(logger)
        self.assertEqual(len(logger.handlers), 1)
        self.assertTrue(os.path.exists(self.log_file))

    def test_find_data_files(self):
        files = find_data_files(self.test_dir)
        self.assertEqual(len(files), 2)
        self.assertTrue(any(f.endswith('.csv') for f in files))
        self.assertTrue(any(f.endswith('.parquet') for f in files))

    def test_log_file_info(self):
        logger = setup_logger(self.log_file)
        df = pd.read_csv(self.csv_file, sep='\t')
        log_file_info(df, self.csv_file, logger)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            self.assertIn("CHECKING", log_content)
            self.assertIn("Shape", log_content)
            self.assertIn("Columns", log_content)

    def test_suppress_warnings(self):
        with self.assertNoLogs(level='WARNING'):
            suppress_warnings()
            import warnings
            warnings.warn("Test warning")

    @patch('pandas.read_csv')
    @patch('pandas.read_parquet')
    def test_check_file(self, mock_read_parquet, mock_read_csv):
        logger = setup_logger(self.log_file)
        mock_read_csv.return_value = pd.DataFrame({'test': [1, 2, 3]})
        check_file(self.csv_file, logger)
        mock_read_csv.assert_called_once()
        mock_read_parquet.return_value = pd.DataFrame({'test': [1, 2, 3]})
        check_file(self.parquet_file, logger)
        mock_read_parquet.assert_called_once()

    @patch('tqdm.tqdm')
    def test_process_folder(self, mock_tqdm):
        logger = setup_logger(self.log_file)
        mock_progress_bar = MagicMock()
        mock_tqdm.return_value = mock_progress_bar
        process_folder(self.test_dir, logger, mock_progress_bar)
        mock_progress_bar.update.assert_called()

    def test_main_with_clean(self):
        with patch('argparse.ArgumentParser.parse_args') as mock_args:
            mock_args.return_value = type('Args', (), {
                'clean': True,
                'output_dir': os.path.join(self.test_dir, 'cleaned'),
                'csv_delimiter': '\t',
                'csv_header': '0',
                'handle_nan': 'ffill',
                'skip_verification': True,
                'log_file': self.log_file,
                'target_folders': [self.test_dir]
            })
            with patch('subprocess.run') as mock_run:
                from eda_batch_check import main
                main()
                mock_run.assert_called()

    def test_main_without_clean(self):
        with patch('argparse.ArgumentParser.parse_args') as mock_args:
            mock_args.return_value = type('Args', (), {
                'clean': False,
                'output_dir': os.path.join(self.test_dir, 'cleaned'),
                'csv_delimiter': '\t',
                'csv_header': '0',
                'handle_nan': 'ffill',
                'skip_verification': True,
                'log_file': self.log_file,
                'target_folders': [self.test_dir]
            })
            with patch('subprocess.run') as mock_run:
                from eda_batch_check import main
                main()
                mock_run.assert_not_called()

    def test_main_clean_skip_verification(self):
        with patch('argparse.ArgumentParser.parse_args') as mock_args, \
             patch('src.eda.eda_data_cleaner.run_data_cleaner', return_value=True), \
             patch('eda_batch_check.analyze_log', return_value={'total_files': 2}) as mock_analyze_log, \
             patch('eda_batch_check.print_summary_diff') as mock_print_diff, \
             patch('eda_batch_check.setup_logger'), \
             patch('eda_batch_check.find_data_files', return_value=[self.csv_file, self.parquet_file]), \
             patch('eda_batch_check.process_folder'), \
             patch('eda_batch_check.tqdm'):
            mock_args.return_value = type('Args', (), {
                'clean': True,
                'output_dir': os.path.join(self.test_dir, 'cleaned'),
                'csv_delimiter': '\t',
                'csv_header': '0',
                'handle_nan': 'ffill',
                'skip_verification': True,
                'log_file': self.log_file,
                'target_folders': [self.test_dir]
            })
            from eda_batch_check import main
            main()
            assert mock_analyze_log.call_count == 1
            mock_print_diff.assert_not_called()

    def test_main_log_analysis_and_summary_diff(self):
        with patch('argparse.ArgumentParser.parse_args') as mock_args, \
             patch('builtins.input', return_value='y'), \
             patch('src.eda.eda_data_cleaner.run_data_cleaner', return_value=True), \
             patch('eda_batch_check.analyze_log', side_effect=[
                 {'total_files': 2, 'errors': 1},
                 {'total_files': 2, 'errors': 0}
             ]) as mock_analyze_log, \
             patch('eda_batch_check.print_summary_diff') as mock_print_diff, \
             patch('eda_batch_check.setup_logger'), \
             patch('eda_batch_check.find_data_files', return_value=[self.csv_file, self.parquet_file]), \
             patch('eda_batch_check.process_folder'), \
             patch('eda_batch_check.tqdm'):
            mock_args.return_value = type('Args', (), {
                'clean': True,
                'output_dir': os.path.join(self.test_dir, 'cleaned'),
                'csv_delimiter': '\t',
                'csv_header': '0',
                'handle_nan': 'ffill',
                'skip_verification': False,
                'log_file': self.log_file,
                'target_folders': [self.test_dir]
            })
            from eda_batch_check import main
            main()
            mock_print_diff.assert_called_once_with(
                {'total_files': 2, 'errors': 1},
                {'total_files': 2, 'errors': 0}
            )

    def test_main_verification_prompt_no(self):
        with patch('argparse.ArgumentParser.parse_args') as mock_args, \
             patch('builtins.input', return_value='n'), \
             patch('src.eda.eda_data_cleaner.run_data_cleaner', return_value=True), \
             patch('eda_batch_check.analyze_log', return_value={'total_files': 2}), \
             patch('eda_batch_check.print_summary_diff'), \
             patch('eda_batch_check.setup_logger'), \
             patch('eda_batch_check.find_data_files', return_value=[self.csv_file, self.parquet_file]), \
             patch('eda_batch_check.process_folder'), \
             patch('eda_batch_check.tqdm'):
            from eda_batch_check import main
            mock_args.return_value = type('Args', (), {
                'clean': True,
                'output_dir': os.path.join(self.test_dir, 'cleaned'),
                'csv_delimiter': '\t',
                'csv_header': '0',
                'handle_nan': 'ffill',
                'skip_verification': False,
                'log_file': self.log_file,
                'target_folders': [self.test_dir]
            })
            main()
            from eda_batch_check import analyze_log
            assert analyze_log.call_count == 1

if __name__ == '__main__':
    unittest.main()