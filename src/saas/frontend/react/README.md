# 🚀 NeoZork SaaS Frontend React Components

## 📋 Overview

This package contains React components and services for the NeoZork SaaS platform frontend. It provides a comprehensive set of reusable components for building dashboards, analytics, and administrative interfaces.

## 🏗️ Architecture

### Components
- **Dashboard Components**: Main dashboard, stats grid, usage charts, recent activity
- **UI Components**: Reusable UI elements like cards, buttons, forms
- **Service Components**: API clients, WebSocket hooks, data services

### Services
- **Dashboard Service**: API calls for dashboard data
- **Chart Service**: Chart data generation and API calls
- **API Client**: HTTP client with authentication and error handling

### Hooks
- **WebSocket Hooks**: Real-time data updates
- **Custom Hooks**: Reusable logic for components

## 🚀 Quick Start

### Installation

```bash
npm install @neozork/saas-frontend-react
```

### Basic Usage

```tsx
import React from 'react';
import { Dashboard, Button, Card } from '@neozork/saas-frontend-react';

function App() {
  return (
    <div>
      <Dashboard 
        tenant={tenant} 
        user={user} 
        onRefresh={() => console.log('Refreshed')} 
      />
      <Card>
        <Card.Header>
          <Card.Title>Welcome</Card.Title>
        </Card.Header>
        <Card.Content>
          <p>Welcome to NeoZork SaaS Platform</p>
        </Card.Content>
      </Card>
    </div>
  );
}
```

## 📚 Components

### Dashboard Components

#### Dashboard
Main dashboard component with statistics, charts, and real-time updates.

```tsx
<Dashboard 
  tenant={tenant} 
  user={user} 
  onRefresh={handleRefresh} 
/>
```

#### StatsGrid
Displays key statistics in a grid layout.

```tsx
<StatsGrid 
  stats={dashboardStats} 
  onError={handleError} 
/>
```

#### UsageChart
Interactive charts for usage analytics.

```tsx
<UsageChart 
  data={usageStats} 
  onError={handleError} 
/>
```

### UI Components

#### Card
Flexible card component with header, content, and footer.

```tsx
<Card variant="elevated" padding="large">
  <CardHeader>
    <CardTitle level={2}>Card Title</CardTitle>
  </CardHeader>
  <CardContent>
    <p>Card content goes here</p>
  </CardContent>
  <CardFooter>
    <Button variant="primary">Action</Button>
  </CardFooter>
</Card>
```

#### Button
Versatile button component with multiple variants and states.

```tsx
<Button 
  variant="primary" 
  size="large" 
  loading={isLoading}
  onClick={handleClick}
>
  Click me
</Button>
```

## 🔧 Services

### Dashboard Service

```tsx
import { dashboardService } from '@neozork/saas-frontend-react';

// Get dashboard statistics
const stats = await dashboardService.getStats('tenant-id');

// Get usage analytics
const analytics = await dashboardService.getUsageAnalytics('tenant-id', {
  date_from: '2023-01-01',
  date_to: '2023-01-31',
  period: 'month'
});
```

### Chart Service

```tsx
import { chartService } from '@neozork/saas-frontend-react';

// Get usage chart data
const chartData = await chartService.getUsageData({
  type: 'line',
  period: '30d',
  dataKey: 'api_calls',
  tenant_id: 'tenant-id'
});
```

### API Client

```tsx
import { apiClient } from '@neozork/saas-frontend-react';

// Set authentication token
apiClient.setAuthToken('your-token');

// Make API calls
const response = await apiClient.get('/api/endpoint');
const data = await apiClient.post('/api/endpoint', { data: 'value' });
```

## 🔌 Hooks

### WebSocket Hooks

```tsx
import { useDashboardWebSocket } from '@neozork/saas-frontend-react';

function Dashboard() {
  const { isConnected, dashboardUpdates } = useDashboardWebSocket('tenant-id');
  
  return (
    <div>
      <p>Status: {isConnected ? 'Connected' : 'Disconnected'}</p>
      {dashboardUpdates && (
        <p>Last update: {dashboardUpdates.timestamp}</p>
      )}
    </div>
  );
}
```

## 🎨 Styling

Components come with built-in CSS styles. You can customize them by:

1. **CSS Variables**: Override CSS custom properties
2. **CSS Classes**: Use your own CSS classes
3. **CSS Modules**: Import and modify the provided CSS files

### Example Customization

```css
/* Override button styles */
.btn--primary {
  background-color: #your-color;
  border-color: #your-color;
}

/* Override card styles */
.card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Writing Tests

```tsx
import { render, screen } from '@testing-library/react';
import { Dashboard } from '@neozork/saas-frontend-react';

test('renders dashboard', () => {
  render(<Dashboard />);
  expect(screen.getByText('Dashboard')).toBeInTheDocument();
});
```

## 📦 Building

### Development Build

```bash
npm run dev
```

### Production Build

```bash
npm run build
```

### Type Checking

```bash
npm run type-check
```

### Linting

```bash
npm run lint
npm run lint:fix
```

## 🔧 Configuration

### TypeScript

The package includes TypeScript definitions. Configure your `tsconfig.json`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@neozork/saas-frontend-react": ["./node_modules/@neozork/saas-frontend-react"]
    }
  }
}
```

### Environment Variables

Set the following environment variables:

```bash
REACT_APP_API_BASE_URL=https://api.neozork.com
REACT_APP_WS_BASE_URL=wss://ws.neozork.com
```

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

- **1.0.0** - Initial release with dashboard and UI components
