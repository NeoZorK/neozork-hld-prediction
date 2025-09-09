/**
 * Main App Component for Pocket Hedge Fund React Dashboard
 * 
 * This component serves as the root of the React application,
 * providing routing, authentication, and layout management.
 */

import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth, useProtectedRoute } from './hooks/useAuth';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import FundManagement from './components/FundManagement';

// ============================================================================
// LOADING COMPONENT
// ============================================================================

const LoadingScreen: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading Pocket Hedge Fund...</p>
      </div>
    </div>
  );
};

// ============================================================================
// NAVIGATION COMPONENT
// ============================================================================

interface NavigationProps {
  currentPage: string;
  onPageChange: (page: string) => void;
}

const Navigation: React.FC<NavigationProps> = ({ currentPage, onPageChange }) => {
  const { user, logout } = useAuth();

  const navigationItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'funds', label: 'Funds', icon: '🏦' },
    { id: 'portfolio', label: 'Portfolio', icon: '📈' },
    { id: 'investors', label: 'Investors', icon: '👥' },
    { id: 'reports', label: 'Reports', icon: '📋' }
  ];

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and Navigation */}
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <div className="h-8 w-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-bold">N</span>
              </div>
              <span className="ml-2 text-xl font-bold text-gray-900">
                Pocket Hedge Fund
              </span>
            </div>
            
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {navigationItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => onPageChange(item.id)}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    currentPage === item.id
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                  }`}
                >
                  <span className="mr-2">{item.icon}</span>
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 bg-gray-300 rounded-full flex items-center justify-center">
                <span className="text-gray-600 text-sm font-medium">
                  {user?.first_name?.charAt(0) || user?.username?.charAt(0) || 'U'}
                </span>
              </div>
              <div className="hidden md:block">
                <p className="text-sm font-medium text-gray-900">
                  {user?.first_name || user?.username}
                </p>
                <p className="text-xs text-gray-500 capitalize">
                  {user?.role}
                </p>
              </div>
            </div>
            
            <button
              onClick={handleLogout}
              className="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

// ============================================================================
// MAIN CONTENT COMPONENT
// ============================================================================

interface MainContentProps {
  currentPage: string;
}

const MainContent: React.FC<MainContentProps> = ({ currentPage }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    return <Login />;
  }

  switch (currentPage) {
    case 'dashboard':
      return <Dashboard />;
    case 'funds':
      return <FundManagement />;
    case 'portfolio':
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <div className="text-gray-400 text-6xl mb-4">📈</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Portfolio Management</h2>
            <p className="text-gray-600">Coming soon...</p>
          </div>
        </div>
      );
    case 'investors':
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <div className="text-gray-400 text-6xl mb-4">👥</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Investor Management</h2>
            <p className="text-gray-600">Coming soon...</p>
          </div>
        </div>
      );
    case 'reports':
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <div className="text-gray-400 text-6xl mb-4">📋</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Reports & Analytics</h2>
            <p className="text-gray-600">Coming soon...</p>
          </div>
        </div>
      );
    default:
      return <Dashboard />;
  }
};

// ============================================================================
// MAIN APP COMPONENT
// ============================================================================

const AppContent: React.FC = () => {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const { isAuthenticated } = useAuth();

  // ============================================================================
  // PAGE ROUTING
  // ============================================================================

  useEffect(() => {
    // Handle browser back/forward navigation
    const handlePopState = () => {
      const path = window.location.pathname.substring(1) || 'dashboard';
      setCurrentPage(path);
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const handlePageChange = (page: string) => {
    setCurrentPage(page);
    // Update URL without page reload
    window.history.pushState({}, '', `/${page}`);
  };

  // ============================================================================
  // RENDER
  // ============================================================================

  return (
    <div className="min-h-screen bg-gray-50">
      {isAuthenticated && (
        <Navigation currentPage={currentPage} onPageChange={handlePageChange} />
      )}
      <MainContent currentPage={currentPage} />
    </div>
  );
};

// ============================================================================
// ROOT APP COMPONENT WITH PROVIDERS
// ============================================================================

const App: React.FC = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default App;
