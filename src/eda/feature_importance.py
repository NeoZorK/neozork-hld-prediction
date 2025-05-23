# Handles feature importance analysis

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
from matplotlib.figure import Figure
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from src.eda.html_report_generator import HTMLReport, ensure_report_directory
from src.eda.correlation_analysis import ensure_plots_directory, compute_feature_importance, generate_feature_importance_plot, print_feature_importance

# Suppress matplotlib warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

def feature_importance_main(df, file_path=None, target_column=None, print_output=True, generate_report=True):
    """
    Main entry point for feature importance analysis. Encapsulates all functionality
    related to computing, visualizing, and reporting feature importance.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to analyze
    file_path : str or None
        Original file path for report generation
    target_column : str or None
        Target column for feature importance
    print_output : bool
        Whether to print results to console
    generate_report : bool
        Whether to generate HTML report

    Returns:
    --------
    dict
        Dictionary with feature importance analysis results
    str or None
        Path to the generated report if generate_report is True, else None
    """
    importance_result = compute_feature_importance(df, target_column)

    if print_output:
        print_feature_importance(importance_result)

    report_path = None
    if generate_report and file_path is not None:
        report_path = generate_feature_importance_report(df, file_path, target_column)

    return importance_result, report_path

def generate_feature_importance_report(df, file_path, target_column=None):
    """
    Generate a detailed HTML report for feature importance analysis.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to analyze
    file_path : str
        Path to the original data file
    target_column : str or None
        Target column for feature importance analysis

    Returns:
    --------
    str
        Path to the generated HTML report
    """
    # Create a new HTML report
    report = HTMLReport("Feature Importance Analysis", file_path)
    report.add_header()

    # Run feature importance analysis
    importance_result = compute_feature_importance(df, target_column)

    # Add overview section
    overview = f"""
    <p>This report analyzes the relative importance of features for predicting the target variable.</p>
    <p>Feature importance is calculated using a Random Forest model, which measures how much each feature contributes to prediction accuracy.</p>
    <p>Higher importance values indicate features that have greater influence on the model's predictions.</p>
    """

    if 'error' in importance_result:
        overview += f"<p><strong>Error:</strong> {importance_result['error']}</p>"
        report.add_section("Overview", overview)

        # Save the report even with error
        report_dir = ensure_report_directory(file_path)
        report_path = os.path.join(report_dir, "feature_importance_analysis.html")
        report.save(report_path)
        return report_path

    # Add target information to overview
    target_info = f"<p><strong>Target:</strong> {importance_result['target_column']} "
    target_info += f"({'Classification' if importance_result['is_classification'] else 'Regression'})</p>"
    overview += target_info

    report.add_section("Overview", overview)

    # Generate feature importance plot
    importance_fig = generate_feature_importance_plot(importance_result)

    # Add plot to the report
    report.add_plot(
        importance_fig,
        "Feature Importance",
        "This chart shows the relative importance of features for predicting the target variable, as determined by a Random Forest model. Features are sorted by importance, with percentages showing relative importance compared to the top feature.",
        "Higher importance values indicate features that contribute more to the model's predictive power. The color coding categorizes features into high (red), medium (yellow), and low (gray) importance groups.",
        "A diverse set of important features can indicate a robust model that captures multiple aspects of the data. Clear separation between important and unimportant features helps with feature selection.",
        "Reliance on just one or two features may indicate overfitting or a too-simplistic model. Low importance across all features may suggest the need for better feature engineering.",
        "Focus on features with high and medium importance for model development. Consider removing or aggregating features with very low importance to simplify the model."
    )

    # Create feature importance table
    feature_importances = importance_result['feature_importances']

    # Convert to DataFrame
    importance_df = pd.DataFrame(feature_importances)

    # Add importance category
    def get_importance_category(row):
        if row['normalized_importance'] >= 70:
            return 'High'
        elif row['normalized_importance'] >= 30:
            return 'Medium'
        else:
            return 'Low'

    importance_df['category'] = importance_df.apply(get_importance_category, axis=1)

    # Format for display
    display_df = importance_df[['feature', 'importance', 'normalized_importance', 'cumulative_importance', 'category']]
    display_df.columns = ['Feature', 'Importance', 'Relative Importance (%)', 'Cumulative Importance', 'Category']

    # Format numeric columns
    display_df['Importance'] = display_df['Importance'].apply(lambda x: f"{x:.4f}")
    display_df['Relative Importance (%)'] = display_df['Relative Importance (%)'].apply(lambda x: f"{x:.1f}%")
    display_df['Cumulative Importance'] = display_df['Cumulative Importance'].apply(lambda x: f"{x:.4f}")

    # Add to report
    report.add_table(
        display_df,
        "Feature Importance Rankings",
        "This table shows all features ranked by their importance scores, with relative importance as a percentage of the maximum importance. The cumulative importance column shows how the total feature importance accumulates as features are added in order of importance."
    )

    # Add feature groups section
    high_imp = importance_result['high_importance']
    med_imp = importance_result['medium_importance']
    low_imp = importance_result['low_importance']

    feature_groups = f"""
    <p>The features have been categorized into importance groups based on their relative importance:</p>
    <div class="feature-groups">
        <div class="feature-group high">
            <h4>High Importance ({len(high_imp)})</h4>
            <p>Features with ≥70% of the maximum importance:</p>
            <ul>
                {"".join([f'<li>{f["feature"]} ({f["normalized_importance"]:.1f}%)</li>' for f in high_imp]) if high_imp else "<li>None</li>"}
            </ul>
        </div>
        <div class="feature-group medium">
            <h4>Medium Importance ({len(med_imp)})</h4>
            <p>Features with 30-70% of the maximum importance:</p>
            <ul>
                {"".join([f'<li>{f["feature"]} ({f["normalized_importance"]:.1f}%)</li>' for f in med_imp[:10]]) + (f"<li>...and {len(med_imp) - 10} more</li>" if len(med_imp) > 10 else "") if med_imp else "<li>None</li>"}
            </ul>
        </div>
        <div class="feature-group low">
            <h4>Low Importance ({len(low_imp)})</h4>
            <p>Features with <30% of the maximum importance:</p>
            <ul>
                {"".join([f'<li>{f["feature"]} ({f["normalized_importance"]:.1f}%)</li>' for f in low_imp[:5]]) + (f"<li>...and {len(low_imp) - 5} more</li>" if len(low_imp) > 5 else "") if low_imp else "<li>None</li>"}
            </ul>
        </div>
    </div>
    <style>
        /* CSS styles for HTML report - IDE might show warnings but this is correct CSS syntax */
        /* noinspection CssUnresolvedReference */
        .feature-groups {
            display: flex; /* CSS flexbox layout - not a Python reference */
            flex-wrap: wrap; /* CSS flexbox property */
            gap: 20px; /* CSS grid/flex gap property */
        }
        /* noinspection CssUnresolvedReference */
        .feature-group {
            flex: 1; /* CSS flexbox property */
            min-width: 250px; /* CSS width property */
            padding: 15px; /* CSS padding property */
            border-radius: 5px; /* CSS border-radius property */
        }
        .high {
            background-color: #FFECEC; /* CSS color property */
            border-left: 5px solid #FF5733; /* CSS border property */
        }
        .medium {
            background-color: #FFF9E6; /* CSS color property */
            border-left: 5px solid #FFC300; /* CSS border property */
        }
        .low {
            background-color: #F2F2F2; /* CSS color property */
            border-left: 5px solid #C2C2C2; /* CSS border property */
        }
        .feature-group h4 {
            margin-top: 0; /* CSS margin property */
        }
    </style>
    """
    report.add_section("Feature Importance Groups", feature_groups, raw_html=True)

    # Add feature relationship plots
    figures = plot_feature_relationships(df, importance_result)

    # Add the pairplot first (should be the first figure)
    if figures and len(figures) > 0:
        report.add_plot(
            figures[0],
            "Feature Relationships",
            "This plot shows the relationships between the top features and the target variable. The diagonal shows the distribution of each variable.",
            "Examining these relationships can help understand how features interact with the target variable and with each other.",
            "Strong linear relationships with the target are good indicators of predictive power. Distributions should be well-behaved (not too skewed).",
            "No clear relationships with the target may suggest the need for feature transformations or more complex modeling approaches.",
            "Consider transformations (like log, sqrt) for highly skewed features. Look for non-linear patterns that might need specialized modeling."
        )

    # Add individual feature-target plots
    for i, fig in enumerate(figures[1:], 1):
        if i <= 5:  # Limit to top 5 features
            try:
                # Extract feature name from the title
                title = fig.axes[0].get_title()
                feature_name = title.split("vs")[0].strip().replace("Relationship: ", "")

                report.add_plot(
                    fig,
                    f"Relationship: {feature_name} vs Target",
                    f"This plot shows the relationship between {feature_name} and the target variable {importance_result['target_column']}.",
                    "The regression line indicates the general trend and direction of the relationship.",
                    "A clear linear relationship with little scatter suggests strong predictive power. Consistent trends are easier to model.",
                    "High scatter or no clear pattern may indicate a weak relationship or the need for additional features.",
                    "Consider transformations if the relationship appears non-linear. Watch for outliers that may distort the relationship."
                )
            except Exception as e:
                # Skip if there's an error with a particular plot
                continue

    # Add cumulative importance analysis
    cum_importance_threshold = 0.95  # 95% of total importance
    features_for_95pct = 0

    for i, feature in enumerate(feature_importances):
        if feature['cumulative_importance'] >= cum_importance_threshold:
            features_for_95pct = i + 1
            break

    if features_for_95pct > 0:
        cum_features = ", ".join([f["feature"] for f in feature_importances[:features_for_95pct]])

        cumulative_analysis = f"""
        <p>The top {features_for_95pct} features (out of {len(feature_importances)}) account for {cum_importance_threshold*100}% of the total feature importance:</p>
        <p><strong>{cum_features}</strong></p>
        <p>This suggests that a simplified model using only these features might perform nearly as well as one using all features.</p>
        """
        report.add_section("Cumulative Feature Importance", cumulative_analysis)

    # Add summary and recommendations
    recommendations = []

    if len(high_imp) <= 3 and len(high_imp) > 0:
        recommendations.append(f"<li><strong>Key Predictors:</strong> The model relies heavily on a small number of features. Consider focusing analysis on {', '.join([f['feature'] for f in high_imp])}.</li>")
    elif len(high_imp) > 3:
        recommendations.append(f"<li><strong>Diverse Predictors:</strong> The model uses multiple important features, suggesting complex relationships in the data.</li>")
    else:  # no high importance features
        recommendations.append("<li><strong>No Dominant Features:</strong> No features stand out as particularly important, suggesting either that all features contribute similarly or that better features may be needed.</li>")

    if len(low_imp) > len(feature_importances) * 0.5:
        recommendations.append(f"<li><strong>Feature Reduction Opportunity:</strong> Over 50% of features have low importance. Consider removing these {len(low_imp)} low-importance features to simplify the model.</li>")

    if features_for_95pct < len(feature_importances) * 0.5:
        recommendations.append(f"<li><strong>Efficient Feature Subset:</strong> Just {features_for_95pct} features ({(features_for_95pct/len(feature_importances)*100):.1f}% of total) account for 95% of total importance. Consider using only these top features for a simpler model.</li>")

    summary_content = f"""
    <p>Based on the feature importance analysis for predicting <strong>{importance_result['target_column']}</strong>, here are the key findings and recommendations:</p>
    <ul>
        {"".join(recommendations)}
        <li><strong>Next Steps:</strong>
            <ul>
                <li>Perform cross-validation to verify that the identified important features generalize well</li>
                <li>Consider feature engineering to combine or transform the most important features</li>
                <li>Use these insights to build more focused and interpretable models</li>
            </ul>
        </li>
    </ul>
    """
    report.add_section("Summary and Recommendations", summary_content)

    # Save the report
    report_dir = ensure_report_directory(file_path)
    report_path = os.path.join(report_dir, "feature_importance_analysis.html")
    report.save(report_path)

    return report_path

