/**
 * Login Screen for Pocket Hedge Fund Mobile App
 * 
 * This screen handles user authentication with email/password
 * and optional biometric authentication.
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  ActivityIndicator
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { Ionicons } from '@expo/vector-icons';
import * as LocalAuthentication from 'expo-local-authentication';

import { loginUser, selectAuthLoading, selectAuthError, clearError } from '../store/authSlice';
import { LoginRequest } from '../types';

// ============================================================================
// TYPES
// ============================================================================

interface LoginScreenProps {
  navigation: any;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

const LoginScreen: React.FC<LoginScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch();
  const isLoading = useSelector(selectAuthLoading);
  const error = useSelector(selectAuthError);

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    mfa_code: '',
    remember_me: false
  });
  const [showMFA, setShowMFA] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [biometricAvailable, setBiometricAvailable] = useState(false);
  const [biometricEnabled, setBiometricEnabled] = useState(false);

  // ============================================================================
  // EFFECTS
  // ============================================================================

  useEffect(() => {
    checkBiometricAvailability();
    checkBiometricEnabled();
  }, []);

  useEffect(() => {
    if (error) {
      Alert.alert('Login Error', error);
      dispatch(clearError());
    }
  }, [error, dispatch]);

  // ============================================================================
  // BIOMETRIC AUTHENTICATION
  // ============================================================================

  const checkBiometricAvailability = async () => {
    try {
      const hasHardware = await LocalAuthentication.hasHardwareAsync();
      const isEnrolled = await LocalAuthentication.isEnrolledAsync();
      setBiometricAvailable(hasHardware && isEnrolled);
    } catch (error) {
      console.error('Biometric check failed:', error);
    }
  };

  const checkBiometricEnabled = async () => {
    try {
      // Check if biometric is enabled in user preferences
      // This would typically be stored in AsyncStorage
      setBiometricEnabled(false); // Placeholder
    } catch (error) {
      console.error('Biometric enabled check failed:', error);
    }
  };

  const handleBiometricLogin = async () => {
    try {
      const result = await LocalAuthentication.authenticateAsync({
        promptMessage: 'Authenticate to access Pocket Hedge Fund',
        fallbackLabel: 'Use Passcode',
        cancelLabel: 'Cancel'
      });

      if (result.success) {
        // Use stored credentials for biometric login
        // This would typically retrieve stored credentials
        Alert.alert('Biometric Login', 'Biometric authentication successful!');
      }
    } catch (error) {
      console.error('Biometric authentication failed:', error);
      Alert.alert('Biometric Error', 'Biometric authentication failed');
    }
  };

  // ============================================================================
  // FORM HANDLING
  // ============================================================================

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const validateForm = (): boolean => {
    if (!formData.email.trim()) {
      Alert.alert('Validation Error', 'Email is required');
      return false;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      Alert.alert('Validation Error', 'Please enter a valid email address');
      return false;
    }

    if (!formData.password) {
      Alert.alert('Validation Error', 'Password is required');
      return false;
    }

    if (formData.password.length < 8) {
      Alert.alert('Validation Error', 'Password must be at least 8 characters');
      return false;
    }

    if (showMFA && formData.mfa_code.length !== 6) {
      Alert.alert('Validation Error', 'MFA code must be 6 digits');
      return false;
    }

    return true;
  };

  const handleLogin = async () => {
    if (!validateForm()) return;

    try {
      const loginRequest: LoginRequest = {
        email: formData.email,
        password: formData.password,
        mfa_code: showMFA ? formData.mfa_code : undefined
      };

      await dispatch(loginUser(loginRequest)).unwrap();
    } catch (error) {
      // Error is handled by the Redux slice
      console.error('Login failed:', error);
    }
  };

  const handleRegister = () => {
    navigation.navigate('Register');
  };

  const handleForgotPassword = () => {
    Alert.alert(
      'Forgot Password',
      'Password reset functionality will be available soon.',
      [{ text: 'OK' }]
    );
  };

  // ============================================================================
  // RENDER
  // ============================================================================

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView 
        contentContainerStyle={styles.scrollContainer}
        keyboardShouldPersistTaps="handled"
      >
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.logoContainer}>
            <View style={styles.logo}>
              <Text style={styles.logoText}>N</Text>
            </View>
          </View>
          <Text style={styles.title}>Pocket Hedge Fund</Text>
          <Text style={styles.subtitle}>Sign in to your account</Text>
        </View>

        {/* Form */}
        <View style={styles.form}>
          {/* Email Input */}
          <View style={styles.inputContainer}>
            <Text style={styles.label}>Email Address</Text>
            <View style={styles.inputWrapper}>
              <Ionicons name="mail-outline" size={20} color="#6B7280" style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                placeholder="Enter your email"
                placeholderTextColor="#9CA3AF"
                value={formData.email}
                onChangeText={(value) => handleInputChange('email', value)}
                keyboardType="email-address"
                autoCapitalize="none"
                autoCorrect={false}
                editable={!isLoading}
              />
            </View>
          </View>

          {/* Password Input */}
          <View style={styles.inputContainer}>
            <Text style={styles.label}>Password</Text>
            <View style={styles.inputWrapper}>
              <Ionicons name="lock-closed-outline" size={20} color="#6B7280" style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                placeholder="Enter your password"
                placeholderTextColor="#9CA3AF"
                value={formData.password}
                onChangeText={(value) => handleInputChange('password', value)}
                secureTextEntry={!showPassword}
                autoCapitalize="none"
                autoCorrect={false}
                editable={!isLoading}
              />
              <TouchableOpacity
                onPress={() => setShowPassword(!showPassword)}
                style={styles.eyeButton}
              >
                <Ionicons 
                  name={showPassword ? "eye-off-outline" : "eye-outline"} 
                  size={20} 
                  color="#6B7280" 
                />
              </TouchableOpacity>
            </View>
          </View>

          {/* MFA Input (conditional) */}
          {showMFA && (
            <View style={styles.inputContainer}>
              <Text style={styles.label}>Multi-Factor Authentication Code</Text>
              <View style={styles.inputWrapper}>
                <Ionicons name="shield-checkmark-outline" size={20} color="#6B7280" style={styles.inputIcon} />
                <TextInput
                  style={styles.input}
                  placeholder="Enter 6-digit code"
                  placeholderTextColor="#9CA3AF"
                  value={formData.mfa_code}
                  onChangeText={(value) => handleInputChange('mfa_code', value)}
                  keyboardType="numeric"
                  maxLength={6}
                  editable={!isLoading}
                />
              </View>
            </View>
          )}

          {/* Remember Me */}
          <View style={styles.rememberContainer}>
            <TouchableOpacity
              style={styles.checkboxContainer}
              onPress={() => handleInputChange('remember_me', !formData.remember_me)}
              disabled={isLoading}
            >
              <View style={[
                styles.checkbox,
                formData.remember_me && styles.checkboxChecked
              ]}>
                {formData.remember_me && (
                  <Ionicons name="checkmark" size={16} color="#ffffff" />
                )}
              </View>
              <Text style={styles.checkboxLabel}>Remember me</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={handleForgotPassword} disabled={isLoading}>
              <Text style={styles.forgotPassword}>Forgot Password?</Text>
            </TouchableOpacity>
          </View>

          {/* Login Button */}
          <TouchableOpacity
            style={[styles.loginButton, isLoading && styles.loginButtonDisabled]}
            onPress={handleLogin}
            disabled={isLoading}
          >
            {isLoading ? (
              <ActivityIndicator color="#ffffff" size="small" />
            ) : (
              <Text style={styles.loginButtonText}>Sign In</Text>
            )}
          </TouchableOpacity>

          {/* Biometric Login */}
          {biometricAvailable && biometricEnabled && (
            <TouchableOpacity
              style={styles.biometricButton}
              onPress={handleBiometricLogin}
              disabled={isLoading}
            >
              <Ionicons name="finger-print" size={24} color="#3B82F6" />
              <Text style={styles.biometricButtonText}>Use Biometric</Text>
            </TouchableOpacity>
          )}

          {/* Register Link */}
          <View style={styles.registerContainer}>
            <Text style={styles.registerText}>Don't have an account? </Text>
            <TouchableOpacity onPress={handleRegister} disabled={isLoading}>
              <Text style={styles.registerLink}>Sign Up</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

