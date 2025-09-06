#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Monitoring and Alerting Module

This module provides comprehensive monitoring and alerting capabilities.
"""

import asyncio
import json
import logging
import time
import psutil
import smtplib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from collections import defaultdict, deque
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    """Alert levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertStatus(Enum):
    """Alert status."""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

class NotificationChannel(Enum):
    """Notification channels."""
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    SLACK = "slack"
    TEAMS = "teams"
    DISCORD = "discord"

class MetricType(Enum):
    """Metric types."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

@dataclass
class Metric:
    """Metric definition."""
    name: str
    value: float
    metric_type: MetricType
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    description: str = ""

@dataclass
class AlertRule:
    """Alert rule definition."""
    rule_id: str
    name: str
    description: str
    metric_name: str
    condition: str
    threshold: float
    alert_level: AlertLevel
    notification_channels: List[NotificationChannel]
    escalation_delay: int = 300
    suppression_duration: int = 3600
    enabled: bool = True

@dataclass
class Alert:
    """Alert instance."""
    alert_id: str
    rule_id: str
    metric_name: str
    current_value: float
    threshold: float
    alert_level: AlertLevel
    status: AlertStatus
    message: str
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class SystemMetricsCollector:
    """Collects system metrics."""
    
    def __init__(self):
        self.metrics: Dict[str, Metric] = {}
    
    def collect_cpu_metrics(self) -> List[Metric]:
        """Collect CPU metrics."""
        metrics = []
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        metrics.append(Metric(
            name="cpu_usage_percent",
            value=cpu_percent,
            metric_type=MetricType.GAUGE,
            description="CPU usage percentage"
        ))
        
        # CPU count
        cpu_count = psutil.cpu_count()
        metrics.append(Metric(
            name="cpu_count",
            value=cpu_count,
            metric_type=MetricType.GAUGE,
            description="Number of CPU cores"
        ))
        
        return metrics
    
    def collect_memory_metrics(self) -> List[Metric]:
        """Collect memory metrics."""
        metrics = []
        
        memory = psutil.virtual_memory()
        
        # Memory usage percentage
        metrics.append(Metric(
            name="memory_usage_percent",
            value=memory.percent,
            metric_type=MetricType.GAUGE,
            description="Memory usage percentage"
        ))
        
        # Memory usage bytes
        metrics.append(Metric(
            name="memory_used_bytes",
            value=memory.used,
            metric_type=MetricType.GAUGE,
            description="Memory used in bytes"
        ))
        
        return metrics
    
    def collect_all_metrics(self) -> List[Metric]:
        """Collect all system metrics."""
        all_metrics = []
        all_metrics.extend(self.collect_cpu_metrics())
        all_metrics.extend(self.collect_memory_metrics())
        
        # Store metrics
        for metric in all_metrics:
            self.metrics[metric.name] = metric
        
        return all_metrics

class AlertManager:
    """Manages alerts and alert rules."""
    
    def __init__(self):
        self.alert_rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default alert rules."""
        # CPU usage rule
        self.add_alert_rule(AlertRule(
            rule_id="cpu_high_usage",
            name="High CPU Usage",
            description="Alert when CPU usage exceeds 80%",
            metric_name="cpu_usage_percent",
            condition="value > 80",
            threshold=80.0,
            alert_level=AlertLevel.WARNING,
            notification_channels=[NotificationChannel.EMAIL]
        ))
        
        # Memory usage rule
        self.add_alert_rule(AlertRule(
            rule_id="memory_high_usage",
            name="High Memory Usage",
            description="Alert when memory usage exceeds 85%",
            metric_name="memory_usage_percent",
            condition="value > 85",
            threshold=85.0,
            alert_level=AlertLevel.ERROR,
            notification_channels=[NotificationChannel.EMAIL]
        ))
    
    def add_alert_rule(self, rule: AlertRule):
        """Add alert rule."""
        self.alert_rules[rule.rule_id] = rule
        logger.info(f"Added alert rule: {rule.name}")
    
    def evaluate_metric(self, metric: Metric):
        """Evaluate metric against alert rules."""
        for rule in self.alert_rules.values():
            if not rule.enabled or rule.metric_name != metric.name:
                continue
            
            # Check if condition is met
            if self._evaluate_condition(metric.value, rule.condition, rule.threshold):
                # Check if alert already exists
                existing_alert = None
                for alert in self.active_alerts.values():
                    if alert.rule_id == rule.rule_id and alert.status == AlertStatus.ACTIVE:
                        existing_alert = alert
                        break
                
                if not existing_alert:
                    # Create new alert
                    alert = Alert(
                        alert_id=str(uuid.uuid4()),
                        rule_id=rule.rule_id,
                        metric_name=metric.name,
                        current_value=metric.value,
                        threshold=rule.threshold,
                        alert_level=rule.alert_level,
                        status=AlertStatus.ACTIVE,
                        message=f"{rule.name}: {metric.name} = {metric.value} (threshold: {rule.threshold})",
                        created_at=datetime.now()
                    )
                    
                    self.active_alerts[alert.alert_id] = alert
                    self.alert_history.append(alert)
                    
                    logger.warning(f"Alert triggered: {alert.message}")
                else:
                    # Update existing alert
                    existing_alert.current_value = metric.value
                    existing_alert.metadata['last_updated'] = datetime.now().isoformat()
    
    def _evaluate_condition(self, value: float, condition: str, threshold: float) -> bool:
        """Evaluate condition."""
        try:
            if ">" in condition:
                return value > threshold
            elif "<" in condition:
                return value < threshold
            elif ">=" in condition:
                return value >= threshold
            elif "<=" in condition:
                return value <= threshold
            elif "==" in condition or "=" in condition:
                return value == threshold
            else:
                return False
        except Exception as e:
            logger.error(f"Failed to evaluate condition: {e}")
            return False
    
    def get_active_alerts(self) -> List[Alert]:
        """Get active alerts."""
        return [alert for alert in self.active_alerts.values() if alert.status == AlertStatus.ACTIVE]

