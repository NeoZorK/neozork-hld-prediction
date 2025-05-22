# Handles basic statistics

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller

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

def descriptive_stats(df):
    """
    Compute detailed descriptive statistics for numeric columns.
    Returns a dictionary with extended stats for each numeric column.
    """
    desc_stats = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Filter out NaN values for calculations
            col_data = df[col].dropna()
            if len(col_data) > 0:
                desc_stats[col] = {
                    'mean': col_data.mean(),
                    'median': col_data.median(),
                    'std': col_data.std(),
                    'var': col_data.var(),
                    'mode': float(stats.mode(col_data, keepdims=False)[0]) if len(col_data) > 0 else None,
                    'min': col_data.min(),
                    'max': col_data.max(),
                    '25%': col_data.quantile(0.25),
                    '50%': col_data.quantile(0.5),
                    '75%': col_data.quantile(0.75),
                    'count': len(col_data),
                    'missing': int(df[col].isnull().sum()),
                    'missing_pct': round(df[col].isnull().sum() / len(df) * 100, 2)
                }
            else:
                desc_stats[col] = {'error': 'No valid data points'}
    return desc_stats

def distribution_analysis(df):
    """
    Analyze distributions of numeric columns by calculating skewness and kurtosis.
    Returns a dictionary with distribution stats for each numeric column.
    """
    dist_stats = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Filter out NaN values for calculations
            col_data = df[col].dropna()
            if len(col_data) > 0:
                dist_stats[col] = {
                    'skewness': stats.skew(col_data),
                    'kurtosis': stats.kurtosis(col_data),
                    'normality_test': stats.normaltest(col_data) if len(col_data) >= 8 else None,
                    'is_normal': 'Unknown' if len(col_data) < 8 else (
                        'Yes' if stats.normaltest(col_data)[1] > 0.05 else 'No'
                    )
                }
            else:
                dist_stats[col] = {'error': 'No valid data points'}
    return dist_stats

def outlier_analysis(df):
    """
    Detect outliers in numeric columns using IQR and Z-score methods.
    Returns a dictionary with outlier stats for each numeric column.
    """
    outlier_stats = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Filter out NaN values for calculations
            col_data = df[col].dropna()
            if len(col_data) > 0:
                # IQR method
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                iqr_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

                # Z-score method
                z_scores = np.abs(stats.zscore(col_data))
                z_outliers = df.iloc[np.where(z_scores > 3)[0]]

                outlier_stats[col] = {
                    'iqr_method': {
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound,
                        'outlier_count': len(iqr_outliers),
                        'outlier_percentage': round(len(iqr_outliers) / len(df) * 100, 2),
                        'outlier_indices': iqr_outliers.index.tolist()[:10]  # Limit to first 10
                    },
                    'z_score_method': {
                        'outlier_count': len(z_outliers),
                        'outlier_percentage': round(len(z_outliers) / len(df) * 100, 2),
                        'outlier_indices': z_outliers.index.tolist()[:10]  # Limit to first 10
                    }
                }
            else:
                outlier_stats[col] = {'error': 'No valid data points'}
    return outlier_stats

