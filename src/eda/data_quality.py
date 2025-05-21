# Handles data quality checks

def nan_check(df, nan_summary, Fore, Style):
    """
    Performs NaN check: for each column, print count and percent of NaNs, and show example rows with NaN.
    Also, collect summary info in nan_summary list.
    """
    print(f"  {Fore.MAGENTA}Data Quality Check: Missing values (NaN){Style.RESET_ALL}")
    for col in df.columns:
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            percent = 100 * n_missing / len(df)
            print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {n_missing} missing ({percent:.2f}%)")
            nan_rows = df[df[col].isna()]
            print(f"      Example rows with NaN in {col}:")
            print(nan_rows.head(3).to_string())
            nan_summary.append({
                'column': col,
                'missing': n_missing,
                'percent': percent
            })

def duplicate_check(df, dupe_summary, Fore, Style):
    """
    Performs duplicate check: print count and examples of fully duplicated rows, and check string columns for duplicated values.
    Also, collect summary info in dupe_summary list.
    """
    n_dupes = df.duplicated().sum()
    if n_dupes > 0:
        print(f"  {Fore.MAGENTA}Data Quality Check: Duplicates{Style.RESET_ALL}")
        print(f"    {Fore.YELLOW}Total fully duplicated rows:{Style.RESET_ALL} {n_dupes}")
        print(f"    {Fore.YELLOW}Example duplicated rows:{Style.RESET_ALL}")
        print(df[df.duplicated()].head(3).to_string())
        dupe_summary.append({'type': 'full_row', 'count': n_dupes})
    else:
        print(f"  {Fore.MAGENTA}No fully duplicated rows found.{Style.RESET_ALL}")
    string_cols = [col for col in df.columns if df[col].dtype == 'object' or str(df[col].dtype).startswith('string')]
    for col in string_cols:
        dupe_vals = df[col][df[col].duplicated(keep=False)]
        if not dupe_vals.empty:
            n_col_dupes = dupe_vals.duplicated().sum()
            print(f"    {Fore.YELLOW}Column '{col}' has {n_col_dupes} duplicated values.{Style.RESET_ALL}")
            print(f"      Example duplicated values in '{col}': {dupe_vals.unique()[:5]}")
            dupe_summary.append({'type': 'column', 'column': col, 'count': n_col_dupes, 'examples': dupe_vals.unique()[:5]})

def gap_check(df, gap_summary, Fore, Style, datetime_col=None, freq=None, schema_datetime_fields=None, file_name=None):
    """
    Checks for gaps in a datetime column: finds abnormally large time intervals between consecutive records.
    If datetime_col is None, tries to auto-detect the first datetime column by dtype, name, or schema info.
    freq can be set to expected frequency (e.g. '1H', '1D') for more precise gap detection.
    Adds info to gap_summary.
    """
    import pandas as pd
    dt_col = None
    # 1. Try explicit argument
    if datetime_col and datetime_col in df.columns:
        dt_col = datetime_col
    # 2. Try dtype
    if not dt_col:
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                dt_col = col
                break
    # 3. Try name
    if not dt_col:
        for col in df.columns:
            if any(name in col.lower() for name in ["date", "time", "datetime", "timestamp"]):
                try:
                    if not pd.api.types.is_datetime64_any_dtype(df[col]):
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        dt_col = col
                        break
                except Exception:
                    continue
    # 4. Try schema info (case-insensitive match, partial match, try convert from int/float)
    if not dt_col and schema_datetime_fields:
        found_in_schema = False
        for schema_col in schema_datetime_fields:
            schema_col_norm = schema_col.lower().replace('_', '')
            for col in df.columns:
                col_norm = col.lower().replace('_', '')
                if col_norm == schema_col_norm:
                    found_in_schema = True
                    try:
                        if not pd.api.types.is_datetime64_any_dtype(df[col]):
                            if pd.api.types.is_integer_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
                                try:
                                    df[col] = pd.to_datetime(df[col], unit='s', errors='coerce')
                                except Exception:
                                    df[col] = pd.to_datetime(df[col], unit='ms', errors='coerce')
                            else:
                                df[col] = pd.to_datetime(df[col], errors='coerce')
                        if pd.api.types.is_datetime64_any_dtype(df[col]):
                            dt_col = col
                            break
                    except Exception:
                        continue
            if dt_col:
                break
        # Partial match if exact not found
        if not dt_col:
            for schema_col in schema_datetime_fields:
                schema_col_norm = schema_col.lower().replace('_', '')
                for col in df.columns:
                    col_norm = col.lower().replace('_', '')
                    if schema_col_norm in col_norm or col_norm in schema_col_norm:
                        print(f"  {Fore.YELLOW}Gap Check: Using partial match for datetime column: '{col}' ~ '{schema_col}'{Style.RESET_ALL}")
                        try:
                            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                                df[col] = pd.to_datetime(df[col], errors='coerce')
                            if pd.api.types.is_datetime64_any_dtype(df[col]):
                                dt_col = col
                                break
                        except Exception:
                            continue
                if dt_col:
                    break
        if not found_in_schema:
            print(f"  {Fore.YELLOW}Gap Check: Columns from schema {schema_datetime_fields} not found in DataFrame columns {list(df.columns)}{Style.RESET_ALL}")
    # 5. Try index if still not found
    if not dt_col:
        if pd.api.types.is_datetime64_any_dtype(df.index):
            dt_col = None  # special marker: use index
            print(f"  {Fore.YELLOW}Gap Check: Using DataFrame index as datetime column.{Style.RESET_ALL}")
        else:
            print(f"  {Fore.MAGENTA}Gap Check: No datetime-like column or index found (by dtype, name, or schema, tried columns: {list(df.columns)}, schema: {schema_datetime_fields}){Style.RESET_ALL}")
            return
    # Ensure sorted by datetime
    if dt_col is not None:
        df_sorted = df.sort_values(dt_col)
        datetimes = df_sorted[dt_col]
        use_iloc = True
    else:
        df_sorted = df.sort_index()
        datetimes = df_sorted.index
        use_iloc = False
    time_deltas = datetimes.to_series().diff().dropna()
    if freq is not None:
        expected = pd.to_timedelta(freq)
        gaps = time_deltas[time_deltas > expected]
    else:
        expected = time_deltas.median()
        gaps = time_deltas[time_deltas > expected * 2]
    if not gaps.empty:
        print(f"  {Fore.MAGENTA}Gap Check: Found {len(gaps)} gaps in '{dt_col if dt_col else 'index'}' (interval > {expected * 2}){Style.RESET_ALL}")
        for i, (idx, delta) in enumerate(gaps.items()):
            # idx is the index in datetimes where the gap is detected
            if use_iloc:
                curr_pos = datetimes.index.get_loc(idx)
                prev_time = datetimes.iloc[curr_pos - 1]
                curr_time = datetimes.iloc[curr_pos]
            else:
                curr_pos = datetimes.get_loc(idx)
                prev_time = datetimes[curr_pos - 1]
                curr_time = datetimes[curr_pos]
            if i < 5:
                print(f"    Gap from {prev_time} to {curr_time}: {delta}")
            gap_summary.append({'file': file_name, 'column': dt_col if dt_col else 'index', 'from': prev_time, 'to': curr_time, 'delta': delta})
    else:
        print(f"  {Fore.MAGENTA}Gap Check: No significant gaps found in '{dt_col if dt_col else 'index'}'.{Style.RESET_ALL}")

