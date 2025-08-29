# Handles data quality checks with aggressive memory optimization
import gc
import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import warnings

def _estimate_memory_usage(df) -> int:
    """Estimate memory usage of DataFrame in MB."""
    try:
        memory_usage = df.memory_usage(deep=True).sum()
        memory_mb = int(memory_usage / (1024 * 1024))  # Convert to MB
        return max(1, memory_mb)  # Ensure at least 1MB
    except Exception:
        # Conservative fallback estimation
        total_bytes = 0
        for col in df.columns:
            if df[col].dtype == 'object':
                # String columns: estimate 32 bytes per value
                total_bytes += df[col].shape[0] * 32
            elif df[col].dtype in ['int64', 'float64']:
                # Numeric columns: 8 bytes per value
                total_bytes += df[col].shape[0] * 8
            elif df[col].dtype in ['int32', 'float32']:
                # 32-bit columns: 4 bytes per value
                total_bytes += df[col].shape[0] * 4
            else:
                # Default: 16 bytes per value
                total_bytes += df[col].shape[0] * 16
        
        fallback_mb = total_bytes // (1024 * 1024)
        return max(1, fallback_mb)  # Ensure at least 1MB

def _check_memory_available(max_memory_mb: int = 1024) -> bool:
    """Check if we have enough memory available."""
    try:
        import psutil
        available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
        return available_memory > max_memory_mb * 0.3  # Keep 30% buffer
    except ImportError:
        # If psutil not available, assume we're OK
        return True

def _get_memory_settings() -> Dict[str, int]:
    """Get memory optimization settings from environment."""
    return {
        'max_memory_mb': int(os.environ.get('MAX_MEMORY_MB', '4096')),  # Increased from 1024 to 4096
        'chunk_size': int(os.environ.get('CHUNK_SIZE', '50000')),  # Increased from 25000 to 50000
        'sample_size': int(os.environ.get('SAMPLE_SIZE', '10000')),
        'enable_memory_optimization': os.environ.get('ENABLE_MEMORY_OPTIMIZATION', 'true').lower() == 'true'
    }

def _process_large_dataframe_in_chunks(df, operation_func, chunk_size: int = 25000, max_memory_mb: int = 1024):
    """Process large DataFrame in chunks to manage memory usage."""
    total_rows = len(df)
    
    if total_rows <= chunk_size:
        # Small DataFrame, process directly
        return operation_func(df)
    
    # Large DataFrame, process in chunks
    results = []
    processed_rows = 0
    
    print(f"    📊 Processing {total_rows:,} rows in chunks of {chunk_size:,}...")
    
    for start_idx in range(0, total_rows, chunk_size):
        end_idx = min(start_idx + chunk_size, total_rows)
        chunk = df.iloc[start_idx:end_idx]
        
        # Process chunk
        try:
            chunk_result = operation_func(chunk)
            results.append(chunk_result)
            processed_rows = end_idx
            
            # Show progress for very large datasets
            if total_rows > 100000 and processed_rows % (chunk_size * 5) == 0:
                progress = (processed_rows / total_rows) * 100
                print(f"    📈 Progress: {progress:.1f}% ({processed_rows:,}/{total_rows:,} rows)")
                
        except Exception as e:
            print(f"⚠️  Error processing chunk at rows {start_idx}-{end_idx}: {e}")
            # Continue with next chunk instead of failing completely
            continue
        finally:
            # Memory management - always clean up
            del chunk
            gc.collect()
        
        # Check memory availability more frequently for very large datasets
        if processed_rows % (chunk_size * 2) == 0:
            if not _check_memory_available(max_memory_mb):
                print(f"⚠️  Low memory detected during processing, stopping at row {end_idx}")
                print(f"    📊 Processed {processed_rows:,} out of {total_rows:,} rows")
                break
    
    # Combine results
    if results:
        if isinstance(results[0], dict):
            # Combine dictionaries
            combined = {}
            for result in results:
                for key, value in result.items():
                    if key in combined:
                        if isinstance(combined[key], (int, float)):
                            combined[key] += value
                        elif isinstance(combined[key], list):
                            combined[key].extend(value)
                    else:
                        combined[key] = value
            return combined
        elif isinstance(results[0], list):
            # Combine lists
            combined = []
            for result in results:
                combined.extend(result)
            return combined
        else:
            # For other types, return the list
            return results
    
    return None

