import React from 'react';
import { View, StyleSheet, ActivityIndicator } from 'react-native';
import { Text } from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { colors, typography, spacing } from '../constants/theme';

export const LoadingScreen = ({ message = 'Loading...' }) => {
  return (
    <LinearGradient
      colors={colors.gradient.primary}
      style={styles.container}
    >
      <View style={styles.content}>
        <View style={styles.logoContainer}>
          <Text style={styles.logo}>📊</Text>
          <Text style={styles.appName}>NeoZork</Text>
          <Text style={styles.appSubtitle}>Pocket Hedge Fund</Text>
        </View>
        
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.white} />
          <Text style={styles.loadingText}>{message}</Text>
        </View>
      </View>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: spacing.xxl,
  },
  logo: {
    fontSize: 80,
    marginBottom: spacing.md,
  },
  appName: {
    ...typography.h1,
    color: colors.white,
    fontWeight: 'bold',
    marginBottom: spacing.xs,
  },
  appSubtitle: {
    ...typography.h5,
    color: colors.white,
    opacity: 0.9,
    textAlign: 'center',
  },
  loadingContainer: {
    alignItems: 'center',
  },
  loadingText: {
    ...typography.body1,
    color: colors.white,
    marginTop: spacing.md,
    textAlign: 'center',
  },
});