def time_series_analysis(df):
    """
    Perform basic time series analysis including trend and seasonality detection.
    Requires a DataFrame with at least one datetime column and OHLC price data.
    """
    ts_stats = {'features': {}, 'stationarity': {}, 'seasonality': {}}

    # Try to identify datetime column
    datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]

    # Try to identify OHLCV columns
    ohlc_patterns = [
        col for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col]) and
        any(pat in col.lower() for pat in ['open', 'high', 'low', 'close', 'volume'])
    ]

    # If we don't have datetime or OHLC columns, return with a message
    if not datetime_cols:
        ts_stats['error'] = 'No datetime columns found for time series analysis'
        return ts_stats

    # Use the first datetime column as the index
    date_col = datetime_cols[0]
    df_ts = df.copy()
    df_ts.set_index(date_col, inplace=True)

    # Calculate derived features if we have OHLC data
    if len([col for col in ohlc_patterns if 'high' in col.lower()]) > 0 and len([col for col in ohlc_patterns if 'low' in col.lower()]) > 0:
        high_col = [col for col in ohlc_patterns if 'high' in col.lower()][0]
        low_col = [col for col in ohlc_patterns if 'low' in col.lower()][0]
        ts_stats['features']['daily_range'] = {
            'mean': (df_ts[high_col] - df_ts[low_col]).mean(),
            'median': (df_ts[high_col] - df_ts[low_col]).median(),
            'std': (df_ts[high_col] - df_ts[low_col]).std()
        }

    if len([col for col in ohlc_patterns if 'open' in col.lower()]) > 0 and len([col for col in ohlc_patterns if 'close' in col.lower()]) > 0:
        open_col = [col for col in ohlc_patterns if 'open' in col.lower()][0]
        close_col = [col for col in ohlc_patterns if 'close' in col.lower()][0]
        ts_stats['features']['daily_change'] = {
            'mean': (df_ts[close_col] - df_ts[open_col]).mean(),
            'median': (df_ts[close_col] - df_ts[open_col]).median(),
            'std': (df_ts[close_col] - df_ts[open_col]).std()
        }

    # Stationarity test (ADF)
    for col in ohlc_patterns:
        if df_ts[col].count() > 10:  # Need sufficient data points
            try:
                adf_result = adfuller(df_ts[col].dropna())
                ts_stats['stationarity'][col] = {
                    'test_statistic': adf_result[0],
                    'p_value': adf_result[1],
                    'is_stationary': adf_result[1] < 0.05,
                    'critical_values': adf_result[4]
                }
            except:
                ts_stats['stationarity'][col] = {'error': 'ADF test failed'}

    # Basic seasonality check - day of week patterns
    if hasattr(df_ts.index, 'dayofweek'):
        for col in ohlc_patterns:
            if 'close' in col.lower():
                try:
                    # Calculate mean closing price by day of week
                    day_means = df_ts.groupby(df_ts.index.dayofweek)[col].mean()
                    ts_stats['seasonality']['day_of_week'] = {day: mean for day, mean in enumerate(day_means)}
                except:
                    ts_stats['seasonality']['day_of_week'] = {'error': 'Day of week analysis failed'}

    return ts_stats

def print_descriptive_stats(desc_stats):
    """Print descriptive statistics in a readable format with columns in row for better space efficiency."""
    print("\n\033[1m\033[94mDescriptive Statistics:\033[0m")

    # Group columns with similar patterns (OHLCV, etc.)
    column_groups = {}
    for col in desc_stats.keys():
        # Try to detect column type using common patterns
        if 'open' in col.lower():
            group = 'price_ohlc'
        elif 'high' in col.lower():
            group = 'price_ohlc'
        elif 'low' in col.lower():
            group = 'price_ohlc'
        elif 'close' in col.lower():
            group = 'price_ohlc'
        elif 'volume' in col.lower():
            group = 'volume'
        elif 'pressure' in col.lower():
            group = 'pressure'
        else:
            group = 'other'

        if group not in column_groups:
            column_groups[group] = []
        column_groups[group].append(col)

    # Print statistics for each group
    for group, columns in column_groups.items():
        if group == 'price_ohlc':
            print(f"\n\033[96mPrice Data (OHLC):\033[0m")
        elif group == 'volume':
            print(f"\n\033[96mVolume Data:\033[0m")
        elif group == 'pressure':
            print(f"\n\033[96mPressure Indicators:\033[0m")
        else:
            print(f"\n\033[96mOther Data:\033[0m")

        # Print columns in row for common metrics
        for metric in ['mean', 'median', 'min', 'max', 'std', 'var']:
            values = []
            for col in columns:
                stats = desc_stats[col]
                if 'error' not in stats and metric in stats:
                    val = stats[metric]
                    if isinstance(val, float):
                        values.append(f"{col}: {val:.4f}")
                    else:
                        values.append(f"{col}: {val}")

            if values:
                print(f"  {metric.capitalize()}: {' | '.join(values)}")

        # Print remaining metrics separately for each column
        for col in columns:
            stats = desc_stats[col]
            if 'error' in stats:
                print(f"  {col} Error: {stats['error']}")
            else:
                other_metrics = [k for k in stats.keys() if k not in ['mean', 'median', 'min', 'max', 'std', 'var']]
                if other_metrics:
                    print(f"  {col} other metrics:")
                    for key in other_metrics:
                        value = stats[key]
                        if isinstance(value, float):
                            print(f"    {key}: {value:.4f}")
                        else:
                            print(f"    {key}: {value}")

    # Add summary and recommendations
    print("\n\033[1m\033[95mSummary and Recommendations:\033[0m")
    print("  • Статистические показатели позволяют оценить характеристики и качество данных")
    print("  • Высокая дисперсия может указывать на необходимость нормализации данных перед моделированием")
    print("  • Наличие существенной разницы между средним и медианой указывает на асимметрию распределения")
    print("  • Следующие шаги: проверка распределений и выявление аномалий с помощью --distribution-analysis и --outlier-analysis")

