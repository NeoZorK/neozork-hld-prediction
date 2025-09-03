# -*- coding: utf-8 -*-
# src/interactive/visualization_manager.py
#!/usr/bin/env python3
"""
Main visualization manager for interactive data visualization.
Coordinates plot generation and HTML report creation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import webbrowser
import os
from .plot_generator import PlotGenerator
from .html_report_generator import HTMLReportGenerator


class VisualizationManager:
    """Main visualization manager coordinating all visualization operations."""
    
    def __init__(self):
        """Initialize VisualizationManager."""
        self.plot_generator = PlotGenerator()
        self.html_generator = HTMLReportGenerator()
    
    def run_visualization_analysis(self, system):
        """
        Run comprehensive visualization analysis.
        
        Args:
            system: InteractiveSystem instance
        """
        print(f"\n📊 VISUALIZATION ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
        
        data = system.current_data
        print(f"📁 Starting visualization analysis for dataset: {data.shape[0]:,} rows × {data.shape[1]} columns")
        
        # Create plots directory
        plots_dir = "plots"
        Path(plots_dir).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created plots directory: {plots_dir}")
        
        # Generate overall plots
        print(f"\n1️⃣  GENERATING OVERALL PLOTS")
        overall_plots = self._generate_overall_plots(data, plots_dir)
        
        # Generate field-specific plots
        print(f"\n2️⃣  GENERATING FIELD-SPECIFIC PLOTS")
        field_plots = self._generate_field_plots(data, plots_dir)
        
        # Generate HTML report
        print(f"\n3️⃣  GENERATING HTML REPORT")
        html_report = self._generate_html_report(data, plots_dir, overall_plots, field_plots)
        
        # Show completion message
        print(f"\n✅ Visualization analysis completed!")
        print(f"   📊 Overall plots: {len(overall_plots)}")
        print(f"   🔬 Field plots: {sum(len(plots) for plots in field_plots.values())}")
        print(f"   📄 HTML report: {html_report}")
        
        # Ask if user wants to view plots
        try:
            view_plots = input("\nView plots in browser? (y/n, default: y): ").strip().lower()
            if view_plots in ['', 'y', 'yes']:
                self.show_plots_in_browser(system)
        except EOFError:
            print("⏭️  Skipping browser view...")
    
    def _generate_overall_plots(self, data: pd.DataFrame, plots_dir: str) -> Dict[str, str]:
        """
        Generate overall dataset plots.
        
        Args:
            data: DataFrame with data
            plots_dir: Directory to save plots
            
        Returns:
            Dictionary mapping plot types to file paths
        """
        plots = {}
        
        try:
            # Get numeric columns
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            # Correlation heatmap
            if len(numeric_cols) > 1:
                print(f"   🔗 Creating correlation heatmap...")
                heatmap_path = self.plot_generator.create_correlation_heatmap(data, numeric_cols)
                if heatmap_path:
                    plots['correlation_heatmap'] = heatmap_path
            
            # Missing values plot
            print(f"   ⚠️  Creating missing values plot...")
            missing_path = self.plot_generator.create_missing_values_plot(data)
            if missing_path:
                plots['missing_values'] = missing_path
            
            # Data types plot
            print(f"   🔍 Creating data types plot...")
            dtype_path = self.plot_generator.create_data_types_plot(data)
            if dtype_path:
                plots['data_types'] = dtype_path
            
            # Summary statistics plot
            if numeric_cols:
                print(f"   📈 Creating summary statistics plot...")
                summary_path = self.plot_generator.create_summary_statistics_plot(data, numeric_cols)
                if summary_path:
                    plots['summary_statistics'] = summary_path
            
            # Outlier analysis plot
            if numeric_cols:
                print(f"   🎯 Creating outlier analysis plot...")
                outlier_path = self.plot_generator.create_outlier_analysis_plot(data, numeric_cols)
                if outlier_path:
                    plots['outlier_analysis'] = outlier_path
            
        except Exception as e:
            print(f"   ❌ Error generating overall plots: {e}")
        
        return plots
    
    def _generate_field_plots(self, data: pd.DataFrame, plots_dir: str) -> Dict[str, Dict[str, str]]:
        """
        Generate plots for individual fields.
        
        Args:
            data: DataFrame with data
            plots_dir: Directory to save plots
            
        Returns:
            Dictionary mapping field names to plot dictionaries
        """
        field_plots = {}
        
        # Limit to first 10 columns to avoid overwhelming output
        columns_to_plot = data.columns[:10]
        
        print(f"   📊 Generating plots for {len(columns_to_plot)} fields...")
        
        for i, col in enumerate(columns_to_plot, 1):
            try:
                print(f"      [{i}/{len(columns_to_plot)}] Processing {col}...")
                
                field_data = data[col]
                plots = self.plot_generator.create_field_plots(field_data, col)
                
                if plots:
                    field_plots[col] = plots
                    print(f"         ✅ Generated {len(plots)} plots")
                else:
                    print(f"         ⚠️  No plots generated")
                
            except Exception as e:
                print(f"         ❌ Error processing {col}: {e}")
                continue
        
        return field_plots
    
    def _generate_html_report(self, data: pd.DataFrame, plots_dir: str, 
                            overall_plots: Dict[str, str], 
                            field_plots: Dict[str, Dict[str, str]]) -> str:
        """
        Generate comprehensive HTML report.
        
        Args:
            data: DataFrame with data
            plots_dir: Directory containing plots
            overall_plots: Overall dataset plots
            field_plots: Field-specific plots
            
        Returns:
            Path to generated HTML report
        """
        try:
            print(f"   📄 Generating HTML report...")
            
            # Generate HTML content
            html_content = self.html_generator.generate_summary_html_report(data, plots_dir)
            
            # Save HTML report
            report_path = f"{plots_dir}/data_analysis_report.html"
            success = self.html_generator.save_html_report(html_content, report_path)
            
            if success:
                print(f"   ✅ HTML report saved to: {report_path}")
                return report_path
            else:
                print(f"   ❌ Failed to save HTML report")
                return ""
                
        except Exception as e:
            print(f"   ❌ Error generating HTML report: {e}")
            return ""
    
    def create_statistics_plots(self, system, data=None) -> bool:
        """
        Create basic statistics plots.
        
        Args:
            system: InteractiveSystem instance
            data: Optional DataFrame (uses system.current_data if None)
            
        Returns:
            bool: True if successful
        """
        print(f"\n📊 CREATE STATISTICS PLOTS")
        print("-" * 50)
        
        if data is None:
            if not hasattr(system, 'current_data') or system.current_data is None:
                print("❌ No data loaded. Please load data first.")
                return False
            data = system.current_data
        
        print(f"📁 Creating statistics plots for dataset: {data.shape[0]:,} rows × {data.shape[1]} columns")
        
        # Create plots directory
        plots_dir = "plots"
        Path(plots_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate plots
        try:
            # Get numeric columns
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols:
                print(f"   📈 Found {len(numeric_cols)} numeric columns")
                
                # Summary statistics plot
                summary_path = self.plot_generator.create_summary_statistics_plot(data, numeric_cols)
                if summary_path:
                    print(f"   ✅ Summary statistics plot: {summary_path}")
                
                # Outlier analysis plot
                outlier_path = self.plot_generator.create_outlier_analysis_plot(data, numeric_cols)
                if outlier_path:
                    print(f"   ✅ Outlier analysis plot: {outlier_path}")
                
                # Correlation heatmap (if multiple numeric columns)
                if len(numeric_cols) > 1:
                    heatmap_path = self.plot_generator.create_correlation_heatmap(data, numeric_cols)
                    if heatmap_path:
                        print(f"   ✅ Correlation heatmap: {heatmap_path}")
            else:
                print(f"   ⚠️  No numeric columns found for statistics plots")
            
            # Missing values plot
            missing_path = self.plot_generator.create_missing_values_plot(data)
            if missing_path:
                print(f"   ✅ Missing values plot: {missing_path}")
            
            # Data types plot
            dtype_path = self.plot_generator.create_data_types_plot(data)
            if dtype_path:
                print(f"   ✅ Data types plot: {dtype_path}")
            
            print(f"\n✅ Statistics plots created successfully!")
            print(f"   📁 Plots saved in: {plots_dir}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating statistics plots: {e}")
            return False
    
    def show_plots_in_browser(self, system):
        """
        Show generated plots in web browser.
        
        Args:
            system: InteractiveSystem instance
        """
        print(f"\n🌐 SHOWING PLOTS IN BROWSER")
        print("-" * 50)
        
        plots_dir = "plots"
        
        if not os.path.exists(plots_dir):
            print("❌ Plots directory not found. Please generate plots first.")
            return
        
        # Find HTML report
        html_report = f"{plots_dir}/data_analysis_report.html"
        
        if os.path.exists(html_report):
            print(f"📄 Opening HTML report: {html_report}")
            try:
                webbrowser.open(f"file://{os.path.abspath(html_report)}")
                print(f"✅ HTML report opened in browser")
            except Exception as e:
                print(f"❌ Error opening HTML report: {e}")
        else:
            print(f"⚠️  HTML report not found: {html_report}")
            print(f"   💡 Generate visualization analysis first to create the report")
        
        # List available plot files
        plot_files = list(Path(plots_dir).glob("*.png"))
        if plot_files:
            print(f"\n📊 Available plot files ({len(plot_files)}):")
            for plot_file in plot_files:
                print(f"   • {plot_file.name}")
        else:
            print(f"\n📊 No plot files found in {plots_dir}")
    
    def create_field_html_report(self, data, field_name: str, plots_dir: str) -> str:
        """
        Create HTML report for a specific field.
        
        Args:
            data: DataFrame with data
            field_name: Name of the field
            plots_dir: Directory containing plots
            
        Returns:
            Path to generated HTML report
        """
        try:
            # Get field data
            field_data = data[field_name]
            
            # Calculate field statistics
            stats = self.html_generator._calculate_field_statistics(field_data)
            
            # Get field plots
            plots = self.plot_generator.create_field_plots(field_data, field_name)
            
            # Generate field HTML content
            field_html = self.html_generator.generate_field_html_content(field_name, stats, plots)
            
            # Create complete HTML document
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Field Analysis: {field_name}</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        line-height: 1.6;
                        margin: 20px;
                        background-color: #f5f5f5;
                    }}
                    .container {{
                        max-width: 800px;
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
                    .field-section {{
                        margin: 20px 0;
                        padding: 20px;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        background-color: #fafafa;
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
                    .insights-list {{
                        background-color: #e8f4fd;
                        padding: 15px;
                        border-radius: 5px;
                        border-left: 4px solid #3498db;
                    }}
                    .insights-list li {{
                        margin: 8px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔬 Field Analysis: {field_name}</h1>
                    {field_html}
                </div>
            </body>
            </html>
            """
            
            # Save HTML report
            report_path = f"{plots_dir}/{field_name}_analysis.html"
            success = self.html_generator.save_html_report(html_content, report_path)
            
            if success:
                print(f"✅ Field HTML report saved to: {report_path}")
                return report_path
            else:
                print(f"❌ Failed to save field HTML report")
                return ""
                
        except Exception as e:
            print(f"❌ Error creating field HTML report: {e}")
            return ""
