# -*- coding: utf-8 -*-
# src/batch_eda/fix_files.py
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

        # Remove rows with NaN in datetime column for frequency analysis
        original_count = len(df)
        df_clean = df.dropna(subset=[dt_col])
        clean_count = len(df_clean)
        skipped_count = original_count - clean_count
        
        if df_clean.empty:
            print(f"Warning: No valid datetime values found in '{dt_col}', skipping gap fixing")
            return df
        
        if skipped_count > 0:
            print(f"Note: Skipped {skipped_count} rows with NaN values in '{dt_col}' for gap analysis")
        
        # Sort by datetime column
        df_clean = df_clean.sort_values(dt_col)

        # Get unique frequencies in the data
        time_diffs = df_clean[dt_col].diff().dropna()
        if time_diffs.empty:
            print("No time differences found, cannot determine frequency")
            return df

        # Find the most common frequency (mode of time differences)
        freq_counts = time_diffs.value_counts()
        most_common_freq = freq_counts.index[0]
        
        # Validate the frequency - it should be a valid timedelta
        if pd.isna(most_common_freq) or most_common_freq == pd.Timedelta(0):
            print(f"Warning: Invalid frequency detected ({most_common_freq}), using median frequency")
            # Use median frequency instead
            median_freq = time_diffs.median()
            if pd.isna(median_freq) or median_freq == pd.Timedelta(0):
                print("Warning: Cannot determine valid frequency, using alternative gap fixing method")
                # Use alternative method for irregular time series
                return _fix_gaps_irregular(df_clean, dt_col)
            most_common_freq = median_freq

        # Reindex with the most common frequency
        start_time = df_clean[dt_col].min()
        end_time = df_clean[dt_col].max()
        
        # Ensure start and end times are valid
        if pd.isna(start_time) or pd.isna(end_time):
            print("Warning: Invalid start or end time, skipping gap fixing")
            return df

        # Check if the gap is too large (more than 30 days)
        total_duration = end_time - start_time
        total_days = total_duration.days
        
        if total_days > 3650:  # More than 10 years
            print(f"Warning: Very large time range detected ({total_duration}), using specialized large range gap fixing method")
            return _fix_gaps_very_large_range(df_clean, dt_col)
        elif total_days > 30:  # More than 30 days but less than 10 years
            print(f"Warning: Large time range detected ({total_duration}), using alternative gap fixing method")
            return _fix_gaps_irregular(df_clean, dt_col)
        
        # Create a new index with regular frequency
        try:
            new_index = pd.date_range(start=start_time, end=end_time, freq=most_common_freq)
            
            # Check if the resulting index is too large
            if len(new_index) > 1000000:  # More than 1 million rows
                print(f"Warning: Very large index created ({len(new_index)} rows), using alternative gap fixing method")
                return _fix_gaps_irregular(df_clean, dt_col)
                
        except Exception as e:
            print(f"Warning: Could not create date range with frequency {most_common_freq}: {e}")
            print("Using alternative gap fixing method")
            return _fix_gaps_irregular(df_clean, dt_col)

        # Create a new DataFrame with the regular index and merge with original data
        temp_df = pd.DataFrame({dt_col: new_index})
        
        # Use merge_asof for better handling of large gaps
        try:
            merged_df = pd.merge_asof(temp_df, df_clean, on=dt_col, direction='nearest')
        except Exception as e:
            print(f"Warning: merge_asof failed, using regular merge: {e}")
            # Fallback to regular merge
            merged_df = pd.merge(temp_df, df_clean, on=dt_col, how='left')
        
        # Interpolate missing values for numeric columns
        numeric_cols = merged_df.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col != dt_col]  # Skip datetime column
        
        if numeric_cols:
            print(f"Interpolating {len(numeric_cols)} numeric columns...")
            with tqdm(total=len(numeric_cols), desc="Interpolating columns", unit="col") as pbar:
                for col in numeric_cols:
                    # Use linear interpolation instead of time-weighted
                    merged_df[col] = merged_df[col].interpolate(method='linear')
                    pbar.update(1)
                    pbar.set_postfix({'column': col})

        print(f"Fixed gaps in '{dt_col}' by reindexing with frequency {most_common_freq}")
        print(f"Original row count: {len(df)}, Clean data rows: {len(df_clean)}, New row count: {len(merged_df)}")

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
        
        # Validate the frequency - it should be a valid timedelta
        if pd.isna(most_common_freq) or most_common_freq == pd.Timedelta(0):
            print(f"Warning: Invalid frequency detected ({most_common_freq}), using median frequency")
            # Use median frequency instead
            median_freq = time_diffs.median()
            if pd.isna(median_freq) or median_freq == pd.Timedelta(0):
                print("Warning: Cannot determine valid frequency, skipping gap fixing")
                return df
            most_common_freq = median_freq

        # Reindex with the most common frequency
        start_time = df.index.min()
        end_time = df.index.max()
        
        # Ensure start and end times are valid
        if pd.isna(start_time) or pd.isna(end_time):
            print("Warning: Invalid start or end time, skipping gap fixing")
            return df

        # Check if the gap is too large (more than 30 days)
        total_duration = end_time - start_time
        total_days = total_duration.days
        
        if total_days > 3650:  # More than 10 years
            print(f"Warning: Very large time range detected ({total_duration}), this may take a very long time to process")
            print("Consider using a smaller time range or different frequency")
            print("For very large ranges, consider using the column-based gap fixing method instead")
        elif total_days > 30:  # More than 30 days but less than 10 years
            print(f"Warning: Large time range detected ({total_duration}), this may take a long time to process")
            print("Consider using a smaller time range or different frequency")
        
        # Create a new index with regular frequency
        try:
            new_index = pd.date_range(start=start_time, end=end_time, freq=most_common_freq)
            
            # Check if the resulting index is too large
            if len(new_index) > 1000000:  # More than 1 million rows
                print(f"Warning: Very large index created ({len(new_index)} rows), this may cause memory issues")
                print("Consider using a larger frequency or smaller time range")
                
        except Exception as e:
            print(f"Warning: Could not create date range with frequency {most_common_freq}: {e}")
            print("Skipping gap fixing")
            return df

        # Reindex and interpolate with progress bar
        print(f"Reindexing with frequency {most_common_freq}...")
        with tqdm(total=1, desc="Reindexing and interpolating", unit="step") as pbar:
            fixed_df = df.reindex(new_index).interpolate(method='time')
            pbar.update(1)

        print(f"Fixed gaps in index by reindexing with frequency {most_common_freq}")
        print(f"Original row count: {len(df)}, New row count: {len(fixed_df)}")

        return fixed_df

    else:
        print(f"Warning: Could not find datetime column '{dt_col}' in DataFrame")
        return df


