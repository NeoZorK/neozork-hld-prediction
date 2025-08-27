# Handles basic statistics

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
from matplotlib.figure import Figure
from io import BytesIO
import base64
import webbrowser
from src.eda.html_report_generator import HTMLReport, ensure_report_directory, create_index_page, clean_all_reports

# Suppress matplotlib warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# Set seaborn style for better looking plots
sns.set(style="whitegrid")

def ensure_plots_directory():
    """Ensure plots directory exists for saving visualizations."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    plots_dir = os.path.join(base_dir, 'results', 'plots')

    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    return plots_dir

def open_last_plot_in_browser(plot_path):
    """Open the last created plot in the default web browser."""
    if os.path.exists(plot_path):
        webbrowser.open(f'file://{os.path.abspath(plot_path)}')
        print(f"\033[93m[INFO]\033[0m Last plot opened in your default browser: {plot_path}")
    else:
        print(f"\033[91m[ERROR]\033[0m Plot file not found: {plot_path}")

def save_plot_with_description(plot_path, description):
    """Save a .txt description file for a plot."""
    desc_path = plot_path + '.txt'
    with open(desc_path, 'w', encoding='utf-8') as f:
        f.write(description)
    print(f"\033[92m[INFO]\033[0m Description saved to: {desc_path}")

def compute_basic_stats(df):
    """
    Compute basic statistics for each column in the DataFrame.
    Returns a dictionary with stats for each column.
    """
    stats = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            stats[col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                '25%': df[col].quantile(0.25),
                '50%': df[col].quantile(0.5),
                '75%': df[col].quantile(0.75),
                'missing': int(df[col].isnull().sum()),
                'unique': int(df[col].nunique())
            }
        else:
            stats[col] = {
                'missing': int(df[col].isnull().sum()),
                'unique': int(df[col].nunique()),
                'top': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                'freq': int(df[col].value_counts().iloc[0]) if not df[col].value_counts().empty else 0
            }
    return stats

def print_basic_stats_summary(stats_result):
    """Print summary and recommendations for basic statistics."""
    # Identify columns with high missing values
    high_missing_cols = []
    numeric_cols = []
    categorical_cols = []
    high_cardinality_cols = []
    low_cardinality_cols = []

    for col, stats in stats_result.items():
        # Check for numeric columns
        if 'std' in stats:
            numeric_cols.append(col)

            # Check for high missing values
            if stats['missing'] > 0:
                missing_pct = stats['missing'] / (stats['missing'] + stats['unique']) * 100
                if missing_pct > 5:
                    high_missing_cols.append((col, missing_pct))
        else:
            categorical_cols.append(col)
            # Check cardinality
            if stats['unique'] > 100:
                high_cardinality_cols.append((col, stats['unique']))
            elif stats['unique'] < 5 and stats['unique'] > 1:
                low_cardinality_cols.append((col, stats['unique']))

    # Print summary
    print("\n\033[1m\033[95mSummary and Recommendations:\033[0m")
    print(f"  • Dataset contains {len(numeric_cols)} numeric and {len(categorical_cols)} non-numeric columns")

    if high_missing_cols:
        print(f"  • {len(high_missing_cols)} columns have significant missing values (>5%):")
        for col, pct in sorted(high_missing_cols, key=lambda x: x[1], reverse=True)[:5]:  # Show top 5
            print(f"    - {col}: {pct:.1f}% missing")
        if len(high_missing_cols) > 5:
            print(f"    - ... and {len(high_missing_cols) - 5} more columns")
        print("  • Consider handling missing values with imputation or feature removal")

    if high_cardinality_cols:
        print(f"  • High cardinality categorical features: {len(high_cardinality_cols)} columns")
        print("  • Consider encoding methods like target encoding for these columns")

    if low_cardinality_cols:
        print(f"  • Low cardinality features: {len(low_cardinality_cols)} columns")
        print("  • These might be good candidates for one-hot encoding")

    print("  • Next steps:")
    print("    - Run --descriptive-stats for more detailed statistics")
    print("    - Check distributions with --distribution-analysis")
    print("    - Run --correlation-analysis to understand relationships between features")

    # Visualization for basic stats
    plots_dir = ensure_plots_directory()
    numeric_cols = [col for col, s in stats_result.items() if 'std' in s]
    if numeric_cols:
        plt.figure(figsize=(10, 6))
        means = [stats_result[col]['mean'] for col in numeric_cols]
        stds = [stats_result[col]['std'] for col in numeric_cols]
        sns.barplot(x=numeric_cols, y=means, color='skyblue', edgecolor='black')
        plt.xticks(rotation=45)
        plt.ylabel('Mean Value')
        plt.title('Mean of Numeric Columns (Basic Stats)')
        plt.tight_layout()
        plot_path = os.path.join(plots_dir, 'basic_stats_means.png')
        plt.savefig(plot_path)
        plt.close()
        description = (
            "Plot: Mean values for numeric columns.\n"
            "Purpose: Quickly compare the mean values of different features.\n"
            "Interpretation: A high mean may indicate scale issues or outliers.\n"
            "Good: Features have comparable scales, no extreme values.\n"
            "Bad: Strongly deviating columns require checking for outliers or errors.\n"
            "Next steps: Perform outlier analysis and normalize data if necessary."
        )
        save_plot_with_description(plot_path, description)
        open_last_plot_in_browser(plot_path)
        print(f"\033[93m[INFO]\033[0m All generated plots can be found in: {plots_dir}")

def outlier_analysis(df):
    """
    Detect outliers in numeric columns using IQR and Z-score methods.
    Returns a dictionary with outlier information for each column.
    """
    result = {}
    for col in df.select_dtypes(include=['number']).columns:
        try:
            col_data = df[col].dropna()

            # Check if there are enough data points for analysis
            if len(col_data) < 3:
                result[col] = {
                    'error': 'Insufficient data points for outlier analysis',
                    'iqr_method': {
                        'lower_bound': float('nan'),
                        'upper_bound': float('nan'),
                        'outliers_count': 0,
                        'outlier_percentage': 0.0,
                        'outlier_indices': [],
                        'outlier_values': []
                    },
                    'z_score_method': {
                        'threshold': 3,
                        'outliers_count': 0,
                        'outlier_percentage': 0.0,
                        'outlier_indices': [],
                        'outlier_values': []
                    }
                }
                continue

            # IQR method
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers_iqr = col_data[(col_data < lower_bound) | (col_data > upper_bound)]

            # Z-score method
            mean = col_data.mean()
            std = col_data.std()

            # Calculate z-scores
            if std == 0:
                z_scores = pd.Series([0] * len(col_data), index=col_data.index)
            else:
                z_scores = abs((col_data - mean) / std)

            # Check for large data range
            max_value = col_data.max()
            min_value = col_data.min()
            data_range = max_value - min_value

            # If the data range is large compared to the mean, we may have a different distribution
            if data_range > 50 * mean and len(col_data) > 5:
                # Sort the data to find large gaps
                sorted_data = col_data.sort_values()
                diffs = sorted_data.diff()
                # Find large gaps
                large_gaps = diffs[diffs > 0.1 * data_range]

                if not large_gaps.empty:
                    # Using the largest gap to determine outliers
                    gap_idx = large_gaps.idxmax()
                    position = sorted_data.index.get_loc(gap_idx)

                    # Determine the outlier range based on the gap
                    if position > len(sorted_data) * 0.5:  # e.g. gap is in the second half
                        outliers_zscore = sorted_data.iloc[position:]
                    else:  # gap is in the first half
                        outliers_zscore = sorted_data.iloc[:position]
                else:
                    # use the standard z-score method
                    outliers_zscore = col_data[z_scores > 3]  # +/- 3 standard deviations
            else:
                # Standard z-score method
                outliers_zscore = col_data[z_scores > 3]  # +/- 3 standard deviations

            result[col] = {
                'iqr_method': {
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound,
                    'outliers_count': len(outliers_iqr),
                    'outlier_percentage': (len(outliers_iqr) / len(col_data)) * 100,
                    'outlier_indices': list(outliers_iqr.index),
                    'outlier_values': list(outliers_iqr.values)
                },
                'z_score_method': {
                    'threshold': 3,  # Z-score threshold
                    'outliers_count': len(outliers_zscore),
                    'outlier_percentage': (len(outliers_zscore) / len(col_data)) * 100,
                    'outlier_indices': list(outliers_zscore.index),
                    'outlier_values': list(outliers_zscore.values)
                }
            }
        except Exception as e:
            # Handle any exceptions that occur during outlier detection
            result[col] = {
                'error': str(e),
                'iqr_method': {
                    'lower_bound': float('nan'),
                    'upper_bound': float('nan'),
                    'outliers_count': 0,
                    'outlier_percentage': 0.0,
                    'outlier_indices': [],
                    'outlier_values': []
                },
                'z_score_method': {
                    'threshold': 3,
                    'outliers_count': 0,
                    'outlier_percentage': 0.0,
                    'outlier_indices': [],
                    'outlier_values': []
                }
            }

    return result

def print_outlier_analysis(outlier_results):
    """Print outlier analysis results with color formatting."""
    print("\n\033[1m\033[95mOutlier Analysis:\033[0m")

    for col, result in outlier_results.items():
        print(f"\n\033[93mColumn: {col}\033[0m")
        if 'error' in result:
            print(f"  Error: {result['error']}")
            continue

        iqr_method = result['iqr_method']
        z_method = result['z_score_method']

        print("  IQR Method:")
        print(f"    Bounds: [{iqr_method['lower_bound']:.4f}, {iqr_method['upper_bound']:.4f}]")
        print(f"    Outliers: {iqr_method['outliers_count']} ({iqr_method['outlier_percentage']:.2f}%)")

        print("  Z-Score Method (threshold=3):")
        print(f"    Outliers: {z_method['outliers_count']} ({z_method['outlier_percentage']:.2f}%)")

        # Show sample outliers if any - with a check for the key's existence
        if iqr_method['outliers_count'] > 0 and 'outlier_values' in iqr_method:
            print("  Sample outlier values (IQR method):")
            for value in iqr_method['outlier_values'][:5]:  # Show max 5 examples
                print(f"    - {value}")
        # If we have outlier indices but no values, we can mention that
        elif iqr_method['outliers_count'] > 0 and 'outlier_indices' in iqr_method:
            print("  Outlier indices (IQR method):")
            for idx in iqr_method['outlier_indices'][:5]:  # Show max 5 examples
                print(f"    - Index {idx}")

def print_distribution_analysis(distribution_stats):
    """
    Print distribution analysis results with color formatting.
    Displays skewness, kurtosis, and normality test results for each column.

    Args:
        distribution_stats (dict): Dictionary with distribution statistics for each column
    """
    print("\n\033[1m\033[95mDistribution Analysis:\033[0m")

    for col, stats in distribution_stats.items():
        print(f"\n\033[93mColumn: {col}\033[0m")

        if 'error' in stats:
            print(f"  Error: {stats['error']}")
            continue

        # Print skewness
        skewness = stats.get('skewness', float('nan'))
        if not np.isnan(skewness):
            skew_desc = "Symmetrical"
            if skewness > 1:
                skew_desc = "Highly positive skewed"
            elif skewness > 0.5:
                skew_desc = "Moderately positive skewed"
            elif skewness > 0.1:
                skew_desc = "Slightly positive skewed"
            elif skewness < -1:
                skew_desc = "Highly negative skewed"
            elif skewness < -0.5:
                skew_desc = "Moderately negative skewed"
            elif skewness < -0.1:
                skew_desc = "Slightly negative skewed"

            print(f"  Skewness: {skewness:.4f} - {skew_desc}")

        # Print kurtosis
        kurtosis = stats.get('kurtosis', float('nan'))
        if not np.isnan(kurtosis):
            kurt_desc = "Mesokurtic (normal-like)"
            if kurtosis > 3:
                kurt_desc = "Leptokurtic (heavy tails)"
            elif kurtosis < -1:
                kurt_desc = "Platykurtic (light tails)"

            print(f"  Kurtosis: {kurtosis:.4f} - {kurt_desc}")

        # Print normality test results
        normality_test = stats.get('normality_test')
        if normality_test is not None:
            statistic, p_value = normality_test
            is_normal = stats.get('is_normal', 'Unknown')
            print(f"  Normality Test (Shapiro-Wilk):")
            print(f"    Statistic: {statistic:.4f}")
            print(f"    p-value: {p_value:.4f}")
            print(f"    Distribution is normal: {is_normal}")
            if p_value < 0.05:
                print("    \033[91mRecommendation:\033[0m Consider non-parametric methods or transformations.")
            else:
                print("    \033[92mRecommendation:\033[0m Parametric methods are likely appropriate.")
        else:
            print("  Normality Test: Not available (insufficient data points)")

        # Add visualization suggestion
        print("  Visualization: Consider histogram, QQ-plot, or KDE for visual inspection")

def generate_outlier_analysis_report(df, file_path):
    """
    Generate a detailed HTML report with plots for outlier analysis

    Parameters:
    - df: DataFrame to analyze
    - file_path: Path to the original data file

    Returns:
    - Path to the generated HTML report
    """
    # Create a new HTML report
    report = HTMLReport("Outlier Analysis", file_path)
    report.add_header()

    # Add overview section
    overview = f"""
    <p>This report provides outlier detection analysis for numeric columns in the dataset.</p>
    <p>Outliers are extreme values that deviate significantly from other observations, 
    which can strongly influence statistical analyses and machine learning models.</p>
    <p>Two detection methods are used:</p>
    <ul>
        <li><strong>IQR Method</strong>: Values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR are considered outliers</li>
        <li><strong>Z-score Method</strong>: Values more than 3 standard deviations from the mean are considered outliers</li>
    </ul>
    """
    report.add_section("Overview", overview)

    # Perform outlier analysis
    outlier_results = outlier_analysis(df)

    # Get numeric columns that were successfully analyzed
    valid_columns = [col for col in outlier_results if 'error' not in outlier_results[col]]

    if not valid_columns:
        report.add_section("No Valid Data",
                          "<p>No numeric columns could be analyzed. Please check if the dataset contains numeric data.</p>")

        # Save the report
        report_dir = ensure_report_directory(file_path)
        report_path = os.path.join(report_dir, "outlier_analysis.html")
        report.save(report_path)
        return report_path

    # Create outlier summary table
    outlier_data = []
    for col in valid_columns:
        result = outlier_results[col]
        iqr_method = result['iqr_method']
        z_method = result['z_score_method']

        outlier_pct = max(iqr_method['outlier_percentage'], z_method['outlier_percentage'])
        severity = "High" if outlier_pct > 5 else "Medium" if outlier_pct > 1 else "Low"

        outlier_data.append({
            'Column': col,
            'IQR Outliers Count': iqr_method['outliers_count'],
            'IQR Outliers %': f"{iqr_method['outlier_percentage']:.2f}%",
            'Z-score Outliers Count': z_method['outliers_count'],
            'Z-score Outliers %': f"{z_method['outlier_percentage']:.2f}%",
            'Lower Bound': f"{iqr_method['lower_bound']:.4f}",
            'Upper Bound': f"{iqr_method['upper_bound']:.4f}",
            'Severity': severity
        })

    outlier_df = pd.DataFrame(outlier_data)
    report.add_table(
        outlier_df,
        "Outlier Analysis Summary",
        "This table summarizes the outlier detection results for each numeric column, showing counts and percentages for both IQR and Z-score methods."
    )

    # Generate visualizations for columns with outliers
    for col in valid_columns:
        result = outlier_results[col]
        iqr_method = result['iqr_method']
        z_method = result['z_score_method']

        # Only create detailed plots for columns with at least some outliers
        if max(iqr_method['outlier_percentage'], z_method['outlier_percentage']) > 0:
            col_data = df[col].dropna()

            # Create a figure with multiple plots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
            fig.suptitle(f'Outlier Analysis for {col}', fontsize=16)

            # 1. Box plot
            sns.boxplot(data=col_data, ax=ax1, color='lightblue', orient='h')
            ax1.set_title('Box Plot (IQR Method)')

            # 2. Scatter plot with IQR bounds
            x = np.arange(len(col_data))
            ax2.scatter(x, col_data, alpha=0.5, color='blue', s=10)
            ax2.axhline(y=iqr_method['lower_bound'], color='red', linestyle='--',
                        label=f"Lower Bound: {iqr_method['lower_bound']:.2f}")
            ax2.axhline(y=iqr_method['upper_bound'], color='red', linestyle='--',
                        label=f"Upper Bound: {iqr_method['upper_bound']:.2f}")
            ax2.set_title('Value Distribution with IQR Bounds')
            ax2.legend()
            ax2.set_xlabel('Index')
            ax2.set_ylabel('Value')

            # 3. Z-score distribution
            mean = col_data.mean()
            std = col_data.std()
            z_scores = (col_data - mean) / std

            sns.histplot(z_scores, kde=True, ax=ax3, color='lightgreen')
            ax3.axvline(x=3, color='red', linestyle='--', label='Z=3')
            ax3.axvline(x=-3, color='red', linestyle='--', label='Z=-3')
            ax3.set_title('Z-score Distribution')
            ax3.set_xlabel('Z-score')
            ax3.legend()

            # 4. Outlier values plot
            outlier_mask = col_data.isin(iqr_method['outlier_values'])
            colors = ['red' if x else 'blue' for x in outlier_mask]
            ax4.scatter(x, col_data, c=colors, alpha=0.5, s=10)
            ax4.set_title('Data Points with Outliers (red)')
            ax4.set_xlabel('Index')
            ax4.set_ylabel('Value')

            # Add summary text
            summary_text = (
                f"IQR Method: {iqr_method['outliers_count']} outliers ({iqr_method['outlier_percentage']:.2f}%)\n"
                f"Z-score Method: {z_method['outliers_count']} outliers ({z_method['outlier_percentage']:.2f}%)\n\n"
                f"IQR Bounds: [{iqr_method['lower_bound']:.4f}, {iqr_method['upper_bound']:.4f}]\n"
                f"Data Range: [{col_data.min():.4f}, {col_data.max():.4f}]"
            )

            # Add text box to figure
            fig.text(0.01, 0.01, summary_text, verticalalignment='bottom',
                    horizontalalignment='left', bbox=dict(boxstyle='round',
                                                        facecolor='wheat', alpha=0.5))

            plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust for main title and text box

            # Create interpretations and recommendations
            if max(iqr_method['outlier_percentage'], z_method['outlier_percentage']) > 5:
                severity = "High proportion of outliers detected"
                impact = "These outliers may significantly impact statistical analyses and model performance."
            elif max(iqr_method['outlier_percentage'], z_method['outlier_percentage']) > 1:
                severity = "Moderate proportion of outliers detected"
                impact = "These outliers may have some impact on analyses and models."
            else:
                severity = "Low proportion of outliers detected"
                impact = "These few outliers are unlikely to significantly impact most analyses."

            interpretation = f"{severity}. {impact}"

            good = "Low percentage of outliers (<1%) or outliers that represent valid extreme values in the domain."

            bad = "High percentage of outliers (>5%) that may be data errors or anomalies requiring special treatment."

            recommendations = []
            if max(iqr_method['outlier_percentage'], z_method['outlier_percentage']) > 5:
                recommendations.append("Investigate the source of these outliers - are they data errors or valid extreme values?")
                recommendations.append("Consider removing or capping outliers if they are errors or not representative of the phenomenon.")
                recommendations.append("If using machine learning, consider robust models less affected by outliers.")
            elif max(iqr_method['outlier_percentage'], z_method['outlier_percentage']) > 1:
                recommendations.append("Review outliers to determine if they are valid data points or errors.")
                recommendations.append("Consider Winsorization (capping) at specified percentiles rather than removing outliers.")
            else:
                recommendations.append("These few outliers can typically be handled with standard robust statistical methods.")

            recommendation_text = " ".join(recommendations)

            report.add_plot(
                plt.gcf(),
                f"Outlier Analysis for {col}",
                "These plots show outlier detection using IQR and Z-score methods, including box plot, value distribution with boundaries, Z-score distribution, and a scatter plot highlighting detected outliers.",
                interpretation,
                good,
                bad,
                recommendation_text
            )

    # Add summary and recommendations section
    high_outlier_cols = []
    moderate_outlier_cols = []
    low_outlier_cols = []

    for col in valid_columns:
        result = outlier_results[col]
        outlier_pct = max(result['iqr_method']['outlier_percentage'],
                         result['z_score_method']['outlier_percentage'])

        if outlier_pct > 5:
            high_outlier_cols.append((col, outlier_pct))
        elif outlier_pct > 1:
            moderate_outlier_cols.append((col, outlier_pct))
        elif outlier_pct > 0:
            low_outlier_cols.append((col, outlier_pct))

    recommendations = []
    if high_outlier_cols:
        recommendations.append("<li><strong>High Outlier Columns:</strong> The following columns have significant outliers (>5%):")
        recommendations.append("<ul>")
        for col, pct in sorted(high_outlier_cols, key=lambda x: x[1], reverse=True):
            recommendations.append(f"<li>{col}: {pct:.2f}%</li>")
        recommendations.append("</ul>")
        recommendations.append("These columns should be carefully examined and may need special treatment.</li>")

    if moderate_outlier_cols:
        recommendations.append("<li><strong>Moderate Outlier Columns:</strong> The following columns have moderate outliers (1-5%):")
        recommendations.append("<ul>")
        for col, pct in sorted(moderate_outlier_cols, key=lambda x: x[1], reverse=True):
            recommendations.append(f"<li>{col}: {pct:.2f}%</li>")
        recommendations.append("</ul>")
        recommendations.append("Consider whether these outliers are legitimate values or errors.</li>")

    if high_outlier_cols or moderate_outlier_cols:
        recommendations.append("<li><strong>Outlier Treatment Options:</strong>")
        recommendations.append("<ul>")
        recommendations.append("<li><strong>Remove:</strong> Delete outlier rows if they are clearly errors</li>")
        recommendations.append("<li><strong>Cap/Winsorize:</strong> Replace outliers with the boundary values</li>")
        recommendations.append("<li><strong>Transform:</strong> Apply log, sqrt, or Box-Cox transformations to reduce the impact of outliers</li>")
        recommendations.append("<li><strong>Robust Methods:</strong> Use statistical methods that are less sensitive to outliers</li>")
        recommendations.append("</ul></li>")

    summary_content = f"""
    <p>Based on the outlier analysis of {len(valid_columns)} numeric columns, here are the key findings and recommendations:</p>
    <ul>
        {"".join(recommendations) if recommendations else "<li>No significant outlier issues detected in the dataset.</li>"}
        <li><strong>Next Steps:</strong> For columns with significant outliers, determine if they represent errors or valid extreme values before deciding on an appropriate treatment strategy.</li>
    </ul>
    """
    report.add_section("Summary and Recommendations", summary_content)

    # Save the report
    report_dir = ensure_report_directory(file_path)
    report_path = os.path.join(report_dir, "outlier_analysis.html")
    report.save(report_path)

    return report_path

def descriptive_stats(df):
    """
    Compute detailed descriptive statistics for each numeric column.
    Returns a dictionary with stats for each column.
    """
    result = {}
    for col in df.select_dtypes(include=['number']).columns:
        try:
            col_data = df[col].dropna()
            if len(col_data) == 0:
                result[col] = {'error': 'No non-null data points'}
                continue

            result[col] = {
                'mean': col_data.mean(),
                'median': col_data.median(),
                'mode': col_data.mode().iloc[0] if not col_data.mode().empty else None,
                'std': col_data.std(),
                'var': col_data.var(),
                'min': col_data.min(),
                'max': col_data.max(),
                '25%': col_data.quantile(0.25),
                '50%': col_data.quantile(0.5),
                '75%': col_data.quantile(0.75),
                'iqr': col_data.quantile(0.75) - col_data.quantile(0.25),
                'range': col_data.max() - col_data.min(),
                'coef_variation': col_data.std() / col_data.mean() if col_data.mean() != 0 else float('inf'),
                'data_points': len(col_data),
                'missing': df[col].isna().sum(),
                'missing_pct': df[col].isna().sum() / len(df) * 100
            }
        except Exception as e:
            result[col] = {'error': str(e)}

    return result

def print_descriptive_stats(desc_stats):
    """Print descriptive statistics with color formatting."""
    print("\n\033[1m\033[95mDescriptive Statistics\033[0m")

    # Group columns by type
    column_groups = {}
    for col in desc_stats.keys():
        # Group by OHLCV pattern
        if col.lower().find('open') != -1 or col.lower().find('high') != -1 or col.lower().find('low') != -1 or col.lower().find('close') != -1:
            group = 'price_ohlc'
        elif col.lower().find('volume') != -1:
            group = 'volume'
        else:
            group = 'other'

        if group not in column_groups:
            column_groups[group] = []
        column_groups[group].append(col)

    # Print each group
    for group, columns in column_groups.items():
        if group == 'price_ohlc':
            print("\n\033[96mPrice Data (OHLC):\033[0m")
        elif group == 'volume':
            print("\n\033[96mVolume Data:\033[0m")
        else:
            print("\n\033[96mOther Data:\033[0m")

        for col in columns:
            stats = desc_stats[col]
            print(f"\n\033[93mColumn: {col}\033[0m")

            # Check for errors
            if 'error' in stats:
                print(f"  Error: {stats['error']}")
                continue

            # Print basic stats
            stats_to_print = [
                ('Mean', 'mean', '{:.4f}'),
                ('Median', 'median', '{:.4f}'),
                ('Mode', 'mode', '{}'),
                ('Standard Deviation', 'std', '{:.4f}'),
                ('Variance', 'var', '{:.4f}'),
                ('Range', 'range', '{:.4f}')
            ]

            for label, key, fmt in stats_to_print:
                if key in stats:
                    value = stats[key]
                    # Format the value if it's numeric
                    if isinstance(value, (int, float)) and fmt != '{}':
                        formatted_value = fmt.format(value)
                    else:
                        formatted_value = str(value)
                    print(f"  {label}: {formatted_value}")

            # Show quartiles
            if 'min' in stats and 'max' in stats:
                print(f"  Range: {stats.get('range', stats['max'] - stats['min']):.4f} (Min: {stats['min']:.4f}, Max: {stats['max']:.4f})")

            # IQR and quartiles
            if all(k in stats for k in ['25%', '75%']):
                iqr_value = stats.get('iqr', stats['75%'] - stats['25%'])
                print(f"  IQR: {iqr_value:.4f} (Q1: {stats['25%']:.4f}, Q3: {stats['75%']:.4f})")

            # Kurtosis and skewness
            if 'coef_variation' in stats:
                print(f"  Coefficient of Variation: {stats['coef_variation']:.4f}")

            # Show missing values
            missing = stats.get('missing', 0)
            missing_pct = stats.get('missing_pct', 0.0)
            print(f"  Data Points: {stats.get('data_points', 'N/A')} (Missing: {missing} - {missing_pct:.2f}%)")

def distribution_analysis(df):
    """
    Analyze distributions of numeric columns (skewness, kurtosis, normality).
    Returns a dictionary with distribution stats for each column.
    """
    result = {}
    for col in df.select_dtypes(include=['number']).columns:
        try:
            col_data = df[col].dropna()
            if len(col_data) < 8:  # Need sufficient data for distribution analysis
                result[col] = {
                    'error': 'Insufficient data points for distribution analysis',
                    'normality_test': None,
                    'is_normal': 'Unknown'
                }
                continue

            # Compute skewness and kurtosis
            skewness = col_data.skew()
            kurtosis = col_data.kurt()

            # Test for normality (Shapiro-Wilk)
            from scipy import stats as scipy_stats
            # Use sample if dataset is large (Shapiro-Wilk has a limit)
            sample = col_data.sample(min(5000, len(col_data))) if len(col_data) > 5000 else col_data
            shapiro_test = scipy_stats.shapiro(sample)

            # Test for normality with D'Agostino-Pearson test
            normality_test = scipy_stats.normaltest(sample)

            # Determine if distribution is normal based on tests and skewness
            # More cautious interpretation using both tests and skewness/kurtosis
            is_normal = "Yes" if (
                (shapiro_test.pvalue > 0.05 or normality_test.pvalue > 0.05) and  # At least one test passes
                abs(skewness) < 0.5 and  # Skewness within reasonable bounds
                abs(kurtosis - 3) < 1  # Kurtosis close to normal distribution value of 3
            ) else "No"

            result[col] = {
                'skewness': skewness,
                'kurtosis': kurtosis,
                'shapiro_test_pvalue': shapiro_test.pvalue,
                'dagostino_test_pvalue': normality_test.pvalue,
                'normality_test': normality_test,
                'is_normal': is_normal,
                'skew_interpretation': interpret_skewness(skewness),
                'kurtosis_interpretation': interpret_kurtosis(kurtosis),
                'transformation_suggestion': suggest_transformation(skewness, kurtosis)
            }
        except Exception as e:
            result[col] = {'error': str(e), 'normality_test': None, 'is_normal': 'Unknown'}

    return result

def interpret_skewness(skew):
    """
    Interpret the skewness value of a distribution.

    Parameters:
    - skew: Skewness value

    Returns:
    - String interpretation of the skewness
    """
    if abs(skew) < 0.5:
        return "Approximately symmetric"
    elif 0.5 <= skew < 1:
        return "Moderately positively skewed"
    elif skew >= 1:
        return "Highly positively skewed"
    elif -1 < skew <= -0.5:
        return "Moderately negatively skewed"
    else:  # skew <= -1
        return "Highly negatively skewed"

def interpret_kurtosis(kurt):
    """
    Interpret the kurtosis value of a distribution.

    Parameters:
    - kurt: Kurtosis value

    Returns:
    - String interpretation of the kurtosis
    """
    # Note: SciPy's kurtosis is already adjusted (excess kurtosis, normal = 0)
    # But pandas' kurt() returns the raw kurtosis where normal = 3
    if abs(kurt - 3) < 0.5:
        return "Mesokurtic (normal-like tails)"
    elif kurt < 3:
        return "Platykurtic (thinner tails than normal)"
    else:  # kurt > 3
        return "Leptokurtic (heavier tails than normal)"

def suggest_transformation(skew, kurt):
    """
    Suggest transformation based on skewness and kurtosis values.

    Parameters:
    - skew: Skewness value
    - kurt: Kurtosis value

    Returns:
    - String with transformation suggestion
    """
    # Default recommendation
    recommendation = "No transformation needed"

    # Check for extreme cases
    if abs(skew) >= 1 or abs(kurt - 3) >= 2:
        if skew > 1:
            if kurt > 5:  # Highly right-skewed with heavy tails
                recommendation = "Try log or Box-Cox transformation"
            else:
                recommendation = "Try square root transformation"
        elif skew < -1:  # Highly left-skewed
            recommendation = "Try square transformation or reflect-and-log"
        elif kurt > 5:  # Heavy tails but not highly skewed
            recommendation = "Consider Winsorizing outliers or robust scaling"
        elif kurt < 1:  # Very light tails
            recommendation = "Consider power transformation"
    elif 0.5 <= abs(skew) < 1:  # Moderate skewness
        if skew > 0:
            recommendation = "Consider mild transformation like square root"
        else:
            recommendation = "Consider mild power transformation"

    return recommendation

def time_series_analysis(df):
    """
    Perform time series analysis on dataframe.

    Parameters:
    - df: DataFrame to analyze, should contain price data and ideally a datetime column

    Returns:
    - Dictionary with time series analysis results
    """
    result = {
        'features': {},
        'stationarity': {},
        'seasonality': {},
    }

    # Check if dataframe has a datetime column or index
    has_date = False
    date_col = None

    # Check for datetime in index
    if pd.api.types.is_datetime64_any_dtype(df.index):
        has_date = True
    else:
        # Check for datetime columns
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                has_date = True
                date_col = col
                break

    # Create a synthetic datetime index if no datetime is found
    if not has_date:
        result['warning'] = "No datetime column found. Using synthetic datetime index."
        df = df.copy()
        df['synthetic_date'] = pd.date_range(start='2023-01-01', periods=len(df))
        date_col = 'synthetic_date'

    # Set datetime as index if it's not already
    if date_col is not None:
        df_ts = df.set_index(date_col)
    else:
        df_ts = df

    # Calculate price-based features (for OHLC data)
    ohlc_cols = {'open', 'high', 'low', 'close'}
    available_ohlc = ohlc_cols.intersection(set(df.columns))

    if len(available_ohlc) >= 2:
        # Calculate price range (high-low or equivalent)
        if all(col in df.columns for col in ['high', 'low']):
            df_ts['price_range'] = df['high'] - df['low']
            price_range = df_ts['price_range'].dropna()
            result['features']['price_range'] = {
                'mean': price_range.mean(),
                'median': price_range.median(),
                'std': price_range.std(),
                'min': price_range.min(),
                'max': price_range.max()
            }

        # Calculate price changes
        if 'close' in df.columns:
            df_ts['price_change'] = df['close'].diff()
            price_change = df_ts['price_change'].dropna()
            result['features']['price_change'] = {
                'mean': price_change.mean(),
                'median': price_change.median(),
                'std': price_change.std(),
                'min': price_change.min(),
                'max': price_change.max()
            }

            # Calculate percentage changes
            df_ts['pct_change'] = df['close'].pct_change() * 100
            pct_change = df_ts['pct_change'].dropna()
            result['features']['pct_change'] = {
                'mean': pct_change.mean(),
                'median': pct_change.median(),
                'std': pct_change.std(),
                'min': pct_change.min(),
                'max': pct_change.max()
            }

    # Perform stationarity tests on numeric columns
    for col in df.select_dtypes(include=['number']).columns:
        # Skip columns that are calculated above
        if col in ['price_range', 'price_change', 'pct_change']:
            continue

        # Need sufficient data for stationarity test
        if len(df[col].dropna()) < 10:
            continue

        try:
            # Perform Augmented Dickey-Fuller test
            adf_result = adfuller(df[col].dropna())

            result['stationarity'][col] = {
                'test_statistic': adf_result[0],
                'p_value': adf_result[1],
                'is_stationary': adf_result[1] < 0.05,  # p-value < 0.05 suggests stationarity
                'critical_values': adf_result[4]
            }
        except Exception as e:
            result['stationarity'][col] = {'error': str(e)}

    # Detect seasonality
    if has_date:
        try:
            # Extract day of week seasonality
            if len(df_ts.index) >= 7:  # Need at least a week of data
                day_of_week = df_ts.index.dayofweek.unique()

                # For each day, calculate mean of all numeric columns
                day_of_week_stats = {}

                # Use 'close' if available, otherwise use first numeric column
                if 'close' in df_ts.columns:
                    target_col = 'close'
                else:
                    target_col = df_ts.select_dtypes(include=['number']).columns[0]

                for day in sorted(day_of_week):
                    day_data = df_ts[df_ts.index.dayofweek == day][target_col].mean()
                    day_of_week_stats[int(day)] = day_data

                if len(day_of_week_stats) > 1:  # Only include if we have different days
                    result['seasonality']['day_of_week'] = day_of_week_stats

            # Extract month seasonality if enough data
            if df_ts.index.max() - df_ts.index.min() > pd.Timedelta(days=60):
                month_stats = {}

                if 'close' in df_ts.columns:
                    target_col = 'close'
                else:
                    target_col = df_ts.select_dtypes(include=['number']).columns[0]

                for month in sorted(df_ts.index.month.unique()):
                    month_data = df_ts[df_ts.index.month == month][target_col].mean()
                    month_stats[int(month)] = month_data

                if len(month_stats) > 1:  # Only include if we have different months
                    result['seasonality']['month'] = month_stats
        except Exception as e:
            result['seasonality']['error'] = str(e)

    return result

def print_time_series_analysis(ts_stats):
    """
    Print time series analysis results with color formatting.

    Parameters:
    - ts_stats: Dictionary returned by time_series_analysis function
    """
    print("\n\033[1m\033[95mTime Series Analysis:\033[0m")

    # Print any warnings
    if 'warning' in ts_stats:
        print(f"\n\033[93mWarning: {ts_stats['warning']}\033[0m")

    # Print features section
    if 'features' in ts_stats and ts_stats['features']:
        print("\n\033[94mFeatures:\033[0m")

        for feature_name, stats in ts_stats['features'].items():
            print(f"  \033[1m{feature_name}:\033[0m")
            for stat_name, value in stats.items():
                print(f"    {stat_name}: {value:.4f}")

    # Print stationarity results
    if 'stationarity' in ts_stats and ts_stats['stationarity']:
        print("\n\033[94mStationarity Tests:\033[0m")

        for col, results in ts_stats['stationarity'].items():
            if 'error' in results:
                print(f"  \033[1m{col}:\033[0m Error - {results['error']}")
                continue

            # Format output based on stationarity
            if results['is_stationary']:
                status = "\033[92mStationary\033[0m"
            else:
                status = "\033[91mNon-stationary\033[0m"

            print(f"  \033[1m{col}:\033[0m {status}")
            print(f"    ADF Test Statistic: {results['test_statistic']:.4f}")
            print(f"    p-value: {results['p_value']:.4f}")
            print("    Critical Values:")
            for significance, value in results['critical_values'].items():
                print(f"      {significance}: {value:.4f}")

    # Print seasonality information
    if 'seasonality' in ts_stats and ts_stats['seasonality']:
        print("\n\033[94mSeasonality:\033[0m")

        if 'error' in ts_stats['seasonality']:
            print(f"  Error: {ts_stats['seasonality']['error']}")

        if 'day_of_week' in ts_stats['seasonality']:
            print("  \033[1mWeekly seasonal patterns:\033[0m")
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for day_num, value in ts_stats['seasonality']['day_of_week'].items():
                day_name = days[day_num] if day_num < len(days) else f"Day {day_num}"
                print(f"    {day_name}: {value:.4f}")

        if 'month' in ts_stats['seasonality']:
            print("  \033[1mMonthly seasonal patterns:\033[0m")
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            for month_num, value in ts_stats['seasonality']['month'].items():
                month_name = months[month_num-1] if 0 < month_num <= 12 else f"Month {month_num}"
                print(f"    {month_name}: {value:.4f}")

    # Print recommendations
    print("\n\033[94mRecommendations:\033[0m")

    # Check for non-stationarity
    non_stationary_cols = []
    if 'stationarity' in ts_stats:
        for col, results in ts_stats['stationarity'].items():
            if 'is_stationary' in results and not results['is_stationary']:
                non_stationary_cols.append(col)

    if non_stationary_cols:
        print("  • \033[93mNon-stationary series detected:\033[0m")
        for col in non_stationary_cols:
            print(f"    - {col}")
        print("    - Consider differencing or detrending these series before modeling")
    else:
        print("  • \033[92mNo significant non-stationarity detected\033[0m")

    # Check for seasonality
    has_seasonality = False
    if 'seasonality' in ts_stats:
        if 'day_of_week' in ts_stats['seasonality'] or 'month' in ts_stats['seasonality']:
            has_seasonality = True

    if has_seasonality:
        print("  • \033[93mSeasonality patterns detected:\033[0m")
        print("    - Consider seasonal decomposition or including seasonal features in models")
    else:
        print("  • \033[92mNo strong seasonal patterns detected\033[0m")

    print("  • For further analysis:")
    print("    - Create ACF/PACF plots to identify AR/MA components")
    print("    - Consider ARIMA modeling for time series forecasting")
    print("    - Test for cointegration if analyzing multiple series")
