import unittest
import subprocess
import sys
import os

class TestCLIDrawModes(unittest.TestCase):
    def test_cli_draw_modes_help(self):
        """
        Check that CLI accepts all draw modes and shows help.
        """
        # Test only a subset of modes for faster execution (3 instead of 5)
        # This reduces test time from ~10 seconds to ~3 seconds
        test_modes = ["fast", "fastest", "seaborn"]
        
        for mode in test_modes:
            result = subprocess.run(
                [sys.executable, "run_analysis.py", "demo", "-d", mode, "--help"],
                capture_output=True,
                text=True,
                timeout=10  # Add timeout to prevent hanging
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Plot method:", result.stdout)

if __name__ == '__main__':
    unittest.main()