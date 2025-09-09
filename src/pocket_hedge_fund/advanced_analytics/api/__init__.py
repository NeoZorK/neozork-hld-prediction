"""
Advanced Analytics API

This module provides REST API endpoints for advanced analytics:
- Real-time analytics endpoints
- Historical data analysis
- ML model predictions
- Insight generation
- Visualization data
"""

from .analytics_api import router

__all__ = ["router"]
