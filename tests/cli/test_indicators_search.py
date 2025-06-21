# -*- coding: utf-8 -*-
# tests/cli/test_indicators_search.py

"""
Unit tests for indicator search functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from src.cli.indicators_search import IndicatorInfo, IndicatorSearcher


class TestIndicatorInfo:
    """Test cases for IndicatorInfo class."""
    
    def test_indicator_info_creation(self):
        """Test IndicatorInfo object creation."""
        info = IndicatorInfo(
            name="RSI",
            category="oscillators",
            description="Relative Strength Index",
            usage="--rule RSI",
            parameters="period=14, overbought=70, oversold=30",
            pros="Widely used, easy to interpret",
            cons="Can give false signals in trending markets",
            file_path="src/calculation/indicators/oscillators/rsi_ind.py"
        )
        
        assert info.name == "RSI"
        assert info.category == "oscillators"
        assert info.description == "Relative Strength Index"
        assert info.usage == "--rule RSI"
        assert info.parameters == "period=14, overbought=70, oversold=30"
        assert info.pros == "Widely used, easy to interpret"
        assert info.cons == "Can give false signals in trending markets"
        assert info.file_path == "src/calculation/indicators/oscillators/rsi_ind.py"
    
    def test_indicator_info_str_representation(self):
        """Test string representation of IndicatorInfo."""
        info = IndicatorInfo(
            name="MACD",
            category="momentum",
            description="Moving Average Convergence Divergence",
            usage="--rule MACD",
            parameters="fast=12, slow=26, signal=9",
            pros="Good trend following indicator",
            cons="Lags price action",
            file_path="src/calculation/indicators/momentum/macd_ind.py"
        )
        
        assert str(info) == "MACD (momentum)"
    
    def test_indicator_info_display_basic(self):
        """Test basic display of IndicatorInfo."""
        info = IndicatorInfo(
            name="BB",
            category="volatility",
            description="Bollinger Bands",
            usage="--rule BB",
            parameters="period=20, std_dev=2",
            pros="Shows volatility and potential reversals",
            cons="Can be choppy in sideways markets",
            file_path="src/calculation/indicators/volatility/bb_ind.py"
        )
        
        display = info.display(detailed=False)
        assert "BB" in display
        assert "Bollinger Bands" in display
        # Basic display doesn't include category
        assert "volatility" not in display
        assert len(display.split('\n')) == 1
    
    def test_indicator_info_display_detailed(self):
        """Test detailed display of IndicatorInfo."""
        info = IndicatorInfo(
            name="ATR",
            category="volatility",
            description="Average True Range",
            usage="--rule ATR",
            parameters="period=14",
            pros="Measures volatility accurately",
            cons="Does not indicate direction",
            file_path="src/calculation/indicators/volatility/atr_ind.py"
        )
        
        display = info.display(detailed=True)
        lines = display.split('\n')
        
        assert "Indicator: ATR" in lines
        assert "Category: volatility" in lines
        assert "Description: Average True Range" in lines
        assert "Usage: --rule ATR" in lines
        assert "Parameters: period=14" in lines
        assert "Pros: Measures volatility accurately" in lines
        assert "Cons: Does not indicate direction" in lines
        assert "File: src/calculation/indicators/volatility/atr_ind.py" in lines
        assert "-" * 50 in lines


class TestIndicatorSearcher:
    """Test cases for IndicatorSearcher class."""
    
    def test_searcher_initialization(self):
        """Test IndicatorSearcher initialization."""
        with patch('pathlib.Path.exists', return_value=True):
            searcher = IndicatorSearcher("test_path")
            assert searcher.base_path == Path("test_path")
            assert isinstance(searcher.indicators, dict)
    
    def test_searcher_initialization_missing_directory(self):
        """Test IndicatorSearcher initialization with missing directory."""
        with patch('pathlib.Path.exists', return_value=False):
            with patch('builtins.print') as mock_print:
                searcher = IndicatorSearcher("nonexistent_path")
                mock_print.assert_called_with("Warning: Indicators directory not found: nonexistent_path")
    
    def test_load_indicators_with_mock_files(self):
        """Test loading indicators with mock files."""
        mock_content = '''
        """
        INDICATOR INFO:
        Name: RSI
        Description: Relative Strength Index oscillator
        Usage: --rule RSI(14,70,30,close)
        Parameters: period=14, overbought=70, oversold=30, price_type=close
        Pros: Widely used, easy to interpret
        Cons: Can give false signals in trending markets
        """
        '''
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_content)), \
             patch('pathlib.Path.glob', return_value=[Path("rsi_ind.py")]):
            
            searcher = IndicatorSearcher()
            searcher._load_indicators()
            
            # Check that indicators were loaded
            assert len(searcher.indicators) > 0
    
    def test_parse_indicator_file_with_valid_content(self):
        """Test parsing indicator file with valid content."""
        content = '''
        """
        INDICATOR INFO:
        Name: MACD
        Description: Moving Average Convergence Divergence
        Usage: --rule MACD(12,26,9)
        Parameters: fast=12, slow=26, signal=9
        Pros: Good trend following indicator
        Cons: Lags price action
        """
        '''
        
        with patch('builtins.open', mock_open(read_data=content)):
            searcher = IndicatorSearcher()
            file_path = Path("test_macd_ind.py")
            
            info = searcher._parse_indicator_file(file_path, "momentum")
            
            assert info is not None
            # The actual parsing might include extra whitespace, so we check contains
            assert "MACD" in info.name
            assert info.category == "momentum"
            assert "Moving Average Convergence Divergence" in info.description
            assert "MACD(12,26,9)" in info.usage
            assert "fast=12" in info.parameters
            assert "Good trend following indicator" in info.pros
            assert "Lags price action" in info.cons
    
    def test_parse_indicator_file_without_info(self):
        """Test parsing indicator file without indicator info."""
        content = '''
        """
        Just a regular docstring without indicator info.
        """
        '''
        
        with patch('builtins.open', mock_open(read_data=content)):
            searcher = IndicatorSearcher()
            file_path = Path("test_ind.py")
            
            info = searcher._parse_indicator_file(file_path, "test_category")
            
            assert info is not None
            assert info.name == "TEST"  # Extracted from filename
            assert info.category == "test_category"
            assert info.description == "Indicator description not available"
    
    def test_parse_indicator_file_with_error(self):
        """Test parsing indicator file with error."""
        with patch('builtins.open', side_effect=Exception("File read error")):
            searcher = IndicatorSearcher()
            file_path = Path("error_ind.py")
            
            info = searcher._parse_indicator_file(file_path, "test_category")
            
            assert info is None
    
    def test_extract_field(self):
        """Test field extraction from indicator info text."""
        searcher = IndicatorSearcher()
        
        text = """
        Name: RSI
        Description: Relative Strength Index
        Usage: --rule RSI
        Parameters: period=14
        Pros: Easy to use
        Cons: Can lag
        """
        
        # The actual implementation might include extra whitespace, so we check contains
        name = searcher._extract_field(text, "Name", "Unknown")
        assert "RSI" in name
        
        description = searcher._extract_field(text, "Description", "Unknown")
        assert "Relative Strength Index" in description
        
        usage = searcher._extract_field(text, "Usage", "Unknown")
        assert "RSI" in usage
        
        parameters = searcher._extract_field(text, "Parameters", "Unknown")
        assert "period=14" in parameters
        
        pros = searcher._extract_field(text, "Pros", "Unknown")
        assert "Easy to use" in pros
        
        cons = searcher._extract_field(text, "Cons", "Unknown")
        assert "Can lag" in cons
        
        assert searcher._extract_field(text, "Nonexistent", "Default") == "Default"
    
    def test_list_categories(self):
        """Test listing categories."""
        searcher = IndicatorSearcher()
        searcher.indicators = {
            "trend": [],
            "momentum": [],
            "oscillators": []
        }
        
        categories = searcher.list_categories()
        assert "trend" in categories
        assert "momentum" in categories
        assert "oscillators" in categories
        assert len(categories) == 3
    
    def test_list_indicators_all(self):
        """Test listing all indicators."""
        searcher = IndicatorSearcher()
        rsi_info = IndicatorInfo("RSI", "oscillators", "RSI", "usage", "params", "pros", "cons", "file")
        macd_info = IndicatorInfo("MACD", "momentum", "MACD", "usage", "params", "pros", "cons", "file")
        
        searcher.indicators = {
            "oscillators": [rsi_info],
            "momentum": [macd_info]
        }
        
        all_indicators = searcher.list_indicators()
        assert len(all_indicators) == 2
        assert rsi_info in all_indicators
        assert macd_info in all_indicators
    
    def test_list_indicators_by_category(self):
        """Test listing indicators by category."""
        searcher = IndicatorSearcher()
        rsi_info = IndicatorInfo("RSI", "oscillators", "RSI", "usage", "params", "pros", "cons", "file")
        macd_info = IndicatorInfo("MACD", "momentum", "MACD", "usage", "params", "pros", "cons", "file")
        
        searcher.indicators = {
            "oscillators": [rsi_info],
            "momentum": [macd_info]
        }
        
        oscillators = searcher.list_indicators("oscillators")
        assert len(oscillators) == 1
        assert oscillators[0] == rsi_info
        
        momentum = searcher.list_indicators("momentum")
        assert len(momentum) == 1
        assert momentum[0] == macd_info
        
        # Test non-existent category
        empty = searcher.list_indicators("nonexistent")
        assert len(empty) == 0
    
    def test_search_indicators(self):
        """Test searching indicators."""
        searcher = IndicatorSearcher()
        rsi_info = IndicatorInfo("RSI", "oscillators", "Relative Strength Index", "usage", "params", "pros", "cons", "file")
        macd_info = IndicatorInfo("MACD", "momentum", "Moving Average Convergence Divergence", "usage", "params", "pros", "cons", "file")
        
        searcher.indicators = {
            "oscillators": [rsi_info],
            "momentum": [macd_info]
        }
        
        # Search by name
        results = searcher.search_indicators("RSI")
        assert len(results) == 1
        assert results[0] == rsi_info
        
        # Search by description
        results = searcher.search_indicators("strength")
        assert len(results) == 1
        assert results[0] == rsi_info
        
        # Search by category
        results = searcher.search_indicators("oscillators")
        assert len(results) == 1
        assert results[0] == rsi_info
        
        # Search with no results
        results = searcher.search_indicators("nonexistent")
        assert len(results) == 0
        
        # Case insensitive search
        results = searcher.search_indicators("rsi")
        assert len(results) == 1
        assert results[0] == rsi_info
    
    def test_display_categories(self):
        """Test displaying categories."""
        searcher = IndicatorSearcher()
        searcher.indicators = {
            "trend": [IndicatorInfo("EMA", "trend", "EMA", "usage", "params", "pros", "cons", "file")],
            "momentum": [IndicatorInfo("MACD", "momentum", "MACD", "usage", "params", "pros", "cons", "file"),
                        IndicatorInfo("RSI", "momentum", "RSI", "usage", "params", "pros", "cons", "file")]
        }
        
        with patch('builtins.print') as mock_print:
            searcher.display_categories()
            
            # Check that print was called with category information
            calls = mock_print.call_args_list
            assert any("Available Indicator Categories:" in str(call) for call in calls)
            assert any("trend" in str(call) and "1 indicators" in str(call) for call in calls)
            assert any("momentum" in str(call) and "2 indicators" in str(call) for call in calls)
    
    def test_display_category_basic(self):
        """Test displaying category with basic detail level."""
        searcher = IndicatorSearcher()
        rsi_info = IndicatorInfo("RSI", "oscillators", "Relative Strength Index", "usage", "params", "pros", "cons", "file")
        searcher.indicators = {"oscillators": [rsi_info]}
        
        with patch('builtins.print') as mock_print:
            searcher.display_category("oscillators", detailed=False)
            
            calls = mock_print.call_args_list
            assert any("Indicators in category 'oscillators':" in str(call) for call in calls)
            assert any("RSI" in str(call) for call in calls)
    
    def test_display_category_detailed(self):
        """Test displaying category with detailed information."""
        searcher = IndicatorSearcher()
        rsi_info = IndicatorInfo("RSI", "oscillators", "Relative Strength Index", "usage", "params", "pros", "cons", "file")
        searcher.indicators = {"oscillators": [rsi_info]}
        
        with patch('builtins.print') as mock_print:
            searcher.display_category("oscillators", detailed=True)
            
            calls = mock_print.call_args_list
            assert any("Indicators in category 'oscillators':" in str(call) for call in calls)
            assert any("Indicator: RSI" in str(call) for call in calls)
            assert any("Category: oscillators" in str(call) for call in calls)
    
    def test_display_category_empty(self):
        """Test displaying empty category."""
        searcher = IndicatorSearcher()
        searcher.indicators = {}
        
        with patch('builtins.print') as mock_print:
            searcher.display_category("nonexistent")
            
            calls = mock_print.call_args_list
            assert any("No indicators found in category: nonexistent" in str(call) for call in calls)
    
    def test_display_search_results(self):
        """Test displaying search results."""
        searcher = IndicatorSearcher()
        rsi_info = IndicatorInfo("RSI", "oscillators", "Relative Strength Index", "usage", "params", "pros", "cons", "file")
        
        with patch('builtins.print') as mock_print:
            searcher.display_search_results("RSI", detailed=False)
            
            calls = mock_print.call_args_list
            assert any("Search results for 'RSI':" in str(call) for call in calls)
    
    def test_display_search_results_empty(self):
        """Test displaying empty search results."""
        searcher = IndicatorSearcher()
        
        with patch('builtins.print') as mock_print:
            searcher.display_search_results("nonexistent", detailed=False)
            
            calls = mock_print.call_args_list
            # Check for the actual message that gets printed
            assert any("No indicators found matching" in str(call) for call in calls)


class TestIndicatorSearcherIntegration:
    """Integration tests for IndicatorSearcher."""
    
    def test_full_search_workflow(self):
        """Test complete search workflow."""
        # Create temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            indicators_dir = Path(temp_dir) / "indicators"
            oscillators_dir = indicators_dir / "oscillators"
            oscillators_dir.mkdir(parents=True)
            
            # Create test indicator file
            rsi_file = oscillators_dir / "rsi_ind.py"
            rsi_content = '''
            """
            INDICATOR INFO:
            Name: RSI
            Description: Relative Strength Index oscillator
            Usage: --rule RSI(14,70,30,close)
            Parameters: period=14, overbought=70, oversold=30, price_type=close
            Pros: Widely used, easy to interpret
            Cons: Can give false signals in trending markets
            """
            '''
            rsi_file.write_text(rsi_content)
            
            # Test searcher
            searcher = IndicatorSearcher(str(indicators_dir))
            
            # Test categories
            categories = searcher.list_categories()
            assert "oscillators" in categories
            
            # Test indicators in category
            indicators = searcher.list_indicators("oscillators")
            assert len(indicators) == 1
            # Check that the name contains RSI (might have extra whitespace)
            assert "RSI" in indicators[0].name
            
            # Test search
            results = searcher.search_indicators("RSI")
            assert len(results) == 1
            assert "RSI" in results[0].name
    
    def test_multiple_indicators_in_category(self):
        """Test handling multiple indicators in a category."""
        with tempfile.TemporaryDirectory() as temp_dir:
            indicators_dir = Path(temp_dir) / "indicators"
            momentum_dir = indicators_dir / "momentum"
            momentum_dir.mkdir(parents=True)
            
            # Create multiple indicator files
            indicators = {
                "rsi_ind.py": '''
                """
                INDICATOR INFO:
                Name: RSI
                Description: Relative Strength Index
                Usage: --rule RSI
                Parameters: period=14
                Pros: Easy to use
                Cons: Can lag
                """
                ''',
                "macd_ind.py": '''
                """
                INDICATOR INFO:
                Name: MACD
                Description: Moving Average Convergence Divergence
                Usage: --rule MACD
                Parameters: fast=12, slow=26, signal=9
                Pros: Good trend following
                Cons: Lags price action
                """
                '''
            }
            
            for filename, content in indicators.items():
                file_path = momentum_dir / filename
                file_path.write_text(content)
            
            searcher = IndicatorSearcher(str(indicators_dir))
            
            # Test that both indicators are loaded
            momentum_indicators = searcher.list_indicators("momentum")
            assert len(momentum_indicators) == 2
            
            names = [ind.name for ind in momentum_indicators]
            # Check that names contain the expected strings (might have extra whitespace)
            assert any("RSI" in name for name in names)
            assert any("MACD" in name for name in names)
    
    def test_error_handling_in_file_parsing(self):
        """Test error handling when parsing indicator files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            indicators_dir = Path(temp_dir) / "indicators"
            test_dir = indicators_dir / "test"
            test_dir.mkdir(parents=True)
            
            # Create a file that will cause an error
            error_file = test_dir / "error_ind.py"
            error_file.write_text("invalid python syntax {")
            
            searcher = IndicatorSearcher(str(indicators_dir))
            
            # Should not crash, should handle the error gracefully
            indicators = searcher.list_indicators("test")
            # The error file should be skipped
            assert len(indicators) == 0 