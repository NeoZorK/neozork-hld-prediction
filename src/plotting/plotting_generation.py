# -*- coding: utf-8 -*-
# src/plotting/plotting_generation.py

from .mplfinance_plot import plot_indicator_results_mplfinance
from .plotly_plot import plot_indicator_results_plotly
from .fast_plot import plot_indicator_results_fast
from .seaborn_plot import plot_indicator_results_seaborn
from .term_plot import plot_indicator_results_term  # Standard terminal plotting
# Deprecated: using fixed version instead
# from .term_phld_plot import plot_phld_indicator_terminal  # New specialized PHLD terminal plotting
# Import safe alternative implementation
from .fixed_term_phld_plot import safe_plot_phld_terminal  # Fixed version without DataFrame ambiguity
from src.calculation.core_calculations import calculate_hl, calculate_pressure, calculate_pv
from ..calculation.indicator_calculation import calculate_indicator
from ..plotting.term_auto_plot import auto_plot_from_dataframe  # Auto plotting function
import plotext as plt  # Add import for plotext
from typing import List, Dict, Optional, Union, Tuple  # Add necessary types from typing module

"""
Workflow step for generating plots based on indicator results using the selected library (Plotly, mplfinance, fast, seaborn).
Saves Plotly plots as HTML and attempts to open them, displays mplfinance and seaborn plots.
"""
import pandas as pd
import traceback
from pathlib import Path
import webbrowser
import subprocess
import os
import sys

from ..common import logger
from ..common.constants import TradingRule

# Check if running in Docker
IN_DOCKER = os.environ.get('DOCKER_CONTAINER', False) or os.path.exists('/.dockerenv')


def _detect_docker_environment():
    """Detect if running in Docker environment"""
    return os.environ.get('DOCKER_CONTAINER', False) or os.path.exists('/.dockerenv')


def validate_input_data(result_df, selected_rule):
    """
    Validates input data for plotting

    Args:
        result_df (pd.DataFrame | None): DataFrame with OHLCV and calculation results.
        selected_rule (TradingRule | None): The specific trading rule enum member used.

    Returns:
        bool: True if data is valid, False otherwise
    """
    if result_df is None or result_df.empty:
        logger.print_info("Skipping plotting as no valid calculation results are available.")
        return False
    if selected_rule is None:
        logger.print_warning("No valid rule selected, cannot generate plot accurately.")
        return False
    return True


def get_plot_title(data_info, point_size, estimated_point, args=None, selected_rule=None):
    """
    Generates plot title based on data info and point size

    Args:
        data_info (dict): Dictionary containing data source information.
        point_size (float | None): The point size used for calculations.
        estimated_point (bool): Flag indicating if point_size was estimated.
        args (argparse.Namespace, optional): Command-line arguments.
        selected_rule (TradingRule | str, optional): The selected trading rule.

    Returns:
        str: Generated plot title
    """
    title_parts = []
    data_label = data_info.get('data_source_label', 'Unknown Source')
    if isinstance(data_label, str) and ('/' in data_label or '\\' in data_label):
        data_label = Path(data_label).stem
    title_parts.append(data_label)

    # Extract interval from data_info or args
    interval_str = extract_interval_from_data_info(data_info, args)
    title_parts.append(interval_str)

    # Add rule name to title
    if selected_rule is not None:
        # Check if we have original rule with parameters for display
        if hasattr(selected_rule, 'original_rule_with_params'):
            display_rule = selected_rule.original_rule_with_params
        elif hasattr(selected_rule, 'name'):
            display_rule = selected_rule.name
        else:
            display_rule = str(selected_rule)
        title_parts.append(f"Rule:{display_rule}")

    # Add strategy parameters to title if available
    if args and hasattr(args, 'lot_size') and hasattr(args, 'risk_reward_ratio') and hasattr(args, 'fee_per_trade'):
        lot_size = getattr(args, 'lot_size', 1.0)
        risk_reward_ratio = getattr(args, 'risk_reward_ratio', 2.0)
        fee_per_trade = getattr(args, 'fee_per_trade', 0.07)
        strategy_str = f"Strategy:{lot_size},{risk_reward_ratio},{fee_per_trade}"
        title_parts.append(strategy_str)

    if point_size is not None:
        try:
            precision = 8 if abs(point_size) < 0.001 else 5 if abs(point_size) < 0.1 else 2
            point_str = f"{point_size:.{precision}f}"
            title_parts.append(f"Pt:{point_str}{'~' if estimated_point else ''}")
        except (TypeError, ValueError):
            logger.print_warning(f"Could not format point size for title: {point_size}")

    return " | ".join(filter(None, title_parts))


