# Handles fixing files
import os
import pandas as pd
import numpy as np
from tqdm import tqdm


def fix_nan(df, nan_summary=None):
    """
    Fixes NaN values in a DataFrame. Strategy depends on column type:
    - Numeric columns: Fills with median
    - String columns: Fills with mode or empty string
    - Datetime columns: Uses forward fill, then backward fill

    Args:
        df: pandas DataFrame with NaN values
        nan_summary: List of dictionaries with info about NaN columns

    Returns:
        Fixed pandas DataFrame
    """
    fixed_df = df.copy()

    # Use nan_summary if provided, otherwise detect all columns with NaN
    columns_to_fix = []
    if nan_summary:
        columns_to_fix = [item['column'] for item in nan_summary]
    else:
        columns_to_fix = [col for col in df.columns if df[col].isna().any()]

    for col in columns_to_fix:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame")
            continue

        # Determine fix strategy based on column type
        if pd.api.types.is_numeric_dtype(df[col]):
            # For numeric columns, fill with median
            median_val = df[col].median()
            fixed_df[col] = df[col].fillna(median_val)
            print(f"Fixed NaN in column '{col}' with median value: {median_val}")

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            # For datetime, try forward fill then backward fill
            fixed_df[col] = df[col].ffill().bfill()
            print(f"Fixed NaN in datetime column '{col}' with forward/backward fill")

        elif pd.api.types.is_string_dtype(df[col]) or df[col].dtype == 'object':
            # For string/object columns, fill with mode or empty string
            if df[col].count() > 0:
                mode_val = df[col].mode().iloc[0] if not df[col].mode().empty else ""
                fixed_df[col] = df[col].fillna(mode_val)
                print(f"Fixed NaN in string column '{col}' with mode value: '{mode_val}'")
            else:
                fixed_df[col] = df[col].fillna("")
                print(f"Fixed NaN in string column '{col}' with empty string")

        else:
            # For other types, use forward fill
            fixed_df[col] = df[col].ffill().bfill()
            print(f"Fixed NaN in column '{col}' with forward/backward fill")

    return fixed_df


def fix_duplicates(df, dupe_summary=None):
    """
    Fixes duplicate rows in a DataFrame by keeping the first occurrence.

    Args:
        df: pandas DataFrame with duplicated rows
        dupe_summary: List of dictionaries with info about duplicated rows/values

    Returns:
        Fixed pandas DataFrame with duplicates removed
    """
    initial_rows = len(df)
    fixed_df = df.drop_duplicates(keep='first')
    removed_rows = initial_rows - len(fixed_df)

    if removed_rows > 0:
        print(f"Removed {removed_rows} duplicate rows from DataFrame")
    else:
        print("No duplicate rows found or removed")

    # For columns with duplicated values, we don't modify them as they might be legitimate
    # Just log the information
    if dupe_summary:
        for entry in dupe_summary:
            if entry['type'] == 'column':
                print(f"Note: Column '{entry['column']}' has {entry['count']} duplicated values. No action taken.")

    return fixed_df


