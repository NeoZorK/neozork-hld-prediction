import pytest
import pandas as pd
import numpy as np
from src.calculation.trading_metrics import TradingMetricsCalculator, calculate_trading_metrics


class TestTradingMetricsCalculator:
    """Test cases for TradingMetricsCalculator class."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample data with trading signals
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Generate realistic price data
        base_price = 100.0
        returns = np.random.normal(0.001, 0.02, 100)  # Daily returns
        prices = [base_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        # Create signals (0=hold, 1=buy, 2=sell)
        signals = np.random.choice([0, 1, 2], 100, p=[0.7, 0.15, 0.15])
        
        self.test_df = pd.DataFrame({
            'Open': prices,
            'High': [p * 1.01 for p in prices],
            'Low': [p * 0.99 for p in prices],
            'Close': prices,
            'Volume': np.random.randint(1000, 10000, 100),
            'Direction': signals
        }, index=dates)
        
        self.calculator = TradingMetricsCalculator()
    
    def test_calculate_all_metrics_with_strategy(self):
        """Test calculation of all metrics with strategy parameters."""
        metrics = self.calculator.calculate_all_metrics(
            self.test_df, 
            lot_size=1.5, 
            risk_reward_ratio=2.5, 
            fee_per_trade=0.08
        )
        
        # Check basic metrics
        assert 'buy_count' in metrics
        assert 'sell_count' in metrics
        assert 'total_trades' in metrics
        assert 'win_ratio' in metrics
        assert 'profit_factor' in metrics
        
        # Check strategy metrics
        assert 'position_size' in metrics
        assert metrics['position_size'] == 1.5
        assert 'risk_reward_setting' in metrics
        assert metrics['risk_reward_setting'] >= 0
        assert 'fee_per_trade' in metrics
        assert metrics['fee_per_trade'] == 0.08
        assert 'kelly_fraction' in metrics
        assert 'optimal_position_size' in metrics
        assert 'net_return' in metrics
        assert 'strategy_efficiency' in metrics
        assert 'strategy_sustainability' in metrics
        
        # Check ML metrics
        assert 'signal_frequency' in metrics
        assert 'signal_stability' in metrics
        assert 'signal_accuracy' in metrics
        assert 'signal_timing_score' in metrics
        assert 'momentum_correlation' in metrics
        assert 'volatility_correlation' in metrics
        assert 'trend_correlation' in metrics
        assert 'pattern_consistency' in metrics
        assert 'signal_clustering' in metrics
        
        # Check Monte Carlo metrics
        assert 'mc_expected_return' in metrics
        assert 'mc_std_deviation' in metrics
        assert 'mc_var_95' in metrics
        assert 'mc_cvar_95' in metrics
        assert 'mc_probability_profit' in metrics
        assert 'mc_max_loss' in metrics
        assert 'mc_max_gain' in metrics
        assert 'mc_sharpe_ratio' in metrics
        assert 'strategy_robustness' in metrics
        assert 'risk_of_ruin' in metrics
    
    def test_strategy_metrics_calculation(self):
        """Test strategy-specific metrics calculation."""
        metrics = self.calculator._calculate_strategy_metrics(
            self.test_df, 'Close', 'Direction', 1.0, 2.0, 0.07
        )
        
        # Check all strategy metrics are present
        required_metrics = [
            'position_size', 'risk_reward_setting', 'fee_per_trade',
            'kelly_fraction', 'optimal_position_size', 'fee_impact',
            'net_return', 'max_risk_per_trade', 'expected_risk_per_trade',
            'expected_reward_per_trade', 'break_even_win_rate',
            'strategy_efficiency', 'risk_adjusted_return_with_fees',
            'min_win_rate_for_profit', 'strategy_sustainability'
        ]
        
        for metric in required_metrics:
            assert metric in metrics, f"Missing metric: {metric}"
        
        # Check value ranges
        assert 0 <= metrics['kelly_fraction'] <= 1
        assert metrics['position_size'] >= 0
        assert metrics['risk_reward_setting'] >= 0
        assert metrics['fee_per_trade'] >= 0
        assert 0 <= metrics['strategy_sustainability'] <= 100
    
    def test_ml_metrics_calculation(self):
        """Test machine learning metrics calculation."""
        metrics = self.calculator._calculate_ml_metrics(
            self.test_df, 'Close', 'Direction'
        )
        
        # Check all ML metrics are present
        required_metrics = [
            'signal_frequency', 'signal_stability', 'signal_accuracy',
            'signal_timing_score', 'momentum_correlation', 'volatility_correlation',
            'trend_correlation', 'pattern_consistency', 'signal_clustering',
            'risk_adjusted_momentum', 'risk_adjusted_trend'
        ]
        
        for metric in required_metrics:
            assert metric in metrics, f"Missing metric: {metric}"
        
        # Check value ranges
        assert 0 <= metrics['signal_frequency'] <= 1
        assert 0 <= metrics['signal_stability'] <= 1
        assert 0 <= metrics['signal_accuracy'] <= 100
        assert -1 <= metrics['momentum_correlation'] <= 1
        assert -1 <= metrics['volatility_correlation'] <= 1
        assert -1 <= metrics['trend_correlation'] <= 1
        assert 0 <= metrics['pattern_consistency'] <= 100
        assert 0 <= metrics['signal_clustering'] <= 100
    
    def test_monte_carlo_metrics_calculation(self):
        """Test Monte Carlo metrics calculation."""
        metrics = self.calculator._calculate_monte_carlo_metrics(
            self.test_df, 'Close', 'Direction'
        )
        
        # Check all Monte Carlo metrics are present
        required_metrics = [
            'mc_expected_return', 'mc_std_deviation', 'mc_var_95',
            'mc_cvar_95', 'mc_probability_profit', 'mc_max_loss',
            'mc_max_gain', 'mc_sharpe_ratio', 'strategy_robustness',
            'risk_of_ruin'
        ]
        
        for metric in required_metrics:
            assert metric in metrics, f"Missing metric: {metric}"
        
        # Check value ranges
        assert 0 <= metrics['mc_probability_profit'] <= 100
        assert 0 <= metrics['strategy_robustness'] <= 100
        assert 0 <= metrics['risk_of_ruin'] <= 100
        assert metrics['mc_max_loss'] <= metrics['mc_max_gain']
    
    def test_pattern_consistency_calculation(self):
        """Test pattern consistency calculation."""
        consistency = self.calculator._calculate_pattern_consistency(
            self.test_df, 'Direction'
        )
        
        assert isinstance(consistency, float)
        assert 0 <= consistency <= 100
    
    def test_signal_clustering_calculation(self):
        """Test signal clustering calculation."""
        clustering = self.calculator._calculate_signal_clustering(
            self.test_df, 'Direction'
        )
        
        assert isinstance(clustering, float)
        assert 0 <= clustering <= 100
    
    def test_strategy_robustness_calculation(self):
        """Test strategy robustness calculation."""
        # Create sample simulation results
        simulation_results = np.random.normal(0.05, 0.15, 1000)
        
        robustness = self.calculator._calculate_strategy_robustness(
            simulation_results
        )
        
        assert isinstance(robustness, float)
        assert 0 <= robustness <= 100
    
    def test_risk_of_ruin_calculation(self):
        """Test risk of ruin calculation."""
        # Create sample trades
        trades = np.random.normal(0.02, 0.05, 100)
        
        risk_of_ruin = self.calculator._calculate_risk_of_ruin(trades)
        
        assert isinstance(risk_of_ruin, float)
        assert 0 <= risk_of_ruin <= 100
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrame."""
        empty_df = pd.DataFrame()
        
        metrics = self.calculator.calculate_all_metrics(empty_df)
        
        # Should return empty metrics with zero values
        assert metrics['buy_count'] == 0
        assert metrics['sell_count'] == 0
        assert metrics['total_trades'] == 0
    
    def test_missing_signal_column(self):
        """Test handling of missing signal column."""
        df_no_signals = self.test_df.drop(columns=['Direction'])
        
        metrics = self.calculator.calculate_all_metrics(df_no_signals)
        
        # Should return empty metrics with zero values
        assert metrics['buy_count'] == 0
        assert metrics['sell_count'] == 0
        assert metrics['total_trades'] == 0