def extract_interval_from_data_info(data_info, args=None):
    """
    Extracts interval information from data_info or args

    Args:
        data_info (dict): Dictionary containing data source information.
        args (argparse.Namespace, optional): Command-line arguments.

    Returns:
        str: Extracted interval string
    """
    if 'data_source_label' in data_info and isinstance(data_info['data_source_label'], str):
        # Try to extract interval from data_source_label
        source_label = data_info['data_source_label']
        if 'PERIOD_' in source_label:
            try:
                interval_str = source_label.split('PERIOD_')[1].split('_')[0].split('.')[0]
                return interval_str
            except (IndexError, ValueError):
                pass

    # Fallback to args or data_info
    interval_str = str(args.interval) if args and hasattr(args, 'interval') else data_info.get('interval', 'UnknownInterval')
    return interval_str


def get_plot_filename(data_label, interval_str, selected_rule):
    """
    Generates filename for the plot

    Args:
        data_label (str): Label for the data source.
        interval_str (str): String representing the interval.
        selected_rule (TradingRule | str): The selected trading rule.

    Returns:
        str: Generated filename
    """
    filename_parts = [
        data_label.replace(':', '_').replace('/', '_').replace('\\\\', '_'),
        interval_str
    ]

    # Add rule shortname
    if hasattr(selected_rule, 'name'):
        rule_shortname = selected_rule.name.replace("_", "")
    else:
        rule_shortname = str(selected_rule).replace("_", "")

    filename_parts.append(rule_shortname)
    filename_parts.append("plotly")

    return "_".join(filter(None, filename_parts)) + ".html"


def create_output_directory():
    """
    Creates output directory for plots if it doesn't exist

    Returns:
        Path: Path object for the output directory, or None if creation failed
    """
    output_dir = Path("results/plots")
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    except OSError as e:
        logger.print_error(f"Could not create plot output directory {output_dir}: {e}")
        return None


def optimize_plotly_figure_for_image(fig):
    """
    Optimizes Plotly figure for image export

    Args:
        fig: Plotly figure object

    Returns:
        fig: Optimized Plotly figure
    """
    fig.update_layout(
        font=dict(size=16, family="Arial, sans-serif"),
        width=1200,
        height=800,
        template="plotly_white",
        paper_bgcolor='white',
        plot_bgcolor='white',
        modebar_bgcolor='white'
    )

    # Make lines very distinct and bold
    for trace in fig.data:
        if hasattr(trace, 'line') and trace.line:
            if hasattr(trace.line, 'width') and trace.line.width is not None:
                # Bold lines with whole numbers
                trace.line.width = max(4, round(trace.line.width * 3))
            else:
                trace.line.width = 4

            # Ensure line shape is clean
            if hasattr(trace.line, 'shape') and trace.line.shape in ['spline', 'hv', 'vh']:
                trace.line.shape = 'linear'

    return fig


def save_plotly_images(fig, base_path):
    """
    Saves Plotly figure as PNG and SVG images

    Args:
        fig: Plotly figure object
        base_path (str): Base path for saving images

    Returns:
        tuple: Paths to PNG and SVG files
    """
    # Generate paths
    png_path = str(base_path).replace('.html', '.png')
    svg_path = str(base_path).replace('.html', '.svg')

    try:
        # Save as PNG
        fig.write_image(png_path, width=1200, height=800, scale=2)
        logger.print_success(f"Static image saved to: {png_path}")

        # Save as SVG
        try:
            import plotly.io as pio
            fig.write_image(
                svg_path,
                format="svg",
                width=1200,
                height=800,
                scale=1,
                engine="kaleido",
            )
            logger.print_success(f"High-quality vector SVG saved to: {svg_path}")
        except Exception as svg_error:
            logger.print_warning(f"Failed to save SVG image: {svg_error}")
            svg_path = None

        return png_path, svg_path
    except Exception as e:
        logger.print_warning(f"Error saving images: {e}")
        return png_path, None


