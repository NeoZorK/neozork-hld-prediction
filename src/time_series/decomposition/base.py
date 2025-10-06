from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Protocol

import pandas as pd


@dataclass
class DecompositionResult:
    original: pd.Series
    components: Dict[str, pd.Series]
    method: str
    params: Dict[str, object]
    metadata: Dict[str, object]

    def to_dataframe_wide(self) -> pd.DataFrame:
        df = pd.DataFrame({"original": self.original})
        for name, comp in self.components.items():
            df[name] = comp
        return df


class DecompositionMethod(Protocol):
    def decompose(self, series: pd.Series, params: Dict[str, object]) -> DecompositionResult:  # pragma: no cover - interface
        ...


def validate_ready_series(
    df: pd.DataFrame,
    target_column: str,
    datetime_col: Optional[str] = None,
) -> pd.Series:
    if datetime_col is not None and datetime_col in df.columns:
        df = df.set_index(pd.to_datetime(df[datetime_col], errors="raise"))
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError(
            "Input must have a DatetimeIndex or specify --datetime-col. Please use clear_data.py upstream."
        )
    if not df.index.is_monotonic_increasing:
        raise ValueError(
            "DatetimeIndex must be monotonic increasing. Please fix ordering via clear_data.py upstream."
        )
    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' not found. Provide --column or prepare data upstream."
        )
    series = pd.to_numeric(df[target_column], errors="coerce")
    if series.isna().any():
        raise ValueError(
            "Target series contains non-numeric or NaN values. Please impute/clean upstream (no preprocessing here)."
        )
    return series


def get_decomposer(method: str) -> DecompositionMethod:
    method_lower = method.lower()
    if method_lower == "classical":
        from .classical import ClassicalDecomposer

        return ClassicalDecomposer()
    if method_lower == "stl":
        from .stl import STLDecomposer

        return STLDecomposer()
    if method_lower == "ceemdan":
        from .ceemdan import CEEMDANDecomposer

        return CEEMDANDecomposer()
    raise ValueError(f"Unknown decomposition method: {method}")


