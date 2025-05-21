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

def data_quality_checks(df, nan_summary, dupe_summary, Fore, Style):
    nan_check(df, nan_summary, Fore, Style)
    duplicate_check(df, dupe_summary, Fore, Style)

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

