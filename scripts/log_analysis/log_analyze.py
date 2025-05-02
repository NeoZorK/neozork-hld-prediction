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

def parse_duplicate_count(line):
    """
    Parse duplicate count from a log line.
    Works with both INFO prefix and without.
    """
    # Example with prefix: 2025-05-02 13:11:09,090 | INFO | Number of duplicate rows: 67449
    # Example without: Number of duplicate rows: 67449
    match = re.search(r"Number of duplicate rows:\s*(\d+)", line)
    if match:
        return int(match.group(1))
    return None

def parse_nan_columns(line):
    """
    Parse list of columns with NaN from a log line.
    """
    # Example with prefix: 2025-05-02 13:11:05,867 | INFO | Columns with NaN values: []
    match = re.search(r"Columns with NaN values:\s*\[(.*?)\]", line)
    if match:
        raw = match.group(1)
        if raw.strip() == "":
            return []
        # Split by comma, strip quotes and spaces
        return [col.strip().strip("'\"") for col in raw.split(",") if col.strip()]
    return None

def parse_checking_file(line):
    """
    Parse file path being checked from a log line.
    Supports both with and without INFO prefix.
    """
    # Example: 2025-05-02 13:11:10,662 | INFO | CHECKING: data/cache/csv_converted/CSVExport_AAPL.NAS_PERIOD_W1.parquet
    match = re.search(r"CHECKING:\s*(\S.*)$", line)
    if match:
        return match.group(1).strip()
    return None

def analyze_log(log_path: str) -> None:
    """
    Analyze the log file for common EDA problems and print a concise report.
    Print file statistics before analysis.
    """
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

    errors = []
    empty_files = []
    file_duplicates = {}
    file_nan_columns = {}
    file_missing = {}
    current_file = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # 1. CHECKING: <file>
        checking_file = parse_checking_file(line)
        if checking_file:
            current_file = checking_file
            i += 1
            continue

        # 2. Error
        if "ERROR processing" in line:
            match = re.search(r"ERROR processing (.*?): (.*)", line)
            if match:
                errors.append((match.group(1), match.group(2)))
            i += 1
            continue

        # 3. Empty shape
        if "Shape: (0, 0)" in line and current_file:
            empty_files.append(current_file)
            i += 1
            continue

        # 4. Duplicates
        dup_count = parse_duplicate_count(line)
        if dup_count is not None and current_file:
            if dup_count > 0:
                file_duplicates[current_file] = dup_count
            i += 1
            continue

        # 5. NaN columns
        nan_cols = parse_nan_columns(line)
        if nan_cols is not None and current_file:
            if len(nan_cols) > 0:
                file_nan_columns[current_file] = nan_cols
            i += 1
            continue

        # 6. Missing values block (Series([], dtype: int64) or real)
        if "Missing values:" in line and current_file:
            missing_lines = []
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                # End block on empty line, next section, or other known keywords
                if next_line == "" or "Number of duplicate rows:" in next_line or \
                   "Column types:" in next_line or "Columns with NaN values:" in next_line or \
                   "First 3 rows:" in next_line or "Statistical summary:" in next_line or \
                   "CHECKING:" in next_line:
                    break
                # Skip empty Series
                if next_line.startswith("Series([], dtype: int64)"):
                    break
                missing_lines.append(next_line)
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