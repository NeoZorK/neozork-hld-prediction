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

    # Columns to plot: all numeric columns except standard OHLCV and time-like columns
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    # Exclude standard OHLCV and time-like columns
    plot_cols = [c for c in numeric_cols if c.lower() not in ['timestamp', 'datetime', 'index', 'date', 'time']]
    if not plot_cols:
        # If no numeric columns left after exclusion, use all numeric columns
        plot_cols = numeric_cols
    if not plot_cols:
        raise ValueError("No numeric columns to plot in this parquet file.")
    n_panels = len(plot_cols)

    # Prepare subplot heights: make all panels (candlestick, auto, volume) visually balanced
    panel_height = 0.7  # Use the same height for all panels for visual consistency
    # Include an extra gap between the candlestick and the first auto panel
    extra_gap = 0.7 * 2  # Additional height for the gap between candlestick and first auto panel
    row_heights = [panel_height, extra_gap] + [panel_height] * (n_panels - 1) + [panel_height]  # candlestick + big gap + auto panels + volume panel
    total_height = int((2 + n_panels) * panel_height * height_per_panel * 1.2 + extra_gap * height_per_panel)

    # Create subplots: 1 - Candlestick, 2+ - auto columns, last - Volume
    fig = make_subplots(
        rows=2 + n_panels,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,  # Equal vertical spacing between all panels
        row_heights=row_heights,
        subplot_titles=[None] + plot_cols + ["Volume"]
    )

    # Candlestick chart (row 1)
    candle_kwargs = dict(
        x=df[time_col] if time_col is not None else df.index,
        open=df['Open'] if 'Open' in df.columns else None,
        high=df['High'] if 'High' in df.columns else None,
        low=df['Low'] if 'Low' in df.columns else None,
        close=df['Close'] if 'Close' in df.columns else None,
        name="Candlestick",
        increasing_line_color='#26a69a',
        decreasing_line_color='#ef5350',
        increasing_fillcolor='rgba(38,166,154,0.3)',
        decreasing_fillcolor='rgba(239,83,80,0.3)',
        whiskerwidth=0.5,
        showlegend=False
    )
    fig.add_trace(go.Candlestick(**candle_kwargs), row=1, col=1)

    # Add traces for each auto column (rows 2+)
    for i, col in enumerate(plot_cols):
        fig.add_trace(
            go.Scatter(
                x=df[time_col] if time_col is not None else df.index,
                y=df[col],
                mode='lines',
                name=col,
                line=dict(width=2)
            ),
            row=2 + i, col=1
        )
        col_min = df[col].min()
        col_max = df[col].max()
        padding = (col_max - col_min) * 0.05 if col_max > col_min else 1
        fig.update_yaxes(
            title_text=col,
            row=2 + i,
            col=1,
            tickformat=".5f",
            range=[col_min - padding, col_max + padding]
        )

    # Volume chart (last row)
    volume_row = 2 + n_panels
    if 'Volume' in df.columns and 'Close' in df.columns and 'Open' in df.columns:
        colors = [
            '#26a69a' if c >= o else '#ef5350'
            for c, o in zip(df['Close'], df['Open'])
        ]
        fig.add_trace(
            go.Bar(
                x=df[time_col] if time_col is not None else df.index,
                y=df['Volume'],
                name="Volume",
                marker_color=colors,
                opacity=0.85,
                showlegend=False
            ),
            row=volume_row, col=1
        )
        vol_max = df['Volume'].max() * 1.1
        fig.update_yaxes(title_text="Volume", row=volume_row, col=1, range=[0, vol_max])
    elif 'Volume' in df.columns:
        fig.add_trace(
            go.Bar(
                x=df[time_col] if time_col is not None else df.index,
                y=df['Volume'],
                name="Volume",
                marker_color='#bdbdbd',
                opacity=0.7,
                showlegend=False
            ),
            row=volume_row, col=1
        )
        vol_max = df['Volume'].max() * 1.1
        fig.update_yaxes(title_text="Volume", row=volume_row, col=1, range=[0, vol_max])
    else:
        fig.add_trace(
            go.Scatter(x=[], y=[]), row=volume_row, col=1
        )

    # X axis formatting: range slider only for the first panel, no labels for other panels
    for i in range(1, 2 + n_panels + 1):
        fig.update_xaxes(row=i, col=1, showticklabels=(i == 2 + n_panels))
    fig.update_xaxes(
        row=1, col=1,
        type='date',
        tickformat='%Y-%m-%d %H:%M',
        tickangle=0,
        title_text='',
        showgrid=True,
        rangeslider_visible=False,
        rangeselector=None
    )
    for i in range(2, 2 + n_panels + 1):
        fig.update_xaxes(
            row=i, col=1,
            type='date',
            tickformat='%Y-%m-%d %H:%M',
            tickangle=0,
            title_text='',
            showgrid=True,
            rangeslider_visible=False,
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
        height=max(1400, total_height),  # Dynamic height based on number of panels
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

