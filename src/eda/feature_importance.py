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
        .feature-groups {
            display: flex; /* CSS flexbox layout - not a Python reference */
            flex-wrap: wrap; /* CSS flexbox property */
            gap: 20px; /* CSS grid/flex gap property */
        }
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