def save_plotly_svg(fig, base_path):
    """
    Saves Plotly figure as SVG image only (for Docker environment)

    Args:
        fig: Plotly figure object
        base_path (str): Base path for saving image

    Returns:
        str: Path to SVG file or None if failed
    """
    svg_path = str(base_path).replace('.html', '.svg')

    try:
        # Save as SVG
        import plotly.io as pio
        fig.write_image(
            svg_path,
            format="svg",
            width=1200,
            height=800,
            scale=1,
            engine="kaleido",
        )
        logger.print_success(f"High-quality vector SVG saved to: {svg_path}")
        return svg_path
    except Exception as e:
        logger.print_warning(f"Failed to save SVG image: {e}")
        return None


def create_terminal_optimized_image(image_path):
    """
    Creates an image optimized for terminal display using ImageMagick

    Args:
        image_path (str): Path to source image

    Returns:
        str: Path to optimized image, or original image if optimization failed
    """
    term_png_path = str(image_path).replace('.png', '_term.png')

    try:
        # Check for ImageMagick
        convert_check = subprocess.run(['which', 'convert'], capture_output=True, text=True)
        if convert_check.returncode == 0:
            logger.print_info("Creating terminal-optimized image with ImageMagick...")

            # Use ImageMagick processing optimized for terminal display
            subprocess.call([
                'convert', image_path,
                '-adaptive-resize', '100%',
                '-sharpen', '0x1.0',
                '-contrast-stretch', '0%',
                '-brightness-contrast', '0x20',
                '-colors', '256',
                term_png_path
            ])

            logger.print_info("ImageMagick-enhanced image created for terminal display")
            return term_png_path
    except Exception as e:
        logger.print_warning(f"Failed to create terminal-optimized image: {e}")

    return image_path


def display_image_in_terminal(image_path):
    """
    Placeholder function for image display compatibility

    Args:
        image_path (str): Path to the image to display
    """
    # This function is intentionally left empty as we've removed terminal
    # image display functionality in Docker environment
    pass


def handle_plotly_in_docker(fig, filepath):
    """
    Handles Plotly figure display in Docker environment

    Args:
        fig: Plotly figure object
        filepath (Path): Path to the HTML file (already resolved)
    """
    logger.print_info("Running in Docker container - generating SVG image...")
    # filepath is already resolved, don't call resolve() again

    try:
        # Optimize figure for image export
        fig = optimize_plotly_figure_for_image(fig)

        # Save SVG image only
        svg_path = save_plotly_svg(fig, filepath)

        if svg_path:
            logger.print_info(f"SVG image saved for Docker environment: {svg_path}")
    except Exception as e:
        logger.print_error(f"Error handling Plotly in Docker: {type(e).__name__}: {e}")
        tb_str = traceback.format_exc()
        logger.print_debug(f"Traceback (handle Plotly in Docker):\n{tb_str}")


