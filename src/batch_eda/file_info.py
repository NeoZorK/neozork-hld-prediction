# Handles file information extraction

import os
import pandas as pd
import pyarrow.parquet as pq

# Handles file information extraction
def get_file_info(filepath):
   # Get file information
    info = {}
    info['file_path'] = filepath
    info['file_name'] = os.path.basename(filepath)
    info['file_size_mb'] = round(os.path.getsize(filepath) / (1024 * 1024), 2)
    try:
        # Get Parquet file schema
        parquet_file = pq.ParquetFile(filepath)
        schema = parquet_file.schema
        info['parquet_schema'] = str(schema)

        # Get schema fields
        schema_arrow = schema.to_arrow_schema()
        datetime_fields = []
        for name, typ in zip(schema_arrow.names, schema_arrow.types):
            if 'timestamp' in str(typ).lower() or 'datetime' in str(typ).lower():
                datetime_fields.append(name)
        info['datetime_or_timestamp_fields'] = datetime_fields

        df = pd.read_parquet(filepath)
        info['n_rows'], info['n_cols'] = df.shape
        info['columns'] = list(df.columns)
        info['dtypes'] = dict(df.dtypes.apply(lambda x: str(x)))

        # Separate datetime and timestamp columns
        datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
        timestamp_cols = [col for col in df.columns if str(df.dtypes[col]).startswith('datetime64[ns]') or str(df.dtypes[col]).startswith('timestamp')]
        info['datetime_columns'] = datetime_cols
        info['timestamp_columns'] = timestamp_cols
    except Exception as e:
        info['error'] = str(e)
    return info

def get_file_info_from_dataframe(df):
    """Get file information from a DataFrame instead of a file path."""
    info = {}
    info['file_path'] = 'DataFrame'
    info['file_name'] = 'DataFrame'
    info['file_size_mb'] = 0  # Cannot determine size from DataFrame
    
    try:
        info['n_rows'], info['n_cols'] = df.shape
        info['columns'] = list(df.columns)
        info['dtypes'] = dict(df.dtypes.apply(lambda x: str(x)))

        # Separate datetime and timestamp columns
        datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
        timestamp_cols = [col for col in df.columns if str(df.dtypes[col]).startswith('datetime64[ns]') or str(df.dtypes[col]).startswith('timestamp')]
        info['datetime_columns'] = datetime_cols
        info['timestamp_columns'] = timestamp_cols
        info['datetime_or_timestamp_fields'] = datetime_cols + timestamp_cols
    except Exception as e:
        info['error'] = str(e)
    return info
