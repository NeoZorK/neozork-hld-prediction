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

    # Find time column
    time_col = None
    for c in df.columns:
        if c.lower() in ['timestamp', 'datetime', 'index', 'date', 'time']:
            time_col = c
            break
    if time_col is None:
        raise ValueError("No time column found in parquet file.")

    # Sort by time
    df = df.sort_values(time_col)

    # Columns to plot (auto)
    plot_cols = [c for c in df.columns if c.lower() not in exclude_cols and pd.api.types.is_numeric_dtype(df[c])]
    n_panels = len(plot_cols)
    if n_panels == 0:
        raise ValueError("No numeric columns to plot except standard OHLCV/time columns.")

    # Prepare subplot heights
    row_heights = [1.0 for _ in range(n_panels)]
    total_height = max(600, n_panels * height_per_panel)

    # Create subplots
    fig = make_subplots(
        rows=n_panels,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,  # Small vertical space between charts
        row_heights=[1.0/n_panels]*n_panels,  # Evenly distribute panel heights
        subplot_titles=plot_cols  # Titles for each subplot
    )

    # Add traces for each column
    for i, col in enumerate(plot_cols):
        fig.add_trace(
            go.Scatter(
                x=df[time_col],
                y=df[col],
                mode='lines',
                name=col,
                line=dict(width=2)
            ),
            row=i+1, col=1
        )
        # Y axis formatting for each subplot
        col_min = df[col].min()
        col_max = df[col].max()
        padding = (col_max - col_min) * 0.05 if col_max > col_min else 1
        fig.update_yaxes(
            title_text=col,
            row=i+1,
            col=1,
            tickformat=".5f",
            range=[col_min - padding, col_max + padding]
        )

    # X axis formatting (show only on the last panel)
    for i in range(1, n_panels):
        fig.update_xaxes(row=i, col=1, showticklabels=False)
    fig.update_xaxes(
        row=n_panels, col=1,
        type='date',
        tickformat='%Y-%m-%d %H:%M',
        tickangle=45,
        title_text='Time'
    )

    # Layout and annotations
    fig.update_layout(
        title=title,
        width=width,
        height=total_height,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.08,
            xanchor="center",
            x=0.5
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12
        ),
        margin=dict(t=120, b=40, l=60, r=40)
    )
    fig.add_annotation(
        text=f"Trading Rule: {trading_rule_name}",
        xref="paper", yref="paper",
        x=0.5, y=1.13,
        showarrow=False,
        font=dict(size=22, color="#2e5cb8"),
        align="center",
    )
    fig.add_annotation(
        text="AUTO Mode: Each numeric column (except OHLCV/time) is shown as a separate chart.",
        xref="paper", yref="paper",
        x=0.5, y=1.08,
        showarrow=False,
        font=dict(size=14),
        align="center",
    )

    # Save and open HTML file in browser
    pio.write_html(fig, output_html_path, auto_open=False)
    abs_path = os.path.abspath(output_html_path)
    webbrowser.open_new_tab(f"file://{abs_path}")
    return fig

# Example usage (for integration with run_analysis.py):
# plot_auto_fastest_parquet('path/to/file.parquet', 'results/plots/auto_fastest.html')