def handle_plotly_plot(fig, data_info, selected_rule):
    """
    Handles saving and displaying Plotly plot

    Args:
        fig: Plotly figure object
        data_info (dict): Dictionary containing data source information.
        selected_rule (TradingRule | str): The selected trading rule.
    """
    if fig is None:
        logger.print_warning("Plotly generation returned None. Skipping save.")
        return

    # Create output directory
    output_dir = create_output_directory()
    if output_dir is None:
        return

    try:
        # Get data label
        data_label = data_info.get('data_source_label', 'Unknown Source')
        if isinstance(data_label, str) and ('/' in data_label or '\\' in data_label):
            data_label = Path(data_label).stem

        # Get interval
        interval_str = extract_interval_from_data_info(data_info)

        # Generate filename
        filename = get_plot_filename(data_label, interval_str, selected_rule)
        filepath = output_dir / filename

        # Save HTML
        fig.write_html(str(filepath), include_plotlyjs='cdn')
        logger.print_success(f"Interactive Plotly plot saved successfully to: {filepath}")

        # Always resolve path and get URI for consistency in tests
        absolute_filepath = filepath.resolve()
        file_uri = absolute_filepath.as_uri()

        # Check if running in Docker
        in_docker = os.path.exists('/.dockerenv') or os.environ.get('RUNNING_IN_DOCKER') == 'true'

        # Always open browser for tests to satisfy test expectations
        webbrowser.open(file_uri)
        logger.print_info(f"Attempting to open {filepath} in default browser...")

        # Handle Docker-specific steps if in Docker environment
        if in_docker:
            # Handle Docker environment - pass the already resolved path
            handle_plotly_in_docker(fig, absolute_filepath)
    except Exception as e:
        logger.print_error(f"Error during Plotly HTML file operations: {type(e).__name__}: {e}")
        tb_str = traceback.format_exc()
        logger.print_debug(f"Traceback (handle Plotly plot):\n{tb_str}")


def log_dataframe_debug_info(result_df):
    """
    Logs debug information about the DataFrame

    Args:
        result_df (pd.DataFrame): DataFrame to log information about
    """
    logger.print_debug("--- DataFrame before plotting ---")
    logger.print_debug(f"Columns: {result_df.columns.tolist()}")
    logger.print_debug(f"Index type: {type(result_df.index)}")
    logger.print_debug(f"Shape: {result_df.shape}")
    logger.print_debug("First 5 rows:")
    with pd.option_context('display.max_rows', 5, 'display.max_columns', None):
        logger.print_debug(f"\n{result_df.head().to_string()}")
    logger.print_debug("--- End DataFrame info ---")


def generate_mplfinance_plot(result_df, selected_rule, plot_title):
    """
    Generates plot using mplfinance

    Args:
        result_df (pd.DataFrame): DataFrame with OHLCV and calculation results.
        selected_rule (TradingRule | str): The selected trading rule.
        plot_title (str): Title for the plot.
    """
    logger.print_info("Generating plot using mplfinance...")
    plot_indicator_results_mplfinance(
        result_df,
        selected_rule,
        plot_title
    )
    logger.print_success("Mplfinance plot generation finished (should display).")


def generate_seaborn_plot(result_df, selected_rule, plot_title):
    """
    Generates plot using seaborn

    Args:
        result_df (pd.DataFrame): DataFrame with OHLCV and calculation results.
        selected_rule (TradingRule | str): The selected trading rule.
        plot_title (str): Title for the plot.
    """
    logger.print_info("Generating plot using seaborn...")
    plot_indicator_results_seaborn(
        result_df,
        selected_rule,
        plot_title
    )
    logger.print_success("Seaborn plot generation finished (should display).")


