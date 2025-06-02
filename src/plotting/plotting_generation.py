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

                            # Increase DPI and size for better quality - optimized for Retina displays
                            fig.update_layout(
                                font=dict(size=18, family="Arial, sans-serif"),  # Larger font for better readability
                                width=3840,          # 4K resolution width
                                height=2160,         # 4K resolution height
                                template="plotly_white",  # Use a clean template for better visibility
                                # Improve SVG quality by enhancing overall rendering
                                paper_bgcolor='white',
                                plot_bgcolor='white',
                                modebar_bgcolor='white'
                            )

                            # Optimize for SVG export by cleaning up the data
                            # Make sure all lines have explicit, clean properties
                            for trace in fig.data:
                                if hasattr(trace, 'line') and trace.line:
                                    if hasattr(trace.line, 'width') and trace.line.width is not None:
                                        # Use clean integer values for SVG line widths when possible
                                        if trace.line.width < 1.5:
                                            trace.line.width = 3  # Increased minimum line width for clarity
                                        else:
                                            trace.line.width = round(trace.line.width * 2)  # Double line width
                                    else:
                                        trace.line.width = 3

                                    # Ensure line shape is clean for vector display
                                    if hasattr(trace.line, 'shape') and trace.line.shape in ['spline', 'hv', 'vh']:
                                        trace.line.shape = 'linear'  # Linear lines render best in SVG

                            # Save as PNG with ultra-high resolution for Retina displays
                            fig.write_image(image_path, width=3840, height=2160, scale=8)  # Scale 8x for ultra-high DPI
                            logger.print_success(f"Static image saved to: {image_path}")

                            # Create high-quality SVG
                            svg_path = str(absolute_filepath).replace('.html', '.svg')

                            # Fixed method for creating SVG (to_svg doesn't exist)
                            try:
                                # Use correct method for SVG export
                                import plotly.io as pio

                                # Configure SVG renderer for highest quality
                                pio.kaleido.scope.default_width = 3840
                                pio.kaleido.scope.default_height = 2160
                                pio.kaleido.scope.default_scale = 1

                                # Save SVG directly with optimal settings
                                fig.write_image(
                                    svg_path,
                                    format="svg",
                                    width=3840,
                                    height=2160,
                                    scale=1,  # For vector format scale=1 is optimal
                                    engine="kaleido",
                                )

                                logger.print_success(f"High-quality vector SVG saved to: {svg_path}")

                                # Check possibility to display SVG in terminal
                                import subprocess

                                # Check for rsvg-convert utility for converting SVG to terminal-friendly format
                                rsvg_check = subprocess.run(['which', 'rsvg-convert'], capture_output=True, text=True)
                                if rsvg_check.returncode == 0:
                                    logger.print_info("Converting SVG for high-DPI terminal display...")
                                    # Create temporary ultra-high-quality PNG from SVG specifically for Retina displays
                                    temp_png_path = svg_path + "_hires.png"
                                    # Use very high resolution for Retina displays with high DPI
                                    subprocess.call(['rsvg-convert', '-w', '3840', '-h', '2160', '-d', '300', '-p', '300',
                                                    '-o', temp_png_path, svg_path])

                                    # Now use this high-DPI PNG for terminal display
                                    image_path_for_terminal = temp_png_path
                                    logger.print_info(f"Using high-DPI converted SVG for terminal display")
                                else:
                                    # If rsvg-convert not available, use regular PNG
                                    image_path_for_terminal = image_path
                                    logger.print_info("SVG terminal display not available (install librsvg2-bin for better quality)")
                            except Exception as svg_error:
                                logger.print_warning(f"Error with direct SVG export: {svg_error}")
                                # Fallback option
                                try:
                                    fig.write_image(
                                        svg_path,
                                        format="svg",
                                        width=3840,
                                        height=2160,
                                        scale=1
                                    )
                                    logger.print_info(f"Vector SVG saved to: {svg_path} (fallback method)")
                                    image_path_for_terminal = image_path  # Use PNG for terminal
                                except Exception as e:
                                    logger.print_error(f"All SVG export methods failed: {e}")
                                    image_path_for_terminal = image_path  # Use PNG for terminal

                            # Display the image in terminal with enhanced settings for high-DPI displays
                            import subprocess

                            # Check for Docker environment
                            in_docker = os.environ.get('DOCKER_CONTAINER', False)

                            # Try chafa first with ultra-high quality settings for Retina displays
                            chafa_check = subprocess.run(['which', 'chafa'], capture_output=True, text=True)
                            if chafa_check.returncode == 0:
                                logger.print_info("Displaying image in terminal (ultra-high quality for Retina displays)...")
                                # Infer terminal size
                                term_width = subprocess.run(['tput', 'cols'], capture_output=True, text=True)
                                term_height = subprocess.run(['tput', 'lines'], capture_output=True, text=True)
                                try:
                                    # Get current terminal dimensions but make them a bit larger
                                    width = int(term_width.stdout.strip())
                                    height = int(term_height.stdout.strip()) - 5
                                except:
                                    width = 200  # Larger default width
                                    height = 100  # Larger default height

                                # Use enhanced settings for Retina/high-DPI displays
                                if in_docker:
                                    # For Docker with high-DPI optimization
                                    subprocess.call(['chafa', '--size', f'{width}x{height}',
                                                    '--colors', 'full', '--color-space', 'rgb',
                                                    '--dither', 'diffusion', '--dither-intensity', '1.0',
                                                    '--optimize', 'detail', '--scale', 'fit',
                                                    '--symbols', 'all', '--work', 'auto',
                                                    image_path_for_terminal])
                                else:
                                    # For native terminal
                                    subprocess.call(['chafa', '--size', f'{width}x{height}',
                                                    '--colors', 'full', '--color-space', 'rgb',
                                                    image_path_for_terminal])
                        except Exception as e:
                            logger.print_error(f"Error generating static image: {e}")
                except Exception as e:
                    logger.print_error(f"Error opening plot in browser: {e}")
            except Exception as e:
                logger.print_error(f"Error saving Plotly plot: {e}")
    except Exception as e:
        logger.print_error(f"Error generating plot: {e}")
        logger.print_debug(traceback.format_exc())