def _fix_gaps_irregular(df, dt_col):
    """
    Alternative gap fixing method for irregular time series data.
    This method identifies large gaps and fills them with interpolated values
    without creating a regular time index.
    
    Args:
        df: pandas DataFrame with datetime column
        dt_col: Name of datetime column
        
    Returns:
        DataFrame with gaps filled using interpolation
    """
    print(f"Using irregular gap fixing method for '{dt_col}'")
    
    # Sort by datetime
    df_sorted = df.sort_values(dt_col).copy()
    
    # Calculate time differences
    time_diffs = df_sorted[dt_col].diff().dropna()
    
    if time_diffs.empty:
        print("No time differences found, cannot fix gaps")
        return df_sorted
    
    # Find large gaps (more than 2 standard deviations from mean)
    mean_diff = time_diffs.mean()
    std_diff = time_diffs.std()
    threshold = mean_diff + 2 * std_diff
    
    large_gaps = time_diffs[time_diffs > threshold]
    
    if large_gaps.empty:
        print("No large gaps detected, returning original data")
        return df_sorted
    
    print(f"Found {len(large_gaps)} large gaps to fill")
    
    # For each large gap, insert interpolated rows
    result_rows = []
    prev_idx = 0
    
    # Add progress bar for gap processing
    with tqdm(total=len(large_gaps), desc="Fixing time series gaps", unit="gap") as pbar:
        for i, (idx, gap_size) in enumerate(large_gaps.items()):
            # Add all rows up to the gap
            result_rows.append(df_sorted.iloc[prev_idx:idx])
            
            # Calculate how many interpolated rows to insert
            # Use a reasonable maximum to avoid creating too many rows
            max_interpolated_rows = min(1000, max(2, int(gap_size / mean_diff)))
            
            if max_interpolated_rows > 1:
                # Create interpolated timestamps
                start_time = df_sorted.iloc[idx-1][dt_col]
                end_time = df_sorted.iloc[idx][dt_col]
                
                # Create evenly spaced timestamps
                interpolated_times = pd.date_range(
                    start=start_time, 
                    end=end_time, 
                    periods=max_interpolated_rows + 2  # +2 to include start and end
                )[1:-1]  # Remove start and end points as they already exist
                
                # Create interpolated rows
                for interp_time in interpolated_times:
                    # Create a new row with interpolated values
                    new_row = df_sorted.iloc[idx-1].copy()
                    new_row[dt_col] = interp_time
                    
                    # Interpolate numeric columns
                    numeric_cols = df_sorted.select_dtypes(include=[np.number]).columns
                    for col in numeric_cols:
                        if col != dt_col:
                            # Simple linear interpolation between surrounding values
                            prev_val = df_sorted.iloc[idx-1][col]
                            next_val = df_sorted.iloc[idx][col]
                            
                            # Calculate interpolation factor
                            total_gap = (end_time - start_time).total_seconds()
                            current_gap = (interp_time - start_time).total_seconds()
                            factor = current_gap / total_gap if total_gap > 0 else 0.5
                            
                            new_row[col] = prev_val + factor * (next_val - prev_val)
                    
                    result_rows.append(pd.DataFrame([new_row]))
            
            prev_idx = idx
            pbar.update(1)
            pbar.set_postfix({
                'gap_size': str(gap_size).split('.')[0],  # Show gap size without microseconds
                'interpolated': max_interpolated_rows if max_interpolated_rows > 1 else 0
            })
    
    # Add remaining rows
    result_rows.append(df_sorted.iloc[prev_idx:])
    
    # Combine all rows
    if result_rows:
        result_df = pd.concat(result_rows, ignore_index=True)
        print(f"Fixed gaps using irregular method. Original: {len(df_sorted)}, Result: {len(result_df)}")
        return result_df
    else:
        return df_sorted


