# -*- coding: utf-8 -*-
# scripts/log_analysis/log_analyze.py

import os
import re

def analyze_log(log_path: str) -> None:
    """
    Analyze the log file for common EDA problems and print a concise report.
    """
    if not os.path.exists(log_path):
        print(f"Log file '{log_path}' not found.")
        return

    error_pattern = re.compile(r"ERROR processing (.*?): (.*)")
    empty_shape_pattern = re.compile(r"Shape: \((0, 0)\)")
    many_missing_pattern = re.compile(r"Missing values:\n(.+)")
    many_duplicates_pattern = re.compile(r"Number of duplicate rows: (\d+)")
    nan_columns_pattern = re.compile(r"Columns with NaN values: \[(.*?)\]")

    errors = []
    empty_files = []
    files_with_many_missing = []
    files_with_duplicates = []
    files_with_nan_columns = []

    current_file = None
    current_missing = None

    with open(log_path, encoding="utf-8") as f:
        for line in f:
            # Detect errors in file processing
            error_match = error_pattern.search(line)
            if error_match:
                errors.append((error_match.group(1), error_match.group(2)))
                continue

            # Detect start of file analysis
            if line.startswith("CHECKING: "):
                current_file = line.strip().split("CHECKING: ")[-1]
                continue

            # Detect empty DataFrame
            if empty_shape_pattern.search(line):
                if current_file:
                    empty_files.append(current_file)
                continue

            # Detect many missing values
            if line.startswith("Missing values:"):
                current_missing = []
                continue
            if current_missing is not None:
                if line.strip() == "":
                    if current_missing and current_file:
                        files_with_many_missing.append((current_file, current_missing.copy()))
                    current_missing = None
                else:
                    current_missing.append(line.strip())
                continue

            # Detect duplicates
            dup_match = many_duplicates_pattern.search(line)
            if dup_match and int(dup_match.group(1)) > 0:
                if current_file:
                    files_with_duplicates.append((current_file, int(dup_match.group(1))))
                continue

            # Detect NaN columns
            nan_match = nan_columns_pattern.search(line)
            if nan_match and nan_match.group(1).strip():
                if current_file:
                    cols = [col.strip().strip("'") for col in nan_match.group(1).split(",") if col.strip()]
                    files_with_nan_columns.append((current_file, cols))
                continue

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
    if files_with_duplicates:
        for path, count in files_with_duplicates:
            print(f"  {path}: {count} duplicates")
    else:
        print("  None")

    print("\nFiles with columns containing NaN values:")
    if files_with_nan_columns:
        for path, cols in files_with_nan_columns:
            print(f"  {path}: {', '.join(cols)}")
    else:
        print("  None")

    print("\nFiles with many missing values (partial list):")
    if files_with_many_missing:
        for path, missings in files_with_many_missing:
            print(f"  {path}:")
            for miss in missings:
                print(f"    {miss}")
    else:
        print("  None")

    print("\n--- End of Report ---\n")

if __name__ == "__main__":
    analyze_log("eda_batch_check.log")