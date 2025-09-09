/**
 * Loading Screen Component for Pocket Hedge Fund Mobile App
 * 
 * This component displays a loading screen with app branding
 * and animated loading indicator.
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  Dimensions
} from 'react-native';

// ============================================================================
// COMPONENT
// ============================================================================

const LoadingScreen: React.FC = () => {
  return (
    <View style={styles.container}>
      {/* Logo */}
      <View style={styles.logoContainer}>
        <View style={styles.logo}>
          <Text style={styles.logoText}>N</Text>
        </View>
      </View>

      {/* App Name */}
      <Text style={styles.appName}>Pocket Hedge Fund</Text>
      <Text style={styles.appSubtitle}>AI-Powered Investment Platform</Text>

      {/* Loading Indicator */}
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#3B82F6" />
        <Text style={styles.loadingText}>Loading...</Text>
      </View>

      {/* Version Info */}
      <View style={styles.versionContainer}>
        <Text style={styles.versionText}>Version 1.0.0</Text>
      </View>
    </View>
  );
};

// ============================================================================
// STYLES
// ============================================================================

const { width, height } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 24
  },
  logoContainer: {
    marginBottom: 24
  },
  logo: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#3B82F6',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.15,
    shadowRadius: 16,
    elevation: 8
  },
  logoText: {
    fontSize: 40,
    fontWeight: 'bold',
    color: '#ffffff'
  },
  appName: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 8,
    textAlign: 'center'
  },
  appSubtitle: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center',
    marginBottom: 48
  },
  loadingContainer: {
    alignItems: 'center',
    marginBottom: 48
  },
  loadingText: {
    fontSize: 16,
    color: '#6B7280',
    marginTop: 16,
    fontWeight: '500'
  },
  versionContainer: {
    position: 'absolute',
    bottom: 40
  },
  versionText: {
    fontSize: 12,
    color: '#9CA3AF',
    textAlign: 'center'
  }
});

export default LoadingScreen;
