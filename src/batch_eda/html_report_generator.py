# -*- coding: utf-8 -*-
# src/batch_eda/html_report_generator.py
# HTML report generator for statistical analysis

import os
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime

class HTMLReport:
    """Class for generating HTML reports with plots and explanations"""

    def __init__(self, title, file_name):
        """Initialize HTML report with a title and file name"""
        self.title = title
        self.file_name = os.path.basename(file_name) if file_name else "Unknown"
        self.content = []
        self.plots = []
        self.css = """
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 25px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #2980b9;
                margin-top: 30px;
            }
            h3 {
                color: #3498db;
            }
            .plot-container {
                margin: 20px 0;
                text-align: center;
            }
            .plot-img {
                max-width: 100%;
                height: auto;
                margin-bottom: 10px;
            }
            .plot-description {
                background-color: #f8f9fa;
                padding: 15px;
                border-left: 4px solid #3498db;
                margin: 15px 0;
            }
            .interpretation {
                background-color: #e8f4f8;
                padding: 15px;
                border-left: 4px solid #2ecc71;
                margin: 15px 0;
            }
            .warning {
                background-color: #fff3cd;
                padding: 15px;
                border-left: 4px solid #f39c12;
                margin: 15px 0;
            }
            .recommendation {
                background-color: #d1ecf1;
                padding: 15px;
                border-left: 4px solid #17a2b8;
                margin: 15px 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #3498db;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .good {
                color: #27ae60;
            }
            .bad {
                color: #e74c3c;
            }
            .summary-box {
                background-color: #e8f4f8;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .timestamp {
                color: #7f8c8d;
                font-size: 0.9em;
                text-align: right;
                margin-top: 40px;
            }
            .nav-menu {
                background-color: #2c3e50;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .nav-menu a {
                color: white;
                margin-right: 15px;
                text-decoration: none;
                font-weight: bold;
            }
            .nav-menu a:hover {
                text-decoration: underline;
            }
        </style>
        """

    def add_header(self):
        """Add header section to the report"""
        header = f"""
        <div class="container">
            <h1>{self.title} - {self.file_name}</h1>
            <p>This report provides a detailed analysis of the data file with visualizations and recommendations.</p>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """
        self.content.append(header)

    def add_section(self, title, content):
        """Add a new section to the report"""
        section = f"""
        <div class="container">
            <h2>{title}</h2>
            {content}
        </div>
        """
        self.content.append(section)

    def add_plot(self, fig, title, description, interpretation=None, good=None, bad=None, recommendations=None):
        """
        Add a plot with description and interpretation

        Parameters:
        - fig: matplotlib figure object
        - title: Title of the plot
        - description: Description of what the plot shows
        - interpretation: How to interpret the plot
        - good: What would be considered good in this plot
        - bad: What would be considered bad in this plot
        - recommendations: Recommendations based on the plot
        """
        # Save plot to a base64 string
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')

        # Create the HTML for the plot and descriptions
        plot_html = f"""
        <div class="plot-container">
            <h3>{title}</h3>
            <img src="data:image/png;base64,{img_str}" class="plot-img" alt="{title}">
            <div class="plot-description">
                <p><strong>Description:</strong> {description}</p>
            </div>
        """

        if interpretation:
            plot_html += f"""
            <div class="interpretation">
                <p><strong>Interpretation:</strong> {interpretation}</p>
            </div>
            """

        if good:
            plot_html += f"""
            <div class="interpretation">
                <p><strong>What's Good:</strong> <span class="good">{good}</span></p>
            </div>
            """

        if bad:
            plot_html += f"""
            <div class="warning">
                <p><strong>What to Watch For:</strong> <span class="bad">{bad}</span></p>
            </div>
            """

        if recommendations:
            plot_html += f"""
            <div class="recommendation">
                <p><strong>Recommendations:</strong> {recommendations}</p>
            </div>
            """

        plot_html += "</div>"
        self.content.append(plot_html)
        plt.close(fig)  # Close the figure to free memory

    def add_table(self, df, title, description=None):
        """Add a DataFrame as an HTML table"""
        table_html = df.to_html(classes='dataframe', border=0)

        html = f"""
        <h3>{title}</h3>
        {f'<p>{description}</p>' if description else ''}
        {table_html}
        """
        self.content.append(html)

    def add_summary(self, summary_text):
        """Add a summary section"""
        summary = f"""
        <div class="summary-box">
            <h3>Summary</h3>
            {summary_text}
        </div>
        """
        self.content.append(summary)

    def add_navigation_menu(self, links):
        """Add a navigation menu with links to other reports"""
        menu_html = '<div class="nav-menu">'
        for text, link in links:
            menu_html += f'<a href="{link}">{text}</a>'
        menu_html += '</div>'
        self.content.append(menu_html)

    def save(self, output_path):
        """Save the HTML report to a file"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.title} - {self.file_name}</title>
            {self.css}
        </head>
        <body>
            {''.join(self.content)}
            <div class="timestamp">
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path


def ensure_report_directory(file_name):
    """
    Create directory structure for reports:
    ../results/reports/file_name/

    Parameters:
    - file_name: Name of the data file being analyzed

    Returns:
    - report_dir: Path to the directory for this file's reports
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    reports_dir = os.path.join(base_dir, 'results', 'reports')

    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Create file-specific directory
    file_base_name = os.path.basename(file_name).replace('.', '_')
    file_report_dir = os.path.join(reports_dir, file_base_name)

    if not os.path.exists(file_report_dir):
        os.makedirs(file_report_dir)

    return file_report_dir


