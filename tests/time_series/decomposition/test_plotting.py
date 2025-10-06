import os
import pandas as pd

from src.time_series.decomposition.base import DecompositionResult
from src.time_series.decomposition.plotting import plot_and_save


def test_plot_and_save_creates_file(tmp_path):
    idx = pd.date_range("2024-01-01", periods=10, freq="D")
    original = pd.Series(range(10), index=idx)
    components = {
        "trend": original.rolling(3, min_periods=1).mean(),
        "seasonal": pd.Series([0] * 10, index=idx),
        "residual": original - original.rolling(3, min_periods=1).mean().fillna(0),
    }
    result = DecompositionResult(original=original, components=components, method="stl", params={}, metadata={})
    out = plot_and_save(result, str(tmp_path), "test", locale_ru=True)
    assert os.path.exists(out)