class AdvancedMonitoringSystem:
    """Main monitoring system."""
    
    def __init__(self):
        self.metrics_collector = SystemMetricsCollector()
        self.alert_manager = AlertManager()
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.is_running = False
        self.collection_interval = 60
    
    async def start_monitoring(self):
        """Start monitoring system."""
        self.is_running = True
        logger.info("Starting advanced monitoring system")
        
        while self.is_running:
            try:
                # Collect metrics
                metrics = self.metrics_collector.collect_all_metrics()
                
                # Store metrics in history
                for metric in metrics:
                    self.metrics_history[metric.name].append(metric)
                
                # Evaluate metrics against alert rules
                for metric in metrics:
                    self.alert_manager.evaluate_metric(metric)
                
                logger.info(f"Collected {len(metrics)} metrics")
                
                # Wait for next collection
                await asyncio.sleep(self.collection_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self.collection_interval)
    
    def stop_monitoring(self):
        """Stop monitoring system."""
        self.is_running = False
        logger.info("Stopped advanced monitoring system")
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        summary = {}
        
        for metric_name, metrics in self.metrics_history.items():
            if metrics:
                latest_metric = metrics[-1]
                summary[metric_name] = {
                    'current_value': latest_metric.value,
                    'timestamp': latest_metric.timestamp.isoformat(),
                    'description': latest_metric.description
                }
        
        return summary
    
    def get_monitoring_dashboard_data(self) -> Dict[str, Any]:
        """Get data for monitoring dashboard."""
        return {
            'metrics': self.get_metrics_summary(),
            'active_alerts': [
                {
                    'alert_id': alert.alert_id,
                    'rule_id': alert.rule_id,
                    'metric_name': alert.metric_name,
                    'current_value': alert.current_value,
                    'threshold': alert.threshold,
                    'alert_level': alert.alert_level.value,
                    'status': alert.status.value,
                    'message': alert.message,
                    'created_at': alert.created_at.isoformat()
                }
                for alert in self.alert_manager.get_active_alerts()
            ],
            'alert_rules': [
                {
                    'rule_id': rule.rule_id,
                    'name': rule.name,
                    'description': rule.description,
                    'metric_name': rule.metric_name,
                    'condition': rule.condition,
                    'threshold': rule.threshold,
                    'alert_level': rule.alert_level.value,
                    'enabled': rule.enabled
                }
                for rule in self.alert_manager.alert_rules.values()
            ],
            'system_status': {
                'monitoring_active': self.is_running,
                'total_metrics': len(self.metrics_history),
                'active_alerts_count': len(self.alert_manager.get_active_alerts()),
                'total_alert_rules': len(self.alert_manager.alert_rules)
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Create monitoring system
    monitoring_system = AdvancedMonitoringSystem()
    
    # Get dashboard data
    print("Monitoring Dashboard Data:")
    dashboard_data = monitoring_system.get_monitoring_dashboard_data()
    print(f"System Status: {dashboard_data['system_status']}")
    print(f"Active Alerts: {len(dashboard_data['active_alerts'])}")
    print(f"Alert Rules: {len(dashboard_data['alert_rules'])}")
    
    # Test metric collection
    print("\nTesting metric collection...")
    metrics = monitoring_system.metrics_collector.collect_all_metrics()
    print(f"Collected {len(metrics)} metrics")
    
    # Show some metrics
    for metric in metrics[:3]:
        print(f"  {metric.name}: {metric.value} ({metric.description})")
    
    print("\nAdvanced Monitoring System initialized successfully!")
    print("Start monitoring with: await monitoring_system.start_monitoring()")