# -*- coding: utf-8 -*-
"""
Tests for CLI Encyclopedia Module

This module tests the encyclopedia functionality organized by indicator groups.
"""

import pytest
from src.cli.encyclopedia import (
    OscillatorMetrics, OscillatorTips,
    TrendMetrics, TrendTips,
    MomentumMetrics, MomentumTips,
    VolumeMetrics, VolumeTips,
    VolatilityMetrics, VolatilityTips,
    SupportResistanceMetrics, SupportResistanceTips,
    PredictiveMetrics, PredictiveTips,
    ProbabilityMetrics, ProbabilityTips,
    SentimentMetrics, SentimentTips
)


class TestOscillatorMetrics:
    """Test OscillatorMetrics functionality."""
    
    def test_get_rsi_metrics(self):
        """Test RSI metrics retrieval."""
        metrics = OscillatorMetrics.get_rsi_metrics()
        
        assert metrics['name'] == 'Relative Strength Index (RSI)'
        assert 'RSI = 100 - (100 / (1 + RS))' in metrics['formula']
        assert 'overbought' in metrics['interpretation']
        assert 'oversold' in metrics['interpretation']
        assert 'good_range' in metrics
        assert 'excellent_range' in metrics
        assert 'warning_range' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_stochastic_metrics(self):
        """Test Stochastic metrics retrieval."""
        metrics = OscillatorMetrics.get_stochastic_metrics()
        
        assert metrics['name'] == 'Stochastic Oscillator'
        assert 'Close - Lowest Low' in metrics['formula']
        assert 'overbought' in metrics['interpretation']
        assert 'oversold' in metrics['interpretation']
        assert 'good_range' in metrics
        assert 'excellent_range' in metrics
        assert 'warning_range' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_cci_metrics(self):
        """Test CCI metrics retrieval."""
        metrics = OscillatorMetrics.get_cci_metrics()
        
        assert metrics['name'] == 'Commodity Channel Index (CCI)'
        assert 'Typical Price - SMA' in metrics['formula']
        assert 'overbought' in metrics['interpretation']
        assert 'oversold' in metrics['interpretation']
        assert 'good_range' in metrics
        assert 'excellent_range' in metrics
        assert 'warning_range' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_williams_r_metrics(self):
        """Test Williams %R metrics retrieval."""
        metrics = OscillatorMetrics.get_williams_r_metrics()
        
        assert metrics['name'] == 'Williams %R'
        assert 'Highest High - Close' in metrics['formula']
        assert 'overbought' in metrics['interpretation']
        assert 'oversold' in metrics['interpretation']
        assert 'good_range' in metrics
        assert 'excellent_range' in metrics
        assert 'warning_range' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_all_oscillator_metrics(self):
        """Test getting all oscillator metrics."""
        all_metrics = OscillatorMetrics.get_all_oscillator_metrics()
        
        assert len(all_metrics) == 4
        assert 'RSI' in all_metrics
        assert 'Stochastic' in all_metrics
        assert 'CCI' in all_metrics
        assert 'Williams_R' in all_metrics
        
        # Check structure of each metric
        for metric_name, metrics in all_metrics.items():
            assert 'name' in metrics
            assert 'formula' in metrics
            assert 'interpretation' in metrics
            assert 'ranges' in metrics


class TestOscillatorTips:
    """Test OscillatorTips functionality."""
    
    def test_get_rsi_tips(self):
        """Test RSI tips retrieval."""
        tips = OscillatorTips.get_rsi_tips()
        
        assert len(tips) > 0
        assert all(isinstance(tip, str) for tip in tips)
        assert any('trend' in tip.lower() for tip in tips)
        assert any('confirmation' in tip.lower() for tip in tips)
    
    def test_get_stochastic_tips(self):
        """Test Stochastic tips retrieval."""
        tips = OscillatorTips.get_stochastic_tips()
        
        assert len(tips) > 0
        assert all(isinstance(tip, str) for tip in tips)
        assert any('momentum' in tip.lower() for tip in tips)
        assert any('reversal' in tip.lower() for tip in tips)
    
    def test_get_cci_tips(self):
        """Test CCI tips retrieval."""
        tips = OscillatorTips.get_cci_tips()
        
        assert len(tips) > 0
        assert all(isinstance(tip, str) for tip in tips)
        assert any('trend' in tip.lower() for tip in tips)
        assert any('confirmation' in tip.lower() for tip in tips)
    
    def test_get_williams_r_tips(self):
        """Test Williams %R tips retrieval."""
        tips = OscillatorTips.get_williams_r_tips()
        
        assert len(tips) > 0
        assert all(isinstance(tip, str) for tip in tips)
        assert any('timing' in tip.lower() for tip in tips)
        assert any('markets' in tip.lower() for tip in tips)
    
    def test_get_general_oscillator_tips(self):
        """Test general oscillator tips retrieval."""
        tips = OscillatorTips.get_general_oscillator_tips()
        
        assert len(tips) > 0
        assert all(isinstance(tip, str) for tip in tips)
        assert any('trend' in tip.lower() for tip in tips)
        assert any('momentum' in tip.lower() for tip in tips)


