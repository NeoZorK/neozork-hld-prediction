/**
 * Main App Component for Pocket Hedge Fund Mobile App
 * 
 * This is the root component that sets up Redux store,
 * navigation, and app-wide providers.
 */

import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

import { store, persistor } from './src/store/store';
import AppNavigator from './src/navigation/AppNavigator';
import LoadingScreen from './src/components/LoadingScreen';

// ============================================================================
// MAIN APP COMPONENT
// ============================================================================

const App: React.FC = () => {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <Provider store={store}>
        <PersistGate loading={<LoadingScreen />} persistor={persistor}>
          <SafeAreaProvider>
            <AppNavigator />
            <StatusBar style="auto" />
          </SafeAreaProvider>
        </PersistGate>
      </Provider>
    </GestureHandlerRootView>
  );
};

export default App;
