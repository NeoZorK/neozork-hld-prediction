# -*- coding: utf-8 -*-
"""
Performance Monitoring for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive performance monitoring capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
from typing import Dict, Any, Optional, List, Tuple
import warnings

class PerformanceMonitoring:
    """
    Performance monitoring system.
    
    Features:
    - System Performance Monitoring
    - Trading Performance Monitoring
    - Resource Usage Tracking
    - Performance Analytics
    - Performance Alerts
    - Performance Reporting
    """
    
    def __init__(self):
        """Initialize the Performance Monitoring system."""
        self.performance_history = []
        self.trading_performance = {}
        self.system_metrics = {}
        self.performance_alerts = {}
        self.performance_reports = {}
    
    def monitor_performance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor system performance.
        
        Args:
            metrics: Performance metrics
            
        Returns:
            Performance monitoring result
        """
        try:
            # Extract performance metrics
            cpu_usage = metrics.get("cpu_usage", 0.0)
            memory_usage = metrics.get("memory_usage", 0.0)
            disk_usage = metrics.get("disk_usage", 0.0)
            network_latency = metrics.get("network_latency", 0.0)
            response_time = metrics.get("response_time", 0.0)
            throughput = metrics.get("throughput", 0.0)
            error_rate = metrics.get("error_rate", 0.0)
            uptime = metrics.get("uptime", 0.0)
            
            # Calculate performance score
            performance_score = self._calculate_performance_score(
                cpu_usage, memory_usage, disk_usage, network_latency, 
                response_time, throughput, error_rate, uptime
            )
            
            # Determine performance status
            if performance_score >= 90:
                status = "excellent"
            elif performance_score >= 80:
                status = "good"
            elif performance_score >= 70:
                status = "fair"
            elif performance_score >= 60:
                status = "poor"
            else:
                status = "critical"
            
            # Store performance data
            performance_data = {
                "timestamp": time.time(),
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "disk_usage": disk_usage,
                "network_latency": network_latency,
                "response_time": response_time,
                "throughput": throughput,
                "error_rate": error_rate,
                "uptime": uptime,
                "performance_score": performance_score,
                "status": status
            }
            
            # Store in performance history
            self.performance_history.append(performance_data)
            
            # Keep only last 1000 records
            if len(self.performance_history) > 1000:
                self.performance_history = self.performance_history[-1000:]
            
            result = {
                "status": "success",
                "performance_data": performance_data,
                "performance_score": performance_score,
                "status": status,
                "message": "Performance monitoring completed"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Performance monitoring failed: {str(e)}"}
    
    def monitor_trading_performance(self, trading_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor trading performance.
        
        Args:
            trading_data: Trading data dictionary
            
        Returns:
            Trading performance monitoring result
        """
        try:
            # Extract trading metrics
            total_return = trading_data.get("total_return", 0.0)
            sharpe_ratio = trading_data.get("sharpe_ratio", 0.0)
            max_drawdown = trading_data.get("max_drawdown", 0.0)
            win_rate = trading_data.get("win_rate", 0.0)
            total_trades = trading_data.get("total_trades", 0)
            profitable_trades = trading_data.get("profitable_trades", 0)
            avg_trade_duration = trading_data.get("avg_trade_duration", 0.0)
            volatility = trading_data.get("volatility", 0.0)
            
            # Calculate trading performance score
            trading_score = self._calculate_trading_performance_score(
                total_return, sharpe_ratio, max_drawdown, win_rate, 
                total_trades, profitable_trades, avg_trade_duration, volatility
            )
            
            # Determine trading performance status
            if trading_score >= 90:
                status = "excellent"
            elif trading_score >= 80:
                status = "good"
            elif trading_score >= 70:
                status = "fair"
            elif trading_score >= 60:
                status = "poor"
            else:
                status = "critical"
            
            # Store trading performance data
            trading_performance_data = {
                "timestamp": time.time(),
                "total_return": total_return,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown,
                "win_rate": win_rate,
                "total_trades": total_trades,
                "profitable_trades": profitable_trades,
                "avg_trade_duration": avg_trade_duration,
                "volatility": volatility,
                "trading_score": trading_score,
                "status": status
            }
            
            # Store in trading performance
            self.trading_performance = trading_performance_data
            
            result = {
                "status": "success",
                "trading_performance": trading_performance_data,
                "trading_score": trading_score,
                "status": status,
                "message": "Trading performance monitoring completed"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Trading performance monitoring failed: {str(e)}"}
    
    def get_performance_summary(self, time_range: str = "1h") -> Dict[str, Any]:
        """
        Get performance summary for time range.
        
        Args:
            time_range: Time range for summary (1h, 6h, 24h, 7d)
            
        Returns:
            Performance summary result
        """
        try:
            # Calculate time range in seconds
            time_ranges = {
                "1h": 3600,
                "6h": 21600,
                "24h": 86400,
                "7d": 604800
            }
            
            if time_range not in time_ranges:
                return {"status": "error", "message": f"Invalid time range: {time_range}"}
            
            range_seconds = time_ranges[time_range]
            current_time = time.time()
            start_time = current_time - range_seconds
            
            # Filter performance history
            filtered_history = [
                record for record in self.performance_history
                if record["timestamp"] >= start_time
            ]
            
            if not filtered_history:
                return {"status": "error", "message": "No performance data available for the specified time range"}
            
            # Calculate summary statistics
            cpu_usage_values = [record["cpu_usage"] for record in filtered_history]
            memory_usage_values = [record["memory_usage"] for record in filtered_history]
            disk_usage_values = [record["disk_usage"] for record in filtered_history]
            network_latency_values = [record["network_latency"] for record in filtered_history]
            response_time_values = [record["response_time"] for record in filtered_history]
            throughput_values = [record["throughput"] for record in filtered_history]
            error_rate_values = [record["error_rate"] for record in filtered_history]
            performance_score_values = [record["performance_score"] for record in filtered_history]
            
            summary = {
                "time_range": time_range,
                "n_records": len(filtered_history),
                "cpu_usage": {
                    "avg": np.mean(cpu_usage_values),
                    "min": np.min(cpu_usage_values),
                    "max": np.max(cpu_usage_values),
                    "std": np.std(cpu_usage_values)
                },
                "memory_usage": {
                    "avg": np.mean(memory_usage_values),
                    "min": np.min(memory_usage_values),
                    "max": np.max(memory_usage_values),
                    "std": np.std(memory_usage_values)
                },
                "disk_usage": {
                    "avg": np.mean(disk_usage_values),
                    "min": np.min(disk_usage_values),
                    "max": np.max(disk_usage_values),
                    "std": np.std(disk_usage_values)
                },
                "network_latency": {
                    "avg": np.mean(network_latency_values),
                    "min": np.min(network_latency_values),
                    "max": np.max(network_latency_values),
                    "std": np.std(network_latency_values)
                },
                "response_time": {
                    "avg": np.mean(response_time_values),
                    "min": np.min(response_time_values),
                    "max": np.max(response_time_values),
                    "std": np.std(response_time_values)
                },
                "throughput": {
                    "avg": np.mean(throughput_values),
                    "min": np.min(throughput_values),
                    "max": np.max(throughput_values),
                    "std": np.std(throughput_values)
                },
                "error_rate": {
                    "avg": np.mean(error_rate_values),
                    "min": np.min(error_rate_values),
                    "max": np.max(error_rate_values),
                    "std": np.std(error_rate_values)
                },
                "performance_score": {
                    "avg": np.mean(performance_score_values),
                    "min": np.min(performance_score_values),
                    "max": np.max(performance_score_values),
                    "std": np.std(performance_score_values)
                }
            }
            
            result = {
                "status": "success",
                "summary": summary,
                "message": "Performance summary generated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get performance summary: {str(e)}"}
    
    def get_performance_trends(self, metric_name: str, time_range: str = "24h") -> Dict[str, Any]:
        """
        Get performance trends for a specific metric.
        
        Args:
            metric_name: Name of the metric
            time_range: Time range for trends
            
        Returns:
            Performance trends result
        """
        try:
            # Calculate time range in seconds
            time_ranges = {
                "1h": 3600,
                "6h": 21600,
                "24h": 86400,
                "7d": 604800
            }
            
            if time_range not in time_ranges:
                return {"status": "error", "message": f"Invalid time range: {time_range}"}
            
            range_seconds = time_ranges[time_range]
            current_time = time.time()
            start_time = current_time - range_seconds
            
            # Filter performance history
            filtered_history = [
                record for record in self.performance_history
                if record["timestamp"] >= start_time
            ]
            
            if not filtered_history:
                return {"status": "error", "message": "No performance data available for the specified time range"}
            
            # Extract metric values
            if metric_name not in filtered_history[0]:
                return {"status": "error", "message": f"Metric {metric_name} not found"}
            
            metric_values = [record[metric_name] for record in filtered_history]
            timestamps = [record["timestamp"] for record in filtered_history]
            
            # Calculate trends
            if len(metric_values) < 2:
                return {"status": "error", "message": "Insufficient data for trend analysis"}
            
            # Linear trend
            x = np.array(timestamps)
            y = np.array(metric_values)
            slope, intercept = np.polyfit(x, y, 1)
            
            # Trend direction
            if slope > 0.01:
                trend_direction = "increasing"
            elif slope < -0.01:
                trend_direction = "decreasing"
            else:
                trend_direction = "stable"
            
            # Trend strength
            trend_strength = abs(slope) * 1000  # Scale for readability
            
            trends = {
                "metric_name": metric_name,
                "time_range": time_range,
                "n_points": len(metric_values),
                "slope": slope,
                "intercept": intercept,
                "trend_direction": trend_direction,
                "trend_strength": trend_strength,
                "current_value": metric_values[-1],
                "start_value": metric_values[0],
                "change": metric_values[-1] - metric_values[0],
                "change_percentage": ((metric_values[-1] - metric_values[0]) / metric_values[0] * 100) if metric_values[0] != 0 else 0
            }
            
            result = {
                "status": "success",
                "trends": trends,
                "message": "Performance trends generated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get performance trends: {str(e)}"}
    
    def create_performance_alert(self, metric_name: str, condition: str, 
                                threshold: float, severity: str = "warning") -> Dict[str, Any]:
        """
        Create a performance alert.
        
        Args:
            metric_name: Name of the metric
            condition: Condition for the alert (>, <, >=, <=, ==, !=)
            threshold: Threshold value
            severity: Alert severity (info, warning, critical)
            
        Returns:
            Performance alert creation result
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
            
            # Generate alert ID
            alert_id = f"perf_alert_{int(time.time())}"
            
            # Create performance alert
            performance_alert = {
                "id": alert_id,
                "metric_name": metric_name,
                "condition": condition,
                "threshold": threshold,
                "severity": severity,
                "enabled": True,
                "created_time": time.time(),
                "last_updated": time.time(),
                "trigger_count": 0,
                "last_triggered": None
            }
            
            # Store performance alert
            self.performance_alerts[alert_id] = performance_alert
            
            result = {
                "status": "success",
                "alert_id": alert_id,
                "metric_name": metric_name,
                "condition": condition,
                "threshold": threshold,
                "severity": severity,
                "message": "Performance alert created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create performance alert: {str(e)}"}
    
    def check_performance_alerts(self) -> Dict[str, Any]:
        """
        Check all performance alerts.
        
        Returns:
            Performance alert check result
        """
        try:
            triggered_alerts = []
            
            if not self.performance_history:
                return {"status": "success", "triggered_alerts": [], "n_triggered": 0}
            
            # Get latest performance data
            latest_data = self.performance_history[-1]
            
            for alert_id, alert in self.performance_alerts.items():
                if not alert["enabled"]:
                    continue
                
                metric_name = alert["metric_name"]
                if metric_name not in latest_data:
                    continue
                
                metric_value = latest_data[metric_name]
                condition = alert["condition"]
                threshold = alert["threshold"]
                
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
                    # Update alert
                    alert["last_triggered"] = time.time()
                    alert["trigger_count"] += 1
                    
                    # Add to triggered alerts
                    triggered_alerts.append({
                        "alert_id": alert_id,
                        "metric_name": metric_name,
                        "metric_value": metric_value,
                        "condition": condition,
                        "threshold": threshold,
                        "severity": alert["severity"],
                        "triggered_time": time.time()
                    })
            
            result = {
                "status": "success",
                "triggered_alerts": triggered_alerts,
                "n_triggered": len(triggered_alerts),
                "n_alerts": len(self.performance_alerts)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to check performance alerts: {str(e)}"}
    
    def generate_performance_report(self, report_type: str = "summary") -> Dict[str, Any]:
        """
        Generate a performance report.
        
        Args:
            report_type: Type of report (summary, detailed, trends)
            
        Returns:
            Performance report result
        """
        try:
            # Generate report ID
            report_id = f"report_{int(time.time())}"
            
            if report_type == "summary":
                # Generate summary report
                report_data = {
                    "report_type": "summary",
                    "generated_time": time.time(),
                    "performance_summary": self.get_performance_summary("24h"),
                    "trading_performance": self.trading_performance,
                    "n_performance_records": len(self.performance_history),
                    "n_performance_alerts": len(self.performance_alerts)
                }
                
            elif report_type == "detailed":
                # Generate detailed report
                report_data = {
                    "report_type": "detailed",
                    "generated_time": time.time(),
                    "performance_history": self.performance_history[-100:],  # Last 100 records
                    "trading_performance": self.trading_performance,
                    "performance_alerts": self.performance_alerts,
                    "n_performance_records": len(self.performance_history),
                    "n_performance_alerts": len(self.performance_alerts)
                }
                
            elif report_type == "trends":
                # Generate trends report
                report_data = {
                    "report_type": "trends",
                    "generated_time": time.time(),
                    "trends": {
                        "cpu_usage": self.get_performance_trends("cpu_usage", "24h"),
                        "memory_usage": self.get_performance_trends("memory_usage", "24h"),
                        "disk_usage": self.get_performance_trends("disk_usage", "24h"),
                        "network_latency": self.get_performance_trends("network_latency", "24h"),
                        "response_time": self.get_performance_trends("response_time", "24h"),
                        "throughput": self.get_performance_trends("throughput", "24h"),
                        "error_rate": self.get_performance_trends("error_rate", "24h"),
                        "performance_score": self.get_performance_trends("performance_score", "24h")
                    }
                }
                
            else:
                return {"status": "error", "message": f"Invalid report type: {report_type}"}
            
            # Store report
            self.performance_reports[report_id] = report_data
            
            result = {
                "status": "success",
                "report_id": report_id,
                "report_type": report_type,
                "report_data": report_data,
                "message": "Performance report generated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to generate performance report: {str(e)}"}
    
    def _calculate_performance_score(self, cpu_usage: float, memory_usage: float, 
                                   disk_usage: float, network_latency: float,
                                   response_time: float, throughput: float, 
                                   error_rate: float, uptime: float) -> float:
        """Calculate overall performance score."""
        try:
            # Normalize metrics (0-100 scale)
            cpu_score = max(0, 100 - cpu_usage)
            memory_score = max(0, 100 - memory_usage)
            disk_score = max(0, 100 - disk_usage)
            latency_score = max(0, 100 - min(network_latency * 10, 100))
            response_score = max(0, 100 - min(response_time * 100, 100))
            throughput_score = min(throughput * 10, 100)
            error_score = max(0, 100 - error_rate * 100)
            uptime_score = min(uptime / 3600 * 10, 100)  # Convert to hours
            
            # Weighted average
            weights = {
                "cpu": 0.2,
                "memory": 0.2,
                "disk": 0.1,
                "latency": 0.15,
                "response": 0.15,
                "throughput": 0.1,
                "error": 0.05,
                "uptime": 0.05
            }
            
            performance_score = (
                cpu_score * weights["cpu"] +
                memory_score * weights["memory"] +
                disk_score * weights["disk"] +
                latency_score * weights["latency"] +
                response_score * weights["response"] +
                throughput_score * weights["throughput"] +
                error_score * weights["error"] +
                uptime_score * weights["uptime"]
            )
            
            return min(100, max(0, performance_score))
            
        except Exception as e:
            return 0.0
    
    def _calculate_trading_performance_score(self, total_return: float, sharpe_ratio: float,
                                           max_drawdown: float, win_rate: float,
                                           total_trades: int, profitable_trades: int,
                                           avg_trade_duration: float, volatility: float) -> float:
        """Calculate trading performance score."""
        try:
            # Normalize metrics (0-100 scale)
            return_score = min(100, max(0, total_return * 100))
            sharpe_score = min(100, max(0, sharpe_ratio * 20))
            drawdown_score = max(0, 100 - abs(max_drawdown) * 100)
            win_rate_score = win_rate * 100
            trade_score = min(100, total_trades / 10)  # Normalize by expected trades
            profit_score = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
            duration_score = max(0, 100 - avg_trade_duration / 3600 * 10)  # Convert to hours
            volatility_score = max(0, 100 - volatility * 100)
            
            # Weighted average
            weights = {
                "return": 0.25,
                "sharpe": 0.2,
                "drawdown": 0.2,
                "win_rate": 0.15,
                "trades": 0.05,
                "profit": 0.05,
                "duration": 0.05,
                "volatility": 0.05
            }
            
            trading_score = (
                return_score * weights["return"] +
                sharpe_score * weights["sharpe"] +
                drawdown_score * weights["drawdown"] +
                win_rate_score * weights["win_rate"] +
                trade_score * weights["trades"] +
                profit_score * weights["profit"] +
                duration_score * weights["duration"] +
                volatility_score * weights["volatility"]
            )
            
            return min(100, max(0, trading_score))
            
        except Exception as e:
            return 0.0