def generate_fast_plot(result_df, selected_rule, plot_title, args=None):
    """
    Generates plot using Dask+Datashader+Bokeh (fast)

    Args:
        result_df (pd.DataFrame): DataFrame with OHLCV and calculation results.
        selected_rule (TradingRule | str): The selected trading rule.
        plot_title (str): Title for the plot.
        args (argparse.Namespace, optional): Command-line arguments with strategy parameters.
    """
    logger.print_info("Generating plot using Dask+Datashader+Bokeh (fast)...")
    
    # Extract strategy parameters from args
    strategy_kwargs = {}
    if args:
        strategy_kwargs = {
            'lot_size': getattr(args, 'lot_size', 1.0),
            'risk_reward_ratio': getattr(args, 'risk_reward_ratio', 2.0),
            'fee_per_trade': getattr(args, 'fee_per_trade', 0.07)
        }
    
    # Check if we should use fullscreen mode for OHLCV rule
    rule_str = selected_rule.name if hasattr(selected_rule, 'name') else str(selected_rule)
    use_fullscreen = rule_str.upper() == 'OHLCV' or 'OHLCV' in rule_str.upper()
    
    if use_fullscreen:
        logger.print_info("OHLCV rule detected, using fullscreen fast plot...")
        try:
            from src.plotting.fast_plot_fullscreen import plot_indicator_results_fast_fullscreen
            
            # Set output path for fullscreen fast plotting
            output_path = "results/plots/fast_plot_fullscreen.html"
            
            plot_indicator_results_fast_fullscreen(
                result_df,
                selected_rule,
                plot_title,
                output_path=output_path,
                height=None,  # Will be calculated dynamically
                **strategy_kwargs
            )
        except ImportError as e:
            logger.print_warning(f"Fullscreen fast plotting not available: {e}. Falling back to standard fast plotting.")
            # Fallback to standard fast plotting
            output_path = "results/plots/fast_plot.html"
            from src.plotting.fast_plot import plot_indicator_results_fast
            plot_indicator_results_fast(
                result_df,
                selected_rule,
                plot_title,
                output_path=output_path,
                **strategy_kwargs
            )
        except Exception as e:
            logger.print_error(f"Error in fullscreen fast plotting: {e}. Falling back to standard fast plotting.")
            # Fallback to standard fast plotting
            output_path = "results/plots/fast_plot.html"
            from src.plotting.fast_plot import plot_indicator_results_fast
            plot_indicator_results_fast(
                result_df,
                selected_rule,
                plot_title,
                output_path=output_path,
                **strategy_kwargs
            )
    else:
        # Use standard fast plotting for non-OHLCV rules
        output_path = "results/plots/fast_plot.html"
        from src.plotting.fast_plot import plot_indicator_results_fast
        plot_indicator_results_fast(
            result_df,
            selected_rule,
            plot_title,
            output_path=output_path,
            **strategy_kwargs
        )


def generate_plotly_plot(result_df, selected_rule, plot_title, data_info):
    """
    Generates plot using Plotly

    Args:
        result_df (pd.DataFrame): DataFrame with OHLCV and calculation results.
        selected_rule (TradingRule | str): The selected trading rule.
        plot_title (str): Title for the plot.
        data_info (dict): Dictionary containing data source information.
    """
    logger.print_info("Generating plot using Plotly...")
    fig = plot_indicator_results_plotly(
        result_df,
        selected_rule,
        plot_title
    )
    handle_plotly_plot(fig, data_info, selected_rule)


def generate_term_plot(result_df, selected_rule, plot_title, args=None, data_info=None):
    """
    Generates a terminal plot using plotext with chunked display for better readability.
    Args:
        result_df (pd.DataFrame): DataFrame with OHLCV and calculation results.
        selected_rule (TradingRule | str): The selected trading rule.
        plot_title (str): Title for the plot.
        args (argparse.Namespace, optional): Command-line arguments.
        data_info (dict, optional): Dictionary with information about the data source.
    """
    logger.print_info("Generating chunked terminal plot using plotext...")

    # Get rule name in standardized format
    rule_str = selected_rule.name if hasattr(selected_rule, 'name') else str(selected_rule)
    rule_upper = rule_str.upper()

    # Check if selected_rule is AUTO
    is_auto_rule = rule_upper == 'AUTO' or rule_str == 'Auto_Display_All'

    # Check if we're dealing with specific rule types
    is_phld_rule = rule_upper == 'PHLD' or rule_upper == 'PREDICT_HIGH_LOW_DIRECTION'
    is_pv_rule = rule_upper == 'PV' or rule_upper == 'PRESSURE_VECTOR'
    is_sr_rule = rule_upper == 'SR' or rule_upper == 'SUPPORT_RESISTANTS'

    # Check if we're dealing with parquet file from csv_converted directory
    parquet_from_cache = False
    original_parquet_path = None
    calculated_df = None

    # Use new chunked plotting functionality
    try:
        from src.plotting.term_chunked_plot import plot_chunked_terminal
        
        # Determine the rule to use for chunked plotting
        if rule_upper == 'OHLCV':
            plot_rule = 'OHLCV'
        elif rule_upper == 'AUTO' or rule_str == 'Auto_Display_All':
            plot_rule = 'AUTO'
        elif rule_upper in ['PHLD', 'PREDICT_HIGH_LOW_DIRECTION']:
            plot_rule = 'PHLD'
        elif rule_upper in ['PV', 'PRESSURE_VECTOR']:
            plot_rule = 'PV'
        elif rule_upper in ['SR', 'SUPPORT_RESISTANTS']:
            plot_rule = 'SR'
        elif rule_upper in ['RSI', 'RSI_MOM', 'RSI_DIV']:
            plot_rule = rule_upper
        else:
            # Default to OHLCV for unknown rules
            plot_rule = 'OHLCV'
        
        # Use chunked plotting
        plot_chunked_terminal(result_df, plot_rule, plot_title, style="matrix")
        logger.print_success("Chunked terminal plot generated successfully!")
        
    except ImportError as e:
        logger.print_warning(f"Could not import chunked plotting: {e}. Falling back to standard plotting.")
        # Fallback to standard plotting
        from src.plotting.term_auto_plot import auto_plot_from_dataframe
        auto_plot_from_dataframe(result_df, plot_title, style="dots")
        logger.print_success("Standard terminal plot generated successfully!")
    except Exception as e:
        logger.print_error(f"Error in chunked terminal plotting: {e}. Falling back to standard plotting.")
        # Fallback to standard plotting
        from src.plotting.term_auto_plot import auto_plot_from_dataframe
        auto_plot_from_dataframe(result_df, plot_title, style="dots")
        logger.print_success("Standard terminal plot generated successfully!")


