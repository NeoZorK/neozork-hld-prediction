# -*- coding: utf-8 -*-
# tests/cli/test_quant_encyclopedia.py

"""
Tests for Quantitative Trading Encyclopedia Module
All comments are in English.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.cli.encyclopedia.quant_encyclopedia import QuantEncyclopedia


class TestQuantEncyclopedia:
    """Test cases for QuantEncyclopedia class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.encyclopedia = QuantEncyclopedia()
    
    def test_initialization(self):
        """Test encyclopedia initialization."""
        assert hasattr(self.encyclopedia, 'metrics')
        assert hasattr(self.encyclopedia, 'tips')
        assert isinstance(self.encyclopedia.metrics, dict)
        assert isinstance(self.encyclopedia.tips, dict)
        assert len(self.encyclopedia.metrics) > 0
        assert len(self.encyclopedia.tips) > 0
    
    def test_metrics_structure(self):
        """Test metrics data structure."""
        for metric_key, metric_data in self.encyclopedia.metrics.items():
            assert 'name' in metric_data
            assert 'icon' in metric_data
            assert 'category' in metric_data
            assert 'description' in metric_data
            assert 'formula' in metric_data
            assert 'interpretation' in metric_data
            assert 'good_range' in metric_data
            assert 'excellent_range' in metric_data
            assert 'warning_range' in metric_data
            assert 'calculation_note' in metric_data
            assert 'strategy_impact' in metric_data
    
    def test_tips_structure(self):
        """Test tips data structure."""
        for tip_key, tip_data in self.encyclopedia.tips.items():
            assert 'title' in tip_data
            assert 'icon' in tip_data
            assert 'category' in tip_data
            assert 'tips' in tip_data
            assert isinstance(tip_data['tips'], list)
            
            for tip in tip_data['tips']:
                assert 'tip' in tip
                assert 'explanation' in tip
                assert 'action' in tip
    
    def test_get_metric_info(self):
        """Test getting metric information."""
        # Test existing metric
        win_ratio_info = self.encyclopedia.get_metric_info('win_ratio')
        assert win_ratio_info is not None
        assert win_ratio_info['name'] == 'Win Ratio'
        
        # Test with different case
        profit_factor_info = self.encyclopedia.get_metric_info('Profit Factor')
        assert profit_factor_info is not None
        assert profit_factor_info['name'] == 'Profit Factor'
        
        # Test non-existent metric
        non_existent = self.encyclopedia.get_metric_info('non_existent_metric')
        assert non_existent is None
    
    def test_get_tips_by_category(self):
        """Test getting tips by category."""
        # Test existing category
        risk_tips = self.encyclopedia.get_tips_by_category('risk')
        assert len(risk_tips) > 0
        
        # Test non-existent category
        non_existent_tips = self.encyclopedia.get_tips_by_category('non_existent')
        assert len(non_existent_tips) == 0
    
    @patch('builtins.print')
    def test_show_all_metrics(self, mock_print):
        """Test showing all metrics."""
        self.encyclopedia.show_all_metrics()
        assert mock_print.called
    
    @patch('builtins.print')
    def test_show_all_metrics_with_filter(self, mock_print):
        """Test showing metrics with filter."""
        self.encyclopedia.show_all_metrics('profit')
        assert mock_print.called
    
    @patch('builtins.print')
    def test_show_all_tips(self, mock_print):
        """Test showing all tips."""
        self.encyclopedia.show_all_tips()
        assert mock_print.called
    
    @patch('builtins.print')
    def test_show_all_tips_with_filter(self, mock_print):
        """Test showing tips with filter."""
        self.encyclopedia.show_all_tips('winrate')
        assert mock_print.called
    
    @patch('builtins.print')
    def test_show_filtered_content(self, mock_print):
        """Test showing filtered content."""
        self.encyclopedia.show_filtered_content('profit factor')
        assert mock_print.called
    
    def test_metrics_categories(self):
        """Test that metrics are properly categorized."""
        categories = set()
        for metric_data in self.encyclopedia.metrics.values():
            categories.add(metric_data['category'])
        
        expected_categories = {
            'Core Performance',
            'Risk-Adjusted Returns',
            'Risk Management',
            'Position Sizing',
            'Performance',
            'Strategy Quality',
            'Strategy Analysis',
            'Probability Analysis'
        }
        
        assert categories.issubset(expected_categories)
    
    def test_tips_categories(self):
        """Test that tips are properly categorized."""
        categories = set()
        for tip_data in self.encyclopedia.tips.values():
            categories.add(tip_data['category'])
        
        expected_categories = {
            'Performance',
            'Risk Management',
            'Advanced Analysis',
            'Machine Learning',
            'Strategy',
            'Strategy Validation'
        }
        
        assert categories.issubset(expected_categories)
    
    def test_specific_metrics_exist(self):
        """Test that specific important metrics exist."""
        important_metrics = [
            'win_ratio',
            'profit_factor',
            'risk_reward_ratio',
            'sharpe_ratio',
            'max_drawdown',
            'kelly_fraction'
        ]
        
        for metric in important_metrics:
            assert metric in self.encyclopedia.metrics
    
    def test_specific_tips_exist(self):
        """Test that specific important tips exist."""
        important_tips = [
            'winrate',
            'risk_management',
            'monte_carlo',
            'neural_networks',
            'deep_learning',
            'profit_factor'
        ]
        
        for tip in important_tips:
            assert tip in self.encyclopedia.tips
    
    def test_metric_filtering(self):
        """Test metric filtering functionality."""
        # Test filtering by metric name
        filtered_metrics = {}
        for key, data in self.encyclopedia.metrics.items():
            if 'profit' in key.lower() or 'profit' in data['name'].lower():
                filtered_metrics[key] = data
        
        assert len(filtered_metrics) > 0
        assert 'profit_factor' in filtered_metrics
    
    def test_tip_filtering(self):
        """Test tip filtering functionality."""
        # Test filtering by tip title
        filtered_tips = {}
        for key, data in self.encyclopedia.tips.items():
            if 'win' in key.lower() or 'win' in data['title'].lower():
                filtered_tips[key] = data
        
        assert len(filtered_tips) > 0
        assert 'winrate' in filtered_tips


