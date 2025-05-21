# Handles folder statistics

import os

def get_folder_stats(folder_path):
    total_size = 0
    file_count = 0
    for root, _, files in os.walk(folder_path):
        for f in files:
            if f.endswith('.parquet'):
                fp = os.path.join(root, f)
                total_size += os.path.getsize(fp)
                file_count += 1
    return {
        'folder': folder_path,
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'file_count': file_count
    }
