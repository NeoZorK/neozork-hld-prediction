from __future__ import annotations

import os
from typing import Iterable, List, Optional, Tuple

import pandas as pd


SUPPORTED_INPUT_DIRS = [
    "data",
    os.path.join("data", "indicators"),
    os.path.join("data", "raw_parquet"),
    os.path.join("data", "cleaned_data"),
]


def discover_files(path: str, select_mask: Optional[str] = None) -> List[str]:
    if os.path.isfile(path):
        return [path]
    candidates: List[str] = []
    for root, _, files in os.walk(path):
        for fname in files:
            if not (fname.endswith(".csv") or fname.endswith(".parquet")):
                continue
            full = os.path.join(root, fname)
            if select_mask and select_mask not in fname:
                continue
            candidates.append(full)
    return sorted(candidates)


def read_timeseries(
    file_path: str,
    datetime_col: Optional[str] = None,
    target_column: Optional[str] = None,
) -> Tuple[pd.DataFrame, str]:
    if file_path.endswith(".parquet"):
        df = pd.read_parquet(file_path)
    else:
        df = pd.read_csv(file_path)

    # Try to infer datetime column if not provided
    dt_col = datetime_col
    if dt_col is None:
        for cand in ["time", "datetime", "date", "timestamp"]:
            if cand in df.columns:
                dt_col = cand
                break
    if dt_col is not None and dt_col in df.columns:
        df[dt_col] = pd.to_datetime(df[dt_col], errors="raise")
        df = df.set_index(dt_col)

    # Target column selection heuristic
    col = target_column
    if col is None:
        preferred = ["close", "value"]
        for p in preferred:
            if p in df.columns:
                col = p
                break
        if col is None:
            numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            if not numeric_cols:
                raise ValueError(
                    f"No numeric columns found in {os.path.basename(file_path)}. Prepare data upstream."
                )
            col = numeric_cols[0]

    return df, col


