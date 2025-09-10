/**
 * Dashboard Screen for Pocket Hedge Fund Mobile App
 * 
 * This screen displays the main dashboard with statistics,
 * charts, and quick access to key features.
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  RefreshControl,
  TouchableOpacity,
  Dimensions
} from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { Ionicons } from '@expo/vector-icons';

import { selectUser } from '../store/authSlice';
import { DashboardStats, Fund, ChartDataPoint } from '../types';
import { fundAPI, systemAPI } from '../services/api';

// ============================================================================
// TYPES
// ============================================================================

interface DashboardScreenProps {
  navigation: any;
}

// ============================================================================
// COMPONENTS
// ============================================================================

const StatCard = ({ 
  title, 
  value, 
  change, 
  icon, 
  color = '#3B82F6' 
}: {
  title: string;
  value: string;
  change?: number;
  icon: string;
  color?: string;
}) => (
  <View style={[styles.statCard, { borderLeftColor: color }]}>
    <View style={styles.statHeader}>
      <Text style={styles.statTitle}>{title}</Text>
      <Ionicons name={icon as any} size={24} color={color} />
    </View>
    <Text style={styles.statValue}>{value}</Text>
    {change !== undefined && (
      <Text style={[
        styles.statChange,
        { color: change >= 0 ? '#10B981' : '#EF4444' }
      ]}>
        {change >= 0 ? '+' : ''}{change.toFixed(2)}%
      </Text>
    )}
  </View>
);

const FundCard = ({ 
  fund, 
  onPress 
}: { 
  fund: Fund; 
  onPress: (fund: Fund) => void;
}) => {
  const returnPercentage = ((fund.current_value - fund.initial_capital) / fund.initial_capital) * 100;
  
  return (
    <TouchableOpacity 
      style={styles.fundCard} 
      onPress={() => onPress(fund)}
      activeOpacity={0.7}
    >
      <View style={styles.fundHeader}>
        <Text style={styles.fundName} numberOfLines={1}>
          {fund.name}
        </Text>
        <View style={[
          styles.fundTypeBadge,
          { backgroundColor: fund.fund_type === 'premium' ? '#F59E0B' : 
                           fund.fund_type === 'standard' ? '#3B82F6' : '#10B981' }
        ]}>
          <Text style={styles.fundTypeText}>
            {fund.fund_type.toUpperCase()}
          </Text>
        </View>
      </View>
      
      <Text style={styles.fundDescription} numberOfLines={2}>
        {fund.description}
      </Text>
      
      <View style={styles.fundStats}>
        <View style={styles.fundStat}>
          <Text style={styles.fundStatLabel}>Value</Text>
          <Text style={styles.fundStatValue}>
            ${fund.current_value.toLocaleString()}
          </Text>
        </View>
        <View style={styles.fundStat}>
          <Text style={styles.fundStatLabel}>Return</Text>
          <Text style={[
            styles.fundStatValue,
            { color: returnPercentage >= 0 ? '#10B981' : '#EF4444' }
          ]}>
            {returnPercentage >= 0 ? '+' : ''}{returnPercentage.toFixed(1)}%
          </Text>
        </View>
        <View style={styles.fundStat}>
          <Text style={styles.fundStatLabel}>Investors</Text>
          <Text style={styles.fundStatValue}>
            {fund.current_investors}
          </Text>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const QuickActionButton = ({ 
  title, 
  icon, 
  onPress, 
  color = '#3B82F6' 
}: {
  title: string;
  icon: string;
  onPress: () => void;
  color?: string;
}) => (
  <TouchableOpacity 
    style={[styles.quickActionButton, { backgroundColor: color }]}
    onPress={onPress}
    activeOpacity={0.8}
  >
    <Ionicons name={icon as any} size={24} color="#ffffff" />
    <Text style={styles.quickActionText}>{title}</Text>
  </TouchableOpacity>
);

// ============================================================================
// MAIN COMPONENT
// ============================================================================

const DashboardScreen: React.FC<DashboardScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch();
  const user = useSelector(selectUser);
  
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentFunds, setRecentFunds] = useState<Fund[]>([]);
  const [topPerformers, setTopPerformers] = useState<Fund[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  // ============================================================================
  // DATA FETCHING
  // ============================================================================

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      
      // Fetch funds data
      const fundsResponse = await fundAPI.getFunds({ page_size: 10 });
      const funds = fundsResponse.items;

      // Calculate statistics
      const totalFunds = funds.length;
      const totalInvestors = funds.reduce((sum, fund) => sum + fund.current_investors, 0);
      const totalAUM = funds.reduce((sum, fund) => sum + fund.current_value, 0);
      
      // Calculate average return
      const totalReturn = funds.reduce((sum, fund) => {
        const returnPercent = ((fund.current_value - fund.initial_capital) / fund.initial_capital) * 100;
        return sum + returnPercent;
      }, 0);
      const avgReturn = funds.length > 0 ? totalReturn / funds.length : 0;

      // Count active strategies
      const activeStrategies = funds.filter(fund => fund.status === 'active').length;

      // Calculate risk score
      const riskScore = funds.reduce((sum, fund) => {
        const riskValue = fund.risk_level === 'low' ? 1 : fund.risk_level === 'medium' ? 2 : 3;
        return sum + riskValue;
      }, 0) / funds.length;

      setStats({
        total_funds: totalFunds,
        total_investors: totalInvestors,
        total_assets_under_management: totalAUM,
        total_return_percentage: avgReturn,
        active_strategies: activeStrategies,
        risk_score: riskScore,
        portfolio_value: totalAUM,
        daily_change: 0,
        daily_change_percentage: avgReturn
      });

      // Set recent funds and top performers
      setRecentFunds(funds.slice(0, 3));
      
      const topPerformers = funds
        .map(fund => ({
          ...fund,
          performance: ((fund.current_value - fund.initial_capital) / fund.initial_capital) * 100
        }))
        .sort((a, b) => b.performance - a.performance)
        .slice(0, 3);
      
      setTopPerformers(topPerformers);

    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchDashboardData();
    setRefreshing(false);
  };

  // ============================================================================
  // EFFECTS
  // ============================================================================

  useEffect(() => {
    fetchDashboardData();
  }, []);

  // ============================================================================
  // HANDLERS
  // ============================================================================

  const handleFundPress = (fund: Fund) => {
    navigation.navigate('FundDetails', { fundId: fund.fund_id });
  };

  const handleQuickAction = (action: string) => {
    switch (action) {
      case 'invest':
        navigation.navigate('Funds');
        break;
      case 'portfolio':
        navigation.navigate('Portfolio');
        break;
      case 'notifications':
        navigation.navigate('Notifications');
        break;
      case 'settings':
        navigation.navigate('Settings');
        break;
    }
  };

  // ============================================================================
  // RENDER HELPERS
  // ============================================================================

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  // ============================================================================
  // RENDER
  // ============================================================================

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Welcome back,</Text>
          <Text style={styles.userName}>
            {user?.first_name || user?.username || 'User'}!
          </Text>
        </View>
        <TouchableOpacity 
          style={styles.notificationButton}
          onPress={() => handleQuickAction('notifications')}
        >
          <Ionicons name="notifications-outline" size={24} color="#6B7280" />
        </TouchableOpacity>
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActions}>
        <QuickActionButton
          title="Invest"
          icon="trending-up"
          onPress={() => handleQuickAction('invest')}
          color="#3B82F6"
        />
        <QuickActionButton
          title="Portfolio"
          icon="pie-chart"
          onPress={() => handleQuickAction('portfolio')}
          color="#10B981"
        />
        <QuickActionButton
          title="Settings"
          icon="settings"
          onPress={() => handleQuickAction('settings')}
          color="#6B7280"
        />
      </View>

      {/* Statistics */}
      {stats && (
        <View style={styles.statsContainer}>
          <Text style={styles.sectionTitle}>Overview</Text>
          <View style={styles.statsGrid}>
            <StatCard
              title="Total Funds"
              value={stats.total_funds.toString()}
              icon="business"
              color="#3B82F6"
            />
            <StatCard
              title="Investors"
              value={stats.total_investors.toString()}
              icon="people"
              color="#10B981"
            />
            <StatCard
              title="AUM"
              value={formatCurrency(stats.total_assets_under_management)}
              icon="cash"
              color="#F59E0B"
            />
            <StatCard
              title="Avg Return"
              value={`${stats.total_return_percentage.toFixed(1)}%`}
              change={stats.total_return_percentage}
              icon="trending-up"
              color="#EF4444"
            />
          </View>
        </View>
      )}

      {/* Recent Funds */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Recent Funds</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Funds')}>
            <Text style={styles.seeAllText}>See All</Text>
          </TouchableOpacity>
        </View>
        {recentFunds.map((fund) => (
          <FundCard
            key={fund.fund_id}
            fund={fund}
            onPress={handleFundPress}
          />
        ))}
      </View>

      {/* Top Performers */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Top Performers</Text>
        </View>
        {topPerformers.map((fund) => (
          <FundCard
            key={fund.fund_id}
            fund={fund}
            onPress={handleFundPress}
          />
        ))}
      </View>
    </ScrollView>
  );
};

