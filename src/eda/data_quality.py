# Handles data quality checks

def data_quality_checks(df, nan_summary, Fore, Style):
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
