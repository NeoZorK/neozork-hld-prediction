# -*- coding: utf-8 -*-
# tests/cli/test_cli_show_mode.py

import unittest
import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path

class TestCLIShowMode(unittest.TestCase):
    """
    Unit tests for the 'show' mode of the CLI.
    The tests simulate CLI calls and check output correctness.
    """

    @classmethod
    def setUpClass(cls):
        """
        Prepare a temporary directory structure and minimal Parquet file for testing show mode.
        """
        # Save original working directory to restore later
        cls._orig_cwd = os.getcwd()
        # Root of the project (where run_analysis.py is)
        cls._project_root = os.path.abspath(os.path.dirname(__file__))
        while not os.path.exists(os.path.join(cls._project_root, "run_analysis.py")):
            up = os.path.dirname(cls._project_root)
            if up == cls._project_root:
                raise RuntimeError("run_analysis.py not found in any parent directory.")
            cls._project_root = up

        # Create a temp directory for test data
        cls.test_dir = tempfile.mkdtemp()
        os.chdir(cls.test_dir)

        # Create necessary data directories
        os.makedirs("data/raw_parquet", exist_ok=True)
        os.makedirs("data/cache/csv_converted", exist_ok=True)

        # Generate a minimal DataFrame and save as Parquet for testing
        try:
            import pandas as pd
            import pyarrow as pa
            import pyarrow.parquet as pq

            df = pd.DataFrame({
                "Open": [1.0, 2.0],
                "High": [2.0, 3.0],
                "Low": [0.5, 1.5],
                "Close": [1.5, 2.5],
                "Volume": [100, 200],
                "HL": [1, 2]
            }, index=pd.date_range("2025-01-01", periods=2, freq="D"))
            df.index.name = "DateTime"
            parquet_path = Path("data/raw_parquet/yfinance_TEST.parquet")
            df.to_parquet(parquet_path)
            cls.test_file_path = parquet_path
        except ImportError:
            cls.test_file_path = None

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the temporary directory after tests.
        """
        os.chdir(cls._orig_cwd)
        shutil.rmtree(cls.test_dir)

    def _run_cli_show(self, *args):
        """
        Helper to run the CLI in 'show' mode with given arguments and capture output.
        Uses the main run_analysis.py from the project root.
        """
        cli_path = os.path.join(self._project_root, "run_analysis.py")
        if not os.path.exists(cli_path):
            self.skipTest("run_analysis.py not found in project root.")

        # PYTHONPATH must include src for imports to work
        pythonpath = os.path.join(self._project_root, "src")
        env = os.environ.copy()
        env["PYTHONPATH"] = pythonpath + (os.pathsep + env.get("PYTHONPATH", ""))

        # Run from self.test_dir so relative paths for data work
        command = [sys.executable, cli_path, "show"] + list(args)
        result = subprocess.run(command, capture_output=True, text=True, env=env, cwd=self.test_dir)
        return result

    def test_show_help_shows_available_data(self):
        """
        Test 'show' mode with no additional arguments (should print help and available data files).
        """
        result = self._run_cli_show()
        self.assertEqual(result.returncode, 0, msg=f"stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn("SHOW MODE HELP", result.stdout)
        self.assertIn("AVAILABLE DATA FILES", result.stdout)

    def test_show_lists_yfinance_files(self):
        """
        Test 'show' mode with 'yf' or 'yfinance' as source (should list yfinance files).
        """
        if not self.test_file_path:
            self.skipTest("Required pyarrow/pandas not installed or Parquet file not created.")
        result = self._run_cli_show("yf")
        self.assertEqual(result.returncode, 0, msg=f"stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn("Searching for 'yfinance' files", result.stdout)
        self.assertIn("Found 1 file(s)", result.stdout)
        self.assertIn("yfinance_TEST.parquet", result.stdout)

    def test_show_with_keywords_filters_files(self):
        """
        Test 'show' mode with a keyword that matches the test file.
        """
        if not self.test_file_path:
            self.skipTest("Required pyarrow/pandas not installed or Parquet file not created.")
        result = self._run_cli_show("yfinance", "test")
        self.assertEqual(result.returncode, 0, msg=f"stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn("Found 1 file(s)", result.stdout)
        self.assertIn("yfinance_TEST.parquet", result.stdout)

    def test_show_with_nonexistent_keyword(self):
        """
        Test 'show' mode with a keyword that does not match any file (should find zero files).
        """
        result = self._run_cli_show("yfinance", "doesnotexist")
        self.assertEqual(result.returncode, 0, msg=f"stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn("Found 0 file(s)", result.stdout)

    def test_show_triggers_plot_or_calc_message(self):
        """
        Test that 'show' triggers either the plot logic or indicator calculation when a single file is found.
        Accepts both possible CLI behaviors for robustness.
        """
        if not self.test_file_path:
            self.skipTest("Required pyarrow/pandas not installed or Parquet file not created.")
        result = self._run_cli_show("yf")
        self.assertEqual(result.returncode, 0, msg=f"stdout: {result.stdout}\nstderr: {result.stderr}")
        out = result.stdout
        # Accept both: plot logic or indicator calculation logic
        self.assertTrue(
            ("Triggering plot with method: 'fastest'" in out or
             "Loading file data and triggering plot with method: 'fastest'" in out or
             "INDICATOR CALCULATION MODE" in out or
             "calculated and shown above." in out or
             "Drawing raw OHLCV data chart using method: 'fastest'" in out),
            msg=f"stdout: {out}\nstderr: {result.stderr}"
        )

    def test_show_csv_cot_rule(self):
        """Test CLI: run_analysis.py show csv mn1 -d fastest --rule cot:10,close"""
        import subprocess
        import sys
        import pandas as pd
        import tempfile
        from pathlib import Path
        # Путь к run_analysis.py
        script_path = os.path.join(self._project_root, "run_analysis.py")
        assert os.path.exists(script_path)
        # Создаём временный parquet-файл с нужными колонками и именем mn1 в текущей рабочей директории
        data_dir = Path("data") / "cache" / "csv_converted"
        data_dir.mkdir(parents=True, exist_ok=True)
        temp_file = data_dir / "CSVExport_GBPUSD_PERIOD_MN1.parquet"
        df = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05],
            'Volume': [100, 200, 300]
        }, index=pd.date_range('2020-01-01', periods=3, freq='D'))
        df.to_parquet(temp_file)
        try:
            # Запускаем команду
            result = subprocess.run([
                sys.executable, script_path, "show", "csv", "mn1", "-d", "fastest", "--rule", "cot:10,close"
            ], capture_output=True, text=True)
            assert result.returncode == 0, f"CLI error: {result.stderr}"
            assert "Indicator 'COT' calculated successfully." in result.stdout
            assert "COT" in result.stdout
            assert "COT_Signal" in result.stdout
        finally:
            if temp_file.exists():
                temp_file.unlink()

if __name__ == '__main__':
    unittest.main()

