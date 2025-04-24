import os
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import (
    HoverTool, Span, Title, ColumnDataSource, NumeralTickFormatter, Div
)
import webbrowser


def get_dynamic_half_width(index):
    # Calculate dynamic bar half-width based on minimum difference between x values
    if len(index) < 2:
        return pd.Timedelta(milliseconds=18000000)  # fallback (5h)
    diffs = (index[1:] - index[:-1]).total_seconds()
    min_diff = min(diffs) if len(diffs) > 0 else 43200  # 12h in seconds fallback
    return pd.Timedelta(seconds=min_diff * 0.4)  # 40% of the minimal bar width


def get_unique_tooltips(df):
    # Define the fields you want to appear, in order, and filter out missing or duplicates
    preferred = [
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
    ]
    existing = set(df.columns) | {"index"}
    result = []
    seen = set()
    for label, expr in preferred:
        col = expr.split("{")[0][1:] if expr.startswith("@") else None
        if col and col in existing and label not in seen:
            result.append((label, expr))
            seen.add(label)
    return result


def plot_indicator_results_fast(
    df,
    rule,
    title='',
    output_path="results/plots/fast_plot.html",
    width=1800,
    height=1100,
    mode="fast",
    **kwargs
):
    """
    Draws fast mode dashboard plot using Bokeh.
    - Trading rule is displayed at the very top above the figure.
    - Main panel: OHLC bars, open/close ticks (with dynamic width!), open/close points, predicted high/low lines, direction arrows, legend, interactive tooltips.
    - Subpanels: Volume, PV, HL, Pressure - each with its own hover tooltip.
    - All panels are adaptive in size with right margin for scrollbar.
    - Opens plot in default browser after saving.
    """

    # Ensure the index column exists and is datetime type
    if 'index' not in df.columns:
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.copy()
            df['index'] = df.index
        else:
            raise ValueError("DataFrame must have datetime index or 'index' column.")
    df['index'] = pd.to_datetime(df['index'])

    # Compute direction for coloring bars
    df['direction'] = (df['Close'] >= df['Open'])
    inc = df['direction']
    dec = ~df['direction']

    # Dynamic bar width for open/close ticks
    index = df['index'].values
    if len(index) > 1:
        diffs = (df['index'][1:] - df['index'][:-1]).total_seconds()
        min_diff = min(diffs) if len(diffs) > 0 else 43200  # 12h fallback
        dynamic_half_width = pd.to_timedelta(min_diff * 0.4, unit='s')
    else:
        dynamic_half_width = pd.Timedelta(hours=6)
    # Prepare ColumnDataSource for interactive tooltips
    source = ColumnDataSource(df)

    # === TRADING RULE HEADER ===
    trading_rule_div = Div(
        text=f"<b style='font-size:18pt;color:#2e5cb8;text-align:center;display:block;'>Trading Rule: {rule}</b>",
        width=width, height=40
    )

    # === MAIN PANEL (PRICE & SIGNALS) ===
    p_main = figure(
        width=width, height=int(height*0.48),
        x_axis_type="datetime", title=title,
        background_fill_color="#f5f7fa",
        sizing_mode="stretch_width",
        margin=(10, 80, 10, 60)
    )
    p_main.yaxis.axis_label = "Price"
    p_main.yaxis.formatter = NumeralTickFormatter(format="0.00000")

    # Draw OHLC bar (vertical segment)
    ohlc_segment = p_main.segment(
        x0='index', y0='High', x1='index', y1='Low',
        color="black", line_width=1.5, source=source, legend_label="OHLC Bar"
    )

    # Draw open tick (left) - dynamic width
    p_main.segment(
        x0=df['index'] - dynamic_half_width,
        y0=df['Open'],
        x1=df['index'],
        y1=df['Open'],
        color=["green" if x else "red" for x in inc],
        line_width=3,
        legend_label="Open"
    )

    # Draw close tick (right) - dynamic width
    p_main.segment(
        x0=df['index'],
        y0=df['Close'],
        x1=df['index'] + dynamic_half_width,
        y1=df['Close'],
        color=["green" if x else "red" for x in inc],
        line_width=3,
        legend_label="Close"
    )

    # Draw open and close points as circles for clarity
    p_main.scatter(
        x='index',
        y='Open',
        marker="circle",
        size=7,
        color="green",
        source=source,
        alpha=0.7,
        legend_label="Open Point"
    )
    p_main.scatter(
        x='index',
        y='Close',
        marker="circle",
        size=7,
        color="red",
        source=source,
        alpha=0.7,
        legend_label="Close Point"
    )

    # Draw predicted high/low lines
    if 'PPrice1' in df.columns:
        p_main.line('index', 'PPrice1', line_color='green', line_dash='dotted', line_width=2, legend_label="Predicted Low (PPrice1)", source=source)
    if 'PPrice2' in df.columns:
        p_main.line('index', 'PPrice2', line_color='red', line_dash='dotted', line_width=2, legend_label="Predicted High (PPrice2)", source=source)

    # Draw predicted direction arrows
    if 'Direction' in df.columns:
        buy_idx = df['Direction'] == 1
        sell_idx = df['Direction'] == 2
        # Up arrows for predicted up
        p_main.scatter(
            x=df.loc[buy_idx, 'index'],
            y=df.loc[buy_idx, 'Low'] - (df['High'] - df['Low']).mean() * 0.08,
            size=16, color="lime", marker="triangle", legend_label="Predicted UP", alpha=0.9
        )
        # Down arrows for predicted down
        p_main.scatter(
            x=df.loc[sell_idx, 'index'],
            y=df.loc[sell_idx, 'High'] + (df['High'] - df['Low']).mean() * 0.08,
            size=16, color="red", marker="inverted_triangle", legend_label="Predicted DOWN", alpha=0.9
        )

    # Overlay legend
    p_main.legend.location = "top_left"
    p_main.legend.click_policy = "hide"
    p_main.legend.label_text_font_size = "13pt"

    # Add chart subtitle
    subtitle = Title(
        text="Fast Mode: OHLC bars, open/close points, predicted lines/arrows, indicators",
        align="center", text_font_size="11pt"
    )
    p_main.add_layout(subtitle, 'above')

    # Hover tool for main chart (unique tooltips only)
    unique_tooltips = get_unique_tooltips(df)
    hover_main = HoverTool(
        renderers=[ohlc_segment],
        tooltips=unique_tooltips,
        formatters={"@index": "datetime"},
        mode='vline'
    )
    p_main.add_tools(hover_main)

    # === VOLUME PANEL ===
    p_vol = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa",
        sizing_mode="stretch_width", margin=(5, 80, 5, 60)
    )
    p_vol.yaxis.axis_label = "Volume"
    vbar_vol = None
    if 'Volume' in df.columns:
        vbar_vol = p_vol.vbar(x='index', top='Volume', width=dynamic_half_width * 2, color="#888888", alpha=0.55, legend_label="Volume", source=source)
        p_vol.legend.location = "top_left"
        p_vol.legend.label_text_font_size = "10pt"
    if vbar_vol:
        hover_vol = HoverTool(
            renderers=[vbar_vol],
            tooltips=[("Date", "@index{%F}"), ("Volume", "@Volume{0}")],
            formatters={"@index": "datetime"},
            mode='vline'
        )
        p_vol.add_tools(hover_vol)

    # === PV PANEL ===
    p_pv = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa",
        sizing_mode="stretch_width", margin=(5, 80, 5, 60)
    )
    p_pv.yaxis.axis_label = "PV"
    p_pv.yaxis.formatter = NumeralTickFormatter(format="0.00000")
    line_pv = None
    if 'PV' in df.columns:
        line_pv = p_pv.line('index', 'PV', color="orange", line_width=2, legend_label="PV", source=source)
        zero = Span(location=0, dimension='width', line_color='gray', line_dash='dashed', line_width=1)
        p_pv.add_layout(zero)
        p_pv.legend.location = "top_left"
        p_pv.legend.label_text_font_size = "10pt"
    if line_pv:
        hover_pv = HoverTool(
            renderers=[line_pv],
            tooltips=[("Date", "@index{%F}"), ("PV", "@PV{0.5f}")],
            formatters={"@index": "datetime"},
            mode='vline'
        )
        p_pv.add_tools(hover_pv)

    # === HL PANEL ===
    p_hl = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa",
        sizing_mode="stretch_width", margin=(5, 80, 5, 60)
    )
    p_hl.yaxis.axis_label = "HL (Points)"
    p_hl.yaxis.formatter = NumeralTickFormatter(format="0.00000")
    line_hl = None
    if 'HL' in df.columns:
        line_hl = p_hl.line('index', 'HL', color="brown", line_width=2, legend_label="HL (Points)", source=source)
        p_hl.legend.location = "top_left"
        p_hl.legend.label_text_font_size = "10pt"
    if line_hl:
        hover_hl = HoverTool(
            renderers=[line_hl],
            tooltips=[("Date", "@index{%F}"), ("HL", "@HL{0.5f}")],
            formatters={"@index": "datetime"},
            mode='vline'
        )
        p_hl.add_tools(hover_hl)

    # === PRESSURE PANEL ===
    p_pressure = figure(
        width=width, height=int(height*0.13), x_axis_type="datetime",
        x_range=p_main.x_range, background_fill_color="#f5f7fa",
        sizing_mode="stretch_width", margin=(5, 80, 10, 60)
    )
    p_pressure.yaxis.axis_label = "Pressure"
    p_pressure.yaxis.formatter = NumeralTickFormatter(format="0.00000")
    line_pressure = None
    if 'Pressure' in df.columns:
        line_pressure = p_pressure.line('index', 'Pressure', color="blue", line_width=2, legend_label="Pressure", source=source)
        zero2 = Span(location=0, dimension='width', line_color='gray', line_dash='dashed', line_width=1)
        p_pressure.add_layout(zero2)
        p_pressure.legend.location = "top_left"
        p_pressure.legend.label_text_font_size = "10pt"
    if line_pressure:
        hover_pressure = HoverTool(
            renderers=[line_pressure],
            tooltips=[("Date", "@index{%F}"), ("Pressure", "@Pressure{0.5f}")],
            formatters={"@index": "datetime"},
            mode='vline'
        )
        p_pressure.add_tools(hover_pressure)

    # === COMBINE AND SAVE ===
    layout = column(
        trading_rule_div,
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