# -*- coding: utf-8 -*-
# scripts/log_analysis/log_file_utils.py

import os

def find_log_file(log_file_arg=None):
    """
    Try to find the log file given an argument, in current dir, or in project root.
    """
    possible_paths = []
    if log_file_arg:
        possible_paths.append(log_file_arg)
    possible_paths.append("eda_batch_check.log")
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    possible_paths.append(os.path.join(repo_root, "eda_batch_check.log"))
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def get_file_stats(log_path):
    """
    Return (file_size_mb, num_lines) for the log file.
    """
    file_size_bytes = os.path.getsize(log_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    with open(log_path, encoding="utf-8") as f:
        num_lines = sum(1 for _ in f)
    return file_size_mb, num_lines