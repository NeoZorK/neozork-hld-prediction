# -*- coding: utf-8 -*-
"""
Prometheus Integration for NeoZork Interactive ML Trading Strategy Development.

This module provides Prometheus metrics collection and monitoring capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
from typing import Dict, Any, Optional, List, Tuple
import warnings

class PrometheusIntegration:
    """
    Prometheus integration system for metrics collection.
    
    Features:
    - Metrics Collection
    - Custom Metrics
    - Performance Monitoring
    - Trading Metrics
    - System Metrics
    - Alerting Integration
    """
    
    def __init__(self):
        """Initialize the Prometheus Integration system."""
        self.metrics = {}
        self.custom_metrics = {}
        self.performance_metrics = {}
        self.trading_metrics = {}
        self.system_metrics = {}
        self.alert_rules = {}
    
    def collect_trading_metrics(self, trading_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect trading-related metrics.
        
        Args:
            trading_data: Trading data dictionary
            
        Returns:
            Trading metrics collection result
        """
        try:
            # Extract trading metrics
            metrics = {
                "trading_orders_total": trading_data.get("total_orders", 0),
                "trading_orders_filled": trading_data.get("filled_orders", 0),
                "trading_orders_canceled": trading_data.get("canceled_orders", 0),
                "trading_volume_total": trading_data.get("total_volume", 0.0),
                "trading_pnl_total": trading_data.get("total_pnl", 0.0),
                "trading_pnl_percentage": trading_data.get("return_percentage", 0.0),
                "trading_drawdown_max": trading_data.get("max_drawdown", 0.0),
                "trading_sharpe_ratio": trading_data.get("sharpe_ratio", 0.0),
                "trading_win_rate": trading_data.get("win_rate", 0.0),
                "trading_avg_trade_duration": trading_data.get("avg_trade_duration", 0.0)
            }
            
            # Add labels
            labels = {
                "strategy": trading_data.get("strategy_name", "unknown"),
                "exchange": trading_data.get("exchange", "unknown"),
                "symbol": trading_data.get("symbol", "unknown")
            }
            
            # Store metrics
            self.trading_metrics = {
                "metrics": metrics,
                "labels": labels,
                "timestamp": time.time()
            }
            
            result = {
                "status": "success",
                "metrics": metrics,
                "labels": labels,
                "n_metrics": len(metrics)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to collect trading metrics: {str(e)}"}
    
    def collect_performance_metrics(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect performance-related metrics.
        
        Args:
            performance_data: Performance data dictionary
            
        Returns:
            Performance metrics collection result
        """
        try:
            # Extract performance metrics
            metrics = {
                "performance_cpu_usage": performance_data.get("cpu_usage", 0.0),
                "performance_memory_usage": performance_data.get("memory_usage", 0.0),
                "performance_disk_usage": performance_data.get("disk_usage", 0.0),
                "performance_network_latency": performance_data.get("network_latency", 0.0),
                "performance_response_time": performance_data.get("response_time", 0.0),
                "performance_throughput": performance_data.get("throughput", 0.0),
                "performance_error_rate": performance_data.get("error_rate", 0.0),
                "performance_uptime": performance_data.get("uptime", 0.0),
                "performance_active_connections": performance_data.get("active_connections", 0),
                "performance_queue_size": performance_data.get("queue_size", 0)
            }
            
            # Add labels
            labels = {
                "service": performance_data.get("service_name", "unknown"),
                "instance": performance_data.get("instance_id", "unknown"),
                "environment": performance_data.get("environment", "unknown")
            }
            
            # Store metrics
            self.performance_metrics = {
                "metrics": metrics,
                "labels": labels,
                "timestamp": time.time()
            }
            
            result = {
                "status": "success",
                "metrics": metrics,
                "labels": labels,
                "n_metrics": len(metrics)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to collect performance metrics: {str(e)}"}
    
    def collect_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect system-related metrics.
        
        Args:
            system_data: System data dictionary
            
        Returns:
            System metrics collection result
        """
        try:
            # Extract system metrics
            metrics = {
                "system_cpu_cores": system_data.get("cpu_cores", 0),
                "system_cpu_frequency": system_data.get("cpu_frequency", 0.0),
                "system_memory_total": system_data.get("memory_total", 0.0),
                "system_memory_available": system_data.get("memory_available", 0.0),
                "system_disk_total": system_data.get("disk_total", 0.0),
                "system_disk_free": system_data.get("disk_free", 0.0),
                "system_load_average": system_data.get("load_average", 0.0),
                "system_processes": system_data.get("processes", 0),
                "system_threads": system_data.get("threads", 0),
                "system_file_descriptors": system_data.get("file_descriptors", 0)
            }
            
            # Add labels
            labels = {
                "hostname": system_data.get("hostname", "unknown"),
                "os": system_data.get("os", "unknown"),
                "architecture": system_data.get("architecture", "unknown")
            }
            
            # Store metrics
            self.system_metrics = {
                "metrics": metrics,
                "labels": labels,
                "timestamp": time.time()
            }
            
            result = {
                "status": "success",
                "metrics": metrics,
                "labels": labels,
                "n_metrics": len(metrics)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to collect system metrics: {str(e)}"}
    
    def create_custom_metric(self, metric_name: str, metric_type: str, 
                           description: str, labels: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Create a custom metric.
        
        Args:
            metric_name: Name of the metric
            metric_type: Type of metric (counter, gauge, histogram, summary)
            description: Description of the metric
            labels: Labels for the metric
            
        Returns:
            Custom metric creation result
        """
        try:
            # Validate metric type
            valid_types = ["counter", "gauge", "histogram", "summary"]
            if metric_type not in valid_types:
                return {"status": "error", "message": f"Invalid metric type: {metric_type}"}
            
            # Create custom metric
            custom_metric = {
                "name": metric_name,
                "type": metric_type,
                "description": description,
                "labels": labels or {},
                "value": 0.0,
                "created_time": time.time(),
                "last_updated": time.time()
            }
            
            # Store custom metric
            self.custom_metrics[metric_name] = custom_metric
            
            result = {
                "status": "success",
                "metric_name": metric_name,
                "metric_type": metric_type,
                "description": description,
                "labels": labels or {},
                "message": "Custom metric created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create custom metric: {str(e)}"}
    
    def update_custom_metric(self, metric_name: str, value: float, 
                           labels: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Update a custom metric value.
        
        Args:
            metric_name: Name of the metric
            value: New value for the metric
            labels: Labels for the metric
            
        Returns:
            Metric update result
        """
        try:
            if metric_name not in self.custom_metrics:
                return {"status": "error", "message": f"Metric {metric_name} not found"}
            
            # Update metric value
            self.custom_metrics[metric_name]["value"] = value
            self.custom_metrics[metric_name]["last_updated"] = time.time()
            
            if labels:
                self.custom_metrics[metric_name]["labels"].update(labels)
            
            result = {
                "status": "success",
                "metric_name": metric_name,
                "value": value,
                "labels": self.custom_metrics[metric_name]["labels"],
                "message": "Metric updated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to update metric: {str(e)}"}
    
    def get_metric_value(self, metric_name: str) -> Dict[str, Any]:
        """
        Get metric value.
        
        Args:
            metric_name: Name of the metric
            
        Returns:
            Metric value result
        """
        try:
            if metric_name not in self.custom_metrics:
                return {"status": "error", "message": f"Metric {metric_name} not found"}
            
            metric = self.custom_metrics[metric_name]
            
            result = {
                "status": "success",
                "metric_name": metric_name,
                "value": metric["value"],
                "type": metric["type"],
                "labels": metric["labels"],
                "last_updated": metric["last_updated"]
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get metric value: {str(e)}"}
    
    def create_alert_rule(self, rule_name: str, metric_name: str, 
                         condition: str, threshold: float, 
                         severity: str = "warning") -> Dict[str, Any]:
        """
        Create an alert rule.
        
        Args:
            rule_name: Name of the alert rule
            metric_name: Name of the metric to monitor
            condition: Condition for the alert (>, <, >=, <=, ==, !=)
            threshold: Threshold value
            severity: Alert severity (info, warning, critical)
            
        Returns:
            Alert rule creation result
        """
        try:
            # Validate condition
            valid_conditions = [">", "<", ">=", "<=", "==", "!="]
            if condition not in valid_conditions:
                return {"status": "error", "message": f"Invalid condition: {condition}"}
            
            # Validate severity
            valid_severities = ["info", "warning", "critical"]
            if severity not in valid_severities:
                return {"status": "error", "message": f"Invalid severity: {severity}"}
            
            # Create alert rule
            alert_rule = {
                "rule_name": rule_name,
                "metric_name": metric_name,
                "condition": condition,
                "threshold": threshold,
                "severity": severity,
                "active": True,
                "created_time": time.time(),
                "last_triggered": None,
                "trigger_count": 0
            }
            
            # Store alert rule
            self.alert_rules[rule_name] = alert_rule
            
            result = {
                "status": "success",
                "rule_name": rule_name,
                "metric_name": metric_name,
                "condition": condition,
                "threshold": threshold,
                "severity": severity,
                "message": "Alert rule created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create alert rule: {str(e)}"}
    
    def check_alerts(self) -> Dict[str, Any]:
        """
        Check all alert rules.
        
        Returns:
            Alert check result
        """
        try:
            triggered_alerts = []
            
            for rule_name, rule in self.alert_rules.items():
                if not rule["active"]:
                    continue
                
                metric_name = rule["metric_name"]
                if metric_name not in self.custom_metrics:
                    continue
                
                metric_value = self.custom_metrics[metric_name]["value"]
                condition = rule["condition"]
                threshold = rule["threshold"]
                
                # Check condition
                triggered = False
                if condition == ">":
                    triggered = metric_value > threshold
                elif condition == "<":
                    triggered = metric_value < threshold
                elif condition == ">=":
                    triggered = metric_value >= threshold
                elif condition == "<=":
                    triggered = metric_value <= threshold
                elif condition == "==":
                    triggered = metric_value == threshold
                elif condition == "!=":
                    triggered = metric_value != threshold
                
                if triggered:
                    # Update rule
                    rule["last_triggered"] = time.time()
                    rule["trigger_count"] += 1
                    
                    # Add to triggered alerts
                    triggered_alerts.append({
                        "rule_name": rule_name,
                        "metric_name": metric_name,
                        "metric_value": metric_value,
                        "condition": condition,
                        "threshold": threshold,
                        "severity": rule["severity"],
                        "triggered_time": time.time()
                    })
            
            result = {
                "status": "success",
                "triggered_alerts": triggered_alerts,
                "n_triggered": len(triggered_alerts),
                "n_rules": len(self.alert_rules)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to check alerts: {str(e)}"}
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Get all collected metrics.
        
        Returns:
            All metrics result
        """
        try:
            all_metrics = {
                "trading_metrics": self.trading_metrics,
                "performance_metrics": self.performance_metrics,
                "system_metrics": self.system_metrics,
                "custom_metrics": self.custom_metrics,
                "alert_rules": self.alert_rules,
                "timestamp": time.time()
            }
            
            result = {
                "status": "success",
                "metrics": all_metrics,
                "n_trading_metrics": len(self.trading_metrics.get("metrics", {})),
                "n_performance_metrics": len(self.performance_metrics.get("metrics", {})),
                "n_system_metrics": len(self.system_metrics.get("metrics", {})),
                "n_custom_metrics": len(self.custom_metrics),
                "n_alert_rules": len(self.alert_rules)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get all metrics: {str(e)}"}
    
    def export_metrics(self, format: str = "json") -> Dict[str, Any]:
        """
        Export metrics in specified format.
        
        Args:
            format: Export format (json, prometheus)
            
        Returns:
            Export result
        """
        try:
            if format == "json":
                # Export as JSON
                export_data = {
                    "trading_metrics": self.trading_metrics,
                    "performance_metrics": self.performance_metrics,
                    "system_metrics": self.system_metrics,
                    "custom_metrics": self.custom_metrics,
                    "alert_rules": self.alert_rules,
                    "export_time": time.time()
                }
                
                result = {
                    "status": "success",
                    "format": "json",
                    "data": export_data,
                    "size": len(json.dumps(export_data))
                }
                
            elif format == "prometheus":
                # Export as Prometheus format
                prometheus_data = []
                
                # Add trading metrics
                if self.trading_metrics:
                    for metric_name, value in self.trading_metrics.get("metrics", {}).items():
                        labels = self.trading_metrics.get("labels", {})
                        label_str = ",".join([f'{k}="{v}"' for k, v in labels.items()])
                        if label_str:
                            prometheus_data.append(f"{metric_name}{{{label_str}}} {value}")
                        else:
                            prometheus_data.append(f"{metric_name} {value}")
                
                # Add performance metrics
                if self.performance_metrics:
                    for metric_name, value in self.performance_metrics.get("metrics", {}).items():
                        labels = self.performance_metrics.get("labels", {})
                        label_str = ",".join([f'{k}="{v}"' for k, v in labels.items()])
                        if label_str:
                            prometheus_data.append(f"{metric_name}{{{label_str}}} {value}")
                        else:
                            prometheus_data.append(f"{metric_name} {value}")
                
                # Add system metrics
                if self.system_metrics:
                    for metric_name, value in self.system_metrics.get("metrics", {}).items():
                        labels = self.system_metrics.get("labels", {})
                        label_str = ",".join([f'{k}="{v}"' for k, v in labels.items()])
                        if label_str:
                            prometheus_data.append(f"{metric_name}{{{label_str}}} {value}")
                        else:
                            prometheus_data.append(f"{metric_name} {value}")
                
                # Add custom metrics
                for metric_name, metric in self.custom_metrics.items():
                    labels = metric.get("labels", {})
                    label_str = ",".join([f'{k}="{v}"' for k, v in labels.items()])
                    if label_str:
                        prometheus_data.append(f"{metric_name}{{{label_str}}} {metric['value']}")
                    else:
                        prometheus_data.append(f"{metric_name} {metric['value']}")
                
                result = {
                    "status": "success",
                    "format": "prometheus",
                    "data": "\n".join(prometheus_data),
                    "n_metrics": len(prometheus_data)
                }
                
            else:
                return {"status": "error", "message": f"Unsupported format: {format}"}
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to export metrics: {str(e)}"}
    
    def clear_metrics(self, metric_type: str = "all") -> Dict[str, Any]:
        """
        Clear metrics.
        
        Args:
            metric_type: Type of metrics to clear (all, trading, performance, system, custom)
            
        Returns:
            Clear result
        """
        try:
            cleared_count = 0
            
            if metric_type in ["all", "trading"]:
                self.trading_metrics = {}
                cleared_count += 1
            
            if metric_type in ["all", "performance"]:
                self.performance_metrics = {}
                cleared_count += 1
            
            if metric_type in ["all", "system"]:
                self.system_metrics = {}
                cleared_count += 1
            
            if metric_type in ["all", "custom"]:
                self.custom_metrics = {}
                cleared_count += 1
            
            result = {
                "status": "success",
                "metric_type": metric_type,
                "cleared_count": cleared_count,
                "message": f"Cleared {metric_type} metrics"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to clear metrics: {str(e)}"}
