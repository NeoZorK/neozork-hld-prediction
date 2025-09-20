#!/usr/bin/env python3
"""
Demo script to test the data cleaning system with automated input.
"""

import subprocess
import sys
from pathlib import Path

def test_cleaning_system():
    """Test the cleaning system with automated input."""
    
    # Test file
    test_file = "binance_BTCUSDT_MN1.parquet"
    
    print(f"Testing data cleaning system with file: {test_file}")
    print("="*60)
    
    # Prepare input responses
    input_responses = [
        "y",  # Proceed with cleaning
        "y",  # Fix gaps
        "y",  # Fix duplicates  
        "y",  # Fix NaN
        "y",  # Fix zeros
        "y",  # Fix negative
        "y",  # Fix infinity
        "y",  # Fix outliers
        "y",  # Save cleaned data
    ]
    
    # Join responses with newlines
    input_text = "\n".join(input_responses) + "\n"
    
    try:
        # Run the cleaning script
        result = subprocess.run(
            [sys.executable, "clear_data.py", "-f", test_file],
            input=input_text,
            text=True,
            capture_output=True,
            timeout=60  # 60 second timeout
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nReturn code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Data cleaning completed successfully!")
        else:
            print("❌ Data cleaning failed!")
            
    except subprocess.TimeoutExpired:
        print("⏰ Process timed out after 60 seconds")
    except Exception as e:
        print(f"❌ Error running cleaning system: {e}")

if __name__ == "__main__":
    test_cleaning_system()