def plot_feature_relationships(df, importance_result):
    """
    Generate plots showing relationships between the top features and the target.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with features and target
    importance_result : dict
        Results from compute_feature_importance function

    Returns:
    --------
    list
        List of matplotlib figures showing feature relationships
    """
    if 'error' in importance_result:
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f"Error: {importance_result['error']}", ha='center', va='center')
        return [fig]

    target_column = importance_result['target_column']
    top_features = [f['feature'] for f in importance_result['feature_importances'][:5]]  # Get top 5 features

    figures = []

    # Generate pairwise plots for top features and target
    columns_to_plot = top_features + [target_column]

    # Check that all columns exist in dataframe
    valid_columns = [col for col in columns_to_plot if col in df.columns]
    if len(valid_columns) < 2:
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "Error: Not enough valid columns for relationship plots", ha='center', va='center')
        return [fig]

    # Create pairplot for top features
    try:
        plt.figure(figsize=(12, 10))
        pair_plot = sns.pairplot(
            df[valid_columns],
            diag_kind='kde',
            corner=True,  # Only show lower triangle
            plot_kws={'alpha': 0.6}
        )
        plt.suptitle('Relationships Between Top Features and Target', y=1.02, fontsize=16)
        fig_pairplot = pair_plot.fig
        figures.append(fig_pairplot)
    except Exception as e:
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f"Error creating pairplot: {e}", ha='center', va='center')
        figures.append(fig)

    # Create individual scatter plots for top features vs target
    for feature in top_features:
        if feature in df.columns and target_column in df.columns:
            try:
                fig = Figure(figsize=(10, 6))
                ax = fig.add_subplot(111)

                # Create scatter plot with regression line
                sns.regplot(
                    x=feature,
                    y=target_column,
                    data=df,
                    scatter_kws={'alpha': 0.5},
                    line_kws={'color': 'red'},
                    ax=ax
                )

                ax.set_title(f'Relationship: {feature} vs {target_column}')
                ax.set_xlabel(feature)
                ax.set_ylabel(target_column)

                # Add correlation coefficient
                correlation = df[[feature, target_column]].corr().iloc[0, 1]
                ax.annotate(
                    f'Correlation: {correlation:.3f}',
                    xy=(0.05, 0.95),
                    xycoords='axes fraction',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8)
                )

                fig.tight_layout()
                figures.append(fig)
            except Exception as e:
                fig = Figure(figsize=(6, 4))
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, f"Error creating plot for {feature}: {e}", ha='center', va='center')
                figures.append(fig)

    return figures

