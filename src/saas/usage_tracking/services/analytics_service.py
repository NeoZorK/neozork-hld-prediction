"""
Analytics Service

This service provides advanced analytics and reporting capabilities
for usage tracking data.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import asdict

from ..models import UsageMetric, UsageEvent, MetricType, MetricValue

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service for advanced analytics and reporting.
    
    This service provides functionality to:
    - Generate analytics reports
    - Calculate trends and patterns
    - Provide insights and recommendations
    - Create custom dashboards
    """
    
    def __init__(self, storage_backend=None, usage_tracker=None):
        """
        Initialize the analytics service.
        
        Args:
            storage_backend: Storage backend for data access
            usage_tracker: Usage tracker service
        """
        self.storage_backend = storage_backend
        self.usage_tracker = usage_tracker
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes
    
    async def get_usage_analytics(self, tenant_id: str, resource_type: str,
                                period_start: datetime, period_end: datetime,
                                granularity: str = "hour") -> Dict[str, Any]:
        """
        Get comprehensive usage analytics.
        
        Args:
            tenant_id: Tenant ID
            resource_type: Resource type
            period_start: Start of period
            period_end: End of period
            granularity: Time granularity
            
        Returns:
            Analytics data dictionary
        """
        cache_key = f"analytics:{tenant_id}:{resource_type}:{period_start}:{period_end}:{granularity}"
        
        # Check cache
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if (datetime.utcnow() - timestamp).seconds < self._cache_ttl:
                return cached_data
        
        # Get metrics
        metrics = await self.usage_tracker.get_usage_metrics(
            tenant_id, resource_type, period_start, period_end, granularity
        )
        
        # Calculate analytics
        analytics = await self._calculate_analytics(metrics, period_start, period_end)
        
        # Cache result
        self._cache[cache_key] = (analytics, datetime.utcnow())
        
        return analytics
    
    async def get_usage_trends(self, tenant_id: str, resource_type: str,
                             period_start: datetime, period_end: datetime,
                             granularity: str = "day") -> Dict[str, Any]:
        """
        Get usage trends and patterns.
        
        Args:
            tenant_id: Tenant ID
            resource_type: Resource type
            period_start: Start of period
            period_end: End of period
            granularity: Time granularity
            
        Returns:
            Trends data dictionary
        """
        metrics = await self.usage_tracker.get_usage_metrics(
            tenant_id, resource_type, period_start, period_end, granularity
        )
        
        if not metrics:
            return {
                "trend": "stable",
                "growth_rate": 0.0,
                "volatility": 0.0,
                "seasonality": False,
                "anomalies": []
            }
        
        # Calculate trend
        trend = await self._calculate_trend(metrics)
        
        # Calculate growth rate
        growth_rate = await self._calculate_growth_rate(metrics)
        
        # Calculate volatility
        volatility = await self._calculate_volatility(metrics)
        
        # Detect seasonality
        seasonality = await self._detect_seasonality(metrics)
        
        # Detect anomalies
        anomalies = await self._detect_anomalies(metrics)
        
        return {
            "trend": trend,
            "growth_rate": growth_rate,
            "volatility": volatility,
            "seasonality": seasonality,
            "anomalies": anomalies
        }
    
    async def get_usage_forecast(self, tenant_id: str, resource_type: str,
                               forecast_days: int = 30) -> Dict[str, Any]:
        """
        Get usage forecast for future periods.
        
        Args:
            tenant_id: Tenant ID
            resource_type: Resource type
            forecast_days: Number of days to forecast
            
        Returns:
            Forecast data dictionary
        """
        # Get historical data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)  # Use 90 days of history
        
        metrics = await self.usage_tracker.get_usage_metrics(
            tenant_id, resource_type, start_date, end_date, "day"
        )
        
        if not metrics:
            return {
                "forecast": [],
                "confidence": 0.0,
                "method": "insufficient_data"
            }
        
        # Generate forecast
        forecast = await self._generate_forecast(metrics, forecast_days)
        
        return forecast
    
    async def get_usage_insights(self, tenant_id: str, resource_type: str,
                               period_start: datetime, period_end: datetime) -> List[Dict[str, Any]]:
        """
        Get usage insights and recommendations.
        
        Args:
            tenant_id: Tenant ID
            resource_type: Resource type
            period_start: Start of period
            period_end: End of period
            
        Returns:
            List of insights
        """
        insights = []
        
        # Get metrics
        metrics = await self.usage_tracker.get_usage_metrics(
            tenant_id, resource_type, period_start, period_end, "day"
        )
        
        if not metrics:
            return insights
        
        # Analyze usage patterns
        patterns = await self._analyze_usage_patterns(metrics)
        insights.extend(patterns)
        
        # Check for optimization opportunities
        optimizations = await self._find_optimization_opportunities(metrics)
        insights.extend(optimizations)
        
        # Check for cost savings
        cost_savings = await self._find_cost_savings(metrics)
        insights.extend(cost_savings)
        
        return insights
    
    async def get_usage_comparison(self, tenant_id: str, resource_type: str,
                                 current_period_start: datetime, current_period_end: datetime,
                                 previous_period_start: datetime, previous_period_end: datetime) -> Dict[str, Any]:
        """
        Compare usage between two periods.
        
        Args:
            tenant_id: Tenant ID
            resource_type: Resource type
            current_period_start: Current period start
            current_period_end: Current period end
            previous_period_start: Previous period start
            previous_period_end: Previous period end
            
        Returns:
            Comparison data dictionary
        """
        # Get current period metrics
        current_metrics = await self.usage_tracker.get_usage_metrics(
            tenant_id, resource_type, current_period_start, current_period_end, "day"
        )
        
        # Get previous period metrics
        previous_metrics = await self.usage_tracker.get_usage_metrics(
            tenant_id, resource_type, previous_period_start, previous_period_end, "day"
        )
        
        # Calculate comparison
        comparison = await self._calculate_comparison(current_metrics, previous_metrics)
        
        return comparison
    
    async def get_usage_breakdown(self, tenant_id: str, resource_type: str,
                                period_start: datetime, period_end: datetime,
                                breakdown_by: str = "user") -> Dict[str, Any]:
        """
        Get usage breakdown by different dimensions.
        
        Args:
            tenant_id: Tenant ID
            resource_type: Resource type
            period_start: Start of period
            period_end: End of period
            breakdown_by: Dimension to breakdown by (user, endpoint, etc.)
            
        Returns:
            Breakdown data dictionary
        """
        if not self.storage_backend:
            return {}
        
        # Get events for the period
        events = await self.storage_backend.get_events(
            tenant_id=tenant_id,
            resource_type=resource_type,
            period_start=period_start,
            period_end=period_end
        )
        
        # Group by breakdown dimension
        breakdown = await self._group_by_dimension(events, breakdown_by)
        
        return breakdown
    
    async def _calculate_analytics(self, metrics: List[UsageMetric], 
                                 period_start: datetime, period_end: datetime) -> Dict[str, Any]:
        """Calculate comprehensive analytics from metrics."""
        if not metrics:
            return {
                "total_usage": 0.0,
                "average_usage": 0.0,
                "peak_usage": 0.0,
                "usage_distribution": [],
                "cost_analysis": {},
                "efficiency_metrics": {}
            }
        
        # Calculate basic metrics
        total_usage = sum(metric.get_value(MetricValue.SUM) for metric in metrics)
        average_usage = total_usage / len(metrics) if metrics else 0.0
        peak_usage = max(metric.get_value(MetricValue.SUM) for metric in metrics)
        
        # Calculate usage distribution
        usage_distribution = []
        for metric in metrics:
            usage_distribution.append({
                "timestamp": metric.period_start.isoformat(),
                "usage": metric.get_value(MetricValue.SUM),
                "cost": metric.total_cost
            })
        
        # Calculate cost analysis
        total_cost = sum(metric.total_cost for metric in metrics)
        cost_per_unit = total_cost / total_usage if total_usage > 0 else 0.0
        
        cost_analysis = {
            "total_cost": total_cost,
            "cost_per_unit": cost_per_unit,
            "currency": metrics[0].currency if metrics else "USD"
        }
        
        # Calculate efficiency metrics
        efficiency_metrics = {
            "utilization_rate": await self._calculate_utilization_rate(metrics),
            "consistency_score": await self._calculate_consistency_score(metrics),
            "growth_rate": await self._calculate_growth_rate(metrics)
        }
        
        return {
            "total_usage": total_usage,
            "average_usage": average_usage,
            "peak_usage": peak_usage,
            "usage_distribution": usage_distribution,
            "cost_analysis": cost_analysis,
            "efficiency_metrics": efficiency_metrics
        }
    
    async def _calculate_trend(self, metrics: List[UsageMetric]) -> str:
        """Calculate trend from metrics."""
        if len(metrics) < 2:
            return "stable"
        
        # Simple linear trend calculation
        values = [metric.get_value(MetricValue.SUM) for metric in metrics]
        n = len(values)
        
        # Calculate slope
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x2_sum = sum(i * i for i in range(n))
        
        slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum)
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    async def _calculate_growth_rate(self, metrics: List[UsageMetric]) -> float:
        """Calculate growth rate from metrics."""
        if len(metrics) < 2:
            return 0.0
        
        first_value = metrics[0].get_value(MetricValue.SUM)
        last_value = metrics[-1].get_value(MetricValue.SUM)
        
        if first_value == 0:
            return 0.0
        
        return ((last_value - first_value) / first_value) * 100
    
    async def _calculate_volatility(self, metrics: List[UsageMetric]) -> float:
        """Calculate volatility from metrics."""
        if len(metrics) < 2:
            return 0.0
        
        values = [metric.get_value(MetricValue.SUM) for metric in metrics]
        mean = sum(values) / len(values)
        
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return (variance ** 0.5) / mean if mean > 0 else 0.0
    
    async def _detect_seasonality(self, metrics: List[UsageMetric]) -> bool:
        """Detect seasonality in metrics."""
        if len(metrics) < 7:  # Need at least a week of data
            return False
        
        # Simple seasonality detection based on day-of-week patterns
        daily_values = {}
        for metric in metrics:
            day = metric.period_start.weekday()
            if day not in daily_values:
                daily_values[day] = []
            daily_values[day].append(metric.get_value(MetricValue.SUM))
        
        # Calculate coefficient of variation for each day
        day_cvs = []
        for day_values in daily_values.values():
            if len(day_values) > 1:
                mean = sum(day_values) / len(day_values)
                std = (sum((x - mean) ** 2 for x in day_values) / len(day_values)) ** 0.5
                cv = std / mean if mean > 0 else 0
                day_cvs.append(cv)
        
        # If there's significant variation between days, it's seasonal
        return len(day_cvs) > 0 and max(day_cvs) > 0.2
    
    async def _detect_anomalies(self, metrics: List[UsageMetric]) -> List[Dict[str, Any]]:
        """Detect anomalies in metrics."""
        if len(metrics) < 3:
            return []
        
        values = [metric.get_value(MetricValue.SUM) for metric in metrics]
        mean = sum(values) / len(values)
        std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
        
        anomalies = []
        for i, (metric, value) in enumerate(zip(metrics, values)):
            if abs(value - mean) > 2 * std:  # 2-sigma rule
                anomalies.append({
                    "timestamp": metric.period_start.isoformat(),
                    "value": value,
                    "expected_range": [mean - 2 * std, mean + 2 * std],
                    "severity": "high" if abs(value - mean) > 3 * std else "medium"
                })
        
        return anomalies
    
    async def _generate_forecast(self, metrics: List[UsageMetric], forecast_days: int) -> Dict[str, Any]:
        """Generate usage forecast."""
        if len(metrics) < 7:  # Need at least a week of data
            return {
                "forecast": [],
                "confidence": 0.0,
                "method": "insufficient_data"
            }
        
        # Simple linear regression forecast
        values = [metric.get_value(MetricValue.SUM) for metric in metrics]
        n = len(values)
        
        # Calculate trend
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x2_sum = sum(i * i for i in range(n))
        
        slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum)
        intercept = (y_sum - slope * x_sum) / n
        
        # Generate forecast
        forecast = []
        for i in range(forecast_days):
            predicted_value = slope * (n + i) + intercept
            forecast.append({
                "date": (metrics[-1].period_end + timedelta(days=i+1)).isoformat(),
                "predicted_usage": max(0, predicted_value),
                "confidence": max(0, 1.0 - (i * 0.1))  # Decreasing confidence over time
            })
        
        return {
            "forecast": forecast,
            "confidence": 0.8,
            "method": "linear_regression"
        }
    
    async def _analyze_usage_patterns(self, metrics: List[UsageMetric]) -> List[Dict[str, Any]]:
        """Analyze usage patterns and generate insights."""
        insights = []
        
        # Peak usage analysis
        peak_usage = max(metric.get_value(MetricValue.SUM) for metric in metrics)
        peak_metric = next(metric for metric in metrics if metric.get_value(MetricValue.SUM) == peak_usage)
        
        insights.append({
            "type": "peak_usage",
            "title": "Peak Usage Detected",
            "description": f"Peak usage of {peak_usage:.2f} occurred on {peak_metric.period_start.strftime('%Y-%m-%d')}",
            "severity": "info",
            "recommendation": "Consider scaling resources during peak periods"
        })
        
        # Low usage analysis
        low_usage_threshold = peak_usage * 0.1
        low_usage_days = [metric for metric in metrics if metric.get_value(MetricValue.SUM) < low_usage_threshold]
        
        if len(low_usage_days) > len(metrics) * 0.3:  # More than 30% of days
            insights.append({
                "type": "low_usage",
                "title": "Frequent Low Usage Periods",
                "description": f"Low usage detected on {len(low_usage_days)} days",
                "severity": "warning",
                "recommendation": "Consider optimizing resource allocation or implementing auto-scaling"
            })
        
        return insights
    
    async def _find_optimization_opportunities(self, metrics: List[UsageMetric]) -> List[Dict[str, Any]]:
        """Find optimization opportunities."""
        insights = []
        
        # Calculate efficiency metrics
        total_usage = sum(metric.get_value(MetricValue.SUM) for metric in metrics)
        total_cost = sum(metric.total_cost for metric in metrics)
        
        if total_usage > 0 and total_cost > 0:
            cost_per_unit = total_cost / total_usage
            
            insights.append({
                "type": "cost_optimization",
                "title": "Cost Optimization Opportunity",
                "description": f"Current cost per unit: {cost_per_unit:.4f}",
                "severity": "info",
                "recommendation": "Review pricing tiers and usage patterns for cost optimization"
            })
        
        return insights
    
    async def _find_cost_savings(self, metrics: List[UsageMetric]) -> List[Dict[str, Any]]:
        """Find cost savings opportunities."""
        insights = []
        
        # Analyze cost trends
        if len(metrics) >= 7:
            recent_cost = sum(metric.total_cost for metric in metrics[-7:])
            previous_cost = sum(metric.total_cost for metric in metrics[-14:-7]) if len(metrics) >= 14 else recent_cost
            
            if previous_cost > 0:
                cost_change = ((recent_cost - previous_cost) / previous_cost) * 100
                
                if cost_change > 20:
                    insights.append({
                        "type": "cost_increase",
                        "title": "Significant Cost Increase",
                        "description": f"Cost increased by {cost_change:.1f}% in the last week",
                        "severity": "warning",
                        "recommendation": "Investigate usage patterns and consider cost controls"
                    })
                elif cost_change < -20:
                    insights.append({
                        "type": "cost_decrease",
                        "title": "Cost Reduction Achieved",
                        "description": f"Cost decreased by {abs(cost_change):.1f}% in the last week",
                        "severity": "success",
                        "recommendation": "Continue monitoring for sustained savings"
                    })
        
        return insights
    
    async def _calculate_comparison(self, current_metrics: List[UsageMetric], 
                                  previous_metrics: List[UsageMetric]) -> Dict[str, Any]:
        """Calculate comparison between two periods."""
        current_total = sum(metric.get_value(MetricValue.SUM) for metric in current_metrics)
        previous_total = sum(metric.get_value(MetricValue.SUM) for metric in previous_metrics)
        
        if previous_total == 0:
            return {
                "change_percentage": 0.0,
                "change_absolute": current_total,
                "trend": "stable"
            }
        
        change_percentage = ((current_total - previous_total) / previous_total) * 100
        change_absolute = current_total - previous_total
        
        if change_percentage > 10:
            trend = "increasing"
        elif change_percentage < -10:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "change_percentage": change_percentage,
            "change_absolute": change_absolute,
            "trend": trend,
            "current_total": current_total,
            "previous_total": previous_total
        }
    
    async def _group_by_dimension(self, events: List[UsageEvent], dimension: str) -> Dict[str, Any]:
        """Group events by specified dimension."""
        groups = {}
        
        for event in events:
            if dimension == "user":
                key = event.user_id or "anonymous"
            elif dimension == "endpoint":
                key = event.metadata.get("endpoint", "unknown")
            elif dimension == "method":
                key = event.metadata.get("method", "unknown")
            else:
                key = "unknown"
            
            if key not in groups:
                groups[key] = {
                    "count": 0,
                    "total_usage": 0.0,
                    "total_cost": 0.0
                }
            
            groups[key]["count"] += 1
            groups[key]["total_usage"] += event.quantity
            groups[key]["total_cost"] += event.total_cost
        
        return groups
    
    async def _calculate_utilization_rate(self, metrics: List[UsageMetric]) -> float:
        """Calculate utilization rate."""
        if not metrics:
            return 0.0
        
        peak_usage = max(metric.get_value(MetricValue.SUM) for metric in metrics)
        average_usage = sum(metric.get_value(MetricValue.SUM) for metric in metrics) / len(metrics)
        
        return (average_usage / peak_usage) * 100 if peak_usage > 0 else 0.0
    
    async def _calculate_consistency_score(self, metrics: List[UsageMetric]) -> float:
        """Calculate consistency score (0-1, higher is more consistent)."""
        if len(metrics) < 2:
            return 1.0
        
        values = [metric.get_value(MetricValue.SUM) for metric in metrics]
        mean = sum(values) / len(values)
        
        if mean == 0:
            return 1.0
        
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        coefficient_of_variation = (variance ** 0.5) / mean
        
        # Convert to 0-1 scale (lower CV = higher consistency)
        return max(0, 1 - coefficient_of_variation)
