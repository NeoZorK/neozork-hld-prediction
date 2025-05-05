# src/eda/eda_file_utils.py

import os
import shutil
from typing import List, Union

# This module provides utility functions for file operations related to data files.
def sort_files_by_type(base_dir: str, parquet_dir: str, csv_dir: str) -> None:
    os.makedirs(parquet_dir, exist_ok=True)
    os.makedirs(csv_dir, exist_ok=True)
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path):
            if file.lower().endswith('.parquet'):
                target_path = os.path.join(parquet_dir, file)
                shutil.move(file_path, target_path)
                print(f"  Moved paquet file: {file} -> {target_path}")
            elif file.lower().endswith('.csv'):
                target_path = os.path.join(csv_dir, file)
                shutil.move(file_path, target_path)
                print(f"  Move CSV File: {file} -> {target_path}")

# This function finds all data files in the specified folder and its subfolders.
def find_data_files(folder_path: Union[str, List[str]], extensions: List[str] = [".parquet", ".csv"], exclude_paths: List[str] = None) -> List[str]:
    data_files = []
    if isinstance(folder_path, str):
        folder_path = [folder_path]
    exclude_abs_paths = [os.path.abspath(p) for p in exclude_paths] if exclude_paths else []
    for folder in folder_path:
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder):
            current_abs_path = os.path.abspath(root)
            if exclude_abs_paths and any(current_abs_path.startswith(p) for p in exclude_abs_paths):
                continue
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    data_files.append(file_path)
    return data_files