def fix_gaps(df, gap_summary=None, datetime_col=None):
    """
    Fixes gaps in time series by interpolating missing values.

    Args:
        df: pandas DataFrame with gaps in datetime column
        gap_summary: List of dictionaries with info about gaps
        datetime_col: Name of datetime column. If None, will try to detect automatically.

    Returns:
        Fixed pandas DataFrame with gaps filled
    """
    if df.empty:
        print("Warning: Empty DataFrame, cannot fix gaps")
        return df

    # Find the datetime column if not specified
    dt_col = datetime_col
    if not dt_col:
        # Try to detect from gap_summary
        if gap_summary and len(gap_summary) > 0 and 'column' in gap_summary[0]:
            dt_col = gap_summary[0]['column']
        else:
            # Try to detect from DataFrame by dtype first
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    dt_col = col
                    print(f"Found datetime column: {col} by dtype")
                    break

            # If still not found, try common date/time column names (case-insensitive)
            if not dt_col:
                common_datetime_names = ['date', 'time', 'datetime', 'timestamp', 'time_open',
                                        'date_time', 'day', 'time_close', 'timeopen', 'timeclose']

                for name in common_datetime_names:
                    for col in df.columns:
                        if name in col.lower():
                            try:
                                df[col] = pd.to_datetime(df[col])
                                dt_col = col
                                print(f"Found and converted datetime column: {col} by name")
                                break
                            except:
                                pass
                    if dt_col:
                        break

                # Check if there's a column that might be numeric timestamp
                if not dt_col:
                    for col in df.select_dtypes(include=['int64', 'float64']).columns:
                        # Try to convert numeric column if it looks like a timestamp (high values)
                        if df[col].mean() > 1000000:  # Likely timestamp (seconds or milliseconds since epoch)
                            try:
                                # Try seconds format first
                                test_dt = pd.to_datetime(df[col].iloc[0], unit='s')
                                if test_dt.year > 1990 and test_dt.year < 2050:  # Sensible year range
                                    df[col] = pd.to_datetime(df[col], unit='s')
                                    dt_col = col
                                    print(f"Converted numeric column {col} to datetime (seconds)")
                                    break
                            except:
                                try:
                                    # Try milliseconds format
                                    test_dt = pd.to_datetime(df[col].iloc[0], unit='ms')
                                    if test_dt.year > 1990 and test_dt.year < 2050:  # Sensible year range
                                        df[col] = pd.to_datetime(df[col], unit='ms')
                                        dt_col = col
                                        print(f"Converted numeric column {col} to datetime (milliseconds)")
                                        break
                                except:
                                    pass

                # If still no column found but index is datetime, use index
                if not dt_col and pd.api.types.is_datetime64_any_dtype(df.index):
                    dt_col = 'index'
                    print("Using DataFrame index as datetime")

    if not dt_col:
        print("Warning: Could not identify datetime column, cannot fix gaps")
        # Print column names and types to help diagnose the issue
        for col in df.columns:
            print(f"Column: {col}, Type: {df[col].dtype}, Sample: {df[col].iloc[0] if not df.empty else None}")
        return df

    if dt_col != 'index' and dt_col in df.columns:
        # Make sure column is actually datetime type
        if not pd.api.types.is_datetime64_any_dtype(df[dt_col]):
            try:
                df[dt_col] = pd.to_datetime(df[dt_col])
                print(f"Converted '{dt_col}' to datetime")
            except Exception as e:
                print(f"Warning: Could not convert '{dt_col}' to datetime: {e}")
                return df

        # Sort by datetime column
        df = df.sort_values(dt_col)

        # Get unique frequencies in the data
        time_diffs = df[dt_col].diff().dropna()
        if time_diffs.empty:
            print("No time differences found, cannot determine frequency")
            return df

        # Find the most common frequency (mode of time differences)
        freq_counts = time_diffs.value_counts()
        most_common_freq = freq_counts.index[0]

        # Reindex with the most common frequency
        start_time = df[dt_col].min()
        end_time = df[dt_col].max()

        # Create a new index with regular frequency
        new_index = pd.date_range(start=start_time, end=end_time, freq=most_common_freq)

        # Create a new DataFrame with the regular index and merge with original data
        temp_df = pd.DataFrame({dt_col: new_index})
        merged_df = pd.merge_asof(temp_df, df, on=dt_col, direction='nearest')

        print(f"Fixed gaps in '{dt_col}' by reindexing with frequency {most_common_freq}")
        print(f"Original row count: {len(df)}, New row count: {len(merged_df)}")

        return merged_df

    elif dt_col == 'index' or pd.api.types.is_datetime64_any_dtype(df.index):
        # DataFrame has datetime index
        df = df.sort_index()

        # Get unique frequencies in the data
        time_diffs = pd.Series(df.index).diff().dropna()
        if time_diffs.empty:
            print("No time differences found, cannot determine frequency")
            return df

        # Find the most common frequency
        freq_counts = time_diffs.value_counts()
        most_common_freq = freq_counts.index[0]

        # Reindex with the most common frequency
        start_time = df.index.min()
        end_time = df.index.max()

        # Create a new index with regular frequency
        new_index = pd.date_range(start=start_time, end=end_time, freq=most_common_freq)

        # Reindex and interpolate
        fixed_df = df.reindex(new_index).interpolate(method='time')

        print(f"Fixed gaps in index by reindexing with frequency {most_common_freq}")
        print(f"Original row count: {len(df)}, New row count: {len(fixed_df)}")

        return fixed_df

    else:
        print(f"Warning: Could not find datetime column '{dt_col}' in DataFrame")
        return df


