"""
Reporting Module

This module provides comprehensive reporting functionality for data cleaning operations.
It generates detailed reports showing what was found, what was fixed, and statistics
about the cleaning process.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
import os


class CleaningReporter:
    """Generates detailed reports for data cleaning operations."""
    
    def __init__(self):
        """Initialize the cleaning reporter."""
        self.report_data = {}
    
    def show_detailed_results(self, procedure_name: str, issues: List[Dict[str, Any]], data: pd.DataFrame) -> None:
        """
        Show detailed results for a specific cleaning procedure.
        
        Args:
            procedure_name: Name of the cleaning procedure
            issues: List of detected issues
            data: Original DataFrame
        """
        print(f"\n{'='*60}")
        print(f"DETAILED RESULTS: {procedure_name.upper()}")
        print(f"{'='*60}")
        
        if not issues:
            print("✅ No issues found!")
            return
        
        if procedure_name.lower() == 'gaps':
            self._show_gaps_details(issues)
        elif procedure_name.lower() == 'duplicates':
            self._show_duplicates_details(issues)
        elif procedure_name.lower() == 'nan':
            self._show_nan_details(issues)
        elif procedure_name.lower() == 'zeros':
            self._show_zeros_details(issues)
        elif procedure_name.lower() == 'negative':
            self._show_negative_details(issues)
        elif procedure_name.lower() == 'infinity':
            self._show_infinity_details(issues)
        elif procedure_name.lower() == 'outliers':
            self._show_outliers_details(issues)
        
        # Show warnings if applicable
        if procedure_name.lower() in ['zeros', 'negative']:
            self._show_warnings(issues)
    
    def _show_gaps_details(self, gaps: List[Dict[str, Any]]) -> None:
        """Show detailed gap information."""
        print(f"Found {len(gaps)} time series gaps:")
        print()
        
        for i, gap in enumerate(gaps[:5]):  # Show first 5 gaps
            print(f"Gap {i+1}:")
            print(f"  Column: {gap['column']}")
            print(f"  Start: {gap['gap_start']}")
            print(f"  End: {gap['gap_end']}")
            print(f"  Duration: {gap['gap_duration']}")
            print(f"  Expected: {gap['expected_duration']}")
            print(f"  Size: {gap['gap_size']:.1f}x expected")
            print()
        
        if len(gaps) > 5:
            print(f"... and {len(gaps) - 5} more gaps")
    
    def _show_duplicates_details(self, duplicates: List[Dict[str, Any]]) -> None:
        """Show detailed duplicate information."""
        total_duplicates = sum(dup['count'] for dup in duplicates)
        print(f"Found {len(duplicates)} duplicate groups ({total_duplicates} total duplicate rows):")
        print()
        
        for i, dup in enumerate(duplicates[:3]):  # Show first 3 groups
            print(f"Group {i+1}:")
            print(f"  Count: {dup['count']} rows")
            print(f"  Indices: {dup['indices'][:5]}{'...' if len(dup['indices']) > 5 else ''}")
            print(f"  Sample data: {list(dup['sample_data'].items())[:3]}")
            print()
        
        if len(duplicates) > 3:
            print(f"... and {len(duplicates) - 3} more duplicate groups")
    
    def _show_nan_details(self, nan_issues: List[Dict[str, Any]]) -> None:
        """Show detailed NaN information."""
        total_nans = sum(issue['count'] for issue in nan_issues)
        print(f"Found NaN values in {len(nan_issues)} columns ({total_nans} total NaN values):")
        print()
        
        for issue in nan_issues:
            print(f"Column '{issue['column']}':")
            print(f"  Count: {issue['count']:,} ({issue['percentage']:.1f}%)")
            print(f"  Indices: {issue['indices'][:5]}{'...' if len(issue['indices']) > 5 else ''}")
            print()
    
    def _show_zeros_details(self, zero_issues: List[Dict[str, Any]]) -> None:
        """Show detailed zero values information."""
        total_zeros = sum(issue['count'] for issue in zero_issues)
        print(f"Found zero values in {len(zero_issues)} columns ({total_zeros} total zero values):")
        print()
        
        for issue in zero_issues:
            print(f"Column '{issue['column']}':")
            print(f"  Count: {issue['count']:,} ({issue['percentage']:.1f}%)")
            print(f"  Indices: {issue['indices'][:5]}{'...' if len(issue['indices']) > 5 else ''}")
            print()
    
    def _show_negative_details(self, negative_issues: List[Dict[str, Any]]) -> None:
        """Show detailed negative values information."""
        total_negative = sum(issue['count'] for issue in negative_issues)
        print(f"Found negative values in {len(negative_issues)} columns ({total_negative} total negative values):")
        print()
        
        for issue in negative_issues:
            print(f"Column '{issue['column']}':")
            print(f"  Count: {issue['count']:,} ({issue['percentage']:.1f}%)")
            print(f"  Indices: {issue['indices'][:5]}{'...' if len(issue['indices']) > 5 else ''}")
            print()
    
    def _show_infinity_details(self, infinity_issues: List[Dict[str, Any]]) -> None:
        """Show detailed infinity values information."""
        total_infinity = sum(issue['count'] for issue in infinity_issues)
        print(f"Found infinity values in {len(infinity_issues)} columns ({total_infinity} total infinity values):")
        print()
        
        for issue in infinity_issues:
            print(f"Column '{issue['column']}':")
            print(f"  Count: {issue['count']:,} ({issue['percentage']:.1f}%)")
            print(f"  Indices: {issue['indices'][:5]}{'...' if len(issue['indices']) > 5 else ''}")
            print()
    
    def _show_outliers_details(self, outliers: List[Dict[str, Any]]) -> None:
        """Show detailed outliers information."""
        print(f"Found outliers in {len(outliers)} columns:")
        print()
        
        for outlier_info in outliers:
            print(f"Column '{outlier_info['column']}':")
            for method, results in outlier_info['methods'].items():
                if results['count'] > 0:
                    print(f"  {method}: {results['count']} outliers")
                    print(f"    Indices: {results['indices'][:5]}{'...' if len(results['indices']) > 5 else ''}")
            print()
    
    def _show_warnings(self, issues: List[Dict[str, Any]]) -> None:
        """Show warnings for zero and negative values."""
        print("⚠️  WARNING:")
        for issue in issues:
            if 'warning' in issue:
                print(f"  {issue['warning']}")
        print()
    
    def show_final_report(self, file_info: Dict[str, Any], cleaning_results: Dict[str, Any]) -> None:
        """
        Show comprehensive final report of the cleaning process.
        
        Args:
            file_info: Original file metadata
            cleaning_results: Results from all cleaning procedures
        """
        print("\n" + "="*80)
        print("FINAL CLEANING REPORT")
        print("="*80)
        
        # File information
        print(f"File: {file_info['filename']}")
        print(f"Format: {file_info['format'].upper()}")
        print(f"Source: {file_info.get('source', 'Unknown')}")
        print(f"Symbol: {file_info.get('symbol', 'Unknown')}")
        print(f"Time Frame: {file_info.get('timeframe', 'Unknown')}")
        if file_info.get('indicator'):
            print(f"Indicator: {file_info['indicator']}")
        
        print("\n" + "-"*80)
        print("DATA STATISTICS")
        print("-"*80)
        
        original_data = cleaning_results['original_data']
        cleaned_data = cleaning_results['cleaned_data']
        
        print(f"Original rows: {len(original_data):,}")
        print(f"Cleaned rows: {len(cleaned_data):,}")
        print(f"Rows removed: {len(original_data) - len(cleaned_data):,}")
        
        print(f"Original columns: {len(original_data.columns)}")
        print(f"Cleaned columns: {len(cleaned_data.columns)}")
        
        # File size information
        original_size = original_data.memory_usage(deep=True).sum()
        cleaned_size = cleaned_data.memory_usage(deep=True).sum()
        size_reduction = ((original_size - cleaned_size) / original_size) * 100 if original_size > 0 else 0
        
        print(f"Original memory usage: {original_size:,} bytes")
        print(f"Cleaned memory usage: {cleaned_size:,} bytes")
        print(f"Memory reduction: {size_reduction:.1f}%")
        
        print("\n" + "-"*80)
        print("CLEANING PROCEDURES SUMMARY")
        print("-"*80)
        
        procedures = [
            ("Time Series Gaps", "gaps"),
            ("Duplicates", "duplicates"),
            ("NaN Values", "nan"),
            ("Zero Values", "zeros"),
            ("Negative Values", "negative"),
            ("Infinity Values", "infinity"),
            ("Outliers", "outliers")
        ]
        
        total_issues_found = 0
        total_issues_fixed = 0
        
        for proc_name, proc_id in procedures:
            if proc_id in cleaning_results['procedures']:
                proc_data = cleaning_results['procedures'][proc_id]
                issues_found = proc_data['issues_found']
                issues_fixed = proc_data['issues_fixed']
                status = proc_data['status']
                
                total_issues_found += issues_found
                total_issues_fixed += issues_fixed
                
                status_icon = {
                    'clean': '✅',
                    'fixed': '🔧',
                    'skipped': '⏭️',
                    'failed': '❌'
                }.get(status, '❓')
                
                print(f"{status_icon} {proc_name}:")
                print(f"    Found: {issues_found:,}")
                print(f"    Fixed: {issues_fixed:,}")
                print(f"    Status: {status.upper()}")
                print()
        
        print("-"*80)
        print("OVERALL SUMMARY")
        print("-"*80)
        print(f"Total issues found: {total_issues_found:,}")
        print(f"Total issues fixed: {total_issues_fixed:,}")
        print(f"Fix rate: {(total_issues_fixed/total_issues_found*100):.1f}%" if total_issues_found > 0 else "Fix rate: N/A")
        
        # Detailed breakdown by procedure
        print("\n📊 DETAILED BREAKDOWN:")
        for proc_name, proc_id in procedures:
            if proc_id in cleaning_results['procedures']:
                proc_data = cleaning_results['procedures'][proc_id]
                issues_found = proc_data['issues_found']
                issues_fixed = proc_data['issues_fixed']
                status = proc_data['status']
                
                if issues_found > 0:
                    status_icon = {
                        'clean': '✅',
                        'fixed': '🔧',
                        'skipped': '⏭️',
                        'failed': '❌'
                    }.get(status, '❓')
                    
                    print(f"  {status_icon} {proc_name}: {issues_found:,} found → {issues_fixed:,} fixed")
        
        # Data quality improvement
        original_nulls = original_data.isnull().sum().sum()
        cleaned_nulls = cleaned_data.isnull().sum().sum()
        null_reduction = ((original_nulls - cleaned_nulls) / original_nulls) * 100 if original_nulls > 0 else 0
        
        print(f"\n📈 DATA QUALITY IMPROVEMENT:")
        print(f"  Original null values: {original_nulls:,}")
        print(f"  Cleaned null values: {cleaned_nulls:,}")
        print(f"  Null reduction: {null_reduction:.1f}%")
        
        # Additional statistics
        print(f"\n📋 ADDITIONAL STATISTICS:")
        print(f"  Rows processed: {len(original_data):,}")
        print(f"  Columns processed: {len(original_data.columns)}")
        print(f"  Memory usage: {original_size:,} → {cleaned_size:,} bytes")
        print(f"  Memory reduction: {size_reduction:.1f}%")
        
        print("="*80)
    
    def save_report(self, file_info: Dict[str, Any], cleaning_results: Dict[str, Any], 
                   output_path: str) -> None:
        """
        Save detailed report to file.
        
        Args:
            file_info: Original file metadata
            cleaning_results: Results from all cleaning procedures
            output_path: Path to save the report
        """
        report_lines = []
        
        # Header
        report_lines.append("DATA CLEANING REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"File: {file_info['filename']}")
        report_lines.append("")
        
        # File information
        report_lines.append("FILE INFORMATION")
        report_lines.append("-" * 30)
        for key, value in file_info.items():
            if key not in ['file_path']:
                report_lines.append(f"{key}: {value}")
        report_lines.append("")
        
        # Cleaning summary
        report_lines.append("CLEANING SUMMARY")
        report_lines.append("-" * 30)
        
        original_data = cleaning_results['original_data']
        cleaned_data = cleaning_results['cleaned_data']
        
        report_lines.append(f"Original rows: {len(original_data):,}")
        report_lines.append(f"Cleaned rows: {len(cleaned_data):,}")
        report_lines.append(f"Rows removed: {len(original_data) - len(cleaned_data):,}")
        report_lines.append("")
        
        # Procedures details
        report_lines.append("PROCEDURES DETAILS")
        report_lines.append("-" * 30)
        
        for proc_id, proc_data in cleaning_results['procedures'].items():
            report_lines.append(f"{proc_id.upper()}:")
            report_lines.append(f"  Found: {proc_data['issues_found']:,}")
            report_lines.append(f"  Fixed: {proc_data['issues_fixed']:,}")
            report_lines.append(f"  Status: {proc_data['status'].upper()}")
            report_lines.append("")
        
        # Save to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
    
    def generate_summary_stats(self, cleaning_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary statistics for the cleaning process.
        
        Args:
            cleaning_results: Results from all cleaning procedures
            
        Returns:
            Dictionary with summary statistics
        """
        original_data = cleaning_results['original_data']
        cleaned_data = cleaning_results['cleaned_data']
        
        stats = {
            'original_rows': len(original_data),
            'cleaned_rows': len(cleaned_data),
            'rows_removed': len(original_data) - len(cleaned_data),
            'original_columns': len(original_data.columns),
            'cleaned_columns': len(cleaned_data.columns),
            'original_memory': original_data.memory_usage(deep=True).sum(),
            'cleaned_memory': cleaned_data.memory_usage(deep=True).sum(),
            'total_issues_found': cleaning_results['total_issues_found'],
            'total_issues_fixed': cleaning_results['total_issues_fixed'],
            'procedures_completed': len(cleaning_results['procedures']),
            'procedures_fixed': sum(1 for p in cleaning_results['procedures'].values() if p['status'] == 'fixed'),
            'procedures_skipped': sum(1 for p in cleaning_results['procedures'].values() if p['status'] == 'skipped'),
            'procedures_clean': sum(1 for p in cleaning_results['procedures'].values() if p['status'] == 'clean')
        }
        
        # Calculate percentages
        if stats['original_rows'] > 0:
            stats['row_reduction_pct'] = (stats['rows_removed'] / stats['original_rows']) * 100
        else:
            stats['row_reduction_pct'] = 0
        
        if stats['original_memory'] > 0:
            stats['memory_reduction_pct'] = ((stats['original_memory'] - stats['cleaned_memory']) / stats['original_memory']) * 100
        else:
            stats['memory_reduction_pct'] = 0
        
        if stats['total_issues_found'] > 0:
            stats['fix_rate_pct'] = (stats['total_issues_fixed'] / stats['total_issues_found']) * 100
        else:
            stats['fix_rate_pct'] = 0
        
        return stats
