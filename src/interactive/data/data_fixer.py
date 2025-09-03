# -*- coding: utf-8 -*-
# src/interactive/data_fixer.py
#!/usr/bin/env python3
"""
Data fixing and issue resolution utilities.
Handles fixing missing values, duplicates, and other data quality issues.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import gc


class DataFixer:
    """Handles fixing of data quality issues."""
    
    def __init__(self):
        """Initialize DataFixer."""
        pass
    
    def fix_data_issues(self, system, nan_summary: List[Dict], 
                        dupe_summary: Dict, gap_summary: List[Dict]) -> bool:
        """
        Fix data quality issues interactively.
        
        Args:
            system: InteractiveSystem instance
            nan_summary: Missing values summary
            dupe_summary: Duplicates summary
            gap_summary: Time series gaps summary
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔧 DATA ISSUE RESOLUTION")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        # Create backup
        backup_data = system.current_data.copy()
        backup_created = True
        print(f"💾 Backup created with {backup_data.shape[0]:,} rows")
        
        # Collect all available fixes
        available_fixes = []
        fixes_applied = []
        
        # Missing values fixes
        if nan_summary:
            for item in nan_summary:
                available_fixes.append({
                    'type': 'missing_values',
                    'column': item['column'],
                    'description': f"Fix {item['missing_count']:,} missing values in {item['column']}",
                    'priority': 'high' if item['missing_percent'] > 10 else 'medium'
                })
        
        # Duplicate fixes
        if dupe_summary.get('total_duplicates', 0) > 0:
            available_fixes.append({
                'type': 'duplicates',
                'column': 'all',
                'description': f"Remove {dupe_summary['total_duplicates']:,} duplicate rows",
                'priority': 'high'
            })
        
        # Time series gap fixes
        if gap_summary:
            for item in gap_summary:
                available_fixes.append({
                    'type': 'time_series_gaps',
                    'column': item['column'],
                    'description': f"Fix {item['gap_count']:,} gaps in {item['column']}",
                    'priority': 'medium'
                })
        
        if not available_fixes:
            print("✅ No data issues found to fix!")
            return True
        
        # Show available fixes
        print(f"📋 Found {len(available_fixes)} issues to fix:")
        for i, fix in enumerate(available_fixes, 1):
            priority_icon = "🔴" if fix['priority'] == 'high' else "🟡" if fix['priority'] == 'medium' else "🟢"
            print(f"   {i}. {priority_icon} {fix['description']}")
        
        # Ask user how to proceed
        print(f"\n💡 How would you like to proceed?")
        print(f"   1. Fix individual issues")
        print(f"   2. Apply all fixes automatically")
        print(f"   3. Skip fixing")
        
        try:
            choice = input("\nSelect option (1-3, default: 3): ").strip()
            if choice == '1':
                return self._show_individual_fix_menu(
                    system, nan_summary, dupe_summary, gap_summary, 
                    available_fixes, fixes_applied, backup_data, backup_created
                )
            elif choice == '2':
                return self._apply_all_remaining_fixes(
                    system, available_fixes, fixes_applied, backup_data, backup_created
                )
            else:
                print("⏭️  Skipping data fixing...")
                return True
                
        except EOFError:
            print("\n👋 Goodbye!")
            return False
    
    def _show_individual_fix_menu(self, system, nan_summary: List[Dict], 
                                 dupe_summary: Dict, gap_summary: List[Dict],
                                 available_fixes: List[Dict], fixes_applied: List[Dict],
                                 backup_data: pd.DataFrame, backup_created: bool) -> bool:
        """
        Show individual fix selection menu.
        
        Args:
            system: InteractiveSystem instance
            nan_summary: Missing values summary
            dupe_summary: Duplicates summary
            gap_summary: Time series gaps summary
            available_fixes: List of available fixes
            fixes_applied: List of applied fixes
            backup_data: Backup of original data
            backup_created: Whether backup was created
            
        Returns:
            bool: True if successful
        """
        while available_fixes:
            print(f"\n🔧 INDIVIDUAL FIX SELECTION")
            print("-" * 40)
            print(f"📋 Available fixes: {len(available_fixes)}")
            print(f"✅ Applied fixes: {len(fixes_applied)}")
            
            # Show available fixes
            for i, fix in enumerate(available_fixes, 1):
                priority_icon = "🔴" if fix['priority'] == 'high' else "🟡" if fix['priority'] == 'medium' else "🟢"
                print(f"   {i}. {priority_icon} {fix['description']}")
            
            print(f"   0. Apply all remaining fixes")
            print(f"   -1. Show fix status")
            print(f"   -2. Undo last fix")
            print(f"   -3. Finish fixing")
            
            try:
                choice = input("\nSelect fix to apply (number): ").strip()
                
                if choice == '0':
                    return self._apply_all_remaining_fixes(
                        system, available_fixes, fixes_applied, backup_data, backup_created
                    )
                elif choice == '-1':
                    self._show_fix_status(available_fixes, fixes_applied)
                    continue
                elif choice == '-2':
                    if fixes_applied:
                        self._undo_last_fix(system, fixes_applied, backup_data)
                    else:
                        print("❌ No fixes to undo")
                    continue
                elif choice == '-3':
                    print("✅ Finishing data fixing...")
                    break
                elif not choice.isdigit():
                    print("❌ Invalid choice")
                    continue
                
                fix_idx = int(choice) - 1
                if 0 <= fix_idx < len(available_fixes):
                    selected_fix = available_fixes[fix_idx]
                    success = self._apply_single_fix(
                        system, selected_fix, nan_summary, dupe_summary, gap_summary,
                        fixes_applied, backup_data, backup_created
                    )
                    
                    if success:
                        # Remove applied fix from available list
                        available_fixes.pop(fix_idx)
                    else:
                        print("❌ Fix failed, keeping in available list")
                else:
                    print("❌ Invalid fix number")
                    
            except EOFError:
                print("\n👋 Goodbye!")
                return False
        
        return True
    
    def _apply_single_fix(self, system, fix: Dict, nan_summary: List[Dict],
                          dupe_summary: Dict, gap_summary: List[Dict],
                          fixes_applied: List[Dict], backup_data: pd.DataFrame,
                          backup_created: bool) -> bool:
        """
        Apply a single fix to the data.
        
        Args:
            system: InteractiveSystem instance
            fix: Fix to apply
            nan_summary: Missing values summary
            dupe_summary: Duplicates summary
            gap_summary: Time series gaps summary
            fixes_applied: List of applied fixes
            backup_data: Backup of original data
            backup_created: Whether backup was created
            
        Returns:
            bool: True if fix was successful
        """
        print(f"\n🔧 Applying fix: {fix['description']}")
        
        try:
            if fix['type'] == 'missing_values':
                success = self._fix_missing_values(system, fix['column'], nan_summary)
            elif fix['type'] == 'duplicates':
                success = self._fix_duplicates(system, dupe_summary)
            elif fix['type'] == 'time_series_gaps':
                success = self._fix_time_series_gaps(system, fix['column'], gap_summary)
            else:
                print(f"❌ Unknown fix type: {fix['type']}")
                return False
            
            if success:
                # Record applied fix
                fixes_applied.append({
                    'type': fix['type'],
                    'column': fix['column'],
                    'description': fix['description'],
                    'timestamp': pd.Timestamp.now()
                })
                print(f"✅ Fix applied successfully!")
                return True
            else:
                print(f"❌ Fix failed!")
                return False
                
        except Exception as e:
            print(f"❌ Error applying fix: {e}")
            return False
    
    def _fix_missing_values(self, system, column: str, nan_summary: List[Dict]) -> bool:
        """Fix missing values in a column."""
        try:
            df = system.current_data
            
            # Find the column info
            col_info = next((item for item in nan_summary if item['column'] == column), None)
            if not col_info:
                print(f"❌ Column {column} not found in missing values summary")
                return False
            
            missing_count = col_info['missing_count']
            data_type = col_info['data_type']
            
            print(f"   📊 Fixing {missing_count:,} missing values in {column}")
            print(f"   🔍 Data type: {data_type}")
            
            # Ask user for strategy
            print(f"\n💡 Select strategy for fixing missing values:")
            print(f"   1. Forward fill (ffill)")
            print(f"   2. Backward fill (bfill)")
            print(f"   3. Interpolate (linear)")
            print(f"   4. Fill with mean (numeric only)")
            print(f"   5. Fill with median (numeric only)")
            print(f"   6. Fill with mode (categorical only)")
            print(f"   7. Drop rows with missing values")
            
            try:
                strategy_choice = input("\nSelect strategy (1-7, default: 1): ").strip()
                if not strategy_choice:
                    strategy_choice = '1'
            except EOFError:
                strategy_choice = '1'
            
            # Apply strategy
            if strategy_choice == '1':
                df[column] = df[column].fillna(method='ffill')
                print(f"   ✅ Applied forward fill")
            elif strategy_choice == '2':
                df[column] = df[column].fillna(method='bfill')
                print(f"   ✅ Applied backward fill")
            elif strategy_choice == '3':
                df[column] = df[column].interpolate(method='linear')
                print(f"   ✅ Applied linear interpolation")
            elif strategy_choice == '4' and 'float' in data_type or 'int' in data_type:
                mean_val = df[column].mean()
                df[column] = df[column].fillna(mean_val)
                print(f"   ✅ Filled with mean: {mean_val:.4f}")
            elif strategy_choice == '5' and 'float' in data_type or 'int' in data_type:
                median_val = df[column].median()
                df[column] = df[column].fillna(median_val)
                print(f"   ✅ Filled with median: {median_val:.4f}")
            elif strategy_choice == '6' and 'object' in data_type:
                mode_val = df[column].mode().iloc[0] if len(df[column].mode()) > 0 else 'Unknown'
                df[column] = df[column].fillna(mode_val)
                print(f"   ✅ Filled with mode: {mode_val}")
            elif strategy_choice == '7':
                original_count = len(df)
                df = df.dropna(subset=[column])
                dropped_count = original_count - len(df)
                system.current_data = df
                print(f"   ✅ Dropped {dropped_count:,} rows with missing values")
            else:
                print(f"❌ Invalid strategy or strategy not applicable to data type")
                return False
            
            # Verify fix
            remaining_missing = df[column].isnull().sum()
            print(f"   📊 Remaining missing values: {remaining_missing:,}")
            
            return remaining_missing == 0
            
        except Exception as e:
            print(f"❌ Error fixing missing values: {e}")
            return False
    
    def _fix_duplicates(self, system, dupe_summary: Dict) -> bool:
        """Fix duplicate rows."""
        try:
            df = system.current_data
            original_count = len(df)
            
            print(f"   🔄 Removing {dupe_summary['total_duplicates']:,} duplicate rows")
            
            # Remove duplicates
            df = df.drop_duplicates()
            new_count = len(df)
            removed_count = original_count - new_count
            
            # Update system data
            system.current_data = df
            
            print(f"   ✅ Removed {removed_count:,} duplicate rows")
            print(f"   📊 New row count: {new_count:,}")
            
            return removed_count > 0
            
        except Exception as e:
            print(f"❌ Error fixing duplicates: {e}")
            return False
    
    def _fix_time_series_gaps(self, system, column: str, gap_summary: List[Dict]) -> bool:
        """Fix time series gaps in a column."""
        try:
            df = system.current_data
            
            # Find the column info
            col_info = next((item for item in gap_summary if item['column'] == column), None)
            if not col_info:
                print(f"❌ Column {column} not found in gap summary")
                return False
            
            gap_count = col_info['gap_count']
            expected_freq = col_info['expected_frequency']
            
            print(f"   ⏱️  Fixing {gap_count:,} gaps in {column}")
            print(f"   🔄 Expected frequency: {expected_freq}")
            
            # Initialize GapFixer
            try:
                from ..data import GapFixer
                gap_fixer = GapFixer(memory_limit_mb=6144)
                print("   ✅ GapFixer initialized")
            except Exception as e:
                print(f"   ❌ Error initializing GapFixer: {e}")
                return False
            
            # Detect gaps
            gap_info = gap_fixer.utils.detect_gaps(df, column)
            
            if not gap_info['has_gaps']:
                print(f"   ✅ No gaps detected in {column}")
                return True
            
            # Fix gaps with auto algorithm
            print(f"   🔧 Fixing gaps with auto algorithm...")
            fixed_df = gap_fixer.algorithms.apply_algorithm(
                df, 'auto', gap_info
            )
            
            if fixed_df is not None:
                # Update system data
                system.current_data = fixed_df
                
                print(f"   ✅ Gaps fixed successfully!")
                print(f"      • Algorithm used: auto")
                print(f"      • Gaps fixed: {gap_info['gap_count']:,}")
                print(f"      • Processing completed successfully")
                
                return True
            else:
                print(f"   ❌ Gap fixing failed")
                return False
                
        except Exception as e:
            print(f"❌ Error fixing time series gaps: {e}")
            return False
    
    def _show_fix_status(self, available_fixes: List[Dict], fixes_applied: List[Dict]):
        """Show status of available and applied fixes."""
        print(f"\n📊 FIX STATUS")
        print("-" * 30)
        print(f"📋 Available fixes: {len(available_fixes)}")
        for fix in available_fixes:
            priority_icon = "🔴" if fix['priority'] == 'high' else "🟡" if fix['priority'] == 'medium' else "🟢"
            print(f"   • {priority_icon} {fix['description']}")
        
        print(f"\n✅ Applied fixes: {len(fixes_applied)}")
        for fix in fixes_applied:
            print(f"   • {fix['type']}: {fix['description']}")
            print(f"     Applied at: {fix['timestamp']}")
    
    def _undo_last_fix(self, system, fixes_applied: List[Dict], backup_data: pd.DataFrame):
        """Undo the last applied fix."""
        if not fixes_applied:
            print("❌ No fixes to undo")
            return
        
        last_fix = fixes_applied.pop()
        print(f"🔄 Undoing last fix: {last_fix['description']}")
        
        # For now, restore from backup (simple approach)
        # In a more sophisticated implementation, you could implement incremental undo
        system.current_data = backup_data.copy()
        print(f"✅ Restored data from backup")
    
    def _apply_all_remaining_fixes(self, system, available_fixes: List[Dict],
                                  fixes_applied: List[Dict], backup_data: pd.DataFrame,
                                  backup_created: bool) -> bool:
        """
        Apply all remaining fixes automatically.
        
        Args:
            system: InteractiveSystem instance
            available_fixes: List of available fixes
            fixes_applied: List of applied fixes
            backup_data: Backup of original data
            backup_created: Whether backup was created
            
        Returns:
            bool: True if successful
        """
        if not available_fixes:
            print("✅ No fixes remaining to apply")
            return True
        
        print(f"\n🚀 APPLYING ALL REMAINING FIXES")
        print("-" * 40)
        print(f"📋 Will apply {len(available_fixes)} fixes automatically")
        
        # Confirm with user
        try:
            confirm = input("\nApply all remaining fixes? (y/n, default: y): ").strip().lower()
            if confirm not in ['', 'y', 'yes']:
                print("⏭️  Automatic fixing cancelled")
                return False
        except EOFError:
            print("⏭️  Automatic fixing cancelled")
            return False
        
        # Apply fixes
        successful_fixes = 0
        failed_fixes = 0
        
        for fix in available_fixes:
            print(f"\n🔧 Applying: {fix['description']}")
            
            try:
                # Create dummy summaries for the fix
                dummy_nan = [{'column': fix['column']}] if fix['type'] == 'missing_values' else []
                dummy_dupe = {'total_duplicates': 0} if fix['type'] == 'duplicates' else {}
                dummy_gap = [{'column': fix['column']}] if fix['type'] == 'time_series_gaps' else []
                
                success = self._apply_single_fix(
                    system, fix, dummy_nan, dummy_dupe, dummy_gap,
                    fixes_applied, backup_data, backup_created
                )
                
                if success:
                    successful_fixes += 1
                    print(f"   ✅ Fix successful")
                else:
                    failed_fixes += 1
                    print(f"   ❌ Fix failed")
                    
            except Exception as e:
                failed_fixes += 1
                print(f"   ❌ Error: {e}")
        
        # Summary
        print(f"\n📊 AUTOMATIC FIXING COMPLETED")
        print("-" * 40)
        print(f"✅ Successful fixes: {successful_fixes}")
        print(f"❌ Failed fixes: {failed_fixes}")
        print(f"📋 Total fixes: {len(available_fixes)}")
        
        return failed_fixes == 0