class TestQuantEncyclopediaIntegration:
    """Integration tests for QuantEncyclopedia."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.encyclopedia = QuantEncyclopedia()
    
    @patch('builtins.print')
    def test_full_encyclopedia_display(self, mock_print):
        """Test full encyclopedia display without filters."""
        self.encyclopedia.show_all_metrics()
        self.encyclopedia.show_all_tips()
        
        # Verify that print was called multiple times
        assert mock_print.call_count > 10
    
    @patch('builtins.print')
    def test_filtered_display(self, mock_print):
        """Test filtered display functionality."""
        self.encyclopedia.show_filtered_content('profit factor')
        
        # Verify that print was called
        assert mock_print.called
    
    def test_encyclopedia_completeness(self):
        """Test that encyclopedia contains comprehensive information."""
        # Check metrics completeness
        assert len(self.encyclopedia.metrics) >= 15  # Should have at least 15 metrics
        
        # Check tips completeness
        assert len(self.encyclopedia.tips) >= 8  # Should have at least 8 tip categories
        
        # Check that each tip category has multiple tips
        for tip_data in self.encyclopedia.tips.values():
            assert len(tip_data['tips']) >= 3  # Each category should have at least 3 tips


def test_main_function():
    """Test the main function of the encyclopedia module."""
    from src.cli.encyclopedia.quant_encyclopedia import main
    
    # This should not raise any exceptions
    try:
        main()
    except Exception as e:
        pytest.fail(f"main() raised {e} unexpectedly!")


if __name__ == "__main__":
    pytest.main([__file__]) 