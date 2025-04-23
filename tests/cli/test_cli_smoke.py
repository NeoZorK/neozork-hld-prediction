import unittest
import subprocess
import sys
import os

class TestCLIDrawModes(unittest.TestCase):
    def test_cli_draw_modes_help(self):
        """
        Check that CLI accepts all draw modes and shows help.
        """
        for mode in ["fast", "plotly", "mpl", "mplfinance"]:
            result = subprocess.run(
                [sys.executable, "run_analysis.py", "demo", "-d", mode, "--help"],
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Choose plotting library", result.stdout)

if __name__ == '__main__':
    unittest.main()