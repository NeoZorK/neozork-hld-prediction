# -*- coding: utf-8 -*-
# src/batch_eda/stats_logger.py
"""
Module for logging statistics analysis results to files
"""
import os
import json
import datetime
import re
from glob import glob
import numpy as np

# Custom JSON encoder for handling pandas Timestamp and other non-serializable objects
class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that can handle pandas Timestamp and other non-serializable types."""
    def default(self, obj):
        # Handle pandas Timestamp objects
        if hasattr(obj, 'isoformat') and callable(getattr(obj, 'isoformat')):
            return obj.isoformat()
        # Handle numpy numeric types
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        # Handle other non-serializable types
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return str(obj)  # Convert any other object to string
        return super().default(obj)


def ensure_logs_directory():
    """Ensure the logs directory exists"""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    stats_log_dir = os.path.join(log_dir, 'stats')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.path.exists(stats_log_dir):
        os.makedirs(stats_log_dir)

    return stats_log_dir


def generate_log_filename():
    """Generate a log filename with current timestamp"""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    return f"stats_analysis_{timestamp}.json"


def generate_unified_log_filename():
    """Generate a unified log filename with current timestamp"""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    return f"unified_stats_analysis_{timestamp}.json"


def extract_file_summaries(basic_stats_results, file_paths):
    """Extract per-file summaries from basic statistics"""
    file_summaries = []

    for file_path, stats in zip(file_paths, basic_stats_results):
        # Count numeric and non-numeric columns
        numeric_cols = []
        categorical_cols = []
        high_missing_cols = []
        high_cardinality_cols = []
        low_cardinality_cols = []

        for col, col_stats in stats.items():
            if 'std' in col_stats:
                numeric_cols.append(col)

                # Check for high missing values
                if col_stats.get('missing', 0) > 0:
                    missing_pct = col_stats['missing'] / (col_stats['missing'] + col_stats.get('unique', 1)) * 100
                    if missing_pct > 5:
                        high_missing_cols.append((col, missing_pct))
            else:
                categorical_cols.append(col)
                # Check cardinality
                unique_count = col_stats.get('unique', 0)
                if unique_count > 100:
                    high_cardinality_cols.append((col, unique_count))
                elif unique_count < 5 and unique_count > 1:
                    low_cardinality_cols.append((col, unique_count))

        summary = {
            'file_path': file_path,
            'numeric_columns': len(numeric_cols),
            'categorical_columns': len(categorical_cols),
            'high_missing_columns': [{'column': col, 'missing_percentage': pct} for col, pct in high_missing_cols],
            'high_cardinality_columns': [{'column': col, 'unique_count': cnt} for col, cnt in high_cardinality_cols],
            'low_cardinality_columns': [{'column': col, 'unique_count': cnt} for col, cnt in low_cardinality_cols],
            'recommendations': []
        }

        # Add basic recommendations
        if high_missing_cols:
            summary['recommendations'].append("Consider handling missing values with imputation or feature removal")
        if high_cardinality_cols:
            summary['recommendations'].append("Consider encoding methods like target encoding for high cardinality categorical features")
        if low_cardinality_cols:
            summary['recommendations'].append("Low cardinality features might be good candidates for one-hot encoding")

        file_summaries.append(summary)

    return file_summaries


def extract_distribution_summaries(dist_stats_results, file_paths):
    """Extract per-file summaries from distribution analysis"""
    file_summaries = []

    for file_path, stats in zip(file_paths, dist_stats_results):
        normal_cols = []
        skewed_cols = []
        highly_skewed_cols = []
        heavy_tailed_cols = []
        light_tailed_cols = []

        for col, col_stats in stats.items():
            if 'error' not in col_stats:
                if col_stats['is_normal'] == 'Yes':
                    normal_cols.append(col)

                skew = col_stats['skewness']
                kurt = col_stats['kurtosis']

                if abs(skew) > 1:
                    highly_skewed_cols.append((col, skew))
                elif abs(skew) > 0.5:
                    skewed_cols.append((col, skew))

                if kurt > 3:
                    heavy_tailed_cols.append((col, kurt))
                elif kurt < 3:
                    light_tailed_cols.append((col, kurt))

        summary = {
            'file_path': file_path,
            'normal_columns': normal_cols,
            'highly_skewed_columns': [{'column': col, 'skewness': skew} for col, skew in highly_skewed_cols],
            'moderately_skewed_columns': [{'column': col, 'skewness': skew} for col, skew in skewed_cols],
            'heavy_tailed_columns': [{'column': col, 'kurtosis': kurt} for col, kurt in heavy_tailed_cols],
            'light_tailed_columns': [col for col, _ in light_tailed_cols],
            'recommendations': []
        }

        # Add specific recommendations
        if highly_skewed_cols:
            summary['recommendations'].append("Consider applying transformations (log, sqrt, Box-Cox) to normalize highly skewed variables")
        if heavy_tailed_cols:
            summary['recommendations'].append("Watch for outliers and use robust statistical methods for heavy-tailed variables")
        if len(normal_cols) < len(stats) / 2:
            summary['recommendations'].append("Most columns don't follow normal distribution - consider using non-parametric methods")

        file_summaries.append(summary)

    return file_summaries


def extract_outlier_summaries(outlier_stats_results, file_paths):
    """Extract per-file summaries from outlier analysis"""
    file_summaries = []

    for file_path, stats in zip(file_paths, outlier_stats_results):
        high_outlier_cols = []
        moderate_outlier_cols = []

        for col, col_stats in stats.items():
            if 'error' not in col_stats:
                iqr_pct = col_stats['iqr_method']['outlier_percentage']
                z_pct = col_stats['z_score_method']['outlier_percentage']
                max_pct = max(iqr_pct, z_pct)

                if max_pct > 5:
                    high_outlier_cols.append((col, max_pct))
                elif max_pct > 1:
                    moderate_outlier_cols.append((col, max_pct))

        summary = {
            'file_path': file_path,
            'high_outlier_columns': [{'column': col, 'percentage': pct} for col, pct in high_outlier_cols],
            'moderate_outlier_columns': [{'column': col, 'percentage': pct} for col, pct in moderate_outlier_cols],
            'recommendations': []
        }

        # Add specific recommendations
        if high_outlier_cols:
            summary['recommendations'].append("Investigate outlier sources: measurement errors vs. genuine extreme values")
            summary['recommendations'].append("Consider using winsorization, trimming, or robust statistics for columns with significant outliers")
            summary['recommendations'].append("For ML models, use algorithms resistant to outliers (RandomForest, Gradient Boosting)")
        elif moderate_outlier_cols:
            summary['recommendations'].append("Consider using robust methods for columns with moderate outliers")

        file_summaries.append(summary)

    return file_summaries


def extract_time_series_summaries(ts_stats_results, file_paths):
    """Extract per-file summaries from time series analysis"""
    file_summaries = []

    for file_path, stats in zip(file_paths, ts_stats_results):
        if 'error' in stats:
            summary = {
                'file_path': file_path,
                'error': stats['error'],
                'recommendations': ["Add or convert a datetime column to enable full time series analysis"]
            }
            file_summaries.append(summary)
            continue

        non_stationary_cols = []
        stationary_cols = []
        has_seasonality = False

        if 'stationarity' in stats:
            for col, result in stats['stationarity'].items():
                if 'error' not in result:
                    if result['is_stationary']:
                        stationary_cols.append(col)
                    else:
                        non_stationary_cols.append(col)

        if 'seasonality' in stats and 'day_of_week' in stats['seasonality'] and 'error' not in stats['seasonality']['day_of_week']:
            has_seasonality = True

        summary = {
            'file_path': file_path,
            'has_derived_features': bool(stats.get('features', {})),
            'stationary_columns': stationary_cols,
            'non_stationary_columns': non_stationary_cols,
            'has_seasonality': has_seasonality,
            'recommendations': []
        }

        # Add specific recommendations
        if non_stationary_cols:
            summary['recommendations'].append("Apply differencing (diff() method) to remove trends in non-stationary series")
            summary['recommendations'].append("Consider logarithmic or other transformations for variance stabilization")

        if stationary_cols:
            summary['recommendations'].append("Stationary series are well-suited for ARIMA, GARCH and other statistical methods")

        if has_seasonality:
            summary['recommendations'].append("Add categorical features (day of week, month, etc.) to capture seasonality patterns")
            summary['recommendations'].append("For statistical models, consider using seasonal differencing or SARIMA")

        if 'warning' in stats:
            summary['warning'] = stats['warning']

        file_summaries.append(summary)

    return file_summaries


def log_all_stats_unified(
    basic_stats_results=None,
    desc_stats_results=None,
    dist_analysis_results=None,
    outlier_analysis_results=None,
    ts_analysis_results=None,
    file_paths=None,
    stats_collector=None
):
    """Log all statistics results to a single unified JSON file"""
    log_dir = ensure_logs_directory()
    filename = generate_unified_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Initialize the unified data structure
    unified_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'total_files_analyzed': len(file_paths) if file_paths else 0,
        'file_paths': file_paths,
        'file_summaries': [],
        'global_summary': {},
        'key_findings_and_recommendations': {}
    }

    # Collect file-specific summaries based on available data
    if file_paths:
        file_specific_data = []
        for idx, path in enumerate(file_paths):
            file_data = {
                'file_path': path,
                'file_name': os.path.basename(path),
                'analyses': {}
            }

            # Add basic stats if available
            if basic_stats_results and idx < len(basic_stats_results):
                file_summary = extract_file_summaries([basic_stats_results[idx]], [path])[0]
                file_data['analyses']['basic_stats'] = {
                    'raw_data': basic_stats_results[idx],  # Store raw analysis data
                    'numeric_columns': file_summary['numeric_columns'],
                    'categorical_columns': file_summary['categorical_columns'],
                    'high_missing_columns': file_summary['high_missing_columns'],
                    'high_cardinality_columns': file_summary['high_cardinality_columns'],
                    'low_cardinality_columns': file_summary['low_cardinality_columns'],
                    'recommendations': file_summary['recommendations'],
                    'summary': f"Dataset contains {file_summary['numeric_columns']} numeric and {file_summary['categorical_columns']} non-numeric columns"
                }

            # Add descriptive stats if available
            if desc_stats_results and idx < len(desc_stats_results):
                # Extract high variance columns for this file
                high_variance_cols = []
                for col, stats in desc_stats_results[idx].items():
                    if 'error' not in stats and 'std' in stats and 'mean' in stats and stats['mean'] != 0:
                        cv = abs(stats['std'] / stats['mean']) if stats['mean'] != 0 else 0
                        if cv > 1.0:  # High variance threshold
                            high_variance_cols.append({'column': col, 'cv': cv})

                file_data['analyses']['descriptive_stats'] = {
                    'raw_data': desc_stats_results[idx],  # Store raw analysis data
                    'high_variance_columns': high_variance_cols,
                    'recommendations': [
                        "Statistical measures provide insights into data characteristics and quality",
                        "Consider normalization for high variance columns",
                        "Significant difference between mean and median suggests distribution asymmetry"
                    ],
                    'summary': f"Found {len(high_variance_cols)} columns with high coefficient of variation"
                }

            # Add distribution analysis if available
            if dist_analysis_results and idx < len(dist_analysis_results):
                file_summary = extract_distribution_summaries([dist_analysis_results[idx]], [path])[0]
                file_data['analyses']['distribution_analysis'] = {
                    'raw_data': dist_analysis_results[idx],  # Store raw analysis data
                    'normal_columns': file_summary['normal_columns'],
                    'normal_columns_count': len(file_summary['normal_columns']),
                    'highly_skewed_columns': file_summary['highly_skewed_columns'],
                    'moderately_skewed_columns': file_summary['moderately_skewed_columns'],
                    'heavy_tailed_columns': file_summary['heavy_tailed_columns'],
                    'light_tailed_columns': file_summary['light_tailed_columns'],
                    'recommendations': file_summary['recommendations'],
                    'summary': f"Found {len(file_summary['normal_columns'])} normally distributed columns, {len(file_summary['highly_skewed_columns'])} highly skewed columns"
                }

            # Add outlier analysis if available
            if outlier_analysis_results and idx < len(outlier_analysis_results):
                file_summary = extract_outlier_summaries([outlier_analysis_results[idx]], [path])[0]
                file_data['analyses']['outlier_analysis'] = {
                    'raw_data': outlier_analysis_results[idx],  # Store raw analysis data
                    'high_outlier_columns': file_summary['high_outlier_columns'],
                    'moderate_outlier_columns': file_summary['moderate_outlier_columns'],
                    'recommendations': file_summary['recommendations'],
                    'summary': f"Found {len(file_summary['high_outlier_columns'])} columns with significant outliers (>5%), {len(file_summary['moderate_outlier_columns'])} with moderate outliers (1-5%)"
                }

            # Add time series analysis if available
            if ts_analysis_results and idx < len(ts_analysis_results):
                file_summary = extract_time_series_summaries([ts_analysis_results[idx]], [path])[0]
                if 'error' in file_summary:
                    file_data['analyses']['time_series_analysis'] = {
                        'raw_data': ts_analysis_results[idx],  # Store raw analysis data
                        'error': file_summary['error'],
                        'recommendations': file_summary['recommendations'],
                        'summary': f"Error in time series analysis: {file_summary['error']}"
                    }
                else:
                    file_data['analyses']['time_series_analysis'] = {
                        'raw_data': ts_analysis_results[idx],  # Store raw analysis data
                        'stationary_columns': file_summary['stationary_columns'],
                        'non_stationary_columns': file_summary['non_stationary_columns'],
                        'has_seasonality': file_summary['has_seasonality'],
                        'recommendations': file_summary['recommendations'],
                        'summary': f"Found {len(file_summary['stationary_columns'])} stationary and {len(file_summary['non_stationary_columns'])} non-stationary time series columns"
                    }
                    if 'warning' in file_summary:
                        file_data['analyses']['time_series_analysis']['warning'] = file_summary['warning']

            # Consolidate all recommendations into a single list
            all_recommendations = []
            for analysis_type, analysis_data in file_data['analyses'].items():
                if 'recommendations' in analysis_data:
                    for rec in analysis_data['recommendations']:
                        if rec not in all_recommendations:  # Avoid duplicates
                            all_recommendations.append(rec)

            file_data['key_recommendations'] = all_recommendations
            file_specific_data.append(file_data)

        unified_data['file_summaries'] = file_specific_data

    # Add global summary from stats_collector if provided
    if stats_collector:
        global_summary = {
            'total_columns': stats_collector.descriptive_summary.get('total_columns', 0),
            'normal_columns_count': len(stats_collector.distribution_summary.get('normal_cols', [])),
            'highly_skewed_columns_count': len(stats_collector.distribution_summary.get('highly_skewed_cols', [])),
            'heavy_tailed_columns_count': len(stats_collector.distribution_summary.get('heavy_tailed_cols', [])),
            'columns_with_high_outliers_count': len(stats_collector.outlier_summary.get('high_outlier_cols', [])),
            'stationary_time_series_count': len(stats_collector.time_series_summary.get('stationary_cols', [])),
            'non_stationary_time_series_count': len(stats_collector.time_series_summary.get('non_stationary_cols', [])),
            'files_with_seasonality': stats_collector.time_series_summary.get('has_seasonality', 0),
            'high_variance_columns': [
                {'file': os.path.basename(path), 'column': col, 'cv': cv}
                for path, col, cv in stats_collector.descriptive_summary.get('high_variance_cols', [])
            ][:15]  # Limit to 15 entries for readability
        }

        # Compile key global recommendations
        key_recommendations = {
            'data_quality': [],
            'data_preparation': [],
            'modeling_strategy': [],
            'next_steps': []
        }

        # Data quality recommendations
        if stats_collector.outlier_summary.get('high_outlier_cols', []):
            key_recommendations['data_quality'].append("Address outliers in the data, particularly in price and volume columns")

        # Data preparation recommendations
        if stats_collector.distribution_summary.get('highly_skewed_cols', []):
            key_recommendations['data_preparation'].append("Apply appropriate transformations to normalize skewed distributions")
        if stats_collector.descriptive_summary.get('high_variance_cols', []):
            key_recommendations['data_preparation'].append("Consider standardizing high-variance features")

        # Modeling strategy recommendations
        if stats_collector.time_series_summary.get('non_stationary_cols', []):
            key_recommendations['modeling_strategy'].append("Use differencing for non-stationary time series")
        if stats_collector.time_series_summary.get('has_seasonality', 0) > 0:
            key_recommendations['modeling_strategy'].append("Incorporate seasonality features (day of week, month) in your models")

        # Next steps recommendations
        key_recommendations['next_steps'] = [
            "Run correlation analysis to identify relationships between features",
            "Perform feature importance analysis to identify key predictors",
            "Consider developing specialized features based on domain knowledge"
        ]

        global_summary['key_recommendations'] = key_recommendations
        unified_data['global_summary'] = global_summary

        # Add KEY FINDINGS AND RECOMMENDATIONS section
        unified_data['key_findings_and_recommendations'] = {
            'data_quality': {
                'findings': [
                    f"Found {len(stats_collector.outlier_summary.get('high_outlier_cols', []))} columns with significant outliers",
                    f"Found {sum(1 for path, col, pct in stats_collector.outlier_summary.get('moderate_outlier_cols', []) if pct > 3)} columns with moderate to high outlier percentages (>3%)"
                ],
                'recommendations': key_recommendations['data_quality']
            },
            'data_preparation': {
                'findings': [
                    f"Found {len(stats_collector.distribution_summary.get('highly_skewed_cols', []))} highly skewed columns",
                    f"Found {len(stats_collector.descriptive_summary.get('high_variance_cols', []))} columns with high variance"
                ],
                'recommendations': key_recommendations['data_preparation']
            },
            'modeling_strategy': {
                'findings': [
                    f"Found {len(stats_collector.time_series_summary.get('non_stationary_cols', []))} non-stationary time series",
                    f"Found {stats_collector.time_series_summary.get('has_seasonality', 0)} files with clear seasonality patterns"
                ],
                'recommendations': key_recommendations['modeling_strategy']
            },
            'next_steps': {
                'recommendations': key_recommendations['next_steps']
            }
        }

    # Write the unified data to a JSON file
    with open(log_path, 'w') as f:
        json.dump(unified_data, f, indent=2, cls=CustomJSONEncoder)

    return log_path


# Keep the individual logging functions for backward compatibility
def log_basic_stats(basic_stats_results, file_paths):
    """Log basic statistics to a file"""
    log_dir = ensure_logs_directory()
    filename = generate_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Extract summary data
    summary_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_type': 'basic_stats',
        'files_analyzed': len(file_paths),
        'file_paths': file_paths,
        'numeric_columns_count': sum(1 for stats in basic_stats_results for col in stats
                                    if 'std' in stats[col]),
        'categorical_columns_count': sum(1 for stats in basic_stats_results for col in stats
                                        if 'std' not in stats[col]),
        'high_missing_columns': [(path, col, stats[col]['missing'])
                               for path, stats in zip(file_paths, basic_stats_results)
                               for col in stats
                               if 'missing' in stats[col] and stats[col]['missing'] > 0],
        'file_summaries': extract_file_summaries(basic_stats_results, file_paths),
        'raw_data': {
            file_path: result for file_path, result in zip(file_paths, basic_stats_results)
        }
    }

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2, cls=CustomJSONEncoder)

    return log_path


def log_descriptive_stats(desc_stats_results, file_paths):
    """Log descriptive statistics to a file"""
    log_dir = ensure_logs_directory()
    filename = generate_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Extract high variance columns for summary
    high_variance_cols = []
    for path_idx, path in enumerate(file_paths):
        stats = desc_stats_results[path_idx]
        for col, col_stats in stats.items():
            if 'error' not in col_stats and 'std' in col_stats and 'mean' in col_stats and col_stats['mean'] != 0:
                cv = abs(col_stats['std'] / col_stats['mean']) if col_stats['mean'] != 0 else 0
                if cv > 1.0:  # High variance threshold
                    high_variance_cols.append((path, col, cv))

    # Comprehensive summary with raw data
    summary_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_type': 'descriptive_stats',
        'files_analyzed': len(file_paths),
        'file_paths': file_paths,
        'high_variance_columns': [
            {'file': os.path.basename(path), 'column': col, 'cv': cv}
            for path, col, cv in high_variance_cols
        ],
        'recommendations': [
            "Statistical measures provide insights into data characteristics and quality",
            "Consider normalization for high variance columns",
            "Significant difference between mean and median suggests distribution asymmetry"
        ],
        'raw_data': {
            file_path: result for file_path, result in zip(file_paths, desc_stats_results)
        }
    }

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2, cls=CustomJSONEncoder)

    return log_path


def log_distribution_analysis(dist_stats_results, file_paths):
    """Log distribution analysis to a file"""
    log_dir = ensure_logs_directory()
    filename = generate_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Extract summary data
    summary_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_type': 'distribution_analysis',
        'files_analyzed': len(file_paths),
        'file_paths': file_paths,
        'file_summaries': extract_distribution_summaries(dist_stats_results, file_paths),
        'raw_data': {
            file_path: result for file_path, result in zip(file_paths, dist_stats_results)
        }
    }

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2, cls=CustomJSONEncoder)

    return log_path


def log_outlier_analysis(outlier_stats_results, file_paths):
    """Log outlier analysis to a file"""
    log_dir = ensure_logs_directory()
    filename = generate_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Extract summary data
    summary_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_type': 'outlier_analysis',
        'files_analyzed': len(file_paths),
        'file_paths': file_paths,
        'file_summaries': extract_outlier_summaries(outlier_stats_results, file_paths),
        'raw_data': {
            file_path: result for file_path, result in zip(file_paths, outlier_stats_results)
        }
    }

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2, cls=CustomJSONEncoder)

    return log_path


def log_time_series_analysis(ts_stats_results, file_paths):
    """Log time series analysis to a file"""
    log_dir = ensure_logs_directory()
    filename = generate_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Extract summary data
    summary_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_type': 'time_series_analysis',
        'files_analyzed': len(file_paths),
        'file_paths': file_paths,
        'file_summaries': extract_time_series_summaries(ts_stats_results, file_paths),
        'raw_data': {
            file_path: result for file_path, result in zip(file_paths, ts_stats_results)
        }
    }

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2, cls=CustomJSONEncoder)

    return log_path


def log_global_stats_summary(stats_collector):
    """Log global statistics summary to a file"""
    log_dir = ensure_logs_directory()
    filename = generate_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Extract summary data from stats_collector
    summary_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_type': 'global_summary',
        'files_analyzed': stats_collector.descriptive_summary['files_analyzed'],
        'total_columns': stats_collector.descriptive_summary['total_columns'],
        'high_variance_columns': [
            {'file': os.path.basename(path), 'column': col, 'cv': cv}
            for path, col, cv in stats_collector.descriptive_summary['high_variance_cols']
        ],
        'normal_columns_count': len(stats_collector.distribution_summary['normal_cols']),
        'highly_skewed_columns_count': len(stats_collector.distribution_summary['highly_skewed_cols']),
        'columns_with_outliers': len(stats_collector.outlier_summary['high_outlier_cols']),
        'stationary_series_count': len(stats_collector.time_series_summary['stationary_cols']),
        'non_stationary_series_count': len(stats_collector.time_series_summary['non_stationary_cols']),
        'files_with_seasonality': stats_collector.time_series_summary['has_seasonality']
    }

    # Add key recommendations
    summary_data['key_recommendations'] = {
        'data_quality': [],
        'data_preparation': [],
        'modeling_strategy': [],
        'next_steps': []
    }

    # Data quality recommendations
    if stats_collector.outlier_summary['high_outlier_cols']:
        summary_data['key_recommendations']['data_quality'].append("Address outliers in the data, particularly in price and volume columns")

    # Data preparation recommendations
    if stats_collector.distribution_summary['highly_skewed_cols']:
        summary_data['key_recommendations']['data_preparation'].append("Apply appropriate transformations to normalize skewed distributions")
    if stats_collector.descriptive_summary['high_variance_cols']:
        summary_data['key_recommendations']['data_preparation'].append("Consider standardizing high-variance features")

    # Modeling strategy recommendations
    if stats_collector.time_series_summary['non_stationary_cols']:
        summary_data['key_recommendations']['modeling_strategy'].append("Use differencing for non-stationary time series")
    if stats_collector.time_series_summary['has_seasonality'] > 0:
        summary_data['key_recommendations']['modeling_strategy'].append("Incorporate seasonality features (day of week, month) in your models")

    # Next steps recommendations
    summary_data['key_recommendations']['next_steps'] = [
        "Run correlation analysis to identify relationships",
        "Perform feature importance analysis to identify key predictors",
        "Consider developing specialized features based on domain knowledge"
    ]

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2, cls=CustomJSONEncoder)

    return log_path


def clean_stats_logs():
    """Delete all statistics log files"""
    log_dir = ensure_logs_directory()
    log_files = glob(os.path.join(log_dir, 'stats_analysis_*.json')) + glob(os.path.join(log_dir, 'unified_stats_analysis_*.json'))

    count = 0
    for file_path in log_files:
        try:
            os.remove(file_path)
            count += 1
        except:
            pass

    return count