// ============================================================================
// STYLES
// ============================================================================

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB'
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 16
  },
  greeting: {
    fontSize: 16,
    color: '#6B7280',
    fontWeight: '500'
  },
  userName: {
    fontSize: 24,
    color: '#111827',
    fontWeight: 'bold',
    marginTop: 4
  },
  notificationButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 20,
    marginBottom: 24
  },
  quickActionButton: {
    width: (width - 80) / 3,
    height: 80,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  quickActionText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '600',
    marginTop: 8
  },
  statsContainer: {
    paddingHorizontal: 20,
    marginBottom: 24
  },
  section: {
    paddingHorizontal: 20,
    marginBottom: 24
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#111827'
  },
  seeAllText: {
    fontSize: 14,
    color: '#3B82F6',
    fontWeight: '600'
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between'
  },
  statCard: {
    width: (width - 60) / 2,
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  statHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8
  },
  statTitle: {
    fontSize: 14,
    color: '#6B7280',
    fontWeight: '500'
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 4
  },
  statChange: {
    fontSize: 12,
    fontWeight: '600'
  },
  fundCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  fundHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8
  },
  fundName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#111827',
    flex: 1,
    marginRight: 8
  },
  fundTypeBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6
  },
  fundTypeText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: '#ffffff'
  },
  fundDescription: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 12,
    lineHeight: 20
  },
  fundStats: {
    flexDirection: 'row',
    justifyContent: 'space-between'
  },
  fundStat: {
    alignItems: 'center'
  },
  fundStatLabel: {
    fontSize: 12,
    color: '#6B7280',
    marginBottom: 4
  },
  fundStatValue: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#111827'
  }
});

export default DashboardScreen;