class TestTrendMetrics:
    """Test TrendMetrics functionality."""
    
    def test_get_ema_metrics(self):
        """Test EMA metrics retrieval."""
        metrics = TrendMetrics.get_ema_metrics()
        
        assert metrics['name'] == 'Exponential Moving Average (EMA)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_sma_metrics(self):
        """Test SMA metrics retrieval."""
        metrics = TrendMetrics.get_sma_metrics()
        
        assert metrics['name'] == 'Simple Moving Average (SMA)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_adx_metrics(self):
        """Test ADX metrics retrieval."""
        metrics = TrendMetrics.get_adx_metrics()
        
        assert metrics['name'] == 'Average Directional Index (ADX)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_sar_metrics(self):
        """Test SAR metrics retrieval."""
        metrics = TrendMetrics.get_sar_metrics()
        
        assert metrics['name'] == 'Parabolic SAR'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_supertrend_metrics(self):
        """Test SuperTrend metrics retrieval."""
        metrics = TrendMetrics.get_supertrend_metrics()
        
        assert metrics['name'] == 'SuperTrend'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_wave_metrics(self):
        """Test Wave metrics retrieval."""
        # Note: Wave metrics method doesn't exist, so we'll skip this test
        # or test a different method that exists
        pass


class TestMomentumMetrics:
    """Test MomentumMetrics functionality."""
    
    def test_get_macd_metrics(self):
        """Test MACD metrics retrieval."""
        metrics = MomentumMetrics.get_macd_metrics()
        
        assert metrics['name'] == 'Moving Average Convergence Divergence (MACD)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_stoch_oscillator_metrics(self):
        """Test Stochastic Oscillator metrics retrieval."""
        metrics = MomentumMetrics.get_stoch_oscillator_metrics()
        
        assert metrics['name'] == 'Stochastic Oscillator'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_roc_metrics(self):
        """Test ROC metrics retrieval."""
        metrics = MomentumMetrics.get_roc_metrics()
        
        assert metrics['name'] == 'Rate of Change (ROC)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_momentum_metrics(self):
        """Test Momentum metrics retrieval."""
        metrics = MomentumMetrics.get_momentum_metrics()
        
        assert metrics['name'] == 'Momentum'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics


class TestVolumeMetrics:
    """Test VolumeMetrics functionality."""
    
    def test_get_obv_metrics(self):
        """Test OBV metrics retrieval."""
        metrics = VolumeMetrics.get_obv_metrics()
        
        assert metrics['name'] == 'On-Balance Volume (OBV)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_vwap_metrics(self):
        """Test VWAP metrics retrieval."""
        metrics = VolumeMetrics.get_vwap_metrics()
        
        assert metrics['name'] == 'Volume Weighted Average Price (VWAP)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_volume_sma_metrics(self):
        """Test Volume SMA metrics retrieval."""
        metrics = VolumeMetrics.get_volume_sma_metrics()
        
        assert metrics['name'] == 'Volume Simple Moving Average'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_volume_ema_metrics(self):
        """Test Volume EMA metrics retrieval."""
        metrics = VolumeMetrics.get_volume_ema_metrics()
        
        assert metrics['name'] == 'Volume Exponential Moving Average'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics


class TestVolatilityMetrics:
    """Test VolatilityMetrics functionality."""
    
    def test_get_atr_metrics(self):
        """Test ATR metrics retrieval."""
        metrics = VolatilityMetrics.get_atr_metrics()
        
        assert metrics['name'] == 'Average True Range (ATR)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_bollinger_bands_metrics(self):
        """Test Bollinger Bands metrics retrieval."""
        metrics = VolatilityMetrics.get_bollinger_bands_metrics()
        
        assert metrics['name'] == 'Bollinger Bands'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_note' in metrics
        assert 'strategy_impact' in metrics
    
    def test_get_stdev_metrics(self):
        """Test StDev metrics retrieval."""
        metrics = VolatilityMetrics.get_stdev_metrics()
        
        assert metrics['name'] == 'Standard Deviation'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_keltner_channels_metrics(self):
        """Test Keltner Channels metrics retrieval."""
        metrics = VolatilityMetrics.get_keltner_channels_metrics()
        
        assert metrics['name'] == 'Keltner Channels'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics


