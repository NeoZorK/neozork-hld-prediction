#!/usr/bin/env python3
"""
Test Results Management Script

This script provides utilities for managing test results stored in logs/test_results/
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas as pd

class TestResultsManager:
    """Manage test results stored in logs/test_results/"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results_dir = project_root / "logs" / "test_results"
        
    def get_results_files(self, days: Optional[int] = None) -> List[Path]:
        """Get list of test result files, optionally filtered by age"""
        if not self.results_dir.exists():
            return []
        
        files = list(self.results_dir.glob("*.json"))
        
        if days is not None:
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_files = []
            for file in files:
                try:
                    # Try to parse timestamp from filename
                    timestamp_str = file.stem.split('_')[-1]
                    file_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    if file_date >= cutoff_date:
                        filtered_files.append(file)
                except (ValueError, IndexError):
                    # If filename doesn't match pattern, include it
                    filtered_files.append(file)
            return filtered_files
        
        return files
    
    def load_results(self, file_path: Path) -> Dict[str, Any]:
        """Load test results from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return {}
    
    def get_latest_results(self) -> Optional[Dict[str, Any]]:
        """Get the most recent test results"""
        files = self.get_results_files()
        if not files:
            return None
        
        # Sort by modification time
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        return self.load_results(latest_file)
    
    def get_results_summary(self, days: int = 7) -> pd.DataFrame:
        """Get summary of test results over specified period"""
        files = self.get_results_files(days)
        if not files:
            return pd.DataFrame()
        
        results = []
        for file in files:
            data = self.load_results(file)
            if data:
                results.append(data)
        
        if not results:
            return pd.DataFrame()
        
        df = pd.DataFrame(results)
        
        # Convert timestamp to datetime if present
        if 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime'])
        
        return df.sort_values('datetime', ascending=False)
    
    def clean_old_results(self, days: int = 30) -> int:
        """Remove test result files older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        files_to_remove = []
        
        for file in self.get_results_files():
            try:
                # Try to parse timestamp from filename
                timestamp_str = file.stem.split('_')[-1]
                file_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                if file_date < cutoff_date:
                    files_to_remove.append(file)
            except (ValueError, IndexError):
                # If filename doesn't match pattern, check file modification time
                file_mtime = datetime.fromtimestamp(file.stat().st_mtime)
                if file_mtime < cutoff_date:
                    files_to_remove.append(file)
        
        # Remove files
        for file in files_to_remove:
            try:
                file.unlink()
                print(f"Removed: {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")
        
        return len(files_to_remove)
    
    def generate_report(self, days: int = 7) -> str:
        """Generate a comprehensive test results report"""
        df = self.get_results_summary(days)
        
        if df.empty:
            return "No test results found for the specified period."
        
        report = []
        report.append("=" * 60)
        report.append("📊 TEST RESULTS REPORT")
        report.append("=" * 60)
        report.append(f"Period: Last {days} days")
        report.append(f"Total test runs: {len(df)}")
        report.append("")
        
        # Overall statistics
        total_tests = df['total'].sum()
        total_passed = df['passed'].sum()
        total_failed = df['failed'].sum()
        total_skipped = df['skipped'].sum()
        total_errors = df['errors'].sum()
        
        overall_success_rate = (total_passed / (total_passed + total_failed + total_errors)) * 100 if (total_passed + total_failed + total_errors) > 0 else 0
        
        report.append("📈 OVERALL STATISTICS")
        report.append("-" * 30)
        report.append(f"Total tests executed: {total_tests:,}")
        report.append(f"Passed: {total_passed:,} ({total_passed/total_tests*100:.1f}%)")
        report.append(f"Failed: {total_failed:,} ({total_failed/total_tests*100:.1f}%)")
        report.append(f"Skipped: {total_skipped:,} ({total_skipped/total_tests*100:.1f}%)")
        report.append(f"Errors: {total_errors:,} ({total_errors/total_tests*100:.1f}%)")
        report.append(f"Overall success rate: {overall_success_rate:.1f}%")
        report.append("")
        
        # Recent runs
        report.append("🕒 RECENT TEST RUNS")
        report.append("-" * 30)
        
        for _, row in df.head(10).iterrows():
            timestamp = row.get('timestamp', 'Unknown')
            passed = row.get('passed', 0)
            failed = row.get('failed', 0)
            skipped = row.get('skipped', 0)
            total = row.get('total', 0)
            success_rate = row.get('success_rate', 0)
            
            status = "✅" if failed == 0 and row.get('errors', 0) == 0 else "❌"
            
            report.append(f"{status} {timestamp}: {passed}/{total} passed ({success_rate:.1f}%)")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def export_results(self, output_file: str, days: int = 7) -> None:
        """Export test results to CSV or Excel file"""
        df = self.get_results_summary(days)
        
        if df.empty:
            print("No test results to export.")
            return
        
        output_path = Path(output_file)
        
        if output_path.suffix.lower() == '.csv':
            df.to_csv(output_path, index=False)
        elif output_path.suffix.lower() in ['.xlsx', '.xls']:
            df.to_excel(output_path, index=False)
        else:
            print("Unsupported file format. Use .csv or .xlsx")
            return
        
        print(f"Test results exported to: {output_path}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Test Results Management")
    parser.add_argument("--project-root", default=".", 
                       help="Project root directory (default: current directory)")
    parser.add_argument("--action", choices=["report", "clean", "export", "latest"], 
                       default="report", help="Action to perform")
    parser.add_argument("--days", type=int, default=7, 
                       help="Number of days to include in report/clean (default: 7)")
    parser.add_argument("--output", help="Output file for export action")
    
    args = parser.parse_args()
    
    project_root = Path(args.project_root).resolve()
    manager = TestResultsManager(project_root)
    
    if args.action == "report":
        report = manager.generate_report(args.days)
        print(report)
    
    elif args.action == "clean":
        removed_count = manager.clean_old_results(args.days)
        print(f"Removed {removed_count} old test result files")
    
    elif args.action == "export":
        if not args.output:
            print("Error: --output is required for export action")
            sys.exit(1)
        manager.export_results(args.output, args.days)
    
    elif args.action == "latest":
        latest = manager.get_latest_results()
        if latest:
            print("Latest test results:")
            print(json.dumps(latest, indent=2))
        else:
            print("No test results found")

if __name__ == "__main__":
    main() 