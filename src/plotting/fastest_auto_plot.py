import os
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
import webbrowser


def plot_auto_fastest_parquet(parquet_path, output_html_path, trading_rule_name="AUTO", title="AUTO Fastest Plot", width=1800, height_per_panel=350):
    """
    Reads a parquet file and creates an HTML file with a vertically scrollable dashboard.
    For each column in the parquet file (except open, high, low, close, volume, timestamp/datetime),
    a separate plot is created. All charts share a common time axis at the bottom.
    The legend and trading rule name are displayed at the top, and all elements are arranged for clarity.
    """
    # Read parquet file
    df = pd.read_parquet(parquet_path)

    # Standard columns to exclude from auto plotting
    exclude_cols = {c.lower() for c in ['open', 'high', 'low', 'close', 'volume', 'timestamp', 'datetime', 'index', 'date', 'time']}

    # Find time column or use DatetimeIndex
    time_col = None
    for c in df.columns:
        if c.lower() in ['timestamp', 'datetime', 'index', 'date', 'time']:
            time_col = c
            break
    if time_col is None:
        if isinstance(df.index, pd.DatetimeIndex):
            time_col = None  # Will use df.index for plotting
        else:
            raise ValueError("No time column found in parquet file.")

    # Sort by time
    if time_col is not None:
        df = df.sort_values(time_col)
    else:
        df = df.sort_index()

    # Columns to plot (auto, excluding OHLCV/time columns)
    plot_cols = [c for c in df.columns if c.lower() not in exclude_cols and pd.api.types.is_numeric_dtype(df[c])]
    n_panels = len(plot_cols)
    if n_panels == 0:
        raise ValueError("No numeric columns to plot except standard OHLCV/time columns.")

    # Prepare subplot heights: more vertical space for each panel
    main_panel_height = 0.32
    volume_panel_height = 0.18
    auto_panel_height = 0.5 / n_panels if n_panels > 0 else 0.5
    row_heights = [main_panel_height, volume_panel_height] + [auto_panel_height] * n_panels
    total_height = max(900, int((main_panel_height + volume_panel_height + auto_panel_height * n_panels) * height_per_panel * 1.2))

    # Create subplots: 1 - Candlestick, 2 - Volume, 3+ - auto columns
    fig = make_subplots(
        rows=2 + n_panels,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,  # More vertical space between panels
        row_heights=row_heights,
        subplot_titles=[None, None] + plot_cols  # No title for candlestick/volume
    )

    # Candlestick chart (row 1)
    fig.add_trace(
        go.Candlestick(
            x=df[time_col] if time_col is not None else df.index,
            open=df['Open'] if 'Open' in df.columns else None,
            high=df['High'] if 'High' in df.columns else None,
            low=df['Low'] if 'Low' in df.columns else None,
            close=df['Close'] if 'Close' in df.columns else None,
            name="Candlestick",
            increasing_line_color='green',
            decreasing_line_color='red',
            showlegend=False
        ),
        row=1, col=1
    )

    # Volume chart (row 2) as bars, not candlestick
    if 'Volume' in df.columns:
        fig.add_trace(
            go.Bar(
                x=df[time_col] if time_col is not None else df.index,
                y=df['Volume'],
                name="Volume",
                marker_color='#7E7E7E',
                opacity=0.7,
                showlegend=False
            ),
            row=2, col=1
        )
        vol_max = df['Volume'].max() * 1.1
        fig.update_yaxes(title_text="Volume", row=2, col=1, range=[0, vol_max])
    else:
        fig.add_trace(
            go.Scatter(x=[], y=[]), row=2, col=1
        )

    # Add traces for each auto column (rows 3+)
    for i, col in enumerate(plot_cols):
        fig.add_trace(
            go.Scatter(
                x=df[time_col] if time_col is not None else df.index,
                y=df[col],
                mode='lines',
                name=col,
                line=dict(width=2)
            ),
            row=3 + i, col=1
        )
        col_min = df[col].min()
        col_max = df[col].max()
        padding = (col_max - col_min) * 0.05 if col_max > col_min else 1
        fig.update_yaxes(
            title_text=col,
            row=3 + i,
            col=1,
            tickformat=".5f",
            range=[col_min - padding, col_max + padding]
        )

    # X axis formatting: only on the last panel, no range selector, no 1w/1d buttons
    for i in range(1, 2 + n_panels):
        fig.update_xaxes(row=i, col=1, showticklabels=(i == 2 + n_panels - 1))
    fig.update_xaxes(
        row=2 + n_panels, col=1,
        type='date',
        tickformat='%Y-%m-%d %H:%M',
        tickangle=0,
        title_text='Time',
        showgrid=True,
        rangeslider_visible=True,
        rangeselector=None
    )

    # Layout and annotations: legend and auto mode text separated, more margin at top
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            y=0.97,
            font=dict(size=22, color="#2e5cb8")
        ),
        width=width,
        height=total_height,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.04,
            xanchor="center",
            x=0.5,
            font=dict(size=13)
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12
        ),
        margin=dict(t=160, b=40, l=60, r=40)  # More top margin for annotation spacing
    )
    # Auto mode annotation (top left, above chart, with more vertical offset)
    fig.add_annotation(
        text="AUTO Mode: Each numeric column (except OHLCV/time) is shown as a separate chart.",
        xref="paper", yref="paper",
        x=0.01, y=1.18,
        showarrow=False,
        font=dict(size=14),
        align="left",
        bordercolor="#2e5cb8",
        borderpad=4,
        bgcolor="#f5f7fa",
        opacity=0.95
    )
    # Trading rule annotation (top right, with more vertical offset)
    fig.add_annotation(
        text=f"Trading Rule: {trading_rule_name}",
        xref="paper", yref="paper",
        x=0.99, y=1.18,
        showarrow=False,
        font=dict(size=16, color="#2e5cb8"),
        align="right",
        bordercolor="#2e5cb8",
        borderpad=4,
        bgcolor="#f5f7fa",
        opacity=0.95
    )

    # Save and open HTML file in browser
    pio.write_html(fig, output_html_path, auto_open=False)
    abs_path = os.path.abspath(output_html_path)
    webbrowser.open_new_tab(f"file://{abs_path}")
    return fig

# Example usage (for integration with run_analysis.py):
# plot_auto_fastest_parquet('path/to/file.parquet', 'results/plots/auto_fastest.html')

