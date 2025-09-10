# -*- coding: utf-8 -*-
"""
Alerting System for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive alerting and notification capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
from typing import Dict, Any, Optional, List, Tuple, Callable
from enum import Enum
import warnings

class AlertSeverity(Enum):
    """Alert severity enumeration."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class AlertStatus(Enum):
    """Alert status enumeration."""
    ACTIVE = "active"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"
    ACKNOWLEDGED = "acknowledged"

class NotificationChannel(Enum):
    """Notification channel enumeration."""
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    WEBHOOK = "webhook"
    TELEGRAM = "telegram"
    DISCORD = "discord"

class AlertingSystem:
    """
    Alerting system for monitoring and notifications.
    
    Features:
    - Alert Management
    - Notification Channels
    - Alert Rules
    - Escalation Policies
    - Alert Suppression
    - Alert History
    """
    
    def __init__(self):
        """Initialize the Alerting System."""
        self.alerts = {}
        self.alert_rules = {}
        self.notification_channels = {}
        self.escalation_policies = {}
        self.alert_history = []
        self.suppression_rules = {}
    
    def create_alert_rule(self, rule_name: str, metric_name: str, 
                         condition: str, threshold: float, 
                         severity: str = "warning", duration: str = "0s") -> Dict[str, Any]:
        """
        Create an alert rule.
        
        Args:
            rule_name: Name of the alert rule
            metric_name: Name of the metric to monitor
            condition: Condition for the alert (>, <, >=, <=, ==, !=)
            threshold: Threshold value
            severity: Alert severity (info, warning, critical, emergency)
            duration: Duration before alert triggers
            
        Returns:
            Alert rule creation result
        """
        try:
            # Validate severity
            valid_severities = [s.value for s in AlertSeverity]
            if severity not in valid_severities:
                return {"status": "error", "message": f"Invalid severity: {severity}"}
            
            # Validate condition
            valid_conditions = [">", "<", ">=", "<=", "==", "!="]
            if condition not in valid_conditions:
                return {"status": "error", "message": f"Invalid condition: {condition}"}
            
            # Generate rule ID
            rule_id = f"rule_{int(time.time())}"
            
            # Create alert rule
            alert_rule = {
                "id": rule_id,
                "name": rule_name,
                "metric_name": metric_name,
                "condition": condition,
                "threshold": threshold,
                "severity": severity,
                "duration": duration,
                "enabled": True,
                "created_time": time.time(),
                "last_updated": time.time(),
                "trigger_count": 0,
                "last_triggered": None
            }
            
            # Store alert rule
            self.alert_rules[rule_id] = alert_rule
            
            result = {
                "status": "success",
                "rule_id": rule_id,
                "rule_name": rule_name,
                "metric_name": metric_name,
                "condition": condition,
                "threshold": threshold,
                "severity": severity,
                "duration": duration,
                "message": "Alert rule created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create alert rule: {str(e)}"}
    
    def create_notification_channel(self, channel_name: str, channel_type: str,
                                  config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a notification channel.
        
        Args:
            channel_name: Name of the notification channel
            channel_type: Type of channel (email, sms, slack, webhook, etc.)
            config: Channel configuration
            
        Returns:
            Notification channel creation result
        """
        try:
            # Validate channel type
            valid_types = [c.value for c in NotificationChannel]
            if channel_type not in valid_types:
                return {"status": "error", "message": f"Invalid channel type: {channel_type}"}
            
            # Generate channel ID
            channel_id = f"channel_{int(time.time())}"
            
            # Create notification channel
            notification_channel = {
                "id": channel_id,
                "name": channel_name,
                "type": channel_type,
                "config": config,
                "enabled": True,
                "created_time": time.time(),
                "last_updated": time.time(),
                "test_status": "not_tested"
            }
            
            # Store notification channel
            self.notification_channels[channel_id] = notification_channel
            
            result = {
                "status": "success",
                "channel_id": channel_id,
                "channel_name": channel_name,
                "channel_type": channel_type,
                "config": config,
                "message": "Notification channel created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create notification channel: {str(e)}"}
    
    def test_notification_channel(self, channel_id: str) -> Dict[str, Any]:
        """
        Test a notification channel.
        
        Args:
            channel_id: Channel ID to test
            
        Returns:
            Test result
        """
        try:
            if channel_id not in self.notification_channels:
                return {"status": "error", "message": f"Channel {channel_id} not found"}
            
            channel = self.notification_channels[channel_id]
            
            # Simulate test notification
            test_message = {
                "title": "Test Alert",
                "message": "This is a test notification from NeoZork Alerting System",
                "severity": "info",
                "timestamp": time.time()
            }
            
            # Update test status
            channel["test_status"] = "tested"
            channel["last_test_time"] = time.time()
            
            result = {
                "status": "success",
                "channel_id": channel_id,
                "channel_name": channel["name"],
                "channel_type": channel["type"],
                "test_message": test_message,
                "test_status": "success",
                "message": "Notification channel tested successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to test notification channel: {str(e)}"}
    
    def create_escalation_policy(self, policy_name: str, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create an escalation policy.
        
        Args:
            policy_name: Name of the escalation policy
            steps: List of escalation steps
            
        Returns:
            Escalation policy creation result
        """
        try:
            # Generate policy ID
            policy_id = f"policy_{int(time.time())}"
            
            # Create escalation policy
            escalation_policy = {
                "id": policy_id,
                "name": policy_name,
                "steps": steps,
                "enabled": True,
                "created_time": time.time(),
                "last_updated": time.time()
            }
            
            # Store escalation policy
            self.escalation_policies[policy_id] = escalation_policy
            
            result = {
                "status": "success",
                "policy_id": policy_id,
                "policy_name": policy_name,
                "steps": steps,
                "message": "Escalation policy created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create escalation policy: {str(e)}"}
    
    def trigger_alert(self, rule_id: str, metric_value: float, 
                     labels: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Trigger an alert.
        
        Args:
            rule_id: Alert rule ID
            metric_value: Current metric value
            labels: Labels for the alert
            
        Returns:
            Alert trigger result
        """
        try:
            if rule_id not in self.alert_rules:
                return {"status": "error", "message": f"Alert rule {rule_id} not found"}
            
            rule = self.alert_rules[rule_id]
            
            if not rule["enabled"]:
                return {"status": "error", "message": f"Alert rule {rule_id} is disabled"}
            
            # Check if alert should trigger
            condition = rule["condition"]
            threshold = rule["threshold"]
            
            should_trigger = False
            if condition == ">":
                should_trigger = metric_value > threshold
            elif condition == "<":
                should_trigger = metric_value < threshold
            elif condition == ">=":
                should_trigger = metric_value >= threshold
            elif condition == "<=":
                should_trigger = metric_value <= threshold
            elif condition == "==":
                should_trigger = metric_value == threshold
            elif condition == "!=":
                should_trigger = metric_value != threshold
            
            if not should_trigger:
                return {"status": "success", "message": "Alert condition not met"}
            
            # Generate alert ID
            alert_id = f"alert_{int(time.time())}"
            
            # Create alert
            alert = {
                "id": alert_id,
                "rule_id": rule_id,
                "rule_name": rule["name"],
                "metric_name": rule["metric_name"],
                "metric_value": metric_value,
                "threshold": threshold,
                "condition": condition,
                "severity": rule["severity"],
                "status": AlertStatus.ACTIVE.value,
                "labels": labels or {},
                "created_time": time.time(),
                "last_updated": time.time(),
                "acknowledged_time": None,
                "resolved_time": None,
                "escalation_step": 0
            }
            
            # Store alert
            self.alerts[alert_id] = alert
            
            # Add to alert history
            self.alert_history.append(alert.copy())
            
            # Update rule
            rule["trigger_count"] += 1
            rule["last_triggered"] = time.time()
            
            result = {
                "status": "success",
                "alert_id": alert_id,
                "rule_id": rule_id,
                "rule_name": rule["name"],
                "severity": rule["severity"],
                "metric_value": metric_value,
                "threshold": threshold,
                "message": "Alert triggered successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to trigger alert: {str(e)}"}
    
    def acknowledge_alert(self, alert_id: str, user: str = "system") -> Dict[str, Any]:
        """
        Acknowledge an alert.
        
        Args:
            alert_id: Alert ID
            user: User acknowledging the alert
            
        Returns:
            Acknowledgment result
        """
        try:
            if alert_id not in self.alerts:
                return {"status": "error", "message": f"Alert {alert_id} not found"}
            
            alert = self.alerts[alert_id]
            
            if alert["status"] != AlertStatus.ACTIVE.value:
                return {"status": "error", "message": f"Alert {alert_id} is not active"}
            
            # Update alert
            alert["status"] = AlertStatus.ACKNOWLEDGED.value
            alert["acknowledged_time"] = time.time()
            alert["acknowledged_by"] = user
            alert["last_updated"] = time.time()
            
            result = {
                "status": "success",
                "alert_id": alert_id,
                "status": AlertStatus.ACKNOWLEDGED.value,
                "acknowledged_by": user,
                "acknowledged_time": alert["acknowledged_time"],
                "message": "Alert acknowledged successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to acknowledge alert: {str(e)}"}
    
    def resolve_alert(self, alert_id: str, user: str = "system") -> Dict[str, Any]:
        """
        Resolve an alert.
        
        Args:
            alert_id: Alert ID
            user: User resolving the alert
            
        Returns:
            Resolution result
        """
        try:
            if alert_id not in self.alerts:
                return {"status": "error", "message": f"Alert {alert_id} not found"}
            
            alert = self.alerts[alert_id]
            
            if alert["status"] == AlertStatus.RESOLVED.value:
                return {"status": "error", "message": f"Alert {alert_id} is already resolved"}
            
            # Update alert
            alert["status"] = AlertStatus.RESOLVED.value
            alert["resolved_time"] = time.time()
            alert["resolved_by"] = user
            alert["last_updated"] = time.time()
            
            result = {
                "status": "success",
                "alert_id": alert_id,
                "status": AlertStatus.RESOLVED.value,
                "resolved_by": user,
                "resolved_time": alert["resolved_time"],
                "message": "Alert resolved successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to resolve alert: {str(e)}"}
    
    def suppress_alert(self, alert_id: str, reason: str, 
                      user: str = "system") -> Dict[str, Any]:
        """
        Suppress an alert.
        
        Args:
            alert_id: Alert ID
            reason: Reason for suppression
            user: User suppressing the alert
            
        Returns:
            Suppression result
        """
        try:
            if alert_id not in self.alerts:
                return {"status": "error", "message": f"Alert {alert_id} not found"}
            
            alert = self.alerts[alert_id]
            
            # Update alert
            alert["status"] = AlertStatus.SUPPRESSED.value
            alert["suppressed_time"] = time.time()
            alert["suppressed_by"] = user
            alert["suppression_reason"] = reason
            alert["last_updated"] = time.time()
            
            result = {
                "status": "success",
                "alert_id": alert_id,
                "status": AlertStatus.SUPPRESSED.value,
                "suppressed_by": user,
                "suppression_reason": reason,
                "suppressed_time": alert["suppressed_time"],
                "message": "Alert suppressed successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to suppress alert: {str(e)}"}
    
    def get_active_alerts(self) -> Dict[str, Any]:
        """
        Get all active alerts.
        
        Returns:
            Active alerts result
        """
        try:
            active_alerts = []
            
            for alert_id, alert in self.alerts.items():
                if alert["status"] == AlertStatus.ACTIVE.value:
                    active_alerts.append(alert)
            
            result = {
                "status": "success",
                "active_alerts": active_alerts,
                "n_active": len(active_alerts)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get active alerts: {str(e)}"}
    
    def get_alert_history(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get alert history.
        
        Args:
            limit: Maximum number of alerts to return
            
        Returns:
            Alert history result
        """
        try:
            # Sort by creation time (newest first)
            sorted_history = sorted(self.alert_history, key=lambda x: x["created_time"], reverse=True)
            
            # Limit results
            limited_history = sorted_history[:limit]
            
            result = {
                "status": "success",
                "alert_history": limited_history,
                "n_alerts": len(limited_history),
                "total_alerts": len(self.alert_history)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get alert history: {str(e)}"}
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """
        Get alert statistics.
        
        Returns:
            Alert statistics result
        """
        try:
            # Calculate statistics
            total_alerts = len(self.alert_history)
            active_alerts = len([a for a in self.alerts.values() if a["status"] == AlertStatus.ACTIVE.value])
            resolved_alerts = len([a for a in self.alerts.values() if a["status"] == AlertStatus.RESOLVED.value])
            acknowledged_alerts = len([a for a in self.alerts.values() if a["status"] == AlertStatus.ACKNOWLEDGED.value])
            suppressed_alerts = len([a for a in self.alerts.values() if a["status"] == AlertStatus.SUPPRESSED.value])
            
            # Count by severity
            severity_counts = {}
            for alert in self.alert_history:
                severity = alert["severity"]
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Count by rule
            rule_counts = {}
            for alert in self.alert_history:
                rule_name = alert["rule_name"]
                rule_counts[rule_name] = rule_counts.get(rule_name, 0) + 1
            
            statistics = {
                "total_alerts": total_alerts,
                "active_alerts": active_alerts,
                "resolved_alerts": resolved_alerts,
                "acknowledged_alerts": acknowledged_alerts,
                "suppressed_alerts": suppressed_alerts,
                "severity_counts": severity_counts,
                "rule_counts": rule_counts,
                "n_rules": len(self.alert_rules),
                "n_channels": len(self.notification_channels),
                "n_policies": len(self.escalation_policies)
            }
            
            result = {
                "status": "success",
                "statistics": statistics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get alert statistics: {str(e)}"}
    
    def send_notification(self, alert_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Send notification for an alert.
        
        Args:
            alert_id: Alert ID
            channel_id: Channel ID
            
        Returns:
            Notification result
        """
        try:
            if alert_id not in self.alerts:
                return {"status": "error", "message": f"Alert {alert_id} not found"}
            
            if channel_id not in self.notification_channels:
                return {"status": "error", "message": f"Channel {channel_id} not found"}
            
            alert = self.alerts[alert_id]
            channel = self.notification_channels[channel_id]
            
            if not channel["enabled"]:
                return {"status": "error", "message": f"Channel {channel_id} is disabled"}
            
            # Create notification message
            notification_message = {
                "alert_id": alert_id,
                "rule_name": alert["rule_name"],
                "severity": alert["severity"],
                "metric_name": alert["metric_name"],
                "metric_value": alert["metric_value"],
                "threshold": alert["threshold"],
                "condition": alert["condition"],
                "created_time": alert["created_time"],
                "channel_type": channel["type"],
                "channel_name": channel["name"]
            }
            
            # Simulate sending notification
            notification_id = f"notif_{int(time.time())}"
            
            result = {
                "status": "success",
                "notification_id": notification_id,
                "alert_id": alert_id,
                "channel_id": channel_id,
                "channel_type": channel["type"],
                "message": notification_message,
                "sent_time": time.time(),
                "message": "Notification sent successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to send notification: {str(e)}"}
    
    def create_suppression_rule(self, rule_name: str, conditions: Dict[str, Any],
                               duration: str = "1h") -> Dict[str, Any]:
        """
        Create a suppression rule.
        
        Args:
            rule_name: Name of the suppression rule
            conditions: Conditions for suppression
            duration: Duration of suppression
            
        Returns:
            Suppression rule creation result
        """
        try:
            # Generate suppression rule ID
            suppression_id = f"suppression_{int(time.time())}"
            
            # Create suppression rule
            suppression_rule = {
                "id": suppression_id,
                "name": rule_name,
                "conditions": conditions,
                "duration": duration,
                "enabled": True,
                "created_time": time.time(),
                "last_updated": time.time()
            }
            
            # Store suppression rule
            self.suppression_rules[suppression_id] = suppression_rule
            
            result = {
                "status": "success",
                "suppression_id": suppression_id,
                "rule_name": rule_name,
                "conditions": conditions,
                "duration": duration,
                "message": "Suppression rule created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create suppression rule: {str(e)}"}
