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

from ..common import logger
from ..common.constants import TradingRule

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
    # --- Basic Validation ---
    if result_df is None or result_df.empty:
        logger.print_info("Skipping plotting as no valid calculation results are available.")
        return
    if selected_rule is None:
        logger.print_warning("No valid rule selected, cannot generate plot accurately.")
        return

    # --- Check for AUTO mode ---
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

    # --- DEBUG: Print DataFrame info before plotting ---
    logger.print_debug("--- DataFrame before plotting ---")
    logger.print_debug(f"Columns: {result_df.columns.tolist()}")
    logger.print_debug(f"Index type: {type(result_df.index)}")
    logger.print_debug(f"Shape: {result_df.shape}")
    logger.print_debug("First 5 rows:")
    with pd.option_context('display.max_rows', 5, 'display.max_columns', None):
        logger.print_debug(f"\n{result_df.head().to_string()}")
    logger.print_debug("--- End DataFrame info ---")

    # --- Construct Title ---
    title_parts = []
    data_label = data_info.get('data_source_label', 'Unknown Source')
    if isinstance(data_label, str) and ('/' in data_label or '\\' in data_label):
        data_label = Path(data_label).stem
    title_parts.append(data_label)

    # Extract interval from data_info or args
    if 'data_source_label' in data_info and isinstance(data_info['data_source_label'], str):
        # Try to extract interval from data_source_label
        source_label = data_info['data_source_label']
        if 'PERIOD_' in source_label:
            try:
                interval_str = source_label.split('PERIOD_')[1].split('_')[0].split('.')[0]
            except (IndexError, ValueError):
                # If extraction fails, fallback to args or data_info
                interval_str = str(args.interval) if hasattr(args, 'interval') else data_info.get('interval', 'UnknownInterval')
        else:
            interval_str = str(args.interval) if hasattr(args, 'interval') else data_info.get('interval', 'UnknownInterval')
    else:
        interval_str = str(args.interval) if hasattr(args, 'interval') else data_info.get('interval', 'UnknownInterval')

    title_parts.append(interval_str)
    if point_size is not None:
        try:
            precision = 8 if abs(point_size) < 0.001 else 5 if abs(point_size) < 0.1 else 2
            point_str = f"{point_size:.{precision}f}"
            title_parts.append(f"Pt:{point_str}{'~' if estimated_point else ''}")
        except (TypeError, ValueError):
            logger.print_warning(f"Could not format point size for title: {point_size}")
    plot_title = " | ".join(filter(None, title_parts))

    # --- Choose Plotting Function based on args.draw ---
    draw_mode = getattr(args, 'draw', 'fastest').lower()
    use_mplfinance = draw_mode in ['mplfinance', 'mpl']
    use_seaborn = draw_mode in ['seaborn', 'sb']

    try:
        if use_mplfinance:
            logger.print_info("Generating plot using mplfinance...")
            plot_indicator_results_mplfinance(
                result_df,
                selected_rule,
                plot_title
            )
            logger.print_success("Mplfinance plot generation finished (should display).")
        elif use_seaborn:
            logger.print_info("Generating plot using seaborn...")
            plot_indicator_results_seaborn(
                result_df,
                selected_rule,
                plot_title
            )
            logger.print_success("Seaborn plot generation finished (should display).")
        elif draw_mode == 'fast':
            logger.print_info("Generating plot using Dask+Datashader+Bokeh (fast)...")
            plot_indicator_results_fast(
                result_df,
                selected_rule,
                plot_title
            )
        else:
            logger.print_info("Generating plot using Plotly...")
            fig = plot_indicator_results_plotly(
                result_df,
                selected_rule,
                plot_title
            )
            if fig is None:
                logger.print_warning("Plotly generation returned None. Skipping save.")
                return
            # --- Save Plotly Plot as HTML ---
            output_dir = Path("results/plots")
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                logger.print_error(f"Could not create plot output directory {output_dir}: {e}")
                return
            # Construct filename
            filename_parts = [
                data_label.replace(':', '_').replace('/', '_').replace('\\\\', '_'),
                interval_str
            ]

            # Add point size if available
            if hasattr(selected_rule, 'name'):
                rule_shortname = selected_rule.name.replace("_", "")
            else:
                rule_shortname = str(selected_rule).replace("_", "")

            filename_parts.append(rule_shortname)
            filename_parts.append("plotly")

            filename = "_".join(filter(None, filename_parts)) + ".html"
            filepath = output_dir / filename
            try:
                fig.write_html(str(filepath), include_plotlyjs='cdn')
                logger.print_success(f"Interactive Plotly plot saved successfully to: {filepath}")
                try:
                    # Import webbrowser only if needed
                    import os

                    # Check if we are running in a Docker container
                    in_docker = os.path.exists('/.dockerenv') or os.environ.get('RUNNING_IN_DOCKER') == 'true'

                    if not in_docker:
                        # Only open in browser if not in Docker
                        absolute_filepath = filepath.resolve()
                        file_uri = absolute_filepath.as_uri()
                        webbrowser.open(file_uri)
                        logger.print_info(f"Attempting to open {filepath} in default browser...")
                    else:
                        logger.print_info(f"Running in Docker container - generating static image...")
                        # Full path for HTML file
                        absolute_filepath = filepath.resolve()

                        # Create PNG image from Plotly figure
                        try:
                            # Generate PNG image path
                            image_path = str(absolute_filepath).replace('.html', '.png')
                            logger.print_info(f"Generating PNG image directly with Plotly...")

                            # Increase DPI and size for better quality
                            fig.update_layout(
                                font=dict(size=14),  # Increase font size for better readability
                                width=1920,          # Setting width
                                height=1080,         # Setting height
                                template="plotly_white"  # Use a clean template for better visibility
                            )

                            # Make lines thicker for better visibility
                            for trace in fig.data:
                                if hasattr(trace, 'line') and trace.line:
                                    trace.line.width = trace.line.width * 1.5 if hasattr(trace.line, 'width') else 2

                            # Save the image with high resolution
                            fig.write_image(image_path, width=1920, height=1080, scale=4)
                            logger.print_success(f"Static image saved to: {image_path}")

                            # Additionally, save as SVG for vector graphics
                            svg_path = str(absolute_filepath).replace('.html', '.svg')
                            fig.write_image(svg_path, format="svg")
                            logger.print_info(f"Vector SVG image saved to: {svg_path}")

                            # Display the image in terminal if possible
                            import subprocess

                            # Check for Docker environment
                            in_docker = os.environ.get('DOCKER_CONTAINER', False)

                            # Try chafa first (best quality for Docker)
                            chafa_check = subprocess.run(['which', 'chafa'], capture_output=True, text=True)
                            if chafa_check.returncode == 0:
                                logger.print_info("Displaying image in terminal (high quality color view)...")
                                # Infer terminal size
                                term_width = subprocess.run(['tput', 'cols'], capture_output=True, text=True)
                                term_height = subprocess.run(['tput', 'lines'], capture_output=True, text=True)
                                try:
                                    width = int(term_width.stdout.strip()) - 5
                                    height = int(term_height.stdout.strip()) - 10
                                except:
                                    width = 180
                                    height = 90

                                # Use better settings for Docker
                                if in_docker:
                                    subprocess.call(['chafa', '--size', f'{width}x{height}',
                                                    '--colors', 'full', '--dither', 'diffusion',
                                                    '--dither-intensity', '0.7', '--optimize', 'quality',
                                                    image_path])
                                else:
                                    subprocess.call(['chafa', '--size', f'{width}x{height}',
                                                    '--colors', 'full', image_path])
                            # Try catimg second
                            elif catimg_check := subprocess.run(['which', 'catimg'], capture_output=True, text=True):
                                if catimg_check.returncode == 0:
                                    logger.print_info("Displaying image in terminal (color view)...")
                                    # Infer terminal width for catimg
                                    term_width = subprocess.run(['tput', 'cols'], capture_output=True, text=True)
                                    try:
                                        width = int(term_width.stdout.strip()) - 5
                                    except:
                                        width = 180

                                    # Use better settings for Docker
                                    if in_docker:
                                        # Higher resolution for Docker
                                        subprocess.call(['catimg', '-w', str(width), '-r', '2', '-c', image_path])
                                    else:
                                        subprocess.call(['catimg', '-w', str(width), image_path])
                                else:
                                    img_viewer_check = subprocess.run(['which', 'img2txt'], capture_output=True, text=True)
                                    if img_viewer_check.returncode == 0:
                                        logger.print_info("Displaying image in terminal (simplified view)...")
                                        # Enhanced parameters for img2txt in Docker
                                        if in_docker:
                                            subprocess.call(['img2txt', '-W', '180', '-H', '90', '--colors', '256',
                                                           '--gamma', '0.8', image_path])
                                        else:
                                            subprocess.call(['img2txt', '-W', '120', '-H', '60', '--colors', '16', image_path])
                                    else:
                                        logger.print_info("For better terminal image viewing, install one of these tools:")
                                        logger.print_info("  - apt-get install libcaca-utils (for img2txt)")
                                        logger.print_info("  - apt-get install catimg")
                                        logger.print_info("  - apt-get install chafa (recommended for Docker)")
                        except Exception as plotly_img_error:
                            logger.print_warning(f"Failed to generate direct image with Plotly: {plotly_img_error}")
                            logger.print_debug(f"Traceback (Plotly image):\n{traceback.format_exc()}")

                            # If Plotly image generation fails, try to open HTML in browser
                            logger.print_info("Falling back to HTML conversion...")
                            import subprocess
                except Exception as e_open:
                    logger.print_warning(
                        f"Could not automatically open the plot in browser: {type(e_open).__name__}: {e_open}")
                    logger.print_debug(f"Traceback (open plot):\n{traceback.format_exc()}")
            except Exception as e_save:
                logger.print_error(f"Failed to save Plotly plot to {filepath}: {type(e_save).__name__}: {e_save}")
                logger.print_debug(f"Traceback (save plot):\n{traceback.format_exc()}")
    except Exception as e_gen:
        logger.print_error(f"An error occurred during plot generation: {type(e_gen).__name__}: {e_gen}")
        logger.print_debug(f"Traceback (generate plot):\n{traceback.format_exc()}")

