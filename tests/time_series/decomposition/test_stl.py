import pandas as pd
import pytest

from src.time_series.decomposition.stl import STLDecomposer


def test_stl_requires_period():
    idx = pd.date_range("2024-01-01", periods=30, freq="D")
    series = pd.Series(range(30), index=idx)
    dec = STLDecomposer()
    with pytest.raises(ValueError):
        dec.decompose(series, {"seasonal": 7})


def test_stl_decomposition_ok():
    idx = pd.date_range("2024-01-01", periods=60, freq="D")
    series = pd.Series(range(60), index=idx)
    dec = STLDecomposer()
    res = dec.decompose(series, {"period": 7, "seasonal": 7, "trend": 13, "robust": True})
    assert set(["trend", "seasonal", "residual"]) <= set(res.components.keys())


