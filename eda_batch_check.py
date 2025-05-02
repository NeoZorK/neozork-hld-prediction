# -*- coding: utf-8 -*-
# /eda_batch_check.py

import os
from typing import List
from tqdm import tqdm
from src.eda.data_overview import (
    load_data,
    show_basic_info,
    show_head,
    check_missing_values,
    check_duplicates,
    get_column_types,
    get_nan_columns,
    get_summary
)

def find_data_files(folder_paths: List[str], extensions: List[str] = [".parquet", ".csv"]) -> List[str]:
    """
    Recursively find all files with given extensions in the provided folders and their subfolders.

    Args:
        folder_paths (List[str]): List of folder paths.
        extensions (List[str]): List of file extensions to include.

    Returns:
        List[str]: List of found file paths.
    """
    data_files = []
    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    data_files.append(os.path.join(root, file))
    return data_files

def check_file(file_path: str):
    """
    Perform EDA-check on a single file.

    Args:
        file_path (str): Path to the file.
    """
    print(f"\n=====================\nCHECKING: {file_path}\n=====================")
    ext = os.path.splitext(file_path)[-1].lower()
    file_type = "parquet" if ext == ".parquet" else "csv"
    try:
        df = load_data(file_path, file_type=file_type)
        show_basic_info(df)
        show_head(df, n=3)
        check_missing_values(df)
        check_duplicates(df)
        get_column_types(df)
        get_nan_columns(df)
        get_summary(df)
    except Exception as e:
        print(f"ERROR processing {file_path}: {e}")

def main():
    """
    Main function to find and check all data files in specified folders.
    """
    target_folders = [
        "data/cache/csv_converted",
        "data/raw_parquet",
        "mql5_feed"
    ]
    data_files = find_data_files(target_folders)
    print(f"Found {len(data_files)} data files in specified folders.")
    for file_path in tqdm(data_files, desc="EDA CHECK", unit="file"):
        check_file(file_path)

if __name__ == "__main__":
    main()