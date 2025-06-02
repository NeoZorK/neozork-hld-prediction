# -*- coding: utf-8 -*-
# src/plotting/plotting_generation.py

from .mplfinance_plot import plot_indicator_results_mplfinance
from .plotly_plot import plot_indicator_results_plotly
from .fast_plot import plot_indicator_results_fast
from .seaborn_plot import plot_indicator_results_seaborn

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

from ..common import logger
from ..common.constants import TradingRule


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


def get_plot_title(data_info, point_size, estimated_point, args=None):
    """
    Generates plot title based on data info and point size

    Args:
        data_info (dict): Dictionary containing data source information.
        point_size (float | None): The point size used for calculations.
        estimated_point (bool): Flag indicating if point_size was estimated.
        args (argparse.Namespace, optional): Command-line arguments.

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
    Displays an image in the terminal using chafa

    Args:
        image_path (str): Path to the image to display
    """
    try:
        # Check if chafa is available
        chafa_check = subprocess.run(['which', 'chafa'], capture_output=True, text=True)
        if chafa_check.returncode == 0:
            logger.print_info("Displaying image with terminal-optimized settings...")

            # Get terminal width
            term_width = subprocess.run(['tput', 'cols'], capture_output=True, text=True)
            try:
                width = int(term_width.stdout.strip()) - 2
            except Exception:
                width = 100

            subprocess.call(['chafa', '--size', f'{width}x50', '--colors', 'full', image_path])
        else:
            logger.print_info("Chafa not available, can't display image in terminal")
    except Exception as e:
        logger.print_warning(f"Failed to display image in terminal: {e}")


def handle_plotly_in_docker(fig, filepath):
    """
    Handles Plotly figure display in Docker environment

    Args:
        fig: Plotly figure object
        filepath (Path): Path to the HTML file
    """
    logger.print_info("Running in Docker container - generating static image...")
    absolute_filepath = filepath.resolve()

    try:
        # Optimize figure for image export
        fig = optimize_plotly_figure_for_image(fig)

        # Save images
        image_path, _ = save_plotly_images(fig, absolute_filepath)

        if image_path:
            # Create terminal-optimized image
            optimized_image = create_terminal_optimized_image(image_path)

            # Display in terminal
            display_image_in_terminal(optimized_image)
    except Exception as e:
        logger.print_error(f"Error handling Plotly in Docker: {type(e).__name__}: {e}")
        tb_str = traceback.format_exc()
        logger.print_debug(f"Traceback (handle Plotly in Docker):\n{tb_str}")
        # Try fallback display
        try:
            if 'image_path' in locals():
                display_image_in_terminal(image_path)
        except Exception as fallback_error:
            logger.print_warning(f"Fallback display also failed: {fallback_error}")


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

        # Check if running in Docker
        in_docker = os.path.exists('/.dockerenv') or os.environ.get('RUNNING_IN_DOCKER') == 'true'

        if not in_docker:
            # Open in browser if not in Docker
            absolute_filepath = filepath.resolve()
            file_uri = absolute_filepath.as_uri()
            webbrowser.open(file_uri)
            logger.print_info(f"Attempting to open {filepath} in default browser...")
        else:
            # Handle Docker environment
            handle_plotly_in_docker(fig, filepath)
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


def generate_fast_plot(result_df, selected_rule, plot_title):
    """
    Generates plot using Dask+Datashader+Bokeh (fast)

    Args:
        result_df (pd.DataFrame): DataFrame with OHLCV and calculation results.
        selected_rule (TradingRule | str): The selected trading rule.
        plot_title (str): Title for the plot.
    """
    logger.print_info("Generating plot using Dask+Datashader+Bokeh (fast)...")
    plot_indicator_results_fast(
        result_df,
        selected_rule,
        plot_title
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

    # Use 'fastest' as default drawing method if draw is not specified
    if not hasattr(args, 'draw') or args.draw is None:
        logger.print_info("Drawing method not specified, using 'fastest' by default.")
        args.draw = 'fastest'

    # Debug: Print DataFrame info before plotting
    log_dataframe_debug_info(result_df)

    # Generate plot title
    plot_title = get_plot_title(data_info, point_size, estimated_point, args)

    # Choose plotting function based on args.draw
    draw_mode = getattr(args, 'draw', 'fastest').lower()

    try:
        if draw_mode in ['mplfinance', 'mpl']:
            generate_mplfinance_plot(result_df, selected_rule, plot_title)
        elif draw_mode in ['seaborn', 'sb']:
            generate_seaborn_plot(result_df, selected_rule, plot_title)
        elif draw_mode == 'fast':
            generate_fast_plot(result_df, selected_rule, plot_title)
        else:
            generate_plotly_plot(result_df, selected_rule, plot_title, data_info)
    except Exception as e:
        # Log error with exception type and message
        logger.print_error(f"An error occurred during plot generation: {type(e).__name__}: {e}")
        # Log formatted traceback for debug
        tb_str = traceback.format_exc()
        logger.print_debug(f"Traceback (generate plot):\n{tb_str}")
