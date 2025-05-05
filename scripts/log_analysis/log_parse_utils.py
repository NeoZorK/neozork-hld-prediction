# -*- coding: utf-8 -*-
# scripts/log_analysis/log_parse_utils.py

import re
from typing import List, Tuple, Optional

def parse_duplicate_count(line: str) -> Optional[int]:
    """
    Parse duplicate count from a log line.
    """
    match = re.search(r"Number of duplicate rows:\s*(\d+)", line)
    if match:
        return int(match.group(1))
    return None

def parse_nan_columns(line: str) -> Optional[List[str]]:
    """
    Parse list of columns with NaN from a log line.
    """
    match = re.search(r"Columns with NaN values:\s*\[(.*?)\]", line)
    if match:
        raw = match.group(1)
        if raw.strip() == "":
            return []
        return [col.strip().strip("'\"") for col in raw.split(",") if col.strip()]
    return None

def parse_checking_file(line: str) -> Optional[str]:
    """
    Parse file path being checked from a log line.
    """
    match = re.search(r"CHECKING:\s*(\S.*)$", line)
    if match:
        return match.group(1).strip()
    return None

def parse_error_line(line: str) -> Optional[Tuple[str, str]]:
    """
    Parse error lines for file path and message.
    """
    if "ERROR processing" in line:
        match = re.search(r"ERROR processing (.*?): (.*)", line)
        if match:
            return (match.group(1), match.group(2))
    return None

def is_empty_shape(line: str) -> bool:
    """
    Determine if the line indicates an empty shape.
    """
    return "Shape: (0, 0)" in line

def is_missing_values_block_start(line: str) -> bool:
    """
    Determine if the line signals the start of a missing values block.
    """
    return "Missing values:" in line

def parse_missing_lines(lines, i_start):
    """
    Parse missing values lines starting at index i_start.
    Returns tuple (missing_lines, new_index)
    """
    missing_lines = []
    i = i_start
    while i < len(lines):
        next_line = lines[i].strip()
        if next_line == "" or "Number of duplicate rows:" in next_line or \
           "Column types:" in next_line or "Columns with NaN values:" in next_line or \
           "First 3 rows:" in next_line or "Statistical summary:" in next_line or \
           "CHECKING:" in next_line:
            break
        if next_line.startswith("Series([], dtype: int64)"):
            break
        missing_lines.append(next_line)
        i += 1
    return missing_lines, i