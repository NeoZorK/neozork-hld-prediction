import os
import dask.dataframe as dd
import datashader as ds
import datashader.transfer_functions as tf
import pandas as pd
from bokeh.plotting import output_file, save, figure
from bokeh.models import Title

def plot_indicator_results_fast(
    df,
    rule,
    title='',
    output_path="results/plots/fast_plot.html",
    width=900,
    height=500,
    **kwargs
):
    """
    Render a fast OHLC/indicator plot using Dask+Datashader+Bokeh.

    Args:
        df (pd.DataFrame): DataFrame with at least columns ['Open', 'High', 'Low', 'Close'] and DateTimeIndex or index column.
        rule: TradingRule or indicator rule name (for title).
        title (str): Plot title.
        output_path (str): Path to save HTML plot.
        width, height (int): Plot size.
        **kwargs: Not used (for signature compatibility).

    Returns:
        None (saves interactive HTML to output_path)
    """

    # Ensure there is a column 'index' of type datetime64[ns] for datashader
    if 'index' not in df.columns:
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.copy()
            df['index'] = df.index
        else:
            raise ValueError("DataFrame must have a datetime index or a column 'index' of type datetime64[ns].")
    df['index'] = pd.to_datetime(df['index'])

    # Convert datetime to nanoseconds since epoch for Datashader's linear x axis
    df['index_num'] = df['index'].astype('int64')

    # Use Dask DataFrame for Datashader
    ddf = dd.from_pandas(df, npartitions=1)

    cvs = ds.Canvas(
        plot_width=width,
        plot_height=height,
        x_range=(df['index_num'].min(), df['index_num'].max()),
        y_range=(df['Low'].min(), df['High'].max())
    )

    # Render close price as line
    agg = cvs.line(ddf, 'index_num', 'Close', agg=ds.mean('Close'))
    img = tf.shade(agg, cmap=['blue'], how='linear')

    # Prepare Bokeh figure
    p = figure(
        width=width,
        height=height,
        x_axis_type="datetime",
        title=f"{title} - Rule: {getattr(rule, 'name', rule)}"
    )
    p.add_layout(Title(text="(Fast Mode: Datashader+Bokeh)", align="center", text_font_size="10pt"), 'above')

    # Convert Datashader image to RGBA and plot as image_rgba
    bokeh_img = tf.dynspread(img, threshold=0.5, max_px=4)

    # Bokeh's image_rgba expects coordinates in data units: x, y, dw, dh
    x_span = (df['index'].min().value, df['index'].max().value)
    y_span = (df['Low'].min(), df['High'].max())
    p.image_rgba(
        image=[bokeh_img.to_pil()],
        x=x_span[0],
        y=y_span[0],
        dw=x_span[1] - x_span[0],
        dh=y_span[1] - y_span[0]
    )

    # Save to HTML
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_file(output_path, title=title)
    save(p)