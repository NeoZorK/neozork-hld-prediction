#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualization Manager for Interactive System

This module handles all visualization operations including charts,
plots, and data visualization functionality.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import time
from tqdm import tqdm
import sys
import webbrowser
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio

class VisualizationManager:
    """Manages visualization operations and plotting functionality."""
    
    def __init__(self):
        """Initialize the visualization manager."""
        pass
    
    def run_visualization_analysis(self, system):
        """Run visualization analysis menu."""
        while True:
            system.menu_manager.print_visualization_menu()
            try:
                choice = input("Select option (0-6): ").strip()
            except EOFError:
                print("\n👋 Goodbye!")
                break
            
            # Handle exit commands
            if choice.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using NeoZorK HLD Prediction Interactive System!")
                print("   Goodbye!")
                break
            
            if choice == '0' or choice == '00':
                break
            elif choice == '1':
                print("⏳ Price Charts - Coming soon!")
            elif choice == '2':
                print("⏳ Feature Distribution Plots - Coming soon!")
            elif choice == '3':
                print("⏳ Correlation Heatmaps - Coming soon!")
            elif choice == '4':
                print("⏳ Time Series Plots - Coming soon!")
            elif choice == '5':
                print("⏳ Feature Importance Charts - Coming soon!")
            elif choice == '6':
                print("⏳ Export Visualizations - Coming soon!")
            else:
                print("❌ Invalid choice. Please select 0-6.")
            
            if choice not in ['0', '00']:
                if system.safe_input() is None:
                    break
    
    def create_statistics_plots(self, system, data=None):
        """Create comprehensive statistics plots for all fields with separate HTML files."""
        if data is None and system.current_data is not None:
            data = system.current_data.select_dtypes(include=['number'])
        
        if data is None or data.empty:
            print("❌ No numeric data available for plotting")
            return False
        
        try:
            # Create plots directory
            plots_dir = Path("results/plots/statistics")
            plots_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"📊 Creating individual HTML reports for {len(data.columns)} fields...")
            
            # Create progress bar for field analysis
            with tqdm(total=len(data.columns), desc="Generating field reports", 
                     unit="field", ncols=80, file=sys.stdout) as pbar:
                
                for col in data.columns:
                    try:
                        # Create individual HTML file for each field
                        self._create_field_html_report(data, col, plots_dir)
                        pbar.update(1)
                    except Exception as e:
                        pbar.write(f"❌ Error creating report for {col}: {e}")
                        pbar.update(1)
                        continue
            
            # Create summary HTML file
            self._create_summary_html_report(data, plots_dir)
            
            print(f"✅ Generated {len(data.columns) + 1} HTML reports:")
            print(f"   • {len(data.columns)} individual field reports")
            print(f"   • 1 summary report")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating statistics plots: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_field_html_report(self, data, field_name, plots_dir):
        """Create a comprehensive HTML report for a single field."""
        field_data = data[field_name].dropna()
        
        if len(field_data) == 0:
            return
        
        # Calculate comprehensive statistics
        stats = self._calculate_field_statistics(field_data)
        
        # Create plots using Plotly (faster than seaborn)
        plots = self._create_field_plots(field_data, field_name)
        
        # Generate HTML content
        html_content = self._generate_field_html_content(field_name, stats, plots)
        
        # Save HTML file
        html_file = plots_dir / f"{field_name}_analysis.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _calculate_field_statistics(self, field_data):
        """Calculate comprehensive statistics for a field."""
        stats = {
            'basic': {
                'count': len(field_data),
                'mean': field_data.mean(),
                'median': field_data.median(),
                'std': field_data.std(),
                'min': field_data.min(),
                'max': field_data.max(),
                'range': field_data.max() - field_data.min(),
                'q25': field_data.quantile(0.25),
                'q75': field_data.quantile(0.75),
                'iqr': field_data.quantile(0.75) - field_data.quantile(0.25),
                'cv': field_data.std() / field_data.mean() if field_data.mean() != 0 else 0
            },
            'distribution': {
                'skewness': field_data.skew(),
                'kurtosis': field_data.kurtosis(),
                'missing_count': field_data.isna().sum(),
                'missing_pct': (field_data.isna().sum() / len(field_data)) * 100
            },
            'outliers': self._detect_outliers(field_data)
        }
        
        return stats
    
    def _detect_outliers(self, field_data):
        """Detect outliers using multiple methods."""
        q25 = field_data.quantile(0.25)
        q75 = field_data.quantile(0.75)
        iqr = q75 - q25
        
        # IQR method
        lower_bound_iqr = q25 - 1.5 * iqr
        upper_bound_iqr = q75 + 1.5 * iqr
        outliers_iqr = field_data[(field_data < lower_bound_iqr) | (field_data > upper_bound_iqr)]
        
        # Z-score method
        z_scores = np.abs((field_data - field_data.mean()) / field_data.std())
        outliers_zscore = field_data[z_scores > 3]
        
        return {
            'iqr': {
                'count': len(outliers_iqr),
                'percentage': len(outliers_iqr) / len(field_data) * 100,
                'lower_bound': lower_bound_iqr,
                'upper_bound': upper_bound_iqr
            },
            'zscore': {
                'count': len(outliers_zscore),
                'percentage': len(outliers_zscore) / len(field_data) * 100
            }
        }
    
    def _create_field_plots(self, field_data, field_name):
        """Create comprehensive plots for a field using Plotly."""
        plots = {}
        
        try:
            # 1. Distribution plot (histogram + KDE)
            fig_dist = go.Figure()
            
            # Histogram
            fig_dist.add_trace(go.Histogram(
                x=field_data,
                nbinsx=min(50, len(field_data) // 10),
                name='Histogram',
                opacity=0.7,
                marker_color='lightblue'
            ))
            
            # KDE (simplified)
            x_range = np.linspace(field_data.min(), field_data.max(), 100)
            kde_values = self._simple_kde(field_data, x_range)
            fig_dist.add_trace(go.Scatter(
                x=x_range,
                y=kde_values,
                mode='lines',
                name='KDE',
                line=dict(color='red', width=2)
            ))
            
            fig_dist.update_layout(
                title=f'{field_name} Distribution',
                xaxis_title=field_name,
                yaxis_title='Frequency',
                showlegend=True,
                height=400
            )
            
            plots['distribution'] = fig_dist.to_html(full_html=False, include_plotlyjs=False)
            
            # 2. Box plot
            fig_box = go.Figure()
            fig_box.add_trace(go.Box(
                y=field_data,
                name=field_name,
                boxpoints='outliers',
                marker_color='lightgreen'
            ))
            
            fig_box.update_layout(
                title=f'{field_name} Box Plot',
                yaxis_title=field_name,
                height=400
            )
            
            plots['boxplot'] = fig_box.to_html(full_html=False, include_plotlyjs=False)
            
            # 3. Time series plot (if data has index)
            if hasattr(field_data, 'index') and len(field_data.index) > 1:
                fig_ts = go.Figure()
                fig_ts.add_trace(go.Scatter(
                    x=field_data.index,
                    y=field_data.values,
                    mode='lines',
                    name=field_name,
                    line=dict(color='blue', width=1)
                ))
                
                fig_ts.update_layout(
                    title=f'{field_name} Time Series',
                    xaxis_title='Time',
                    yaxis_title=field_name,
                    height=400
                )
                
                plots['timeseries'] = fig_ts.to_html(full_html=False, include_plotlyjs=False)
            
            # 4. Q-Q plot (simplified)
            fig_qq = go.Figure()
            
            # Calculate theoretical quantiles
            theoretical_quantiles = np.percentile(np.random.normal(0, 1, 10000), 
                                                np.linspace(0, 100, len(field_data)))
            actual_quantiles = np.sort(field_data)
            
            fig_qq.add_trace(go.Scatter(
                x=theoretical_quantiles,
                y=actual_quantiles,
                mode='markers',
                name='Q-Q Plot',
                marker=dict(color='purple', size=4)
            ))
            
            # Add diagonal line
            min_val = min(theoretical_quantiles.min(), actual_quantiles.min())
            max_val = max(theoretical_quantiles.max(), actual_quantiles.max())
            fig_qq.add_trace(go.Scatter(
                x=[min_val, max_val],
                y=[min_val, max_val],
                mode='lines',
                name='Normal Line',
                line=dict(color='red', dash='dash')
            ))
            
            fig_qq.update_layout(
                title=f'{field_name} Q-Q Plot',
                xaxis_title='Theoretical Quantiles',
                yaxis_title='Sample Quantiles',
                height=400
            )
            
            plots['qqplot'] = fig_qq.to_html(full_html=False, include_plotlyjs=False)
            
        except Exception as e:
            print(f"Warning: Could not create plots for {field_name}: {e}")
        
        return plots
    
    def _simple_kde(self, data, x_range):
        """Simple KDE implementation."""
        try:
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(data)
            return kde(x_range)
        except ImportError:
            # Fallback to simple histogram-based approximation
            hist, bins = np.histogram(data, bins=min(50, len(data) // 10))
            bin_centers = (bins[:-1] + bins[1:]) / 2
            return np.interp(x_range, bin_centers, hist)
    
    def _generate_field_html_content(self, field_name, stats, plots):
        """Generate comprehensive HTML content for a field."""
        # Get statistics
        basic = stats['basic']
        dist = stats['distribution']
        outliers = stats['outliers']
        
        # Generate interpretations
        interpretations = self._generate_interpretations(stats)
        
        # Create HTML content
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{field_name} Analysis - NeoZorK HLD Prediction</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 20px; 
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stats-card {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }}
        .stats-card h3 {{
            color: #007bff;
            margin-top: 0;
        }}
        .stat-item {{
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            padding: 5px 0;
            border-bottom: 1px solid #eee;
        }}
        .stat-label {{
            font-weight: bold;
            color: #555;
        }}
        .stat-value {{
            color: #333;
        }}
        .interpretation {{
            background-color: #e8f4f8;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .interpretation h3 {{
            color: #0c5460;
            margin-top: 0;
        }}
        .plot-container {{
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #fafafa;
        }}
        .plot-container h3 {{
            color: #333;
            margin-top: 0;
            margin-bottom: 15px;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        .alert {{
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        .alert-warning {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }}
        .alert-success {{
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 {field_name} Analysis</h1>
            <p>Comprehensive Statistical Analysis Report</p>
            <p>Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stats-card">
                <h3>📈 Basic Statistics</h3>
                <div class="stat-item">
                    <span class="stat-label">Count:</span>
                    <span class="stat-value">{basic['count']:,}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Mean:</span>
                    <span class="stat-value">{basic['mean']:.6f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Median:</span>
                    <span class="stat-value">{basic['median']:.6f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Standard Deviation:</span>
                    <span class="stat-value">{basic['std']:.6f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Range:</span>
                    <span class="stat-value">{basic['range']:.6f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">IQR:</span>
                    <span class="stat-value">{basic['iqr']:.6f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">CV:</span>
                    <span class="stat-value">{basic['cv']:.4f}</span>
                </div>
            </div>
            
            <div class="stats-card">
                <h3>📊 Distribution Properties</h3>
                <div class="stat-item">
                    <span class="stat-label">Skewness:</span>
                    <span class="stat-value">{dist['skewness']:.4f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Kurtosis:</span>
                    <span class="stat-value">{dist['kurtosis']:.4f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Missing Values:</span>
                    <span class="stat-value">{dist['missing_count']:,} ({dist['missing_pct']:.2f}%)</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Min:</span>
                    <span class="stat-value">{basic['min']:.6f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Max:</span>
                    <span class="stat-value">{basic['max']:.6f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Q25:</span>
                    <span class="stat-value">{basic['q25']:.6f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Q75:</span>
                    <span class="stat-value">{basic['q75']:.6f}</span>
                </div>
            </div>
            
            <div class="stats-card">
                <h3>🔍 Outlier Analysis</h3>
                <div class="stat-item">
                    <span class="stat-label">IQR Outliers:</span>
                    <span class="stat-value">{outliers['iqr']['count']:,} ({outliers['iqr']['percentage']:.2f}%)</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Z-Score Outliers:</span>
                    <span class="stat-value">{outliers['zscore']['count']:,} ({outliers['zscore']['percentage']:.2f}%)</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">IQR Lower Bound:</span>
                    <span class="stat-value">{outliers['iqr']['lower_bound']:.6f}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">IQR Upper Bound:</span>
                    <span class="stat-value">{outliers['iqr']['upper_bound']:.6f}</span>
                </div>
            </div>
        </div>
        
        <div class="interpretation">
            <h3>🎯 Statistical Interpretations</h3>
            {interpretations}
        </div>
        
        <div class="plot-container">
            <h3>📈 Distribution Analysis</h3>
            {plots.get('distribution', '<p>Plot not available</p>')}
        </div>
        
        <div class="plot-container">
            <h3>📦 Box Plot & Outliers</h3>
            {plots.get('boxplot', '<p>Plot not available</p>')}
        </div>
        
        {f'<div class="plot-container"><h3>📈 Time Series</h3>{plots.get("timeseries", "<p>Plot not available</p>")}</div>' if 'timeseries' in plots else ''}
        
        <div class="plot-container">
            <h3>📊 Q-Q Plot (Normality Check)</h3>
            {plots.get('qqplot', '<p>Plot not available</p>')}
        </div>
        
        <div class="timestamp">
            <p>Report generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>NeoZorK HLD Prediction System - Field Analysis</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html_content
    
    def _generate_interpretations(self, stats):
        """Generate statistical interpretations."""
        basic = stats['basic']
        dist = stats['distribution']
        outliers = stats['outliers']
        
        interpretations = []
        
        # Mean vs Median
        if abs(basic['mean'] - basic['median']) / basic['mean'] > 0.1:
            interpretations.append('<div class="alert alert-warning">⚠️ Mean differs from median → Data may be skewed or have outliers</div>')
        else:
            interpretations.append('<div class="alert alert-success">✅ Mean and median are similar → Data is well-centered</div>')
        
        # Skewness
        if abs(dist['skewness']) < 0.5:
            interpretations.append('<div class="alert alert-success">✅ Low skewness → Data is approximately symmetric</div>')
        elif dist['skewness'] > 0.5:
            interpretations.append('<div class="alert alert-warning">⚠️ Positive skewness → Right-tailed distribution</div>')
        else:
            interpretations.append('<div class="alert alert-warning">⚠️ Negative skewness → Left-tailed distribution</div>')
        
        # Kurtosis
        if abs(dist['kurtosis']) < 2:
            interpretations.append('<div class="alert alert-success">✅ Moderate kurtosis → Normal-like tails</div>')
        elif dist['kurtosis'] > 2:
            interpretations.append('<div class="alert alert-warning">⚠️ High kurtosis → Heavy tails, more outliers</div>')
        else:
            interpretations.append('<div class="alert alert-warning">⚠️ Low kurtosis → Light tails, fewer outliers</div>')
        
        # Coefficient of Variation
        if basic['cv'] > 1:
            interpretations.append('<div class="alert alert-warning">⚠️ High CV → High relative variability</div>')
        elif basic['cv'] < 0.1:
            interpretations.append('<div class="alert alert-success">✅ Low CV → Low relative variability</div>')
        else:
            interpretations.append('<div class="alert alert-success">✅ Moderate CV → Reasonable variability</div>')
        
        # Outliers
        max_outlier_pct = max(outliers['iqr']['percentage'], outliers['zscore']['percentage'])
        if max_outlier_pct > 5:
            interpretations.append('<div class="alert alert-warning">⚠️ High outlier percentage → Consider outlier treatment</div>')
        else:
            interpretations.append('<div class="alert alert-success">✅ Reasonable outlier percentage</div>')
        
        # Sample size
        if basic['count'] < 100:
            interpretations.append('<div class="alert alert-warning">⚠️ Small sample size → Consider collecting more data</div>')
        
        return '\n'.join(interpretations)
    
    def _create_summary_html_report(self, data, plots_dir):
        """Create a summary HTML report with overview of all fields."""
        # Calculate summary statistics for all fields
        summary_stats = data.describe()
        
        # Create correlation heatmap
        correlation_matrix = data.corr()
        
        # Create summary plots
        plots = {}
        
        # Correlation heatmap
        fig_corr = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmid=0
        ))
        
        fig_corr.update_layout(
            title='Correlation Heatmap',
            height=600,
            width=800
        )
        
        plots['correlation'] = fig_corr.to_html(full_html=False, include_plotlyjs=False)
        
        # Summary statistics plots
        fig_summary = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Mean Values', 'Standard Deviation', 'Min Values', 'Max Values'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Mean values
        fig_summary.add_trace(
            go.Bar(x=summary_stats.columns, y=summary_stats.loc['mean'], name='Mean'),
            row=1, col=1
        )
        
        # Standard deviation
        fig_summary.add_trace(
            go.Bar(x=summary_stats.columns, y=summary_stats.loc['std'], name='Std'),
            row=1, col=2
        )
        
        # Min values
        fig_summary.add_trace(
            go.Bar(x=summary_stats.columns, y=summary_stats.loc['min'], name='Min'),
            row=2, col=1
        )
        
        # Max values
        fig_summary.add_trace(
            go.Bar(x=summary_stats.columns, y=summary_stats.loc['max'], name='Max'),
            row=2, col=2
        )
        
        fig_summary.update_layout(height=800, title_text="Summary Statistics")
        plots['summary'] = fig_summary.to_html(full_html=False, include_plotlyjs=False)
        
        # Generate summary HTML
        # Create table rows for statistics
        table_rows = []
        for stat in summary_stats.index:
            row_cells = [f'<td>{stat}</td>']
            for col in summary_stats.columns:
                value = summary_stats.loc[stat, col]
                if pd.isna(value):
                    row_cells.append('<td>N/A</td>')
                else:
                    row_cells.append(f'<td>{value:.6f}</td>')
            table_rows.append(f'<tr>{"".join(row_cells)}</tr>')
        
        # Create field links
        field_links = []
        for col in data.columns:
            field_links.append(f'<a href="{col}_analysis.html" class="field-link">{col}</a>')
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Summary Analysis - NeoZorK HLD Prediction</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 20px; 
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }}
        .stats-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .stats-table th, .stats-table td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: right;
        }}
        .stats-table th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .plot-container {{
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #fafafa;
        }}
        .plot-container h3 {{
            color: #333;
            margin-top: 0;
            margin-bottom: 15px;
        }}
        .field-links {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            margin: 20px 0;
        }}
        .field-link {{
            padding: 10px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            text-align: center;
        }}
        .field-link:hover {{
            background-color: #0056b3;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Summary Analysis Report</h1>
            <p>Comprehensive Overview of All Fields</p>
            <p>Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <h2>📈 Summary Statistics</h2>
        <table class="stats-table">
            <tr>
                <th>Statistic</th>
                {''.join(f'<th>{col}</th>' for col in summary_stats.columns)}
            </tr>
            {''.join(table_rows)}
        </table>
        
        <h2>🔗 Individual Field Reports</h2>
        <div class="field-links">
            {''.join(field_links)}
        </div>
        
        <div class="plot-container">
            <h3>📊 Correlation Heatmap</h3>
            {plots.get('correlation', '<p>Plot not available</p>')}
        </div>
        
        <div class="plot-container">
            <h3>📈 Summary Statistics Overview</h3>
            {plots.get('summary', '<p>Plot not available</p>')}
        </div>
        
        <div class="timestamp">
            <p>Report generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>NeoZorK HLD Prediction System - Summary Analysis</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Save summary HTML
        summary_file = plots_dir / 'summary_analysis.html'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def show_plots_in_browser(self, system):
        """Show the summary HTML report in browser."""
        try:
            plots_dir = Path("results/plots/statistics")
            summary_file = plots_dir / 'summary_analysis.html'
            
            if not summary_file.exists():
                print("❌ Summary analysis file not found")
                return False
            
            # Try to open in Safari first, then fallback to default browser
            try:
                webbrowser.get('safari').open(f'file://{summary_file.absolute()}')
                print(f"✅ Summary report opened in Safari browser: {summary_file}")
            except:
                webbrowser.open(f'file://{summary_file.absolute()}')
                print(f"✅ Summary report opened in default browser: {summary_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error showing plots in browser: {e}")
            return False