def fix_zeros(df, zero_summary=None):
    """
    Fixes zero values in numeric columns that shouldn't have zeros.
    Only fixes columns marked as anomalies in zero_summary.

    Args:
        df: pandas DataFrame with zero values
        zero_summary: List of dictionaries with info about zero values

    Returns:
        Fixed pandas DataFrame
    """
    fixed_df = df.copy()

    # Only fix columns marked as anomalies in zero_summary
    columns_to_fix = []
    if zero_summary:
        columns_to_fix = [item['column'] for item in zero_summary if item.get('anomaly', False) is True]

    # If no summary or no anomalies marked, detect price-related columns
    if not columns_to_fix:
        for col in df.select_dtypes(include=[np.number]).columns:
            col_lower = col.lower()
            # Only fix price columns, not volume/quantity columns
            if any(key in col_lower for key in ['price', 'close', 'open', 'high', 'low', 'pressure']):
                columns_to_fix.append(col)

    for col in columns_to_fix:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame")
            continue

        # Count zeros
        zeros_mask = df[col] == 0
        zero_count = zeros_mask.sum()

        if zero_count > 0:
            # Get previous and next non-zero values for each zero
            fixed_df[col] = df[col].replace(0, np.nan)
            fixed_df[col] = fixed_df[col].ffill().bfill()

            # If still NaN (e.g., at the start/end), use median of non-zero values
            if fixed_df[col].isna().any():
                median_nonzero = df[df[col] != 0][col].median()
                fixed_df[col] = fixed_df[col].fillna(median_nonzero)

            print(f"Fixed {zero_count} zero values in column '{col}'")

    return fixed_df


def fix_negatives(df, negative_summary=None):
    """
    Fixes negative values in OHLCV columns that shouldn't be negative.

    Args:
        df: pandas DataFrame with negative values
        negative_summary: List of dictionaries with info about negative values

    Returns:
        Fixed pandas DataFrame
    """
    fixed_df = df.copy()

    columns_to_fix = []
    if negative_summary:
        columns_to_fix = [item['column'] for item in negative_summary]
    else:
        # Try to detect OHLCV columns
        ohlcv_keys = ['open', 'high', 'low', 'close', 'volume', 'amount', 'qty']
        for col in df.select_dtypes(include=[np.number]).columns:
            col_lower = col.lower()
            if any(key in col_lower for key in ohlcv_keys):
                columns_to_fix.append(col)

    for col in columns_to_fix:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame")
            continue

        # Count negatives
        neg_mask = df[col] < 0
        neg_count = neg_mask.sum()

        if neg_count > 0:
            # For OHLCV columns, take absolute values
            col_lower = col.lower()
            if any(key in col_lower for key in ['open', 'high', 'low', 'close', 'price']):
                fixed_df.loc[neg_mask, col] = df.loc[neg_mask, col].abs()
                print(f"Fixed {neg_count} negative values in column '{col}' by taking absolute values")
            elif any(key in col_lower for key in ['volume', 'amount', 'qty']):
                # For volume, if negative, replace with previous/next values
                fixed_df.loc[neg_mask, col] = np.nan
                fixed_df[col] = fixed_df[col].ffill().bfill()

                # If still NaN, use median of positive values
                if fixed_df[col].isna().any():
                    median_pos = df[df[col] >= 0][col].median()
                    fixed_df[col] = fixed_df[col].fillna(median_pos)

                print(f"Fixed {neg_count} negative values in volume column '{col}' by interpolation")
            else:
                # For other columns specified in negative_summary, take absolute values as default
                fixed_df.loc[neg_mask, col] = df.loc[neg_mask, col].abs()
                print(f"Fixed {neg_count} negative values in column '{col}' by taking absolute values (default behavior)")

    return fixed_df


def fix_infs(df, inf_summary=None):
    """
    Fixes infinite values in numeric columns.

    Args:
        df: pandas DataFrame with infinite values
        inf_summary: List of dictionaries with info about infinite values

    Returns:
        Fixed pandas DataFrame
    """
    fixed_df = df.copy()

    # Find columns with inf values
    columns_to_fix = []
    if inf_summary:
        columns_to_fix = [item['column'] for item in inf_summary]
    else:
        # Detect all columns with inf values
        for col in df.select_dtypes(include=[np.number]).columns:
            if np.isinf(df[col]).any():
                columns_to_fix.append(col)

    for col in columns_to_fix:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame")
            continue

        # Count inf values
        inf_mask = np.isinf(df[col])
        inf_count = inf_mask.sum()

        if inf_count > 0:
            # Replace inf/-inf with NaN, then interpolate
            fixed_df[col] = df[col].replace([np.inf, -np.inf], np.nan)

            # Fill with previous/next valid values
            fixed_df[col] = fixed_df[col].interpolate(method='linear').ffill().bfill()

            # If still NaN (e.g., at the start/end), use median
            if fixed_df[col].isna().any():
                valid_values = df[~np.isinf(df[col])][col]
                if not valid_values.empty:
                    median_val = valid_values.median()
                    fixed_df[col] = fixed_df[col].fillna(median_val)

            print(f"Fixed {inf_count} infinite values in column '{col}'")

    return fixed_df


