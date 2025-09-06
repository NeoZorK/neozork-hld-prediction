# -*- coding: utf-8 -*-
"""
Advanced Monitoring System for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive monitoring with Prometheus, Grafana, and intelligent alerting.
"""

import time
import logging
import threading
import queue
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import asyncio
import aiohttp
from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    """Alert levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MetricType(Enum):
    """Metric types."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

@dataclass
class Alert:
    """Alert structure."""
    id: str
    level: AlertLevel
    title: str
    message: str
    timestamp: datetime
    source: str
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Metric:
    """Metric structure."""
    name: str
    value: float
    labels: Dict[str, str]
    timestamp: datetime
    metric_type: MetricType

class PrometheusMetrics:
    """Prometheus metrics collection."""
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.metrics = {}
        self.server_started = False
        
        # Initialize metrics
        self._init_metrics()
    
    def _init_metrics(self):
        """Initialize Prometheus metrics."""
        # Trading metrics
        self.metrics['trades_total'] = Counter(
            'neozork_trades_total',
            'Total number of trades',
            ['symbol', 'side', 'status']
        )
        
        self.metrics['trade_value'] = Histogram(
            'neozork_trade_value_usd',
            'Trade value in USD',
            ['symbol', 'side'],
            buckets=[10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
        )
        
        self.metrics['portfolio_value'] = Gauge(
            'neozork_portfolio_value_usd',
            'Current portfolio value in USD'
        )
        
        self.metrics['portfolio_return'] = Gauge(
            'neozork_portfolio_return_percent',
            'Portfolio return percentage'
        )
        
        self.metrics['positions_count'] = Gauge(
            'neozork_positions_count',
            'Number of open positions'
        )
        
        # ML model metrics
        self.metrics['model_predictions'] = Counter(
            'neozork_model_predictions_total',
            'Total number of model predictions',
            ['model_name', 'model_type']
        )
        
        self.metrics['model_accuracy'] = Gauge(
            'neozork_model_accuracy',
            'Model accuracy',
            ['model_name', 'model_type']
        )
        
        self.metrics['model_training_time'] = Histogram(
            'neozork_model_training_time_seconds',
            'Model training time in seconds',
            ['model_name', 'model_type']
        )
        
        # API metrics
        self.metrics['api_requests'] = Counter(
            'neozork_api_requests_total',
            'Total API requests',
            ['exchange', 'endpoint', 'status']
        )
        
        self.metrics['api_response_time'] = Histogram(
            'neozork_api_response_time_seconds',
            'API response time in seconds',
            ['exchange', 'endpoint'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        )
        
        # System metrics
        self.metrics['system_cpu_usage'] = Gauge(
            'neozork_system_cpu_usage_percent',
            'System CPU usage percentage'
        )
        
        self.metrics['system_memory_usage'] = Gauge(
            'neozork_system_memory_usage_percent',
            'System memory usage percentage'
        )
        
        self.metrics['system_disk_usage'] = Gauge(
            'neozork_system_disk_usage_percent',
            'System disk usage percentage'
        )
        
        # Error metrics
        self.metrics['errors_total'] = Counter(
            'neozork_errors_total',
            'Total number of errors',
            ['component', 'error_type']
        )
        
        logger.info("Prometheus metrics initialized")
    
    def start_server(self):
        """Start Prometheus metrics server."""
        if not self.server_started:
            start_http_server(self.port)
            self.server_started = True
            logger.info(f"Prometheus metrics server started on port {self.port}")
    
    def record_trade(self, symbol: str, side: str, value: float, status: str = "success"):
        """Record a trade metric."""
        self.metrics['trades_total'].labels(symbol=symbol, side=side, status=status).inc()
        self.metrics['trade_value'].labels(symbol=symbol, side=side).observe(value)
    
    def update_portfolio(self, value: float, return_pct: float, positions_count: int):
        """Update portfolio metrics."""
        self.metrics['portfolio_value'].set(value)
        self.metrics['portfolio_return'].set(return_pct)
        self.metrics['positions_count'].set(positions_count)
    
    def record_model_prediction(self, model_name: str, model_type: str, accuracy: float):
        """Record model prediction metric."""
        self.metrics['model_predictions'].labels(model_name=model_name, model_type=model_type).inc()
        self.metrics['model_accuracy'].labels(model_name=model_name, model_type=model_type).set(accuracy)
    
    def record_model_training(self, model_name: str, model_type: str, training_time: float):
        """Record model training metric."""
        self.metrics['model_training_time'].labels(model_name=model_name, model_type=model_type).observe(training_time)
    
    def record_api_request(self, exchange: str, endpoint: str, response_time: float, status: str = "success"):
        """Record API request metric."""
        self.metrics['api_requests'].labels(exchange=exchange, endpoint=endpoint, status=status).inc()
        self.metrics['api_response_time'].labels(exchange=exchange, endpoint=endpoint).observe(response_time)
    
    def update_system_metrics(self, cpu_usage: float, memory_usage: float, disk_usage: float):
        """Update system metrics."""
        self.metrics['system_cpu_usage'].set(cpu_usage)
        self.metrics['system_memory_usage'].set(memory_usage)
        self.metrics['system_disk_usage'].set(disk_usage)
    
    def record_error(self, component: str, error_type: str):
        """Record error metric."""
        self.metrics['errors_total'].labels(component=component, error_type=error_type).inc()

class AlertManager:
    """Alert management system."""
    
    def __init__(self):
        self.alerts = []
        self.alert_rules = []
        self.alert_handlers = []
        self.alert_queue = queue.Queue()
        self.is_running = False
        self.alert_thread = None
    
    def add_alert_rule(self, name: str, condition: Callable, level: AlertLevel, 
                      title: str, message: str, source: str):
        """Add an alert rule."""
        rule = {
            'name': name,
            'condition': condition,
            'level': level,
            'title': title,
            'message': message,
            'source': source
        }
        self.alert_rules.append(rule)
        logger.info(f"Added alert rule: {name}")
    
    def add_alert_handler(self, handler: Callable):
        """Add an alert handler."""
        self.alert_handlers.append(handler)
        logger.info("Added alert handler")
    
    def create_alert(self, level: AlertLevel, title: str, message: str, 
                    source: str, metadata: Dict[str, Any] = None) -> Alert:
        """Create a new alert."""
        alert = Alert(
            id=f"alert_{int(time.time())}_{len(self.alerts)}",
            level=level,
            title=title,
            message=message,
            timestamp=datetime.now(),
            source=source,
            metadata=metadata or {}
        )
        
        self.alerts.append(alert)
        self.alert_queue.put(alert)
        
        logger.warning(f"Alert created: {alert.title} ({alert.level.value})")
        return alert
    
    def resolve_alert(self, alert_id: str):
        """Resolve an alert."""
        for alert in self.alerts:
            if alert.id == alert_id and not alert.resolved:
                alert.resolved = True
                alert.resolved_at = datetime.now()
                logger.info(f"Alert resolved: {alert.title}")
                break
    
    def start_monitoring(self):
        """Start alert monitoring."""
        if not self.is_running:
            self.is_running = True
            self.alert_thread = threading.Thread(target=self._monitor_alerts, daemon=True)
            self.alert_thread.start()
            logger.info("Alert monitoring started")
    
    def stop_monitoring(self):
        """Stop alert monitoring."""
        self.is_running = False
        if self.alert_thread:
            self.alert_thread.join(timeout=5)
        logger.info("Alert monitoring stopped")
    
    def _monitor_alerts(self):
        """Monitor alert rules and process alerts."""
        while self.is_running:
            try:
                # Check alert rules
                for rule in self.alert_rules:
                    try:
                        if rule['condition']():
                            # Check if alert already exists
                            existing_alert = None
                            for alert in self.alerts:
                                if (alert.source == rule['source'] and 
                                    alert.title == rule['title'] and 
                                    not alert.resolved):
                                    existing_alert = alert
                                    break
                            
                            if not existing_alert:
                                self.create_alert(
                                    rule['level'],
                                    rule['title'],
                                    rule['message'],
                                    rule['source']
                                )
                    except Exception as e:
                        logger.error(f"Error checking alert rule {rule['name']}: {e}")
                
                # Process alert queue
                while not self.alert_queue.empty():
                    try:
                        alert = self.alert_queue.get_nowait()
                        for handler in self.alert_handlers:
                            try:
                                handler(alert)
                            except Exception as e:
                                logger.error(f"Error in alert handler: {e}")
                    except queue.Empty:
                        break
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in alert monitoring: {e}")
                time.sleep(30)
    
    def get_active_alerts(self) -> List[Alert]:
        """Get active (unresolved) alerts."""
        return [alert for alert in self.alerts if not alert.resolved]
    
    def get_alert_stats(self) -> Dict[str, Any]:
        """Get alert statistics."""
        total_alerts = len(self.alerts)
        active_alerts = len(self.get_active_alerts())
        
        level_counts = {}
        for alert in self.alerts:
            level = alert.level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'resolved_alerts': total_alerts - active_alerts,
            'level_counts': level_counts
        }

class GrafanaDashboard:
    """Grafana dashboard management."""
    
    def __init__(self, grafana_url: str, api_key: str):
        self.grafana_url = grafana_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    async def create_dashboard(self, dashboard_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Grafana dashboard."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.grafana_url}/api/dashboards/db"
                
                async with session.post(url, json=dashboard_config, headers=self.headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Dashboard created: {dashboard_config.get('dashboard', {}).get('title', 'Unknown')}")
                        return {
                            'status': 'success',
                            'dashboard_id': result.get('id'),
                            'url': result.get('url'),
                            'message': 'Dashboard created successfully'
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'status': 'error',
                            'message': f'Failed to create dashboard: {error_text}'
                        }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to create dashboard: {str(e)}'
            }
    
    def generate_trading_dashboard_config(self) -> Dict[str, Any]:
        """Generate trading dashboard configuration."""
        return {
            'dashboard': {
                'title': 'NeoZork Trading Dashboard',
                'tags': ['trading', 'neozork', 'ml'],
                'timezone': 'browser',
                'panels': [
                    {
                        'title': 'Portfolio Value',
                        'type': 'stat',
                        'targets': [
                            {
                                'expr': 'neozork_portfolio_value_usd',
                                'legendFormat': 'Portfolio Value (USD)'
                            }
                        ],
                        'gridPos': {'h': 8, 'w': 12, 'x': 0, 'y': 0}
                    },
                    {
                        'title': 'Portfolio Return',
                        'type': 'stat',
                        'targets': [
                            {
                                'expr': 'neozork_portfolio_return_percent',
                                'legendFormat': 'Return (%)'
                            }
                        ],
                        'gridPos': {'h': 8, 'w': 12, 'x': 12, 'y': 0}
                    },
                    {
                        'title': 'Trades Over Time',
                        'type': 'graph',
                        'targets': [
                            {
                                'expr': 'rate(neozork_trades_total[5m])',
                                'legendFormat': 'Trades/sec'
                            }
                        ],
                        'gridPos': {'h': 8, 'w': 24, 'x': 0, 'y': 8}
                    },
                    {
                        'title': 'Model Accuracy',
                        'type': 'graph',
                        'targets': [
                            {
                                'expr': 'neozork_model_accuracy',
                                'legendFormat': '{{model_name}} ({{model_type}})'
                            }
                        ],
                        'gridPos': {'h': 8, 'w': 12, 'x': 0, 'y': 16}
                    },
                    {
                        'title': 'API Response Time',
                        'type': 'graph',
                        'targets': [
                            {
                                'expr': 'histogram_quantile(0.95, rate(neozork_api_response_time_seconds_bucket[5m]))',
                                'legendFormat': '95th percentile'
                            }
                        ],
                        'gridPos': {'h': 8, 'w': 12, 'x': 12, 'y': 16}
                    }
                ],
                'time': {
                    'from': 'now-1h',
                    'to': 'now'
                },
                'refresh': '5s'
            }
        }

class AdvancedMonitoringSystem:
    """Advanced monitoring system with Prometheus, Grafana, and alerting."""
    
    def __init__(self, prometheus_port: int = 8000, grafana_url: str = None, 
                 grafana_api_key: str = None):
        self.prometheus = PrometheusMetrics(prometheus_port)
        self.alert_manager = AlertManager()
        self.grafana = None
        
        if grafana_url and grafana_api_key:
            self.grafana = GrafanaDashboard(grafana_url, grafana_api_key)
        
        self.is_running = False
        self.monitoring_thread = None
        
        # Setup default alert rules
        self._setup_default_alerts()
        
        # Setup default alert handlers
        self._setup_default_handlers()
    
    def _setup_default_alerts(self):
        """Setup default alert rules."""
        # Portfolio alerts
        self.alert_manager.add_alert_rule(
            name="portfolio_loss_alert",
            condition=lambda: self._check_portfolio_loss(),
            level=AlertLevel.WARNING,
            title="Portfolio Loss Alert",
            message="Portfolio has lost more than 5%",
            source="portfolio_monitor"
        )
        
        # API alerts
        self.alert_manager.add_alert_rule(
            name="api_error_rate_alert",
            condition=lambda: self._check_api_error_rate(),
            level=AlertLevel.ERROR,
            title="High API Error Rate",
            message="API error rate is above 10%",
            source="api_monitor"
        )
        
        # System alerts
        self.alert_manager.add_alert_rule(
            name="high_cpu_usage_alert",
            condition=lambda: self._check_cpu_usage(),
            level=AlertLevel.WARNING,
            title="High CPU Usage",
            message="CPU usage is above 80%",
            source="system_monitor"
        )
    
    def _setup_default_handlers(self):
        """Setup default alert handlers."""
        def log_alert_handler(alert: Alert):
            logger.warning(f"ALERT [{alert.level.value.upper()}] {alert.title}: {alert.message}")
        
        def webhook_alert_handler(alert: Alert):
            # In real implementation, this would send to webhook
            logger.info(f"Webhook alert: {alert.title}")
        
        self.alert_manager.add_alert_handler(log_alert_handler)
        self.alert_manager.add_alert_handler(webhook_alert_handler)
    
    def _check_portfolio_loss(self) -> bool:
        """Check if portfolio has significant loss."""
        # Simulate portfolio loss check
        return np.random.random() < 0.1  # 10% chance of triggering
    
    def _check_api_error_rate(self) -> bool:
        """Check if API error rate is high."""
        # Simulate API error rate check
        return np.random.random() < 0.05  # 5% chance of triggering
    
    def _check_cpu_usage(self) -> bool:
        """Check if CPU usage is high."""
        # Simulate CPU usage check
        return np.random.random() < 0.15  # 15% chance of triggering
    
    def start(self):
        """Start the monitoring system."""
        if not self.is_running:
            self.is_running = True
            
            # Start Prometheus server
            self.prometheus.start_server()
            
            # Start alert monitoring
            self.alert_manager.start_monitoring()
            
            # Start system monitoring thread
            self.monitoring_thread = threading.Thread(target=self._monitor_system, daemon=True)
            self.monitoring_thread.start()
            
            logger.info("Advanced monitoring system started")
    
    def stop(self):
        """Stop the monitoring system."""
        self.is_running = False
        
        # Stop alert monitoring
        self.alert_manager.stop_monitoring()
        
        # Stop system monitoring thread
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        logger.info("Advanced monitoring system stopped")
    
    def _monitor_system(self):
        """Monitor system metrics."""
        while self.is_running:
            try:
                # Simulate system metrics
                cpu_usage = np.random.uniform(20, 90)
                memory_usage = np.random.uniform(30, 80)
                disk_usage = np.random.uniform(40, 70)
                
                self.prometheus.update_system_metrics(cpu_usage, memory_usage, disk_usage)
                
                time.sleep(30)  # Update every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in system monitoring: {e}")
                time.sleep(60)
    
    def record_trading_activity(self, symbol: str, side: str, value: float, status: str = "success"):
        """Record trading activity."""
        self.prometheus.record_trade(symbol, side, value, status)
    
    def update_portfolio_metrics(self, value: float, return_pct: float, positions_count: int):
        """Update portfolio metrics."""
        self.prometheus.update_portfolio(value, return_pct, positions_count)
    
    def record_model_activity(self, model_name: str, model_type: str, accuracy: float, training_time: float):
        """Record model activity."""
        self.prometheus.record_model_prediction(model_name, model_type, accuracy)
        self.prometheus.record_model_training(model_name, model_type, training_time)
    
    def record_api_activity(self, exchange: str, endpoint: str, response_time: float, status: str = "success"):
        """Record API activity."""
        self.prometheus.record_api_request(exchange, endpoint, response_time, status)
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get monitoring system status."""
        alert_stats = self.alert_manager.get_alert_stats()
        
        return {
            'status': 'running' if self.is_running else 'stopped',
            'prometheus_port': self.prometheus.port,
            'prometheus_server': self.prometheus.server_started,
            'alert_monitoring': self.alert_manager.is_running,
            'grafana_configured': self.grafana is not None,
            'alert_stats': alert_stats,
            'active_alerts': len(self.alert_manager.get_active_alerts())
        }
    
    async def setup_grafana_dashboard(self) -> Dict[str, Any]:
        """Setup Grafana dashboard."""
        if not self.grafana:
            return {
                'status': 'error',
                'message': 'Grafana not configured'
            }
        
        dashboard_config = self.grafana.generate_trading_dashboard_config()
        return await self.grafana.create_dashboard(dashboard_config)

# Example usage and testing
async def test_advanced_monitoring():
    """Test advanced monitoring system."""
    print("🧪 Testing Advanced Monitoring System...")
    
    # Create monitoring system
    monitoring = AdvancedMonitoringSystem(
        prometheus_port=8001,
        grafana_url="http://localhost:3000",
        grafana_api_key="demo_api_key"
    )
    
    # Start monitoring
    monitoring.start()
    print("  • Monitoring system started")
    
    # Simulate some activity
    print("  • Simulating trading activity...")
    monitoring.record_trading_activity("BTCUSDT", "buy", 1000.0)
    monitoring.record_trading_activity("ETHUSDT", "sell", 500.0)
    
    print("  • Simulating portfolio updates...")
    monitoring.update_portfolio_metrics(10000.0, 5.2, 3)
    
    print("  • Simulating model activity...")
    monitoring.record_model_activity("model_1", "random_forest", 0.85, 120.5)
    
    print("  • Simulating API activity...")
    monitoring.record_api_activity("binance", "klines", 0.5)
    
    # Wait a bit for metrics to be recorded
    time.sleep(2)
    
    # Get status
    status = monitoring.get_monitoring_status()
    print(f"  • Monitoring status: {status['status']}")
    print(f"  • Prometheus server: {'✅' if status['prometheus_server'] else '❌'}")
    print(f"  • Alert monitoring: {'✅' if status['alert_monitoring'] else '❌'}")
    print(f"  • Active alerts: {status['active_alerts']}")
    
    # Test Grafana dashboard setup
    if monitoring.grafana:
        print("  • Testing Grafana dashboard setup...")
        dashboard_result = await monitoring.setup_grafana_dashboard()
        print(f"    Grafana dashboard: {'✅' if dashboard_result['status'] == 'success' else '❌'}")
    
    # Stop monitoring
    monitoring.stop()
    print("  • Monitoring system stopped")
    
    print("✅ Advanced Monitoring System test completed!")
    
    return monitoring

if __name__ == "__main__":
    asyncio.run(test_advanced_monitoring())
