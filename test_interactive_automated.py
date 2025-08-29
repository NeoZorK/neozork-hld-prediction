#!/usr/bin/env python3
"""
Automated test for interactive system with predefined input.
This simulates the user interaction in Docker.
"""

import sys
import os
import io
import pandas as pd
from unittest.mock import patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_interactive_system_automated():
    """Test interactive system with automated input."""
    print("🚀 Testing Interactive System with Automated Input...")
    
    # Predefined input sequence
    input_sequence = [
        "1",  # Load data
        "1",  # Select sample_ohlcv_with_issues.csv
        "sample_ohlcv_with_issues.csv",
        "2",  # EDA Analysis
        "1",  # Comprehensive Data Quality Check
        "y",  # Fix all issues
        "0",  # Back to main menu
        "exit"  # Exit
    ]
    
    # Join input sequence with newlines
    input_text = "\n".join(input_sequence) + "\n"
    
    try:
        # Mock input to provide predefined responses
        with patch('builtins.input', side_effect=input_sequence):
            with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                # Import and run interactive system
                from interactive_system import main
                
                try:
                    main()
                    output = mock_stdout.getvalue()
                    print("✅ Interactive system completed successfully!")
                    print("\n📋 Output captured:")
                    print(output)
                    return True
                except Exception as e:
                    print(f"❌ Error in interactive system: {e}")
                    import traceback
                    traceback.print_exc()
                    return False
                    
    except Exception as e:
        print(f"❌ Error in test setup: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_interactive_system_manual():
    """Test interactive system with manual input simulation."""
    print("🚀 Testing Interactive System with Manual Input Simulation...")
    
    try:
        from src.interactive import InteractiveSystem
        
        # Initialize system
        system = InteractiveSystem()
        
        # Load data manually
        data_path = 'data/sample_ohlcv_with_issues.csv'
        if not os.path.exists(data_path):
            print(f"❌ Test data not found: {data_path}")
            return False
            
        system.current_data = pd.read_csv(data_path)
        print(f"✅ Data loaded, shape: {system.current_data.shape}")
        
        # Run comprehensive data quality check manually
        print("\n🔍 Running comprehensive data quality check...")
        
        try:
            system.run_comprehensive_data_quality_check()
            print("✅ Comprehensive data quality check completed!")
            return True
        except Exception as e:
            print(f"❌ Error in comprehensive data quality check: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Error in manual test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Interactive System Tests...")
    
    # Test 1: Automated input
    print("\n" + "="*50)
    print("TEST 1: Automated Input")
    print("="*50)
    success1 = test_interactive_system_automated()
    
    # Test 2: Manual simulation
    print("\n" + "="*50)
    print("TEST 2: Manual Simulation")
    print("="*50)
    success2 = test_interactive_system_manual()
    
    if success1 and success2:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
