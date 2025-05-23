# Handles correlation analysis

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
import io
import base64
from matplotlib.figure import Figure
from scipy.stats import spearmanr, pearsonr
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from src.eda.html_report_generator import HTMLReport, ensure_report_directory

# Suppress matplotlib warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

def ensure_plots_directory():
    """Ensure plots directory exists for saving visualizations."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    plots_dir = os.path.join(base_dir, 'results', 'plots')

    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    return plots_dir

def compute_correlation(df, method='pearson'):
    """
    Compute correlation matrix between numeric features in DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame for correlation analysis
    method : str
        Correlation method. Options: 'pearson' or 'spearman'

    Returns:
    --------
    dict
        Dictionary with correlation matrices and strong correlations
    """
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=['number'])

    # Compute correlation
    if len(numeric_df.columns) < 2:
        return {
            'error': 'Not enough numeric columns for correlation analysis',
            'min_columns': 2,
            'found_columns': len(numeric_df.columns)
        }

    try:
        # Compute correlation matrix
        corr_matrix = numeric_df.corr(method=method)

        # Find strong correlations (excluding self-correlations)
        strong_corr = []
        # Get the upper triangular of the correlation matrix to avoid duplicates
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                corr_val = corr_matrix.iloc[i, j]

                if abs(corr_val) > 0.7:  # Strong correlation threshold
                    strong_corr.append({
                        'column1': col1,
                        'column2': col2,
                        'correlation': corr_val,
                        'strength': 'Very Strong' if abs(corr_val) > 0.9 else 'Strong'
                    })

        # Sort by absolute correlation value
        strong_corr = sorted(strong_corr, key=lambda x: abs(x['correlation']), reverse=True)

        return {
            'matrix': corr_matrix,
            'strong_correlations': strong_corr,
            'method': method,
            'columns': list(corr_matrix.columns)
        }
    except Exception as e:
        return {'error': str(e)}

def generate_correlation_plot(corr_result, title='Correlation Matrix'):
    """
    Generate a correlation heatmap visualization.

    Parameters:
    -----------
    corr_result : dict
        Results from compute_correlation function
    title : str
        Title for the plot

    Returns:
    --------
    matplotlib.figure.Figure
        The generated figure
    """
    if 'error' in corr_result:
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f"Error: {corr_result['error']}", ha='center', va='center')
        return fig

    corr_matrix = corr_result['matrix']
    method = corr_result['method']

    # Generate heatmap
    fig = Figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    # Create a mask for the upper triangle
    mask = np.zeros_like(corr_matrix, dtype=bool)
    mask[np.triu_indices_from(mask, 1)] = True

    # Generate a custom colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap
    sns.heatmap(
        corr_matrix,
        mask=mask,
        cmap=cmap,
        vmax=1,
        vmin=-1,
        center=0,
        square=True,
        linewidths=.5,
        cbar_kws={"shrink": .8},
        annot=True,
        fmt=".2f",
        ax=ax
    )

    # Set title and adjust layout
    ax.set_title(f"{title} ({method.capitalize()} Method)")
    fig.tight_layout()

    return fig

def print_correlation_analysis(corr_result):
    """
    Print correlation analysis results with color formatting.

    Parameters:
    -----------
    corr_result : dict
        Results from the compute_correlation function
    """
    print("\n\033[1m\033[95mCorrelation Analysis:\033[0m")

    if 'error' in corr_result:
        print(f"\n\033[91mError: {corr_result['error']}\033[0m")
        return

    method = corr_result['method']
    print(f"\n\033[93mMethod: {method.capitalize()}\033[0m")

    # Print strong correlations
    strong_correlations = corr_result['strong_correlations']

    if not strong_correlations:
        print("\n\033[94mNo strong correlations found (threshold: 0.7)\033[0m")
    else:
        print(f"\n\033[94mStrong Correlations (|r| > 0.7): {len(strong_correlations)}\033[0m")

        for idx, corr in enumerate(strong_correlations[:10], 1):  # Show top 10
            col1 = corr['column1']
            col2 = corr['column2']
            corr_val = corr['correlation']
            strength = corr['strength']

            # Color code based on correlation value
            if abs(corr_val) > 0.9:
                color_code = "\033[91m"  # Red for very strong
            elif abs(corr_val) > 0.8:
                color_code = "\033[93m"  # Yellow for strong
            else:
                color_code = "\033[96m"  # Cyan for moderate

            # Direction of correlation
            direction = "positive" if corr_val > 0 else "negative"

            print(f"  {idx}. {col1} ↔ {col2}: {color_code}{corr_val:.3f}\033[0m ({direction}, {strength})")

        # Show message if there are more correlations
        if len(strong_correlations) > 10:
            print(f"  ... and {len(strong_correlations) - 10} more strong correlations")

    # Print interpretation and recommendations
    print("\n\033[94mInterpretation:\033[0m")
    if strong_correlations:
        print("  • Strong correlations indicate features that vary together")
        print("  • For predictive modeling, consider:")
        print("    - Removing one feature from highly correlated pairs (|r| > 0.9) to reduce multicollinearity")
        print("    - Using dimensionality reduction techniques like PCA")
        if method == 'pearson':
            print("  • Pearson correlation measures linear relationships; consider Spearman for non-linear patterns")
        else:
            print("  • Spearman correlation captures monotonic relationships, including non-linear patterns")
    else:
        print("  • No strong linear correlations between features")
        print("  • Features appear to be relatively independent")
        print("  • Consider:")
        print("    - Checking for non-linear relationships")
        print("    - Feature engineering to create more informative predictors")

    # Generate visualization
    plots_dir = ensure_plots_directory()
    fig = generate_correlation_plot(corr_result)
    plot_path = os.path.join(plots_dir, f'correlation_{method}.png')
    fig.savefig(plot_path)
    print(f"\n\033[93m[INFO]\033[0m Correlation heatmap saved to: {plot_path}")

def compute_feature_importance(df, target_column=None):
    """
    Compute feature importance using a Random Forest model.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame for feature importance analysis
    target_column : str or None
        Target column for feature importance. If None, attempts to detect a target.

    Returns:
    --------
    dict
        Dictionary with feature importances and analysis results
    """
    # Select numeric columns
    numeric_df = df.select_dtypes(include=['number'])

    if len(numeric_df.columns) < 2:
        return {
            'error': 'Not enough numeric columns for feature importance analysis',
            'min_columns': 2,
            'found_columns': len(numeric_df.columns)
        }

    # Try to identify a target if not specified
    if target_column is None:
        # Common target column names
        common_targets = ['target', 'label', 'class', 'outcome', 'response', 'y']
        for col in common_targets:
            if col in df.columns:
                target_column = col
                break

        # If still not found, try to find columns with 'target' or 'pred' in name
        if target_column is None:
            for col in df.columns:
                if 'target' in col.lower() or 'pred' in col.lower():
                    target_column = col
                    break

        # For financial data, let's try to use 'close' or price-related columns as targets
        if target_column is None:
            # Look for typical price targets in financial data
            price_targets = ['next_day_close', 'future_price', 'return', 'next_return']
            for col in price_targets:
                if col in df.columns:
                    target_column = col
                    break

            # Use close as a fallback for price prediction (if it exists)
            if target_column is None and 'close' in df.columns:
                # Create a future price column as target
                target_column = 'future_close'
                df[target_column] = df['close'].shift(-1)  # Next day's close price

    if target_column is None:
        return {'error': 'No target column specified or detected'}

    if target_column not in df.columns:
        return {'error': f'Target column "{target_column}" not found in DataFrame'}

    try:
        # Prepare data
        X = df.drop(columns=[target_column]).select_dtypes(include=['number'])
        y = df[target_column]

        # Handle missing values in the target
        if y.isna().any():
            y = y.dropna()
            X = X.loc[y.index]

        # Check if we have enough data
        if len(X) < 10:  # Arbitrary minimum number of samples
            return {
                'error': 'Not enough samples for feature importance analysis',
                'min_samples': 10,
                'found_samples': len(X)
            }

        # Determine if classification or regression
        is_classification = False
        if pd.api.types.is_categorical_dtype(y) or y.nunique() <= 10:
            is_classification = True
            # Encode categorical target
            le = LabelEncoder()
            y = le.fit_transform(y)

        # Choose model based on problem type
        if is_classification:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)

        # Fit model
        model.fit(X, y)

        # Get feature importances
        importances = model.feature_importances_

        # Create sorted list of feature importances
        feature_importances = []
        for i, feature_name in enumerate(X.columns):
            feature_importances.append({
                'feature': feature_name,
                'importance': importances[i],
                'normalized_importance': importances[i] / importances.max() * 100  # As percentage of max
            })

        # Sort by importance, descending
        feature_importances = sorted(feature_importances, key=lambda x: x['importance'], reverse=True)

        # Calculate cumulative importance
        cumulative = 0
        for feature in feature_importances:
            cumulative += feature['importance']
            feature['cumulative_importance'] = cumulative

        # Group features by importance
        high_importance = []
        medium_importance = []
        low_importance = []

        for feature in feature_importances:
            if feature['normalized_importance'] >= 70:  # 70% of max importance
                high_importance.append(feature)
            elif feature['normalized_importance'] >= 30:  # 30-70% of max importance
                medium_importance.append(feature)
            else:
                low_importance.append(feature)

        return {
            'feature_importances': feature_importances,
            'high_importance': high_importance,
            'medium_importance': medium_importance,
            'low_importance': low_importance,
            'target_column': target_column,
            'is_classification': is_classification,
            'num_features': len(X.columns),
            'top_features': [f['feature'] for f in feature_importances[:5]]  # Top 5 features
        }

    except Exception as e:
        return {'error': str(e)}

def generate_feature_importance_plot(importance_result):
    """
    Generate a feature importance visualization.

    Parameters:
    -----------
    importance_result : dict
        Results from compute_feature_importance function

    Returns:
    --------
    matplotlib.figure.Figure
        The generated figure
    """
    if 'error' in importance_result:
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f"Error: {importance_result['error']}", ha='center', va='center')
        return fig

    feature_importances = importance_result['feature_importances']
    target_column = importance_result['target_column']
    is_classification = importance_result['is_classification']

    # Create horizontal bar plot of feature importances
    fig = Figure(figsize=(12, max(6, len(feature_importances) * 0.3)))  # Dynamic height
    ax = fig.add_subplot(111)

    # Extract data for plotting
    features = [item['feature'] for item in feature_importances]
    importances = [item['importance'] for item in feature_importances]
    normalized = [item['normalized_importance'] for item in feature_importances]

    # Generate colors based on importance level
    colors = []
    for imp in normalized:
        if imp >= 70:
            colors.append('#FF5733')  # High importance (red)
        elif imp >= 30:
            colors.append('#FFC300')  # Medium importance (yellow)
        else:
            colors.append('#C2C2C2')  # Low importance (gray)

    # Plot horizontal bars
    bars = ax.barh(features, importances, color=colors)

    # Add importance percentages
    for i, bar in enumerate(bars):
        width = bar.get_width()
        label_x_pos = width * 1.01  # Slightly to the right of the bar
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{normalized[i]:.1f}%',
                va='center', color='black', fontsize=8)

    # Set labels and title
    model_type = "Classification" if is_classification else "Regression"
    ax.set_xlabel('Feature Importance')
    ax.set_title(f'Feature Importance for {target_column} ({model_type})')

    # Add a legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FF5733', label='High Importance (>= 70%)'),
        Patch(facecolor='#FFC300', label='Medium Importance (30-70%)'),
        Patch(facecolor='#C2C2C2', label='Low Importance (< 30%)')
    ]
    ax.legend(handles=legend_elements, loc='lower right')

    fig.tight_layout()
    return fig

def print_feature_importance(importance_result):
    """
    Print feature importance analysis results with color formatting.

    Parameters:
    -----------
    importance_result : dict
        Results from the compute_feature_importance function
    """
    print("\n\033[1m\033[95mFeature Importance Analysis:\033[0m")

    if 'error' in importance_result:
        print(f"\n\033[91mError: {importance_result['error']}\033[0m")
        return

    target_column = importance_result['target_column']
    is_classification = importance_result['is_classification']
    feature_importances = importance_result['feature_importances']

    model_type = "Classification" if is_classification else "Regression"
    print(f"\n\033[93mTarget: {target_column} ({model_type})\033[0m")
    print(f"\033[93mFeatures analyzed: {importance_result['num_features']}\033[0m")

    # Print top features
    print(f"\n\033[94mTop 10 Most Important Features:\033[0m")
    for idx, feature in enumerate(feature_importances[:10], 1):
        feature_name = feature['feature']
        importance = feature['importance']
        norm_importance = feature['normalized_importance']

        # Color code based on importance
        if norm_importance >= 70:
            color_code = "\033[91m"  # Red for high importance
        elif norm_importance >= 30:
            color_code = "\033[93m"  # Yellow for medium importance
        else:
            color_code = "\033[96m"  # Cyan for low importance

        print(f"  {idx}. {feature_name}: {color_code}{importance:.4f}\033[0m ({norm_importance:.1f}%)")

    # Print feature groups
    high_imp = importance_result['high_importance']
    med_imp = importance_result['medium_importance']
    low_imp = importance_result['low_importance']

    print(f"\n\033[94mFeatures by Importance Level:\033[0m")
    print(f"  \033[91mHigh Importance ({len(high_imp)}):\033[0m " +
          (", ".join([f['feature'] for f in high_imp]) if high_imp else "None"))
    print(f"  \033[93mMedium Importance ({len(med_imp)}):\033[0m " +
          (", ".join([f['feature'] for f in med_imp[:5]]) +
           (f" and {len(med_imp) - 5} more..." if len(med_imp) > 5 else "") if med_imp else "None"))
    print(f"  \033[96mLow Importance ({len(low_imp)}):\033[0m " +
          (", ".join([f['feature'] for f in low_imp[:3]]) +
           (f" and {len(low_imp) - 3} more..." if len(low_imp) > 3 else "") if low_imp else "None"))

    # Print interpretation and recommendations
    print("\n\033[94mInterpretation:\033[0m")
    print("  • Higher importance scores indicate features with greater predictive power")

    if len(high_imp) <= 3:
        print("  • A small number of features dominate the model's decisions")
        print("  • This suggests that the model is relying heavily on a few key indicators")
    else:
        print("  • The model uses a good mix of features for predictions")
        print("  • Multiple features contribute significantly to the model's decisions")

    print("\n\033[94mRecommendations:\033[0m")
    print("  • Prioritize high-importance features for further analysis and feature engineering")
    print("  • Consider removing or combining low-importance features to simplify the model")

    if len(high_imp) == 0:
        print("  • No standout features - consider creating more informative features")

    if len(low_imp) > len(high_imp) + len(med_imp):
        print("  • Many low-importance features suggest opportunity for dimensionality reduction")

    # Generate visualization
    plots_dir = ensure_plots_directory()
    fig = generate_feature_importance_plot(importance_result)
    plot_path = os.path.join(plots_dir, 'feature_importance.png')
    fig.savefig(plot_path)
    print(f"\n\033[93m[INFO]\033[0m Feature importance plot saved to: {plot_path}")

def generate_correlation_report(df, file_path):
    """
    Generate a detailed HTML report for correlation analysis.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to analyze
    file_path : str
        Path to the original data file

    Returns:
    --------
    str
        Path to the generated HTML report
    """
    # Create a new HTML report
    report = HTMLReport("Correlation Analysis", file_path)
    report.add_header()

    # Add overview section
    overview = """
    <p>This report provides correlation analysis between numeric features in the dataset.</p>
    <p>Correlations measure the strength and direction of linear relationships between pairs of features:</p>
    <ul>
        <li><strong>+1</strong>: Perfect positive correlation (as one variable increases, the other increases proportionally)</li>
        <li><strong>0</strong>: No correlation (variables are unrelated)</li>
        <li><strong>-1</strong>: Perfect negative correlation (as one variable increases, the other decreases proportionally)</li>
    </ul>
    <p>This analysis uses both Pearson (linear relationships) and Spearman (monotonic relationships) correlation methods.</p>
    """
    report.add_section("Overview", overview)

    # Pearson correlation
    pearson_result = compute_correlation(df, method='pearson')

    if 'error' in pearson_result:
        report.add_section("Error", f"<p>Could not compute correlation: {pearson_result['error']}</p>")

        # Save the report
        report_dir = ensure_report_directory(file_path)
        report_path = os.path.join(report_dir, "correlation_analysis.html")
        report.save(report_path)
        return report_path

    # Generate Pearson correlation plot
    pearson_fig = generate_correlation_plot(pearson_result, "Pearson Correlation Matrix")

    # Add correlation heatmap to the report
    report.add_plot(
        pearson_fig,
        "Pearson Correlation Matrix",
        "The heatmap shows Pearson correlation coefficients between pairs of numeric features. Blue indicates positive correlation, red indicates negative correlation, and the intensity represents the strength of correlation.",
        "Correlation coefficients range from -1 (perfect negative correlation) to +1 (perfect positive correlation). Values close to 0 indicate weak or no linear relationship.",
        "Strong correlations (|r| > 0.7) can reveal important relationships between features that might be useful for feature selection or understanding underlying patterns in the data.",
        "High correlations between predictors (|r| > 0.9) may cause multicollinearity problems in regression models, inflating variance in coefficient estimates.",
        "Consider removing one feature from highly correlated pairs to reduce dimensionality and improve model stability."
    )

    # Spearman correlation
    spearman_result = compute_correlation(df, method='spearman')

    if 'error' not in spearman_result:
        # Generate Spearman correlation plot
        spearman_fig = generate_correlation_plot(spearman_result, "Spearman Correlation Matrix")

        # Add Spearman correlation heatmap to the report
        report.add_plot(
            spearman_fig,
            "Spearman Correlation Matrix",
            "The heatmap shows Spearman rank correlation coefficients between pairs of numeric features, which capture monotonic (not just linear) relationships.",
            "Differences between Pearson and Spearman coefficients may reveal non-linear relationships between features.",
            "Similar Pearson and Spearman correlations suggest predominantly linear relationships.",
            "Significantly different Pearson and Spearman correlations indicate the presence of non-linear but monotonic relationships.",
            "When Spearman correlations are stronger than Pearson, consider non-linear transformations or models that can handle non-linear relationships."
        )

    # Create strong correlations table
    strong_correlations = pearson_result['strong_correlations']
    if strong_correlations:
        # Create DataFrame for strong correlations
        strong_corr_df = pd.DataFrame(strong_correlations)

        # Add correlation type (positive/negative)
        strong_corr_df['type'] = strong_corr_df['correlation'].apply(
            lambda x: 'Positive' if x > 0 else 'Negative')

        # Reorder columns for better presentation
        strong_corr_df = strong_corr_df[['column1', 'column2', 'correlation', 'type', 'strength']]

        # Add to report
        report.add_table(
            strong_corr_df,
            "Strong Correlations (|r| > 0.7)",
            "This table shows pairs of features with strong correlations, highlighting relationships that may be important for modeling or feature selection."
        )
    else:
        report.add_section(
            "Strong Correlations",
            "<p>No strong correlations (|r| > 0.7) were found between features in this dataset.</p>"
        )

    # Add summary and recommendations
    recommendations = []

    if strong_correlations:
        very_strong = [c for c in strong_correlations if abs(c['correlation']) > 0.9]
        if very_strong:
            recommendations.append("<li><strong>Multicollinearity Risk:</strong> The following feature pairs have very strong correlations (|r| > 0.9):")
            recommendations.append("<ul>")
            for corr in very_strong:
                recommendations.append(f"<li>{corr['column1']} ↔ {corr['column2']}: {corr['correlation']:.3f}</li>")
            recommendations.append("</ul>")
            recommendations.append("Consider removing one feature from each pair to reduce multicollinearity in regression models.</li>")

        recommendations.append("<li><strong>Feature Reduction Opportunity:</strong> Consider using PCA (Principal Component Analysis) or other dimensionality reduction techniques to create uncorrelated features from groups of correlated variables.</li>")
    else:
        recommendations.append("<li><strong>Low Feature Redundancy:</strong> Features in this dataset show relatively low correlation with each other, suggesting minimal redundancy in the feature set.</li>")
        recommendations.append("<li><strong>Feature Engineering:</strong> Since existing features have low correlation, consider creating interaction terms or polynomial features to capture more complex relationships.</li>")

    summary_content = f"""
    <p>Based on the correlation analysis of {len(pearson_result['columns'])} numeric features, here are the key findings and recommendations:</p>
    <ul>
        {"".join(recommendations)}
        <li><strong>Next Steps:</strong>
            <ul>
                <li>Run feature importance analysis to identify the most predictive features</li>
                <li>Consider both correlation and importance when selecting features for modeling</li>
            </ul>
        </li>
    </ul>
    """
    report.add_section("Summary and Recommendations", summary_content)

    # Save the report
    report_dir = ensure_report_directory(file_path)
    report_path = os.path.join(report_dir, "correlation_analysis.html")
    report.save(report_path)

    return report_path
