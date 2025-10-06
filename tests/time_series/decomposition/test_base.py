import pandas as pd
import pytest

from src.time_series.decomposition.base import get_decomposer, validate_ready_series


def test_validate_ready_series_ok():
    idx = pd.date_range("2024-01-01", periods=10, freq="D")
    df = pd.DataFrame({"close": range(10)}, index=idx)
    s = validate_ready_series(df, "close")
    assert isinstance(s, pd.Series)
    assert s.shape[0] == 10


def test_validate_ready_series_requires_datetime_index():
    df = pd.DataFrame({"close": range(5)})
    with pytest.raises(ValueError):
        validate_ready_series(df, "close")


def test_validate_ready_series_non_monotonic():
    idx = pd.to_datetime(["2024-01-02", "2024-01-01"])  # not monotonic
    df = pd.DataFrame({"close": [1, 2]}, index=idx)
    with pytest.raises(ValueError):
        validate_ready_series(df, "close")


def test_validate_ready_series_missing_column():
    idx = pd.date_range("2024-01-01", periods=3, freq="D")
    df = pd.DataFrame({"open": [1, 2, 3]}, index=idx)
    with pytest.raises(ValueError):
        validate_ready_series(df, "close")


def test_validate_ready_series_non_numeric():
    idx = pd.date_range("2024-01-01", periods=3, freq="D")
    df = pd.DataFrame({"close": [1, float("nan"), 3]}, index=idx)
    with pytest.raises(ValueError):
        validate_ready_series(df, "close")


def test_get_decomposer_variants():
    assert get_decomposer("classical").__class__.__name__.endswith("Decomposer")
    assert get_decomposer("stl").__class__.__name__.endswith("Decomposer")
    assert get_decomposer("ceemdan").__class__.__name__.endswith("Decomposer")
    with pytest.raises(ValueError):
        get_decomposer("unknown")


