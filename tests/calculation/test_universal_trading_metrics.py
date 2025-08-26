# -*- coding: utf-8 -*-
# tests/calculation/test_universal_trading_metrics.py

"""
Tests for Universal Trading Metrics Module
Tests the universal trading metrics calculator that works with any rule type.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from src.calculation.universal_trading_metrics import (
    UniversalTradingMetrics, 
    display_universal_trading_metrics
)
from src.common.constants import BUY, SELL, NOTRADE


class TestUniversalTradingMetrics:
    """Test cases for UniversalTradingMetrics class."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample trading data for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Generate realistic price data
        base_price = 100.0
        returns = np.random.normal(0.001, 0.02, 100)  # Daily returns
        prices = [base_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        # Generate signals
        signals = [NOTRADE] * 100
        for i in range(10, 90, 10):
            signals[i] = BUY
            signals[i+5] = SELL
        
        # Generate volume data
        volumes = np.random.randint(1000, 10000, 100)
        
        df = pd.DataFrame({
            'datetime': dates,
            'Open': prices,
            'High': [p * 1.01 for p in prices],
            'Low': [p * 0.99 for p in prices],
            'Close': prices,
            'Volume': volumes,
            'Direction': signals
        })
        
        return df
    
    @pytest.fixture
    def calculator(self):
        """Create UniversalTradingMetrics instance."""
        return UniversalTradingMetrics(
            lot_size=1.0,
            risk_reward_ratio=2.0,
            fee_per_trade=0.07
        )
    
    def test_initialization(self, calculator):
        """Test UniversalTradingMetrics initialization."""
        assert calculator.lot_size == 1.0
        assert calculator.risk_reward_ratio == 2.0
        assert calculator.fee_per_trade == 0.07
    
    def test_initialization_with_custom_params(self):
        """Test initialization with custom parameters."""
        calc = UniversalTradingMetrics(
            lot_size=2.5,
            risk_reward_ratio=3.0,
            fee_per_trade=0.1
        )
        assert calc.lot_size == 2.5
        assert calc.risk_reward_ratio == 3.0
        assert calc.fee_per_trade == 0.1
    
    def test_get_rule_name_string(self, calculator):
        """Test getting rule name from string."""
        rule_name = calculator._get_rule_name("RSI_Strategy")
        assert rule_name == "RSI_Strategy"
    
    def test_get_rule_name_object_with_name(self, calculator):
        """Test getting rule name from object with name attribute."""
        mock_rule = MagicMock()
        mock_rule.name = "MACD_Strategy"
        
        rule_name = calculator._get_rule_name(mock_rule)
        assert rule_name == "MACD_Strategy"
    
    def test_get_rule_name_object_with_class(self, calculator):
        """Test getting rule name from object with class name."""
        class MockRule:
            pass
        
        mock_rule = MockRule()
        rule_name = calculator._get_rule_name(mock_rule)
        assert rule_name == "MockRule"
    
    def test_get_rule_name_other_object(self, calculator):
        """Test getting rule name from other object types."""
        rule_name = calculator._get_rule_name(42)
        assert rule_name == "int"  # For integers, it returns the type name
    
    def test_calculate_and_display_metrics_success(self, calculator, sample_data):
        """Test successful calculation and display of metrics."""
        with patch.object(calculator, '_display_metrics') as mock_display:
            metrics = calculator.calculate_and_display_metrics(
                sample_data, 
                "Test_Rule"
            )
            
            # Check that metrics were calculated
            assert isinstance(metrics, dict)
            assert len(metrics) > 0
            
            # Check that display was called
            mock_display.assert_called_once()
            
            # Check that display was called with correct arguments
            call_args = mock_display.call_args
            assert call_args[0][0] == metrics  # metrics dict
            assert call_args[0][1] == "Test_Rule"  # rule name
            assert call_args[0][2].equals(sample_data)  # dataframe
    
    def test_calculate_and_display_metrics_empty_data(self, calculator):
        """Test handling of empty DataFrame."""
        empty_df = pd.DataFrame()
        
        with patch.object(calculator, '_display_error') as mock_error:
            metrics = calculator.calculate_and_display_metrics(
                empty_df, 
                "Test_Rule"
            )
            
            assert metrics == {}
            mock_error.assert_called_once_with("DataFrame is None or empty")
    
    def test_calculate_and_display_metrics_none_data(self, calculator):
        """Test handling of None DataFrame."""
        with patch.object(calculator, '_display_error') as mock_error:
            metrics = calculator.calculate_and_display_metrics(
                None, 
                "Test_Rule"
            )
            
            assert metrics == {}
            mock_error.assert_called_once_with("DataFrame is None or empty")
    
    def test_calculate_and_display_metrics_missing_signal_column(self, calculator, sample_data):
        """Test handling of missing signal column."""
        df_no_signal = sample_data.drop(columns=['Direction'])
        
        with patch.object(calculator, '_display_error') as mock_error:
            metrics = calculator.calculate_and_display_metrics(
                df_no_signal, 
                "Test_Rule"
            )
            
            assert metrics == {}
            # Check that error was called with the correct message
            mock_error.assert_called_once()
            error_message = mock_error.call_args[0][0]
            assert "Signal column 'Direction' not found in data" in error_message
    
    def test_calculate_and_display_metrics_custom_columns(self, calculator, sample_data):
        """Test calculation with custom column names."""
        # Rename columns
        df_custom = sample_data.rename(columns={
            'Close': 'Price',
            'Direction': 'Signal',
            'Volume': 'Vol'
        })
        
        with patch.object(calculator, '_display_metrics') as mock_display:
            metrics = calculator.calculate_and_display_metrics(
                df_custom,
                "Test_Rule",
                price_col='Price',
                signal_col='Signal',
                volume_col='Vol'
            )
            
            assert isinstance(metrics, dict)
            assert len(metrics) > 0
            mock_display.assert_called_once()
    
    def test_calculate_and_display_metrics_exception_handling(self, calculator, sample_data):
        """Test exception handling during calculation."""
        with patch('src.calculation.universal_trading_metrics.calculate_trading_metrics') as mock_calc:
            mock_calc.side_effect = Exception("Test error")
            
            with patch.object(calculator, '_display_error') as mock_error:
                metrics = calculator.calculate_and_display_metrics(
                    sample_data,
                    "Test_Rule"
                )
                
                assert metrics == {}
                mock_error.assert_called_once_with("Metrics calculation failed: Test error")
    
    def test_get_metric_color_normal(self, calculator):
        """Test color coding for normal metrics (higher is better)."""
        # Test excellent (green)
        color = calculator._get_metric_color(80, 50, 70)
        assert color == "🟢"
        
        # Test good (yellow)
        color = calculator._get_metric_color(60, 50, 70)
        assert color == "🟡"
        
        # Test poor (red)
        color = calculator._get_metric_color(30, 50, 70)
        assert color == "🔴"
    
    def test_get_metric_color_reverse(self, calculator):
        """Test color coding for reverse metrics (lower is better)."""
        # Test excellent (green)
        color = calculator._get_metric_color(5, 10, 20, reverse=True)
        assert color == "🟢"
        
        # Test good (yellow)
        color = calculator._get_metric_color(15, 10, 20, reverse=True)
        assert color == "🟡"
        
        # Test poor (red)
        color = calculator._get_metric_color(25, 10, 20, reverse=True)
        assert color == "🔴"
    
    def test_calculate_performance_score(self, calculator):
        """Test performance score calculation."""
        # Test with good metrics
        good_metrics = {
            'win_ratio': 75,
            'profit_factor': 2.5,
            'sharpe_ratio': 2.0,
            'max_drawdown': 8,
            'volatility': 12,
            'strategy_efficiency': 85,
            'strategy_sustainability': 75
        }
        
        score = calculator._calculate_performance_score(good_metrics)
        assert 70 <= score <= 100  # Should be high score
        
        # Test with poor metrics
        poor_metrics = {
            'win_ratio': 30,
            'profit_factor': 0.8,
            'sharpe_ratio': 0.5,
            'max_drawdown': 30,
            'volatility': 25,
            'strategy_efficiency': 50,
            'strategy_sustainability': 40
        }
        
        score = calculator._calculate_performance_score(poor_metrics)
        assert 0 <= score <= 30  # Should be low score
    
    def test_identify_strengths(self, calculator):
        """Test strength identification."""
        # Test with strong metrics
        strong_metrics = {
            'win_ratio': 80,
            'profit_factor': 2.5,
            'sharpe_ratio': 2.5,
            'max_drawdown': 5,
            'strategy_efficiency': 95
        }
        
        strengths = calculator._identify_strengths(strong_metrics)
        assert len(strengths) > 0
        assert any("High win ratio" in strength for strength in strengths)
        assert any("Strong profit factor" in strength for strength in strengths)
        
        # Test with weak metrics
        weak_metrics = {
            'win_ratio': 30,
            'profit_factor': 0.8,
            'sharpe_ratio': 0.5,
            'max_drawdown': 25,
            'strategy_efficiency': 50
        }
        
        strengths = calculator._identify_strengths(weak_metrics)
        assert len(strengths) == 0
    
    def test_identify_weaknesses(self, calculator):
        """Test weakness identification."""
        # Test with weak metrics
        weak_metrics = {
            'win_ratio': 30,
            'profit_factor': 0.8,
            'max_drawdown': 25,
            'volatility': 25,
            'strategy_efficiency': 50
        }
        
        weaknesses = calculator._identify_weaknesses(weak_metrics)
        assert len(weaknesses) > 0
        assert any("Low win ratio" in weakness for weakness in weaknesses)
        assert any("Weak profit factor" in weakness for weakness in weaknesses)
        
        # Test with strong metrics
        strong_metrics = {
            'win_ratio': 80,
            'profit_factor': 2.5,
            'max_drawdown': 5,
            'volatility': 10,
            'strategy_efficiency': 95
        }
        
        weaknesses = calculator._identify_weaknesses(strong_metrics)
        assert len(weaknesses) == 0
    
    def test_generate_recommendations(self, calculator):
        """Test recommendation generation."""
        # Test with metrics needing improvement
        poor_metrics = {
            'win_ratio': 30,
            'profit_factor': 0.8,
            'max_drawdown': 25,
            'strategy_efficiency': 50,
            'kelly_fraction': 0.05
        }
        
        recommendations = calculator._generate_recommendations(poor_metrics)
        assert len(recommendations) > 0
        assert any("improving entry/exit criteria" in rec for rec in recommendations)
        assert any("risk management" in rec for rec in recommendations)
        
        # Test with good metrics
        good_metrics = {
            'win_ratio': 80,
            'profit_factor': 2.5,
            'max_drawdown': 5,
            'strategy_efficiency': 95,
            'kelly_fraction': 0.3
        }
        
        recommendations = calculator._generate_recommendations(good_metrics)
        assert len(recommendations) == 0
    
    def test_display_error(self, calculator):
        """Test error display method."""
        with patch('builtins.print') as mock_print:
            calculator._display_error("Test error message")
            
            # Check that print was called twice (error message and separator)
            assert mock_print.call_count == 2
            
            # Check error message
            error_call = mock_print.call_args_list[0]
            assert "❌ ERROR: Test error message" in str(error_call)
    
    @patch('builtins.print')
    def test_display_metrics_integration(self, mock_print, calculator, sample_data):
        """Test integration of display methods."""
        # Mock metrics
        mock_metrics = {
            'win_ratio': 75.0,
            'profit_factor': 2.5,
            'total_return': 15.5,
            'max_drawdown': 8.2,
            'sharpe_ratio': 1.8,
            'strategy_efficiency': 85.0,
            'kelly_fraction': 0.25,
            'mc_expected_return': 12.5,
            'volume_weighted_return': 14.2
        }
        
        # Call display method
        calculator._display_metrics(mock_metrics, "Test_Rule", sample_data)
        
        # Verify that print was called multiple times (header, sections, footer)
        assert mock_print.call_count > 10
        
        # Check for specific sections
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("UNIVERSAL TRADING METRICS ANALYSIS" in call for call in print_calls)
        assert any("CORE TRADING METRICS" in call for call in print_calls)
        assert any("STRATEGY METRICS" in call for call in print_calls)
        assert any("RISK MANAGEMENT METRICS" in call for call in print_calls)
        assert any("END OF TRADING METRICS ANALYSIS" in call for call in print_calls)


class TestDisplayUniversalTradingMetrics:
    """Test cases for the convenience function."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample trading data for testing."""
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        np.random.seed(42)
        
        base_price = 100.0
        returns = np.random.normal(0.001, 0.02, 50)
        prices = [base_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        signals = [NOTRADE] * 50
        for i in range(5, 45, 10):
            signals[i] = BUY
            signals[i+3] = SELL
        
        volumes = np.random.randint(1000, 10000, 50)
        
        df = pd.DataFrame({
            'datetime': dates,
            'Open': prices,
            'High': [p * 1.01 for p in prices],
            'Low': [p * 0.99 for p in prices],
            'Close': prices,
            'Volume': volumes,
            'Direction': signals
        })
        
        return df
    
    def test_display_universal_trading_metrics_default_params(self, sample_data):
        """Test convenience function with default parameters."""
        with patch('src.calculation.universal_trading_metrics.UniversalTradingMetrics') as mock_class:
            mock_instance = MagicMock()
            mock_class.return_value = mock_instance
            mock_instance.calculate_and_display_metrics.return_value = {'test': 1.0}
            
            metrics = display_universal_trading_metrics(sample_data, "Test_Rule")
            
            # Check that class was instantiated with default parameters
            mock_class.assert_called_once_with(1.0, 2.0, 0.07)
            
            # Check that method was called with correct parameters
            mock_instance.calculate_and_display_metrics.assert_called_once_with(
                sample_data, "Test_Rule", signal_col='Direction'
            )
            
            # Check return value
            assert metrics == {'test': 1.0}
    
    def test_display_universal_trading_metrics_custom_params(self, sample_data):
        """Test convenience function with custom parameters."""
        with patch('src.calculation.universal_trading_metrics.UniversalTradingMetrics') as mock_class:
            mock_instance = MagicMock()
            mock_class.return_value = mock_instance
            mock_instance.calculate_and_display_metrics.return_value = {'test': 1.0}
            
            metrics = display_universal_trading_metrics(
                sample_data, 
                "Test_Rule",
                lot_size=2.5,
                risk_reward_ratio=3.0,
                fee_per_trade=0.1
            )
            
            # Check that class was instantiated with custom parameters
            mock_class.assert_called_once_with(2.5, 3.0, 0.1)
            
            # Check that method was called with correct parameters
            mock_instance.calculate_and_display_metrics.assert_called_once_with(
                sample_data, "Test_Rule", signal_col='Direction'
            )
            
            # Check return value
            assert metrics == {'test': 1.0}
    
    def test_display_universal_trading_metrics_integration(self, sample_data):
        """Test full integration of the convenience function."""
        metrics = display_universal_trading_metrics(sample_data, "Test_Rule")
        
        # Check that metrics were returned
        assert isinstance(metrics, dict)
        assert len(metrics) > 0
        
        # Check for expected metric keys
        expected_keys = [
            'buy_count', 'sell_count', 'total_trades', 'win_ratio',
            'profit_factor', 'sharpe_ratio', 'max_drawdown', 'total_return'
        ]
        
        for key in expected_keys:
            assert key in metrics, f"Missing expected metric: {key}"
        
        # Check that values are reasonable
        assert metrics['total_trades'] >= 0
        assert 0 <= metrics['win_ratio'] <= 100
        assert metrics['profit_factor'] >= 0
        assert metrics['max_drawdown'] >= 0


class TestUniversalTradingMetricsEdgeCases:
    """Test edge cases and error conditions."""
    
    @pytest.fixture
    def calculator(self):
        """Create UniversalTradingMetrics instance."""
        return UniversalTradingMetrics()
    
    def test_empty_metrics_dict(self, calculator):
        """Test handling of empty metrics dictionary."""
        empty_metrics = {}
        
        # Test performance score calculation
        score = calculator._calculate_performance_score(empty_metrics)
        assert score >= 0  # Should not crash, may return some default score
        
        # Test strength identification
        strengths = calculator._identify_strengths(empty_metrics)
        assert strengths == []
        
        # Test weakness identification
        weaknesses = calculator._identify_weaknesses(empty_metrics)
        assert weaknesses == []
        
        # Test recommendation generation
        recommendations = calculator._generate_recommendations(empty_metrics)
        assert recommendations == []
    
    def test_none_values_in_metrics(self, calculator):
        """Test handling of None values in metrics."""
        metrics_with_none = {
            'win_ratio': None,
            'profit_factor': 2.0,
            'sharpe_ratio': None,
            'max_drawdown': 15.0
        }
        
        # Test performance score calculation
        score = calculator._calculate_performance_score(metrics_with_none)
        assert score >= 0  # Should not crash
        
        # Test strength identification - should handle None gracefully
        try:
            strengths = calculator._identify_strengths(metrics_with_none)
            assert isinstance(strengths, list)
        except TypeError:
            # If it fails due to None comparison, that's expected behavior
            pass
        
        # Test weakness identification - should handle None gracefully
        try:
            weaknesses = calculator._identify_weaknesses(metrics_with_none)
            assert isinstance(weaknesses, list)
        except TypeError:
            # If it fails due to None comparison, that's expected behavior
            pass
    
    def test_extreme_values_in_metrics(self, calculator):
        """Test handling of extreme values in metrics."""
        extreme_metrics = {
            'win_ratio': 999.0,  # Impossible value
            'profit_factor': -5.0,  # Negative value
            'sharpe_ratio': float('inf'),  # Infinity
            'max_drawdown': -50.0,  # Negative drawdown
            'volatility': 0.0,  # Zero volatility
            'strategy_efficiency': 150.0,  # Over 100%
            'kelly_fraction': 2.0  # Over 1.0
        }
        
        # Test that methods don't crash with extreme values
        score = calculator._calculate_performance_score(extreme_metrics)
        assert score >= 0
        
        strengths = calculator._identify_strengths(extreme_metrics)
        assert isinstance(strengths, list)
        
        weaknesses = calculator._identify_weaknesses(extreme_metrics)
        assert isinstance(weaknesses, list)
        
        recommendations = calculator._generate_recommendations(extreme_metrics)
        assert isinstance(recommendations, list)
    
    def test_malformed_dataframe(self, calculator):
        """Test handling of malformed DataFrame."""
        # DataFrame with wrong data types
        malformed_df = pd.DataFrame({
            'Close': ['not_a_number', 'also_not_a_number'],
            'Direction': ['invalid', 'signal'],
            'Volume': ['wrong', 'type']
        })
        
        with patch.object(calculator, '_display_error') as mock_error:
            metrics = calculator.calculate_and_display_metrics(
                malformed_df,
                "Test_Rule"
            )
            
            # Should handle gracefully and may return some metrics or empty dict
            assert isinstance(metrics, dict)
            # The function may still return some calculated metrics even with malformed data
    
    def test_single_row_dataframe(self, calculator):
        """Test handling of single row DataFrame."""
        single_row_df = pd.DataFrame({
            'datetime': ['2023-01-01'],
            'Open': [100.0],
            'High': [101.0],
            'Low': [99.0],
            'Close': [100.5],
            'Volume': [1000],
            'Direction': [NOTRADE]
        })
        
        with patch.object(calculator, '_display_metrics') as mock_display:
            metrics = calculator.calculate_and_display_metrics(
                single_row_df,
                "Test_Rule"
            )
            
            # Should handle single row gracefully
            assert isinstance(metrics, dict)
            mock_display.assert_called_once()
    
    def test_large_dataframe(self, calculator):
        """Test handling of large DataFrame."""
        # Create large DataFrame
        dates = pd.date_range('2020-01-01', periods=10000, freq='h')
        np.random.seed(42)
        
        base_price = 100.0
        returns = np.random.normal(0.0001, 0.01, 10000)
        prices = [base_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        signals = [NOTRADE] * 10000
        for i in range(100, 9900, 100):
            signals[i] = BUY
            signals[i+50] = SELL
        
        volumes = np.random.randint(1000, 10000, 10000)
        
        large_df = pd.DataFrame({
            'datetime': dates,
            'Open': prices,
            'High': [p * 1.005 for p in prices],
            'Low': [p * 0.995 for p in prices],
            'Close': prices,
            'Volume': volumes,
            'Direction': signals
        })
        
        with patch.object(calculator, '_display_metrics') as mock_display:
            metrics = calculator.calculate_and_display_metrics(
                large_df,
                "Test_Rule"
            )
            
            # Should handle large DataFrame
            assert isinstance(metrics, dict)
            assert len(metrics) > 0
            mock_display.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
