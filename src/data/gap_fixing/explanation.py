# -*- coding: utf-8 -*-
# src/data/gap_fixing/explanation.py

"""
Gap fixing explanation and documentation module.
Provides explanations and information about gap fixing methods.
All comments are in English.
"""

from typing import Dict, List, Any


def explain_why_fix_gaps() -> str:
    """
    Explain why fixing gaps in time series data is important.
    
    Returns:
        String explanation of gap fixing importance
    """
    explanation = """
    Why Fix Gaps in Time Series Data?
    
    Time series data often contains gaps due to:
    - Data collection issues
    - System downtime
    - Missing observations
    - Data corruption
    
    These gaps can cause problems in:
    - Machine learning models
    - Statistical analysis
    - Trading algorithms
    - Data visualization
    - Forecasting models
    
    Gap fixing helps by:
    - Maintaining data continuity
    - Improving model accuracy
    - Enabling consistent analysis
    - Preserving temporal relationships
    """
    return explanation.strip()


def get_gap_fixing_benefits() -> Dict[str, List[str]]:
    """
    Get the benefits of fixing gaps in time series data.
    
    Returns:
        Dictionary with benefit categories and descriptions
    """
    benefits = {
        "Data Quality": [
            "Eliminates missing values",
            "Maintains data consistency",
            "Improves data completeness",
            "Preserves temporal structure"
        ],
        "Analysis Benefits": [
            "Enables continuous analysis",
            "Improves statistical validity",
            "Reduces bias in results",
            "Maintains sample size"
        ],
        "Model Performance": [
            "Better machine learning results",
            "Improved forecasting accuracy",
            "More reliable predictions",
            "Consistent model inputs"
        ],
        "Business Value": [
            "More accurate trading signals",
            "Better risk assessment",
            "Improved decision making",
            "Reduced data preparation time"
        ]
    }
    return benefits


def get_gap_fixing_methods() -> Dict[str, Dict[str, Any]]:
    """
    Get information about available gap fixing methods.
    
    Returns:
        Dictionary with method information
    """
    methods = {
        "linear": {
            "name": "Linear Interpolation",
            "description": "Fills gaps using linear interpolation between known values",
            "best_for": "Small to medium gaps, smooth data",
            "pros": ["Simple", "Fast", "Preserves trends"],
            "cons": ["May not capture complex patterns", "Can be too smooth"]
        },
        "cubic": {
            "name": "Cubic Interpolation",
            "description": "Uses cubic splines for smoother interpolation",
            "best_for": "Medium gaps, data with curvature",
            "pros": ["Smooth", "Captures curvature", "Better than linear"],
            "cons": ["Slower than linear", "May overshoot"]
        },
        "seasonal": {
            "name": "Seasonal Interpolation",
            "description": "Uses seasonal patterns to fill gaps",
            "best_for": "Data with seasonal patterns",
            "pros": ["Captures seasonality", "More realistic"],
            "cons": ["Requires seasonal data", "More complex"]
        },
        "forward_fill": {
            "name": "Forward Fill",
            "description": "Uses the last known value to fill gaps",
            "best_for": "Very small gaps, stable data",
            "pros": ["Simple", "Fast", "Preserves exact values"],
            "cons": ["Can create plateaus", "May not reflect reality"]
        },
        "backward_fill": {
            "name": "Backward Fill",
            "description": "Uses the next known value to fill gaps",
            "best_for": "Very small gaps, stable data",
            "pros": ["Simple", "Fast", "Preserves exact values"],
            "cons": ["Can create plateaus", "May not reflect reality"]
        },
        "ml_forecast": {
            "name": "Machine Learning Forecasting",
            "description": "Uses ML models to predict missing values",
            "best_for": "Large gaps, complex patterns",
            "pros": ["Can capture complex patterns", "More accurate"],
            "cons": ["Slower", "More complex", "Requires training data"]
        },
        "chunked": {
            "name": "Chunked Processing",
            "description": "Processes large datasets in chunks",
            "best_for": "Very large datasets, memory constraints",
            "pros": ["Memory efficient", "Handles large data"],
            "cons": ["More complex", "May have chunk boundaries"]
        }
    }
    return methods


def get_gap_detection_metrics() -> Dict[str, str]:
    """
    Get information about gap detection metrics.
    
    Returns:
        Dictionary with metric descriptions
    """
    metrics = {
        "gap_count": "Total number of gaps detected in the data",
        "gap_size": "Average size of gaps in time units",
        "gap_percentage": "Percentage of data that is missing",
        "time_range": "Start and end times of the data",
        "expected_frequency": "Expected time interval between observations",
        "data_quality": "Overall quality assessment of the data",
        "time_series_type": "Type of time series (e.g., regular, irregular)"
    }
    return metrics


def get_gap_fixing_recommendations(gap_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get recommendations for gap fixing based on gap characteristics.
    
    Args:
        gap_info: Dictionary containing gap information
        
    Returns:
        Dictionary with recommendations
    """
    gap_count = gap_info.get('gap_count', 0)
    gap_size = gap_info.get('gap_size', 0)
    data_quality = gap_info.get('data_quality', 'unknown')
    
    recommendations = {
        "algorithm": "linear",  # Default
        "reasoning": "Standard approach for most cases",
        "alternatives": [],
        "warnings": [],
        "notes": []
    }
    
    # Algorithm selection logic
    if gap_count == 0:
        recommendations["algorithm"] = "none"
        recommendations["reasoning"] = "No gaps detected"
    elif gap_size <= 5:
        recommendations["algorithm"] = "forward_fill"
        recommendations["reasoning"] = "Small gaps, forward fill is appropriate"
        recommendations["alternatives"] = ["backward_fill", "linear"]
    elif gap_size <= 20:
        recommendations["algorithm"] = "linear"
        recommendations["reasoning"] = "Medium gaps, linear interpolation works well"
        recommendations["alternatives"] = ["cubic", "seasonal"]
    elif gap_size <= 100:
        recommendations["algorithm"] = "cubic"
        recommendations["reasoning"] = "Large gaps, cubic interpolation for smoothness"
        recommendations["alternatives"] = ["seasonal", "ml_forecast"]
    else:
        recommendations["algorithm"] = "chunked"
        recommendations["reasoning"] = "Very large gaps, chunked processing recommended"
        recommendations["alternatives"] = ["ml_forecast", "seasonal"]
    
    # Quality-based adjustments
    if data_quality == 'poor':
        recommendations["warnings"].append("Data quality is poor, results may be unreliable")
        recommendations["notes"].append("Consider data cleaning before gap fixing")
    
    # Add general notes
    if gap_count > 1000:
        recommendations["warnings"].append("Large number of gaps detected")
        recommendations["notes"].append("Consider investigating data source issues")
    
    return recommendations
