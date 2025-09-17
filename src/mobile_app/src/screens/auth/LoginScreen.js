import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import {
  Text,
  TextInput,
  Button,
  Card,
  Divider,
  Checkbox,
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../../services/AuthContext';
import { colors, spacing, borderRadius, typography } from '../../constants/theme';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { login } = useAuth();

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    setIsLoading(true);
    const result = await login(email, password);
    setIsLoading(false);

    if (!result.success) {
      Alert.alert('Login Failed', result.error);
    }
  };

  const handleForgotPassword = () => {
    navigation.navigate('ForgotPassword');
  };

  const handleRegister = () => {
    navigation.navigate('Register');
  };

  return (
    <LinearGradient
      colors={colors.gradient.primary}
      style={styles.container}
    >
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.logo}>📊</Text>
            <Text style={styles.appName}>NeoZork</Text>
            <Text style={styles.appSubtitle}>Pocket Hedge Fund</Text>
            <Text style={styles.welcomeText}>Welcome back!</Text>
          </View>

          {/* Login Form */}
          <Card style={styles.formCard}>
            <Card.Content style={styles.formContent}>
              <Text style={styles.formTitle}>Sign In</Text>
              
              <TextInput
                label="Email"
                value={email}
                onChangeText={setEmail}
                mode="outlined"
                keyboardType="email-address"
                autoCapitalize="none"
                autoComplete="email"
                style={styles.input}
                left={<TextInput.Icon icon="email" />}
              />

              <TextInput
                label="Password"
                value={password}
                onChangeText={setPassword}
                mode="outlined"
                secureTextEntry={!showPassword}
                autoComplete="password"
                style={styles.input}
                left={<TextInput.Icon icon="lock" />}
                right={
                  <TextInput.Icon
                    icon={showPassword ? 'eye-off' : 'eye'}
                    onPress={() => setShowPassword(!showPassword)}
                  />
                }
              />

              <View style={styles.optionsRow}>
                <View style={styles.rememberMe}>
                  <Checkbox
                    status={rememberMe ? 'checked' : 'unchecked'}
                    onPress={() => setRememberMe(!rememberMe)}
                    color={colors.primary}
                  />
                  <Text style={styles.rememberMeText}>Remember me</Text>
                </View>
                
                <Button
                  mode="text"
                  onPress={handleForgotPassword}
                  labelStyle={styles.forgotPasswordText}
                >
                  Forgot Password?
                </Button>
              </View>

              <Button
                mode="contained"
                onPress={handleLogin}
                loading={isLoading}
                disabled={isLoading}
                style={styles.loginButton}
                contentStyle={styles.loginButtonContent}
              >
                Sign In
              </Button>

              <Divider style={styles.divider} />

              <View style={styles.socialLogin}>
                <Text style={styles.socialText}>Or sign in with</Text>
                <View style={styles.socialButtons}>
                  <Button
                    mode="outlined"
                    onPress={() => Alert.alert('Coming Soon', 'Social login will be available soon')}
                    style={styles.socialButton}
                    icon="google"
                  >
                    Google
                  </Button>
                  <Button
                    mode="outlined"
                    onPress={() => Alert.alert('Coming Soon', 'Social login will be available soon')}
                    style={styles.socialButton}
                    icon="apple"
                  >
                    Apple
                  </Button>
                </View>
              </View>
            </Card.Content>
          </Card>

          {/* Register Link */}
          <View style={styles.registerContainer}>
            <Text style={styles.registerText}>Don't have an account? </Text>
            <Button
              mode="text"
              onPress={handleRegister}
              labelStyle={styles.registerButtonText}
            >
              Sign Up
            </Button>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.xl,
  },
  header: {
    alignItems: 'center',
    marginBottom: spacing.xl,
    marginTop: spacing.xxl,
  },
  logo: {
    fontSize: 60,
    marginBottom: spacing.md,
  },
  appName: {
    ...typography.h2,
    color: colors.white,
    fontWeight: 'bold',
    marginBottom: spacing.xs,
  },
  appSubtitle: {
    ...typography.h6,
    color: colors.white,
    opacity: 0.9,
    marginBottom: spacing.lg,
  },
  welcomeText: {
    ...typography.h4,
    color: colors.white,
    textAlign: 'center',
  },
  formCard: {
    borderRadius: borderRadius.xl,
    elevation: 8,
    marginBottom: spacing.lg,
  },
  formContent: {
    padding: spacing.lg,
  },
  formTitle: {
    ...typography.h3,
    textAlign: 'center',
    marginBottom: spacing.lg,
    color: colors.text,
  },
  input: {
    marginBottom: spacing.md,
  },
  optionsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.lg,
  },
  rememberMe: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rememberMeText: {
    ...typography.body2,
    color: colors.textSecondary,
  },
  forgotPasswordText: {
    color: colors.primary,
    fontSize: 14,
  },
  loginButton: {
    marginBottom: spacing.lg,
    borderRadius: borderRadius.lg,
  },
  loginButtonContent: {
    paddingVertical: spacing.sm,
  },
  divider: {
    marginVertical: spacing.lg,
  },
  socialLogin: {
    alignItems: 'center',
  },
  socialText: {
    ...typography.body2,
    color: colors.textSecondary,
    marginBottom: spacing.md,
  },
  socialButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
  },
  socialButton: {
    flex: 1,
    marginHorizontal: spacing.xs,
    borderRadius: borderRadius.lg,
  },
  registerContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  registerText: {
    ...typography.body1,
    color: colors.white,
  },
  registerButtonText: {
    color: colors.white,
    fontWeight: 'bold',
  },
});
