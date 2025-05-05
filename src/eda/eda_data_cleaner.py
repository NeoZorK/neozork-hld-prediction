# src/eda/eda_data_cleaner.py

import os
import subprocess
import time
from pathlib import Path
from tqdm import tqdm
from src.eda.eda_file_utils import find_data_files

def run_data_cleaner(args, target_folders):
    """
    Run the data cleaner script and analyze its log.
    """
    data_cleaner_script_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts", "data_processing"
    )
    data_cleaner_script = os.path.join(data_cleaner_script_dir, "data_cleaner_v2.py")
    os.makedirs(data_cleaner_script_dir, exist_ok=True)

    if not os.path.exists(data_cleaner_script):
        print(f"Data cleaner script not found at: {data_cleaner_script}")
        print("Please create scripts/data_processing/data_cleaner_v2.py first.")
        return

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True, parents=True)
    cleaner_log_file = logs_dir / "data_cleaner_run.log"

    if args.output_dir.startswith("data/"):
        base_output_dir = args.output_dir
    else:
        base_output_dir = os.path.join("data", args.output_dir)
    raw_parquet_dir = os.path.join(base_output_dir, "raw_parquet")
    csv_converted_dir = os.path.join(base_output_dir, "cache", "csv_converted")
    os.makedirs(raw_parquet_dir, exist_ok=True)
    os.makedirs(csv_converted_dir, exist_ok=True)

    all_files = []
    for folder in target_folders:
        if os.path.exists(folder):
            all_files.extend(find_data_files(folder))
    required_folders = ["data/raw_parquet", "data/cache/csv_converted"]
    for folder in required_folders:
        if folder not in target_folders and os.path.exists(folder):
            all_files.extend(find_data_files(folder))
    parquet_files = [f for f in all_files if f.lower().endswith('.parquet')]
    csv_files = [f for f in all_files if f.lower().endswith('.csv')]
    all_dirs = set()
    if parquet_files:
        all_dirs.update(os.path.dirname(f) for f in parquet_files)
    if csv_files:
        all_dirs.update(os.path.dirname(f) for f in csv_files)
    if "data/raw_parquet" not in all_dirs and os.path.exists("data/raw_parquet"):
        all_dirs.add("data/raw_parquet")
    if "data/cache/csv_converted" not in all_dirs and os.path.exists("data/cache/csv_converted"):
        all_dirs.add("data/cache/csv_converted")
    all_dirs_list = list(all_dirs)

    if not all_dirs_list:
        tqdm.write("Не найдено CSV или Parquet файлов для обработки.")
        return

    cmd = [
        "python", data_cleaner_script,
        "-i", *all_dirs_list,
        "-o", base_output_dir,
        "--handle-duplicates", "remove",
        "--handle-nan", args.handle_nan,
        "--csv-delimiter", args.csv_delimiter,
        "--csv-header", args.csv_header,
        "--log-file", str(cleaner_log_file),
        "--verbose"
    ]

    with open(cleaner_log_file, "w", encoding="utf-8") as f:
        f.write("# Data cleaner log file\n")
        f.write(f"\nRunning command: {' '.join(cmd)}\n")

    print(f"Processing all files...")
    start_time = time.time()
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    elapsed_time = time.time() - start_time

    with open(cleaner_log_file, "a", encoding="utf-8") as f:
        if result.returncode != 0:
            f.write(f"\nError output:\n{result.stderr}\n")
        else:
            f.write(f"\nOutput:\n{result.stdout}\n")

    if result.returncode != 0:
        print(f"Data cleaning failed with exit code {result.returncode}")
        if result.stderr:
            print(f"Error: {result.stderr.splitlines()[0]}")
        print(f"Check log file: {cleaner_log_file}")
        return

    print(f"Data cleaning completed. Files saved to: {base_output_dir}")

    # Verification and log analysis can be added here as a separate function if needed