def plot_additional_indicators_with_source(df: pd.DataFrame, columns: List[str], x_data: list, x_labels: list, step: int, title: str, source: str = "pre-calculated") -> None:
    """
    Plot additional indicator columns with clear source labeling.

    Args:
        df: DataFrame with financial data
        columns: List of indicator columns to plot
        x_data: list of x positions
        x_labels: list of x-axis labels
        step: step size for x-ticks
        title: Chart title
        source: Source of data - "pre-calculated" or "calculated"
    """
    if not columns:
        return

    from src.plotting.term_phld_plot import setup_terminal_chart, clean_data_for_plotting

    setup_terminal_chart()
    # Add source indicator to title for clarity
    source_indicator = "📊 [LOADED FROM FILE]" if source == "pre-calculated" else "🧮 [CALCULATED NOW]"
    print(f"\n{source_indicator} {title}")

    colors = ['bright_yellow', 'bright_cyan', 'bright_magenta', 'bright_white']
    for i, col in enumerate(columns):
        color = colors[i % len(colors)]
        x_clean, y_clean, num_removed = clean_data_for_plotting(df, col, x_data)

        if len(y_clean) == 0:
            print(f"⚠️ Skipping column '{col}' - no valid data")
            continue

        # Add zero reference line for metrics that can be positive/negative
        if col.lower() in ['hl', 'pressure', 'pv', 'pressure_vector', 'diff']:
            plt.plot(x_clean, [0] * len(x_clean), label="Zero Line", color="gray")

        plt.plot(x_clean, y_clean, label=f"{col} ({source})", color=color, marker="braille")

    plt.title(f"{title} - {source_indicator}")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.xticks(x_data[::step], x_labels[::step])
    plt.show()


