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
  Checkbox,
  Divider,
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { useAuth } from '../../services/AuthContext';
import { colors, spacing, borderRadius, typography } from '../../constants/theme';

export default function RegisterScreen({ navigation }) {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [agreeToTerms, setAgreeToTerms] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { register } = useAuth();

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const validateForm = () => {
    const { firstName, lastName, email, username, password, confirmPassword } = formData;

    if (!firstName || !lastName || !email || !username || !password || !confirmPassword) {
      Alert.alert('Error', 'Please fill in all fields');
      return false;
    }

    if (password !== confirmPassword) {
      Alert.alert('Error', 'Passwords do not match');
      return false;
    }

    if (password.length < 8) {
      Alert.alert('Error', 'Password must be at least 8 characters long');
      return false;
    }

    if (!agreeToTerms) {
      Alert.alert('Error', 'Please agree to the terms and conditions');
      return false;
    }

    return true;
  };

  const handleRegister = async () => {
    if (!validateForm()) return;

    setIsLoading(true);
    const result = await register(formData);
    setIsLoading(false);

    if (result.success) {
      Alert.alert(
        'Registration Successful',
        result.message,
        [
          {
            text: 'OK',
            onPress: () => navigation.navigate('Login'),
          },
        ]
      );
    } else {
      Alert.alert('Registration Failed', result.error);
    }
  };

  const handleLogin = () => {
    navigation.navigate('Login');
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
            <Text style={styles.welcomeText}>Create your account</Text>
          </View>

          {/* Registration Form */}
          <Card style={styles.formCard}>
            <Card.Content style={styles.formContent}>
              <Text style={styles.formTitle}>Sign Up</Text>
              
              <View style={styles.nameRow}>
                <TextInput
                  label="First Name"
                  value={formData.firstName}
                  onChangeText={(value) => handleInputChange('firstName', value)}
                  mode="outlined"
                  autoCapitalize="words"
                  style={[styles.input, styles.halfInput]}
                  left={<TextInput.Icon icon="account" />}
                />
                <TextInput
                  label="Last Name"
                  value={formData.lastName}
                  onChangeText={(value) => handleInputChange('lastName', value)}
                  mode="outlined"
                  autoCapitalize="words"
                  style={[styles.input, styles.halfInput]}
                />
              </View>

              <TextInput
                label="Email"
                value={formData.email}
                onChangeText={(value) => handleInputChange('email', value)}
                mode="outlined"
                keyboardType="email-address"
                autoCapitalize="none"
                autoComplete="email"
                style={styles.input}
                left={<TextInput.Icon icon="email" />}
              />

              <TextInput
                label="Username"
                value={formData.username}
                onChangeText={(value) => handleInputChange('username', value)}
                mode="outlined"
                autoCapitalize="none"
                autoComplete="username"
                style={styles.input}
                left={<TextInput.Icon icon="account-circle" />}
              />

              <TextInput
                label="Password"
                value={formData.password}
                onChangeText={(value) => handleInputChange('password', value)}
                mode="outlined"
                secureTextEntry={!showPassword}
                autoComplete="password-new"
                style={styles.input}
                left={<TextInput.Icon icon="lock" />}
                right={
                  <TextInput.Icon
                    icon={showPassword ? 'eye-off' : 'eye'}
                    onPress={() => setShowPassword(!showPassword)}
                  />
                }
              />

              <TextInput
                label="Confirm Password"
                value={formData.confirmPassword}
                onChangeText={(value) => handleInputChange('confirmPassword', value)}
                mode="outlined"
                secureTextEntry={!showConfirmPassword}
                autoComplete="password-new"
                style={styles.input}
                left={<TextInput.Icon icon="lock-check" />}
                right={
                  <TextInput.Icon
                    icon={showConfirmPassword ? 'eye-off' : 'eye'}
                    onPress={() => setShowConfirmPassword(!showConfirmPassword)}
                  />
                }
              />

              <View style={styles.termsContainer}>
                <Checkbox
                  status={agreeToTerms ? 'checked' : 'unchecked'}
                  onPress={() => setAgreeToTerms(!agreeToTerms)}
                  color={colors.primary}
                />
                <Text style={styles.termsText}>
                  I agree to the{' '}
                  <Text style={styles.termsLink}>Terms and Conditions</Text>
                  {' '}and{' '}
                  <Text style={styles.termsLink}>Privacy Policy</Text>
                </Text>
              </View>

              <Button
                mode="contained"
                onPress={handleRegister}
                loading={isLoading}
                disabled={isLoading}
                style={styles.registerButton}
                contentStyle={styles.registerButtonContent}
              >
                Create Account
              </Button>

              <Divider style={styles.divider} />

              <View style={styles.socialLogin}>
                <Text style={styles.socialText}>Or sign up with</Text>
                <View style={styles.socialButtons}>
                  <Button
                    mode="outlined"
                    onPress={() => Alert.alert('Coming Soon', 'Social registration will be available soon')}
                    style={styles.socialButton}
                    icon="google"
                  >
                    Google
                  </Button>
                  <Button
                    mode="outlined"
                    onPress={() => Alert.alert('Coming Soon', 'Social registration will be available soon')}
                    style={styles.socialButton}
                    icon="apple"
                  >
                    Apple
                  </Button>
                </View>
              </View>
            </Card.Content>
          </Card>

          {/* Login Link */}
          <View style={styles.loginContainer}>
            <Text style={styles.loginText}>Already have an account? </Text>
            <Button
              mode="text"
              onPress={handleLogin}
              labelStyle={styles.loginButtonText}
            >
              Sign In
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
    marginTop: spacing.lg,
  },
  logo: {
    fontSize: 50,
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
  nameRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  input: {
    marginBottom: spacing.md,
  },
  halfInput: {
    flex: 1,
    marginHorizontal: spacing.xs,
  },
  termsContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: spacing.lg,
  },
  termsText: {
    ...typography.body2,
    color: colors.textSecondary,
    flex: 1,
    marginLeft: spacing.sm,
  },
  termsLink: {
    color: colors.primary,
    fontWeight: 'bold',
  },
  registerButton: {
    marginBottom: spacing.lg,
    borderRadius: borderRadius.lg,
  },
  registerButtonContent: {
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
  loginContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loginText: {
    ...typography.body1,
    color: colors.white,
  },
  loginButtonText: {
    color: colors.white,
    fontWeight: 'bold',
  },
});