def zero_check(df, zero_summary, Fore, Style, file_name=None):
    """
    Checks for zero values in numeric columns. Prints columns with zeros and their counts.
    Marks columns where zeros are likely normal (e.g., volume) or likely anomalous (e.g., price).
    Adds info to zero_summary.
    """
    import numpy as np
    print(f"  {Fore.MAGENTA}Data Quality Check: Zero values (0){Style.RESET_ALL}")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        n_zeros = (df[col] == 0).sum()
        if n_zeros > 0:
            # Heuristic: columns with 'volume' or 'qty' in name are likely to allow zeros
            col_lower = col.lower()
            if any(key in col_lower for key in ['volume', 'qty', 'amount']):
                note = f"{Fore.GREEN}OK (likely normal){Style.RESET_ALL}"
                anomaly = False
            elif any(key in col_lower for key in ['price', 'close', 'open', 'high', 'low']):
                note = f"{Fore.RED}ANOMALY? (check!){Style.RESET_ALL}"
                anomaly = True
            else:
                note = f"{Fore.YELLOW}Check meaning{Style.RESET_ALL}"
                anomaly = None
            print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {n_zeros} zeros. {note}")
            zero_summary.append({'column': col, 'zeros': n_zeros, 'anomaly': anomaly, 'df': df, 'file': file_name})

def negative_check(df, negative_summary, Fore, Style, file_name=None):
    """
    Checks for negative values in OHLCV and datetime columns. Prints columns with negatives and their counts.
    Shows example rows with negative values (index and row number).
    Adds info to negative_summary.
    """
    import numpy as np
    import pandas as pd
    print(f"  {Fore.MAGENTA}Data Quality Check: Negative values{Style.RESET_ALL}")
    # Define relevant columns by name
    ohlcv_keys = ['open', 'high', 'low', 'close', 'volume', 'amount', 'qty']
    # Numeric columns with OHLCV-like names
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    check_cols = [col for col in numeric_cols if any(key in col.lower() for key in ohlcv_keys)]
    # Add datetime columns (as int/float)
    datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    for col in check_cols:
        n_neg = (df[col] < 0).sum()
        if n_neg > 0:
            print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {n_neg} negative values. {Fore.RED}ANOMALY!{Style.RESET_ALL}")
            negative_summary.append({'column': col, 'negatives': n_neg, 'df': df, 'file': file_name})
    for col in datetime_cols:
        # Check if any datetime values are negative (as timestamp)
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # Convert to int64 (nanoseconds since epoch)
            negatives = df[col].dropna().astype('int64') < 0
            n_neg = negatives.sum()
            if n_neg > 0:
                print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: {n_neg} negative datetime values. {Fore.RED}ANOMALY!{Style.RESET_ALL}")
                negative_summary.append({'column': col, 'negatives': n_neg, 'df': df, 'file': file_name, 'is_datetime': True})

def inf_check(df, inf_summary, Fore, Style, file_name=None):
    """
    Checks for -inf and +inf values in numeric columns. Prints columns with infs and their counts.
    Adds info to inf_summary.
    """
    import numpy as np
    print(f"  {Fore.MAGENTA}Data Quality Check: Inf values (+inf, -inf){Style.RESET_ALL}")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        n_posinf = (df[col] == np.inf).sum()
        n_neginf = (df[col] == -np.inf).sum()
        if n_posinf > 0 or n_neginf > 0:
            print(f"    {Fore.YELLOW}{col}{Style.RESET_ALL}: +inf: {n_posinf}, -inf: {n_neginf}")
            inf_summary.append({'column': col, 'posinf': n_posinf, 'neginf': n_neginf, 'df': df, 'file': file_name})

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
            if entry['type'] == 'full_row':
                print(f"  {Fore.YELLOW}Fully duplicated rows:{Style.RESET_ALL} {entry['count']}")
            elif entry['type'] == 'column':
                print(f"  {Fore.YELLOW}Column '{entry['column']}' duplicated values:{Style.RESET_ALL} {entry['count']}, examples: {entry['examples']}")
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
