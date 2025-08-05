# -*- coding: utf-8 -*-
# tests/cli/test_adx_help.py

"""
Test ADX help functionality.
All comments and text are in English.
"""

import pytest
from src.cli.error_handling import get_indicator_help_data


def test_adx_help_data_exists():
    """Test that ADX help data exists and has correct structure."""
    help_data = get_indicator_help_data('adx')
    
    assert help_data is not None
    assert 'name' in help_data
    assert 'description' in help_data
    assert 'format' in help_data
    assert 'parameters' in help_data
    assert 'examples' in help_data
    assert 'tips' in help_data
    assert 'common_errors' in help_data


def test_adx_help_data_content():
    """Test that ADX help data has correct content."""
    help_data = get_indicator_help_data('adx')
    
    assert help_data['name'] == 'ADX (Average Directional Index)'
    assert 'trend strength' in help_data['description'].lower()
    assert help_data['format'] == 'adx:period'
    
    # Check parameters
    assert len(help_data['parameters']) == 1
    param = help_data['parameters'][0]
    assert param[0] == 'period'
    assert param[1] == 'int'
    assert 'ADX calculation period' in param[2]
    assert param[3] == '14'
    
    # Check examples
    assert len(help_data['examples']) >= 2
    examples = [ex[0] for ex in help_data['examples']]
    assert 'adx:14' in examples
    assert 'adx:21' in examples
    
    # Check tips
    assert len(help_data['tips']) >= 5
    tips_text = ' '.join(help_data['tips']).lower()
    assert 'weak trend' in tips_text
    assert 'strong trend' in tips_text
    
    # Check common errors
    assert len(help_data['common_errors']) >= 2
    errors_text = ' '.join(help_data['common_errors']).lower()
    assert 'invalid period' in errors_text
    assert 'positive integer' in errors_text


def test_adx_help_case_insensitive():
    """Test that ADX help works with different case variations."""
    help_data_upper = get_indicator_help_data('ADX')
    help_data_lower = get_indicator_help_data('adx')
    help_data_mixed = get_indicator_help_data('Adx')
    
    assert help_data_upper is not None
    assert help_data_lower is not None
    assert help_data_mixed is not None
    
    assert help_data_upper['name'] == help_data_lower['name']
    assert help_data_upper['name'] == help_data_mixed['name']


def test_adx_help_vs_macd_help_structure():
    """Test that ADX help has the same structure as MACD help."""
    adx_help = get_indicator_help_data('adx')
    macd_help = get_indicator_help_data('macd')
    
    # Both should have the same keys
    assert set(adx_help.keys()) == set(macd_help.keys())
    
    # Both should have the same data types for each key
    for key in adx_help.keys():
        assert type(adx_help[key]) == type(macd_help[key])
    
    # Both should have parameters as list of tuples
    assert isinstance(adx_help['parameters'], list)
    assert isinstance(macd_help['parameters'], list)
    
    for param in adx_help['parameters']:
        assert isinstance(param, tuple)
        assert len(param) == 4  # name, type, description, default
    
    for param in macd_help['parameters']:
        assert isinstance(param, tuple)
        assert len(param) == 4  # name, type, description, default
    
    # Both should have examples as list of tuples
    assert isinstance(adx_help['examples'], list)
    assert isinstance(macd_help['examples'], list)
    
    for example in adx_help['examples']:
        assert isinstance(example, tuple)
        assert len(example) == 2  # command, description
    
    for example in macd_help['examples']:
        assert isinstance(example, tuple)
        assert len(example) == 2  # command, description
    
    # Both should have tips and common_errors as lists
    assert isinstance(adx_help['tips'], list)
    assert isinstance(macd_help['tips'], list)
    assert isinstance(adx_help['common_errors'], list)
    assert isinstance(macd_help['common_errors'], list)


if __name__ == '__main__':
    pytest.main([__file__]) 