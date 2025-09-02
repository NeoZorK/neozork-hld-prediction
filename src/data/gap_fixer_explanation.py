# File: src/data/gap_fixer_explanation.py
# -*- coding: utf-8 -*-

"""
Explanation module for gap fixing importance.
Provides educational content about why time series gaps need to be fixed.
All comments are in English.
"""


def explain_why_fix_gaps() -> str:
    """Explain why time series gaps need to be fixed before EDA analysis."""
    explanation = """
🔍 WHY TIME SERIES GAPS NEED TO BE FIXED BEFORE EDA ANALYSIS
============================================================

📊 Data Quality Issues:
   • Gaps create artificial patterns that can mislead analysis
   • Missing data points affect statistical calculations
   • Inconsistent time intervals distort trend analysis

📈 Analysis Accuracy:
   • Technical indicators become unreliable with gaps
   • Correlation analysis produces incorrect results
   • Seasonal patterns are distorted or missed entirely

🎯 ML Model Performance:
   • Models trained on gapped data learn incorrect patterns
   • Feature engineering produces unreliable results
   • Prediction accuracy is significantly reduced

⚡ Performance Benefits:
   • Faster processing with complete datasets
   • More accurate statistical calculations
   • Better visualization quality

🔄 Recommended Workflow:
   1. Load and inspect data
   2. Identify and fix gaps
   3. Perform EDA analysis
   4. Engineer features
   5. Train ML models

💡 Best Practices:
   • Always fix gaps before analysis
   • Use appropriate interpolation methods
   • Create backups before modifications
   • Validate data after gap fixing
"""
    return explanation


def get_gap_fixing_benefits() -> dict:
    """Get a structured list of benefits from gap fixing."""
    return {
        "data_quality": [
            "Eliminates artificial patterns",
            "Ensures consistent time intervals",
            "Improves data completeness",
            "Reduces analysis bias"
        ],
        "analysis_accuracy": [
            "More reliable technical indicators",
            "Accurate trend analysis",
            "Proper seasonal pattern detection",
            "Correct correlation calculations"
        ],
        "ml_performance": [
            "Better feature engineering",
            "Improved model training",
            "Higher prediction accuracy",
            "More robust model validation"
        ],
        "performance": [
            "Faster data processing",
            "Efficient memory usage",
            "Optimized calculations",
            "Better visualization quality"
        ]
    }


def get_gap_fixing_methods() -> dict:
    """Get available gap fixing methods and their use cases."""
    return {
        "linear": {
            "description": "Linear interpolation between known points",
            "best_for": "Small gaps, smooth data",
            "pros": "Simple, fast, preserves trends",
            "cons": "May not capture complex patterns"
        },
        "cubic": {
            "description": "Cubic spline interpolation",
            "best_for": "Medium gaps, smooth data",
            "pros": "Smooth curves, good for trends",
            "cons": "Can overshoot at boundaries"
        },
        "forward_fill": {
            "description": "Carry forward last known value",
            "best_for": "Categorical data, small gaps",
            "pros": "Simple, preserves categorical values",
            "cons": "Creates flat lines, may not be realistic"
        },
        "backward_fill": {
            "description": "Carry backward next known value",
            "best_for": "Categorical data, small gaps",
            "pros": "Simple, preserves categorical values",
            "cons": "Creates flat lines, may not be realistic"
        },
        "interpolate": {
            "description": "Advanced interpolation with fallbacks",
            "best_for": "Mixed data types, various gap sizes",
            "pros": "Robust, handles different data types",
            "cons": "May be slower than simple methods"
        },
        "seasonal": {
            "description": "Seasonal decomposition with interpolation",
            "best_for": "Data with seasonal patterns",
            "pros": "Captures seasonal effects, realistic",
            "cons": "Computationally intensive, requires patterns"
        }
    }


def get_gap_detection_metrics() -> dict:
    """Get metrics used for gap detection and analysis."""
    return {
        "gap_count": "Total number of gaps detected",
        "gap_ratio": "Percentage of data points that are gaps",
        "gap_size_distribution": "Distribution of gap sizes",
        "time_coverage": "Percentage of expected time covered by data",
        "frequency_consistency": "How consistent the time intervals are",
        "data_completeness": "Overall completeness of the dataset"
    }
