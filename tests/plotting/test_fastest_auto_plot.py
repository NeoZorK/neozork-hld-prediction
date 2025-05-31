import os
import tempfile
import pandas as pd
import pytest
from plotly.graph_objs._figure import Figure

from src.plotting import fastest_auto_plot

def create_test_parquet(tmp_path, columns=None, nrows=100):
    if columns is None:
        columns = {
            'Open': 1.0,
            'High': 2.0,
            'Low': 0.5,
            'Close': 1.5,
            'Volume': 100,
            'timestamp': pd.date_range('2023-01-01', periods=nrows, freq='min'),
            'custom1': range(nrows),
            'custom2': [x * 2 for x in range(nrows)]
        }
    df = pd.DataFrame({k: v if hasattr(v, '__len__') and not isinstance(v, str) else [v]*nrows for k, v in columns.items()})
    parquet_path = tmp_path / "test.parquet"
    df.to_parquet(parquet_path)
    return parquet_path, df

def test_plot_auto_fastest_parquet_creates_html_and_returns_figure(tmp_path):
    parquet_path, df = create_test_parquet(tmp_path)
    output_html = tmp_path / "output.html"
    fig = fastest_auto_plot.plot_auto_fastest_parquet(
        str(parquet_path), str(output_html), trading_rule_name="AUTO_TEST", title="Test Title", width=800, height_per_panel=200
    )
    assert isinstance(fig, Figure)
    assert os.path.exists(output_html)
    # Check that the figure contains at least as many traces as custom columns
    custom_cols = [c for c in df.columns if c.lower() not in ['open','high','low','close','volume','timestamp','datetime','index','date','time'] and pd.api.types.is_numeric_dtype(df[c])]
    assert len(fig.data) >= len(custom_cols)

def test_plot_auto_fastest_parquet_raises_on_no_numeric(tmp_path):
    columns = {
        'timestamp': pd.date_range('2023-01-01', periods=10, freq='min'),
        'text_col': ['a']*10
    }
    parquet_path, _ = create_test_parquet(tmp_path, columns=columns, nrows=10)
    output_html = tmp_path / "output2.html"
    with pytest.raises(ValueError):
        fastest_auto_plot.plot_auto_fastest_parquet(str(parquet_path), str(output_html))


def test_plot_auto_fastest_parquet_handles_index_time(tmp_path):
    # No explicit time column, but DatetimeIndex
    nrows = 20
    df = pd.DataFrame({
        'Open': 1.0,
        'High': 2.0,
        'Low': 0.5,
        'Close': 1.5,
        'Volume': 100,
        'custom1': range(nrows),
        'custom2': [x * 2 for x in range(nrows)]
    }, index=pd.date_range('2023-01-01', periods=nrows, freq='min'))
    parquet_path = tmp_path / "test3.parquet"
    df.to_parquet(parquet_path)
    output_html = tmp_path / "output3.html"
    fig = fastest_auto_plot.plot_auto_fastest_parquet(str(parquet_path), str(output_html))
    assert isinstance(fig, Figure)
    assert os.path.exists(output_html)

