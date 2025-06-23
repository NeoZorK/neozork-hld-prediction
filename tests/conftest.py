# Automatically add project root to Python path for tests
import sys
import os
import pytest
from pathlib import Path

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def pytest_sessionfinish(session, exitstatus):
    """Run test coverage analysis after all tests complete"""
    print("\n" + "="*60)
    print("🔍 RUNNING TEST COVERAGE ANALYSIS")
    print("="*60)
    
    # Import and run the coverage analysis
    try:
        from tests.summary.zzz_analyze_test_coverage import analyze_coverage
        missing_tests = analyze_coverage()
        
        # Exit with error code if there are missing tests
        if missing_tests:
            print(f"\n⚠️  Found {len(missing_tests)} files without tests!")
            print("Consider adding tests for uncovered files.")
        else:
            print("\n✅ All source files have corresponding tests!")
            
    except Exception as e:
        print(f"❌ Error running coverage analysis: {e}")
        import traceback
        traceback.print_exc() 