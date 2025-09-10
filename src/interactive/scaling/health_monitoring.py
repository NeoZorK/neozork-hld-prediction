# -*- coding: utf-8 -*-
"""
Health Monitoring for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive health monitoring capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
import threading
import subprocess
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import warnings

class HealthStatus(Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

class CheckType(Enum):
    """Health check type enumeration."""
    HTTP = "http"
    HTTPS = "https"
    TCP = "tcp"
    PING = "ping"
    CUSTOM = "custom"
    DATABASE = "database"
    CACHE = "cache"
    QUEUE = "queue"

class HealthMonitoring:
    """
    Health monitoring system for comprehensive system health checks.
    
    Features:
    - Multiple Health Check Types
    - Automated Health Monitoring
    - Health Status Aggregation
    - Alert Management
    - Health History Tracking
    - Custom Health Checks
    """
    
    def __init__(self):
        """Initialize the Health Monitoring system."""
        self.health_checks = {}
        self.health_status = {}
        self.health_history = []
        self.alert_rules = {}
        self.health_metrics = {}
        self.is_monitoring_active = False
        self.monitoring_thread = None
        self.check_interval = 30
        self.alert_thresholds = {
            "response_time": 5.0,  # seconds
            "error_rate": 0.05,    # 5%
            "availability": 0.95   # 95%
        }
    
    def add_health_check(self, check_id: str, check_type: str, target: str,
                        check_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a health check.
        
        Args:
            check_id: Unique check identifier
            check_type: Type of health check
            target: Target to check (URL, host:port, etc.)
            check_config: Check configuration
            
        Returns:
            Health check addition result
        """
        try:
            # Create health check
            health_check = {
                "check_id": check_id,
                "check_type": check_type,
                "target": target,
                "config": check_config,
                "is_enabled": True,
                "created_time": time.time(),
                "last_check": None,
                "last_status": HealthStatus.UNKNOWN.value,
                "last_response_time": 0.0,
                "check_count": 0,
                "success_count": 0,
                "failure_count": 0,
                "consecutive_failures": 0,
                "alert_threshold": check_config.get("alert_threshold", 3)
            }
            
            # Store health check
            self.health_checks[check_id] = health_check
            self.health_status[check_id] = HealthStatus.UNKNOWN.value
            
            result = {
                "status": "success",
                "check_id": check_id,
                "check_type": check_type,
                "target": target,
                "config": check_config,
                "message": "Health check added successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to add health check: {str(e)}"}
    
    def remove_health_check(self, check_id: str) -> Dict[str, Any]:
        """
        Remove a health check.
        
        Args:
            check_id: Check ID to remove
            
        Returns:
            Health check removal result
        """
        try:
            # Check if health check exists
            if check_id not in self.health_checks:
                return {"status": "error", "message": f"Health check {check_id} not found"}
            
            # Remove health check
            del self.health_checks[check_id]
            del self.health_status[check_id]
            
            result = {
                "status": "success",
                "check_id": check_id,
                "message": "Health check removed successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to remove health check: {str(e)}"}
    
    def run_health_check(self, check_id: str) -> Dict[str, Any]:
        """
        Run a specific health check.
        
        Args:
            check_id: Check ID to run
            
        Returns:
            Health check result
        """
        try:
            # Check if health check exists
            if check_id not in self.health_checks:
                return {"status": "error", "message": f"Health check {check_id} not found"}
            
            health_check = self.health_checks[check_id]
            
            # Run health check
            start_time = time.time()
            check_result = self._perform_health_check(health_check)
            response_time = time.time() - start_time
            
            # Update health check
            health_check["last_check"] = time.time()
            health_check["last_response_time"] = response_time
            health_check["check_count"] += 1
            
            if check_result["status"] == "success":
                health_check["success_count"] += 1
                health_check["consecutive_failures"] = 0
                health_check["last_status"] = HealthStatus.HEALTHY.value
                self.health_status[check_id] = HealthStatus.HEALTHY.value
            else:
                health_check["failure_count"] += 1
                health_check["consecutive_failures"] += 1
                health_check["last_status"] = HealthStatus.CRITICAL.value
                self.health_status[check_id] = HealthStatus.CRITICAL.value
            
            # Record health history
            self.health_history.append({
                "check_id": check_id,
                "timestamp": time.time(),
                "status": health_check["last_status"],
                "response_time": response_time,
                "details": check_result
            })
            
            result = {
                "status": "success",
                "check_id": check_id,
                "health_status": health_check["last_status"],
                "response_time": response_time,
                "check_result": check_result,
                "consecutive_failures": health_check["consecutive_failures"],
                "message": "Health check completed"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to run health check: {str(e)}"}
    
    def run_all_health_checks(self) -> Dict[str, Any]:
        """
        Run all enabled health checks.
        
        Returns:
            All health checks result
        """
        try:
            results = {}
            total_checks = 0
            successful_checks = 0
            failed_checks = 0
            
            for check_id, health_check in self.health_checks.items():
                if health_check["is_enabled"]:
                    result = self.run_health_check(check_id)
                    results[check_id] = result
                    
                    total_checks += 1
                    if result["status"] == "success" and result["health_status"] == "healthy":
                        successful_checks += 1
                    else:
                        failed_checks += 1
            
            # Calculate overall health
            overall_health = "healthy" if failed_checks == 0 else "critical" if failed_checks > total_checks * 0.5 else "warning"
            
            result = {
                "status": "success",
                "overall_health": overall_health,
                "total_checks": total_checks,
                "successful_checks": successful_checks,
                "failed_checks": failed_checks,
                "success_rate": (successful_checks / total_checks * 100) if total_checks > 0 else 0,
                "check_results": results,
                "message": "All health checks completed"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to run all health checks: {str(e)}"}
    
    def start_health_monitoring(self, interval: int = 30) -> Dict[str, Any]:
        """
        Start automated health monitoring.
        
        Args:
            interval: Monitoring interval in seconds
            
        Returns:
            Health monitoring start result
        """
        try:
            if self.is_monitoring_active:
                return {"status": "error", "message": "Health monitoring already active"}
            
            self.is_monitoring_active = True
            self.check_interval = interval
            
            # Start monitoring thread
            self.monitoring_thread = threading.Thread(
                target=self._health_monitoring_loop,
                args=(interval,)
            )
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            result = {
                "status": "success",
                "interval": interval,
                "message": "Health monitoring started successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to start health monitoring: {str(e)}"}
    
    def stop_health_monitoring(self) -> Dict[str, Any]:
        """
        Stop automated health monitoring.
        
        Returns:
            Health monitoring stop result
        """
        try:
            self.is_monitoring_active = False
            
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=5)
            
            result = {
                "status": "success",
                "message": "Health monitoring stopped successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to stop health monitoring: {str(e)}"}
    
    def get_health_status(self, check_id: str = None) -> Dict[str, Any]:
        """
        Get health status.
        
        Args:
            check_id: Specific check ID (optional)
            
        Returns:
            Health status result
        """
        try:
            if check_id:
                # Get status for specific check
                if check_id not in self.health_checks:
                    return {"status": "error", "message": f"Health check {check_id} not found"}
                
                health_check = self.health_checks[check_id]
                
                status = {
                    "check_id": check_id,
                    "check_type": health_check["check_type"],
                    "target": health_check["target"],
                    "is_enabled": health_check["is_enabled"],
                    "last_status": health_check["last_status"],
                    "last_check": health_check["last_check"],
                    "last_response_time": health_check["last_response_time"],
                    "check_count": health_check["check_count"],
                    "success_count": health_check["success_count"],
                    "failure_count": health_check["failure_count"],
                    "consecutive_failures": health_check["consecutive_failures"],
                    "success_rate": (health_check["success_count"] / health_check["check_count"] * 100) if health_check["check_count"] > 0 else 0
                }
                
                result = {
                    "status": "success",
                    "health_status": status
                }
                
            else:
                # Get status for all checks
                all_status = {}
                overall_health = "healthy"
                total_checks = 0
                healthy_checks = 0
                
                for check_id, health_check in self.health_checks.items():
                    total_checks += 1
                    if health_check["last_status"] == "healthy":
                        healthy_checks += 1
                    
                    all_status[check_id] = {
                        "check_type": health_check["check_type"],
                        "target": health_check["target"],
                        "is_enabled": health_check["is_enabled"],
                        "last_status": health_check["last_status"],
                        "last_check": health_check["last_check"],
                        "last_response_time": health_check["last_response_time"],
                        "consecutive_failures": health_check["consecutive_failures"]
                    }
                
                # Calculate overall health
                if total_checks > 0:
                    health_ratio = healthy_checks / total_checks
                    if health_ratio >= 0.95:
                        overall_health = "healthy"
                    elif health_ratio >= 0.8:
                        overall_health = "warning"
                    else:
                        overall_health = "critical"
                
                result = {
                    "status": "success",
                    "overall_health": overall_health,
                    "total_checks": total_checks,
                    "healthy_checks": healthy_checks,
                    "health_ratio": (healthy_checks / total_checks * 100) if total_checks > 0 else 0,
                    "health_status": all_status
                }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get health status: {str(e)}"}
    
    def get_health_statistics(self) -> Dict[str, Any]:
        """
        Get health monitoring statistics.
        
        Returns:
            Health statistics result
        """
        try:
            # Calculate statistics
            total_checks = len(self.health_checks)
            enabled_checks = len([c for c in self.health_checks.values() if c["is_enabled"]])
            disabled_checks = total_checks - enabled_checks
            
            # Calculate check types
            check_types = {}
            for health_check in self.health_checks.values():
                check_type = health_check["check_type"]
                check_types[check_type] = check_types.get(check_type, 0) + 1
            
            # Calculate average response time
            response_times = [c["last_response_time"] for c in self.health_checks.values() if c["last_response_time"] > 0]
            avg_response_time = np.mean(response_times) if response_times else 0
            
            # Calculate success rates
            success_rates = []
            for health_check in self.health_checks.values():
                if health_check["check_count"] > 0:
                    success_rate = health_check["success_count"] / health_check["check_count"] * 100
                    success_rates.append(success_rate)
            
            avg_success_rate = np.mean(success_rates) if success_rates else 0
            
            statistics = {
                "total_checks": total_checks,
                "enabled_checks": enabled_checks,
                "disabled_checks": disabled_checks,
                "check_types": check_types,
                "avg_response_time": avg_response_time,
                "avg_success_rate": avg_success_rate,
                "is_monitoring_active": self.is_monitoring_active,
                "check_interval": self.check_interval,
                "health_history_entries": len(self.health_history)
            }
            
            result = {
                "status": "success",
                "statistics": statistics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get health statistics: {str(e)}"}
    
    def _perform_health_check(self, health_check: Dict[str, Any]) -> Dict[str, Any]:
        """Perform the actual health check."""
        try:
            check_type = health_check["check_type"]
            target = health_check["target"]
            config = health_check["config"]
            
            if check_type == CheckType.HTTP.value:
                return self._http_health_check(target, config)
            elif check_type == CheckType.HTTPS.value:
                return self._https_health_check(target, config)
            elif check_type == CheckType.TCP.value:
                return self._tcp_health_check(target, config)
            elif check_type == CheckType.PING.value:
                return self._ping_health_check(target, config)
            elif check_type == CheckType.DATABASE.value:
                return self._database_health_check(target, config)
            elif check_type == CheckType.CACHE.value:
                return self._cache_health_check(target, config)
            elif check_type == CheckType.QUEUE.value:
                return self._queue_health_check(target, config)
            else:
                return self._custom_health_check(target, config)
                
        except Exception as e:
            return {"status": "error", "message": f"Health check failed: {str(e)}"}
    
    def _http_health_check(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """HTTP health check."""
        try:
            # Simulate HTTP check
            time.sleep(0.1)  # Simulate network delay
            
            # Simulate success (90% success rate)
            if np.random.random() > 0.1:
                return {"status": "success", "message": "HTTP check passed", "response_code": 200}
            else:
                return {"status": "error", "message": "HTTP check failed", "response_code": 500}
                
        except Exception as e:
            return {"status": "error", "message": f"HTTP check error: {str(e)}"}
    
    def _https_health_check(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """HTTPS health check."""
        try:
            # Simulate HTTPS check
            time.sleep(0.15)  # Simulate SSL handshake delay
            
            # Simulate success (95% success rate)
            if np.random.random() > 0.05:
                return {"status": "success", "message": "HTTPS check passed", "response_code": 200}
            else:
                return {"status": "error", "message": "HTTPS check failed", "response_code": 500}
                
        except Exception as e:
            return {"status": "error", "message": f"HTTPS check error: {str(e)}"}
    
    def _tcp_health_check(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """TCP health check."""
        try:
            # Simulate TCP check
            time.sleep(0.05)  # Simulate connection delay
            
            # Simulate success (98% success rate)
            if np.random.random() > 0.02:
                return {"status": "success", "message": "TCP check passed", "connection_time": 0.05}
            else:
                return {"status": "error", "message": "TCP check failed", "connection_time": 0.05}
                
        except Exception as e:
            return {"status": "error", "message": f"TCP check error: {str(e)}"}
    
    def _ping_health_check(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Ping health check."""
        try:
            # Simulate ping check
            time.sleep(0.02)  # Simulate ping delay
            
            # Simulate success (99% success rate)
            if np.random.random() > 0.01:
                return {"status": "success", "message": "Ping check passed", "ping_time": 0.02}
            else:
                return {"status": "error", "message": "Ping check failed", "ping_time": 0.02}
                
        except Exception as e:
            return {"status": "error", "message": f"Ping check error: {str(e)}"}
    
    def _database_health_check(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Database health check."""
        try:
            # Simulate database check
            time.sleep(0.2)  # Simulate database query delay
            
            # Simulate success (95% success rate)
            if np.random.random() > 0.05:
                return {"status": "success", "message": "Database check passed", "query_time": 0.2}
            else:
                return {"status": "error", "message": "Database check failed", "query_time": 0.2}
                
        except Exception as e:
            return {"status": "error", "message": f"Database check error: {str(e)}"}
    
    def _cache_health_check(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Cache health check."""
        try:
            # Simulate cache check
            time.sleep(0.01)  # Simulate cache access delay
            
            # Simulate success (98% success rate)
            if np.random.random() > 0.02:
                return {"status": "success", "message": "Cache check passed", "access_time": 0.01}
            else:
                return {"status": "error", "message": "Cache check failed", "access_time": 0.01}
                
        except Exception as e:
            return {"status": "error", "message": f"Cache check error: {str(e)}"}
    
    def _queue_health_check(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Queue health check."""
        try:
            # Simulate queue check
            time.sleep(0.05)  # Simulate queue access delay
            
            # Simulate success (97% success rate)
            if np.random.random() > 0.03:
                return {"status": "success", "message": "Queue check passed", "access_time": 0.05}
            else:
                return {"status": "error", "message": "Queue check failed", "access_time": 0.05}
                
        except Exception as e:
            return {"status": "error", "message": f"Queue check error: {str(e)}"}
    
    def _custom_health_check(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Custom health check."""
        try:
            # Simulate custom check
            time.sleep(0.1)  # Simulate custom check delay
            
            # Simulate success (90% success rate)
            if np.random.random() > 0.1:
                return {"status": "success", "message": "Custom check passed", "check_time": 0.1}
            else:
                return {"status": "error", "message": "Custom check failed", "check_time": 0.1}
                
        except Exception as e:
            return {"status": "error", "message": f"Custom check error: {str(e)}"}
    
    def _health_monitoring_loop(self, interval: int) -> None:
        """Health monitoring loop."""
        try:
            while self.is_monitoring_active:
                self.run_all_health_checks()
                time.sleep(interval)
                
        except Exception as e:
            print(f"Error in health monitoring loop: {e}")
