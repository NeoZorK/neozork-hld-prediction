# 📊 NeoZork SaaS Usage Tracking

## 📋 Overview

The Usage Tracking module provides comprehensive tracking, analytics, and monitoring capabilities for the NeoZork SaaS platform. It enables real-time monitoring of resource consumption, usage limits enforcement, and advanced analytics for business intelligence.

## 🏗️ Architecture

### Core Components

- **Usage Tracker**: Core service for recording and processing usage events
- **Analytics Service**: Advanced analytics and reporting capabilities
- **Monitoring Service**: Real-time monitoring and alerting
- **Limits Service**: Usage limits and quota management
- **Reporting Service**: Report generation and export
- **Alert Service**: Notification and alerting system

### Models

- **UsageEvent**: Individual usage events and resource consumption
- **UsageMetric**: Aggregated metrics and statistics
- **UsageLimit**: Usage limits and quotas
- **UsageAnalytics**: Analytics data and insights
- **UsageAlert**: Alert definitions and notifications
- **UsageReport**: Generated reports and exports

## 🚀 Quick Start

### Installation

```python
from src.saas.usage_tracking import UsageTracker, AnalyticsService
from src.saas.usage_tracking.models import UsageEvent, EventType
```

### Basic Usage

```python
# Initialize usage tracker
usage_tracker = UsageTracker(storage_backend=storage, limits_service=limits)

# Start the tracker
await usage_tracker.start()

# Record an API call
event_id = await usage_tracker.record_api_call(
    tenant_id="tenant-1",
    user_id="user-1",
    endpoint="/api/users",
    method="GET",
    response_time_ms=150,
    status_code=200
)

# Record storage usage
event_id = await usage_tracker.record_storage_usage(
    tenant_id="tenant-1",
    user_id="user-1",
    operation="write",
    size_bytes=1024,
    file_type="image/jpeg"
)

# Get current usage
current_usage = await usage_tracker.get_current_usage(
    tenant_id="tenant-1",
    resource_type="api_calls"
)
```

## 📚 API Reference

### Usage Tracker

#### `record_event(event: UsageEvent) -> str`
Record a usage event and return the event ID.

#### `record_api_call(tenant_id: str, user_id: str, endpoint: str, method: str, **kwargs) -> str`
Record an API call event with automatic event creation.

#### `record_storage_usage(tenant_id: str, user_id: str, operation: str, size_bytes: int, **kwargs) -> str`
Record storage usage event.

#### `record_database_query(tenant_id: str, user_id: str, query_type: str, table: str, **kwargs) -> str`
Record database query event.

#### `get_usage_metrics(tenant_id: str, resource_type: str, period_start: datetime, period_end: datetime, granularity: str) -> List[UsageMetric]`
Get aggregated usage metrics for a specific period.

#### `get_current_usage(tenant_id: str, resource_type: str) -> float`
Get current usage for a tenant and resource type.

#### `check_limit(tenant_id: str, resource_type: str) -> Tuple[bool, Optional[UsageLimit]]`
Check if usage is within limits.

### Analytics Service

#### `get_usage_analytics(tenant_id: str, resource_type: str, period_start: datetime, period_end: datetime, granularity: str) -> Dict[str, Any]`
Get comprehensive usage analytics including trends, costs, and efficiency metrics.

#### `get_usage_trends(tenant_id: str, resource_type: str, period_start: datetime, period_end: datetime, granularity: str) -> Dict[str, Any]`
Get usage trends and patterns including growth rate, volatility, and seasonality.

#### `get_usage_forecast(tenant_id: str, resource_type: str, forecast_days: int) -> Dict[str, Any]`
Get usage forecast for future periods using machine learning models.

#### `get_usage_insights(tenant_id: str, resource_type: str, period_start: datetime, period_end: datetime) -> List[Dict[str, Any]]`
Get usage insights and recommendations for optimization.

#### `get_usage_comparison(tenant_id: str, resource_type: str, current_period_start: datetime, current_period_end: datetime, previous_period_start: datetime, previous_period_end: datetime) -> Dict[str, Any]`
Compare usage between two periods.

#### `get_usage_breakdown(tenant_id: str, resource_type: str, period_start: datetime, period_end: datetime, breakdown_by: str) -> Dict[str, Any]`
Get usage breakdown by different dimensions (user, endpoint, etc.).

## 🔧 Configuration

### Environment Variables

```bash
# Usage Tracking Configuration
USAGE_TRACKING_ENABLED=true
USAGE_TRACKING_STORAGE_BACKEND=redis
USAGE_TRACKING_REDIS_URL=redis://localhost:6379
USAGE_TRACKING_METRICS_RETENTION_DAYS=90
USAGE_TRACKING_EVENTS_RETENTION_DAYS=30

# Analytics Configuration
ANALYTICS_CACHE_TTL=300
ANALYTICS_FORECAST_MODEL=linear_regression
ANALYTICS_ANOMALY_DETECTION_THRESHOLD=2.0

# Limits Configuration
LIMITS_ENFORCEMENT_ENABLED=true
LIMITS_GRACE_PERIOD_MINUTES=5
LIMITS_NOTIFICATION_ENABLED=true
```

### Storage Backend

The usage tracking system supports multiple storage backends:

