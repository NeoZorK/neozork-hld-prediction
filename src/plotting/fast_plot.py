import os
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import Legend, LegendItem, Span, Title
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
    Draws a combined dashboard plot in fast mode:
    - Main panel: pseudo-candlesticks (OHLC bars), predicted high/low lines, predicted direction arrows, legend.
    - Subpanels: Volume, PV, HL, Pressure.
    - Opens plot in default browser.
    """

    # Ensure index column
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

    width_ms = 12 * 60 * 60 * 1000  # half day in ms, for bar tick width

    # ======================= MAIN PANEL (PRICE & SIGNALS) =========================
    p_main = figure(
        width=width, height=int(height*0.48),
        x_axis_type="datetime", title=title,
        background_fill_color="#f5f7fa"
    )
    p_main.yaxis.axis_label = "Price"

    # Plot pseudo-candlesticks (OHLC bars)
    # High-low line (black)
    p_main.segment(df['index'], df['High'], df['index'], df['Low'], color="black", line_width=1.5, legend_label="OHLC Bar")
    # Open tick (left)
    p_main.segment(
        df['index'] - pd.to_timedelta(width_ms // 2, unit='ms'),
        df['Open'],
        df['index'],
        df['Open'],
        color=["green" if x else "red" for x in inc],
        line_width=3,
        legend_label=None
    )
    # Close tick (right)
    p_main.segment(
        df['index'],
        df['Close'],
        df['index'] + pd.to_timedelta(width_ms // 2, unit='ms'),
        df['Close'],
        color=["green" if x else "red" for x in inc],
        line_width=3,
        legend_label=None
    )

    # Predicted High / Low Lines
    if 'PPrice1' in df.columns:
        p_main.line(df['index'], df['PPrice1'], line_color='green', line_dash='dotted', line_width=2, legend_label="Predicted Low (PPrice1)")
    if 'PPrice2' in df.columns:
        p_main.line(df['index'], df['PPrice2'], line_color='red', line_dash='dotted', line_width=2, legend_label="Predicted High (PPrice2)")

    # Predicted Direction Arrows (triangle up/down)
    if 'Direction' in df.columns:
        # 1=buy prediction (up, green), 2=sell prediction (down, red)
        buy_idx = df['Direction'] == 1
        sell_idx = df['Direction'] == 2

        # Plot up arrows for predicted up
        p_main.triangle(
            x=df.loc[buy_idx, 'index'],
            y=df.loc[buy_idx, 'Low'] - (df['High'] - df['Low']).mean() * 0.08,
            size=16, color="lime", legend_label="Predicted UP", angle=0, alpha=0.9
        )
        # Plot down arrows for predicted down
        p_main.inverted_triangle(
            x=df.loc[sell_idx, 'index'],
            y=df.loc[sell_idx, 'High'] + (df['High'] - df['Low']).mean() * 0.08,
            size=16, color="red", legend_label="Predicted DOWN", angle=0, alpha=0.9
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
        x_range=p_main.x_range, background_fill_color="#f5f7fa"
    )
    p_vol.yaxis.axis_label = "Volume"
    if 'Volume' in df.columns:
        p_vol.vbar(x=df['index'], top=df['Volume'], width=width_ms, color="#888888", alpha=0.55, legend_label="Volume")
        p_vol.legend.location = "top_left"
        p_vol.legend.label_text_font_size = "10pt"

    # ======================= PV PANEL =========================
    p_pv = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa"
    )
    p_pv.yaxis.axis_label = "PV"
    if 'PV' in df.columns:
        p_pv.line(df['index'], df['PV'], color="orange", line_width=2, legend_label="PV")
        # Baseline
        zero = Span(location=0, dimension='width', line_color='gray', line_dash='dashed', line_width=1)
        p_pv.add_layout(zero)
        p_pv.legend.location = "top_left"
        p_pv.legend.label_text_font_size = "10pt"

    # ======================= HL PANEL =========================
    p_hl = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa"
    )
    p_hl.yaxis.axis_label = "HL (Points)"
    if 'HL' in df.columns:
        p_hl.line(df['index'], df['HL'], color="brown", line_width=2, legend_label="HL (Points)")
        p_hl.legend.location = "top_left"
        p_hl.legend.label_text_font_size = "10pt"

    # ======================= PRESSURE PANEL =========================
    p_pressure = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa"
    )
    p_pressure.yaxis.axis_label = "Pressure"
    if 'Pressure' in df.columns:
        p_pressure.line(df['index'], df['Pressure'], color="blue", line_width=2, legend_label="Pressure")
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
        sizing_mode="scale_width"
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_file(output_path, title=title)
    save(layout)
    abs_path = os.path.abspath(output_path)
    webbrowser.open_new_tab(f"file://{abs_path}")