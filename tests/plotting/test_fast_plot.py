import pandas as pd
import numpy as np
from src.plotting.fast_plot import plot_indicator_results_fast

def test_fast_plot_smoke(tmp_path):
    """
    Smoke test for fast plot: plot a simple OHLCV DataFrame and ensure file is created.
    """
    # Generate sample data
    n = 10000
    idx = pd.date_range("2024-01-01", freq="T", periods=n)
    df = pd.DataFrame({
        "Open": np.random.rand(n) * 100,
        "High": np.random.rand(n) * 100 + 1,
        "Low": np.random.rand(n) * 100 - 1,
        "Close": np.random.rand(n) * 100,
    }, index=idx)
    class DummyRule:
        name = "DummyRule"
    plot_indicator_results_fast(df, DummyRule, title="Test Fast Plot")
    # Check output file exists
    out_plot = tmp_path / "results" / "plots" / "fast_plot.html"
    assert out_plot.exists() or (tmp_path / "fast_plot.html").exists()