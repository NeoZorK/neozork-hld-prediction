import os
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import HoverTool, Span, Title, ColumnDataSource
import webbrowser

def plot_indicator_results_fast(
    df,
    rule,
    title='',
    output_path="results/plots/fast_plot.html",
    width=1800,
    height=1100,
    **kwargs
):
    """
    Draws a combined dashboard plot in fast mode using Bokeh:
    - Main panel: pseudo-candlesticks (OHLC bars), predicted high/low lines, predicted direction arrows, legend, interactive tooltips.
    - Subpanels: Volume, PV, HL, Pressure.
    - All panels are adaptive in size with right margin for scrollbar.
    - Opens plot in default browser after saving.
    """

    # Ensure index column exists and is datetime
    if 'index' not in df.columns:
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.copy()
            df['index'] = df.index
        else:
            raise ValueError("DataFrame must have datetime index or 'index' column.")
    df['index'] = pd.to_datetime(df['index'])

    # Calculate up/down direction for coloring bars
    df['direction'] = (df['Close'] >= df['Open'])
    inc = df['direction']
    dec = ~df['direction']

    width_ms = 12 * 60 * 60 * 1000  # Half a day in milliseconds for bar width

    # Prepare ColumnDataSource for interactive tooltips
    source = ColumnDataSource(df)

    # ======================= MAIN PANEL (PRICE & SIGNALS) =========================
    p_main = figure(
        width=width, height=int(height*0.48),
        x_axis_type="datetime", title=title,
        background_fill_color="#f5f7fa",
        sizing_mode="stretch_width",
        margin=(30, 80, 10, 60)  # (top, right, bottom, left)
    )
    p_main.yaxis.axis_label = "Price"

    # Draw pseudo-candlesticks (OHLC bars)
    ohlc_segment = p_main.segment(
        x0='index', y0='High', x1='index', y1='Low',
        color="black", line_width=1.5, source=source, legend_label="OHLC Bar"
    )

    # Add hover tool for interactive tooltips only for ohlc_segment
    hover = HoverTool(
        renderers=[ohlc_segment],
        tooltips=[
            ("Date", "@index{%F}"),
            ("Open", "@Open{0.5f}"),
            ("High", "@High{0.5f}"),
            ("Low", "@Low{0.5f}"),
            ("Close", "@Close{0.5f}"),
            ("PPrice1", "@PPrice1{0.5f}"),
            ("PPrice2", "@PPrice2{0.5f}"),
            ("Direction", "@Direction"),
            ("Pressure", "@Pressure{0.5f}"),
            ("PV", "@PV{0.5f}"),
            ("HL", "@HL{0.5f}"),
            ("Volume", "@Volume{0}")
        ],
        formatters={"@index": "datetime"},
        mode='vline'
    )
    p_main.add_tools(hover)

    # Open tick (left)
    p_main.segment(
        x0=df['index'] - pd.to_timedelta(width_ms // 2, unit='ms'),
        y0=df['Open'],
        x1=df['index'],
        y1=df['Open'],
        color=["green" if x else "red" for x in inc],
        line_width=3
    )
    # Close tick (right)
    p_main.segment(
        x0=df['index'],
        y0=df['Close'],
        x1=df['index'] + pd.to_timedelta(width_ms // 2, unit='ms'),
        y1=df['Close'],
        color=["green" if x else "red" for x in inc],
        line_width=3
    )

    # Predicted High / Low Lines
    if 'PPrice1' in df.columns:
        p_main.line('index', 'PPrice1', line_color='green', line_dash='dotted', line_width=2, legend_label="Predicted Low (PPrice1)", source=source)
    if 'PPrice2' in df.columns:
        p_main.line('index', 'PPrice2', line_color='red', line_dash='dotted', line_width=2, legend_label="Predicted High (PPrice2)", source=source)

    # Predicted Direction Arrows (triangle up/down)
    if 'Direction' in df.columns:
        # 1 = buy prediction (up, green), 2 = sell prediction (down, red)
        buy_idx = df['Direction'] == 1
        sell_idx = df['Direction'] == 2

        # Plot up arrows for predicted up
        p_main.triangle(
            x=df.loc[buy_idx, 'index'],
            y=df.loc[buy_idx, 'Low'] - (df['High'] - df['Low']).mean() * 0.08,
            size=16, color="lime", legend_label="Predicted UP", alpha=0.9
        )
        # Plot down arrows for predicted down
        p_main.inverted_triangle(
            x=df.loc[sell_idx, 'index'],
            y=df.loc[sell_idx, 'High'] + (df['High'] - df['Low']).mean() * 0.08,
            size=16, color="red", legend_label="Predicted DOWN", alpha=0.9
        )

    # Overlay legend
    p_main.legend.location = "top_left"
    p_main.legend.click_policy = "hide"
    p_main.legend.label_text_font_size = "13pt"

    # Add chart subtitle
    subtitle = Title(text="Fast Mode: OHLC bars, predicted lines/arrows, indicators", align="center", text_font_size="11pt")
    p_main.add_layout(subtitle, 'above')

    # ======================= VOLUME PANEL =========================
    p_vol = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa",
        sizing_mode="stretch_width", margin=(5, 80, 5, 60)
    )
    p_vol.yaxis.axis_label = "Volume"
    if 'Volume' in df.columns:
        p_vol.vbar(x='index', top='Volume', width=width_ms, color="#888888", alpha=0.55, legend_label="Volume", source=source)
        p_vol.legend.location = "top_left"
        p_vol.legend.label_text_font_size = "10pt"

    # ======================= PV PANEL =========================
    p_pv = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa",
        sizing_mode="stretch_width", margin=(5, 80, 5, 60)
    )
    p_pv.yaxis.axis_label = "PV"
    if 'PV' in df.columns:
        p_pv.line('index', 'PV', color="orange", line_width=2, legend_label="PV", source=source)
        zero = Span(location=0, dimension='width', line_color='gray', line_dash='dashed', line_width=1)
        p_pv.add_layout(zero)
        p_pv.legend.location = "top_left"
        p_pv.legend.label_text_font_size = "10pt"

    # ======================= HL PANEL =========================
    p_hl = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa",
        sizing_mode="stretch_width", margin=(5, 80, 5, 60)
    )
    p_hl.yaxis.axis_label = "HL (Points)"
    if 'HL' in df.columns:
        p_hl.line('index', 'HL', color="brown", line_width=2, legend_label="HL (Points)", source=source)
        p_hl.legend.location = "top_left"
        p_hl.legend.label_text_font_size = "10pt"

    # ======================= PRESSURE PANEL =========================
    p_pressure = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa",
        sizing_mode="stretch_width", margin=(5, 80, 10, 60)
    )
    p_pressure.yaxis.axis_label = "Pressure"
    if 'Pressure' in df.columns:
        p_pressure.line('index', 'Pressure', color="blue", line_width=2, legend_label="Pressure", source=source)
        zero2 = Span(location=0, dimension='width', line_color='gray', line_dash='dashed', line_width=1)
        p_pressure.add_layout(zero2)
        p_pressure.legend.location = "top_left"
        p_pressure.legend.label_text_font_size = "10pt"

    # ======================= COMBINE AND SAVE =========================
    layout = column(
        p_main,
        p_vol,
        p_pv,
        p_hl,
        p_pressure,
        sizing_mode="stretch_width"
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_file(output_path, title=title)
    save(layout)
    abs_path = os.path.abspath(output_path)
    webbrowser.open_new_tab(f"file://{abs_path}")