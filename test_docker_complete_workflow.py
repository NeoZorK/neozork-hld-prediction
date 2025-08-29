#!/usr/bin/env python3
"""
Complete workflow test for Docker environment.
This script tests the full interactive system workflow.
"""

import sys
import os
import pandas as pd
from colorama import Fore, Style

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_complete_workflow():
    """Test the complete workflow from data loading to fixing."""
    print("🚀 Testing Complete Workflow...")
    
    try:
        from src.interactive import InteractiveSystem
        
        # Initialize system
        system = InteractiveSystem()
        
        # Load test data
        data_path = 'data/sample_ohlcv_with_issues.csv'
        if not os.path.exists(data_path):
            print(f"❌ Test data not found: {data_path}")
            return False
            
        system.current_data = pd.read_csv(data_path)
        print(f"✅ Data loaded, shape: {system.current_data.shape}")
        
        # Run comprehensive data quality check
        print("\n🔍 Running comprehensive data quality check...")
        
        try:
            # Call the method directly
            system.analysis_runner.run_comprehensive_data_quality_check(system)
            print("✅ Comprehensive data quality check completed!")
            return True
        except Exception as e:
            print(f"❌ Error in comprehensive data quality check: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Error in complete workflow: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_interactive_system_direct():
    """Test interactive system with direct method calls."""
    print("🚀 Testing Interactive System Direct Method Calls...")
    
    try:
        from src.interactive import InteractiveSystem
        
        # Initialize system
        system = InteractiveSystem()
        
        # Load test data
        data_path = 'data/sample_ohlcv_with_issues.csv'
        if not os.path.exists(data_path):
            print(f"❌ Test data not found: {data_path}")
            return False
            
        system.current_data = pd.read_csv(data_path)
        print(f"✅ Data loaded, shape: {system.current_data.shape}")
        
        # Run comprehensive data quality check using the core method
        print("\n🔍 Running comprehensive data quality check via core...")
        
        try:
            system.run_comprehensive_data_quality_check()
            print("✅ Comprehensive data quality check completed via core!")
            return True
        except Exception as e:
            print(f"❌ Error in comprehensive data quality check via core: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Error in direct method calls: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Complete Workflow Tests...")
    
    # Test 1: Complete workflow
    print("\n" + "="*50)
    print("TEST 1: Complete Workflow")
    print("="*50)
    success1 = test_complete_workflow()
    
    # Test 2: Direct method calls
    print("\n" + "="*50)
    print("TEST 2: Direct Method Calls")
    print("="*50)
    success2 = test_interactive_system_direct()
    
    if success1 and success2:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
