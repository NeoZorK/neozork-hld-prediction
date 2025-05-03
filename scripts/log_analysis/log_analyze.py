# -*- coding: utf-8 -*-
# scripts/log_analysis/log_analyze.py

import os
import sys

# Add the project root to sys.path for absolute imports to work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import re
from collections import defaultdict
from typing import List, Dict, Optional, Tuple

from scripts.log_analysis.log_file_utils import (
    find_log_file,
    get_file_stats,
)
from scripts.log_analysis.log_parse_utils import (
    parse_duplicate_count,
    parse_nan_columns,
    parse_checking_file,
    parse_error_line,
    is_empty_shape,
    is_missing_values_block_start,
    parse_missing_lines,
)

def analyze_log(log_path: str) -> Dict[str, any]:
    """
    Analyze the log file for common EDA problems and return a report dictionary.
    """
    if not os.path.exists(log_path):
        print(f"Log file '{log_path}' not found.")
        return {}

    file_size_mb, num_lines = get_file_stats(log_path)
    print(f"\nLog file '{log_path}' found.")
    print(f"File size: {file_size_mb:.2f} MB")
    print(f"Line count: {num_lines}")
    print("Starting log analysis...\n")

    errors: List[Tuple[str, str]] = []
    empty_files: List[str] = []
    file_duplicates: Dict[str, int] = {}
    file_nan_columns: Dict[str, List[str]] = {}
    file_missing: Dict[str, List[str]] = defaultdict(list)
    current_file: Optional[str] = None

    with open(log_path, encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Parse file section start
        checking_file = parse_checking_file(line)
        if checking_file:
            current_file = checking_file
            i += 1
            continue

        # Parse errors
        error = parse_error_line(line)
        if error:
            errors.append(error)
            i += 1
            continue

        # Parse empty files
        if is_empty_shape(line) and current_file:
            empty_files.append(current_file)
            i += 1
            continue

        # Parse duplicates
        dup_count = parse_duplicate_count(line)
        if dup_count is not None and current_file:
            if dup_count > 0:
                file_duplicates[current_file] = dup_count
            i += 1
            continue

        # Parse NaN columns
        nan_cols = parse_nan_columns(line)
        if nan_cols is not None and current_file:
            if len(nan_cols) > 0:
                file_nan_columns[current_file] = nan_cols
            i += 1
            continue

        # Parse missing values block
        if is_missing_values_block_start(line) and current_file:
            missing_lines, i = parse_missing_lines(lines, i + 1)
            if missing_lines:
                file_missing[current_file].extend(missing_lines)
            continue

        i += 1

    report = {
        "file_size_mb": file_size_mb,
        "num_lines": num_lines,
        "errors": errors,
        "empty_files": empty_files,
        "file_duplicates": file_duplicates,
        "file_nan_columns": file_nan_columns,
        "file_missing": dict(file_missing)
    }
    print_report(report)
    return report

def print_report(report: Dict[str, any]) -> None:
    """
    Print the parsed EDA log analysis report.
    """
    print("\n--- EDA Log Analysis Report ---\n")

    # Errors
    errors = report.get("errors", [])
    if errors:
        print("Files with errors:")
        for path, msg in errors:
            print(f"  {path}: {msg}")
    else:
        print("No file processing errors found.")

    # Empty files
    print("\nEmpty files (Shape: (0, 0)):")
    empty_files = report.get("empty_files", [])
    if empty_files:
        for path in empty_files:
            print(f"  {path}")
    else:
        print("  None")

    # Duplicates
    print("\nFiles with duplicate rows:")
    file_duplicates = report.get("file_duplicates", {})
    if file_duplicates:
        for path, count in sorted(file_duplicates.items(), key=lambda t: t[1], reverse=True):
            print(f"  {path}: {count} duplicates")
    else:
        print("  None")

    # NaN columns
    print("\nFiles with columns containing NaN values:")
    file_nan_columns = report.get("file_nan_columns", {})
    if file_nan_columns:
        for path, cols in file_nan_columns.items():
            print(f"  {path}: {', '.join(cols)}")
    else:
        print("  None")

    # Missing values
    print("\nFiles with many missing values (partial list):")
    file_missing = report.get("file_missing", {})
    if file_missing:
        for path, missings in file_missing.items():
            print(f"  {path}:")
            for miss in missings:
                print(f"    {miss}")
    else:
        print("  None")

    print("\n--- End of Report ---\n")

if __name__ == "__main__":
    log_file_arg = sys.argv[1] if len(sys.argv) > 1 else None
    log_path = find_log_file(log_file_arg)
    if not log_path:
        print("Log file 'eda_batch_check.log' not found. (Tried current dir and project root)")
        sys.exit(1)
    analyze_log(log_path)