def fix_file(filepath, fix_nan_flag=False, fix_duplicates_flag=False, fix_gaps_flag=False,
             fix_zeros_flag=False, fix_negatives_flag=False, fix_infs_flag=False):
    """
    Fixes issues in a parquet file and saves the fixed version.

    Args:
        filepath: Path to the parquet file to fix
        fix_nan_flag: Fix NaN values
        fix_duplicates_flag: Fix duplicate rows
        fix_gaps_flag: Fix gaps in time series
        fix_zeros_flag: Fix zero values in price columns
        fix_negatives_flag: Fix negative values in OHLCV columns
        fix_infs_flag: Fix infinite values

    Returns:
        True if file was fixed, False otherwise
    """
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found")
        return False

    try:
        # Load the file
        df = pd.read_parquet(filepath)
        original_df = df.copy()
        print(f"Loaded file {filepath} with {len(df)} rows and {len(df.columns)} columns")

        # Apply fixes based on flags
        applied_fixes = []

        if fix_nan_flag:
            df = fix_nan(df)
            applied_fixes.append("NaN values")

        if fix_duplicates_flag:
            df = fix_duplicates(df)
            applied_fixes.append("duplicate rows")

        if fix_gaps_flag:
            df = fix_gaps(df)
            applied_fixes.append("gaps in time series")

        if fix_zeros_flag:
            df = fix_zeros(df)
            applied_fixes.append("zero values")

        if fix_negatives_flag:
            df = fix_negatives(df)
            applied_fixes.append("negative values")

        if fix_infs_flag:
            df = fix_infs(df)
            applied_fixes.append("infinite values")

        # Check if any fixes were actually applied
        if original_df.equals(df):
            print(f"No changes were made to {filepath}")
            return False

        # Create backup of original file
        backup_path = filepath + ".bak"
        original_df.to_parquet(backup_path)
        print(f"Created backup at {backup_path}")

        # Save fixed file
        df.to_parquet(filepath)
        print(f"Saved fixed file to {filepath} with fixes: {', '.join(applied_fixes)}")

        return True

    except Exception as e:
        print(f"Error fixing file {filepath}: {str(e)}")
        return False


def batch_fix_files(directory, fix_nan_flag=False, fix_duplicates_flag=False, fix_gaps_flag=False,
                    fix_zeros_flag=False, fix_negatives_flag=False, fix_infs_flag=False):
    """
    Batch fix all parquet files in a directory and its subdirectories.

    Args:
        directory: Directory containing parquet files
        fix_nan_flag: Fix NaN values
        fix_duplicates_flag: Fix duplicate rows
        fix_gaps_flag: Fix gaps in time series
        fix_zeros_flag: Fix zero values in price columns
        fix_negatives_flag: Fix negative values in OHLCV columns
        fix_infs_flag: Fix infinite values

    Returns:
        Tuple of (number of files fixed, total number of files processed)
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory {directory} not found")
        return (0, 0)

    # Find all parquet files
    parquet_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.parquet'):
                parquet_files.append(os.path.join(root, file))

    # No parquet files found
    if not parquet_files:
        print(f"No parquet files found in {directory}")
        return (0, 0)

    # Fix files with progress bar
    fixed_count = 0
    with tqdm(total=len(parquet_files), desc="Fixing files", position=0) as pbar:
        for filepath in parquet_files:
            was_fixed = fix_file(
                filepath,
                fix_nan_flag=fix_nan_flag,
                fix_duplicates_flag=fix_duplicates_flag,
                fix_gaps_flag=fix_gaps_flag,
                fix_zeros_flag=fix_zeros_flag,
                fix_negatives_flag=fix_negatives_flag,
                fix_infs_flag=fix_infs_flag
            )
            if was_fixed:
                fixed_count += 1
            pbar.update(1)

    print(f"Fixed {fixed_count} out of {len(parquet_files)} files")
    return (fixed_count, len(parquet_files))
