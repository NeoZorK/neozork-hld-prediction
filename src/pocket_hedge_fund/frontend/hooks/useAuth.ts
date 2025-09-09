/**
 * Authentication Hook for Pocket Hedge Fund React Dashboard
 * 
 * This hook provides authentication state management, login/logout functionality,
 * and user session handling throughout the application.
 */

import { useState, useEffect, useCallback, useContext, createContext } from 'react';
import { User, LoginRequest, RegisterRequest, ApiError } from '../types';
import { authAPI } from '../services/api';

// ============================================================================
// AUTHENTICATION CONTEXT
// ============================================================================

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (userData: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// ============================================================================
// AUTHENTICATION PROVIDER
// ============================================================================

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const isAuthenticated = !!user;

  // ============================================================================
  // ERROR HANDLING
  // ============================================================================

  const handleError = useCallback((error: any) => {
    console.error('Auth Error:', error);
    
    if (error instanceof ApiError) {
      setError(error.message);
    } else if (error.message) {
      setError(error.message);
    } else {
      setError('An unexpected error occurred');
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // ============================================================================
  // AUTHENTICATION METHODS
  // ============================================================================

  const login = useCallback(async (credentials: LoginRequest) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await authAPI.login(credentials);
      setUser(response.user);
      
      // Store tokens in localStorage
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      
    } catch (error) {
      handleError(error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [handleError]);

  const register = useCallback(async (userData: RegisterRequest) => {
    try {
      setIsLoading(true);
      setError(null);
      
      await authAPI.register(userData);
      
      // Auto-login after successful registration
      await login({
        email: userData.email,
        password: userData.password
      });
      
    } catch (error) {
      handleError(error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [login, handleError]);

  const logout = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      await authAPI.logout();
      
    } catch (error) {
      // Even if logout fails on server, clear local state
      console.warn('Logout error:', error);
    } finally {
      // Clear local state regardless of server response
      setUser(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setIsLoading(false);
    }
  }, []);

  const refreshToken = useCallback(async () => {
    try {
      const response = await authAPI.refreshToken();
      setUser(response.user);
      
      // Update tokens in localStorage
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      
    } catch (error) {
      // If refresh fails, logout user
      console.error('Token refresh failed:', error);
      await logout();
    }
  }, [logout]);

  // ============================================================================
  // INITIALIZATION
  // ============================================================================

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        setIsLoading(true);
        
        const token = localStorage.getItem('access_token');
        if (!token) {
          setIsLoading(false);
          return;
        }

        // Verify token by fetching current user
        const currentUser = await authAPI.getCurrentUser();
        setUser(currentUser);
        
      } catch (error) {
        // If token is invalid, clear it
        console.error('Auth initialization failed:', error);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // ============================================================================
  // TOKEN REFRESH INTERVAL
  // ============================================================================

  useEffect(() => {
    if (!isAuthenticated) return;

    // Refresh token every 25 minutes (tokens expire in 30 minutes)
    const refreshInterval = setInterval(() => {
      refreshToken();
    }, 25 * 60 * 1000);

    return () => clearInterval(refreshInterval);
  }, [isAuthenticated, refreshToken]);

  // ============================================================================
  // CONTEXT VALUE
  // ============================================================================

  const contextValue: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    refreshToken,
    clearError
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// ============================================================================
// USE AUTH HOOK
// ============================================================================

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

// ============================================================================
// PROTECTED ROUTE HOOK
// ============================================================================

export const useProtectedRoute = () => {
  const { isAuthenticated, isLoading } = useAuth();
  
  return {
    isAuthenticated,
    isLoading,
    shouldRedirect: !isLoading && !isAuthenticated
  };
};

// ============================================================================
// USER PERMISSIONS HOOK
// ============================================================================

export const usePermissions = () => {
  const { user } = useAuth();
  
  const hasRole = useCallback((role: string) => {
    return user?.role === role;
  }, [user]);
  
  const hasAnyRole = useCallback((roles: string[]) => {
    return user && roles.includes(user.role);
  }, [user]);
  
  const isAdmin = useCallback(() => {
    return hasRole('admin');
  }, [hasRole]);
  
  const isManager = useCallback(() => {
    return hasAnyRole(['admin', 'manager']);
  }, [hasAnyRole]);
  
  const isInvestor = useCallback(() => {
    return hasAnyRole(['admin', 'manager', 'investor']);
  }, [hasAnyRole]);
  
  const canManageFunds = useCallback(() => {
    return hasAnyRole(['admin', 'manager']);
  }, [hasAnyRole]);
  
  const canViewFunds = useCallback(() => {
    return hasAnyRole(['admin', 'manager', 'investor', 'viewer']);
  }, [hasAnyRole]);
  
  return {
    user,
    hasRole,
    hasAnyRole,
    isAdmin,
    isManager,
    isInvestor,
    canManageFunds,
    canViewFunds
  };
};

// ============================================================================
// EXPORT
// ============================================================================

export default useAuth;