def create_index_page(reports_map):
    """
    Create an index.html page that lists all reports by file

    Parameters:
    - reports_map: Dict mapping file names to their report directories

    Returns:
    - Path to the index.html file
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    reports_dir = os.path.join(base_dir, 'results', 'reports')
    index_path = os.path.join(reports_dir, 'index.html')

    # Generate HTML content
    css = """
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #2980b9;
            margin-top: 30px;
        }
        .file-list {
            margin-top: 20px;
        }
        .file-item {
            background-color: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #3498db;
        }
        .file-item h3 {
            margin-top: 0;
            color: #2c3e50;
        }
        .report-links {
            margin-left: 20px;
        }
        .report-links a {
            display: inline-block;
            margin-right: 15px;
            margin-bottom: 10px;
            padding: 8px 15px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .report-links a:hover {
            background-color: #2980b9;
        }
        .timestamp {
            color: #7f8c8d;
            font-size: 0.9em;
            text-align: right;
            margin-top: 40px;
        }
    </style>
    """

    # Begin HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Statistical Analysis Reports</title>
        {css}
    </head>
    <body>
        <div class="container">
            <h1>Statistical Analysis Reports</h1>
            <p>This page contains links to all generated statistical analysis reports.</p>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="file-list">
    """

    # Add entries for each file
    for file_name, file_data in reports_map.items():
        html_content += f"""
        <div class="file-item">
            <h3>{os.path.basename(file_name)}</h3>
            <div class="report-links">
        """

        # Add links to each report type
        for report_name, report_path in file_data['reports'].items():
            rel_path = os.path.relpath(report_path, reports_dir)
            html_content += f'<a href="{rel_path}">{report_name}</a>'

        html_content += """
            </div>
        </div>
        """

    # Close HTML
    html_content += """
            </div>
            <div class="timestamp">
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Write the file
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return index_path


def clean_all_reports():
    """Delete all report directories and files"""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    reports_dir = os.path.join(base_dir, 'results', 'reports')

    if os.path.exists(reports_dir):
        import shutil
        try:
            shutil.rmtree(reports_dir)
            return True, f"Removed reports directory: {reports_dir}"
        except Exception as e:
            return False, f"Error removing reports directory: {str(e)}"
    else:
        return True, "No reports directory found to clean"