def print_distribution_analysis(dist_stats):
    """Print distribution analysis in a readable format."""
    print("\n\033[1m\033[94mDistribution Analysis:\033[0m")

    # Group columns by normality for summary
    normal_cols = []
    skewed_cols = []
    highly_skewed_cols = []
    heavy_tailed_cols = []

    for col, stats in dist_stats.items():
        print(f"\n\033[96m{col}:\033[0m")
        if 'error' in stats:
            print(f"  Error: {stats['error']}")
        else:
            skew = stats['skewness']
            kurt = stats['kurtosis']

            # Track for summary
            if stats['is_normal'] == 'Yes':
                normal_cols.append(col)
            if abs(skew) > 1:
                highly_skewed_cols.append((col, skew))
            elif abs(skew) > 0.5:
                skewed_cols.append((col, skew))
            if kurt > 3:
                heavy_tailed_cols.append((col, kurt))

            # Print individual stats
            print(f"  Skewness: {skew:.4f} ({'Положительная (правосторонняя)' if skew > 0 else 'Отрицательная (левосторонняя)' if skew < 0 else 'Нет'})")
            print(f"  Kurtosis: {kurt:.4f} ({'Тяжелые хвосты' if kurt > 3 else 'Легкие хвосты' if kurt < 3 else 'Нормальное'})")
            if stats['normality_test'] is not None:
                print(f"  Normality test p-value: {stats['normality_test'][1]:.4f}")
                print(f"  Distribution appears normal: {stats['is_normal']}")
            else:
                print("  Normality test: Not enough data points")

    # Add summary and recommendations
    print("\n\033[1m\033[95mSummary and Recommendations:\033[0m")
    print(f"  • Обнаружено {len(normal_cols)} колонок с нормальным распределением: {', '.join(normal_cols) if normal_cols else 'нет'}")
    if highly_skewed_cols:
        print(f"  • Обнаружены колонки с сильной асимметрией (skewness > 1): {', '.join([f'{col} ({skew:.2f})' for col, skew in highly_skewed_cols])}")
        print("  • Рекомендация: рассмотрите применение трансформации (log, sqrt, Box-Cox) для нормализации")
    if heavy_tailed_cols:
        print(f"  • Обнаружены колонки с тяжелыми хвостами (kurtosis > 3): {', '.join([f'{col} ({kurt:.2f})' for col, kurt in heavy_tailed_cols])}")
        print("  • Рекомендация: обратите внимание на возможные выбросы, используйте робастные методы")
    print("  • Следующие шаги: выполните анализ выбросов с помощью --outlier-analysis для выявления аномальных значений")

def print_outlier_analysis(outlier_stats):
    """Print outlier analysis in a readable format."""
    print("\n\033[1m\033[94mOutlier Analysis:\033[0m")

    # Track columns with significant outliers for summary
    high_outlier_cols = []

    for col, stats in outlier_stats.items():
        print(f"\n\033[96m{col}:\033[0m")
        if 'error' in stats:
            print(f"  Error: {stats['error']}")
        else:
            # Print IQR method results
            iqr_pct = stats['iqr_method']['outlier_percentage']
            print("  IQR Method:")
            print(f"    Lower bound: {stats['iqr_method']['lower_bound']:.4f}")
            print(f"    Upper bound: {stats['iqr_method']['upper_bound']:.4f}")
            print(f"    Outlier count: {stats['iqr_method']['outlier_count']}")
            print(f"    Outlier percentage: {iqr_pct}%")

            # Print Z-Score method results
            z_pct = stats['z_score_method']['outlier_percentage']
            print("  Z-Score Method:")
            print(f"    Outlier count: {stats['z_score_method']['outlier_count']}")
            print(f"    Outlier percentage: {z_pct}%")

            # Show sample outlier indices
            if stats['iqr_method']['outlier_indices']:
                print(f"  Sample outlier indices (IQR): {', '.join(map(str, stats['iqr_method']['outlier_indices']))}")

            # Track for summary
            if max(iqr_pct, z_pct) > 5:  # If more than 5% are outliers
                high_outlier_cols.append((col, max(iqr_pct, z_pct)))

    # Add summary and recommendations
    print("\n\033[1m\033[95mSummary and Recommendations:\033[0m")
    if high_outlier_cols:
        print(f"  • Обнаружено {len(high_outlier_cols)} колонок со значительным количеством выбросов (>5%):")
        for col, pct in high_outlier_cols:
            print(f"    - {col}: {pct:.2f}% выбросов")
        print("  • Рекомендации для обработки выбросов:")
        print("    1. Проверьте природу выбросов - ошибки измерений или истинные экстремальные значения")
        print("    2. Для ошибок: исправьте или удалите")
        print("    3. Для истинных выбросов: winsorization или робастные методы")
        print("    4. Для ML моделей: используйте алгоритмы, устойчивые к выбросам (RandomForest, Gradient Boosting)")
    else:
        print("  • Значительного количества выбросов не обнаружено (>5%)")

    print("  • Следующие шаги: рассмотрите вопрос об использовании --time-series-analysis для исследования временных паттернов")

