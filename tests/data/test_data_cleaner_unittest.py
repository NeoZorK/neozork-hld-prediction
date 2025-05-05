import os
import sys
import tempfile
import unittest
import argparse
import pandas as pd

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from scripts.data_processing.data_cleaner_v2 import (
    setup_logger,
    find_data_files,
    clean_file,
    parse_header
)

class TestDataCleaner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment before all tests."""
        cls.temp_dir = tempfile.mkdtemp()
        
        # Set up logger
        log_file = os.path.join(cls.temp_dir, "test.log")
        cls.logger = setup_logger(log_file)
        
        # Create sample CSV file with duplicates
        cls.sample_csv_path = os.path.join(cls.temp_dir, "test.csv")
        df_csv = pd.DataFrame({
            'A': [1, 1, 2, 2, 3, None],  # Two pairs of duplicates and one unique value
            'B': ['a', 'a', 'b', 'b', 'c', None],  # Same pattern as A
            'C': [1.1, 1.1, 2.2, 2.2, 3.3, None]  # Same pattern as A and B
        })
        df_csv.to_csv(cls.sample_csv_path, index=False)
        
        # Create sample Parquet file with the same data
        cls.sample_parquet_path = os.path.join(cls.temp_dir, "test.parquet")
        df_parquet = pd.DataFrame({
            'A': [1, 1, 2, 2, 3, None],
            'B': ['a', 'a', 'b', 'b', 'c', None],
            'C': [1.1, 1.1, 2.2, 2.2, 3.3, None]
        })
        df_parquet.to_parquet(cls.sample_parquet_path, index=False)
        
        # Create output directory
        cls.output_dir = os.path.join(cls.temp_dir, "output")
        os.makedirs(cls.output_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        import shutil
        shutil.rmtree(cls.temp_dir)

    def test_setup_logger(self):
        """Test logger setup."""
        self.assertIsNotNone(self.logger)
        self.assertEqual(len(self.logger.handlers), 2)  # File and console handlers
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "test.log")))

    def test_find_data_files(self):
            """Test finding data files in directory."""
            files = find_data_files([self.temp_dir])
            # Filter files to include only .csv and .parquet
            filtered_files = [f for f in files if f[0].endswith(('.csv', '.parquet'))]
            self.assertEqual(len(filtered_files), 2)
            self.assertTrue(any(self.sample_csv_path in f[0] for f in filtered_files))
            self.assertTrue(any(self.sample_parquet_path in f[0] for f in filtered_files))

    def test_clean_file_csv_duplicates(self):
        """Test cleaning CSV file with duplicates."""
        output_file = os.path.join(self.output_dir, "raw_parquet", "test.csv")  # Updated path
        print(f"Expected output file path: {output_file}")  # Debug log

        # Run the cleaning process
        result = clean_file(
            input_path=self.sample_csv_path,
            input_base_dir=self.temp_dir,
            output_base_dir=self.output_dir,
            handle_duplicates="remove",
            handle_nan="ffill",
            csv_delimiter=",",
            csv_header=0
        )

        # Check if the cleaning process succeeded
        self.assertTrue(result, "The clean_file function returned False.")

        # Check if the file exists
        if not os.path.exists(output_file):
            print(f"File not found at: {output_file}")  # Debug log
        self.assertTrue(os.path.exists(output_file), f"Output file not found at {output_file}")

        # Verify the contents of the cleaned file
        df = pd.read_csv(output_file)
        self.assertEqual(len(df), 3, "The cleaned file does not have the expected number of rows.")

    def test_clean_file_parquet_nan(self):
            """Test cleaning Parquet file with NaN values."""
            output_file = os.path.join(self.output_dir, "raw_parquet", "test.parquet")  # Updated path
            print(f"Expected output file path: {output_file}")  # Debug log

            # Run the cleaning process
            result = clean_file(
                input_path=self.sample_parquet_path,
                input_base_dir=self.temp_dir,
                output_base_dir=self.output_dir,
                handle_duplicates="remove",
                handle_nan="ffill",
                csv_delimiter=",",
                csv_header=0
            )

            # Check if the cleaning process succeeded
            self.assertTrue(result, "The clean_file function returned False.")

            # Check if the file exists
            if not os.path.exists(output_file):
                print(f"File not found at: {output_file}")  # Debug log
            self.assertTrue(os.path.exists(output_file), f"Output file not found at {output_file}")

            # Verify the contents of the cleaned file
            df = pd.read_parquet(output_file)
            self.assertEqual(df.isnull().sum().sum(), 0, "NaN values remain in the cleaned file.")

    def test_clean_file_invalid_input(self):
        """Test handling of invalid input file."""
        invalid_file = os.path.join(self.temp_dir, "invalid.txt")
        with open(invalid_file, 'w') as f:
            f.write("test")
        
        result = clean_file(
            input_path=invalid_file,
            input_base_dir=self.temp_dir,
            output_base_dir=self.output_dir,
            handle_duplicates="remove",
            handle_nan="ffill",
            csv_delimiter=",",
            csv_header=0
        )
        
        self.assertFalse(result)

    def test_parse_header(self):
        """Test header parsing function."""
        self.assertEqual(parse_header("0"), 0)
        self.assertEqual(parse_header("1"), 1)
        self.assertIsNone(parse_header("infer"))
        self.assertIsNone(parse_header("none"))
        
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_header("invalid")

    def test_clean_file_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        empty_file = os.path.join(self.temp_dir, "empty.csv")
        pd.DataFrame().to_csv(empty_file, index=False)
        
        result = clean_file(
            input_path=empty_file,
            input_base_dir=self.temp_dir,
            output_base_dir=self.output_dir,
            handle_duplicates="remove",
            handle_nan="ffill",
            csv_delimiter=",",
            csv_header=0
        )
        
        self.assertTrue(result)
        output_file = os.path.join(self.output_dir, "empty.csv")
        self.assertFalse(os.path.exists(output_file))  # Empty files should not be saved

    def test_clean_file_different_nan_strategies(self):
        """Test different NaN handling strategies."""
        # Test ffill strategy
        result_ffill = clean_file(
            input_path=self.sample_csv_path,
            input_base_dir=self.temp_dir,
            output_base_dir=self.output_dir,
            handle_duplicates="remove",
            handle_nan="ffill",
            csv_delimiter=",",
            csv_header=0
        )
        self.assertTrue(result_ffill)
        
        # Test dropna_rows strategy
        result_dropna = clean_file(
            input_path=self.sample_csv_path,
            input_base_dir=self.temp_dir,
            output_base_dir=self.output_dir,
            handle_duplicates="remove",
            handle_nan="dropna_rows",
            csv_delimiter=",",
            csv_header=0
        )
        self.assertTrue(result_dropna)
        
        # Test none strategy
        result_none = clean_file(
            input_path=self.sample_csv_path,
            input_base_dir=self.temp_dir,
            output_base_dir=self.output_dir,
            handle_duplicates="remove",
            handle_nan="none",
            csv_delimiter=",",
            csv_header=0
        )
        self.assertTrue(result_none)

if __name__ == '__main__':
    unittest.main() 