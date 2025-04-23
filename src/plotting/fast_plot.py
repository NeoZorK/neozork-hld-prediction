import pandas as pd
import dask.dataframe as dd
import datashader as ds
import datashader.transfer_functions as tf
from bokeh.plotting import figure, output_file, save, show
from bokeh.models import DatetimeTickFormatter
from pathlib import Path
from ..common import logger

def plot_indicator_results_fast(df, rule, title="Indicator Results (Fast)"):
    """
    Renders an OHLCV chart using Dask + Datashader + Bokeh for large DataFrames.
    Suitable for visualizing millions of rows (e.g., M1 OHLCV).
    """
    logger.print_info("Rendering chart using Dask+Datashader+Bokeh (fast mode)...")
    # Ensure index is datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        if 'DateTime' in df.columns:
            df = df.copy()
            df.index = pd.to_datetime(df['DateTime'])
        else:
            logger.print_warning("Index is not datetime and no 'DateTime' column found.")

    ddf = dd.from_pandas(df, npartitions=16)
    cvs = ds.Canvas(plot_width=1200, plot_height=600,
                    x_range=(df.index.min(), df.index.max()),
                    y_range=(df['Low'].min(), df['High'].max()))
    agg = cvs.line(ddf, 'index', 'Close', agg=ds.mean('Close'))
    img = tf.shade(agg, cmap=['lightblue', 'navy'], how='linear')

    p = figure(title=title, x_axis_type='datetime', width=1200, height=600)
    p.xaxis.formatter = DatetimeTickFormatter(minutes=["%Y-%m-%d %H:%M"], hours=["%Y-%m-%d %H:%M"], days=["%Y-%m-%d"])
    p.xaxis.axis_label = "Time"
    p.yaxis.axis_label = "Price"
    # Convert Datashader image to RGBA and plot as image on Bokeh canvas
    p.image_rgba(image=[img.to_pil().convert("RGBA")],
                 x=df.index.min().value // 10 ** 6,
                 y=df['Low'].min(),
                 dw=(df.index.max() - df.index.min()).total_seconds() * 1000,
                 dh=df['High'].max() - df['Low'].min())

    output_dir = Path("results/plots")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "fast_plot.html"
    output_file(str(output_path), title=title, mode="cdn")
    save(p)
    logger.print_success(f"Fast chart (datashader+bokeh) saved to {output_path}")
    try:
        show(p)
    except Exception:
        logger.print_info("Could not auto-open plot (possibly headless environment)")