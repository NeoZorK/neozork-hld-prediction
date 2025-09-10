import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  RefreshControl,
  Dimensions,
} from 'react-native';
import {
  Text,
  Card,
  Button,
  Surface,
  ProgressBar,
  Chip,
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { LineChart, PieChart } from 'react-native-chart-kit';
import { useAuth } from '../../services/AuthContext';
import { apiService } from '../../services/ApiService';
import { colors, spacing, borderRadius, typography, shadows } from '../../constants/theme';

const { width } = Dimensions.get('window');

export default function DashboardScreen({ navigation }) {
  const { user } = useAuth();
  const [dashboardData, setDashboardData] = useState(null);
  const [portfolioData, setPortfolioData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      const [portfolioResponse, returnsResponse] = await Promise.all([
        apiService.getPortfolioSummary(),
        apiService.getPortfolioReturns(),
      ]);

      if (portfolioResponse.success) {
        setPortfolioData(portfolioResponse.data);
      }

      if (returnsResponse.success) {
        setDashboardData(returnsResponse.data);
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const formatPercentage = (value) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  const getPerformanceColor = (value) => {
    if (value > 0) return colors.success;
    if (value < 0) return colors.error;
    return colors.textSecondary;
  };

  const chartConfig = {
    backgroundColor: colors.primary,
    backgroundGradientFrom: colors.primary,
    backgroundGradientTo: colors.secondary,
    decimalPlaces: 2,
    color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    style: {
      borderRadius: borderRadius.lg,
    },
    propsForDots: {
      r: '6',
      strokeWidth: '2',
      stroke: colors.white,
    },
  };

  const pieData = portfolioData?.fund_allocations?.map((fund, index) => ({
    name: fund.fund_name,
    population: fund.percentage,
    color: colors.gradient.primary[index % colors.gradient.primary.length],
    legendFontColor: colors.text,
    legendFontSize: 12,
  })) || [];

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading dashboard...</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Welcome Header */}
      <LinearGradient
        colors={colors.gradient.primary}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <View>
            <Text style={styles.welcomeText}>Welcome back,</Text>
            <Text style={styles.userName}>{user?.first_name || 'Investor'}</Text>
          </View>
          <Button
            mode="contained"
            onPress={() => navigation.navigate('CreateInvestment')}
            style={styles.investButton}
            contentStyle={styles.investButtonContent}
          >
            <Ionicons name="add" size={20} color={colors.white} />
            <Text style={styles.investButtonText}>Invest</Text>
          </Button>
        </View>
      </LinearGradient>

      {/* Portfolio Overview */}
      <Card style={styles.overviewCard}>
        <Card.Content>
          <Text style={styles.cardTitle}>Portfolio Overview</Text>
          
          <View style={styles.portfolioStats}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>
                {formatCurrency(portfolioData?.total_value || 0)}
              </Text>
              <Text style={styles.statLabel}>Total Value</Text>
            </View>
            
            <View style={styles.statItem}>
              <Text style={[styles.statValue, { color: getPerformanceColor(dashboardData?.total_return_percentage || 0) }]}>
                {formatCurrency(dashboardData?.total_return || 0)}
              </Text>
              <Text style={styles.statLabel}>Total Return</Text>
            </View>
            
            <View style={styles.statItem}>
              <Text style={[styles.statValue, { color: getPerformanceColor(dashboardData?.total_return_percentage || 0) }]}>
                {formatPercentage(dashboardData?.total_return_percentage || 0)}
              </Text>
              <Text style={styles.statLabel}>Return %</Text>
            </View>
          </View>
        </Card.Content>
      </Card>

      {/* Performance Chart */}
      <Card style={styles.chartCard}>
        <Card.Content>
          <Text style={styles.cardTitle}>Performance Trend</Text>
          {dashboardData?.performance_history && (
            <LineChart
              data={{
                labels: dashboardData.performance_history.map((_, index) => `${index + 1}D`),
                datasets: [
                  {
                    data: dashboardData.performance_history.map(point => point.value),
                    color: (opacity = 1) => `rgba(102, 126, 234, ${opacity})`,
                    strokeWidth: 3,
                  },
                ],
              }}
              width={width - 64}
              height={220}
              chartConfig={chartConfig}
              bezier
              style={styles.chart}
            />
          )}
        </Card.Content>
      </Card>

      {/* Fund Allocation */}
      <Card style={styles.allocationCard}>
        <Card.Content>
          <Text style={styles.cardTitle}>Fund Allocation</Text>
          {pieData.length > 0 ? (
            <PieChart
              data={pieData}
              width={width - 64}
              height={220}
              chartConfig={chartConfig}
              accessor="population"
              backgroundColor="transparent"
              paddingLeft="15"
              style={styles.chart}
            />
          ) : (
            <View style={styles.noDataContainer}>
              <Text style={styles.noDataText}>No investments yet</Text>
              <Button
                mode="contained"
                onPress={() => navigation.navigate('CreateInvestment')}
                style={styles.startInvestingButton}
              >
                Start Investing
              </Button>
            </View>
          )}
        </Card.Content>
      </Card>

      {/* Quick Actions */}
      <Card style={styles.actionsCard}>
        <Card.Content>
          <Text style={styles.cardTitle}>Quick Actions</Text>
          <View style={styles.actionsGrid}>
            <Button
              mode="outlined"
              onPress={() => navigation.navigate('Funds')}
              style={styles.actionButton}
              icon="trending-up"
            >
              Browse Funds
            </Button>
            <Button
              mode="outlined"
              onPress={() => navigation.navigate('Portfolio')}
              style={styles.actionButton}
              icon="pie-chart"
            >
              View Portfolio
            </Button>
            <Button
              mode="outlined"
              onPress={() => navigation.navigate('Analytics')}
              style={styles.actionButton}
              icon="analytics"
            >
              Analytics
            </Button>
            <Button
              mode="outlined"
              onPress={() => navigation.navigate('Profile')}
              style={styles.actionButton}
              icon="person"
            >
              Profile
            </Button>
          </View>
        </Card.Content>
      </Card>

      {/* Recent Activity */}
      <Card style={styles.activityCard}>
        <Card.Content>
          <Text style={styles.cardTitle}>Recent Activity</Text>
          <View style={styles.activityList}>
            {portfolioData?.recent_investments?.slice(0, 3).map((investment, index) => (
              <View key={index} style={styles.activityItem}>
                <View style={styles.activityIcon}>
                  <Ionicons name="trending-up" size={20} color={colors.primary} />
                </View>
                <View style={styles.activityContent}>
                  <Text style={styles.activityTitle}>{investment.fund_name}</Text>
                  <Text style={styles.activitySubtitle}>
                    {formatCurrency(investment.amount)} • {investment.date}
                  </Text>
                </View>
                <Chip
                  mode="outlined"
                  textStyle={styles.activityChipText}
                  style={styles.activityChip}
                >
                  {investment.status}
                </Chip>
              </View>
            )) || (
              <Text style={styles.noActivityText}>No recent activity</Text>
            )}
          </View>
        </Card.Content>
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.xl,
    paddingTop: spacing.xxl,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  welcomeText: {
    ...typography.h5,
    color: colors.white,
    opacity: 0.9,
  },
  userName: {
    ...typography.h2,
    color: colors.white,
    fontWeight: 'bold',
  },
  investButton: {
    borderRadius: borderRadius.lg,
    backgroundColor: colors.white,
  },
  investButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  investButtonText: {
    color: colors.primary,
    fontWeight: 'bold',
    marginLeft: spacing.xs,
  },
  overviewCard: {
    margin: spacing.md,
    borderRadius: borderRadius.lg,
    ...shadows.md,
  },
  cardTitle: {
    ...typography.h5,
    color: colors.text,
    marginBottom: spacing.md,
  },
  portfolioStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    ...typography.h4,
    fontWeight: 'bold',
    color: colors.text,
  },
  statLabel: {
    ...typography.caption,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  chartCard: {
    margin: spacing.md,
    borderRadius: borderRadius.lg,
    ...shadows.md,
  },
  allocationCard: {
    margin: spacing.md,
    borderRadius: borderRadius.lg,
    ...shadows.md,
  },
  chart: {
    marginVertical: spacing.sm,
    borderRadius: borderRadius.md,
  },
  noDataContainer: {
    alignItems: 'center',
    paddingVertical: spacing.xl,
  },
  noDataText: {
    ...typography.body1,
    color: colors.textSecondary,
    marginBottom: spacing.md,
  },
  startInvestingButton: {
    borderRadius: borderRadius.lg,
  },
  actionsCard: {
    margin: spacing.md,
    borderRadius: borderRadius.lg,
    ...shadows.md,
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  actionButton: {
    width: '48%',
    marginBottom: spacing.sm,
    borderRadius: borderRadius.lg,
  },
  activityCard: {
    margin: spacing.md,
    borderRadius: borderRadius.lg,
    ...shadows.md,
  },
  activityList: {
    marginTop: spacing.sm,
  },
  activityItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  activityIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.primary + '20',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  activityContent: {
    flex: 1,
  },
  activityTitle: {
    ...typography.body1,
    fontWeight: '600',
    color: colors.text,
  },
  activitySubtitle: {
    ...typography.caption,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  activityChip: {
    height: 28,
  },
  activityChipText: {
    fontSize: 12,
  },
  noActivityText: {
    ...typography.body1,
    color: colors.textSecondary,
    textAlign: 'center',
    paddingVertical: spacing.lg,
  },
});
