/**
 * Main Navigation Component for Pocket Hedge Fund Mobile App
 * 
 * This component handles the main navigation structure,
 * authentication flow, and tab navigation.
 */

import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { useSelector, useDispatch } from 'react-redux';
import { Ionicons } from '@expo/vector-icons';

import { RootStackParamList, TabParamList } from '../types';
import { selectIsAuthenticated, selectAuthLoading } from '../store/authSlice';
import { getCurrentUser } from '../store/authSlice';

// Import screens
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import DashboardScreen from '../screens/DashboardScreen';
import FundListScreen from '../screens/FundListScreen';
import FundDetailsScreen from '../screens/FundDetailsScreen';
import PortfolioScreen from '../screens/PortfolioScreen';
import ProfileScreen from '../screens/ProfileScreen';
import SettingsScreen from '../screens/SettingsScreen';
import NotificationsScreen from '../screens/NotificationsScreen';

// ============================================================================
// NAVIGATION STACKS
// ============================================================================

const Stack = createStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<TabParamList>();

// ============================================================================
// AUTH STACK
// ============================================================================

const AuthStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerShown: false,
      cardStyle: { backgroundColor: '#ffffff' }
    }}
  >
    <Stack.Screen name="Login" component={LoginScreen} />
    <Stack.Screen name="Register" component={RegisterScreen} />
  </Stack.Navigator>
);

// ============================================================================
// MAIN TAB NAVIGATOR
// ============================================================================

const MainTabNavigator = () => (
  <Tab.Navigator
    screenOptions={({ route }) => ({
      tabBarIcon: ({ focused, color, size }) => {
        let iconName: keyof typeof Ionicons.glyphMap;

        switch (route.name) {
          case 'Dashboard':
            iconName = focused ? 'home' : 'home-outline';
            break;
          case 'Funds':
            iconName = focused ? 'trending-up' : 'trending-up-outline';
            break;
          case 'Portfolio':
            iconName = focused ? 'pie-chart' : 'pie-chart-outline';
            break;
          case 'Profile':
            iconName = focused ? 'person' : 'person-outline';
            break;
          default:
            iconName = 'circle';
        }

        return <Ionicons name={iconName} size={size} color={color} />;
      },
      tabBarActiveTintColor: '#3B82F6',
      tabBarInactiveTintColor: '#6B7280',
      tabBarStyle: {
        backgroundColor: '#ffffff',
        borderTopColor: '#E5E7EB',
        borderTopWidth: 1,
        paddingBottom: 5,
        paddingTop: 5,
        height: 60
      },
      tabBarLabelStyle: {
        fontSize: 12,
        fontWeight: '500'
      },
      headerShown: false
    })}
  >
    <Tab.Screen 
      name="Dashboard" 
      component={DashboardScreen}
      options={{
        tabBarLabel: 'Dashboard'
      }}
    />
    <Tab.Screen 
      name="Funds" 
      component={FundListScreen}
      options={{
        tabBarLabel: 'Funds'
      }}
    />
    <Tab.Screen 
      name="Portfolio" 
      component={PortfolioScreen}
      options={{
        tabBarLabel: 'Portfolio'
      }}
    />
    <Tab.Screen 
      name="Profile" 
      component={ProfileScreen}
      options={{
        tabBarLabel: 'Profile'
      }}
    />
  </Tab.Navigator>
);

// ============================================================================
// MAIN STACK NAVIGATOR
// ============================================================================

const MainStackNavigator = () => (
  <Stack.Navigator
    screenOptions={{
      headerShown: false,
      cardStyle: { backgroundColor: '#F9FAFB' }
    }}
  >
    <Stack.Screen name="MainTabs" component={MainTabNavigator} />
    <Stack.Screen 
      name="FundDetails" 
      component={FundDetailsScreen}
      options={{
        headerShown: true,
        title: 'Fund Details',
        headerStyle: {
          backgroundColor: '#3B82F6'
        },
        headerTintColor: '#ffffff',
        headerTitleStyle: {
          fontWeight: 'bold'
        }
      }}
    />
    <Stack.Screen 
      name="Settings" 
      component={SettingsScreen}
      options={{
        headerShown: true,
        title: 'Settings',
        headerStyle: {
          backgroundColor: '#3B82F6'
        },
        headerTintColor: '#ffffff',
        headerTitleStyle: {
          fontWeight: 'bold'
        }
      }}
    />
    <Stack.Screen 
      name="Notifications" 
      component={NotificationsScreen}
      options={{
        headerShown: true,
        title: 'Notifications',
        headerStyle: {
          backgroundColor: '#3B82F6'
        },
        headerTintColor: '#ffffff',
        headerTitleStyle: {
          fontWeight: 'bold'
        }
      }}
    />
  </Stack.Navigator>
);

// ============================================================================
// LOADING SCREEN
// ============================================================================

const LoadingScreen = () => (
  <div style={{
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F9FAFB'
  }}>
    <div style={{
      width: 50,
      height: 50,
      border: '4px solid #E5E7EB',
      borderTop: '4px solid #3B82F6',
      borderRadius: '50%',
      animation: 'spin 1s linear infinite'
    }} />
    <div style={{
      marginTop: 16,
      fontSize: 16,
      color: '#6B7280',
      fontWeight: '500'
    }}>
      Loading Pocket Hedge Fund...
    </div>
  </div>
);

// ============================================================================
// MAIN APP NAVIGATOR
// ============================================================================

const AppNavigator = () => {
  const dispatch = useDispatch();
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const isLoading = useSelector(selectAuthLoading);

  // ============================================================================
  // INITIALIZATION
  // ============================================================================

  useEffect(() => {
    // Check if user is already authenticated
    if (!isAuthenticated) {
      dispatch(getCurrentUser());
    }
  }, [dispatch, isAuthenticated]);

  // ============================================================================
  // RENDER LOGIC
  // ============================================================================

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <NavigationContainer>
      {isAuthenticated ? <MainStackNavigator /> : <AuthStack />}
    </NavigationContainer>
  );
};

// ============================================================================
// EXPORTS
// ============================================================================

export default AppNavigator;
export { AuthStack, MainTabNavigator, MainStackNavigator };