def _fix_gaps_very_large_range(df, dt_col):
    """
    Specialized gap fixing method for very large time ranges (10+ years).
    This method uses a more efficient approach to avoid creating too many interpolated rows.
    
    Args:
        df: pandas DataFrame with datetime column
        dt_col: Name of datetime column
        
    Returns:
        DataFrame with gaps filled using efficient interpolation
    """
    print(f"Using very large range gap fixing method for '{dt_col}'")
    
    # Sort by datetime
    df_sorted = df.sort_values(dt_col).copy()
    
    # Calculate time differences
    time_diffs = df_sorted[dt_col].diff().dropna()
    
    if time_diffs.empty:
        print("No time differences found, cannot fix gaps")
        return df_sorted
    
    # Calculate total time range
    total_range = df_sorted[dt_col].max() - df_sorted[dt_col].min()
    total_days = total_range.days
    
    print(f"Total time range: {total_days} days ({total_days/365.25:.1f} years)")
    
    # For very large ranges, use a more conservative approach
    # Only fix gaps that are significantly larger than the typical gap
    mean_diff = time_diffs.mean()
    median_diff = time_diffs.median()
    
    # Use a more conservative threshold for very large ranges
    if total_days > 3650:  # More than 10 years
        # Use 5x median instead of 2x std for very large ranges
        threshold = median_diff * 5
        print(f"Using conservative threshold: {threshold} (5x median)")
    else:
        # Use standard threshold for smaller ranges
        std_diff = time_diffs.std()
        threshold = mean_diff + 2 * std_diff
        print(f"Using standard threshold: {threshold} (mean + 2*std)")
    
    large_gaps = time_diffs[time_diffs > threshold]
    
    if large_gaps.empty:
        print("No large gaps detected, returning original data")
        return df_sorted
    
    print(f"Found {len(large_gaps)} large gaps to fill")
    
    # For very large ranges, limit the number of interpolated rows per gap
    if total_days > 3650:  # More than 10 years
        max_rows_per_gap = 10  # Very conservative
        print(f"Limiting to {max_rows_per_gap} interpolated rows per gap for large time range")
    else:
        max_rows_per_gap = 100  # Standard limit
    
    # For each large gap, insert interpolated rows
    result_rows = []
    prev_idx = 0
    
    # Add progress bar for gap processing
    with tqdm(total=len(large_gaps), desc="Fixing time series gaps", unit="gap") as pbar:
        for i, (idx, gap_size) in enumerate(large_gaps.items()):
            # Add all rows up to the gap
            result_rows.append(df_sorted.iloc[prev_idx:idx])
            
            # Calculate how many interpolated rows to insert
            # Use a very conservative approach for large ranges
            if total_days > 3650:
                # For very large ranges, use fixed number of interpolated rows
                max_interpolated_rows = min(max_rows_per_gap, max(1, int(gap_size / pd.Timedelta(days=30))))
            else:
                # For smaller ranges, use the original logic
                max_interpolated_rows = min(max_rows_per_gap, max(2, int(gap_size / mean_diff)))
            
            if max_interpolated_rows > 1:
                # Create interpolated timestamps
                start_time = df_sorted.iloc[idx-1][dt_col]
                end_time = df_sorted.iloc[idx][dt_col]
                
                # Create evenly spaced timestamps
                interpolated_times = pd.date_range(
                    start=start_time, 
                    end=end_time, 
                    periods=max_interpolated_rows + 2  # +2 to include start and end
                )[1:-1]  # Remove start and end points as they already exist
                
                # Create interpolated rows
                for interp_time in interpolated_times:
                    # Create a new row with interpolated values
                    new_row = df_sorted.iloc[idx-1].copy()
                    new_row[dt_col] = interp_time
                    
                    # Interpolate numeric columns
                    numeric_cols = df_sorted.select_dtypes(include=[np.number]).columns
                    for col in numeric_cols:
                        if col != dt_col:
                            # Simple linear interpolation between surrounding values
                            prev_val = df_sorted.iloc[idx-1][col]
                            next_val = df_sorted.iloc[idx][col]
                            
                            # Calculate interpolation factor
                            total_gap = (end_time - start_time).total_seconds()
                            current_gap = (interp_time - start_time).total_seconds()
                            factor = current_gap / total_gap if total_gap > 0 else 0.5
                            
                            new_row[col] = prev_val + factor * (next_val - prev_val)
                    
                    result_rows.append(pd.DataFrame([new_row]))
            
            prev_idx = idx
            pbar.update(1)
            pbar.set_postfix({
                'gap_size': str(gap_size).split('.')[0],  # Show gap size without microseconds
                'interpolated': max_interpolated_rows if max_interpolated_rows > 1 else 0
            })
    
    # Add remaining rows
    result_rows.append(df_sorted.iloc[prev_idx:])
    
    # Combine all rows
    if result_rows:
        result_df = pd.concat(result_rows, ignore_index=True)
        print(f"Gap fixing completed. Original rows: {len(df_sorted)}, New rows: {len(result_df)}")
        return result_df
    else:
        return df_sorted


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
        # Try to detect OHLCV columns (exclude pressure_vector which can be negative)
        ohlcv_keys = ['open', 'high', 'low', 'close', 'volume', 'amount', 'qty']
        for col in df.select_dtypes(include=[np.number]).columns:
            col_lower = col.lower()
            # Skip pressure_vector as it can legitimately be negative
            if col_lower == 'pressure_vector':
                continue
            if any(key in col_lower for key in ohlcv_keys):
                columns_to_fix.append(col)

    for col in columns_to_fix:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame")
            continue

        # Skip pressure_vector as it can legitimately be negative
        if col.lower() == 'pressure_vector':
            print(f"Skipping pressure_vector column as it can legitimately contain negative values")
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
