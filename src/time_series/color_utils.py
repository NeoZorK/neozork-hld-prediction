"""
Color utilities for time series analysis output.

This module provides colorized text output for better readability
and highlighting of important information in time series reports.
"""

from typing import Any, Dict, List, Optional, Union


class ColorUtils:
    """Utility class for colorized text output."""
    
    # ANSI color codes
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'end': '\033[0m'
    }
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Apply color to text."""
        if color not in cls.COLORS:
            return text
        return f"{cls.COLORS[color]}{text}{cls.COLORS['end']}"
    
    @classmethod
    def red(cls, text: str) -> str:
        """Red text for warnings, errors, high importance."""
        return cls.colorize(text, 'red')
    
    @classmethod
    def green(cls, text: str) -> str:
        """Green text for success, good values, positive indicators."""
        return cls.colorize(text, 'green')
    
    @classmethod
    def yellow(cls, text: str) -> str:
        """Yellow text for warnings, medium values, attention needed."""
        return cls.colorize(text, 'yellow')
    
    @classmethod
    def blue(cls, text: str) -> str:
        """Blue text for information, headers."""
        return cls.colorize(text, 'blue')
    
    @classmethod
    def cyan(cls, text: str) -> str:
        """Cyan text for highlights, special values."""
        return cls.colorize(text, 'cyan')
    
    @classmethod
    def bold(cls, text: str) -> str:
        """Bold text for emphasis."""
        return cls.colorize(text, 'bold')
    
    @classmethod
    def underline(cls, text: str) -> str:
        """Underlined text for headers."""
        return cls.colorize(text, 'underline')
    
    @classmethod
    def get_stationarity_color(cls, p_value: float) -> str:
        """Get color based on stationarity test p-value."""
        if p_value > 0.05:
            return 'green'  # Stationary - good
        elif p_value > 0.01:
            return 'yellow'  # Borderline - attention needed
        else:
            return 'red'  # Non-stationary - transformation needed
    
    @classmethod
    def get_volatility_color(cls, volatility: float) -> str:
        """Get color based on volatility level."""
        if volatility < 0.1:
            return 'green'  # Low volatility - stable
        elif volatility < 0.3:
            return 'yellow'  # Medium volatility - moderate risk
        else:
            return 'red'  # High volatility - high risk
    
    @classmethod
    def get_seasonality_color(cls, strength: float) -> str:
        """Get color based on seasonality strength."""
        if strength < 0.1:
            return 'green'  # Weak seasonality - good for trend analysis
        elif strength < 0.3:
            return 'yellow'  # Moderate seasonality - consider seasonal models
        else:
            return 'red'  # Strong seasonality - seasonal adjustment needed
    
    @classmethod
    def get_trend_color(cls, trend_strength: float) -> str:
        """Get color based on trend strength."""
        if trend_strength < 0.1:
            return 'green'  # Weak trend - stable
        elif trend_strength < 0.3:
            return 'yellow'  # Moderate trend - some direction
        else:
            return 'red'  # Strong trend - clear direction
    
    @classmethod
    def format_stationarity_p_value(cls, p_value: float) -> str:
        """Format stationarity test p-value with color."""
        color = cls.get_stationarity_color(p_value)
        return cls.colorize(f"{p_value:.6f}", color)
    
    @classmethod
    def format_volatility(cls, volatility: float) -> str:
        """Format volatility with color."""
        color = cls.get_volatility_color(volatility)
        return cls.colorize(f"{volatility:.4f}", color)
    
    @classmethod
    def format_seasonality_strength(cls, strength: float) -> str:
        """Format seasonality strength with color."""
        color = cls.get_seasonality_color(strength)
        return cls.colorize(f"{strength:.4f}", color)
    
    @classmethod
    def format_trend_strength(cls, strength: float) -> str:
        """Format trend strength with color."""
        color = cls.get_trend_color(strength)
        return cls.colorize(f"{strength:.4f}", color)
    
    @classmethod
    def format_price_change(cls, change: float) -> str:
        """Format price change with color."""
        if change > 0:
            return cls.green(f"+{change:.4f}")
        elif change < 0:
            return cls.red(f"{change:.4f}")
        else:
            return cls.yellow(f"{change:.4f}")
    
    @classmethod
    def format_percentage_change(cls, change: float) -> str:
        """Format percentage change with color."""
        if change > 0:
            return cls.green(f"+{change:.2f}%")
        elif change < 0:
            return cls.red(f"{change:.2f}%")
        else:
            return cls.yellow(f"{change:.2f}%")
    
    @classmethod
    def format_critical_value(cls, value: float, level: str) -> str:
        """Format critical value with color based on significance level."""
        if level == "1%":
            return cls.red(f"{value:.4f}")
        elif level == "5%":
            return cls.yellow(f"{value:.4f}")
        elif level == "10%":
            return cls.blue(f"{value:.4f}")
        else:
            return f"{value:.4f}"
    
    @classmethod
    def format_adf_statistic(cls, statistic: float, p_value: float) -> str:
        """Format ADF statistic with color based on significance."""
        color = cls.get_stationarity_color(p_value)
        return cls.colorize(f"{statistic:.4f}", color)
    
    @classmethod
    def format_recommendation(cls, recommendation: str) -> str:
        """Format recommendation with appropriate color."""
        recommendation_lower = recommendation.lower()
        
        if any(keyword in recommendation_lower for keyword in [
            'stationary', 'no transformation needed', 'good', 'excellent'
        ]):
            return cls.green(recommendation)
        elif any(keyword in recommendation_lower for keyword in [
            'differencing', 'transformation needed', 'moderate', 'consider'
        ]):
            return cls.yellow(recommendation)
        elif any(keyword in recommendation_lower for keyword in [
            'strongly recommended', 'critical', 'essential', 'required'
        ]):
            return cls.red(recommendation)
        else:
            return cls.blue(recommendation)
    
    @classmethod
    def format_pattern_strength(cls, strength: float) -> str:
        """Format pattern strength with color."""
        if strength < 0.1:
            return cls.green(f"{strength:.4f} (Weak)")
        elif strength < 0.3:
            return cls.yellow(f"{strength:.4f} (Moderate)")
        else:
            return cls.red(f"{strength:.4f} (Strong)")
    
    @classmethod
    def format_cyclical_period(cls, period: float) -> str:
        """Format cyclical period with color."""
        if period < 10:
            return cls.green(f"{period:.1f} periods")
        elif period < 50:
            return cls.yellow(f"{period:.1f} periods")
        else:
            return cls.red(f"{period:.1f} periods")
    
    @classmethod
    def format_financial_metric(cls, value: float, metric_type: str) -> str:
        """Format financial metric with appropriate color."""
        if metric_type == "volatility":
            return cls.format_volatility(value)
        elif metric_type == "price_change":
            return cls.format_price_change(value)
        elif metric_type == "percentage_change":
            return cls.format_percentage_change(value)
        elif metric_type == "range":
            return cls.format_range(value)
        else:
            return f"{value:.4f}"
    
    @classmethod
    def format_range(cls, range_val: float) -> str:
        """Format range with color based on magnitude."""
        if range_val < 0.1:
            return cls.colorize(f"{range_val:.4f}", 'green')  # Low range - stable
        elif range_val < 1.0:
            return cls.colorize(f"{range_val:.4f}", 'yellow')  # Medium range
        else:
            return cls.colorize(f"{range_val:.4f}", 'red')  # High range - volatile
    
    @classmethod
    def format_quality_assessment(cls, assessment: str) -> str:
        """Format data quality assessment with color."""
        if 'excellent' in assessment.lower():
            return cls.green(assessment)
        elif 'good' in assessment.lower():
            return cls.yellow(assessment)
        elif 'poor' in assessment.lower() or 'concerning' in assessment.lower():
            return cls.red(assessment)
        else:
            return assessment
    
    @classmethod
    def format_interpretation(cls, interpretation: str) -> str:
        """Format interpretation with appropriate color."""
        interpretation_lower = interpretation.lower()
        
        if any(keyword in interpretation_lower for keyword in [
            'highly skewed', 'heavily skewed', 'extremely skewed', 'severe',
            'heavy-tailed', 'light-tailed', 'extreme', 'critical'
        ]):
            return cls.red(interpretation)
        elif any(keyword in interpretation_lower for keyword in [
            'moderately skewed', 'moderate', 'attention', 'warning',
            'slightly different', 'somewhat'
        ]):
            return cls.yellow(interpretation)
        elif any(keyword in interpretation_lower for keyword in [
            'approximately normal', 'approximately symmetric', 'normal',
            'good', 'excellent', 'satisfactory'
        ]):
            return cls.green(interpretation)
        else:
            return cls.blue(interpretation)