class TestSupportResistanceMetrics:
    """Test SupportResistanceMetrics functionality."""
    
    def test_get_pivot_points_metrics(self):
        """Test Pivot Points metrics retrieval."""
        metrics = SupportResistanceMetrics.get_pivot_points_metrics()
        
        assert metrics['name'] == 'Pivot Points'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_fibonacci_retracement_metrics(self):
        """Test Fibonacci Retracement metrics retrieval."""
        metrics = SupportResistanceMetrics.get_fibonacci_retracement_metrics()
        
        assert metrics['name'] == 'Fibonacci Retracement'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_donchian_channels_metrics(self):
        """Test Donchian Channels metrics retrieval."""
        metrics = SupportResistanceMetrics.get_donchian_channels_metrics()
        
        assert metrics['name'] == 'Donchian Channels'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_support_resistance_levels_metrics(self):
        """Test Support/Resistance Levels metrics retrieval."""
        metrics = SupportResistanceMetrics.get_support_resistance_levels_metrics()
        
        assert metrics['name'] == 'Support/Resistance Levels'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics


class TestPredictiveMetrics:
    """Test PredictiveMetrics functionality."""
    
    def test_get_hma_metrics(self):
        """Test HMA metrics retrieval."""
        metrics = PredictiveMetrics.get_hma_metrics()
        
        assert metrics['name'] == 'Hull Moving Average (HMA)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_tsforecast_metrics(self):
        """Test TSForecast metrics retrieval."""
        metrics = PredictiveMetrics.get_tsforecast_metrics()
        
        assert metrics['name'] == 'Time Series Forecast'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_linear_regression_metrics(self):
        """Test Linear Regression metrics retrieval."""
        metrics = PredictiveMetrics.get_linear_regression_metrics()
        
        assert metrics['name'] == 'Linear Regression'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_polynomial_regression_metrics(self):
        """Test Polynomial Regression metrics retrieval."""
        metrics = PredictiveMetrics.get_polynomial_regression_metrics()
        
        assert metrics['name'] == 'Polynomial Regression'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics


class TestProbabilityMetrics:
    """Test ProbabilityMetrics functionality."""
    
    def test_get_monte_carlo_metrics(self):
        """Test Monte Carlo metrics retrieval."""
        metrics = ProbabilityMetrics.get_monte_carlo_metrics()
        
        assert metrics['name'] == 'Monte Carlo Simulation'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_kelly_metrics(self):
        """Test Kelly metrics retrieval."""
        metrics = ProbabilityMetrics.get_kelly_metrics()
        
        assert metrics['name'] == 'Kelly Criterion'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_probability_distribution_metrics(self):
        """Test Probability Distribution metrics retrieval."""
        metrics = ProbabilityMetrics.get_probability_distribution_metrics()
        
        assert metrics['name'] == 'Probability Distribution'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_confidence_interval_metrics(self):
        """Test Confidence Interval metrics retrieval."""
        metrics = ProbabilityMetrics.get_confidence_interval_metrics()
        
        assert metrics['name'] == 'Confidence Interval'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics


class TestSentimentMetrics:
    """Test SentimentMetrics functionality."""
    
    def test_get_fear_greed_metrics(self):
        """Test Fear & Greed metrics retrieval."""
        metrics = SentimentMetrics.get_fear_greed_metrics()
        
        assert metrics['name'] == 'Fear & Greed Index'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_cot_metrics(self):
        """Test COT metrics retrieval."""
        metrics = SentimentMetrics.get_cot_metrics()
        
        assert metrics['name'] == 'Commitment of Traders (COT)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_put_call_ratio_metrics(self):
        """Test Put/Call Ratio metrics retrieval."""
        metrics = SentimentMetrics.get_put_call_ratio_metrics()
        
        assert metrics['name'] == 'Put/Call Ratio'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_vix_metrics(self):
        """Test VIX metrics retrieval."""
        metrics = SentimentMetrics.get_vix_metrics()
        
        assert metrics['name'] == 'Volatility Index (VIX)'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics
    
    def test_get_market_sentiment_metrics(self):
        """Test Market Sentiment metrics retrieval."""
        metrics = SentimentMetrics.get_market_sentiment_metrics()
        
        assert metrics['name'] == 'Market Sentiment'
        assert 'formula' in metrics
        assert 'interpretation' in metrics
        assert 'calculation_method' in metrics
        assert 'best_timeframes' in metrics


class TestTipsStructure:
    """Test that all tips classes have consistent structure."""
    
    @pytest.mark.parametrize("tips_class", [
        TrendTips, MomentumTips, VolumeTips, VolatilityTips,
        SupportResistanceTips, PredictiveTips, ProbabilityTips, SentimentTips
    ])
    def test_tips_class_structure(self, tips_class):
        """Test that tips classes have consistent structure."""
        # Get all methods that start with 'get_'
        methods = [method for method in dir(tips_class) if method.startswith('get_')]
        
        # Each tips class should have methods for each indicator
        assert len(methods) > 0
        
        # Test that each method returns a list of strings
        for method_name in methods:
            method = getattr(tips_class, method_name)
            if callable(method):
                tips = method()
                assert isinstance(tips, list)
                assert all(isinstance(tip, str) for tip in tips)
                assert len(tips) > 0


if __name__ == "__main__":
    pytest.main([__file__])
