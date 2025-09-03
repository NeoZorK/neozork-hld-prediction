#!/usr/bin/env python3
"""
Test script to verify the Docker fix is working.
"""

import sys
import os
import subprocess

def test_docker_fix():
    """Test the Docker fix by running the interactive system."""
    print("🚀 Testing Docker Fix...")
    
    # Create a simple test script that simulates the problematic scenario
    test_script = """
import sys
import os
sys.path.append('/app/src')

try:
    from src.interactive.core.interactive_system import InteractiveSystem
    import pandas as pd
    
    # Initialize system
    system = InteractiveSystem()
    
    # Load test data
    data_path = '/app/data/sample_ohlcv_with_issues.csv'
    system.current_data = pd.read_csv(data_path)
    print(f"Data loaded, shape: {system.current_data.shape}")
    
    # Run comprehensive data quality check
    print("Running comprehensive data quality check...")
    system.run_comprehensive_data_quality_check()
    print("Comprehensive data quality check completed!")
    
    # Check if we can continue after the check
    print("System is still running after comprehensive data quality check!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
    
    # Write test script to file
    script_path = "/tmp/test_docker_fix.py"
    with open(script_path, "w") as f:
        f.write(test_script)
    
    try:
        # Copy script to container
        subprocess.run(f"docker cp {script_path} neozork-hld-prediction-neozork-hld-1:/app/", shell=True, check=True)
        
        # Run script in container
        cmd = "docker-compose exec neozork-hld python /app/test_docker_fix.py"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        print("✅ Docker fix test executed successfully!")
        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout}")
        
        if result.returncode == 0:
            print("✅ Docker fix test passed!")
            return True
        else:
            print(f"❌ Docker fix test failed with return code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running Docker fix test: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(script_path):
            os.remove(script_path)

def test_interactive_system_continuation():
    """Test that the interactive system continues after input errors."""
    print("🚀 Testing Interactive System Continuation...")
    
    # Create input that will trigger EOFError
    input_sequence = [
        "1\n",  # Load data
        "1\n",  # Select data folder
        "\n",   # Accept all files
        "n\n",  # No preview
        "\n",   # Continue
        "2\n",  # EDA Analysis
        "1\n",  # Comprehensive Data Quality Check
        "y\n",  # Convert timestamp columns
        # Note: We don't provide input for "Do you want to fix all issues?" 
        # This should trigger EOFError and the system should continue
    ]
    
    # Create input file
    input_file = "/tmp/test_input_eof.txt"
    with open(input_file, "w") as f:
        f.writelines(input_sequence)
    
    try:
        # Run interactive system with input that will cause EOFError
        cmd = f"docker-compose exec -T neozork-hld bash -c 'cat {input_file} | timeout 30 python /app/interactive_system.py'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        print("✅ Interactive system continuation test executed!")
        print(f"Return code: {result.returncode}")
        print(f"Output length: {len(result.stdout)}")
        
        # Check if the system handled the EOFError gracefully
        if "Skipping fixes due to input error" in result.stdout:
            print("✅ System handled EOFError gracefully!")
            return True
        else:
            print("❌ System did not handle EOFError gracefully")
            print(f"Output: {result.stdout}")
            return False
            
    except Exception as e:
        print(f"❌ Error running interactive system continuation test: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(input_file):
            os.remove(input_file)

if __name__ == "__main__":
    print("🚀 Docker Fix Verification Tests")
    print("=" * 50)
    
    # Test 1: Basic Docker fix
    print("\n" + "="*50)
    print("TEST 1: Basic Docker Fix")
    print("="*50)
    success1 = test_docker_fix()
    
    # Test 2: Interactive system continuation
    print("\n" + "="*50)
    print("TEST 2: Interactive System Continuation")
    print("="*50)
    success2 = test_interactive_system_continuation()
    
    if success1 and success2:
        print("\n✅ All Docker fix verification tests passed!")
        print("🔧 The Docker input issue has been successfully resolved!")
        sys.exit(0)
    else:
        print("\n❌ Some Docker fix verification tests failed!")
        sys.exit(1)
