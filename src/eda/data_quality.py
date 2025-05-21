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

def gap_check(df, gap_summary, Fore, Style, datetime_col=None, freq=None, schema_datetime_fields=None):
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
        for i, (idx, delta) in enumerate(gaps.head(5).items()):
            if use_iloc:
                prev_time = datetimes.iloc[i]
                curr_time = datetimes.iloc[i + 1]
            else:
                prev_time = datetimes[i]
                curr_time = datetimes[i + 1]
            print(f"    Gap from {prev_time} to {curr_time}: {delta}")
            gap_summary.append({'column': dt_col if dt_col else 'index', 'from': prev_time, 'to': curr_time, 'delta': delta})
    else:
        print(f"  {Fore.MAGENTA}Gap Check: No significant gaps found in '{dt_col if dt_col else 'index'}'.{Style.RESET_ALL}")

def data_quality_checks(df, nan_summary, dupe_summary, gap_summary, Fore, Style, schema_datetime_fields=None):
    nan_check(df, nan_summary, Fore, Style)
    duplicate_check(df, dupe_summary, Fore, Style)
    gap_check(df, gap_summary, Fore, Style, schema_datetime_fields=schema_datetime_fields)

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
    Prints summary of gaps for all files after processing.
    """
    if gap_summary:
        print(f"\n{Fore.MAGENTA}Gap Summary for all files:{Style.RESET_ALL}")
        for entry in gap_summary:
            print(f"  {Fore.YELLOW}Gap in '{entry['column']}':{Style.RESET_ALL} from {entry['from']} to {entry['to']} (delta: {entry['delta']})")
    else:
        print(f"\n{Fore.MAGENTA}Gap Summary for all files: No significant gaps found.{Style.RESET_ALL}")
