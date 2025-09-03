# -*- coding: utf-8 -*-
# src/interactive/html_report_generator.py
#!/usr/bin/env python3
"""
HTML report generation utilities for data visualization.
Handles creation of comprehensive HTML reports with plots and statistics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import os


class HTMLReportGenerator:
    """Handles generation of HTML reports for data analysis."""
    
    def __init__(self):
        """Initialize HTMLReportGenerator."""
        pass
    
    def generate_field_html_content(self, field_name: str, stats: Dict, plots: Dict) -> str:
        """
        Generate HTML content for a specific field.
        
        Args:
            field_name: Name of the field
            stats: Statistics for the field
            plots: Dictionary of plot file paths
            
        Returns:
            HTML content string
        """
        html_content = f"""
        <div class="field-section">
            <h3>📊 {field_name}</h3>
            
            <div class="stats-container">
                <h4>📈 Statistics</h4>
                <table class="stats-table">
                    <tr><td>Data Type:</td><td>{stats.get('data_type', 'Unknown')}</td></tr>
                    <tr><td>Total Values:</td><td>{stats.get('total_values', 0):,}</td></tr>
                    <tr><td>Missing Values:</td><td>{stats.get('missing_values', 0):,}</td></tr>
                    <tr><td>Missing Percentage:</td><td>{stats.get('missing_percentage', 0):.2f}%</td></tr>
        """
        
        # Add numeric-specific statistics
        if stats.get('data_type') in ['int64', 'float64']:
            html_content += f"""
                    <tr><td>Mean:</td><td>{stats.get('mean', 0):.4f}</td></tr>
                    <tr><td>Median:</td><td>{stats.get('median', 0):.4f}</td></tr>
                    <tr><td>Standard Deviation:</td><td>{stats.get('std', 0):.4f}</td></tr>
                    <tr><td>Minimum:</td><td>{stats.get('min', 0):.4f}</td></tr>
                    <tr><td>Maximum:</td><td>{stats.get('max', 0):.4f}</td></tr>
                    <tr><td>Range:</td><td>{stats.get('range', 0):.4f}</td></tr>
            """
        elif stats.get('data_type') == 'object':
            html_content += f"""
                    <tr><td>Unique Values:</td><td>{stats.get('unique_values', 0):,}</td></tr>
                    <tr><td>Most Common:</td><td>{stats.get('most_common', 'N/A')}</td></tr>
                    <tr><td>Most Common Count:</td><td>{stats.get('most_common_count', 0):,}</td></tr>
            """
        elif stats.get('data_type') == 'datetime64[ns]':
            html_content += f"""
                    <tr><td>Date Range:</td><td>{stats.get('date_range', 'N/A')}</td></tr>
                    <tr><td>Duration:</td><td>{stats.get('duration', 'N/A')}</td></tr>
            """
        
        html_content += """
                </table>
            </div>
        """
        
        # Add plots
        if plots:
            html_content += """
            <div class="plots-container">
                <h4>📊 Visualizations</h4>
                <div class="plots-grid">
            """
            
            for plot_type, plot_path in plots.items():
                if os.path.exists(plot_path):
                    html_content += f"""
                    <div class="plot-item">
                        <h5>{plot_type.replace('_', ' ').title()}</h5>
                        <img src="{plot_path}" alt="{plot_type}" class="plot-image">
                    </div>
                    """
            
            html_content += """
                </div>
            </div>
            """
        
        # Add interpretations
        interpretations = self._generate_interpretations(stats)
        if interpretations:
            html_content += f"""
            <div class="interpretations-container">
                <h4>💡 Insights</h4>
                <ul class="insights-list">
            """
            
            for insight in interpretations:
                html_content += f"<li>{insight}</li>"
            
            html_content += """
                </ul>
            </div>
            """
        
        html_content += """
        </div>
        """
        
        return html_content
    
    def _generate_interpretations(self, stats: Dict) -> List[str]:
        """
        Generate insights and interpretations from statistics.
        
        Args:
            stats: Statistics dictionary
            
        Returns:
            List of insight strings
        """
        insights = []
        
        try:
            # Missing values insights
            missing_pct = stats.get('missing_percentage', 0)
            if missing_pct > 20:
                insights.append("⚠️ High percentage of missing values - consider data quality investigation")
            elif missing_pct > 5:
                insights.append("⚠️ Moderate missing values - may need imputation strategies")
            elif missing_pct > 0:
                insights.append("✅ Low missing values - data quality is good")
            else:
                insights.append("✅ No missing values - excellent data completeness")
            
            # Numeric insights
            if stats.get('data_type') in ['int64', 'float64']:
                mean_val = stats.get('mean', 0)
                median_val = stats.get('median', 0)
                std_val = stats.get('std', 0)
                min_val = stats.get('min', 0)
                max_val = stats.get('max', 0)
                
                # Distribution insights
                if abs(mean_val - median_val) > std_val * 0.5:
                    insights.append("📊 Distribution appears skewed (mean ≠ median)")
                else:
                    insights.append("📊 Distribution appears relatively symmetric")
                
                # Outlier insights
                iqr = stats.get('q75', 0) - stats.get('q25', 0)
                if iqr > 0:
                    lower_bound = stats.get('q25', 0) - 1.5 * iqr
                    upper_bound = stats.get('q75', 0) + 1.5 * iqr
                    outliers = sum(1 for x in [min_val, max_val] if x < lower_bound or x > upper_bound)
                    if outliers > 0:
                        insights.append("🎯 Potential outliers detected using IQR method")
                    else:
                        insights.append("✅ No obvious outliers detected")
                
                # Range insights
                range_val = max_val - min_val
                if range_val > std_val * 10:
                    insights.append("📏 Large range suggests high variability in the data")
                elif range_val < std_val * 2:
                    insights.append("📏 Small range suggests low variability in the data")
            
            # Categorical insights
            elif stats.get('data_type') == 'object':
                unique_vals = stats.get('unique_values', 0)
                total_vals = stats.get('total_values', 0)
                
                if unique_vals == 1:
                    insights.append("🏷️ Single unique value - no variation in this field")
                elif unique_vals == total_vals:
                    insights.append("🏷️ All values are unique - high cardinality field")
                elif unique_vals < total_vals * 0.1:
                    insights.append("🏷️ Low cardinality - good for categorical analysis")
                else:
                    insights.append("🏷️ Moderate cardinality - consider grouping strategies")
            
            # Datetime insights
            elif stats.get('data_type') == 'datetime64[ns]':
                duration = stats.get('duration', 'N/A')
                if duration != 'N/A':
                    insights.append(f"⏱️ Time span: {duration}")
                
                # Check for gaps
                if stats.get('expected_frequency'):
                    insights.append(f"🔄 Expected frequency: {stats.get('expected_frequency')}")
            
        except Exception as e:
            insights.append(f"❌ Error generating insights: {e}")
        
        return insights
    
    def generate_summary_html_report(self, data: pd.DataFrame, plots_dir: str) -> str:
        """
        Generate comprehensive HTML report.
        
        Args:
            data: DataFrame with data
            plots_dir: Directory containing plots
            
        Returns:
            HTML report string
        """
        # Create plots directory if it doesn't exist
        Path(plots_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate overall statistics
        total_rows, total_cols = data.shape
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = data.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Calculate missing values
        missing_data = data.isnull().sum()
        total_missing = missing_data.sum()
        missing_percent = (total_missing / (total_rows * total_cols)) * 100
        
        # Generate HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Data Analysis Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    text-align: center;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                }}
                h3 {{
                    color: #2c3e50;
                    margin-top: 25px;
                }}
                h4 {{
                    color: #34495e;
                    margin-top: 20px;
                }}
                .summary-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .summary-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                }}
                .summary-card h3 {{
                    margin: 0 0 10px 0;
                    color: white;
                }}
                .summary-card .number {{
                    font-size: 2em;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .stats-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                }}
                .stats-table td {{
                    padding: 8px 12px;
                    border-bottom: 1px solid #ddd;
                }}
                .stats-table td:first-child {{
                    font-weight: bold;
                    color: #2c3e50;
                    width: 40%;
                }}
                .plots-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin: 15px 0;
                }}
                .plot-item {{
                    text-align: center;
                    padding: 15px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    background-color: #f9f9f9;
                }}
                .plot-image {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 5px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .field-section {{
                    margin: 30px 0;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    background-color: #fafafa;
                }}
                .insights-list {{
                    background-color: #e8f4fd;
                    padding: 15px;
                    border-radius: 5px;
                    border-left: 4px solid #3498db;
                }}
                .insights-list li {{
                    margin: 8px 0;
                }}
                .timestamp {{
                    text-align: center;
                    color: #7f8c8d;
                    font-style: italic;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Data Analysis Report</h1>
                
                <h2>📋 Dataset Overview</h2>
                <div class="summary-grid">
                    <div class="summary-card">
                        <h3>📁 Total Rows</h3>
                        <div class="number">{total_rows:,}</div>
                    </div>
                    <div class="summary-card">
                        <h3>📊 Total Columns</h3>
                        <div class="number">{total_cols}</div>
                    </div>
                    <div class="summary-card">
                        <h3>⚠️ Missing Values</h3>
                        <div class="number">{total_missing:,}</div>
                        <div>({missing_percent:.1f}%)</div>
                    </div>
                    <div class="summary-card">
                        <h3>💾 Memory Usage</h3>
                        <div class="number">{data.memory_usage(deep=True).sum() / 1024**2:.1f} MB</div>
                    </div>
                </div>
                
                <h2>🔍 Data Types Distribution</h2>
                <div class="summary-grid">
                    <div class="summary-card">
                        <h3>📈 Numeric Columns</h3>
                        <div class="number">{len(numeric_cols)}</div>
                    </div>
                    <div class="summary-card">
                        <h3>🏷️ Categorical Columns</h3>
                        <div class="number">{len(categorical_cols)}</div>
                    </div>
                    <div class="summary-card">
                        <h3>⏱️ Datetime Columns</h3>
                        <div class="number">{len(datetime_cols)}</div>
                    </div>
                </div>
        """
        
        # Add overall plots
        if numeric_cols:
            html_content += f"""
                <h2>📊 Overall Visualizations</h2>
                <div class="plots-grid">
            """
            
            # Add correlation heatmap if multiple numeric columns
            if len(numeric_cols) > 1:
                html_content += """
                    <div class="plot-item">
                        <h4>Correlation Heatmap</h4>
                        <img src="../plots/correlation_heatmap.png" alt="Correlation Heatmap" class="plot-image">
                    </div>
                """
            
            # Add missing values plot
            html_content += """
                <div class="plot-item">
                    <h4>Missing Values</h4>
                    <img src="../plots/missing_values.png" alt="Missing Values" class="plot-image">
                </div>
            """
            
            # Add data types plot
            html_content += """
                <div class="plot-item">
                    <h4>Data Types Distribution</h4>
                    <img src="../plots/data_types.png" alt="Data Types" class="plot-image">
                </div>
            """
            
            # Add summary statistics plot
            html_content += """
                <div class="plot-item">
                    <h4>Summary Statistics</h4>
                    <img src="../plots/summary_statistics.png" alt="Summary Statistics" class="plot-image">
                </div>
            """
            
            # Add outlier analysis plot
            html_content += """
                <div class="plot-item">
                    <h4>Outlier Analysis</h4>
                    <img src="../plots/outlier_analysis.png" alt="Outlier Analysis" class="plot-image">
                </div>
            """
            
            html_content += """
                </div>
            """
        
        # Add field-by-field analysis
        html_content += """
                <h2>🔬 Field-by-Field Analysis</h2>
        """
        
        # Analyze each field
        for col in data.columns:
            field_data = data[col]
            
            # Calculate field statistics
            stats = self._calculate_field_statistics(field_data)
            
            # Generate field plots (this would be done by PlotGenerator)
            # For now, we'll just reference the plots directory
            plots = {}  # This would be populated by PlotGenerator
            
            # Generate field HTML content
            field_html = self.generate_field_html_content(col, stats, plots)
            html_content += field_html
        
        # Add timestamp
        html_content += f"""
                <div class="timestamp">
                    Report generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _calculate_field_statistics(self, field_data: pd.Series) -> Dict:
        """
        Calculate comprehensive statistics for a field.
        
        Args:
            field_data: Series data for the field
            
        Returns:
            Dictionary with field statistics
        """
        stats = {}
        
        try:
            # Basic statistics
            stats['data_type'] = str(field_data.dtype)
            stats['total_values'] = len(field_data)
            stats['missing_values'] = field_data.isnull().sum()
            stats['missing_percentage'] = (stats['missing_values'] / stats['total_values']) * 100
            
            # Clean data for further analysis
            clean_data = field_data.dropna()
            
            if len(clean_data) == 0:
                return stats
            
            # Numeric statistics
            if pd.api.types.is_numeric_dtype(field_data):
                stats['mean'] = clean_data.mean()
                stats['median'] = clean_data.median()
                stats['std'] = clean_data.std()
                stats['min'] = clean_data.min()
                stats['max'] = clean_data.max()
                stats['range'] = stats['max'] - stats['min']
                stats['q25'] = clean_data.quantile(0.25)
                stats['q75'] = clean_data.quantile(0.75)
            
            # Categorical statistics
            elif pd.api.types.is_object_dtype(field_data) or pd.api.types.is_categorical_dtype(field_data):
                value_counts = clean_data.value_counts()
                stats['unique_values'] = len(value_counts)
                if len(value_counts) > 0:
                    stats['most_common'] = str(value_counts.index[0])
                    stats['most_common_count'] = value_counts.iloc[0]
            
            # Datetime statistics
            elif pd.api.types.is_datetime64_any_dtype(field_data):
                stats['date_range'] = f"{clean_data.min()} to {clean_data.max()}"
                duration = clean_data.max() - clean_data.min()
                stats['duration'] = str(duration)
                
                # Calculate expected frequency
                if len(clean_data) > 1:
                    time_diffs = clean_data.sort_values().diff().dropna()
                    if len(time_diffs) > 0:
                        median_diff = time_diffs.median()
                        stats['expected_frequency'] = self._format_timedelta(median_diff)
            
        except Exception as e:
            stats['error'] = str(e)
        
        return stats
    
    def _format_timedelta(self, td: pd.Timedelta) -> str:
        """Format timedelta to human-readable string."""
        try:
            if td <= pd.Timedelta(minutes=1):
                return f"{td.total_seconds():.0f}s"
            elif td <= pd.Timedelta(hours=1):
                return f"{td.total_seconds() / 60:.0f}m"
            elif td <= pd.Timedelta(days=1):
                return f"{td.total_seconds() / 3600:.0f}h"
            else:
                return f"{td.days}d"
        except:
            return str(td)
    
    def save_html_report(self, html_content: str, output_path: str) -> bool:
        """
        Save HTML report to file.
        
        Args:
            html_content: HTML content string
            output_path: Path to save the report
            
        Returns:
            bool: True if successful
        """
        try:
            # Create output directory if it doesn't exist
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save HTML file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ HTML report saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving HTML report: {e}")
            return False
