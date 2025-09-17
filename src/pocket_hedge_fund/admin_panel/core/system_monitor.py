"""
System Monitor

Monitors system health, performance, and metrics.
"""

import asyncio
import logging
import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal

from ..models.admin_models import SystemMetrics, AdminAlert, AdminAlertLevel

logger = logging.getLogger(__name__)


class SystemMonitor:
    """
    Monitors system health, performance, and metrics.
    """
    
    def __init__(self, db_manager=None):
        """Initialize system monitor."""
        self.db_manager = db_manager
        self.metrics_history = []
        self.alerts = []
        self.is_monitoring = False
        self.monitoring_task = None
        self.alert_thresholds = {
            'cpu_usage': 80.0,
            'memory_usage': 85.0,
            'disk_usage': 90.0,
            'response_time': 1000.0,  # milliseconds
            'error_rate': 5.0,  # percentage
            'queue_size': 1000
        }
        self.health_status = "unknown"
        self.last_health_check = None
    
    async def initialize(self):
        """Initialize system monitor."""
        try:
            # Start monitoring
            await self.start_monitoring()
            
            logger.info("System monitor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize system monitor: {e}")
            raise
    
    async def start_monitoring(self):
        """Start system monitoring."""
        try:
            if self.is_monitoring:
                return
            
            self.is_monitoring = True
            self.monitoring_task = asyncio.create_task(self._monitoring_loop())
            
            logger.info("Started system monitoring")
        except Exception as e:
            logger.error(f"Failed to start monitoring: {e}")
            raise
    
    async def stop_monitoring(self):
        """Stop system monitoring."""
        try:
            if not self.is_monitoring:
                return
            
            self.is_monitoring = False
            
            if self.monitoring_task:
                self.monitoring_task.cancel()
                try:
                    await self.monitoring_task
                except asyncio.CancelledError:
                    pass
            
            logger.info("Stopped system monitoring")
        except Exception as e:
            logger.error(f"Failed to stop monitoring: {e}")
    
    async def _monitoring_loop(self):
        """Main monitoring loop."""
        try:
            while self.is_monitoring:
                try:
                    # Collect metrics
                    metrics = await self._collect_metrics()
                    
                    # Store metrics
                    self.metrics_history.append(metrics)
                    
                    # Keep only last 1000 metrics
                    if len(self.metrics_history) > 1000:
                        self.metrics_history = self.metrics_history[-1000:]
                    
                    # Check for alerts
                    await self._check_alerts(metrics)
                    
                    # Update health status
                    await self._update_health_status(metrics)
                    
                    # Wait before next collection
                    await asyncio.sleep(30)  # Collect every 30 seconds
                    
                except Exception as e:
                    logger.error(f"Monitoring loop error: {e}")
                    await asyncio.sleep(30)
                    
        except Exception as e:
            logger.error(f"Monitoring loop failed: {e}")
    
    async def _collect_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        try:
            # Get CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Get memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Get disk usage
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            
            # Get network I/O
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            # Get active connections
            connections = len(psutil.net_connections())
            
            # Mock response time (in a real system, this would be measured)
            response_time = 150.0  # milliseconds
            
            # Mock error rate
            error_rate = 0.5  # percentage
            
            # Mock throughput
            throughput = 1250.7  # requests per second
            
            # Mock queue size
            queue_size = 25
            
            # Mock cache hit rate
            cache_hit_rate = 89.3  # percentage
            
            # Mock database connections
            database_connections = 15
            
            metrics = SystemMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                network_io=network_io,
                active_connections=connections,
                response_time=response_time,
                error_rate=error_rate,
                throughput=throughput,
                queue_size=queue_size,
                cache_hit_rate=cache_hit_rate,
                database_connections=database_connections
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect metrics: {e}")
            # Return default metrics on error
            return SystemMetrics(
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_io={},
                active_connections=0,
                response_time=0.0,
                error_rate=0.0,
                throughput=0.0,
                queue_size=0,
                cache_hit_rate=0.0,
                database_connections=0
            )
    
    async def _check_alerts(self, metrics: SystemMetrics):
        """Check for alert conditions."""
        try:
            current_time = datetime.now()
            
            # Check CPU usage
            if metrics.cpu_usage > self.alert_thresholds['cpu_usage']:
                await self._create_alert(
                    title="High CPU Usage",
                    message=f"CPU usage is {metrics.cpu_usage:.1f}% (threshold: {self.alert_thresholds['cpu_usage']}%)",
                    level=AdminAlertLevel.WARNING,
                    category="performance",
                    source="system_monitor",
                    metadata={"cpu_usage": metrics.cpu_usage, "threshold": self.alert_thresholds['cpu_usage']}
                )
            
            # Check memory usage
            if metrics.memory_usage > self.alert_thresholds['memory_usage']:
                await self._create_alert(
                    title="High Memory Usage",
                    message=f"Memory usage is {metrics.memory_usage:.1f}% (threshold: {self.alert_thresholds['memory_usage']}%)",
                    level=AdminAlertLevel.WARNING,
                    category="performance",
                    source="system_monitor",
                    metadata={"memory_usage": metrics.memory_usage, "threshold": self.alert_thresholds['memory_usage']}
                )
            
            # Check disk usage
            if metrics.disk_usage > self.alert_thresholds['disk_usage']:
                await self._create_alert(
                    title="High Disk Usage",
                    message=f"Disk usage is {metrics.disk_usage:.1f}% (threshold: {self.alert_thresholds['disk_usage']}%)",
                    level=AdminAlertLevel.ERROR,
                    category="storage",
                    source="system_monitor",
                    metadata={"disk_usage": metrics.disk_usage, "threshold": self.alert_thresholds['disk_usage']}
                )
            
            # Check response time
            if metrics.response_time > self.alert_thresholds['response_time']:
                await self._create_alert(
                    title="High Response Time",
                    message=f"Response time is {metrics.response_time:.1f}ms (threshold: {self.alert_thresholds['response_time']}ms)",
                    level=AdminAlertLevel.WARNING,
                    category="performance",
                    source="system_monitor",
                    metadata={"response_time": metrics.response_time, "threshold": self.alert_thresholds['response_time']}
                )
            
            # Check error rate
            if metrics.error_rate > self.alert_thresholds['error_rate']:
                await self._create_alert(
                    title="High Error Rate",
                    message=f"Error rate is {metrics.error_rate:.1f}% (threshold: {self.alert_thresholds['error_rate']}%)",
                    level=AdminAlertLevel.ERROR,
                    category="errors",
                    source="system_monitor",
                    metadata={"error_rate": metrics.error_rate, "threshold": self.alert_thresholds['error_rate']}
                )
            
            # Check queue size
            if metrics.queue_size > self.alert_thresholds['queue_size']:
                await self._create_alert(
                    title="High Queue Size",
                    message=f"Queue size is {metrics.queue_size} (threshold: {self.alert_thresholds['queue_size']})",
                    level=AdminAlertLevel.WARNING,
                    category="performance",
                    source="system_monitor",
                    metadata={"queue_size": metrics.queue_size, "threshold": self.alert_thresholds['queue_size']}
                )
            
        except Exception as e:
            logger.error(f"Failed to check alerts: {e}")
    
    async def _create_alert(
        self,
        title: str,
        message: str,
        level: AdminAlertLevel,
        category: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Create system alert."""
        try:
            # Check if similar alert already exists
            existing_alert = None
            for alert in self.alerts:
                if (alert.title == title and 
                    alert.level == level and 
                    alert.is_active and 
                    not alert.is_acknowledged):
                    existing_alert = alert
                    break
            
            if existing_alert:
                # Update existing alert timestamp
                existing_alert.created_at = datetime.now()
                return
            
            # Create new alert
            alert = AdminAlert(
                title=title,
                message=message,
                level=level,
                category=category,
                source=source,
                metadata=metadata
            )
            
            self.alerts.append(alert)
            
            # Keep only last 1000 alerts
            if len(self.alerts) > 1000:
                self.alerts = self.alerts[-1000:]
            
            logger.warning(f"Created alert: {title} - {message}")
            
        except Exception as e:
            logger.error(f"Failed to create alert: {e}")
    
    async def _update_health_status(self, metrics: SystemMetrics):
        """Update overall system health status."""
        try:
            # Determine health status based on metrics
            if (metrics.cpu_usage > 90 or 
                metrics.memory_usage > 95 or 
                metrics.disk_usage > 95 or 
                metrics.error_rate > 10):
                self.health_status = "critical"
            elif (metrics.cpu_usage > 80 or 
                  metrics.memory_usage > 85 or 
                  metrics.disk_usage > 90 or 
                  metrics.error_rate > 5):
                self.health_status = "warning"
            else:
                self.health_status = "healthy"
            
            self.last_health_check = datetime.now()
            
        except Exception as e:
            logger.error(f"Failed to update health status: {e}")
            self.health_status = "unknown"
    
    async def get_current_metrics(self) -> SystemMetrics:
        """Get current system metrics."""
        try:
            if not self.metrics_history:
                return await self._collect_metrics()
            
            return self.metrics_history[-1]
        except Exception as e:
            logger.error(f"Failed to get current metrics: {e}")
            return await self._collect_metrics()
    
    async def get_metrics_history(
        self,
        hours: int = 24,
        limit: int = 100
    ) -> List[SystemMetrics]:
        """Get metrics history."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter metrics by time
            filtered_metrics = [
                m for m in self.metrics_history
                if m.timestamp >= cutoff_time
            ]
            
            # Limit results
            return filtered_metrics[-limit:] if limit else filtered_metrics
            
        except Exception as e:
            logger.error(f"Failed to get metrics history: {e}")
            return []
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get system health status."""
        try:
            current_metrics = await self.get_current_metrics()
            
            return {
                'status': self.health_status,
                'last_check': self.last_health_check.isoformat() if self.last_health_check else None,
                'metrics': {
                    'cpu_usage': current_metrics.cpu_usage,
                    'memory_usage': current_metrics.memory_usage,
                    'disk_usage': current_metrics.disk_usage,
                    'response_time': current_metrics.response_time,
                    'error_rate': current_metrics.error_rate,
                    'queue_size': current_metrics.queue_size
                },
                'thresholds': self.alert_thresholds,
                'active_alerts': len([a for a in self.alerts if a.is_active and not a.is_acknowledged])
            }
        except Exception as e:
            logger.error(f"Failed to get system health: {e}")
            return {
                'status': 'unknown',
                'error': str(e)
            }
    
    async def get_system_health_report(self) -> Dict[str, Any]:
        """Get comprehensive system health report."""
        try:
            current_metrics = await self.get_current_metrics()
            metrics_history = await self.get_metrics_history(hours=24)
            
            # Calculate averages
            if metrics_history:
                avg_cpu = sum(m.cpu_usage for m in metrics_history) / len(metrics_history)
                avg_memory = sum(m.memory_usage for m in metrics_history) / len(metrics_history)
                avg_disk = sum(m.disk_usage for m in metrics_history) / len(metrics_history)
                avg_response_time = sum(m.response_time for m in metrics_history) / len(metrics_history)
                avg_error_rate = sum(m.error_rate for m in metrics_history) / len(metrics_history)
            else:
                avg_cpu = avg_memory = avg_disk = avg_response_time = avg_error_rate = 0.0
            
            # Get active alerts
            active_alerts = [a for a in self.alerts if a.is_active and not a.is_acknowledged]
            
            # Get recent alerts (last 24 hours)
            recent_alerts = [
                a for a in self.alerts
                if a.created_at >= datetime.now() - timedelta(hours=24)
            ]
            
            return {
                'report_generated_at': datetime.now().isoformat(),
                'health_status': self.health_status,
                'current_metrics': {
                    'cpu_usage': current_metrics.cpu_usage,
                    'memory_usage': current_metrics.memory_usage,
                    'disk_usage': current_metrics.disk_usage,
                    'response_time': current_metrics.response_time,
                    'error_rate': current_metrics.error_rate,
                    'queue_size': current_metrics.queue_size,
                    'active_connections': current_metrics.active_connections,
                    'throughput': current_metrics.throughput,
                    'cache_hit_rate': current_metrics.cache_hit_rate,
                    'database_connections': current_metrics.database_connections
                },
                'average_metrics_24h': {
                    'cpu_usage': avg_cpu,
                    'memory_usage': avg_memory,
                    'disk_usage': avg_disk,
                    'response_time': avg_response_time,
                    'error_rate': avg_error_rate
                },
                'alerts': {
                    'active_count': len(active_alerts),
                    'recent_count': len(recent_alerts),
                    'active_alerts': [
                        {
                            'title': a.title,
                            'level': a.level.value,
                            'category': a.category,
                            'created_at': a.created_at.isoformat()
                        }
                        for a in active_alerts
                    ]
                },
                'thresholds': self.alert_thresholds,
                'monitoring_status': {
                    'is_monitoring': self.is_monitoring,
                    'metrics_collected': len(self.metrics_history),
                    'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None
                }
            }
        except Exception as e:
            logger.error(f"Failed to get system health report: {e}")
            raise
    
    async def get_alerts(
        self,
        level: Optional[AdminAlertLevel] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: int = 100
    ) -> List[AdminAlert]:
        """Get system alerts with optional filtering."""
        try:
            alerts = self.alerts.copy()
            
            # Apply filters
            if level:
                alerts = [a for a in alerts if a.level == level]
            
            if category:
                alerts = [a for a in alerts if a.category == category]
            
            if is_active is not None:
                alerts = [a for a in alerts if a.is_active == is_active]
            
            # Sort by creation time (newest first)
            alerts.sort(key=lambda x: x.created_at, reverse=True)
            
            # Limit results
            return alerts[:limit] if limit else alerts
            
        except Exception as e:
            logger.error(f"Failed to get alerts: {e}")
            return []
    
    async def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge system alert."""
        try:
            for alert in self.alerts:
                if alert.id == alert_id:
                    alert.is_acknowledged = True
                    alert.acknowledged_by = acknowledged_by
                    alert.acknowledged_at = datetime.now()
                    logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Failed to acknowledge alert: {e}")
            return False
    
    async def resolve_alert(self, alert_id: str, resolved_by: str, resolution_notes: str = None) -> bool:
        """Resolve system alert."""
        try:
            for alert in self.alerts:
                if alert.id == alert_id:
                    alert.is_active = False
                    alert.resolved_at = datetime.now()
                    alert.resolved_by = resolved_by
                    alert.resolution_notes = resolution_notes
                    logger.info(f"Alert {alert_id} resolved by {resolved_by}")
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Failed to resolve alert: {e}")
            return False
    
    async def update_alert_thresholds(self, thresholds: Dict[str, float]):
        """Update alert thresholds."""
        try:
            for key, value in thresholds.items():
                if key in self.alert_thresholds:
                    self.alert_thresholds[key] = value
            
            logger.info("Updated alert thresholds")
        except Exception as e:
            logger.error(f"Failed to update alert thresholds: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup system monitor resources."""
        try:
            await self.stop_monitoring()
            self.metrics_history.clear()
            self.alerts.clear()
            self.health_status = "unknown"
            self.last_health_check = None
            logger.info("System monitor cleanup completed")
        except Exception as e:
            logger.error(f"Error during system monitor cleanup: {e}")