def print_time_series_analysis(ts_stats):
    """Print time series analysis in a readable format."""
    print("\n\033[1m\033[94mTime Series Analysis:\033[0m")

    if 'error' in ts_stats:
        print(f"  Error: {ts_stats['error']}")
        return

    # Track information for summary
    has_features = False
    non_stationary_cols = []
    stationary_cols = []
    has_seasonality = False

    # Print derived features
    if 'features' in ts_stats and ts_stats['features']:
        has_features = True
        print("\n\033[96mDerived Features:\033[0m")

        # Group feature stats for more compact display
        for feature, stats in ts_stats['features'].items():
            feature_name = feature.replace('_', ' ').title()
            print(f"  {feature_name}: Mean: {stats['mean']:.4f} | Median: {stats['median']:.4f} | Std: {stats['std']:.4f}")

    # Print stationarity test results
    if 'stationarity' in ts_stats and ts_stats['stationarity']:
        print("\n\033[96mStationarity Tests (ADF):\033[0m")
        for col, result in ts_stats['stationarity'].items():
            print(f"  {col}:")
            if 'error' in result:
                print(f"    Error: {result['error']}")
            else:
                print(f"    Test statistic: {result['test_statistic']:.4f}")
                print(f"    p-value: {result['p_value']:.4f}")
                print(f"    Is stationary: {'Yes' if result['is_stationary'] else 'No'}")

                # Track for summary
                if result['is_stationary']:
                    stationary_cols.append(col)
                else:
                    non_stationary_cols.append(col)

    # Print seasonality analysis
    if 'seasonality' in ts_stats and ts_stats['seasonality']:
        print("\n\033[96mSeasonality Analysis:\033[0m")
        if 'day_of_week' in ts_stats['seasonality']:
            has_seasonality = True
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_stats = ts_stats['seasonality']['day_of_week']

            if 'error' in dow_stats:
                print(f"  Day of Week: {dow_stats['error']}")
            else:
                # Print all days in one line
                day_values = [f"{day_names[day_num]}: {mean_value:.4f}" for day_num, mean_value in dow_stats.items()]
                print("  Average by Day of Week: " + " | ".join(day_values))

    # Add summary and recommendations
    print("\n\033[1m\033[95mSummary and Recommendations:\033[0m")
    if has_features:
        print("  • Успешно рассчитаны производные признаки на основе временных рядов")

    # Stationarity advice
    if non_stationary_cols:
        print(f"  • Обнаружены нестационарные временные ряды: {', '.join(non_stationary_cols)}")
        print("  • Рекомендации для нестационарных рядов:")
        print("    1. Используйте дифференцирование (метод diff()) для устранения тренда")
        print("    2. Рассмотрите логарифмирование или другие трансформации для стабилизации дисперсии")
        print("    3. Для ML моделей: добавьте признаки тренда и используйте относительные изменения")

    if stationary_cols:
        print(f"  • Обнаружены стационарные временные ряды: {', '.join(stationary_cols)}")
        print("  • Стационарные ряды хорошо подходят для моделирования через ARIMA, GARCH и другие статистические методы")

    if has_seasonality:
        print("  • Обнаружены недельные сезонные паттерны")
        print("  • Рекомендации для работы с сезонностью:")
        print("    1. Добавьте категориальные признаки (день недели, месяц и т.д.)")
        print("    2. Для статистических моделей: используйте сезонное дифференцирование или SARIMA")
        print("    3. Для глубокого обучения: рассмотрите архитектуры с механизмами внимания")

    print("  • Следующие шаги: выполните корреляционный анализ с помощью --correlation-analysis для выявления взаимосвязей")
