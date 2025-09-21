"""
Color utilities for statistical analysis output.

This module provides colorized text output for better readability
and highlighting of important information in statistical reports.
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
    def get_variability_color(cls, cv_percentage: float) -> str:
        """Get color based on coefficient of variation."""
        if cv_percentage < 30:
            return 'green'  # Low variability - good
        elif cv_percentage < 70:
            return 'yellow'  # Medium variability - attention
        else:
            return 'red'  # High variability - concerning
    
    @classmethod
    def get_skewness_color(cls, skewness: float) -> str:
        """Get color based on skewness value."""
        abs_skew = abs(skewness)
        if abs_skew < 0.5:
            return 'green'  # Approximately symmetric - good
        elif abs_skew < 1.0:
            return 'yellow'  # Moderately skewed - attention
        else:
            return 'red'  # Highly skewed - concerning
    
    @classmethod
    def get_kurtosis_color(cls, kurtosis: float) -> str:
        """Get color based on kurtosis value."""
        if -0.5 <= kurtosis <= 0.5:
            return 'green'  # Approximately normal - good
        elif -1.0 <= kurtosis <= 1.0:
            return 'yellow'  # Slightly different from normal - attention
        else:
            return 'red'  # Significantly different from normal - concerning
    
    @classmethod
    def get_missing_data_color(cls, missing_percentage: float) -> str:
        """Get color based on missing data percentage."""
        if missing_percentage < 1.0:
            return 'green'  # Excellent - very little missing data
        elif missing_percentage < 5.0:
            return 'yellow'  # Good - acceptable missing data
        else:
            return 'red'  # Poor - too much missing data
    
    @classmethod
    def get_normality_test_color(cls, p_value: float) -> str:
        """Get color based on normality test p-value."""
        if p_value > 0.05:
            return 'green'  # Normal distribution - good
        elif p_value > 0.01:
            return 'yellow'  # Borderline - attention needed
        else:
            return 'red'  # Non-normal - transformation needed
    
    @classmethod
    def get_recommendation_color(cls, recommendation_type: str) -> str:
        """Get color based on recommendation type."""
        if 'strongly recommended' in recommendation_type.lower():
            return 'red'
        elif 'recommended' in recommendation_type.lower():
            return 'yellow'
        elif 'good' in recommendation_type.lower() or 'excellent' in recommendation_type.lower():
            return 'green'
        else:
            return 'blue'
    
    @classmethod
    def format_percentage(cls, value: float, color_by_value: bool = True) -> str:
        """Format percentage with appropriate color."""
        if color_by_value:
            if value < 1.0:
                color = 'green'
            elif value < 5.0:
                color = 'yellow'
            else:
                color = 'red'
            return cls.colorize(f"{value:.2f}%", color)
        return f"{value:.2f}%"
    
    @classmethod
    def format_coefficient_variation(cls, cv: float) -> str:
        """Format coefficient of variation with color."""
        color = cls.get_variability_color(cv)
        return cls.colorize(f"{cv:.2f}%", color)
    
    @classmethod
    def format_skewness(cls, skewness: float) -> str:
        """Format skewness with color and interpretation."""
        color = cls.get_skewness_color(skewness)
        if abs(skewness) < 0.5:
            interpretation = "Approximately symmetric"
        elif abs(skewness) < 1.0:
            interpretation = "Moderately skewed"
        else:
            interpretation = "Highly skewed"
        
        direction = "right-tailed" if skewness > 0 else "left-tailed"
        return f"{cls.colorize(f'{skewness:.4f}', color)} - {cls.colorize(interpretation, color)} ({direction})"
    
    @classmethod
    def format_kurtosis(cls, kurtosis: float) -> str:
        """Format kurtosis with color and interpretation."""
        color = cls.get_kurtosis_color(kurtosis)
        if -0.5 <= kurtosis <= 0.5:
            interpretation = "Approximately normal (mesokurtic)"
        elif kurtosis > 0.5:
            interpretation = "Heavy-tailed (leptokurtic)"
        else:
            interpretation = "Light-tailed (platykurtic)"
        
        return f"{cls.colorize(f'{kurtosis:.4f}', color)} - {cls.colorize(interpretation, color)}"
    
    @classmethod
    def format_missing_data(cls, missing_percentage: float) -> str:
        """Format missing data percentage with color."""
        color = cls.get_missing_data_color(missing_percentage)
        return cls.colorize(f"{missing_percentage:.2f}%", color)
    
    @classmethod
    def format_normality_p_value(cls, p_value: float) -> str:
        """Format normality test p-value with color."""
        color = cls.get_normality_test_color(p_value)
        return cls.colorize(f"{p_value:.6f}", color)
    
    @classmethod
    def format_success_status(cls, status: str) -> str:
        """Format success status with color."""
        if 'success' in status.lower() or 'completed' in status.lower():
            return cls.green(status)
        elif 'warning' in status.lower() or 'attention' in status.lower():
            return cls.yellow(status)
        elif 'error' in status.lower() or 'failed' in status.lower():
            return cls.red(status)
        else:
            return status
    
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
    def get_transformation_recommendation_color(cls, recommendation: str) -> str:
        """Get color based on transformation recommendation type."""
        recommendation_lower = recommendation.lower()
        
        # Green - where no transformation is needed
        if any(keyword in recommendation_lower for keyword in [
            'no transformation needed', 'no transformation required', 'good as is',
            'excellent', 'normal distribution', 'no change needed', 'satisfactory',
            'appears approximately normal'
        ]):
            return 'green'
        
        # Red - where transformation is needed
        elif any(keyword in recommendation_lower for keyword in [
            'strongly recommended', 'transformation needed', 'highly recommended',
            'critical', 'essential', 'required', 'necessary', 'box-cox transformation',
            'log transformation', 'sqrt transformation', 'yeo-johnson transformation',
            'square transformation'
        ]):
            return 'red'
        
        # Yellow - moderate recommendations or warnings
        elif any(keyword in recommendation_lower for keyword in [
            'recommended', 'suggested', 'consider', 'may benefit', 'optional',
            'moderate', 'attention', 'warning', 'caution'
        ]):
            return 'yellow'
        
        # Default to blue for other cases
        else:
            return 'blue'
    
    @classmethod
    def format_transformation_recommendation(cls, recommendation: str) -> str:
        """Format transformation recommendation with appropriate color."""
        color = cls.get_transformation_recommendation_color(recommendation)
        return cls.colorize(recommendation, color)