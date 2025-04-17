# tests/calculation/test_core_calculations.py

import unittest
import pandas as pd
import numpy as np

# Import functions to test
from src.calculation.core_calculations import (
    calculate_hl,
    calculate_pressure,
    calculate_pv
)

# Unit tests for core indicator calculation functions
class TestCoreCalculations(unittest.TestCase):

    # Setup sample data for tests
    def setUp(self):
        self.high_prev = pd.Series([1.10, 1.12, 1.15, np.nan, 1.18])
        self.low_prev = pd.Series([1.08, 1.09, 1.11, 1.12, 1.16])
        self.volume_prev = pd.Series([1000, 1200, 1500, 1300, 1600])
        self.hl_prev2 = pd.Series([np.nan, 200, 300, 400, 200]) # HL in points already
        self.pressure = pd.Series([np.nan, 5.0, 5.0, 3.25, 8.0])
        self.pressure_prev = pd.Series([np.nan, np.nan, 5.0, 5.0, 3.25])
        self.point = 0.0001

    # Test calculate_hl function
    def test_calculate_hl(self):
        expected_hl = pd.Series([200.0, 300.0, 400.0, 0.0, 200.0]) # (high-low)/point, nan results in 0 after fillna
        calculated_hl = calculate_hl(self.high_prev, self.low_prev, self.point)
        pd.testing.assert_series_equal(calculated_hl, expected_hl, check_dtype=False)

    # Test calculate_hl with zero point size
    def test_calculate_hl_zero_point(self):
        with self.assertRaises(ValueError) as cm:
            calculate_hl(self.high_prev, self.low_prev, 0)
        self.assertIn("Point size cannot be zero", str(cm.exception))

    # Test calculate_pressure function
    def test_calculate_pressure(self):
        # Expected: volume_prev / hl_prev2
        # 1000/nan = nan
        # 1200/200 = 6.0
        # 1500/300 = 5.0
        # 1300/400 = 3.25
        # 1600/200 = 8.0
        expected_pressure = pd.Series([np.nan, 6.0, 5.0, 3.25, 8.0])
        calculated_pressure = calculate_pressure(self.volume_prev, self.hl_prev2)
        pd.testing.assert_series_equal(calculated_pressure, expected_pressure, check_dtype=False)

    # Test calculate_pressure with zero in hl_prev2
    def test_calculate_pressure_zero_hl(self):
        hl_prev2_with_zero = pd.Series([np.nan, 200, 0, 400, 200]) # Added a zero
        # Expected: division by zero (replaced by NaN) results in NaN
        # 1000/nan = nan
        # 1200/200 = 6.0
        # 1500/0 = nan
        # 1300/400 = 3.25
        # 1600/200 = 8.0
        expected_pressure = pd.Series([np.nan, 6.0, np.nan, 3.25, 8.0])
        calculated_pressure = calculate_pressure(self.volume_prev, hl_prev2_with_zero)
        pd.testing.assert_series_equal(calculated_pressure, expected_pressure, check_dtype=False)

    # Test calculate_pressure with NaN inputs
    def test_calculate_pressure_nan_inputs(self):
        volume_nan = pd.Series([1000, np.nan, 1500, 1300, 1600])
        hl_nan = pd.Series([np.nan, 200, 300, np.nan, 200])
         # Expected: nan wherever input is nan
        # 1000/nan = nan
        # nan/200 = nan
        # 1500/300 = 5.0
        # 1300/nan = nan
        # 1600/200 = 8.0
        expected_pressure = pd.Series([np.nan, np.nan, 5.0, np.nan, 8.0])
        calculated_pressure = calculate_pressure(volume_nan, hl_nan)
        pd.testing.assert_series_equal(calculated_pressure, expected_pressure, check_dtype=False)

    # Test calculate_pv function
    def test_calculate_pv(self):
        # Expected: pressure - pressure_prev
        # nan - nan = nan
        # 5.0 - nan = nan
        # 5.0 - 5.0 = 0.0
        # 3.25 - 5.0 = -1.75
        # 8.0 - 3.25 = 4.75
        expected_pv = pd.Series([np.nan, np.nan, 0.0, -1.75, 4.75])
        calculated_pv = calculate_pv(self.pressure, self.pressure_prev)
        pd.testing.assert_series_equal(calculated_pv, expected_pv, check_dtype=False)

    # Test calculate_pv with NaN inputs
    def test_calculate_pv_nan_inputs(self):
        pressure_nan = pd.Series([np.nan, 5.0, np.nan, 3.25, 8.0])
        pressure_prev_nan = pd.Series([np.nan, np.nan, 5.0, np.nan, 3.25])
         # Expected: nan wherever input is nan
        # nan - nan = nan
        # 5.0 - nan = nan
        # nan - 5.0 = nan
        # 3.25 - nan = nan
        # 8.0 - 3.25 = 4.75
        expected_pv = pd.Series([np.nan, np.nan, np.nan, np.nan, 4.75])
        calculated_pv = calculate_pv(pressure_nan, pressure_prev_nan)
        pd.testing.assert_series_equal(calculated_pv, expected_pv, check_dtype=False)


# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()