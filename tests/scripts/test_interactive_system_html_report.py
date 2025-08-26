#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for HTML report with Recommendations/Summary and seaborn fixes.
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import patch

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from interactive_system import InteractiveSystem

def test_html_and_plots():
    """Test HTML report generation and seaborn plots without errors."""
    
    # Create sample data
    np.random.seed(42)
    data = pd.DataFrame({
        'Open': np.random.normal(100, 10, 1000),
        'High': np.random.normal(102, 10, 1000),
        'Low': np.random.normal(98, 10, 1000),
        'Close': np.random.normal(101, 10, 1000),
        'Volume': np.random.exponential(1000, 1000),  # Skewed data
        'predicted_high': np.random.normal(102, 5, 1000),
        'predicted_low': np.random.normal(98, 5, 1000),
        'pressure': np.random.uniform(0, 10, 1000),
        'pressure_vector': np.random.normal(0, 1, 1000)
    })
    
    # Create interactive system
    system = InteractiveSystem()
    system.current_data = data
    
    print("🧪 Testing HTML Report with Recommendations/Summary...")
    print("=" * 60)
    
    # Run basic statistics to generate data for HTML report
    print("\n1. Running Basic Statistics...")
    with patch('builtins.input', return_value='n'):
        system.run_basic_statistics()
    
    # Verify that basic statistics results are saved
    assert 'basic_statistics' in system.current_results
    assert 'analysis_summary' in system.current_results['basic_statistics']
    
    print("\n2. Generating HTML Report...")
    system.generate_html_report()
    
    print("\n✅ Test completed!")
    print("📁 Check reports/ folder for HTML report")
    print("📁 Check results/plots/statistics/ for plots")

if __name__ == "__main__":
    test_html_and_plots()
