# -*- coding: utf-8 -*-
# eda_batch_check.py

import os
import warnings
import subprocess
import argparse
from typing import List, Dict, Union
from tqdm import tqdm
import glob
import shutil
import logging
from pathlib import Path
import sys
import time  # Для отслеживания времени выполнения команд

from src.eda.data_overview import (
    load_data,
    show_basic_info,
    show_head,
    check_missing_values,
    check_duplicates,
    get_column_types,
    get_nan_columns,
    get_summary
)

def setup_logger(log_file: str = None) -> logging.Logger:
    """
    Set up a logger to write info and errors to a file in 'logs' directory.
    No console output to keep terminal clean for progress bar.
    
    Args:
        log_file: Path to the log file (default: "logs/eda_batch_check.log")
    
    Returns:
        Logger instance with file handler only
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True, parents=True)
    
    # Set default log file path if not provided
    if log_file is None:
        log_file = logs_dir / "eda_batch_check.log"
    else:
        # Ensure the log file is in the logs directory
        log_path = Path(log_file)
        if not log_path.is_absolute():
            if not str(log_path).startswith("logs/"):
                log_file = logs_dir / log_path.name
    
    logger = logging.getLogger("eda_batch_check")
    
    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()  # Properly close the handler
    
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # Add file handler only
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # Console handler removed - to keep progress bar visible alone

    logger.propagate = False
    return logger

def sort_files_by_type(base_dir: str, parquet_dir: str, csv_dir: str) -> None:
    """
    Sort files in the base directory into parquet and csv directories.
    """
    # Create directories if they don't exist
    os.makedirs(parquet_dir, exist_ok=True)
    os.makedirs(csv_dir, exist_ok=True)
    
    # Search for all files in the base directory
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        
        # Process only files, not directories
        if os.path.isfile(file_path):
            # Determine the file type and move it to the appropriate directory
            if file.lower().endswith('.parquet'):
                target_path = os.path.join(parquet_dir, file)
                shutil.move(file_path, target_path)
                print(f"  Moved paquet file: {file} -> {target_path}")
            elif file.lower().endswith('.csv'):
                target_path = os.path.join(csv_dir, file)
                shutil.move(file_path, target_path)
                print(f"  Move CSV File: {file} -> {target_path}")

def find_data_files(folder_path: Union[str, List[str]], extensions: List[str] = [".parquet", ".csv"], exclude_paths: List[str] = None) -> List[str]:
    """
    Find all data files in the specified folder(s) with given extensions.
    """
    data_files = []
    
    # Transform folder_path to a list if it's a string
    if isinstance(folder_path, str):
        folder_path = [folder_path]
    
    # Transform exclude_paths to absolute paths if provided
    exclude_abs_paths = []
    if exclude_paths:
        exclude_abs_paths = [os.path.abspath(p) for p in exclude_paths]
    
    for folder in folder_path:
        if not os.path.exists(folder):
            continue
            
        for root, dirs, files in os.walk(folder):
            # Check if the current directory is in the exclude paths
            current_abs_path = os.path.abspath(root)
            
            if exclude_abs_paths and any(current_abs_path.startswith(p) for p in exclude_abs_paths):
                continue
                
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    data_files.append(file_path)
    
    return data_files

def log_file_info(df, file_path, logger):
    """
    Log detailed information about the dataframe to the logger.
    """
    logger.info(f"CHECKING: {file_path}")
    logger.info(f"Shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"First 3 rows:\n{df.head(3).to_string()}")
    missing = df.isnull().sum()
    logger.info(f"Missing values:\n{missing[missing > 0]}")
    num_dup = df.duplicated().sum()
    logger.info(f"Number of duplicate rows: {num_dup}")
    logger.info(f"Column types:\n{df.dtypes}")
    nan_cols = df.columns[df.isnull().any()].tolist()
    logger.info(f"Columns with NaN values: {nan_cols}")
    logger.info(f"Statistical summary:\n{df.describe()}")

def suppress_warnings():
    """
    Suppress all warnings from being printed to stderr, to keep tqdm progress bar clear.
    """
    warnings.filterwarnings("ignore")

def check_file(file_path: str, logger: logging.Logger) -> None:
    """
    Perform EDA-check on a single file, log all outputs.
    """
    ext = os.path.splitext(file_path)[-1].lower()
    file_type = "parquet" if ext == ".parquet" else "csv"
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = load_data(file_path, file_type=file_type)
            log_file_info(df, file_path, logger)
    except Exception as e:
        tqdm.write(f"ERROR processing {file_path}: {e}")
        logger.error(f"ERROR processing {file_path}: {e}")

def process_folder(folder_path: str, logger: logging.Logger, progress_bar: tqdm) -> None:
    """
    Process all data files in a folder with progress bar.
    """
    logger.info(f"Processing folder: {folder_path}")
    
    try:
        if not os.path.exists(folder_path):
            logger.error(f"Folder does not exist: {folder_path}")
            return
            
        if not os.path.isdir(folder_path):
            logger.error(f"Path is not a directory: {folder_path}")
            return
            
        data_files = find_data_files(folder_path)
        logger.info(f"Found {len(data_files)} data files in '{folder_path}'.")
        
        for file_path in data_files:
            check_file(file_path, logger)
            progress_bar.update(1)
    except Exception as e:
        error_msg = f"Error processing folder {folder_path}: {str(e)}"
        logger.error(error_msg)

def main():
    """
    Main function to check all data files in specified folders with a single progress bar and per-folder output.
    Suppresses all warnings and errors from libraries to keep tqdm progress bar clean.
    At the end, runs log analysis script and optionally runs data cleaner.
    """
    # Declare global variable at the beginning of the function
    global initial_data_analysis
    initial_data_analysis = None
    
    parser = argparse.ArgumentParser(
        description="""Perform EDA checks on data files and optionally clean the data.
        
