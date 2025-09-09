/**
 * Login Component for Pocket Hedge Fund React Dashboard
 * 
 * This component provides user authentication with email/password
 * and optional MFA support.
 */

import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { LoginRequest } from '../types';

// ============================================================================
// LOGIN FORM INTERFACE
// ============================================================================

interface LoginFormData {
  email: string;
  password: string;
  mfa_code: string;
  remember_me: boolean;
}

// ============================================================================
// LOGIN COMPONENT
// ============================================================================

const Login: React.FC = () => {
  const { login, isLoading, error, clearError } = useAuth();
  const [formData, setFormData] = useState<LoginFormData>({
    email: '',
    password: '',
    mfa_code: '',
    remember_me: false
  });
  const [showMFA, setShowMFA] = useState(false);
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  // ============================================================================
  // FORM VALIDATION
  // ============================================================================

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    // Email validation
    if (!formData.email) {
      errors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Please enter a valid email address';
    }

    // Password validation
    if (!formData.password) {
      errors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      errors.password = 'Password must be at least 8 characters';
    }

    // MFA validation (if required)
    if (showMFA && !formData.mfa_code) {
      errors.mfa_code = 'MFA code is required';
    } else if (showMFA && formData.mfa_code.length !== 6) {
      errors.mfa_code = 'MFA code must be 6 digits';
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // ============================================================================
  // FORM HANDLERS
  // ============================================================================

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));

    // Clear validation error for this field
    if (validationErrors[name]) {
      setValidationErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }

    // Clear general error when user starts typing
    if (error) {
      clearError();
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      const loginRequest: LoginRequest = {
        email: formData.email,
        password: formData.password
      };

      // Add MFA code if provided
      if (showMFA && formData.mfa_code) {
        loginRequest.mfa_code = formData.mfa_code;
      }

      await login(loginRequest);
    } catch (error) {
      // Error is handled by the auth hook
      console.error('Login failed:', error);
    }
  };

  // ============================================================================
  // MFA HANDLING
  // ============================================================================

  const handleMFARequired = () => {
    setShowMFA(true);
    setFormData(prev => ({ ...prev, mfa_code: '' }));
  };

  // ============================================================================
  // EFFECTS
  // ============================================================================

  useEffect(() => {
    // Clear errors when component mounts
    clearError();
  }, [clearError]);

  // ============================================================================
  // RENDER HELPERS
  // ============================================================================

  const getInputClassName = (fieldName: string) => {
    const baseClass = "w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500";
    const errorClass = validationErrors[fieldName] ? "border-red-300 focus:ring-red-500 focus:border-red-500" : "border-gray-300";
    return `${baseClass} ${errorClass}`;
  };

  // ============================================================================
  // RENDER
  // ============================================================================

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        {/* Logo and Title */}
        <div className="text-center">
          <div className="mx-auto h-12 w-12 bg-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white text-xl font-bold">N</span>
          </div>
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Pocket Hedge Fund
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Sign in to your account
          </p>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {/* Error Display */}
          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 rounded-md p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">
                    Authentication Error
                  </h3>
                  <div className="mt-2 text-sm text-red-700">
                    {error}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Login Form */}
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <div className="mt-1">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className={getInputClassName('email')}
                  placeholder="Enter your email"
                  disabled={isLoading}
                />
                {validationErrors.email && (
                  <p className="mt-1 text-sm text-red-600">{validationErrors.email}</p>
                )}
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <div className="mt-1">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  value={formData.password}
                  onChange={handleInputChange}
                  className={getInputClassName('password')}
                  placeholder="Enter your password"
                  disabled={isLoading}
                />
                {validationErrors.password && (
                  <p className="mt-1 text-sm text-red-600">{validationErrors.password}</p>
                )}
              </div>
            </div>

            {/* MFA Field (conditional) */}
            {showMFA && (
              <div>
                <label htmlFor="mfa_code" className="block text-sm font-medium text-gray-700">
                  Multi-Factor Authentication Code
                </label>
                <div className="mt-1">
                  <input
                    id="mfa_code"
                    name="mfa_code"
                    type="text"
                    maxLength={6}
                    value={formData.mfa_code}
                    onChange={handleInputChange}
                    className={getInputClassName('mfa_code')}
                    placeholder="Enter 6-digit code"
                    disabled={isLoading}
                  />
                  {validationErrors.mfa_code && (
                    <p className="mt-1 text-sm text-red-600">{validationErrors.mfa_code}</p>
                  )}
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  Enter the 6-digit code from your authenticator app
                </p>
              </div>
            )}

            {/* Remember Me */}
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember_me"
                  name="remember_me"
                  type="checkbox"
                  checked={formData.remember_me}
                  onChange={handleInputChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  disabled={isLoading}
                />
                <label htmlFor="remember_me" className="ml-2 block text-sm text-gray-900">
                  Remember me
                </label>
              </div>

              <div className="text-sm">
                <a href="#" className="font-medium text-blue-600 hover:text-blue-500">
                  Forgot your password?
                </a>
              </div>
            </div>

            {/* Submit Button */}
            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Signing in...
                  </div>
                ) : (
                  'Sign in'
                )}
              </button>
            </div>
          </form>

          {/* Additional Links */}
          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">New to Pocket Hedge Fund?</span>
              </div>
            </div>

            <div className="mt-6">
              <a
                href="/register"
                className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Create an account
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
