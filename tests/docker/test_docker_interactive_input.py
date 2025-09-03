#!/usr/bin/env python3
"""
Test script to simulate real interactive input in Docker.
This script tests the input handling in the interactive system.
"""

import sys
import os
import io
import subprocess
from unittest.mock import patch

def test_real_interactive_input():
    """Test real interactive input handling."""
    print("🚀 Testing Real Interactive Input...")
    
    # Create input file with predefined responses
    input_file = "/tmp/test_input.txt"
    with open(input_file, "w") as f:
        f.write("1\n")  # Load data
        f.write("1\n")  # Select data folder
        f.write("\n")   # Accept all files
        f.write("n\n")  # No preview
        f.write("\n")   # Continue
        f.write("2\n")  # EDA Analysis
        f.write("1\n")  # Comprehensive Data Quality Check
        f.write("y\n")  # Convert timestamp columns
        f.write("y\n")  # Fix all issues
        f.write("0\n")  # Back to main menu
        f.write("0\n")  # Exit
    
    try:
        # Run interactive system with input from file
        cmd = f"docker-compose exec -T neozork-hld bash -c 'cat {input_file} | python /app/interactive_system.py'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        print("✅ Command executed successfully!")
        print(f"Return code: {result.returncode}")
        print(f"Output length: {len(result.stdout)}")
        
        if result.returncode == 0:
            print("✅ Interactive system completed successfully!")
            return True
        else:
            print(f"❌ Interactive system failed with return code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running interactive system: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(input_file):
            os.remove(input_file)

def test_docker_interactive_direct():
    """Test Docker interactive system directly."""
    print("🚀 Testing Docker Interactive System Directly...")
    
    # Create a simple test script that runs the interactive system
    test_script = """
import sys
import os
sys.path.append('/app/src')

try:
    from src.interactive.core.interactive_system import InteractiveSystem
    
    # Initialize system
    system = InteractiveSystem()
    
    # Load test data
    import pandas as pd
    data_path = '/app/data/sample_ohlcv_with_issues.csv'
    system.current_data = pd.read_csv(data_path)
    print(f"Data loaded, shape: {system.current_data.shape}")
    
    # Run comprehensive data quality check
    print("Running comprehensive data quality check...")
    system.run_comprehensive_data_quality_check()
    print("Comprehensive data quality check completed!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
    
    # Write test script to file
    script_path = "/tmp/test_docker_script.py"
    with open(script_path, "w") as f:
        f.write(test_script)
    
    try:
        # Copy script to container
        subprocess.run(f"docker cp {script_path} neozork-hld-prediction-neozork-hld-1:/app/", shell=True, check=True)
        
        # Run script in container
        cmd = "docker-compose exec neozork-hld python /app/test_docker_script.py"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        print("✅ Docker script executed successfully!")
        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ Docker interactive system completed successfully!")
            return True
        else:
            print(f"❌ Docker interactive system failed with return code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running Docker script: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(script_path):
            os.remove(script_path)

if __name__ == "__main__":
    print("🚀 Starting Docker Interactive Input Tests...")
    
    # Test 1: Real interactive input
    print("\n" + "="*50)
    print("TEST 1: Real Interactive Input")
    print("="*50)
    success1 = test_real_interactive_input()
    
    # Test 2: Docker interactive direct
    print("\n" + "="*50)
    print("TEST 2: Docker Interactive Direct")
    print("="*50)
    success2 = test_docker_interactive_direct()
    
    if success1 and success2:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
