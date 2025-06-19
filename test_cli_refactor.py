#!/usr/bin/env python3
"""Test script for the refactored CLI show mode"""

import sys
import os
sys.path.insert(0, '/workspaces/neozork-hld-prediction')

# Ensure we're in the right directory
os.chdir('/workspaces/neozork-hld-prediction')

def test_imports():
    print("=== Testing Imports ===")
    try:
        from src.cli.cli_show_common import show_indicator_help, count_indicator_files
        print("✓ Successfully imported from cli_show_common")
        
        from src.cli.cli_show_indicators import handle_indicator_mode
        print("✓ Successfully imported handle_indicator_mode")
        
        from src.cli.cli_show_ind_parquet import handle_parquet_indicators
        print("✓ Successfully imported handle_parquet_indicators")
        
        from src.cli.cli_show_ind_csv import handle_csv_indicators
        print("✓ Successfully imported handle_csv_indicators")
        
        from src.cli.cli_show_ind_json import handle_json_indicators
        print("✓ Successfully imported handle_json_indicators")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_help_function():
    print("\n=== Testing Help Function ===")
    try:
        from src.cli.cli_show_common import show_indicator_help
        show_indicator_help()
        return True
    except Exception as e:
        print(f"✗ Help function error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_count():
    print("\n=== Testing File Count ===")
    try:
        from src.cli.cli_show_common import count_indicator_files
        counts = count_indicator_files()
        print(f"Indicator file counts: {counts}")
        return True
    except Exception as e:
        print(f"✗ File count error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_indicator_mode():
    print("\n=== Testing Indicator Mode ===")
    try:
        from src.cli.cli_show_indicators import handle_indicator_mode
        
        # Create a test args object
        class TestArgs:
            def __init__(self):
                self.source = 'ind'
                self.keywords = ['help']
                self.start = None
                self.end = None
        
        args = TestArgs()
        result = handle_indicator_mode(args)
        print(f"Result: {result}")
        return True
    except Exception as e:
        print(f"✗ Indicator mode error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Refactored CLI Show Mode")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_help_function()
    success &= test_file_count()
    success &= test_indicator_mode()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed!")
    
    sys.exit(0 if success else 1)
