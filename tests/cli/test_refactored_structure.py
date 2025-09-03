# -*- coding: utf-8 -*-
# tests/cli/test_refactored_structure.py

"""
Tests for the refactored CLI structure.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestCLIStructure:
    """Test that the refactored CLI structure works correctly."""
    
    def test_core_imports(self):
        """Test that core CLI modules can be imported."""
        try:
            from src.cli.core import (
                main,
                show_indicator_help,
                parse_arguments,
                validate_and_process_arguments,
                ColoredHelpFormatter
            )
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import core CLI modules: {e}")
    
    def test_indicators_imports(self):
        """Test that indicators modules can be imported."""
        try:
            from src.cli.indicators import IndicatorSearcher
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import indicators modules: {e}")
    
    def test_parsers_imports(self):
        """Test that parsers modules can be imported."""
        try:
            from src.cli.parsers import (
                parse_indicator_parameters,
                parse_rsi_parameters,
                parse_macd_parameters
            )
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import parsers modules: {e}")
    
    def test_examples_imports(self):
        """Test that examples modules can be imported."""
        try:
            from src.cli.examples import show_cli_examples_colored
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import examples modules: {e}")
    
    def test_encyclopedia_imports(self):
        """Test that encyclopedia modules can be imported."""
        try:
            from src.cli.encyclopedia import QuantEncyclopedia
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import encyclopedia modules: {e}")
    
    def test_main_cli_imports(self):
        """Test that main CLI module can be imported."""
        try:
            from src.cli.cli import (
                main,
                show_indicator_help,
                parse_arguments,
                validate_and_process_arguments,
                parse_indicator_parameters
            )
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import main CLI module: {e}")
    
    def test_show_mode_imports(self):
        """Test that show mode modules can be imported."""
        try:
            from src.cli.core.cli_show_mode import main_show_mode, show_help
            from src.cli.core.show_csv import handle_csv_show_mode
            from src.cli.core.show_yfinance import handle_yfinance_show_mode
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import show mode modules: {e}")


class TestFileStructure:
    """Test that the file structure is correct."""
    
    def test_core_directory_structure(self):
        """Test that core directory contains expected files."""
        core_dir = Path("src/cli/core")
        expected_files = [
            "__init__.py",
            "cli.py",
            "argument_parser.py",
            "argument_validator.py",
            "help_formatter.py",
            "cli_show_mode.py",
            "show_csv.py",
            "show_yfinance.py",
            "show_polygon.py",
            "show_binance.py",
            "show_exrate.py",
            "show_indicators.py"
        ]
        
        for file_name in expected_files:
            file_path = core_dir / file_name
            assert file_path.exists(), f"Expected file {file_name} not found in core directory"
    
    def test_indicators_directory_structure(self):
        """Test that indicators directory contains expected files."""
        indicators_dir = Path("src/cli/indicators")
        expected_files = [
            "__init__.py",
            "indicators_search.py"
        ]
        
        for file_name in expected_files:
            file_path = indicators_dir / file_name
            assert file_path.exists(), f"Expected file {file_name} not found in indicators directory"
    
    def test_parsers_directory_structure(self):
        """Test that parsers directory contains expected files."""
        parsers_dir = Path("src/cli/parsers")
        expected_files = [
            "__init__.py",
            "indicator_parsers.py"
        ]
        
        for file_name in expected_files:
            file_path = parsers_dir / file_name
            assert file_path.exists(), f"Expected file {file_name} not found in parsers directory"
    
    def test_parsers_indicators_directory_structure(self):
        """Test that parsers/indicators directory contains expected files."""
        indicators_dir = Path("src/cli/parsers/indicators")
        expected_files = [
            "__init__.py",
            "rsi_parsers.py",
            "moving_average_parsers.py",
            "momentum_parsers.py",
            "volatility_parsers.py",
            "advanced_parsers.py",
            "volume_sentiment_parsers.py",
            "statistical_parsers.py"
        ]
        
        for file_name in expected_files:
            file_path = indicators_dir / file_name
            assert file_path.exists(), f"Expected file {file_name} not found in parsers/indicators directory"
    
    def test_examples_directory_structure(self):
        """Test that examples directory contains expected files."""
        examples_dir = Path("src/cli/examples")
        expected_files = [
            "__init__.py",
            "cli_examples.py"
        ]
        
        for file_name in expected_files:
            file_path = examples_dir / file_name
            assert file_path.exists(), f"Expected file {file_name} not found in examples directory"
    
    def test_encyclopedia_directory_structure(self):
        """Test that encyclopedia directory contains expected files."""
        encyclopedia_dir = Path("src/cli/encyclopedia")
        expected_files = [
            "__init__.py",
            "quant_encyclopedia.py"
        ]
        
        for file_name in expected_files:
            file_path = encyclopedia_dir / file_name
            assert file_path.exists(), f"Expected file {file_name} not found in encyclopedia directory"
    
    def test_help_directory_structure(self):
        """Test that help directory contains expected files."""
        help_dir = Path("src/cli/help")
        expected_files = [
            "__init__.py",
            "basic_indicators.py",
            "moving_averages.py",
            "volatility_indicators.py",
            "momentum_indicators.py",
            "volume_indicators.py",
            "advanced_indicators.py",
            "statistical_indicators.py",
            "sentiment_indicators.py"
        ]
        
        for file_name in expected_files:
            file_path = help_dir / file_name
            assert file_path.exists(), f"Expected file {file_name} not found in help directory"


class TestFileSizes:
    """Test that files are within size limits."""
    
    def test_file_sizes_under_300_lines(self):
        """Test that all new files are under 300 lines."""
        max_lines = 300
        
        # Check core files
        core_files = [
            "src/cli/core/help_formatter.py",
            "src/cli/core/argument_parser.py",
            "src/cli/core/argument_validator.py",
            "src/cli/core/cli.py",
            "src/cli/core/cli_show_mode.py",
            "src/cli/core/indicator_help.py",
            "src/cli/core/special_flags_handler.py",
            "src/cli/core/show_csv.py",
            "src/cli/core/show_yfinance.py",
            "src/cli/core/show_polygon.py",
            "src/cli/core/show_binance.py",
            "src/cli/core/show_exrate.py",
            "src/cli/core/show_indicators.py"
        ]
        
        for file_path in core_files:
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_count = len(f.readlines())
                    assert line_count <= max_lines, f"File {file_path} has {line_count} lines, exceeds {max_lines}"
        
        # Check parsers files
        parsers_files = [
            "src/cli/parsers/indicator_parsers.py",
            "src/cli/parsers/indicators/__init__.py",
            "src/cli/parsers/indicators/rsi_parsers.py",
            "src/cli/parsers/indicators/moving_average_parsers.py",
            "src/cli/parsers/indicators/momentum_parsers.py",
            "src/cli/parsers/indicators/volatility_parsers.py",
            "src/cli/parsers/indicators/advanced_parsers.py",
            "src/cli/parsers/indicators/volume_sentiment_parsers.py",
            "src/cli/parsers/indicators/statistical_parsers.py"
        ]
        
        for file_path in parsers_files:
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_count = len(f.readlines())
                    assert line_count <= max_lines, f"File {file_path} has {line_count} lines, exceeds {max_lines}"
        
        # Check help files
        help_files = [
            "src/cli/help/__init__.py",
            "src/cli/help/basic_indicators.py",
            "src/cli/help/moving_averages.py",
            "src/cli/help/volatility_indicators.py",
            "src/cli/help/momentum_indicators.py",
            "src/cli/help/volume_indicators.py",
            "src/cli/help/advanced_indicators.py",
            "src/cli/help/statistical_indicators.py",
            "src/cli/help/sentiment_indicators.py"
        ]
        
        for file_path in help_files:
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_count = len(f.readlines())
                    assert line_count <= max_lines, f"File {file_path} has {line_count} lines, exceeds {max_lines}"


if __name__ == "__main__":
    pytest.main([__file__])