def save_feature_relationships_plots(df, importance_result, base_filename='feature_relationships'):
    """
    Generate and save plots showing relationships between top features and target.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with features and target
    importance_result : dict
        Results from compute_feature_importance function
    base_filename : str
        Base filename for saving plots

    Returns:
    --------
    list
        List of paths to the saved plots
    """
    figures = plot_feature_relationships(df, importance_result)
    plots_dir = ensure_plots_directory()

    saved_paths = []
    for i, fig in enumerate(figures):
        plot_path = os.path.join(plots_dir, f'{base_filename}_{i}.png')
        fig.savefig(plot_path)
        saved_paths.append(plot_path)
        plt.close(fig)

    return saved_paths

def feature_importance_cli(df, target_column=None, file_path=None):
    """
    CLI wrapper for feature importance analysis.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to analyze
    target_column : str or None
        Target column for feature importance
    file_path : str or None
        Original file path for report generation

    Returns:
    --------
    dict
        Dictionary with feature importance analysis results
    """
    # Run feature importance analysis
    importance_result, report_path = feature_importance_main(
        df,
        file_path=file_path,
        target_column=target_column
    )

    # Generate relationship plots if analysis was successful
    if 'error' not in importance_result:
        plot_paths = save_feature_relationships_plots(df, importance_result)

        # Print paths to generated plots
        if plot_paths:
            print(f"\n\033[93m[INFO]\033[0m Generated {len(plot_paths)} feature relationship plots:")
            for path in plot_paths:
                print(f"  - {path}")

    # Print report path if generated
    if report_path:
        print(f"\n\033[93m[INFO]\033[0m Feature importance report saved to: {report_path}")

    return importance_result