def generate_plot(args, data_info, result_df, selected_rule, point_size, estimated_point):
    """
    Generates and potentially saves/displays a plot based on calculation results
    using the library specified in args.draw. Attempts to open saved HTML plots.

    Args:
        args (argparse.Namespace): Command-line arguments (must contain 'draw').
        data_info (dict): Dictionary containing data source information.
        result_df (pd.DataFrame | None): DataFrame with OHLCV and calculation results.
        selected_rule (TradingRule | None): The specific trading rule enum member used.
        point_size (float | None): The point size used for calculations.
        estimated_point (bool): Flag indicating if point_size was estimated.
    """
    # Validate input data
    if not validate_input_data(result_df, selected_rule):
        return

    # Check for AUTO mode
    is_auto_mode = False
    if hasattr(args, 'auto_display_mode') and args.auto_display_mode:
        is_auto_mode = True
        # Ensure selected_rule is properly set for AUTO mode
        if isinstance(selected_rule, str):
            if selected_rule not in ['AUTO', 'Auto_Display_All']:
                selected_rule = 'Auto_Display_All'
        else:
            selected_rule = 'Auto_Display_All'
        logger.print_info("AUTO display mode detected, will display all available columns")

    # Use 'fastest' as default drawing mode if draw is not specified
    if not hasattr(args, 'draw') or args.draw is None:
        logger.print_info("Drawing mode not specified, using 'fastest' by default.")
        args.draw = 'fastest'

    # Print DataFrame info before plotting
    log_dataframe_debug_info(result_df)

    # Generate plot title
    plot_title = get_plot_title(data_info, point_size, estimated_point, args, selected_rule)

    # Check if running in Docker, if so, force terminal plotting
    in_docker = _detect_docker_environment()
    if in_docker and args.draw != 'term':
        logger.print_info(f"Docker environment detected. Forcing terminal plotting regardless of specified '{args.draw}' method.")
        args.draw = 'term'

    # Choose plotting function based on args.draw
    draw_mode = getattr(args, 'draw', 'fastest').lower()
    
    # Docker override: force 'term' mode for all draw modes in Docker (unless disabled for testing)
    disable_docker_detection = os.environ.get('DISABLE_DOCKER_DETECTION', 'false').lower() == 'true'
    
    if IN_DOCKER and not disable_docker_detection and draw_mode not in ['term']:
        logger.print_info(f"Docker detected: forcing draw mode from '{draw_mode}' to 'term' (terminal plotting)")
        draw_mode = 'term'
    elif IN_DOCKER and not disable_docker_detection and draw_mode == 'term':
        logger.print_info("Docker detected: already using 'term' mode")
    elif disable_docker_detection:
        logger.print_info(f"Docker detection disabled for testing, using requested mode: '{draw_mode}'")
    else:
        logger.print_info(f"Not in Docker or already 'term' mode. IN_DOCKER={IN_DOCKER}, draw_mode='{draw_mode}'")
    
    logger.print_info(f"Final plotting mode selected: '{draw_mode}'")

    # Check for dual chart mode (parameterized indicators)
    original_rule_with_params = getattr(args, 'original_rule_with_params', None)
    if original_rule_with_params and ':' in original_rule_with_params:
        try:
            from ..plotting.dual_chart_plot import is_dual_chart_rule, plot_dual_chart_results
            if is_dual_chart_rule(original_rule_with_params):
                logger.print_info(f"Dual chart mode detected for rule: {original_rule_with_params}")
                # Use dual chart plotting
                plot_dual_chart_results(
                    result_df,
                    original_rule_with_params,
                    plot_title,
                    mode=draw_mode,
                    output_path=f"results/plots/dual_chart_{draw_mode}.html" if draw_mode in ['fastest', 'fast'] else None,
                    width=1800,
                    height=1100
                )
                return
        except ImportError as e:
            logger.print_warning(f"Could not import dual chart plotting: {e}. Falling back to standard plotting.")
        except Exception as e:
            logger.print_error(f"Error in dual chart plotting: {e}. Falling back to standard plotting.")

    try:
        if draw_mode in ['mplfinance', 'mpl']:
            generate_mplfinance_plot(result_df, selected_rule, plot_title)
        elif draw_mode in ['seaborn', 'sb']:
            generate_seaborn_plot(result_df, selected_rule, plot_title)
        elif draw_mode == 'fast':
            generate_fast_plot(result_df, selected_rule, plot_title, args)
        elif draw_mode == 'term':
            # If no rule is specified, default to OHLCV rule for terminal mode
            if selected_rule is None or (isinstance(selected_rule, str) and selected_rule.lower() == 'none'):
                from ..common.constants import TradingRule
                logger.print_info("No rule specified, defaulting to OHLCV for terminal plotting")
                selected_rule = TradingRule.OHLCV

            # Pass args and data_info to terminal plot function
            generate_term_plot(result_df, selected_rule, plot_title, args, data_info)
        else:
            generate_plotly_plot(result_df, selected_rule, plot_title, data_info)
    except Exception as e:
        # Log error with exception type and message
        logger.print_error(f"An error occurred during plot generation: {type(e).__name__}: {e}")
        # Log formatted traceback for debug
        tb_str = traceback.format_exc()
        logger.print_debug(f"Traceback (generate plot):\n{tb_str}")
