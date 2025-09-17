"""Monitoring System - Real-time investor monitoring"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Alert level enumeration."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class MonitoringMetric(Enum):
    """Monitoring metric enumeration."""
    PORTFOLIO_VALUE = "portfolio_value"
    PERFORMANCE = "performance"
    RISK = "risk"
    LIQUIDITY = "liquidity"
    CONCENTRATION = "concentration"


@dataclass
class Alert:
    """Alert data class."""
    alert_id: str
    investor_id: str
    metric: MonitoringMetric
    level: AlertLevel
    message: str
    value: float
    threshold: float
    timestamp: datetime
    acknowledged: bool = False


class MonitoringSystem:
    """Real-time investor monitoring system."""
    
    def __init__(self):
        self.investor_alerts: Dict[str, List[Alert]] = {}
        self.monitoring_rules: Dict[str, Dict[str, Any]] = {}
        self.metric_history: Dict[str, List[Dict[str, Any]]] = {}
        
    async def monitor_investor(self, investor_id: str, 
                             portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor investor portfolio and generate alerts."""
        try:
            alerts = []
            
            # Check portfolio value changes
            value_alerts = await self._check_portfolio_value(investor_id, portfolio_data)
            alerts.extend(value_alerts)
            
            # Check performance metrics
            performance_alerts = await self._check_performance_metrics(investor_id, portfolio_data)
            alerts.extend(performance_alerts)
            
            # Check risk metrics
            risk_alerts = await self._check_risk_metrics(investor_id, portfolio_data)
            alerts.extend(risk_alerts)
            
            # Store alerts
            if investor_id not in self.investor_alerts:
                self.investor_alerts[investor_id] = []
            self.investor_alerts[investor_id].extend(alerts)
            
            # Store metric history
            await self._store_metric_history(investor_id, portfolio_data)
            
            logger.info(f"Monitored investor {investor_id}: {len(alerts)} alerts generated")
            return {
                'investor_id': investor_id,
                'alerts_generated': len(alerts),
                'alerts': [alert.__dict__ for alert in alerts],
                'monitoring_timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Failed to monitor investor: {e}")
            return {'error': str(e)}
    
    async def get_investor_alerts(self, investor_id: str, 
                                unread_only: bool = False) -> Dict[str, Any]:
        """Get alerts for a specific investor."""
        try:
            if investor_id not in self.investor_alerts:
                return {'alerts': [], 'total_count': 0}
            
            alerts = self.investor_alerts[investor_id]
            
            if unread_only:
                alerts = [alert for alert in alerts if not alert.acknowledged]
            
            # Sort by timestamp (newest first)
            alerts.sort(key=lambda x: x.timestamp, reverse=True)
            
            return {
                'investor_id': investor_id,
                'alerts': [alert.__dict__ for alert in alerts],
                'total_count': len(alerts),
                'unread_count': len([a for a in self.investor_alerts[investor_id] if not a.acknowledged])
            }
            
        except Exception as e:
            logger.error(f"Failed to get investor alerts: {e}")
            return {'error': str(e)}
    
    async def acknowledge_alert(self, investor_id: str, alert_id: str) -> Dict[str, Any]:
        """Acknowledge an alert."""
        try:
            if investor_id not in self.investor_alerts:
                return {'error': 'Investor not found'}
            
            for alert in self.investor_alerts[investor_id]:
                if alert.alert_id == alert_id:
                    alert.acknowledged = True
                    logger.info(f"Acknowledged alert {alert_id} for investor {investor_id}")
                    return {'status': 'success', 'alert_id': alert_id}
            
            return {'error': 'Alert not found'}
            
        except Exception as e:
            logger.error(f"Failed to acknowledge alert: {e}")
            return {'error': str(e)}
    
    async def _check_portfolio_value(self, investor_id: str, 
                                   portfolio_data: Dict[str, Any]) -> List[Alert]:
        """Check portfolio value for alerts."""
        alerts = []
        
        # TODO: Implement portfolio value monitoring
        # Check for significant drops, gains, etc.
        
        return alerts
    
    async def _check_performance_metrics(self, investor_id: str, 
                                       portfolio_data: Dict[str, Any]) -> List[Alert]:
        """Check performance metrics for alerts."""
        alerts = []
        
        # TODO: Implement performance monitoring
        # Check for underperformance, excessive volatility, etc.
        
        return alerts
    
    async def _check_risk_metrics(self, investor_id: str, 
                                portfolio_data: Dict[str, Any]) -> List[Alert]:
        """Check risk metrics for alerts."""
        alerts = []
        
        # TODO: Implement risk monitoring
        # Check for risk limit breaches, concentration issues, etc.
        
        return alerts
    
    async def _store_metric_history(self, investor_id: str, 
                                  portfolio_data: Dict[str, Any]) -> None:
        """Store metric history for trend analysis."""
        if investor_id not in self.metric_history:
            self.metric_history[investor_id] = []
        
        metric_record = {
            'timestamp': datetime.now(),
            'portfolio_value': portfolio_data.get('total_value', 0),
            'daily_return': portfolio_data.get('daily_return', 0),
            'risk_metrics': portfolio_data.get('risk_metrics', {})
        }
        
        self.metric_history[investor_id].append(metric_record)
        
        # Keep only last 1000 records
        if len(self.metric_history[investor_id]) > 1000:
            self.metric_history[investor_id] = self.metric_history[investor_id][-1000:]