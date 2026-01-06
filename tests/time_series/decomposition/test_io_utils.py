import os
import pandas as pd

from src.time_series.decomposition.io_utils import read_timeseries


def test_read_timeseries_infers_time_and_column(tmp_path):
    p = tmp_path / "sample.parquet"
    df = pd.DataFrame({
        "datetime": pd.date_range("2024-01-01", periods=5, freq="D"),
        "open": [1, 2, 3, 4, 5],
        "high": [2, 3, 4, 5, 6],
        "low": [0, 1, 2, 3, 4],
        "close": [1.5, 2.5, 3.5, 4.5, 5.5],
        "my_ind": [10, 11, 12, 13, 14],
    })
    df.to_parquet(p)

    loaded, col = read_timeseries(str(p))
    assert isinstance(loaded.index, pd.DatetimeIndex)
    assert col == "close"


def test_read_timeseries_fallback_numeric_column(tmp_path):
    p = tmp_path / "sample.csv"
    df = pd.DataFrame({
        "time": pd.date_range("2024-01-01", periods=3, freq="D"),
        "value": [1.0, 2.0, 3.0],
        "text": ["a", "b", "c"],
    })
    df.to_csv(p, index=False)
    loaded, col = read_timeseries(str(p))
    assert isinstance(loaded.index, pd.DatetimeIndex)
    assert col == "value"


