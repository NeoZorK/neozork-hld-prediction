# -*- coding: utf-8 -*-
# scripts/log_analysis/log_analyze.py

import os
import sys
import re

def find_log_file(log_file_arg=None):
    """
    Find the log file. Try argument, then current dir, then project root.
    """
    possible_paths = []
    if log_file_arg:
        possible_paths.append(log_file_arg)
    possible_paths.append("eda_batch_check.log")
    # Try project root
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    possible_paths.append(os.path.join(repo_root, "eda_batch_check.log"))
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def analyze_log(log_path: str) -> None:
    """
    Analyze the log file for common EDA problems and print a concise report.
    Print file statistics before analysis.
    """
    # Check if log file exists
    if not os.path.exists(log_path):
        print(f"Log file '{log_path}' not found.")
        return

    # Gather file statistics
    file_size_bytes = os.path.getsize(log_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    with open(log_path, encoding="utf-8") as f:
        lines = f.readlines()
    num_lines = len(lines)

    print(f"\nLog file '{log_path}' found.")
    print(f"File size: {file_size_mb:.2f} MB")
    print(f"Line count: {num_lines}")
    print("Starting log analysis...\n")

    # Regular expression patterns for matching log lines
    error_pattern = re.compile(r"ERROR processing (.*?): (.*)")
    checking_pattern = re.compile(r"CHECKING: (.+)")
    empty_shape_pattern = re.compile(r"Shape: \((0, 0)\)")
    duplicate_pattern = re.compile(r"Number of duplicate rows: (\d+)")
    nan_columns_pattern = re.compile(r"Columns with NaN values: \[(.*?)\]")
    missing_value_start = re.compile(r"Missing values:\n?$")

    # Data structures for collecting issues
    errors = []
    empty_files = []
    files_with_duplicates = []
    files_with_nan_columns = []
    files_with_many_missing = []

    current_file = None
    file_duplicates = {}
    file_nan_columns = {}
    file_missing = {}

    i = 0
    while i < len(lines):
        line = lines[i]
        # Match file start
        match_chk = checking_pattern.match(line)
        if match_chk:
            current_file = match_chk.group(1)
            i += 1
            continue

        # Match errors
        match_err = error_pattern.match(line)
        if match_err:
            errors.append((match_err.group(1), match_err.group(2)))
            i += 1
            continue

        # Match empty shape
        if empty_shape_pattern.search(line):
            if current_file:
                empty_files.append(current_file)
            i += 1
            continue

        # Match duplicates
        match_dup = duplicate_pattern.match(line)
        if match_dup and current_file:
            count = int(match_dup.group(1))
            if count > 0:
                file_duplicates.setdefault(current_file, 0)
                file_duplicates[current_file] += count
            i += 1
            continue

        # Match NaN columns
        match_nan = nan_columns_pattern.match(line)
        if match_nan and current_file:
            nan_cols = [col.strip().strip("'") for col in match_nan.group(1).split(",") if col.strip()]
            if nan_cols:
                file_nan_columns.setdefault(current_file, set())
                file_nan_columns[current_file].update(nan_cols)
            i += 1
            continue

        # Match missing values
        if missing_value_start.match(line) and current_file:
            missing_lines = []
            i += 1
            # Collect missing values until next empty line or section
            while i < len(lines) and lines[i].strip() and not checking_pattern.match(lines[i]):
                missing_lines.append(lines[i].strip())
                i += 1
            if missing_lines:
                file_missing.setdefault(current_file, [])
                file_missing[current_file].extend(missing_lines)
            continue

        i += 1

    # Output report
    print("\n--- EDA Log Analysis Report ---\n")

    if errors:
        print("Files with errors:")
        for path, msg in errors:
            print(f"  {path}: {msg}")
    else:
        print("No file processing errors found.")

    print("\nEmpty files (Shape: (0, 0)):")
    if empty_files:
        for path in empty_files:
            print(f"  {path}")
    else:
        print("  None")

    print("\nFiles with duplicate rows:")
    if file_duplicates:
        for path, count in file_duplicates.items():
            print(f"  {path}: {count} duplicates")
    else:
        print("  None")

    print("\nFiles with columns containing NaN values:")
    if file_nan_columns:
        for path, cols in file_nan_columns.items():
            print(f"  {path}: {', '.join(cols)}")
    else:
        print("  None")

    print("\nFiles with many missing values (partial list):")
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