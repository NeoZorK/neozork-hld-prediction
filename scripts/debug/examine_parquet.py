#!/usr/bin/env python3

import pandas as pd
import sys
import os
import argparse
import glob
from pathlib import Path

def find_parquet_files(project_root):
    """
    Find all parquet files in the project directory.

    Args:
        project_root (Path): Root directory of the project

    Returns:
        list: List of parquet file paths
    """
    parquet_files = []

    # Look for .parquet files
    for path in project_root.glob('**/*.parquet'):
        parquet_files.append(str(path))

    # Also check for .parquet. files (with dot at the end)
    for path in project_root.glob('**/*.parquet.*'):
        parquet_files.append(str(path))

    # Filter out files from test/venv directories to keep the list cleaner
    filtered_files = [f for f in parquet_files if 'site-packages' not in f]

    return sorted(filtered_files)

def examine_parquet(file_path, show_rows=3, verbose=False):
    """
    Examines a parquet file and prints its structure and content information.

    Args:
        file_path (str): Path to the parquet file (can be absolute or relative)
        show_rows (int): Number of rows to display in the preview
        verbose (bool): Whether to show detailed information about columns

    Returns:
        tuple: (standard_fields_list, non_standard_fields_list) if successful, (None, None) otherwise
    """
    try:
        # Convert to absolute path if relative
        abs_path = os.path.abspath(file_path)

        # Handle the case with trailing dot in filename (e.g., .parquet.)
        if abs_path.endswith('.parquet.'):
            # Try the path as is first
            if not os.path.exists(abs_path):
                # If not found, try without the trailing dot
                alternative_path = abs_path[:-1]
                if os.path.exists(alternative_path):
                    abs_path = alternative_path
                    print(f"Using alternative path: {abs_path}")

        # Check if file exists
        if not os.path.exists(abs_path):
            print(f"Error: File not found at {abs_path}")

            # Try to suggest alternative paths if file exists elsewhere
            filename = os.path.basename(file_path)
            project_root = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent

            potential_paths = []
            for root, dirs, files in os.walk(project_root):
                for file in files:
                    if filename in file:
                        potential_paths.append(os.path.join(root, file))

            # Try Docker container paths if we're likely in a container
            if '/app/' in os.getcwd():
                docker_paths = []
                # Common data directories in our container
                for data_dir in ['/app/data', '/app/data/raw_parquet', '/app/data/cache/csv_converted']:
                    if os.path.exists(data_dir):
                        test_path = os.path.join(data_dir, filename)
                        if os.path.exists(test_path):
                            docker_paths.append(test_path)

                if docker_paths:
                    print("\nFound files in Docker container paths:")
                    for path in docker_paths:
                        print(f"  - {path}")

                    # If only one match, use it automatically
                    if len(docker_paths) == 1:
                        print(f"Automatically using the found file: {docker_paths[0]}")
                        return examine_parquet(docker_paths[0], show_rows, verbose)

            if potential_paths:
                print("\nSimilar files found at:")
                for path in potential_paths[:5]:  # Show first 5 alternatives
                    print(f"  - {path}")
                print(f"Try using one of these paths instead.")

            return None, None

        # Print reading message at the beginning of actual processing
        print(f"Reading parquet file: {abs_path}")

        # Read the parquet file
        try:
            df = pd.read_parquet(abs_path)
        except Exception as e:
            print(f"Error reading parquet file format: {str(e)}")
            print("Trying with alternative engine (pyarrow)...")
            try:
                df = pd.read_parquet(abs_path, engine='pyarrow')
            except Exception as e2:
                print(f"Still failed with pyarrow: {str(e2)}")
                print("Trying with fastparquet engine...")
                try:
                    df = pd.read_parquet(abs_path, engine='fastparquet')
                except Exception as e3:
                    print(f"All engines failed. Last error: {str(e3)}")
                    return None, None

        print("\n=== PARQUET FILE STRUCTURE ===")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        print("\n=== COLUMN TYPES ===")
        for col, dtype in df.dtypes.items():
            print(f"  {col}: {dtype}")
        
        print(f"\n=== FIRST {show_rows} ROWS ===")
        print(df.head(show_rows))

        # Identify standard vs non-standard fields
        standard_fields = {'open', 'high', 'low', 'close', 'volume', 'timeseries', 'datetime', 'date', 'time'}
        standard_found = []
        non_standard_found = []
        
        for col in df.columns:
            if col.lower() in standard_fields:
                standard_found.append(col)
            else:
                non_standard_found.append(col)
        
        print("\n=== FIELD CLASSIFICATION ===")
        print(f"Standard fields: {standard_found}")
        print(f"Non-standard fields: {non_standard_found}")
        
        if non_standard_found and verbose:
            print("\n=== NON-STANDARD FIELD SAMPLE DATA ===")
            for field in non_standard_found[:5]:  # Show first 5 non-standard fields
                print(f"\n{field}:")
                sample_data = df[field].dropna().head(3)
                print(f"  Sample values: {list(sample_data)}")
                print(f"  Data type: {df[field].dtype}")
                print(f"  Non-null count: {df[field].count()}/{len(df)}")

            # Additional statistics in verbose mode
            print("\n=== NUMERICAL COLUMNS STATISTICS ===")
            numeric_cols = df.select_dtypes(include=['number']).columns
            if not numeric_cols.empty:
                print(df[numeric_cols].describe())
            else:
                print("No numerical columns found.")

        return standard_found, non_standard_found

    except Exception as e:
        print(f"Error reading parquet file: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

def main():
    """Main function to parse arguments and execute the script."""
    parser = argparse.ArgumentParser(description='Examine Parquet file structure and content')
    parser.add_argument('file_path', nargs='?', help='Path to the parquet file')
    parser.add_argument('-l', '--list', action='store_true', help='List all parquet files in the project')
    parser.add_argument('-r', '--rows', type=int, default=3, help='Number of rows to display (default: 3)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed information')
    parser.add_argument('-n', '--number', type=int, help='Select file by number from the list')
    args = parser.parse_args()

    # Get project root - handle both local and Docker environments
    if '/app/' in os.getcwd():
        # Docker environment
        project_root = Path('/app')
    else:
        # Local environment
        project_root = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent

    # Find all parquet files
    parquet_files = find_parquet_files(project_root)

    if args.list:
        print("Available parquet files in the project:")
        for i, file_path in enumerate(parquet_files, 1):
            print(f"{i}. {file_path}")
        return

    # Direct selection by number argument
    if args.number is not None:
        if 1 <= args.number <= len(parquet_files):
            selected_file = parquet_files[args.number - 1]
            print(f"Selected file #{args.number}: {selected_file}")
            examine_parquet(selected_file, args.rows, args.verbose)
            return
        else:
            print(f"Invalid file number. Please choose between 1 and {len(parquet_files)}")
            return

    if not args.file_path:
        # If no file path provided, automatically select the first available file
        if not parquet_files:
            print("No parquet files found in the project.")
            return

        # Automatically select the first file for non-interactive execution
        selected_file = parquet_files[0]
        print(f"Automatically selected: {selected_file}")
        examine_parquet(selected_file, args.rows, args.verbose)
        return
    else:
        examine_parquet(args.file_path, args.rows, args.verbose)

if __name__ == "__main__":
    main()
