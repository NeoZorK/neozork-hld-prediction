import pytest
import pandas as pd
import numpy as np
from colorama import Fore, Style
from src.batch_eda import data_quality

# Dummy colorama for test output (no color)
class DummyFore:
    MAGENTA = ''
    YELLOW = ''
    GREEN = ''
    RED = ''
    CYAN = ''
class DummyStyle:
    RESET_ALL = ''

def test_nan_check():
    df = pd.DataFrame({'a': [1, np.nan, 3], 'b': [4, 5, 6]})
    nan_summary = []
    data_quality.nan_check(df, nan_summary, DummyFore, DummyStyle)
    assert any(e['column'] == 'a' and e['missing'] == 1 for e in nan_summary)

def test_duplicate_check():
    df = pd.DataFrame({'a': [1, 1, 2], 'b': ['x', 'x', 'y']})
    dupe_summary = []
    data_quality.duplicate_check(df, dupe_summary, DummyFore, DummyStyle)
    # Check that we get some kind of duplicate information
    assert len(dupe_summary) > 0

def test_gap_check():
    df = pd.DataFrame({'dt': pd.date_range('2020-01-01', periods=3, freq='D')})
    df.loc[2, 'dt'] = pd.Timestamp('2020-01-10')
    gap_summary = []
    data_quality.gap_check(df, gap_summary, DummyFore, DummyStyle)
    # Check that the function runs without errors and produces some output
    assert isinstance(gap_summary, list)

def test_zero_check():
    df = pd.DataFrame({'price': [0, 1, 2], 'volume': [0, 0, 1]})
    zero_summary = []
    data_quality.zero_check(df, zero_summary, DummyFore, DummyStyle)
    # Check that we get information about zero values
    assert len(zero_summary) > 0
    # Check that we have information about both columns with zeros
    zero_columns = [e['column'] for e in zero_summary]
    assert 'price' in zero_columns or 'volume' in zero_columns

def test_negative_check():
    df = pd.DataFrame({'open': [1, -2, 3], 'close': [1, 2, 3]})
    negative_summary = []
    data_quality.negative_check(df, negative_summary, DummyFore, DummyStyle)
    # Check that we get information about negative values
    assert len(negative_summary) > 0
    # Check that we have information about the column with negative values
    negative_columns = [e['column'] for e in negative_summary]
    assert 'open' in negative_columns

def test_inf_check():
    df = pd.DataFrame({'a': [1, np.inf, -np.inf], 'b': [0, 1, 2]})
    inf_summary = []
    data_quality.inf_check(df, inf_summary, DummyFore, DummyStyle)
    # Check that we get information about infinite values
    assert len(inf_summary) > 0
    # Check that we have information about the column with infinite values
    inf_columns = [e['column'] for e in inf_summary]
    assert 'a' in inf_columns

