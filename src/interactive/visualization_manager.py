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
            
            # Create a simple HTML file to display plots
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Statistics Plots</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .plot { margin: 20px 0; text-align: center; }
        img { max-width: 100%; height: auto; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>Statistics Plots</h1>
"""
            
            plot_files = ['distributions.png', 'boxplots.png', 'correlation_heatmap.png', 'statistical_summary.png']
            for plot_file in plot_files:
                plot_path = plots_dir / plot_file
                if plot_path.exists():
                    html_content += f"""
    <div class="plot">
        <h2>{plot_file.replace('.png', '').replace('_', ' ').title()}</h2>
        <img src="{plot_path}" alt="{plot_file}">
    </div>
"""
            
            html_content += """
</body>
</html>
"""
            
            # Save HTML file
            html_path = plots_dir / 'plots_viewer.html'
            with open(html_path, 'w') as f:
                f.write(html_content)
            
            # Open in browser
            webbrowser.open(f'file://{html_path.absolute()}')
            print(f"✅ Plots opened in browser: {html_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error showing plots in browser: {e}")
            return False