def generate_global_feature_importance_summary(feature_importance_results, file_paths, output_path=None):
    """
    Generate a global statistical analysis summary for feature importance across multiple files.

    Parameters:
    -----------
    feature_importance_results : list
        List of dictionaries containing feature importance results
    file_paths : list
        List of file paths corresponding to the results
    output_path : str or None
        Path where to save the HTML report (default: results/reports/global_feature_importance_summary.html)

    Returns:
    --------
    str
        Path to the generated HTML report
    """
    # Ensure output path exists
    if output_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        reports_dir = os.path.join(base_dir, 'results', 'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        output_path = os.path.join(reports_dir, 'global_feature_importance_summary.html')

    # Collect all important features across files
    all_important_features = []
    total_files = len(feature_importance_results)
    total_features_analyzed = 0

    for i, result in enumerate(feature_importance_results):
        if 'error' in result:
            continue

        file_name = os.path.basename(file_paths[i])

        if 'feature_importances' in result:
            total_features_analyzed += len(result['feature_importances'])

            for feature in result['feature_importances']:
                all_important_features.append({
                    'file': file_name,
                    'feature': feature['feature'],
                    'importance': feature['importance'],
                    'normalized_importance': feature['normalized_importance']
                })

    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Глобальный анализ важности признаков</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #3498db;
        }}
        .overall-stats {{
            background-color: #3498db;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .overall-stats h2 {{
            color: white;
            margin-top: 0;
        }}
        .file-card {{
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-left: 5px solid #3498db;
        }}
        .file-title {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        .file-title h3 {{
            margin: 0;
            color: #2980b9;
        }}
        .feature-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        .feature-table th, .feature-table td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        .feature-table th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .importance-bar {{
            height: 20px;
            background-color: #f1c40f;
            border-radius: 3px;
        }}
        .high-importance {{
            background-color: #e74c3c;
        }}
        .medium-importance {{
            background-color: #f39c12;
        }}
        .low-importance {{
            background-color: #95a5a6;
        }}
        .summary-section {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
        }}
        .summary-section h2 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        .importance-category {{
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }}
        .importance-color {{
            width: 15px;
            height: 15px;
            display: inline-block;
            margin-right: 8px;
            border-radius: 3px;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .top-features-card {{
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .top-features-card h4 {{
            color: #3498db;
            margin-top: 0;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        .feature-badge {{
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            margin: 3px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>Отчёт по глобальному анализу важности признаков</h1>
    
    <div class="overall-stats">
        <h2>Общая статистика</h2>
        <p><strong>Проанализированных файлов:</strong> {total_files}</p>
        <p><strong>Всего признаков проанализировано:</strong> {total_features_analyzed}</p>
        <p><strong>Обнаружено важных признаков:</strong> {len(all_important_features)}</p>
    </div>"""

    # Add file-specific cards for top files (limit to 5)
    unique_files = set(item['file'] for item in all_important_features)
    for i, file_name in enumerate(unique_files):
        if i >= 5:  # Limit to 5 files
            break

        file_features = [f for f in all_important_features if f['file'] == file_name]
        target_column = next((result['target_column'] for result, path in zip(feature_importance_results, file_paths)
                            if os.path.basename(path) == file_name and 'target_column' in result), "Unknown")

        # Sort by importance
        file_features.sort(key=lambda x: x['importance'], reverse=True)

        html_content += f"""
    <div class="file-card">
        <div class="file-title">
            <h3>{file_name.replace('.parquet', '')}</h3>
            <span>Целевой признак: <strong>{target_column}</strong></span>
        </div>
        
        <p><strong>Количество признаков:</strong> {len(file_features)}</p>
        
        <h4>Распределение важности признаков</h4>
        <table class="feature-table">
            <thead>
                <tr>
                    <th>Признак</th>
                    <th>Важность</th>
                    <th>Нормализованная важность</th>
                    <th>Визуализация</th>
                </tr>
            </thead>
            <tbody>"""

        # Add top 8 features
        for feature in file_features[:8]:
            importance_class = "high-importance" if feature['normalized_importance'] >= 70 else \
                              "medium-importance" if feature['normalized_importance'] >= 30 else \
                              "low-importance"

            html_content += f"""
                <tr>
                    <td>{feature['feature']}</td>
                    <td>{feature['importance']:.3f}</td>
                    <td>{feature['normalized_importance']:.1f}%</td>
                    <td><div class="importance-bar {importance_class}" style="width: {min(100, max(1, feature['normalized_importance']))}%"></div></td>
                </tr>"""

        html_content += """
            </tbody>
        </table>
    </div>"""

    # Group features by importance across files
    high_importance_features = {}
    medium_importance_features = {}
    low_importance_features = {}

    for feature_data in all_important_features:
        feature_name = feature_data['feature']
        importance = feature_data['normalized_importance']
        file_name = feature_data['file']

        if importance >= 70:
            if feature_name not in high_importance_features:
                high_importance_features[feature_name] = []
            high_importance_features[feature_name].append((file_name, importance))
        elif importance >= 30:
            if feature_name not in medium_importance_features:
                medium_importance_features[feature_name] = []
            medium_importance_features[feature_name].append((file_name, importance))
        else:
            if feature_name not in low_importance_features:
                low_importance_features[feature_name] = []
            low_importance_features[feature_name].append((file_name, importance))

    # Sort features by maximum importance
    high_importance_features = {k: v for k, v in sorted(
        high_importance_features.items(),
        key=lambda item: max(x[1] for x in item[1]),
        reverse=True
    )}

    medium_importance_features = {k: v for k, v in sorted(
        medium_importance_features.items(),
        key=lambda item: max(x[1] for x in item[1]),
        reverse=True
    )}

    # Add top features section
    html_content += """
    <div class="summary-section">
        <h2>Ключевые признаки по категориям важности</h2>
        
        <div class="grid-container">"""

    # High importance features card
    html_content += """
            <div class="top-features-card">
                <h4>Признаки высокой важности (≥70%)</h4>"""

    if high_importance_features:
        for feature_name, occurrences in high_importance_features.items():
            max_importance = max(imp for _, imp in occurrences)
            file_count = len(occurrences)
            html_content += f"""
                <div class="feature-badge" title="Максимальная важность: {max_importance:.1f}%, Встречается в {file_count} файлах">
                    {feature_name}
                </div>"""
    else:
        html_content += """
                <p>Не обнаружено признаков высокой важности</p>"""

    html_content += """
            </div>"""

    # Medium importance features card
    html_content += """
            <div class="top-features-card">
                <h4>Признаки средней важности (30-70%)</h4>"""

    if medium_importance_features:
        # Limit to top 15 medium importance features
        count = 0
        for feature_name, occurrences in medium_importance_features.items():
            if count >= 15:
                break
            max_importance = max(imp for _, imp in occurrences)
            file_count = len(occurrences)
            html_content += f"""
                <div class="feature-badge" title="Максимальная важность: {max_importance:.1f}%, Встречается в {file_count} файлах">
                    {feature_name}
                </div>"""
            count += 1

        if len(medium_importance_features) > 15:
            html_content += f"""
                <p>...и еще {len(medium_importance_features) - 15} признаков средней важности</p>"""
    else:
        html_content += """
                <p>Не обнаружено признаков средней важности</p>"""

    html_content += """
            </div>
        </div>"""

    # Add cross-file analysis section
    most_common_features = {}
    for feature_data in all_important_features:
        feature_name = feature_data['feature']
        if feature_name not in most_common_features:
            most_common_features[feature_name] = 0
        most_common_features[feature_name] += 1

    # Sort by frequency
    most_common_features = {k: v for k, v in sorted(
        most_common_features.items(),
        key=lambda item: item[1],
        reverse=True
    )}

    html_content += """
        <h3>Частота появления признаков в разных файлах</h3>
        <table class="feature-table">
            <thead>
                <tr>
                    <th>Признак</th>
                    <th>Количество файлов</th>
                    <th>% от общего числа файлов</th>
                </tr>
            </thead>
            <tbody>"""

    # Add top 10 most common features
    for i, (feature_name, count) in enumerate(most_common_features.items()):
        if i >= 10:  # Limit to 10 features
            break
        percentage = (count / total_files) * 100
        html_content += f"""
                <tr>
                    <td>{feature_name}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>"""

    html_content += """
            </tbody>
        </table>"""

    # Add recommendations section
    html_content += """
        <h3>Выводы и рекомендации</h3>
        
        <h4>Ключевые наблюдения:</h4>
        <ul>"""

    if high_importance_features:
        top_high_feature = next(iter(high_importance_features))
        html_content += f"""
            <li>Признак <strong>{top_high_feature}</strong> имеет высокую важность и может быть ключевым предиктором в большинстве моделей</li>"""

    if len(high_importance_features) <= 3:
        html_content += """
            <li>Относительно небольшое число признаков имеет высокую важность, что говорит о концентрации полезной информации в нескольких ключевых переменных</li>"""
    else:
        html_content += """
            <li>Множество признаков имеют высокую важность, что говорит о сложной структуре данных и богатом информационном содержании набора признаков</li>"""

    html_content += """
        </ul>
        
        <h4>Рекомендации:</h4>
        <ul>
            <li><strong>Упрощение модели:</strong> Рассмотреть возможность построения моделей на основе только наиболее важных признаков</li>
            <li><strong>Инженерия признаков:</strong> Создать новые признаки, которые комбинируют или трансформируют высокоинформативные переменные</li>
            <li><strong>Анализ мультиколлинеарности:</strong> Проверить зависимости между важными признаками, чтобы избежать дублирования информации</li>
            <li><strong>Стратегия моделирования:</strong> Использовать стекинг или ансамблевые модели, учитывающие различную важность признаков в разных наборах данных</li>
        </ul>
        
        <h4>Дальнейшие шаги:</h4>
        <ul>
            <li>Провести кросс-валидацию моделей с различными наборами признаков для определения оптимального баланса между сложностью и производительностью</li>
            <li>Изучить временные паттерны в важности признаков для разных периодов данных</li>
            <li>Применить методы снижения размерности (PCA, t-SNE) для визуализации структуры данных в пространстве признаков</li>
        </ul>
    </div>
</body>
</html>"""

    # Write the HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path
