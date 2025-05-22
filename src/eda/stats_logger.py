"""
Module for logging statistics analysis results to files
"""
import os
import json
import datetime
import re
from glob import glob


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
                               for col in stats if 'missing' in stats[col] and stats[col]['missing'] > 0]
    }

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2)

    return log_path


def log_descriptive_stats(desc_stats_results, file_paths):
    """Log descriptive statistics to a file"""
    log_dir = ensure_logs_directory()
    filename = generate_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Extract summary data
    summary_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_type': 'descriptive_stats',
        'files_analyzed': len(file_paths),
        'file_paths': file_paths,
        'columns_analyzed': sum(len(stats) for stats in desc_stats_results),
        'high_variance_columns': [(path, col)
                               for path, stats in zip(file_paths, desc_stats_results)
                               for col in stats
                               if 'error' not in stats[col] and 'std' in stats[col] and 'mean' in stats[col]
                               and abs(stats[col]['std'] / stats[col]['mean'] if stats[col]['mean'] != 0 else 0) > 1]
    }

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2)

    return log_path


def log_distribution_analysis(dist_stats_results, file_paths):
    """Log distribution analysis to a file"""
    log_dir = ensure_logs_directory()
    filename = generate_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Extract summary data
    normal_cols = []
    skewed_cols = []

    for path, stats in zip(file_paths, dist_stats_results):
        for col, col_stats in stats.items():
            if 'error' not in col_stats:
                if col_stats['is_normal'] == 'Yes':
                    normal_cols.append((path, col))

                if abs(col_stats['skewness']) > 1:
                    skewed_cols.append((path, col, col_stats['skewness']))

    summary_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_type': 'distribution_analysis',
        'files_analyzed': len(file_paths),
        'file_paths': file_paths,
        'normal_columns': normal_cols,
        'highly_skewed_columns': skewed_cols
    }

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2)

    return log_path


def log_outlier_analysis(outlier_stats_results, file_paths):
    """Log outlier analysis to a file"""
    log_dir = ensure_logs_directory()
    filename = generate_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Extract summary data
    high_outlier_cols = []

    for path, stats in zip(file_paths, outlier_stats_results):
        for col, col_stats in stats.items():
            if 'error' not in col_stats:
                iqr_pct = col_stats['iqr_method']['outlier_percentage']
                z_pct = col_stats['z_score_method']['outlier_percentage']
                max_pct = max(iqr_pct, z_pct)

                if max_pct > 5:
                    high_outlier_cols.append((path, col, max_pct))

    summary_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_type': 'outlier_analysis',
        'files_analyzed': len(file_paths),
        'file_paths': file_paths,
        'high_outlier_columns': high_outlier_cols
    }

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2)

    return log_path


def log_time_series_analysis(ts_stats_results, file_paths):
    """Log time series analysis to a file"""
    log_dir = ensure_logs_directory()
    filename = generate_log_filename()
    log_path = os.path.join(log_dir, filename)

    # Extract summary data
    non_stationary_cols = []
    stationary_cols = []
    seasonality_files = []

    for path, stats in zip(file_paths, ts_stats_results):
        if 'error' not in stats:
            if 'stationarity' in stats:
                for col, result in stats['stationarity'].items():
                    if 'error' not in result:
                        if result['is_stationary']:
                            stationary_cols.append((path, col))
                        else:
                            non_stationary_cols.append((path, col))

            if 'seasonality' in stats and 'day_of_week' in stats['seasonality'] and 'error' not in stats['seasonality']['day_of_week']:
                seasonality_files.append(path)

    summary_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_type': 'time_series_analysis',
        'files_analyzed': len(file_paths),
        'file_paths': file_paths,
        'stationary_columns': stationary_cols,
        'non_stationary_columns': non_stationary_cols,
        'seasonality_files': seasonality_files
    }

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2)

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

    with open(log_path, 'w') as f:
        json.dump(summary_data, f, indent=2)

    return log_path


def clean_stats_logs():
    """Delete all statistics log files"""
    log_dir = ensure_logs_directory()
    log_files = glob(os.path.join(log_dir, 'stats_analysis_*.json'))

    count = 0
    for file_path in log_files:
        try:
            os.remove(file_path)
            count += 1
        except:
            pass

    return count
