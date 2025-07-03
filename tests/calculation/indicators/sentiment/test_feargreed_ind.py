#!/usr/bin/env python3
"""
Unit tests for feargreed_ind
"""

import pytest
import pandas as pd
import numpy as np
import os
from src.calculation.indicators.sentiment.feargreed_ind import calculate_feargreed

def test_feargreed_ind_file_exists():
    """Test that feargreed_ind file exists"""
    file_path = "src/calculation/indicators/sentiment/feargreed_ind.py"
    assert os.path.exists(file_path), f"feargreed_ind file not found: {file_path}"

def test_feargreed_ind_import():
    """Test that feargreed_ind can be imported"""
    try:
        import src.calculation.indicators.sentiment.feargreed_ind
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import feargreed_ind: {e}")

def test_feargreed_ind_basic_functionality():
    """Test basic feargreed_ind functionality"""
    try:
        # Test that the module can be imported and has expected attributes
        module = __import__("src.calculation.indicators.sentiment.feargreed_ind", fromlist=["*"])
        
        # Check if module has any functions or classes
        module_attrs = [attr for attr in dir(module) if not attr.startswith("_")]
        assert len(module_attrs) > 0, f"No public attributes found in feargreed_ind"
        
    except Exception as e:
        pytest.fail(f"Basic functionality test failed: {e}")

def test_feargreed_ind_module_structure():
    """Test feargreed_ind module structure"""
    try:
        module = __import__("src.calculation.indicators.sentiment.feargreed_ind", fromlist=["*"])
        
        # Check for common indicator patterns
        has_functions = any(callable(getattr(module, attr)) for attr in dir(module) if not attr.startswith("_"))
        assert has_functions, f"No functions found in feargreed_ind"
        
    except Exception as e:
        pytest.fail(f"Module structure test failed: {e}")

def test_feargreed_enough_data():
    # 30 точек, период 14
    data = pd.Series(np.linspace(1, 2, 30))
    result = calculate_feargreed(data, period=14)
    # После периода должны быть не только NaN
    assert result.iloc[14:].notna().any(), "Fear & Greed must return non-NaN values if enough data"
    # До периода должны быть NaN
    assert result.iloc[:14].isna().all(), "First period values must be NaN"

def test_feargreed_not_enough_data():
    # 10 точек, период 14
    data = pd.Series(np.linspace(1, 2, 10))
    result = calculate_feargreed(data, period=14)
    assert result.isna().all(), "If not enough data, all values must be NaN"