// ============================================================================
// STYLES
// ============================================================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB'
  },
  scrollContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
    paddingVertical: 40
  },
  header: {
    alignItems: 'center',
    marginBottom: 40
  },
  logoContainer: {
    marginBottom: 16
  },
  logo: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#3B82F6',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5
  },
  logoText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#ffffff'
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 8
  },
  subtitle: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center'
  },
  form: {
    width: '100%'
  },
  inputContainer: {
    marginBottom: 20
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 8
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#D1D5DB',
    paddingHorizontal: 16,
    height: 56
  },
  inputIcon: {
    marginRight: 12
  },
  input: {
    flex: 1,
    fontSize: 16,
    color: '#111827'
  },
  eyeButton: {
    padding: 4
  },
  rememberContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center'
  },
  checkbox: {
    width: 20,
    height: 20,
    borderRadius: 4,
    borderWidth: 2,
    borderColor: '#D1D5DB',
    marginRight: 8,
    justifyContent: 'center',
    alignItems: 'center'
  },
  checkboxChecked: {
    backgroundColor: '#3B82F6',
    borderColor: '#3B82F6'
  },
  checkboxLabel: {
    fontSize: 14,
    color: '#374151'
  },
  forgotPassword: {
    fontSize: 14,
    color: '#3B82F6',
    fontWeight: '600'
  },
  loginButton: {
    backgroundColor: '#3B82F6',
    borderRadius: 12,
    height: 56,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  loginButtonDisabled: {
    backgroundColor: '#9CA3AF'
  },
  loginButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff'
  },
  biometricButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ffffff',
    borderRadius: 12,
    height: 56,
    borderWidth: 1,
    borderColor: '#3B82F6',
    marginBottom: 24
  },
  biometricButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#3B82F6',
    marginLeft: 8
  },
  registerContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center'
  },
  registerText: {
    fontSize: 14,
    color: '#6B7280'
  },
  registerLink: {
    fontSize: 14,
    color: '#3B82F6',
    fontWeight: '600'
  }
});

export default LoginScreen;
