# NeoZork Pocket Hedge Fund Mobile App

A modern, cross-platform mobile application for the NeoZork Pocket Hedge Fund platform, built with React Native and Expo.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure login/registration with biometric support
- **Portfolio Management**: Real-time portfolio tracking and analytics
- **Investment Management**: Create, view, and manage investments
- **Fund Browsing**: Explore available hedge funds with detailed information
- **Performance Analytics**: Comprehensive performance charts and metrics
- **Risk Assessment**: Real-time risk metrics and portfolio analysis

### User Experience
- **Modern UI/UX**: Beautiful, intuitive interface with gradient designs
- **Responsive Design**: Optimized for all screen sizes
- **Dark/Light Themes**: Adaptive theming support
- **Offline Support**: Core functionality works offline
- **Push Notifications**: Real-time alerts and updates
- **Biometric Authentication**: Touch ID/Face ID support

### Security Features
- **Secure Storage**: Encrypted local storage for sensitive data
- **JWT Authentication**: Token-based authentication
- **API Security**: Secure API communication with HTTPS
- **Data Validation**: Client-side and server-side validation
- **Audit Logging**: Comprehensive activity tracking

## 📱 Screenshots

### Authentication
- Login Screen with biometric support
- Registration with form validation
- Forgot Password functionality

### Main App
- Dashboard with portfolio overview
- Portfolio management with charts
- Fund browsing and details
- Investment creation and management
- Analytics with performance metrics
- Profile management and settings

## 🛠 Technology Stack

### Frontend
- **React Native**: Cross-platform mobile development
- **Expo**: Development platform and tools
- **React Navigation**: Navigation library
- **React Native Paper**: Material Design components
- **React Native Chart Kit**: Charts and graphs
- **Expo Linear Gradient**: Gradient backgrounds
- **React Native Vector Icons**: Icon library

### State Management
- **React Context**: Global state management
- **AsyncStorage**: Local data persistence
- **Expo SecureStore**: Secure data storage

### API Integration
- **Axios**: HTTP client for API calls
- **JWT**: Token-based authentication
- **RESTful API**: Backend integration

## 📦 Installation

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Expo CLI
- iOS Simulator (for iOS development)
- Android Studio (for Android development)

### Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mobile_app
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Install Expo CLI globally**
   ```bash
   npm install -g @expo/cli
   ```

4. **Start the development server**
   ```bash
   npm start
   # or
   expo start
   ```

5. **Run on device/simulator**
   - Scan QR code with Expo Go app (iOS/Android)
   - Press `i` for iOS simulator
   - Press `a` for Android emulator

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
API_BASE_URL=http://localhost:8080/api/v1
EXPO_PUBLIC_API_URL=http://localhost:8080/api/v1
```

### App Configuration
Update `app.json` for your specific needs:
- Bundle identifier
- App name and version
- Icons and splash screen
- Permissions

## 📱 Building for Production

### iOS
```bash
expo build:ios
```

### Android
```bash
expo build:android
```

### EAS Build (Recommended)
```bash
npm install -g @expo/eas-cli
eas build --platform ios
eas build --platform android
```

## 🧪 Testing

### Unit Tests
```bash
npm test
```

### E2E Tests
```bash
npm run test:e2e
```

### Manual Testing
- Test on multiple devices
- Test different screen sizes
- Test offline functionality
- Test biometric authentication

## 📊 Performance

### Optimization Features
- **Lazy Loading**: Components loaded on demand
- **Image Optimization**: Optimized images and caching
- **Bundle Splitting**: Code splitting for faster loading
- **Memory Management**: Efficient memory usage
- **Network Optimization**: Request caching and batching

### Metrics
- App startup time: < 3 seconds
- Screen transition: < 300ms
- API response time: < 2 seconds
- Memory usage: < 100MB
- Battery usage: Optimized

## 🔒 Security

### Data Protection
- **Encryption**: All sensitive data encrypted
- **Secure Storage**: Biometric-protected storage
- **Network Security**: HTTPS/TLS encryption
- **Token Management**: Secure JWT handling
- **Input Validation**: Client and server validation

### Privacy
- **Data Minimization**: Only necessary data collected
- **User Consent**: Clear privacy policies
- **Data Retention**: Automatic data cleanup
- **GDPR Compliance**: European privacy standards

## 🚀 Deployment

### App Stores
1. **iOS App Store**
   - Build with EAS Build
   - Submit through App Store Connect
   - Follow Apple guidelines

2. **Google Play Store**
   - Build with EAS Build
   - Submit through Google Play Console
   - Follow Google guidelines

### Over-the-Air Updates
```bash
expo publish
```

## 📈 Analytics

### Tracking
- User engagement metrics
- Feature usage statistics
- Performance monitoring
- Error tracking and reporting
- Crash analytics

### Tools
- Expo Analytics
- Firebase Analytics
- Sentry for error tracking
- Custom analytics dashboard

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

### Code Standards
- ESLint configuration
- Prettier formatting
- TypeScript for type safety
- Comprehensive documentation
- Unit test coverage

## 📚 Documentation

### API Documentation
- RESTful API endpoints
- Authentication flow
- Error handling
- Response formats

### User Guide
- Getting started guide
- Feature explanations
- Troubleshooting
- FAQ section

## 🐛 Troubleshooting

### Common Issues
1. **Metro bundler issues**
   ```bash
   expo start --clear
   ```

2. **iOS simulator issues**
   ```bash
   expo run:ios --clear
   ```

3. **Android emulator issues**
   ```bash
   expo run:android --clear
   ```

4. **Dependency conflicts**
   ```bash
   rm -rf node_modules
   npm install
   ```

### Support
- GitHub Issues
- Expo Documentation
- React Native Documentation
- Community Forums

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Expo team for the amazing development platform
- React Native community for continuous support
- Material Design for UI guidelines
- Chart.js for beautiful charts
- All contributors and testers

---

**NeoZork Pocket Hedge Fund Mobile App** - Bringing hedge fund management to your pocket! 📱💰
