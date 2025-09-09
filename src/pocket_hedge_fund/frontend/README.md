# Pocket Hedge Fund - React Frontend

## 🎯 Overview

This is the React frontend application for the Pocket Hedge Fund system - a revolutionary AI-powered hedge fund management platform. The frontend provides a modern, responsive web interface for fund management, investor operations, and portfolio tracking.

## 🚀 Features

### ✅ Implemented Features
- **Authentication System**: JWT-based login with MFA support
- **Dashboard**: Real-time statistics and performance charts
- **Fund Management**: Create, edit, view, and delete funds
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **TypeScript**: Full type safety and IntelliSense support
- **Modern React**: Hooks, Context API, and functional components

### 🚧 Planned Features
- **Portfolio Management**: Real-time portfolio tracking and analysis
- **Investor Management**: Investor onboarding and management
- **Reports & Analytics**: Comprehensive reporting and analytics
- **Real-time Updates**: WebSocket integration for live data
- **Advanced Charts**: Interactive charts with Chart.js or D3.js
- **Mobile App**: React Native mobile application

## 🏗️ Architecture

### Component Structure
```
src/
├── components/          # React components
│   ├── Dashboard.tsx   # Main dashboard view
│   ├── Login.tsx       # Authentication component
│   └── FundManagement.tsx # Fund management interface
├── hooks/              # Custom React hooks
│   ├── useAuth.ts      # Authentication state management
│   └── useDashboard.ts # Dashboard data management
├── services/           # API services
│   └── api.ts          # HTTP client and API endpoints
├── types/              # TypeScript type definitions
│   └── index.ts        # All type definitions
├── utils/              # Utility functions
└── App.tsx             # Main application component
```

### Key Technologies
- **React 18**: Latest React with concurrent features
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Fetch API**: Modern HTTP client
- **Context API**: State management
- **Custom Hooks**: Reusable logic

## 🛠️ Development Setup

### Prerequisites
- Node.js 16+ and npm/yarn
- Pocket Hedge Fund backend running on port 8080

### Installation
```bash
# Navigate to frontend directory
cd src/pocket_hedge_fund/frontend

# Install dependencies
npm install

# Start development server
npm start
```

The application will be available at `http://localhost:3000`

### Environment Variables
Create a `.env` file in the frontend directory:
```bash
REACT_APP_API_URL=http://localhost:8080/api/v1
REACT_APP_ENVIRONMENT=development
```

## 📱 Usage

### Authentication
1. Navigate to the login page
2. Enter your email and password
3. Complete MFA if enabled
4. Access the dashboard

### Fund Management
1. Click "Funds" in the navigation
2. View existing funds in the table
3. Click "Create Fund" to add a new fund
4. Fill in fund details and submit
5. Edit or delete funds as needed

### Dashboard
- View real-time statistics
- Monitor fund performance
- Track recent activity
- Access quick actions

## 🔧 API Integration

### Authentication Endpoints
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user

### Fund Management Endpoints
- `GET /funds/` - List all funds
- `POST /funds/` - Create new fund
- `GET /funds/{id}` - Get fund details
- `PUT /funds/{id}` - Update fund
- `DELETE /funds/{id}` - Delete fund

### Portfolio Endpoints
- `GET /portfolio/{fund_id}/positions` - Get positions
- `POST /portfolio/{fund_id}/positions` - Add position
- `PUT /portfolio/{fund_id}/positions/{symbol}` - Update position

## 🎨 Styling

### Tailwind CSS Configuration
- Custom color palette for brand consistency
- Responsive design utilities
- Custom animations and transitions
- Form styling with @tailwindcss/forms

### Design System
- **Primary Colors**: Blue palette for main actions
- **Secondary Colors**: Gray palette for text and backgrounds
- **Typography**: Inter font family
- **Spacing**: Consistent spacing scale
- **Components**: Reusable component patterns

## 🧪 Testing

### Running Tests
```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Test Structure
- Unit tests for components
- Integration tests for hooks
- API service tests
- E2E tests with Cypress (planned)

## 📦 Building for Production

### Build Process
```bash
# Create production build
npm run build

# Serve production build locally
npx serve -s build
```

### Build Optimization
- Code splitting for better performance
- Tree shaking to remove unused code
- Minification and compression
- Asset optimization

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM node:16-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Environment Configuration
- Development: `http://localhost:8080`
- Staging: `https://api-staging.neozork.com`
- Production: `https://api.neozork.com`

## 🔒 Security

### Authentication Security
- JWT token storage in localStorage
- Automatic token refresh
- Secure logout with token invalidation
- MFA support for enhanced security

### API Security
- HTTPS enforcement in production
- CORS configuration
- Request/response validation
- Error handling without sensitive data exposure

## 📊 Performance

### Optimization Strategies
- Lazy loading for components
- Memoization for expensive calculations
- Virtual scrolling for large lists
- Image optimization and lazy loading

### Monitoring
- Performance metrics tracking
- Error boundary implementation
- User interaction analytics
- API response time monitoring

## 🤝 Contributing

### Development Guidelines
1. Follow TypeScript best practices
2. Use functional components with hooks
3. Implement proper error handling
4. Write comprehensive tests
5. Follow the established code style

### Code Style
- ESLint configuration for consistency
- Prettier for code formatting
- TypeScript strict mode
- Component naming conventions

## 📚 Documentation

### API Documentation
- Complete API reference in `/docs/api/`
- Type definitions in `/types/`
- Service documentation in `/services/`

### Component Documentation
- Storybook integration (planned)
- Component prop documentation
- Usage examples and best practices

## 🐛 Troubleshooting

### Common Issues
1. **API Connection Failed**: Check backend server status
2. **Authentication Errors**: Verify JWT token validity
3. **Build Failures**: Clear node_modules and reinstall
4. **Type Errors**: Run `npm run type-check`

### Debug Mode
Enable debug logging by setting:
```bash
REACT_APP_DEBUG=true
```

## 📞 Support

For technical support or questions:
- Check the documentation in `/docs/`
- Review the API documentation
- Contact the development team
- Submit issues via GitHub

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Status**: 80% Complete - Core features implemented
