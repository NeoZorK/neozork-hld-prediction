# -*- coding: utf-8 -*-
"""
Scaling module for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive scaling and production capabilities.
"""

from .horizontal_scaling import HorizontalScaling
from .load_balancer import LoadBalancer
from .production_deployment import ProductionDeployment
from .health_monitoring import HealthMonitoring

class ScalingSystem:
    """Main scaling system class."""
    def __init__(self):
        self.horizontal_scaling = HorizontalScaling()
        self.load_balancer = LoadBalancer()
        self.production_deployment = ProductionDeployment()
        self.health_monitoring = HealthMonitoring()

__all__ = [
    'ScalingSystem',
    'HorizontalScaling',
    'LoadBalancer',
    'ProductionDeployment',
    'HealthMonitoring'
]
