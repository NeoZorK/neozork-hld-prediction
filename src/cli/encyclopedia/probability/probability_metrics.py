# -*- coding: utf-8 -*-
"""
Probability Indicator Metrics Encyclopedia

This module provides comprehensive metrics information for probability indicators.
"""

from typing import Dict, Any

class ProbabilityMetrics:
    """Comprehensive metrics for probability indicators."""
    
    @staticmethod
    def get_monte_carlo_metrics() -> Dict[str, Any]:
        """Get Monte Carlo-specific metrics and explanations."""
        return {
            'name': 'Monte Carlo Simulation',
            'icon': '🎲',
            'category': 'Probability',
            'description': 'Statistical method using random sampling to estimate probability distributions',
            'formula': 'Uses random number generation to simulate multiple price paths',
            'interpretation': 'Higher probability of reaching target indicates stronger signal',
            'good_range': '60-80% probability',
            'excellent_range': '70-90% probability',
            'warning_range': '<50% or >95% probability',
            'calculation_note': 'Requires historical volatility and drift parameters',
            'strategy_impact': 'Advanced risk assessment and probability-based decision making'
        }
    
    @staticmethod
    def get_kelly_criterion_metrics() -> Dict[str, Any]:
        """Get Kelly Criterion-specific metrics and explanations."""
        return {
            'name': 'Kelly Criterion',
            'icon': '💰',
            'category': 'Probability',
            'description': 'Formula to determine optimal position size based on win rate and odds',
            'formula': 'Kelly % = (bp - q) / b where b = odds-1, p = win probability, q = loss probability',
            'interpretation': 'Positive values indicate profitable opportunities, negative indicate avoid',
            'good_range': '5-20% of capital',
            'excellent_range': '10-25% of capital',
            'warning_range': '<2% or >30% of capital',
            'calculation_note': 'Based on historical win rate and average win/loss ratios',
            'strategy_impact': 'Optimal position sizing for long-term capital growth'
        }
    
    @staticmethod
    def get_probability_distribution_metrics() -> Dict[str, Any]:
        """Get Probability Distribution-specific metrics and explanations."""
        return {
            'name': 'Probability Distribution',
            'icon': '📊',
            'category': 'Probability',
            'description': 'Statistical distribution of price movements and returns',
            'formula': 'Various distributions: Normal, Log-normal, Student-t, etc.',
            'interpretation': 'Distribution shape indicates market behavior and risk characteristics',
            'good_range': 'Distribution fits data with R² > 0.8',
            'excellent_range': 'Distribution fits data with R² > 0.9',
            'warning_range': 'Distribution fits data with R² < 0.6',
            'calculation_note': 'Statistical fitting of price data to theoretical distributions',
            'strategy_impact': 'Foundation for risk modeling and probability calculations'
        }
    
    @staticmethod
    def get_confidence_interval_metrics() -> Dict[str, Any]:
        """Get Confidence Interval-specific metrics and explanations."""
        return {
            'name': 'Confidence Interval',
            'icon': '🎯',
            'category': 'Probability',
            'description': 'Range within which true parameter value lies with specified confidence',
            'formula': 'CI = Sample Mean ± (Critical Value × Standard Error)',
            'interpretation': 'Narrower intervals indicate more precise estimates',
            'good_range': '90-95% confidence level',
            'excellent_range': '95-99% confidence level',
            'warning_range': '<85% or >99.9% confidence level',
            'calculation_note': 'Based on sample statistics and desired confidence level',
            'strategy_impact': 'Statistical validation of trading signals and risk estimates'
        }
    
    @staticmethod
    def get_all_probability_metrics() -> Dict[str, Dict[str, Any]]:
        """Get all probability metrics."""
        return {
            'MonteCarlo': ProbabilityMetrics.get_monte_carlo_metrics(),
            'Kelly': ProbabilityMetrics.get_kelly_criterion_metrics(),
            'Probability_Distribution': ProbabilityMetrics.get_probability_distribution_metrics(),
            'Confidence_Interval': ProbabilityMetrics.get_confidence_interval_metrics()
        }
