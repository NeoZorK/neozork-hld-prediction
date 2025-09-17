/**
 * Usage Chart Component for Dashboard
 * 
 * This component displays usage analytics in various chart formats
 * including line, bar, and pie charts.
 */

import React, { useState, useEffect } from 'react';
import { Button } from './ui/Button';
import { UsageStats, ChartData, ChartDataPoint } from '../../types';
import { chartService } from '../../services/chartService';
import './UsageChart.css';

// ============================================================================
// INTERFACES
// ============================================================================

interface UsageChartProps {
  data: UsageStats;
  onError?: (error: string) => void;
}

interface ChartOption {
  id: string;
  label: string;
  type: 'line' | 'bar' | 'pie';
  dataKey: string;
}

// ============================================================================
// CONSTANTS
// ============================================================================

const CHART_OPTIONS: ChartOption[] = [
  { id: 'api_calls', label: 'API Calls', type: 'line', dataKey: 'api_calls' },
  { id: 'storage', label: 'Storage Usage', type: 'bar', dataKey: 'storage' },
  { id: 'users', label: 'Active Users', type: 'line', dataKey: 'users' },
  { id: 'revenue', label: 'Revenue', type: 'bar', dataKey: 'revenue' }
];

const CHART_PERIODS = [
  { id: '7d', label: '7 Days' },
  { id: '30d', label: '30 Days' },
  { id: '90d', label: '90 Days' },
  { id: '1y', label: '1 Year' }
];

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const UsageChart: React.FC<UsageChartProps> = ({
  data,
  onError
}) => {
  const [selectedChart, setSelectedChart] = useState<ChartOption>(CHART_OPTIONS[0]);
  const [selectedPeriod, setSelectedPeriod] = useState<string>('30d');
  const [chartData, setChartData] = useState<ChartData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadChartData();
  }, [selectedChart, selectedPeriod]);

  const loadChartData = async () => {
    try {
      setLoading(true);
      
      const response = await chartService.getUsageData({
        type: selectedChart.type,
        period: selectedPeriod,
        dataKey: selectedChart.dataKey
      });
      
      if (response.success) {
        setChartData(response.data);
      } else {
        onError?.(response.error || 'Failed to load chart data');
      }
    } catch (error) {
      onError?.(error instanceof Error ? error.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const renderChart = () => {
    if (!chartData) return null;

    switch (selectedChart.type) {
      case 'line':
        return <LineChart data={chartData} />;
      case 'bar':
        return <BarChart data={chartData} />;
      case 'pie':
        return <PieChart data={chartData} />;
      default:
        return null;
    }
  };

  return (
    <div className="usage-chart">
      {/* Chart Controls */}
      <div className="chart-controls">
        <div className="chart-type-selector">
          {CHART_OPTIONS.map(option => (
            <Button
              key={option.id}
              variant={selectedChart.id === option.id ? 'primary' : 'secondary'}
              size="small"
              onClick={() => setSelectedChart(option)}
            >
              {option.label}
            </Button>
          ))}
        </div>
        
        <div className="chart-period-selector">
          {CHART_PERIODS.map(period => (
            <Button
              key={period.id}
              variant={selectedPeriod === period.id ? 'primary' : 'secondary'}
              size="small"
              onClick={() => setSelectedPeriod(period.id)}
            >
              {period.label}
            </Button>
          ))}
        </div>
      </div>

      {/* Chart Container */}
      <div className="chart-container">
        {loading ? (
          <div className="chart-loading">
            <div className="loading-spinner" />
            <p>Loading chart data...</p>
          </div>
        ) : (
          renderChart()
        )}
      </div>

      {/* Chart Summary */}
      {data && (
        <div className="chart-summary">
          <div className="summary-item">
            <span className="summary-label">Current Usage:</span>
            <span className="summary-value">
              {selectedChart.dataKey === 'api_calls' && data.total_api_calls.toLocaleString()}
              {selectedChart.dataKey === 'storage' && `${data.total_storage_used.toFixed(1)} GB`}
              {selectedChart.dataKey === 'users' && data.active_users}
            </span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Peak Usage:</span>
            <span className="summary-value">
              {data.peak_usage.toLocaleString()}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// CHART COMPONENTS
// ============================================================================

const LineChart: React.FC<{ data: ChartData }> = ({ data }) => {
  return (
    <div className="line-chart">
      <svg viewBox="0 0 400 200" className="chart-svg">
        {/* Grid lines */}
        <defs>
          <pattern id="grid" width="40" height="20" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 20" fill="none" stroke="#e0e0e0" strokeWidth="1"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
        
        {/* Chart line */}
        <polyline
          fill="none"
          stroke="#3b82f6"
          strokeWidth="2"
          points={data.datasets[0]?.data.map((value, index) => 
            `${40 + (index * 360 / (data.datasets[0].data.length - 1))},${180 - (value * 160 / Math.max(...data.datasets[0].data))}`
          ).join(' ')}
        />
        
        {/* Data points */}
        {data.datasets[0]?.data.map((value, index) => (
          <circle
            key={index}
            cx={40 + (index * 360 / (data.datasets[0].data.length - 1))}
            cy={180 - (value * 160 / Math.max(...data.datasets[0].data))}
            r="4"
            fill="#3b82f6"
          />
        ))}
      </svg>
    </div>
  );
};

const BarChart: React.FC<{ data: ChartData }> = ({ data }) => {
  const maxValue = Math.max(...data.datasets[0]?.data || [1]);
  
  return (
    <div className="bar-chart">
      <svg viewBox="0 0 400 200" className="chart-svg">
        {data.datasets[0]?.data.map((value, index) => {
          const barHeight = (value / maxValue) * 160;
          const barWidth = 360 / data.datasets[0].data.length;
          const x = 20 + (index * barWidth);
          
          return (
            <rect
              key={index}
              x={x}
              y={180 - barHeight}
              width={barWidth - 4}
              height={barHeight}
              fill="#3b82f6"
              rx="2"
            />
          );
        })}
      </svg>
    </div>
  );
};

const PieChart: React.FC<{ data: ChartData }> = ({ data }) => {
  const total = data.datasets[0]?.data.reduce((sum, value) => sum + value, 0) || 1;
  let currentAngle = 0;
  
  return (
    <div className="pie-chart">
      <svg viewBox="0 0 200 200" className="chart-svg">
        {data.datasets[0]?.data.map((value, index) => {
          const percentage = value / total;
          const angle = percentage * 360;
          const startAngle = currentAngle;
          const endAngle = currentAngle + angle;
          
          const startAngleRad = (startAngle - 90) * Math.PI / 180;
          const endAngleRad = (endAngle - 90) * Math.PI / 180;
          
          const x1 = 100 + 80 * Math.cos(startAngleRad);
          const y1 = 100 + 80 * Math.sin(startAngleRad);
          const x2 = 100 + 80 * Math.cos(endAngleRad);
          const y2 = 100 + 80 * Math.sin(endAngleRad);
          
          const largeArcFlag = angle > 180 ? 1 : 0;
          
          const pathData = [
            `M 100 100`,
            `L ${x1} ${y1}`,
            `A 80 80 0 ${largeArcFlag} 1 ${x2} ${y2}`,
            `Z`
          ].join(' ');
          
          currentAngle += angle;
          
          return (
            <path
              key={index}
              d={pathData}
              fill={`hsl(${index * 60}, 70%, 50%)`}
              stroke="#fff"
              strokeWidth="2"
            />
          );
        })}
      </svg>
    </div>
  );
};

export default UsageChart;
