#!/usr/bin/env python3
"""
Test script to diagnose the Docker fix issue.
This script simulates the interactive system behavior in Docker.
"""

import sys
import os
import pandas as pd
import numpy as np
from colorama import Fore, Style

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_comprehensive_data_quality_check():
    """Test the comprehensive data quality check functionality."""
    print("🔍 Testing Comprehensive Data Quality Check...")
    
    try:
        # Import required modules
        from src.batch_eda import data_quality, fix_files
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
        
        # Initialize summary lists
        nan_summary = []
        dupe_summary = []
        gap_summary = []
        zero_summary = []
        negative_summary = []
        inf_summary = []
        
        # Run data quality checks
        print("\n🔍 Running data quality checks...")
        
        try:
            data_quality.nan_check(system.current_data, nan_summary, Fore, Style)
            print(f"✅ NaN check completed, found {len(nan_summary)} issues")
        except Exception as e:
            print(f"❌ Error in NaN check: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        try:
            data_quality.duplicate_check(system.current_data, dupe_summary, Fore, Style)
            print(f"✅ Duplicate check completed, found {len(dupe_summary)} issues")
        except Exception as e:
            print(f"❌ Error in duplicate check: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        try:
            data_quality.gap_check(system.current_data, gap_summary, Fore, Style)
            print(f"✅ Gap check completed, found {len(gap_summary)} issues")
        except Exception as e:
            print(f"❌ Error in gap check: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        try:
            data_quality.zero_check(system.current_data, zero_summary, Fore, Style)
            print(f"✅ Zero check completed, found {len(zero_summary)} issues")
        except Exception as e:
            print(f"❌ Error in zero check: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        try:
            data_quality.negative_check(system.current_data, negative_summary, Fore, Style)
            print(f"✅ Negative check completed, found {len(negative_summary)} issues")
        except Exception as e:
            print(f"❌ Error in negative check: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        try:
            data_quality.inf_check(system.current_data, inf_summary, Fore, Style)
            print(f"✅ Infinity check completed, found {len(inf_summary)} issues")
        except Exception as e:
            print(f"❌ Error in infinity check: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Calculate total issues
        total_issues = len(nan_summary) + len(dupe_summary) + len(gap_summary) + len(zero_summary) + len(negative_summary) + len(inf_summary)
        
        print(f"\n📊 QUALITY CHECK SUMMARY:")
        print(f"   • NaN issues: {len(nan_summary)}")
        print(f"   • Duplicate issues: {len(dupe_summary)}")
        print(f"   • Gap issues: {len(gap_summary)}")
        print(f"   • Zero value issues: {len(zero_summary)}")
        print(f"   • Negative value issues: {len(negative_summary)}")
        print(f"   • Infinity issues: {len(inf_summary)}")
        print(f"   • Total issues found: {total_issues}")
        
        if total_issues > 0:
            print(f"\n🔧 ISSUES DETECTED - TESTING FIXES...")
            print("-" * 50)
            
            # Create backup before fixing
            backup_data = system.current_data.copy()
            print(f"✅ Backup created, original shape: {backup_data.shape}")
            
            # Test fixing all issues
            try:
                # Fix NaN values
                if nan_summary:
                    print("   • Testing NaN fixing...")
                    fixed_data = fix_files.fix_nan(system.current_data, nan_summary)
                    if fixed_data is not None:
                        system.current_data = fixed_data
                        print(f"   ✅ NaN values fixed. Data shape: {system.current_data.shape}")
                    else:
                        print("   ⚠️  NaN fixing returned None")
                
                # Fix duplicate rows
                if dupe_summary:
                    print("   • Testing duplicate fixing...")
                    fixed_data = fix_files.fix_duplicates(system.current_data, dupe_summary)
                    if fixed_data is not None:
                        system.current_data = fixed_data
                        print(f"   ✅ Duplicate rows fixed. Data shape: {system.current_data.shape}")
                    else:
                        print("   ⚠️  Duplicate fixing returned None")
                
                # Fix gaps
                if gap_summary:
                    print("   • Testing gap fixing...")
                    # Find datetime column
                    datetime_col = None
                    for col in system.current_data.columns:
                        if pd.api.types.is_datetime64_any_dtype(system.current_data[col]):
                            datetime_col = col
                            break
                    fixed_data = fix_files.fix_gaps(system.current_data, gap_summary, datetime_col)
                    if fixed_data is not None:
                        system.current_data = fixed_data
                        print(f"   ✅ Gaps fixed. Data shape: {system.current_data.shape}")
                    else:
                        print("   ⚠️  Gap fixing returned None")
                
                # Fix zero values
                if zero_summary:
                    print("   • Testing zero fixing...")
                    fixed_data = fix_files.fix_zeros(system.current_data, zero_summary)
                    if fixed_data is not None:
                        system.current_data = fixed_data
                        print(f"   ✅ Zero values fixed. Data shape: {system.current_data.shape}")
                    else:
                        print("   ⚠️  Zero fixing returned None")
                
                # Fix negative values
                if negative_summary:
                    print("   • Testing negative fixing...")
                    fixed_data = fix_files.fix_negatives(system.current_data, negative_summary)
                    if fixed_data is not None:
                        system.current_data = fixed_data
                        print(f"   ✅ Negative values fixed. Data shape: {system.current_data.shape}")
                    else:
                        print("   ⚠️  Negative fixing returned None")
                
                # Fix infinity values
                if inf_summary:
                    print("   • Testing infinity fixing...")
                    fixed_data = fix_files.fix_infs(system.current_data, inf_summary)
                    if fixed_data is not None:
                        system.current_data = fixed_data
                        print(f"   ✅ Infinity values fixed. Data shape: {system.current_data.shape}")
                    else:
                        print("   ⚠️  Infinity fixing returned None")
                
                print("\n✅ All fixes completed successfully!")
                print(f"   • Original data shape: {backup_data.shape}")
                print(f"   • Fixed data shape: {system.current_data.shape}")
                
                return True
                
            except Exception as e:
                print(f"❌ Error during fixing: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print("\n✅ No issues found, no fixes needed!")
            return True
            
    except Exception as e:
        print(f"❌ Error in comprehensive data quality check: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Docker Fix Issue Test...")
    success = test_comprehensive_data_quality_check()
    
    if success:
        print("\n✅ Test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)
