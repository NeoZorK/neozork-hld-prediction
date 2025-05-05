import os
import tempfile
import pandas as pd
import pytest
from scripts.data_processing.data_cleaner_v2 import (
    setup_logger,
    find_data_files,
    clean_file,
    parse_header
)

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def sample_csv_file(temp_dir):
    """Create a sample CSV file with test data."""
    file_path = os.path.join(temp_dir, "test.csv")
    df = pd.DataFrame({
        'A': [1, 1, 2, 2, 3, None],
        'B': ['a', 'a', 'b', 'b', 'c', None],
        'C': [1.1, 1.1, 2.2, 2.2, 3.3, None]
    })
    df.to_csv(file_path, index=False)
    return file_path

@pytest.fixture
def sample_parquet_file(temp_dir):
    """Create a sample Parquet file with test data."""
    file_path = os.path.join(temp_dir, "test.parquet")
    df = pd.DataFrame({
        'A': [1, 1, 2, 2, 3, None],
        'B': ['a', 'a', 'b', 'b', 'c', None],
        'C': [1.1, 1.1, 2.2, 2.2, 3.3, None]
    })
    df.to_parquet(file_path, index=False)
    return file_path

def test_setup_logger(temp_dir):
    """Test logger setup."""
    log_file = os.path.join(temp_dir, "test.log")
    logger = setup_logger(log_file)
    
    assert logger is not None
    assert len(logger.handlers) == 2  # File and console handlers
    assert os.path.exists(log_file)

def test_find_data_files(temp_dir, sample_csv_file, sample_parquet_file):
    """Test finding data files in directory."""
    files = find_data_files([temp_dir])
    assert len(files) == 2
    assert any(sample_csv_file in f[0] for f in files)
    assert any(sample_parquet_file in f[0] for f in files)

def test_clean_file_csv_duplicates(temp_dir, sample_csv_file):
    """Test cleaning CSV file with duplicates."""
    output_dir = os.path.join(temp_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    result = clean_file(
        input_path=sample_csv_file,
        input_base_dir=temp_dir,
        output_base_dir=output_dir,
        handle_duplicates="remove",
        handle_nan="ffill",
        csv_delimiter=",",
        csv_header=0
    )
    
    assert result is True
    output_file = os.path.join(output_dir, "test.csv")
    assert os.path.exists(output_file)
    
    df = pd.read_csv(output_file)
    assert len(df) == 3  # Should have 3 unique rows

def test_clean_file_parquet_nan(temp_dir, sample_parquet_file):
    """Test cleaning Parquet file with NaN values."""
    output_dir = os.path.join(temp_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    result = clean_file(
        input_path=sample_parquet_file,
        input_base_dir=temp_dir,
        output_base_dir=output_dir,
        handle_duplicates="remove",
        handle_nan="ffill",
        csv_delimiter=",",
        csv_header=0
    )
    
    assert result is True
    output_file = os.path.join(output_dir, "test.parquet")
    assert os.path.exists(output_file)
    
    df = pd.read_parquet(output_file)
    assert df.isnull().sum().sum() == 0  # No NaN values should remain

def test_clean_file_invalid_input(temp_dir):
    """Test handling of invalid input file."""
    invalid_file = os.path.join(temp_dir, "invalid.txt")
    with open(invalid_file, 'w') as f:
        f.write("test")
    
    output_dir = os.path.join(temp_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    result = clean_file(
        input_path=invalid_file,
        input_base_dir=temp_dir,
        output_base_dir=output_dir,
        handle_duplicates="remove",
        handle_nan="ffill",
        csv_delimiter=",",
        csv_header=0
    )
    
    assert result is False

def test_parse_header():
    """Test header parsing function."""
    assert parse_header("0") == 0
    assert parse_header("1") == 1
    assert parse_header("infer") is None
    assert parse_header("none") is None
    
    with pytest.raises(argparse.ArgumentTypeError):
        parse_header("invalid")

def test_clean_file_empty_dataframe(temp_dir):
    """Test handling of empty DataFrame."""
    empty_file = os.path.join(temp_dir, "empty.csv")
    pd.DataFrame().to_csv(empty_file, index=False)
    
    output_dir = os.path.join(temp_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    result = clean_file(
        input_path=empty_file,
        input_base_dir=temp_dir,
        output_base_dir=output_dir,
        handle_duplicates="remove",
        handle_nan="ffill",
        csv_delimiter=",",
        csv_header=0
    )
    
    assert result is True
    output_file = os.path.join(output_dir, "empty.csv")
    assert not os.path.exists(output_file)  # Empty files should not be saved

def test_clean_file_different_nan_strategies(temp_dir, sample_csv_file):
    """Test different NaN handling strategies."""
    output_dir = os.path.join(temp_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Test ffill strategy
    result_ffill = clean_file(
        input_path=sample_csv_file,
        input_base_dir=temp_dir,
        output_base_dir=output_dir,
        handle_duplicates="remove",
        handle_nan="ffill",
        csv_delimiter=",",
        csv_header=0
    )
    assert result_ffill is True
    
    # Test dropna_rows strategy
    result_dropna = clean_file(
        input_path=sample_csv_file,
        input_base_dir=temp_dir,
        output_base_dir=output_dir,
        handle_duplicates="remove",
        handle_nan="dropna_rows",
        csv_delimiter=",",
        csv_header=0
    )
    assert result_dropna is True
    
    # Test none strategy
    result_none = clean_file(
        input_path=sample_csv_file,
        input_base_dir=temp_dir,
        output_base_dir=output_dir,
        handle_duplicates="remove",
        handle_nan="none",
        csv_delimiter=",",
        csv_header=0
    )
    assert result_none is True 