def nan_check(df, nan_summary, Fore, Style):
    """
    Performs NaN check with aggressive memory optimization for large datasets.
    """
    print(f"  {Fore.MAGENTA}Data Quality Check: Missing values (NaN){Style.RESET_ALL}")
    
    # Get memory settings
    settings = _get_memory_settings()
    memory_mb = _estimate_memory_usage(df)
    max_memory_mb = settings['max_memory_mb']
    
    # For extremely large datasets, use aggressive sampling
    if memory_mb > max_memory_mb * 3.0:  # Increased from 2.0 to 3.0
        print(f"    📊 Extremely large dataset detected ({memory_mb}MB), using aggressive sampling...")
        
        try:
            # Use very small sample for extremely large datasets
            sample_size = min(5000, len(df) // 50)  # Sample 2% or 5k rows, whichever is smaller
            sample_df = df.sample(n=sample_size, random_state=42)
            
            for col in sample_df.columns:
                n_missing_sample = sample_df[col].isna().sum()
                if n_missing_sample > 0:
                    # Estimate total missing values
                    estimated_missing = int((n_missing_sample / sample_size) * len(df))
                    estimated_percent = 100 * estimated_missing / len(df)
                    
                    print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: ~{estimated_missing} missing ({estimated_percent:.2f}%) [estimated from sample]")
                    
                    nan_summary.append({
                        'column': col,
                        'missing': estimated_missing,
                        'percent': estimated_percent,
                        'method': 'aggressive_sampling'
                    })
            return
            
        except Exception as e:
            print(f"    ⚠️  Error in aggressive sampling: {e}")
            print(f"    Skipping NaN check for extremely large dataset")
            return
    
    # For very large datasets, use sampling approach
    elif memory_mb > max_memory_mb * 1.5:  # Increased from 1.0 to 1.5
        print(f"    📊 Very large dataset detected ({memory_mb}MB), using sampling approach...")
        
        try:
            # Use sampling for very large datasets
            sample_size = min(settings['sample_size'], len(df) // 20)  # Sample 5% or sample_size rows
            sample_df = df.sample(n=sample_size, random_state=42)
            
            for col in sample_df.columns:
                n_missing_sample = sample_df[col].isna().sum()
                if n_missing_sample > 0:
                    # Estimate total missing values
                    estimated_missing = int((n_missing_sample / sample_size) * len(df))
                    estimated_percent = 100 * estimated_missing / len(df)
                    
                    print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: ~{estimated_missing} missing ({estimated_percent:.2f}%) [estimated from sample]")
                    
                    nan_summary.append({
                        'column': col,
                        'missing': estimated_missing,
                        'percent': estimated_percent,
                        'method': 'sampling'
                    })
            return
            
        except Exception as e:
            print(f"    ⚠️  Error in sampling approach: {e}")
            print(f"    Skipping NaN check for very large dataset")
            return
    
    # For large datasets, use chunked processing
    elif memory_mb > max_memory_mb * 0.5:
        print(f"    📊 Large dataset detected ({memory_mb}MB), using chunked processing...")
        
        def process_nan_chunk(chunk):
            chunk_nan_summary = []
            for col in chunk.columns:
                n_missing = chunk[col].isna().sum()
                if n_missing > 0:
                    percent = 100 * n_missing / len(chunk)
                    chunk_nan_summary.append({
                        'column': col,
                        'missing': n_missing,
                        'percent': percent
                    })
            return chunk_nan_summary
        
        # Process in chunks with smaller chunk size for large datasets
        chunk_size = min(settings['chunk_size'], 10000)
        chunk_results = _process_large_dataframe_in_chunks(df, process_nan_chunk, chunk_size=chunk_size)
        
        if chunk_results and isinstance(chunk_results, list):
            # Aggregate results from chunks
            column_nan_counts = {}
            for chunk_result in chunk_results:
                for item in chunk_result:
                    col = item['column']
                    if col in column_nan_counts:
                        column_nan_counts[col]['missing'] += item['missing']
                    else:
                        column_nan_counts[col] = item.copy()
            
            # Calculate percentages and display results
            for col, info in column_nan_counts.items():
                percent = 100 * info['missing'] / len(df)
                print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {info['missing']} missing ({percent:.2f}%)")
                
                nan_summary.append({
                    'column': col,
                    'missing': info['missing'],
                    'percent': percent,
                    'method': 'chunked'
                })
    else:
        # Process normally for smaller DataFrames
        for col in df.columns:
            n_missing = df[col].isna().sum()
            if n_missing > 0:
                percent = 100 * n_missing / len(df)
                print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {n_missing} missing ({percent:.2f}%)")
                
                # Show example rows with NaN (only for first few columns)
                if len(nan_summary) < 3:
                    try:
                        nan_rows = df[df[col].isna()].head(3)
                        print(f"      Example rows with NaN in {col}:")
                        print(nan_rows.to_string())
                    except Exception as e:
                        print(f"      Could not display example rows: {e}")
                
                nan_summary.append({
                    'column': col,
                    'missing': n_missing,
                    'percent': percent,
                    'method': 'direct'
                })

def duplicate_check(df, dupe_summary, Fore, Style):
    """
    Performs duplicate check with aggressive memory optimization for large datasets.
    """
    print(f"  {Fore.MAGENTA}Data Quality Check: Duplicates{Style.RESET_ALL}")
    
    # Get memory settings
    settings = _get_memory_settings()
    memory_mb = _estimate_memory_usage(df)
    max_memory_mb = settings['max_memory_mb']
    
    # For extremely large datasets, use aggressive sampling
    if memory_mb > max_memory_mb * 3.0:  # Increased from 2.0 to 3.0
        print(f"    📊 Extremely large dataset detected ({memory_mb}MB), using aggressive sampling for duplicate detection...")
        
        try:
            # Use very small sample for extremely large datasets
            sample_size = min(5000, len(df) // 50)  # Sample 2% or 5k rows
            sample_df = df.sample(n=sample_size, random_state=42)
            
            # Check for duplicates in sample
            n_dupes_sample = sample_df.duplicated().sum()
            if n_dupes_sample > 0:
                # Estimate total duplicates
                estimated_dupes = int((n_dupes_sample / sample_size) * len(df))
                estimated_percent = 100 * estimated_dupes / len(df)
                
                print(f"    {Fore.YELLOW}Estimated fully duplicated rows{Style.RESET_ALL}: ~{estimated_dupes} ({estimated_percent:.2f}%) [from sample]")
                
                dupe_summary.append({
                    'type': 'full_duplicates',
                    'count': estimated_dupes,
                    'percent': estimated_percent,
                    'method': 'aggressive_sampling'
                })
            else:
                print(f"    {Fore.GREEN}No duplicates detected in sample{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"    ⚠️  Error in aggressive sampling: {e}")
            print(f"    Skipping duplicate check for extremely large dataset")
            return
    
    # For very large datasets, use sampling approach
    elif memory_mb > max_memory_mb * 1.0:
        print(f"    📊 Very large dataset detected ({memory_mb}MB), using sampling for duplicate detection...")
        
        try:
            # Use sampling for very large datasets
            sample_size = min(settings['sample_size'], len(df) // 20)  # Sample 5% or sample_size rows
            sample_df = df.sample(n=sample_size, random_state=42)
            
            # Check for duplicates in sample
            n_dupes_sample = sample_df.duplicated().sum()
            if n_dupes_sample > 0:
                # Estimate total duplicates
                estimated_dupes = int((n_dupes_sample / sample_size) * len(df))
                estimated_percent = 100 * estimated_dupes / len(df)
                
                print(f"    {Fore.YELLOW}Estimated fully duplicated rows{Style.RESET_ALL}: ~{estimated_dupes} ({estimated_percent:.2f}%) [from sample]")
                
                dupe_summary.append({
                    'type': 'full_duplicates',
                    'count': estimated_dupes,
                    'percent': estimated_percent,
                    'method': 'sampling'
                })
            else:
                print(f"    {Fore.GREEN}No duplicates detected in sample{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"    ⚠️  Error in sampling approach: {e}")
            print(f"    Skipping duplicate check for very large dataset")
            return
    
    # For large datasets, use chunked processing
    elif memory_mb > max_memory_mb * 0.5:
        print(f"    📊 Large dataset detected ({memory_mb}MB), using chunked processing for duplicate detection...")
        
        def process_dupe_chunk(chunk):
            n_dupes = chunk.duplicated().sum()
            return {'duplicates': n_dupes}
        
        # Process in chunks
        chunk_size = min(settings['chunk_size'], 10000)
        chunk_results = _process_large_dataframe_in_chunks(df, process_dupe_chunk, chunk_size=chunk_size)
        
        if chunk_results and isinstance(chunk_results, dict):
            total_dupes = chunk_results.get('duplicates', 0)
            if total_dupes > 0:
                percent = 100 * total_dupes / len(df)
                print(f"    {Fore.YELLOW}Total duplicated rows{Style.RESET_ALL}: {total_dupes} ({percent:.2f}%)")
                
                dupe_summary.append({
                    'type': 'full_duplicates',
                    'count': total_dupes,
                    'percent': percent,
                    'method': 'chunked'
                })
            else:
                print(f"    {Fore.GREEN}No duplicates detected{Style.RESET_ALL}")
    else:
        # Process normally for smaller DataFrames
        n_dupes = df.duplicated().sum()
        if n_dupes > 0:
            percent = 100 * n_dupes / len(df)
            print(f"    {Fore.YELLOW}Fully duplicated rows{Style.RESET_ALL}: {n_dupes} ({percent:.2f}%)")
            
            # Show example duplicates
            try:
                dupes = df[df.duplicated()].head(3)
                print(f"      Example duplicated rows:")
                print(dupes.to_string())
            except Exception as e:
                print(f"      Could not display example duplicates: {e}")
            
            dupe_summary.append({
                'type': 'full_duplicates',
                'count': n_dupes,
                'percent': percent,
                'method': 'direct'
            })
        else:
            print(f"    {Fore.GREEN}No duplicates detected{Style.RESET_ALL}")

def gap_check(df, gap_summary, Fore, Style):
    """
    Performs gap check with aggressive memory optimization for large datasets.
    """
    print(f"  {Fore.MAGENTA}Data Quality Check: Gaps{Style.RESET_ALL}")
    
    # Get memory settings
    settings = _get_memory_settings()
    memory_mb = _estimate_memory_usage(df)
    max_memory_mb = settings['max_memory_mb']
    
    # For very large datasets, use aggressive sampling instead of skipping
    if memory_mb > max_memory_mb * 1.5:
        print(f"    📊 Very large dataset detected ({memory_mb}MB), using aggressive sampling for gap analysis...")
        
        try:
            # Use very small sample for extremely large datasets
            sample_size = min(5000, len(df) // 100)  # Sample 1% or 5k rows, whichever is smaller
            sample_df = df.sample(n=sample_size, random_state=42)
            
            # Find datetime column
            datetime_col = None
            for col in sample_df.columns:
                if any(keyword in col.lower() for keyword in ['date', 'time', 'datetime', 'timestamp']):
                    datetime_col = col
                    break
            
            if datetime_col and pd.api.types.is_datetime64_any_dtype(sample_df[datetime_col]):
                # Sort by datetime
                sample_df = sample_df.sort_values(datetime_col)
                
                # Calculate time differences
                time_diffs = sample_df[datetime_col].diff().dropna()
                
                if not time_diffs.empty:
                    # Find gaps (unusual time differences)
                    mean_diff = time_diffs.mean()
                    std_diff = time_diffs.std()
                    threshold = mean_diff + 2 * std_diff
                    
                    gaps = time_diffs[time_diffs > threshold]
                    if not gaps.empty:
                        print(f"    {Fore.YELLOW}Gaps detected in {datetime_col} (sampled data){Style.RESET_ALL}: {len(gaps)} gaps")
                        print(f"      Largest gap: {gaps.max()}")
                        print(f"      Note: Analysis based on {sample_size:,} sample rows")
                        
                        gap_summary.append({
                            'column': datetime_col,
                            'gaps_count': len(gaps),
                            'largest_gap': str(gaps.max()),
                            'method': 'aggressive_sampling',
                            'sample_size': sample_size
                        })
                    else:
                        print(f"    {Fore.GREEN}No significant gaps detected in sample{Style.RESET_ALL}")
                        print(f"      Note: Analysis based on {sample_size:,} sample rows")
                else:
                    print(f"    {Fore.YELLOW}Insufficient data for gap analysis{Style.RESET_ALL}")
            else:
                print(f"    {Fore.YELLOW}No suitable datetime column found for gap analysis{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"    ⚠️  Error in gap analysis: {e}")
            print(f"    Skipping gap check due to error")
            return
    
    # For large datasets, use sampling
    elif memory_mb > max_memory_mb * 0.5:
        print(f"    📊 Large dataset detected ({memory_mb}MB), using sampling for gap analysis...")
        
        try:
            # Use sampling for large datasets
            sample_size = min(settings['sample_size'], len(df) // 10)  # Sample 10% or sample_size rows
            sample_df = df.sample(n=sample_size, random_state=42)
            
            # Find datetime column
            datetime_col = None
            for col in sample_df.columns:
                if any(keyword in col.lower() for keyword in ['date', 'time', 'datetime', 'timestamp']):
                    datetime_col = col
                    break
            
            if datetime_col and pd.api.types.is_datetime64_any_dtype(sample_df[datetime_col]):
                # Sort by datetime
                sample_df = sample_df.sort_values(datetime_col)
                
                # Calculate time differences
                time_diffs = sample_df[datetime_col].diff().dropna()
                
                if not time_diffs.empty:
                    # Find gaps (unusual time differences)
                    mean_diff = time_diffs.mean()
                    std_diff = time_diffs.std()
                    threshold = mean_diff + 2 * std_diff
                    
                    gaps = time_diffs[time_diffs > threshold]
                    if not gaps.empty:
                        print(f"    {Fore.YELLOW}Gaps detected in {datetime_col}{Style.RESET_ALL}: {len(gaps)} gaps")
                        print(f"      Largest gap: {gaps.max()}")
                        
                        gap_summary.append({
                            'column': datetime_col,
                            'gaps_count': len(gaps),
                            'largest_gap': str(gaps.max()),
                            'method': 'sampling'
                        })
                    else:
                        print(f"    {Fore.GREEN}No significant gaps detected{Style.RESET_ALL}")
                else:
                    print(f"    {Fore.YELLOW}Insufficient data for gap analysis{Style.RESET_ALL}")
            else:
                print(f"    {Fore.YELLOW}No suitable datetime column found for gap analysis{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"    ⚠️  Error in gap analysis: {e}")
            print(f"    Skipping gap check for large dataset")
            return
    else:
        # Process normally for smaller DataFrames
        try:
            # Find datetime column
            datetime_col = None
            for col in df.columns:
                if any(keyword in col.lower() for keyword in ['date', 'time', 'datetime', 'timestamp']):
                    datetime_col = col
                    break
            
            if datetime_col and pd.api.types.is_datetime64_any_dtype(df[datetime_col]):
                # Sort by datetime
                df_sorted = df.sort_values(datetime_col)
                
                # Calculate time differences
                time_diffs = df_sorted[datetime_col].diff().dropna()
                
                if not time_diffs.empty:
                    # Find gaps (unusual time differences)
                    mean_diff = time_diffs.mean()
                    std_diff = time_diffs.std()
                    threshold = mean_diff + 2 * std_diff
                    
                    gaps = time_diffs[time_diffs > threshold]
                    if not gaps.empty:
                        print(f"    {Fore.YELLOW}Gaps detected in {datetime_col}{Style.RESET_ALL}: {len(gaps)} gaps")
                        print(f"      Largest gap: {gaps.max()}")
                        
                        gap_summary.append({
                            'column': datetime_col,
                            'gaps_count': len(gaps),
                            'largest_gap': str(gaps.max()),
                            'method': 'direct'
                        })
                    else:
                        print(f"    {Fore.GREEN}No significant gaps detected{Style.RESET_ALL}")
                else:
                    print(f"    {Fore.YELLOW}Insufficient data for gap analysis{Style.RESET_ALL}")
            else:
                print(f"    {Fore.YELLOW}No suitable datetime column found for gap analysis{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"    ⚠️  Error in gap analysis: {e}")

def zero_check(df, zero_summary, Fore, Style):
    """
    Performs zero value check with aggressive memory optimization for large datasets.
    """
    print(f"  {Fore.MAGENTA}Data Quality Check: Zero Values{Style.RESET_ALL}")
    
    # Get memory settings
    settings = _get_memory_settings()
    memory_mb = _estimate_memory_usage(df)
    max_memory_mb = settings['max_memory_mb']
    
    # For very large datasets, use sampling
    if memory_mb > max_memory_mb * 1.0:
        print(f"    📊 Large dataset detected ({memory_mb}MB), using optimized zero value detection...")
        
        try:
            # Use sampling for very large datasets
            sample_size = min(settings['sample_size'], len(df) // 20)  # Sample 5% or sample_size rows
            sample_df = df.sample(n=sample_size, random_state=42)
            
            for col in sample_df.columns:
                if pd.api.types.is_numeric_dtype(sample_df[col]):
                    n_zeros_sample = (sample_df[col] == 0).sum()
                    if n_zeros_sample > 0:
                        # Estimate total zero values
                        estimated_zeros = int((n_zeros_sample / sample_size) * len(df))
                        estimated_percent = 100 * estimated_zeros / len(df)
                        
                        print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: ~{estimated_zeros} zeros ({estimated_percent:.2f}%) [estimated from sample]")
                        
                        zero_summary.append({
                            'column': col,
                            'zeros': estimated_zeros,
                            'percent': estimated_percent,
                            'method': 'sampling'
                        })
                        
        except Exception as e:
            print(f"    ⚠️  Error in zero value check: {e}")
            return
    
    # For large datasets, use chunked processing
    elif memory_mb > max_memory_mb * 0.5:
        print(f"    📊 Large dataset detected ({memory_mb}MB), using chunked processing for zero values...")
        
        def process_zero_chunk(chunk):
            chunk_zero_summary = []
            for col in chunk.columns:
                if pd.api.types.is_numeric_dtype(chunk[col]):
                    n_zeros = (chunk[col] == 0).sum()
                    if n_zeros > 0:
                        percent = 100 * n_zeros / len(chunk)
                        chunk_zero_summary.append({
                            'column': col,
                            'zeros': n_zeros,
                            'percent': percent
                        })
            return chunk_zero_summary
        
        # Process in chunks
        chunk_size = min(settings['chunk_size'], 10000)
        chunk_results = _process_large_dataframe_in_chunks(df, process_zero_chunk, chunk_size=chunk_size)
        
        if chunk_results and isinstance(chunk_results, list):
            # Aggregate results from chunks
            column_zero_counts = {}
            for chunk_result in chunk_results:
                for item in chunk_result:
                    col = item['column']
                    if col in column_zero_counts:
                        column_zero_counts[col]['zeros'] += item['zeros']
                    else:
                        column_zero_counts[col] = item.copy()
            
            # Calculate percentages and display results
            for col, info in column_zero_counts.items():
                percent = 100 * info['zeros'] / len(df)
                print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {info['zeros']} zeros ({percent:.2f}%)")
                
                zero_summary.append({
                    'column': col,
                    'zeros': info['zeros'],
                    'percent': percent,
                    'method': 'chunked'
                })
    else:
        # Process normally for smaller DataFrames
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                n_zeros = (df[col] == 0).sum()
                if n_zeros > 0:
                    percent = 100 * n_zeros / len(df)
                    print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {n_zeros} zeros ({percent:.2f}%)")
                    
                    zero_summary.append({
                        'column': col,
                        'zeros': n_zeros,
                        'percent': percent,
                        'method': 'direct'
                    })

def negative_check(df, negative_summary, Fore, Style):
    """
    Performs negative value check with aggressive memory optimization for large datasets.
    """
    print(f"  {Fore.MAGENTA}Data Quality Check: Negative Values{Style.RESET_ALL}")
    
    # Get memory settings
    settings = _get_memory_settings()
    memory_mb = _estimate_memory_usage(df)
    max_memory_mb = settings['max_memory_mb']
    
    # For very large datasets, use sampling
    if memory_mb > max_memory_mb * 1.5:  # Increased from 1.0 to 1.5
        print(f"    📊 Large dataset detected ({memory_mb}MB), using sampling for negative value detection...")
        
        try:
            # Use sampling for very large datasets
            sample_size = min(settings['sample_size'], len(df) // 20)  # Sample 5% or sample_size rows
            sample_df = df.sample(n=sample_size, random_state=42)
            
            for col in sample_df.columns:
                if pd.api.types.is_numeric_dtype(sample_df[col]):
                    # Skip pressure_vector as it can legitimately be negative
                    if col.lower() == 'pressure_vector':
                        n_negatives_sample = (sample_df[col] < 0).sum()
                        if n_negatives_sample > 0:
                            estimated_negatives = int((n_negatives_sample / sample_size) * len(df))
                            estimated_percent = 100 * estimated_negatives / len(df)
                            print(f"    {Fore.CYAN}{col}{Style.RESET_ALL}: ~{estimated_negatives} negatives ({estimated_percent:.2f}%) [expected for pressure_vector]")
                        continue
                    
                    n_negatives_sample = (sample_df[col] < 0).sum()
                    if n_negatives_sample > 0:
                        # Estimate total negative values
                        estimated_negatives = int((n_negatives_sample / sample_size) * len(df))
                        estimated_percent = 100 * estimated_negatives / len(df)
                        
                        print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: ~{estimated_negatives} negatives ({estimated_percent:.2f}%) [estimated from sample]")
                        
                        negative_summary.append({
                            'column': col,
                            'negatives': estimated_negatives,
                            'percent': estimated_percent,
                            'method': 'sampling'
                        })
                        
        except Exception as e:
            print(f"    ⚠️  Error in negative value check: {e}")
            return
    
    # For large datasets, use chunked processing
    elif memory_mb > max_memory_mb * 0.5:
        print(f"    📊 Large dataset detected ({memory_mb}MB), using chunked processing for negative values...")
        
        def process_negative_chunk(chunk):
            chunk_negative_summary = []
            for col in chunk.columns:
                if pd.api.types.is_numeric_dtype(chunk[col]):
                    # Skip pressure_vector as it can legitimately be negative
                    if col.lower() == 'pressure_vector':
                        continue
                    
                    n_negatives = (chunk[col] < 0).sum()
                    if n_negatives > 0:
                        percent = 100 * n_negatives / len(chunk)
                        chunk_negative_summary.append({
                            'column': col,
                            'negatives': n_negatives,
                            'percent': percent
                        })
            return chunk_negative_summary
        
        # Process in chunks
        chunk_size = min(settings['chunk_size'], 10000)
        chunk_results = _process_large_dataframe_in_chunks(df, process_negative_chunk, chunk_size=chunk_size)
        
        if chunk_results and isinstance(chunk_results, list):
            # Aggregate results from chunks
            column_negative_counts = {}
            for chunk_result in chunk_results:
                for item in chunk_result:
                    col = item['column']
                    if col in column_negative_counts:
                        column_negative_counts[col]['negatives'] += item['negatives']
                    else:
                        column_negative_counts[col] = item.copy()
            
            # Calculate percentages and display results
            for col, info in column_negative_counts.items():
                percent = 100 * info['negatives'] / len(df)
                print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {info['negatives']} negatives ({percent:.2f}%)")
                
                negative_summary.append({
                    'column': col,
                    'negatives': info['negatives'],
                    'percent': percent,
                    'method': 'chunked'
                })
    else:
        # Process normally for smaller DataFrames
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                # Skip pressure_vector as it can legitimately be negative
                if col.lower() == 'pressure_vector':
                    n_negatives = (df[col] < 0).sum()
                    if n_negatives > 0:
                        percent = 100 * n_negatives / len(df)
                        print(f"    {Fore.CYAN}{col}{Style.RESET_ALL}: {n_negatives} negatives ({percent:.2f}%) [expected for pressure_vector]")
                    continue
                
                n_negatives = (df[col] < 0).sum()
                if n_negatives > 0:
                    percent = 100 * n_negatives / len(df)
                    print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {n_negatives} negatives ({percent:.2f}%)")
                    
                    negative_summary.append({
                        'column': col,
                        'negatives': n_negatives,
                        'percent': percent,
                        'method': 'direct'
                    })

def inf_check(df, inf_summary, Fore, Style):
    """
    Performs infinite value check with aggressive memory optimization for large datasets.
    """
    print(f"  {Fore.MAGENTA}Data Quality Check: Infinite Values{Style.RESET_ALL}")
    
    # Get memory settings
    settings = _get_memory_settings()
    memory_mb = _estimate_memory_usage(df)
    max_memory_mb = settings['max_memory_mb']
    
    # For very large datasets, use sampling
    if memory_mb > max_memory_mb * 1.0:
        print(f"    📊 Large dataset detected ({memory_mb}MB), using sampling for infinite value detection...")
        
        try:
            # Use sampling for very large datasets
            sample_size = min(settings['sample_size'], len(df) // 20)  # Sample 5% or sample_size rows
            sample_df = df.sample(n=sample_size, random_state=42)
            
            for col in sample_df.columns:
                if pd.api.types.is_numeric_dtype(sample_df[col]):
                    n_infs_sample = np.isinf(sample_df[col]).sum()
                    if n_infs_sample > 0:
                        # Estimate total infinite values
                        estimated_infs = int((n_infs_sample / sample_size) * len(df))
                        estimated_percent = 100 * estimated_infs / len(df)
                        
                        print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: ~{estimated_infs} infinite values ({estimated_percent:.2f}%) [estimated from sample]")
                        
                        inf_summary.append({
                            'column': col,
                            'infs': estimated_infs,
                            'percent': estimated_percent,
                            'method': 'sampling'
                        })
                        
        except Exception as e:
            print(f"    ⚠️  Error in infinite value check: {e}")
            return
    
    # For large datasets, use chunked processing
    elif memory_mb > max_memory_mb * 0.5:
        print(f"    📊 Large dataset detected ({memory_mb}MB), using chunked processing for infinite values...")
        
        def process_inf_chunk(chunk):
            chunk_inf_summary = []
            for col in chunk.columns:
                if pd.api.types.is_numeric_dtype(chunk[col]):
                    n_infs = np.isinf(chunk[col]).sum()
                    if n_infs > 0:
                        percent = 100 * n_infs / len(chunk)
                        chunk_inf_summary.append({
                            'column': col,
                            'infs': n_infs,
                            'percent': percent
                        })
            return chunk_inf_summary
        
        # Process in chunks
        chunk_size = min(settings['chunk_size'], 10000)
        chunk_results = _process_large_dataframe_in_chunks(df, process_inf_chunk, chunk_size=chunk_size)
        
        if chunk_results and isinstance(chunk_results, list):
            # Aggregate results from chunks
            column_inf_counts = {}
            for chunk_result in chunk_results:
                for item in chunk_result:
                    col = item['column']
                    if col in column_inf_counts:
                        column_inf_counts[col]['infs'] += item['infs']
                    else:
                        column_inf_counts[col] = item.copy()
            
            # Calculate percentages and display results
            for col, info in column_inf_counts.items():
                percent = 100 * info['infs'] / len(df)
                print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {info['infs']} infinite values ({percent:.2f}%)")
                
                inf_summary.append({
                    'column': col,
                    'infs': info['infs'],
                    'percent': percent,
                    'method': 'chunked'
                })
    else:
        # Process normally for smaller DataFrames
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                n_infs = np.isinf(df[col]).sum()
                if n_infs > 0:
                    percent = 100 * n_infs / len(df)
                    print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {n_infs} infinite values ({percent:.2f}%)")
                    
                    inf_summary.append({
                        'column': col,
                        'infs': n_infs,
                        'percent': percent,
                        'method': 'direct'
                    })

def data_quality_checks(df, nan_summary, dupe_summary, gap_summary, Fore, Style, schema_datetime_fields=None, file_name=None, zero_summary=None, negative_summary=None, inf_summary=None):
    nan_check(df, nan_summary, Fore, Style)
    duplicate_check(df, dupe_summary, Fore, Style)
    gap_check(df, gap_summary, Fore, Style, schema_datetime_fields=schema_datetime_fields, file_name=file_name)
    if zero_summary is not None:
        zero_check(df, zero_summary, Fore, Style, file_name=file_name)
    if negative_summary is not None:
        negative_check(df, negative_summary, Fore, Style, file_name=file_name)
    if inf_summary is not None:
        inf_check(df, inf_summary, Fore, Style, file_name=file_name)

def print_nan_summary(nan_summary, Fore, Style):
    """
    Prints summary of NaN for all files after processing.
    """
    if nan_summary:
        print(f"\n{Fore.MAGENTA}NaN Summary for all files:{Style.RESET_ALL}")
        for entry in nan_summary:
            print(f"  {Fore.YELLOW}{entry['column']}{Style.RESET_ALL}: {entry['missing']} missing ({entry['percent']:.2f}%)")
    else:
        print(f"\n{Fore.MAGENTA}NaN Summary for all files: No missing values found.{Style.RESET_ALL}")

def print_duplicate_summary(dupe_summary, Fore, Style):
    """
    Prints summary of duplicates for all files after processing.
    """
    if dupe_summary:
        print(f"\n{Fore.MAGENTA}Duplicate Summary for all files:{Style.RESET_ALL}")
        for entry in dupe_summary:
            if entry['type'] == 'full_duplicates':
                print(f"  {Fore.YELLOW}Fully duplicated rows:{Style.RESET_ALL} {entry['count']} ({entry['percent']:.2f}%)")
    else:
        print(f"\n{Fore.MAGENTA}Duplicate Summary for all files: No duplicates found.{Style.RESET_ALL}")

def print_gap_summary(gap_summary, Fore, Style):
    """
    Prints summary of gaps for all files after processing, grouped by file.
    Shows all gaps for each file and total count in header.
    """
    if gap_summary:
        from collections import defaultdict
        gaps_by_file = defaultdict(list)
        for entry in gap_summary:
            gaps_by_file[entry.get('file', 'Unknown file')].append(entry)
        print(f"\n{Fore.MAGENTA}Gap Summary for all files (grouped by file):{Style.RESET_ALL}")
        for file, gaps in gaps_by_file.items():
            print(f"  {Fore.CYAN}File: {file} | Total gaps: {len(gaps)}{Style.RESET_ALL}")
            for entry in gaps:
                print(f"    {Fore.YELLOW}Gap in '{entry['column']}':{Style.RESET_ALL} from {entry['from']} to {entry['to']} (delta: {entry['delta']})")
    else:
        print(f"\n{Fore.MAGENTA}Gap Summary for all files: No significant gaps found.{Style.RESET_ALL}")

def print_zero_summary(zero_summary, Fore, Style):
    """
    Prints summary of zero values for all files after processing, grouped by file and row index.
    Only shows columns where zeros are anomaly or require check, in a grouped and readable format per file.
    For each row prints row number, index, column and value (one per line, pretty format).
    """
    if zero_summary:
        from collections import defaultdict
        zeros_by_file = defaultdict(list)
        for entry in zero_summary:
            zeros_by_file[entry.get('file', 'Unknown file')].append(entry)
        print(f"\n{Fore.MAGENTA}Zero Value Summary for all files (grouped by file, grouped by row index):{Style.RESET_ALL}")
        for file, zeros in zeros_by_file.items():
            filtered = [z for z in zeros if z['anomaly'] is not False]
            if not filtered:
                continue
            row_col_val = []
            for entry in filtered:
                col = entry['column']
                df = entry.get('df')
                if df is not None:
                    zero_rows = df[df[col] == 0]
                    for i, idx in enumerate(zero_rows.index[:20]):
                        rownum = zero_rows.index.get_loc(idx)
                        val = zero_rows.loc[idx, col]
                        row_col_val.append((rownum, idx, col, val))
            if not row_col_val:
                continue
            print(f"\n  {Fore.CYAN}File: {file}{Style.RESET_ALL}")
            print(f"    {'Row':<8} {'Index':<12} {'Column':<30} {'Value':<15}")
            print(f"    {'-'*70}")
            for rownum, idx, col, val in sorted(row_col_val, key=lambda x: (x[0], x[2])):
                print(f"    {str(rownum):<8} {str(idx):<12} {col:<30} {str(val):<15}")
    else:
        print(f"\n{Fore.MAGENTA}Zero Value Summary for all files: No zeros found.{Style.RESET_ALL}")

def print_negative_summary(negative_summary, Fore, Style):
    """
    Prints summary of negative values for all files after processing, grouped by file and row index.
    Only shows rows with negative values, one per value (pretty format).
    """
    if negative_summary:
        from collections import defaultdict
        neg_by_file = defaultdict(list)
        for entry in negative_summary:
            neg_by_file[entry.get('file', 'Unknown file')].append(entry)
        print(f"\n{Fore.MAGENTA}Negative Value Summary for all files (grouped by file, grouped by row index):{Style.RESET_ALL}")
        for file, negs in neg_by_file.items():
            row_col_val = []
            for entry in negs:
                col = entry['column']
                df = entry.get('df')
                if df is not None:
                    neg_rows = df[df[col] < 0]
                    for i, idx in enumerate(neg_rows.index[:20]):
                        rownum = neg_rows.index.get_loc(idx)
                        val = neg_rows.loc[idx, col]
                        row_col_val.append((rownum, idx, col, val))
            if not row_col_val:
                continue
            print(f"\n  {Fore.CYAN}File: {file}{Style.RESET_ALL}")
            print(f"    {'Row':<8} {'Index':<12} {'Column':<30} {'Value':<15}")
            print(f"    {'-'*70}")
            for rownum, idx, col, val in sorted(row_col_val, key=lambda x: (x[0], x[2])):
                print(f"    {str(rownum):<8} {str(idx):<12} {col:<30} {str(val):<15}")
    else:
        print(f"\n{Fore.MAGENTA}Negative Value Summary for all files: No negatives found.{Style.RESET_ALL}")

def print_inf_summary(inf_summary, Fore, Style):
    """
    Prints summary of inf values for all files after processing, grouped by file and row index.
    Only shows rows with inf, one per value (pretty format).
    """
    if inf_summary:
        from collections import defaultdict
        infs_by_file = defaultdict(list)
        for entry in inf_summary:
            infs_by_file[entry.get('file', 'Unknown file')].append(entry)
        print(f"\n{Fore.MAGENTA}Inf Value Summary for all files (grouped by file, grouped by row index):{Style.RESET_ALL}")
        for file, infs in infs_by_file.items():
            row_col_val = []
            for entry in infs:
                col = entry['column']
                df = entry.get('df')
                if df is not None:
                    inf_rows = df[(df[col] == float('inf')) | (df[col] == float('-inf'))]
                    for i, idx in enumerate(inf_rows.index[:20]):
                        rownum = inf_rows.index.get_loc(idx)
                        val = inf_rows.loc[idx, col]
                        row_col_val.append((rownum, idx, col, val))
            if not row_col_val:
                continue
            print(f"\n  {Fore.CYAN}File: {file}{Style.RESET_ALL}")
            print(f"    {'Row':<8} {'Index':<12} {'Column':<30} {'Value':<15}")
            print(f"    {'-'*70}")
            for rownum, idx, col, val in sorted(row_col_val, key=lambda x: (x[0], x[2])):
                print(f"    {str(rownum):<8} {str(idx):<12} {col:<30} {str(val):<15}")
    else:
        print(f"\n{Fore.MAGENTA}Inf Value Summary for all files: No infs found.{Style.RESET_ALL}")
