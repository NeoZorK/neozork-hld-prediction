#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualization Manager for Interactive System

This module handles all visualization operations including charts,
plots, and data visualization functionality.
"""

from pathlib import Path
from typing import Dict, Any


class VisualizationManager:
    """Manages visualization operations and plotting functionality."""
    
    def __init__(self):
        """Initialize the visualization manager."""
        pass
    
    def run_visualization_analysis(self, system):
        """Run visualization analysis menu."""
        print("\n📊 DATA VISUALIZATION")
        print("-" * 30)
        print("⏳ Visualization features coming soon!")
        print("   This will include interactive charts, plots, and export capabilities.")
        system.safe_input()
    
    def create_statistics_plots(self, system, data=None):
        """Create statistics plots for the given data."""
        if data is None and system.current_data is not None:
            data = system.current_data.select_dtypes(include=['number'])
        
        if data is None or data.empty:
            print("❌ No numeric data available for plotting")
            return False
        
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # Create plots directory
            plots_dir = Path("results/plots/statistics")
            plots_dir.mkdir(parents=True, exist_ok=True)
            
            # Set style
            plt.style.use('default')
            sns.set_palette("husl")
            
            # 1. Distribution plots
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Data Distributions', fontsize=16, fontweight='bold')
            
            for i, col in enumerate(data.columns[:4]):  # Plot first 4 columns
                row, col_idx = i // 2, i % 2
                sns.histplot(data[col].dropna(), kde=True, ax=axes[row, col_idx])
                axes[row, col_idx].set_title(f'{col} Distribution')
                axes[row, col_idx].set_xlabel(col)
                axes[row, col_idx].set_ylabel('Frequency')
            
            plt.tight_layout()
            plt.savefig(plots_dir / 'distributions.png', dpi=150, bbox_inches='tight')
            plt.close()
            
            # 2. Box plots
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Box Plots', fontsize=16, fontweight='bold')
            
            for i, col in enumerate(data.columns[:4]):
                row, col_idx = i // 2, i % 2
                sns.boxplot(y=data[col].dropna(), ax=axes[row, col_idx])
                axes[row, col_idx].set_title(f'{col} Box Plot')
                axes[row, col_idx].set_ylabel(col)
            
            plt.tight_layout()
            plt.savefig(plots_dir / 'boxplots.png', dpi=150, bbox_inches='tight')
            plt.close()
            
            # 3. Correlation heatmap
            if len(data.columns) > 1:
                plt.figure(figsize=(10, 8))
                correlation_matrix = data.corr()
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                           square=True, linewidths=0.5)
                plt.title('Correlation Heatmap', fontsize=16, fontweight='bold')
                plt.tight_layout()
                plt.savefig(plots_dir / 'correlation_heatmap.png', dpi=150, bbox_inches='tight')
                plt.close()
            
            # 4. Statistical summary
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Statistical Summary', fontsize=16, fontweight='bold')
            
            # Summary statistics
            summary_stats = data.describe()
            
            # Plot 1: Mean values
            axes[0, 0].bar(summary_stats.columns, summary_stats.loc['mean'])
            axes[0, 0].set_title('Mean Values')
            axes[0, 0].set_ylabel('Mean')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Plot 2: Standard deviation
            axes[0, 1].bar(summary_stats.columns, summary_stats.loc['std'])
            axes[0, 1].set_title('Standard Deviation')
            axes[0, 1].set_ylabel('Std')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Plot 3: Min values
            axes[1, 0].bar(summary_stats.columns, summary_stats.loc['min'])
            axes[1, 0].set_title('Minimum Values')
            axes[1, 0].set_ylabel('Min')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # Plot 4: Max values
            axes[1, 1].bar(summary_stats.columns, summary_stats.loc['max'])
            axes[1, 1].set_title('Maximum Values')
            axes[1, 1].set_ylabel('Max')
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig(plots_dir / 'statistical_summary.png', dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"✅ Statistics plots created in: {plots_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating statistics plots: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def show_plots_in_browser(self, system):
        """Show plots in browser."""
        try:
            import webbrowser
            import tempfile
            
            plots_dir = Path("results/plots/statistics")
            if not plots_dir.exists():
                print("❌ No plots directory found")
                return False
            
            # Create a comprehensive HTML file to display plots with detailed descriptions
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Statistics Plots - NeoZorK HLD Prediction</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 20px; 
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }
        .plot { 
            margin: 30px 0; 
            text-align: center; 
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #fafafa;
        }
        .plot h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 24px;
        }
        .plot-description {
            text-align: left;
            margin: 20px 0;
            padding: 15px;
            background-color: #e8f4f8;
            border-left: 4px solid #2196F3;
            border-radius: 5px;
        }
        .plot-description h3 {
            color: #1976D2;
            margin-top: 0;
        }
        .plot-description ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .plot-description li {
            margin: 5px 0;
        }
        img { 
            max-width: 100%; 
            height: auto; 
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .field-highlight {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .field-highlight strong {
            color: #856404;
        }
        .interpretation {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        .interpretation h4 {
            color: #0c5460;
            margin-top: 0;
        }
        .recommendations {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        .recommendations h4 {
            color: #155724;
            margin-top: 0;
        }
        .timestamp {
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Statistics Plots - NeoZorK HLD Prediction</h1>
            <p>Comprehensive Data Analysis and Visualization Report</p>
        </div>
"""
            
            # Define plot descriptions with detailed explanations
            plot_descriptions = {
                'distributions.png': {
                    'title': 'Distribution Analysis',
                    'description': 'Histograms with Kernel Density Estimation (KDE) showing the distribution of values for each field.',
                    'interpretation': {
                        'predicted_high': 'Shows the distribution of predicted high values. Look for normal distribution, skewness, and potential outliers.',
                        'predicted_low': 'Shows the distribution of predicted low values. Compare with predicted_high to understand prediction ranges.',
                        'pressure': 'Shows the distribution of pressure values. This indicates market pressure levels and their frequency.',
                        'pressure_vector': 'Shows the distribution of pressure vector values. This represents directional pressure strength.'
                    },
                    'what_to_look_for': [
                        'Normal distribution (bell-shaped curve)',
                        'Skewness (asymmetric distributions)',
                        'Outliers (extreme values)',
                        'Bimodal distributions (two peaks)',
                        'Gaps or unusual patterns'
                    ],
                    'recommendations': [
                        'If distributions are skewed, consider log transformations',
                        'If outliers are present, investigate their validity',
                        'For bimodal distributions, consider if data comes from different regimes',
                        'Check for data quality issues if distributions look unusual'
                    ]
                },
                'boxplots.png': {
                    'title': 'Outlier Detection (Box Plots)',
                    'description': 'Box plots showing the median, quartiles, and outliers for each field. Points outside the whiskers are considered outliers.',
                    'interpretation': {
                        'predicted_high': 'Outliers in predicted high may indicate extreme market conditions or prediction errors.',
                        'predicted_low': 'Outliers in predicted low may indicate extreme market conditions or prediction errors.',
                        'pressure': 'Outliers in pressure may indicate unusual market pressure events.',
                        'pressure_vector': 'Outliers in pressure vector may indicate extreme directional pressure.'
                    },
                    'what_to_look_for': [
                        'Outliers (points beyond whiskers)',
                        'Box symmetry (median position)',
                        'Whisker length (data spread)',
                        'Box height (interquartile range)',
                        'Overall data range'
                    ],
                    'recommendations': [
                        'Investigate outliers to determine if they are errors or valid extreme values',
                        'Consider outlier treatment methods (capping, removal, transformation)',
                        'Check for data quality issues if many outliers are present',
                        'Use robust statistics if outliers are valid but extreme'
                    ]
                },
                'correlation_heatmap.png': {
                    'title': 'Feature Relationships (Correlation Matrix)',
                    'description': 'Heatmap showing correlations between different fields. Red indicates positive correlation, blue indicates negative correlation.',
                    'interpretation': {
                        'predicted_high': 'Correlation with other fields shows which factors influence high predictions.',
                        'predicted_low': 'Correlation with other fields shows which factors influence low predictions.',
                        'pressure': 'Correlation shows how pressure relates to other market indicators.',
                        'pressure_vector': 'Correlation shows how directional pressure relates to other factors.'
                    },
                    'what_to_look_for': [
                        'Strong positive correlations (dark red)',
                        'Strong negative correlations (dark blue)',
                        'Weak correlations (light colors)',
                        'Correlation patterns between related fields',
                        'Unexpected correlations that need investigation'
                    ],
                    'recommendations': [
                        'Highly correlated features may be redundant for modeling',
                        'Negative correlations may indicate inverse relationships',
                        'Use correlation to understand feature relationships',
                        'Consider feature selection based on correlation patterns'
                    ]
                },
                'statistical_summary.png': {
                    'title': 'Statistical Summary Comparison',
                    'description': 'Bar charts comparing key statistical measures (mean, std, min, max) across all fields.',
                    'interpretation': {
                        'predicted_high': 'Compare mean and range with other fields to understand prediction scales.',
                        'predicted_low': 'Compare mean and range with other fields to understand prediction scales.',
                        'pressure': 'Compare pressure statistics with other market indicators.',
                        'pressure_vector': 'Compare pressure vector statistics with other directional indicators.'
                    },
                    'what_to_look_for': [
                        'Relative scales of different fields',
                        'Fields with high variability (large std)',
                        'Fields with extreme ranges (min to max)',
                        'Consistent patterns across related fields',
                        'Anomalous values that need investigation'
                    ],
                    'recommendations': [
                        'Consider feature scaling if scales vary greatly',
                        'Investigate fields with unusually high variability',
                        'Check for data quality issues in extreme ranges',
                        'Use appropriate scaling methods for machine learning'
                    ]
                }
            }
            
            plot_files = ['distributions.png', 'boxplots.png', 'correlation_heatmap.png', 'statistical_summary.png']
            
            for plot_file in plot_files:
                plot_path = plots_dir / plot_file
                if plot_path.exists():
                    desc = plot_descriptions.get(plot_file, {})
                    
                    html_content += f"""
        <div class="plot">
            <h2>{desc.get('title', plot_file.replace('.png', '').replace('_', ' ').title())}</h2>
            <img src="{plot_path}" alt="{plot_file}">
            
            <div class="plot-description">
                <h3>📋 Description</h3>
                <p>{desc.get('description', 'Statistical visualization showing data patterns and relationships.')}</p>
                
                <div class="field-highlight">
                    <strong>🎯 Key Fields Analysis:</strong>
                    <ul>
"""
                    
                    # Add field-specific interpretations
                    field_interpretations = desc.get('interpretation', {})
                    for field, interpretation in field_interpretations.items():
                        html_content += f"                        <li><strong>{field}:</strong> {interpretation}</li>\n"
                    
                    html_content += """
                    </ul>
                </div>
                
                <div class="interpretation">
                    <h4>🔍 What to Look For:</h4>
                    <ul>
"""
                    
                    for item in desc.get('what_to_look_for', []):
                        html_content += f"                        <li>{item}</li>\n"
                    
                    html_content += """
                    </ul>
                </div>
                
                <div class="recommendations">
                    <h4>💡 Recommendations:</h4>
                    <ul>
"""
                    
                    for item in desc.get('recommendations', []):
                        html_content += f"                        <li>{item}</li>\n"
                    
                    html_content += """
                    </ul>
                </div>
            </div>
        </div>
"""
            
            # Add timestamp
            import time
            html_content += f"""
        <div class="timestamp">
            <p>Report generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>NeoZorK HLD Prediction System - Interactive Analysis</p>
        </div>
    </div>
</body>
</html>
"""
            
            # Save HTML file
            html_path = plots_dir / 'plots_viewer.html'
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Open in Safari browser
            try:
                webbrowser.get('safari').open(f'file://{html_path.absolute()}')
                print(f"✅ Plots opened in Safari browser: {html_path}")
            except:
                # Fallback to default browser if Safari is not available
                webbrowser.open(f'file://{html_path.absolute()}')
                print(f"✅ Plots opened in default browser: {html_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error showing plots in browser: {e}")
            return False