- **Redis**: High-performance in-memory storage for real-time data
- **PostgreSQL**: Relational database for persistent storage
- **MongoDB**: Document database for flexible schema
- **InfluxDB**: Time-series database for metrics

### Limits Configuration

```python
from src.saas.usage_tracking.models import UsageLimit, LimitType, LimitStatus

# Create a usage limit
limit = UsageLimit(
    tenant_id="tenant-1",
    limit_name="API Calls Monthly Limit",
    limit_type=LimitType.HARD_LIMIT,
    resource_type="api_calls",
    limit_value=10000.0,
    unit="calls",
    period_type="month",
    period_value=1,
    status=LimitStatus.ACTIVE,
    enforce_immediately=True,
    warning_threshold=0.8,
    warning_message="Approaching API call limit"
)
```

## 📊 Analytics Features

### Real-time Metrics

- **Current Usage**: Real-time usage tracking
- **Usage Trends**: Growth rates and patterns
- **Peak Usage**: Identification of peak periods
- **Cost Analysis**: Cost per unit and total costs

### Advanced Analytics

- **Forecasting**: ML-based usage predictions
- **Anomaly Detection**: Automatic detection of unusual patterns
- **Seasonality Analysis**: Identification of seasonal patterns
- **Optimization Insights**: Recommendations for cost and efficiency

### Reporting

- **Usage Reports**: Detailed usage reports by period
- **Cost Reports**: Cost analysis and breakdowns
- **Trend Reports**: Usage trend analysis
- **Custom Reports**: Configurable report generation

## 🚨 Monitoring and Alerts

### Alert Types

- **Usage Threshold Alerts**: When usage approaches limits
- **Limit Exceeded Alerts**: When limits are exceeded
- **Anomaly Alerts**: When unusual patterns are detected
- **Cost Alerts**: When costs exceed thresholds

### Notification Channels

- **Email**: Email notifications for alerts
- **Webhook**: HTTP webhook notifications
- **Slack**: Slack channel notifications
- **SMS**: SMS notifications for critical alerts

### Alert Configuration

```python
from src.saas.usage_tracking.models import UsageAlert, AlertType, AlertStatus

# Create an alert
alert = UsageAlert(
    tenant_id="tenant-1",
    alert_name="High API Usage",
    alert_type=AlertType.USAGE_THRESHOLD,
    resource_type="api_calls",
    threshold_value=8000.0,
    threshold_percentage=80.0,
    status=AlertStatus.ACTIVE,
    notification_emails=["admin@example.com"],
    webhook_url="https://hooks.slack.com/..."
)
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest src/saas/usage_tracking/__tests__/

# Run specific test file
pytest src/saas/usage_tracking/__tests__/test_usage_tracker.py

# Run with coverage
pytest --cov=src.saas.usage_tracking src/saas/usage_tracking/__tests__/
```

### Test Coverage

The usage tracking module has comprehensive test coverage including:

- Unit tests for all services
- Integration tests for API endpoints
- Performance tests for high-load scenarios
- End-to-end tests for complete workflows

## 🔧 Development

### Adding New Event Types

```python
from src.saas.usage_tracking.models import EventType

# Add new event type
EventType.CUSTOM_EVENT = "custom_event"

# Use in events
event = UsageEvent(
    tenant_id="tenant-1",
    event_type=EventType.CUSTOM_EVENT,
    event_name="Custom Event",
    resource_consumed="custom_resource",
    quantity=1.0
)
```

### Adding New Metrics

```python
from src.saas.usage_tracking.models import MetricType, MetricValue

# Add new metric type
MetricType.CUSTOM_METRIC = "custom_metric"

# Add new metric value
MetricValue.CUSTOM_VALUE = "custom_value"
```

### Custom Storage Backend

```python
from src.saas.usage_tracking.services import UsageTracker

class CustomStorageBackend:
    async def store_event(self, event: UsageEvent):
        # Custom storage implementation
        pass
    
    async def get_events(self, **filters):
        # Custom retrieval implementation
        pass

# Use custom backend
usage_tracker = UsageTracker(storage_backend=CustomStorageBackend())
```

## 📈 Performance

### Optimization Features

- **Event Batching**: Batch multiple events for efficient processing
- **Async Processing**: Non-blocking event processing
- **Caching**: Intelligent caching for frequently accessed data
- **Compression**: Data compression for storage efficiency

### Scalability

- **Horizontal Scaling**: Support for multiple tracker instances
- **Load Balancing**: Distributed processing across multiple nodes
- **Sharding**: Data sharding for large-scale deployments
- **Caching**: Redis-based caching for high performance

## 🔒 Security

### Data Protection

- **Encryption**: Data encryption at rest and in transit
- **Access Control**: Role-based access control for sensitive data
- **Audit Logging**: Comprehensive audit logging for compliance
- **Data Retention**: Configurable data retention policies

### Privacy

- **Data Anonymization**: Automatic anonymization of sensitive data
- **GDPR Compliance**: Full GDPR compliance for data handling
- **Data Export**: User data export capabilities
- **Data Deletion**: Secure data deletion on request

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the NeoZork team
- Check the documentation

## 🔄 Version History

- **1.0.0** - Initial release with core usage tracking functionality
- **1.1.0** - Added advanced analytics and forecasting
- **1.2.0** - Added real-time monitoring and alerting
- **1.3.0** - Added usage limits and quota management