This script performs exploratory data analysis (EDA) on CSV and Parquet files in specified directories.
It checks for missing values, duplicates, data types, and provides statistical summaries.
Optionally, it can run the data cleaner to fix identified issues.
        
Example usage:
    # Basic EDA check
    python eda_batch_check.py
    
    # Run EDA check and clean data
    python eda_batch_check.py --clean
    
    # Specify custom output directory and NaN handling
    python eda_batch_check.py --clean --output-dir data/cleaned --handle-nan ffill
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--clean", 
        action="store_true",
        help="Run data cleaner after log analysis to fix issues"
    )
    parser.add_argument(
        "--output-dir", 
        default="cleaned",
        help="Output directory for cleaned data (default: 'cleaned')"
    )
    parser.add_argument(
        "--csv-delimiter", 
        default="\t",
        help="Delimiter for CSV files (default is tab which works for mql5_feed)"
    )
    parser.add_argument(
        "--csv-header", 
        default="0",
        help="CSV header row (0 = first row, or 'infer')"
    )
    parser.add_argument(
        "--handle-nan", 
        default="ffill",
        choices=['ffill', 'dropna_rows', 'none'],
        help="Strategy for handling NaN values: 'ffill' (forward fill), 'dropna_rows' (remove rows with NaN), 'none' (don't process)"
    )
    parser.add_argument(
        "--skip-verification",
        action="store_true",
        help="Skip asking to verify cleaned files with another EDA check"
    )
    parser.add_argument(
        "--log-file",
        default="logs/eda_batch_check.log",
        help="Log file name for recording the EDA process (will be created in logs directory)"
    )
    parser.add_argument(
        "--target-folders",
        nargs="+",
        default=["data/cache/csv_converted", "data/raw_parquet"],
        help="List of folders to check (default: data/cache/csv_converted data/raw_parquet)"
    )
    args = parser.parse_args()

    suppress_warnings()

    target_folders = args.target_folders

    # Define logger variable in the outer scope first
    logger = None
    
    def run_eda_check(folders_to_check):
        """Inner function to run EDA check on specified folders"""
        nonlocal logger
        
        # Reset if logger already exists
        if logger is not None:
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
        
        logger = setup_logger(args.log_file)
        
        all_data_files: Dict[str, List[str]] = {}
        total_files = 0
    
        for folder in folders_to_check:
            if not os.path.exists(folder):
                error_msg = f"Warning: Folder not found: {folder}"
                tqdm.write(error_msg)
                continue
                
            files = find_data_files(folder)
            all_data_files[folder] = files
            total_files += len(files)

        if total_files == 0:
            tqdm.write("No files found for checking in the specified folders.")
            logger.info("No files found for checking.")
            return False

        with tqdm(total=total_files, desc="EDA CHECK", unit="file", position=0, leave=True) as progress_bar:
            for folder in folders_to_check:
                if os.path.exists(folder):
                    process_folder(folder, logger, progress_bar)

        # Clear line to prevent overlap with future output
        print("\033[K", end="\r")
        log_path = Path(args.log_file)
        if not log_path.is_absolute():
            log_path = Path("logs") / log_path.name if not str(log_path).startswith("logs/") else log_path
        tqdm.write(f"\nLog file: {log_path}")
        logger.info("EDA batch check completed.")
        return True

    # Run initial EDA check on original folders
    initial_check_success = run_eda_check(target_folders)
    
    if not initial_check_success:
        return

    # Automatically analyze log after main process
    log_analyze_script = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "scripts", "log_analysis", "log_analyze.py"
    )
    if os.path.exists(log_analyze_script):
        # Clear previous line
        print("\033[K", end="\r")
        
        with tqdm(total=1, desc="ANALYZING LOG", unit="file", position=0, leave=True) as progress_bar:
            try:
                # Import the module directly instead of using subprocess for better integration
                import importlib.util
                spec = importlib.util.spec_from_file_location("log_analyze", log_analyze_script)
                log_analyze = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(log_analyze)
                
                # Use the global variable if available
                if initial_data_analysis:
                    eda_log_report = initial_data_analysis
                
                # Analyze the log file and store the results for later comparison
                initial_log_report = log_analyze.analyze_log(args.log_file)
                
                # Save the analysis results in a global variable for later comparison
                initial_data_analysis = initial_log_report
                progress_bar.update(1)
                
                # Print analysis statistics after progress bar completes
                print("\033[K", end="\r")  # Clear line
                tqdm.write("\n=== Log Analysis Summary ===")
                for category, stats in initial_log_report.items():
                    tqdm.write(f"{category}: {stats}")
                tqdm.write("==========================\n")
            except Exception as e:
                progress_bar.update(1)
                print("\033[K", end="\r")  # Clear line
                tqdm.write(f"\nLog analysis failed: {e}")
    else:
        tqdm.write("Log analysis script not found.")
    
    # Run data cleaner if requested
    if args.clean:
        data_cleaner_script_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "scripts", "data_processing"
        )
        
        data_cleaner_script = os.path.join(
            data_cleaner_script_dir, "data_cleaner_v2.py"
        )
        
        # Ensure the directory exists
        os.makedirs(data_cleaner_script_dir, exist_ok=True)
        
        if os.path.exists(data_cleaner_script):
            # Minimal output with progress bar
            try:
                # Ensure the log file goes to logs directory
                logs_dir = Path("logs")
                logs_dir.mkdir(exist_ok=True, parents=True)
                cleaner_log_file = logs_dir / "data_cleaner_run.log"
                
                # Create the output directory if it doesn't exist
                # Use args.output_dir but ensure it's prefixed with "data/" if not already
                if args.output_dir.startswith("data/"):
                    base_output_dir = args.output_dir
                else:
                    base_output_dir = os.path.join("data", args.output_dir)
                raw_parquet_dir = os.path.join(base_output_dir, "raw_parquet")
                csv_converted_dir = os.path.join(base_output_dir, "cache", "csv_converted")
                
                print(f"[DEBUG] Output directories:")
                print(f"[DEBUG] - Base output dir: {base_output_dir} (absolute: {os.path.abspath(base_output_dir)})")
                print(f"[DEBUG] - Raw parquet dir: {raw_parquet_dir} (absolute: {os.path.abspath(raw_parquet_dir)})")
                print(f"[DEBUG] - CSV converted dir: {csv_converted_dir} (absolute: {os.path.abspath(csv_converted_dir)})")
                
                # Create directories for cleaned data
                print(f"[DEBUG] Creating output directories...")
                try:
                    os.makedirs(raw_parquet_dir, exist_ok=True)
                    print(f"[DEBUG] Created directory: {raw_parquet_dir}")
                    
                    os.makedirs(csv_converted_dir, exist_ok=True)
                    print(f"[DEBUG] Created directory: {csv_converted_dir}")
                except Exception as e:
                    print(f"[DEBUG] ERROR creating directories: {str(e)}")
                    print(f"[DEBUG] Current permissions: {oct(os.stat('.').st_mode)[-3:]}")
                
                # Находим все файлы в target_folders
                all_files = []
                print(f"[DEBUG] Looking for files in target folders: {target_folders}")
                for folder in target_folders:
                    if os.path.exists(folder):
                        print(f"[DEBUG] Scanning folder: {folder}")
                        folder_files = find_data_files(folder)
                        print(f"[DEBUG] Found {len(folder_files)} files in folder {folder}")
                        all_files.extend(folder_files)
                    else:
                        print(f"[DEBUG] WARNING: Folder does not exist: {folder}")
                
                print(f"[DEBUG] Total files found across all folders: {len(all_files)}")
                
                # Группируем файлы по типу для обработки
                parquet_files = [f for f in all_files if f.lower().endswith('.parquet')]
                csv_files = [f for f in all_files if f.lower().endswith('.csv')]
                
                # Более детальная проверка файлов
                print(f"[DEBUG] Detailed file type breakdown:")
                print(f"[DEBUG] - Parquet files: {len(parquet_files)}")
                print(f"[DEBUG] - CSV files: {len(csv_files)}")
                print(f"[DEBUG] - Other files: {len(all_files) - len(parquet_files) - len(csv_files)}")
                
                # Проверка первых нескольких файлов каждого типа
                if parquet_files:
                    print(f"[DEBUG] First 3 parquet files:")
                    for i, f in enumerate(parquet_files[:3]):
                        file_size = os.path.getsize(f) if os.path.exists(f) else "File not found"
                        print(f"[DEBUG]   {i+1}. {f} (Size: {file_size} bytes)")
                        
                if csv_files:
                    print(f"[DEBUG] First 3 CSV files:")
                    for i, f in enumerate(csv_files[:3]):
                        file_size = os.path.getsize(f) if os.path.exists(f) else "File not found"
                        print(f"[DEBUG]   {i+1}. {f} (Size: {file_size} bytes)")
                
                # Запускаем два отдельных процесса для каждого типа файлов
                cmds = []
                
                # Проверяем наличие директории logs и создаем ее, если она не существует
                os.makedirs("logs", exist_ok=True)
                
                # Принудительное создание пустого лог-файла перед запуском
                with open(cleaner_log_file, "w", encoding="utf-8") as f:
                    f.write("# Data cleaner log file\n")
                
                # Убедимся, что директории для выходных файлов существуют
                os.makedirs(raw_parquet_dir, exist_ok=True)
                os.makedirs(csv_converted_dir, exist_ok=True)
                
                # Проверяем содержимое первого parquet файла, если он существует
                if parquet_files:
                    try:
                        first_parquet = parquet_files[0]
                        print(f"[DEBUG] Testing parquet file: {first_parquet}")
                        
                        # Проверяем наличие pyarrow
                        try:
                            import pyarrow
                            print(f"[DEBUG] Using pyarrow version: {pyarrow.__version__}")
                        except ImportError:
                            print("[DEBUG] WARNING: pyarrow not installed, which is required to read parquet files")
                            
                        # Проверяем наличие pandas
                        try:
                            import pandas as pd
                            print(f"[DEBUG] Using pandas version: {pd.__version__}")
                        except ImportError:
                            print("[DEBUG] WARNING: pandas not installed")
                        
                        # Проверяем возможность чтения файла
                        try:
                            if os.path.exists(first_parquet):
                                # Попытка прочитать файл с помощью pandas
                                df = pd.read_parquet(first_parquet)
                                print(f"[DEBUG] Successfully read parquet file. Shape: {df.shape}")
                                print(f"[DEBUG] Columns: {df.columns[:5].tolist()}...")
                            else:
                                print(f"[DEBUG] ERROR: Parquet file not found: {first_parquet}")
                        except Exception as e:
                            print(f"[DEBUG] ERROR reading parquet file: {type(e).__name__}: {str(e)}")
                            
                            # Проверка с помощью pyarrow напрямую
                            try:
                                table = pyarrow.parquet.read_table(first_parquet)
                                print(f"[DEBUG] pyarrow read successful. Schema: {table.schema}")
                            except Exception as e2:
                                print(f"[DEBUG] pyarrow read also failed: {type(e2).__name__}: {str(e2)}")
                    except Exception as e:
                        print(f"[DEBUG] Error during parquet file testing: {str(e)}")
                else:
                    print(f"[DEBUG] No parquet files to test")
                        
                # Сгруппировать файлы по директориям
                parquet_dirs = set(os.path.dirname(f) for f in parquet_files)
                csv_dirs = set(os.path.dirname(f) for f in csv_files)
                
                print(f"[DEBUG] Parquet directories: {parquet_dirs}")
                print(f"[DEBUG] CSV directories: {csv_dirs}")
                
                # Команда для parquet файлов
                if parquet_files:
                    print(f"[DEBUG] Found {len(parquet_files)} parquet files in {len(parquet_dirs)} directories")
                    for parquet_dir in parquet_dirs:
                        if not parquet_dir:  # Пропустить пустые директории
                            print(f"[DEBUG] Skipping empty directory")
                            continue
                            
                        print(f"[DEBUG] Creating command for parquet directory: {parquet_dir}")
                        # Проверяем существование директории
                        if not os.path.exists(parquet_dir):
                            print(f"[DEBUG] WARNING: Parquet directory does not exist: {parquet_dir}")
                        else:
                            print(f"[DEBUG] Parquet directory exists: {parquet_dir} (absolute: {os.path.abspath(parquet_dir)})")
                            
                        # Подсчитываем количество парке-файлов в этой директории
                        dir_parquet_files = [f for f in parquet_files if os.path.dirname(f) == parquet_dir]
                        print(f"[DEBUG] Found {len(dir_parquet_files)} parquet files in {parquet_dir}")
                        
                        # Проверим расширения файлов детально
                        extensions = {}
                        if os.path.exists(parquet_dir) and os.path.isdir(parquet_dir):
                            for f in os.listdir(parquet_dir):
                                ext = os.path.splitext(f)[1].lower()
                                extensions[ext] = extensions.get(ext, 0) + 1
                            print(f"[DEBUG] File extensions in {parquet_dir}: {extensions}")
                        
                        # Создаем команду для data_cleaner
                        cmd_parquet = [
                            "python", data_cleaner_script,
                            "-i", parquet_dir,
                            "-o", base_output_dir,
                            "--handle-duplicates", "remove",
                            "--handle-nan", args.handle_nan,
                            "--csv-delimiter", args.csv_delimiter,
                            "--csv-header", args.csv_header,
                            "--log-file", str(cleaner_log_file),
                            "--verbose"  # Добавляем флаг для большей детализации вывода
                        ]
                        cmds.append(('parquet', cmd_parquet))
                        print(f"[DEBUG] Added parquet command: {' '.join(cmd_parquet)}")
                
                # Команда для csv файлов
                if csv_files:
                    print(f"[DEBUG] Found {len(csv_files)} CSV files in {len(csv_dirs)} directories")
                    for csv_dir in csv_dirs:
                        if not csv_dir:  # Пропустить пустые директории
                            print(f"[DEBUG] Skipping empty directory")
                            continue
                        
                        print(f"[DEBUG] Creating command for CSV directory: {csv_dir}")
                        # Проверяем существование директории
                        if not os.path.exists(csv_dir):
                            print(f"[DEBUG] WARNING: CSV directory does not exist: {csv_dir}")
                        else:
                            print(f"[DEBUG] CSV directory exists: {csv_dir} (absolute: {os.path.abspath(csv_dir)})")
                            # Проверим содержимое директории
                            files_in_dir = [f for f in os.listdir(csv_dir) if f.lower().endswith('.csv')]
                            print(f"[DEBUG] Number of CSV files in directory: {len(files_in_dir)}")
                            
                        # Подсчитываем количество CSV-файлов в этой директории
                        dir_csv_files = [f for f in csv_files if os.path.dirname(f) == csv_dir]
                        print(f"[DEBUG] Found {len(dir_csv_files)} CSV files in {csv_dir}")
                        
                        # Проверим содержимое первого CSV файла из этой директории, если есть
                        if dir_csv_files:
                            try:
                                first_csv = dir_csv_files[0]
                                print(f"[DEBUG] Testing CSV file: {first_csv}")
                                if os.path.exists(first_csv):
                                    with open(first_csv, 'r', encoding='utf-8', errors='replace') as f:
                                        first_lines = [next(f, None) for _ in range(5)]
                                        first_lines = [line.strip() if line else None for line in first_lines]
                                    
                                    print(f"[DEBUG] First 5 lines of CSV file:")
                                    for i, line in enumerate(first_lines):
                                        if line:
                                            print(f"[DEBUG]   Line {i+1}: {line[:100]}{'...' if len(line) > 100 else ''}")
                                        else:
                                            print(f"[DEBUG]   Line {i+1}: <None>")
                                            
                                    # Определить вероятный разделитель
                                    if first_lines and first_lines[0]:
                                        first_line = first_lines[0]
                                        potential_delimiters = {',': first_line.count(','), 
                                                               '\t': first_line.count('\t'),
                                                               ';': first_line.count(';'),
                                                               '|': first_line.count('|')}
                                        likely_delimiter = max(potential_delimiters.items(), key=lambda x: x[1])[0]
                                        print(f"[DEBUG] Likely delimiter counts: {potential_delimiters}")
                                        print(f"[DEBUG] Most likely delimiter: '{likely_delimiter}' (ascii {ord(likely_delimiter)})")
                                        
                                    # Проверим, совпадает ли разделитель с указанным
                                    specified_delimiter = args.csv_delimiter
                                    print(f"[DEBUG] Specified delimiter: '{specified_delimiter}' (ascii {ord(specified_delimiter[0]) if specified_delimiter else 'None'})")
                            except Exception as e:
                                print(f"[DEBUG] Error while checking CSV file: {str(e)}")
                        
                        cmd_csv = [
                            "python", data_cleaner_script,
                            "-i", csv_dir,
                            "-o", base_output_dir,
                            "--handle-duplicates", "remove",
                            "--handle-nan", args.handle_nan,
                            "--csv-delimiter", args.csv_delimiter,
                            "--csv-header", args.csv_header,
                            "--log-file", str(cleaner_log_file),
                            "--verbose"  # Добавляем флаг для большей детализации вывода
                        ]
                        cmds.append(('csv', cmd_csv))
                        print(f"[DEBUG] Added CSV command: {' '.join(cmd_csv)}")
                
                if not cmds:
                    tqdm.write("Не найдено CSV или Parquet файлов для обработки.")
                    return
                # Only show progress bar, suppress output from subprocess
                with tqdm(total=len(cmds), desc="CLEANING DATA", unit="process", position=0, leave=True) as progress_bar:
                    all_success = True
                    
                    for file_type, cmd in cmds:
                        # Run subprocess with minimal output
                        tqdm.write(f"Processing {file_type} files...")
                        print(f"[DEBUG] ===== Running {file_type} command =====")
                        print(f"[DEBUG] Command: {' '.join(cmd)}")
                        
                        # Debug: проверить существование скрипта data_cleaner
                        cleaner_exists = os.path.exists(data_cleaner_script)
                        print(f"[DEBUG] Data cleaner script exists: {cleaner_exists}")
                        if cleaner_exists:
                            print(f"[DEBUG] Data cleaner script size: {os.path.getsize(data_cleaner_script)} bytes")
                        
                        # Запись команды в лог для диагностики
                        with open(cleaner_log_file, "a", encoding="utf-8") as f:
                            f.write(f"\nRunning command: {' '.join(cmd)}\n")
                        
                        # Создадим отдельный debug-лог для текущего запуска
                        debug_log_file = f"logs/debug_cleaner_{file_type}_{int(time.time())}.log"
                        
                        # Запишем всю отладочную информацию в отдельный лог-файл
                        with open(debug_log_file, "w", encoding="utf-8") as f:
                            f.write(f"Debug log for {file_type} command\n")
                            f.write(f"Command: {' '.join(cmd)}\n\n")
                            f.write(f"Current directory: {os.getcwd()}\n")
                        
                        # Проверяем существование входной директории
                        input_dir_index = cmd.index("-i") + 1
                        if input_dir_index < len(cmd):
                            input_dir = cmd[input_dir_index]
                            print(f"[DEBUG] Input directory: {input_dir}")
                            print(f"[DEBUG] Input directory exists: {os.path.exists(input_dir)}")
                            
                            # Запишем в debug-лог
                            with open(debug_log_file, "a", encoding="utf-8") as f:
                                f.write(f"Input directory: {input_dir}\n")
                                f.write(f"Input directory exists: {os.path.exists(input_dir)}\n")
                            
                            if os.path.exists(input_dir):
                                files_in_dir = os.listdir(input_dir)
                                print(f"[DEBUG] Files in input directory: {len(files_in_dir)}")
                                
                                # Подробная информация о файлах в директории
                                print(f"[DEBUG] File extensions in input directory:")
                                extensions = {}
                                for file in files_in_dir:
                                    ext = os.path.splitext(file)[1].lower()
                                    extensions[ext] = extensions.get(ext, 0) + 1
                                print(f"[DEBUG] Extensions: {extensions}")
                                
                                # Запишем в debug-лог
                                with open(debug_log_file, "a", encoding="utf-8") as f:
                                    f.write(f"Files in input directory: {len(files_in_dir)}\n")
                                    f.write(f"File extensions in input directory: {extensions}\n")
                                    f.write("\nFirst 10 files in directory:\n")
                                    for i, filename in enumerate(files_in_dir[:10]):
                                        file_path = os.path.join(input_dir, filename)
                                        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else "File not found"
                                        f.write(f"{i+1}. {filename} (Size: {file_size} bytes)\n")
                        
                        # Проверяем существование выходной директории
                        output_dir_index = cmd.index("-o") + 1
                        if output_dir_index < len(cmd):
                            output_dir = cmd[output_dir_index]
                            print(f"[DEBUG] Output directory: {output_dir}")
                            print(f"[DEBUG] Output directory exists: {os.path.exists(output_dir)}")
                        
                        # Выполняем команду
                        print(f"[DEBUG] Executing subprocess...")
                        start_time = time.time()
                        # Запускаем команду и перехватываем вывод для анализа
                        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        elapsed_time = time.time() - start_time
                        print(f"[DEBUG] Command completed in {elapsed_time:.2f} seconds with exit code: {result.returncode}")
                        
                        # Анализируем stdout на предмет ключевой информации
                        stdout_lines = result.stdout.splitlines()
                        stderr_lines = result.stderr.splitlines()
                        
                        # Ищем ключевые сообщения в выводе
                        processed_count = 0
                        processed_msg = None
                        for line in stdout_lines:
                            if "Processing file:" in line:
                                processed_count += 1
                            if "Successfully processed" in line:
                                processed_msg = line.strip()
                        
                        print(f"[DEBUG] Files processed according to output: {processed_count}")
                        if processed_msg:
                            print(f"[DEBUG] Success message: {processed_msg}")
                            
                        # Сохраняем вывод в debug-лог
                        with open(debug_log_file, "a", encoding="utf-8") as f:
                            f.write("\n=== COMMAND OUTPUT ===\n")
                            f.write(f"Exit code: {result.returncode}\n")
                            f.write(f"Execution time: {elapsed_time:.2f} seconds\n\n")
                            f.write("=== STDOUT ===\n")
                            f.write(result.stdout)
                            f.write("\n\n=== STDERR ===\n")
                            f.write(result.stderr)
                            f.write("\n\n=== ANALYSIS ===\n")
                            f.write(f"Files processed according to output: {processed_count}\n")
                            if processed_msg:
                                f.write(f"Success message: {processed_msg}\n")
                        
                        print(f"[DEBUG] Debug log saved to: {debug_log_file}")
                        
                        # Если есть ошибки, показываем первые несколько строк
                        if result.stderr:
                            print(f"[DEBUG] STDERR (first 3 lines):")
                            for i, line in enumerate(stderr_lines[:3]):
                                print(f"[DEBUG]   {line}")
                                
                        progress_bar.update(1)
                        
                        # Check if process succeeded
                        if result.returncode != 0:
                            # Only show error message without full command details
                            tqdm.write(f"Data cleaning for {file_type} files failed with exit code {result.returncode}")
                            
                            # Записать stderr в лог-файл
                            with open(cleaner_log_file, "a", encoding="utf-8") as f:
                                f.write(f"\nError output:\n{result.stderr}\n")
                            
                            # Показать первую строку ошибки
                            if result.stderr:
                                tqdm.write(f"Error: {result.stderr.splitlines()[0]}")
                                # Показать полную команду для отладки
                                tqdm.write(f"Command: {' '.join(cmd)}")
                            
                            tqdm.write(f"Check log file: {cleaner_log_file}")
                            all_success = False
                        else:
                            # Записать stdout в лог-файл
                            with open(cleaner_log_file, "a", encoding="utf-8") as f:
                                f.write(f"\nOutput:\n{result.stdout}\n")
                                
                            #
                            processed_files = result.stdout.count("Processing file:")
                            tqdm.write(f"Successfully processed {processed_files} {file_type} files")
                    
                    # Show minimal success message
                    if all_success:
                        tqdm.write(f"Data cleaning completed. Files saved to: {base_output_dir}")
                    else:
                        tqdm.write(f"Data cleaning completed with some errors. Check log file: {cleaner_log_file}")

                # Ask user if they want to verify cleaned files
                if not args.skip_verification:
                    # Clear any leftovers from progress bar
                    print("\033[K", end="\r")
                    verification = input("\nVerify cleaned files with another EDA check? (Y/n): ")
                    if verification.lower() != 'n':
                        # Ensure output directory exists to avoid warning message
                        # Since files are saved to base_output_dir, we need to check that path
                        if os.path.exists(base_output_dir):
                            run_eda_check([base_output_dir])

                            # Analyze data_cleaner_run.log
                            cleaner_log_file = Path("logs") / "data_cleaner_run.log"
                            try:
                                if os.path.exists(cleaner_log_file):
                                    # Analyze the cleaning log with minimal output
                                    with tqdm(total=1, desc="ANALYZING CLEANING RESULTS", unit="log", position=0, leave=True) as progress_bar:
                                        with open(cleaner_log_file, "r", encoding="utf-8") as f:
                                            log_content = f.read()

                                        # Extract statistics from log
                                        total_files = log_content.count("Processing file:")
                                        files_with_nan = log_content.count("NaN values detected")
                                        files_with_duplicates = log_content.count("Duplicates removed")

                                        # Calculate total rows removed
                                        total_rows_removed = 0
                                        for line in log_content.split("\n"):
                                            if "Duplicates removed:" in line:
                                                try:
                                                    removed = int(line.split(":")[1].split(".")[0].strip())
                                                    total_rows_removed += removed
                                                except (ValueError, IndexError):
                                                    continue

                                        # Get final summary
                                        final_summary = None
                                        for line in reversed(log_content.split("\n")):
                                            if "Successfully processed/saved:" in line:
                                                final_summary = line
                                                break

                                        progress_bar.update(1)

                                        # Display summary directly on the screen
                                        tqdm.write("\n" + "-" * 50)
                                        tqdm.write("Data Cleaning Results:")
                                        tqdm.write(f"Total files processed: {total_files}")
                                        tqdm.write(f"Files with NaN values: {files_with_nan}")
                                        tqdm.write(f"Files with duplicates: {files_with_duplicates}")
                                        tqdm.write(f"Total rows removed: {total_rows_removed}")
                                        if final_summary:
                                            tqdm.write(f"\nFinal Summary: {final_summary}")
                                        tqdm.write("-" * 50)
                                else:
                                    tqdm.write(f"Data cleaning log file not found at: {cleaner_log_file}")
                            except Exception as e:
                                tqdm.write(f"Error analyzing cleaning log: {e}")
                        else:
                            tqdm.write(f"Output directory {args.output_dir} not found. No files to verify.")
                    else:
                        tqdm.write(f"\nSkipping verification. Run manually with: python eda_batch_check.py --target-folders {base_output_dir}")
            except Exception as e:
                print(f"Error during data cleaning: {str(e).split(':')[0]}")
                print("Check logs directory for details.")
                
                # Try to provide guidance about the issue
                if "unrecognized arguments" in str(e):
                    print("\nNOTE: There may be a mismatch between the arguments expected by data_cleaner_v2.py")
                    print("and those being passed. Check the script documentation for correct usage.")
        else:
            print(f"Data cleaner script not found at: {data_cleaner_script}")
            print("Please create scripts/data_processing/data_cleaner_v2.py first.")

if __name__ == "__main__":
    main()