# SaaS Billing Integration

This module provides comprehensive billing functionality for the SaaS platform, including payment processing, invoice management, webhook handling, and reporting.

## Features

### Payment Processing
- **Payment Models**: Payment and Invoice entities with status tracking
- **Payment Service**: Core business logic for payment operations
- **Stripe Integration**: Payment gateway integration with Stripe
- **Payment API**: RESTful API endpoints for payment operations

### Invoice Management
- **Invoice Generation**: Automated invoice creation and management
- **Invoice Status Tracking**: Draft, sent, paid, overdue status management
- **Tax Calculations**: Automatic tax calculation and application
- **Due Date Management**: Invoice due date tracking and reminders

### Webhook Handling
- **Stripe Webhooks**: Real-time event processing from Stripe
- **Event Processing**: Payment success, failure, and refund handling
- **Signature Verification**: Secure webhook signature validation
- **Error Handling**: Robust error handling and logging

### Reporting & Analytics
- **Billing Reports**: Comprehensive billing and revenue reports
- **Revenue Analytics**: MRR, ARR, growth rate, and churn analysis
- **Forecasting**: Revenue forecasting with confidence levels
- **Tenant Analytics**: Per-tenant billing and usage analytics

## Architecture

```
src/saas/billing/
├── models/                 # Data models
│   ├── payment.py         # Payment entity
│   └── invoice.py         # Invoice entity
├── services/              # Business logic
│   └── payment_service.py # Payment operations
├── integrations/          # External integrations
│   └── stripe_gateway.py  # Stripe payment gateway
├── api/                   # API endpoints
│   └── payment_api.py     # Payment API routes
├── webhooks/              # Webhook handlers
│   └── stripe_webhook.py  # Stripe webhook processing
├── reports/               # Reporting and analytics
│   ├── billing_reports.py # Billing reports
│   └── revenue_analytics.py # Revenue analytics
└── __tests__/             # Test files
    ├── test_payment_models.py
    ├── test_payment_service.py
    ├── test_stripe_gateway.py
    ├── test_payment_api.py
    ├── test_stripe_webhook.py
    ├── test_billing_reports.py
    └── test_revenue_analytics.py
```

## Usage

### Basic Payment Processing

```python
from src.saas.billing import PaymentService, StripeGateway

# Initialize services
payment_service = PaymentService()
stripe_gateway = StripeGateway(api_key="sk_test_...")

# Create payment
payment = await payment_service.create_payment(
    tenant_id="tenant_123",
    amount=Decimal("99.99"),
    currency="USD",
    payment_method=PaymentMethod.CREDIT_CARD
)

# Process payment
result = await payment_service.process_payment(payment)
```

### Invoice Management

```python
# Create invoice
invoice = await payment_service.create_invoice(
    tenant_id="tenant_123",
    amount=Decimal("199.99"),
    currency="USD",
    due_date=datetime.now() + timedelta(days=30)
)

# Send invoice
await payment_service.send_invoice(invoice.id)
```

### Webhook Processing

```python
from src.saas.billing import StripeWebhookHandler

# Initialize webhook handler
webhook_handler = StripeWebhookHandler(
    webhook_secret="whsec_...",
    payment_service=payment_service
)

# Handle webhook
result = await webhook_handler.handle_webhook(
    payload=payload,
    signature=signature,
    timestamp=timestamp
)
```

### Reporting

```python
from src.saas.billing import BillingReports, RevenueAnalytics

# Initialize reporting services
billing_reports = BillingReports(payment_service, invoice_service)
revenue_analytics = RevenueAnalytics(payment_service, invoice_service)

# Generate tenant report
report = await billing_reports.generate_tenant_report(
    tenant_id="tenant_123",
    start_date=start_date,
    end_date=end_date
)

# Calculate MRR
mrr = await revenue_analytics.calculate_mrr("tenant_123", datetime.now())
```

## API Endpoints

### Payments
- `POST /payments` - Create payment
- `GET /payments/{id}` - Get payment by ID
- `POST /payments/{id}/process` - Process payment
- `POST /payments/{id}/refund` - Refund payment
- `GET /tenants/{id}/payments` - Get payments by tenant

### Invoices
- `POST /invoices` - Create invoice
- `GET /invoices/{id}` - Get invoice by ID
- `POST /invoices/{id}/send` - Send invoice
- `POST /invoices/{id}/mark-paid` - Mark invoice as paid

### Webhooks
- `POST /webhooks/stripe` - Stripe webhook endpoint

## Configuration

### Environment Variables
- `STRIPE_API_KEY` - Stripe API key
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook secret
- `BILLING_DATABASE_URL` - Database connection string

### Stripe Setup
1. Create Stripe account and get API keys
2. Set up webhook endpoints
3. Configure payment methods
4. Set up products and pricing

## Testing

Run the test suite:

```bash
pytest src/saas/billing/__tests__/
```

## Security

- All webhook signatures are verified
- Payment data is encrypted in transit
- API endpoints require authentication
- Sensitive data is not logged

## Monitoring

- Payment success/failure rates
- Webhook processing latency
- Revenue metrics and trends
- Error rates and alerts

## Dependencies

- `stripe` - Stripe Python SDK
- `aiohttp` - Async HTTP client/server
- `pydantic` - Data validation
- `pytest` - Testing framework
- `pytest-asyncio` - Async testing support
