#!/usr/bin/env python3
"""
Plot generation utilities for data visualization.
Handles creation of various types of plots and charts.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import warnings

# Suppress matplotlib warnings
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')


class PlotGenerator:
    """Handles generation of various types of plots."""
    
    def __init__(self):
        """Initialize PlotGenerator."""
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
    
    def create_field_plots(self, field_data: pd.Series, field_name: str) -> Dict[str, str]:
        """
        Create plots for a specific field.
        
        Args:
            field_data: Series data for the field
            field_name: Name of the field
            
        Returns:
            Dictionary mapping plot types to file paths
        """
        plots = {}
        
        try:
            # Determine data type
            dtype = field_data.dtype
            
            if pd.api.types.is_numeric_dtype(dtype):
                plots.update(self._create_numeric_plots(field_data, field_name))
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                plots.update(self._create_datetime_plots(field_data, field_name))
            elif pd.api.types.is_categorical_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
                plots.update(self._create_categorical_plots(field_data, field_name))
            
        except Exception as e:
            print(f"   ❌ Error creating plots for {field_name}: {e}")
        
        return plots
    
    def _create_numeric_plots(self, field_data: pd.Series, field_name: str) -> Dict[str, str]:
        """Create plots for numeric fields."""
        plots = {}
        
        try:
            # Clean data
            clean_data = field_data.dropna()
            if len(clean_data) == 0:
                return plots
            
            # 1. Histogram
            plt.figure(figsize=(10, 6))
            plt.hist(clean_data, bins=50, alpha=0.7, edgecolor='black')
            plt.title(f'Histogram of {field_name}')
            plt.xlabel(field_name)
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            
            hist_path = f"../plots/{field_name}_histogram.png"
            plt.savefig(hist_path, dpi=300, bbox_inches='tight')
            plt.close()
            plots['histogram'] = hist_path
            
            # 2. Box plot
            plt.figure(figsize=(8, 6))
            plt.boxplot(clean_data)
            plt.title(f'Box Plot of {field_name}')
            plt.ylabel(field_name)
            plt.grid(True, alpha=0.3)
            
            box_path = f"../plots/{field_name}_boxplot.png"
            plt.savefig(box_path, dpi=300, bbox_inches='tight')
            plt.close()
            plots['boxplot'] = box_path
            
            # 3. KDE plot
            plt.figure(figsize=(10, 6))
            clean_data.plot.kde()
            plt.title(f'Kernel Density Estimation of {field_name}')
            plt.xlabel(field_name)
            plt.ylabel('Density')
            plt.grid(True, alpha=0.3)
            
            kde_path = f"../plots/{field_name}_kde.png"
            plt.savefig(kde_path, dpi=300, bbox_inches='tight')
            plt.close()
            plots['kde'] = kde_path
            
            # 4. Q-Q plot (for normality check)
            plt.figure(figsize=(8, 8))
            from scipy import stats
            stats.probplot(clean_data, dist="norm", plot=plt)
            plt.title(f'Q-Q Plot of {field_name} (Normal Distribution)')
            plt.grid(True, alpha=0.3)
            
            qq_path = f"../plots/{field_name}_qqplot.png"
            plt.savefig(qq_path, dpi=300, bbox_inches='tight')
            plt.close()
            plots['qqplot'] = qq_path
            
        except Exception as e:
            print(f"   ❌ Error creating numeric plots for {field_name}: {e}")
        
        return plots
    
    def _create_datetime_plots(self, field_data: pd.Series, field_name: str) -> Dict[str, str]:
        """Create plots for datetime fields."""
        plots = {}
        
        try:
            # Clean data
            clean_data = field_data.dropna()
            if len(clean_data) == 0:
                return plots
            
            # Convert to datetime if needed
            if not pd.api.types.is_datetime64_any_dtype(clean_data):
                clean_data = pd.to_datetime(clean_data, errors='coerce')
                clean_data = clean_data.dropna()
            
            if len(clean_data) == 0:
                return plots
            
            # 1. Time series plot
            plt.figure(figsize=(12, 6))
            clean_data.value_counts().sort_index().plot(kind='line')
            plt.title(f'Time Series Distribution of {field_name}')
            plt.xlabel('Date')
            plt.ylabel('Frequency')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            ts_path = f"../plots/{field_name}_timeseries.png"
            plt.savefig(ts_path, dpi=300, bbox_inches='tight')
            plt.close()
            plots['timeseries'] = ts_path
            
            # 2. Monthly distribution
            plt.figure(figsize=(10, 6))
            monthly_counts = clean_data.dt.month.value_counts().sort_index()
            monthly_counts.plot(kind='bar')
            plt.title(f'Monthly Distribution of {field_name}')
            plt.xlabel('Month')
            plt.ylabel('Frequency')
            plt.xticks(rotation=0)
            plt.grid(True, alpha=0.3)
            
            monthly_path = f"../plots/{field_name}_monthly.png"
            plt.savefig(monthly_path, dpi=300, bbox_inches='tight')
            plt.close()
            plots['monthly'] = monthly_path
            
            # 3. Hourly distribution (if time component exists)
            if clean_data.dt.hour.nunique() > 1:
                plt.figure(figsize=(10, 6))
                hourly_counts = clean_data.dt.hour.value_counts().sort_index()
                hourly_counts.plot(kind='bar')
                plt.title(f'Hourly Distribution of {field_name}')
                plt.xlabel('Hour')
                plt.ylabel('Frequency')
                plt.xticks(rotation=0)
                plt.grid(True, alpha=0.3)
                
                hourly_path = f"../plots/{field_name}_hourly.png"
                plt.savefig(hourly_path, dpi=300, bbox_inches='tight')
                plt.close()
                plots['hourly'] = hourly_path
            
        except Exception as e:
            print(f"   ❌ Error creating datetime plots for {field_name}: {e}")
        
        return plots
    
    def _create_categorical_plots(self, field_data: pd.Series, field_name: str) -> Dict[str, str]:
        """Create plots for categorical fields."""
        plots = {}
        
        try:
            # Clean data
            clean_data = field_data.dropna()
            if len(clean_data) == 0:
                return plots
            
            # Limit to top categories if too many
            value_counts = clean_data.value_counts()
            if len(value_counts) > 20:
                top_values = value_counts.head(20)
                clean_data = clean_data[clean_data.isin(top_values.index)]
                print(f"   ⚠️  Limiting to top 20 categories for {field_name}")
            
            # 1. Bar plot
            plt.figure(figsize=(12, 6))
            clean_data.value_counts().plot(kind='bar')
            plt.title(f'Distribution of {field_name}')
            plt.xlabel(field_name)
            plt.ylabel('Frequency')
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            
            bar_path = f"../plots/{field_name}_barplot.png"
            plt.savefig(bar_path, dpi=300, bbox_inches='tight')
            plt.close()
            plots['barplot'] = bar_path
            
            # 2. Pie chart (for top 10 categories)
            top_10 = clean_data.value_counts().head(10)
            if len(top_10) > 0:
                plt.figure(figsize=(10, 8))
                plt.pie(top_10.values, labels=top_10.index, autopct='%1.1f%%', startangle=90)
                plt.title(f'Top 10 Categories in {field_name}')
                plt.axis('equal')
                
                pie_path = f"../plots/{field_name}_piechart.png"
                plt.savefig(pie_path, dpi=300, bbox_inches='tight')
                plt.close()
                plots['piechart'] = pie_path
            
        except Exception as e:
            print(f"   ❌ Error creating categorical plots for {field_name}: {e}")
        
        return plots
    
    def create_correlation_heatmap(self, data: pd.DataFrame, numeric_cols: List[str]) -> str:
        """
        Create correlation heatmap for numeric columns.
        
        Args:
            data: DataFrame with data
            numeric_cols: List of numeric column names
            
        Returns:
            Path to saved heatmap
        """
        try:
            if len(numeric_cols) < 2:
                return ""
            
            # Calculate correlation matrix
            corr_matrix = data[numeric_cols].corr()
            
            # Create heatmap
            plt.figure(figsize=(12, 10))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, linewidths=0.5, cbar_kws={"shrink": .8})
            plt.title('Correlation Heatmap')
            plt.tight_layout()
            
            heatmap_path = "../plots/correlation_heatmap.png"
            plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return heatmap_path
            
        except Exception as e:
            print(f"   ❌ Error creating correlation heatmap: {e}")
            return ""
    
    def create_missing_values_plot(self, data: pd.DataFrame) -> str:
        """
        Create missing values visualization.
        
        Args:
            data: DataFrame with data
            
        Returns:
            Path to saved plot
        """
        try:
            # Calculate missing values
            missing_data = data.isnull().sum()
            missing_percent = (missing_data / len(data)) * 100
            
            # Filter columns with missing values
            missing_cols = missing_data[missing_data > 0]
            if len(missing_cols) == 0:
                return ""
            
            # Create bar plot
            plt.figure(figsize=(12, 6))
            missing_percent[missing_cols.index].plot(kind='bar')
            plt.title('Missing Values by Column')
            plt.xlabel('Column')
            plt.ylabel('Missing Percentage')
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            plt.ylim(0, 100)
            
            missing_path = "../plots/missing_values.png"
            plt.savefig(missing_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return missing_path
            
        except Exception as e:
            print(f"   ❌ Error creating missing values plot: {e}")
            return ""
    
    def create_data_types_plot(self, data: pd.DataFrame) -> str:
        """
        Create data types distribution plot.
        
        Args:
            data: DataFrame with data
            
        Returns:
            Path to saved plot
        """
        try:
            # Count data types
            dtype_counts = data.dtypes.value_counts()
            
            # Create pie chart
            plt.figure(figsize=(10, 8))
            plt.pie(dtype_counts.values, labels=dtype_counts.index, autopct='%1.1f%%', startangle=90)
            plt.title('Data Types Distribution')
            plt.axis('equal')
            
            dtype_path = "../plots/data_types.png"
            plt.savefig(dtype_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return dtype_path
            
        except Exception as e:
            print(f"   ❌ Error creating data types plot: {e}")
            return ""
    
    def create_summary_statistics_plot(self, data: pd.DataFrame, numeric_cols: List[str]) -> str:
        """
        Create summary statistics visualization.
        
        Args:
            data: DataFrame with data
            numeric_cols: List of numeric column names
            
        Returns:
            Path to saved plot
        """
        try:
            if len(numeric_cols) == 0:
                return ""
            
            # Calculate summary statistics
            summary_stats = data[numeric_cols].describe()
            
            # Create subplots
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Summary Statistics Overview', fontsize=16)
            
            # 1. Mean values
            axes[0, 0].bar(range(len(numeric_cols)), summary_stats.loc['mean'])
            axes[0, 0].set_title('Mean Values')
            axes[0, 0].set_xticks(range(len(numeric_cols)))
            axes[0, 0].set_xticklabels(numeric_cols, rotation=45, ha='right')
            axes[0, 0].grid(True, alpha=0.3)
            
            # 2. Standard deviation
            axes[0, 1].bar(range(len(numeric_cols)), summary_stats.loc['std'])
            axes[0, 1].set_title('Standard Deviation')
            axes[0, 1].set_xticks(range(len(numeric_cols)))
            axes[0, 1].set_xticklabels(numeric_cols, rotation=45, ha='right')
            axes[0, 1].grid(True, alpha=0.3)
            
            # 3. Min values
            axes[1, 0].bar(range(len(numeric_cols)), summary_stats.loc['min'])
            axes[1, 0].set_title('Minimum Values')
            axes[1, 0].set_xticks(range(len(numeric_cols)))
            axes[1, 0].set_xticklabels(numeric_cols, rotation=45, ha='right')
            axes[1, 0].grid(True, alpha=0.3)
            
            # 4. Max values
            axes[1, 1].bar(range(len(numeric_cols)), summary_stats.loc['max'])
            axes[1, 1].set_title('Maximum Values')
            axes[1, 1].set_xticks(range(len(numeric_cols)))
            axes[1, 1].set_xticklabels(numeric_cols, rotation=45, ha='right')
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            summary_path = "../plots/summary_statistics.png"
            plt.savefig(summary_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return summary_path
            
        except Exception as e:
            print(f"   ❌ Error creating summary statistics plot: {e}")
            return ""
    
    def create_outlier_analysis_plot(self, data: pd.DataFrame, numeric_cols: List[str]) -> str:
        """
        Create outlier analysis visualization.
        
        Args:
            data: DataFrame with data
            numeric_cols: List of numeric column names
            
        Returns:
            Path to saved plot
        """
        try:
            if len(numeric_cols) == 0:
                return ""
            
            # Limit to first 6 columns for readability
            cols_to_plot = numeric_cols[:6]
            
            # Create subplots
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Outlier Analysis', fontsize=16)
            
            for i, col in enumerate(cols_to_plot):
                row = i // 3
                col_idx = i % 3
                
                # Create box plot
                axes[row, col_idx].boxplot(data[col].dropna())
                axes[row, col_idx].set_title(f'{col}')
                axes[row, col_idx].set_ylabel('Value')
                axes[row, col_idx].grid(True, alpha=0.3)
            
            # Hide empty subplots
            for i in range(len(cols_to_plot), 6):
                row = i // 3
                col_idx = i % 3
                axes[row, col_idx].set_visible(False)
            
            plt.tight_layout()
            
            outlier_path = "../plots/outlier_analysis.png"
            plt.savefig(outlier_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return outlier_path
            
        except Exception as e:
            print(f"   ❌ Error creating outlier analysis plot: {e}")
            return ""
