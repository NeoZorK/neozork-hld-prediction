#!/usr/bin/env python3
"""
Script to generate minimal unit tests for uncovered files
"""

import os
import sys
from pathlib import Path

def generate_test_file(src_file_path, test_file_path):
    """Generate a minimal test file for the given source file"""
    
    # Extract module name and class name
    module_name = src_file_path.stem
    class_name = ''.join(word.capitalize() for word in module_name.split('_')) + 'Indicator'
    
    # Determine import path
    rel_path = src_file_path.relative_to(Path("src"))
    import_path = f"src.{'.'.join(rel_path.parts[:-1])}.{module_name}"
    
    # Generate test content
    test_content = f'''#!/usr/bin/env python3
"""
Unit tests for {module_name}
"""

import pytest
import pandas as pd
import numpy as np

def test_{module_name}_import():
    """Test that {class_name} can be imported"""
    try:
        from {import_path} import {class_name}
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import {class_name}: {{e}}")

def test_{module_name}_basic_functionality():
    """Test basic {class_name} functionality"""
    try:
        from {import_path} import {class_name}
        
        # Create test data
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        df = pd.DataFrame({{
            'Open': np.random.rand(100) * 100,
            'High': np.random.rand(100) * 100 + 1,
            'Low': np.random.rand(100) * 100 - 1,
            'Close': np.random.rand(100) * 100,
            'Volume': np.random.randint(1000, 10000, 100)
        }}, index=dates)
        
        # Test indicator creation
        indicator = {class_name}()
        assert indicator is not None
        
        # Test calculation (should not raise exception)
        try:
            result = indicator.calculate(df)
            assert isinstance(result, pd.DataFrame)
        except Exception as e:
            pytest.fail(f"{class_name} calculation failed: {{e}}")
    except Exception as e:
        pytest.fail(f"Test failed: {{e}}")

def test_{module_name}_with_parameters():
    """Test {class_name} with custom parameters"""
    try:
        from {import_path} import {class_name}
        
        # Create test data
        dates = pd.date_range('2024-01-01', periods=50, freq='D')
        df = pd.DataFrame({{
            'Open': np.random.rand(50) * 100,
            'High': np.random.rand(50) * 100 + 1,
            'Low': np.random.rand(50) * 100 - 1,
            'Close': np.random.rand(50) * 100,
            'Volume': np.random.randint(1000, 10000, 50)
        }}, index=dates)
        
        # Test with custom parameters
        indicator = {class_name}()
        try:
            result = indicator.calculate(df, period=14)
            assert isinstance(result, pd.DataFrame)
        except Exception as e:
            pytest.fail(f"{class_name} calculation with parameters failed: {{e}}")
    except Exception as e:
        pytest.fail(f"Test failed: {{e}}")
'''
    
    # Write test file
    test_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(test_file_path, 'w') as f:
        f.write(test_content)
    
    print(f"Generated test: {test_file_path}")

def main():
    """Generate tests for all uncovered files"""
    
    # List of uncovered files from the analysis
    uncovered_files = [
        "src/calculation/indicators/momentum/macd_ind.py",
        "src/calculation/indicators/momentum/stochoscillator_ind.py",
        "src/calculation/indicators/oscillators/cci_ind.py",
        "src/calculation/indicators/oscillators/rsi_ind.py",
        "src/calculation/indicators/oscillators/stoch_ind.py",
        "src/calculation/indicators/predictive/hma_ind.py",
        "src/calculation/indicators/predictive/tsforecast_ind.py",
        "src/calculation/indicators/probability/kelly_ind.py",
        "src/calculation/indicators/probability/montecarlo_ind.py",
        "src/calculation/indicators/sentiment/cot_ind.py",
        "src/calculation/indicators/sentiment/feargreed_ind.py",
        "src/calculation/indicators/sentiment/putcallratio_ind.py",
        "src/calculation/indicators/suportresist/donchain_ind.py",
        "src/calculation/indicators/suportresist/fiboretr_ind.py",
        "src/calculation/indicators/suportresist/pivot_ind.py",
        "src/calculation/indicators/trend/adx_ind.py",
        "src/calculation/indicators/trend/ema_ind.py",
        "src/calculation/indicators/trend/sar_ind.py",
        "src/calculation/indicators/trend/supertrend_ind.py",
        "src/calculation/indicators/volatility/atr_ind.py",
        "src/calculation/indicators/volatility/bb_ind.py",
        "src/calculation/indicators/volatility/stdev_ind.py",
        "src/calculation/indicators/volume/obv_ind.py",
        "src/calculation/indicators/volume/vwap_ind.py",
    ]
    
    for src_file in uncovered_files:
        src_path = Path(src_file)
        if src_path.exists():
            # Create corresponding test path
            test_path = Path("tests") / src_path.relative_to(Path("src"))
            test_path = test_path.parent / f"test_{test_path.name}"
            
            generate_test_file(src_path, test_path)
        else:
            print(f"Warning: Source file not found: {src_file}")
    
    print("\nTest generation completed!")

if __name__ == "__main__":
    main() 