class TestCalculateTradingMetrics:
    """Test cases for calculate_trading_metrics function."""
    
    def setup_method(self):
        """Set up test data."""
        dates = pd.date_range('2024-01-01', periods=50, freq='D')
        np.random.seed(42)
        
        prices = [100.0]
        for _ in range(49):
            prices.append(prices[-1] * (1 + np.random.normal(0.001, 0.02)))
        
        self.test_df = pd.DataFrame({
            'Open': prices,
            'High': [p * 1.01 for p in prices],
            'Low': [p * 0.99 for p in prices],
            'Close': prices,
            'Volume': np.random.randint(1000, 10000, 50),
            'Direction': np.random.choice([0, 1, 2], 50, p=[0.7, 0.15, 0.15])
        }, index=dates)
    
    def test_calculate_trading_metrics_with_strategy(self):
        """Test calculate_trading_metrics function with strategy parameters."""
        metrics = calculate_trading_metrics(
            self.test_df,
            lot_size=2.0,
            risk_reward_ratio=3.0,
            fee_per_trade=0.1
        )
        
        # Check strategy parameters are correctly passed
        assert metrics['position_size'] == 2.0
        assert metrics['risk_reward_setting'] >= 0
        assert metrics['fee_per_trade'] == 0.1
    
    def test_calculate_trading_metrics_defaults(self):
        """Test calculate_trading_metrics function with default parameters."""
        metrics = calculate_trading_metrics(self.test_df)
        
        # Check default strategy parameters
        assert metrics['position_size'] == 1.0
        assert metrics['risk_reward_setting'] >= 0
        assert metrics['fee_per_trade'] == 0.07
    
    def test_calculate_trading_metrics_with_volume(self):
        """Test calculate_trading_metrics function with volume data."""
        metrics = calculate_trading_metrics(
            self.test_df,
            volume_col='Volume'
        )
        
        # Should include volume-weighted metrics if available
        assert 'volume_weighted_return' in metrics or 'volume_win_ratio' in metrics


if __name__ == "__main__":
    pytest.main([__file__]) 