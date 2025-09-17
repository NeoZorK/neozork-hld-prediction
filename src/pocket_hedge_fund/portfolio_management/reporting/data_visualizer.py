"""
Data Visualizer - Portfolio Data Visualization

This module provides data visualization functionality for portfolio
reports including charts, graphs, and interactive visualizations.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, date, timedelta
from decimal import Decimal
import json

logger = logging.getLogger(__name__)


class DataVisualizer:
    """Portfolio data visualization functionality."""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.chart_types = {
            'line': self._create_line_chart,
            'bar': self._create_bar_chart,
            'pie': self._create_pie_chart,
            'scatter': self._create_scatter_chart,
            'heatmap': self._create_heatmap,
            'candlestick': self._create_candlestick_chart
        }
        
    async def create_portfolio_charts(
        self, 
        portfolio_data: Dict[str, Any],
        chart_configs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create portfolio visualization charts."""
        try:
            charts = {}
            
            for config in chart_configs:
                chart_type = config.get('type')
                chart_id = config.get('id')
                chart_title = config.get('title', f'{chart_type.title()} Chart')
                
                if chart_type in self.chart_types:
                    chart_data = await self.chart_types[chart_type](portfolio_data, config)
                    charts[chart_id] = {
                        'type': chart_type,
                        'title': chart_title,
                        'data': chart_data,
                        'config': config
                    }
                else:
                    logger.warning(f"Unknown chart type: {chart_type}")
            
            return charts
            
        except Exception as e:
            logger.error(f"Failed to create portfolio charts: {e}")
            return {}
    
    async def create_performance_charts(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create performance visualization charts."""
        try:
            charts = {}
            
            # Portfolio value over time
            charts['portfolio_value'] = await self._create_line_chart(
                performance_data, 
                {
                    'data_key': 'portfolio_values',
                    'x_axis': 'dates',
                    'y_axis': 'values',
                    'title': 'Portfolio Value Over Time'
                }
            )
            
            # Returns distribution
            charts['returns_distribution'] = await self._create_bar_chart(
                performance_data,
                {
                    'data_key': 'returns_distribution',
                    'x_axis': 'return_ranges',
                    'y_axis': 'frequencies',
                    'title': 'Returns Distribution'
                }
            )
            
            # Drawdown chart
            charts['drawdown'] = await self._create_line_chart(
                performance_data,
                {
                    'data_key': 'drawdowns',
                    'x_axis': 'dates',
                    'y_axis': 'drawdown_percentages',
                    'title': 'Portfolio Drawdown'
                }
            )
            
            return charts
            
        except Exception as e:
            logger.error(f"Failed to create performance charts: {e}")
            return {}
    
    async def create_risk_charts(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create risk visualization charts."""
        try:
            charts = {}
            
            # VaR chart
            charts['var_chart'] = await self._create_line_chart(
                risk_data,
                {
                    'data_key': 'var_data',
                    'x_axis': 'dates',
                    'y_axis': 'var_values',
                    'title': 'Value at Risk Over Time'
                }
            )
            
            # Risk heatmap
            charts['risk_heatmap'] = await self._create_heatmap(
                risk_data,
                {
                    'data_key': 'correlation_matrix',
                    'title': 'Asset Correlation Matrix'
                }
            )
            
            # Risk contribution pie chart
            charts['risk_contribution'] = await self._create_pie_chart(
                risk_data,
                {
                    'data_key': 'risk_contributions',
                    'title': 'Risk Contribution by Asset'
                }
            )
            
            return charts
            
        except Exception as e:
            logger.error(f"Failed to create risk charts: {e}")
            return {}
    
    async def create_allocation_charts(self, allocation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create allocation visualization charts."""
        try:
            charts = {}
            
            # Asset allocation pie chart
            charts['asset_allocation'] = await self._create_pie_chart(
                allocation_data,
                {
                    'data_key': 'asset_allocation',
                    'title': 'Asset Allocation'
                }
            )
            
            # Sector allocation pie chart
            charts['sector_allocation'] = await self._create_pie_chart(
                allocation_data,
                {
                    'data_key': 'sector_allocation',
                    'title': 'Sector Allocation'
                }
            )
            
            # Position weights bar chart
            charts['position_weights'] = await self._create_bar_chart(
                allocation_data,
                {
                    'data_key': 'position_weights',
                    'x_axis': 'assets',
                    'y_axis': 'weights',
                    'title': 'Position Weights'
                }
            )
            
            return charts
            
        except Exception as e:
            logger.error(f"Failed to create allocation charts: {e}")
            return {}
    
    # Chart creation methods
    async def _create_line_chart(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create line chart data."""
        try:
            data_key = config.get('data_key')
            x_axis = config.get('x_axis', 'x')
            y_axis = config.get('y_axis', 'y')
            
            chart_data = data.get(data_key, {})
            
            return {
                'type': 'line',
                'data': {
                    'labels': chart_data.get(x_axis, []),
                    'datasets': [{
                        'label': config.get('title', 'Data'),
                        'data': chart_data.get(y_axis, []),
                        'borderColor': config.get('color', '#3B82F6'),
                        'backgroundColor': config.get('fill_color', 'rgba(59, 130, 246, 0.1)'),
                        'fill': config.get('fill', True)
                    }]
                },
                'options': {
                    'responsive': True,
                    'scales': {
                        'x': {
                            'title': {
                                'display': True,
                                'text': x_axis.title()
                            }
                        },
                        'y': {
                            'title': {
                                'display': True,
                                'text': y_axis.title()
                            }
                        }
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create line chart: {e}")
            return {}
    
    async def _create_bar_chart(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create bar chart data."""
        try:
            data_key = config.get('data_key')
            x_axis = config.get('x_axis', 'x')
            y_axis = config.get('y_axis', 'y')
            
            chart_data = data.get(data_key, {})
            
            return {
                'type': 'bar',
                'data': {
                    'labels': chart_data.get(x_axis, []),
                    'datasets': [{
                        'label': config.get('title', 'Data'),
                        'data': chart_data.get(y_axis, []),
                        'backgroundColor': config.get('colors', ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6']),
                        'borderColor': config.get('border_colors', ['#1D4ED8', '#DC2626', '#059669', '#D97706', '#7C3AED']),
                        'borderWidth': 1
                    }]
                },
                'options': {
                    'responsive': True,
                    'scales': {
                        'x': {
                            'title': {
                                'display': True,
                                'text': x_axis.title()
                            }
                        },
                        'y': {
                            'title': {
                                'display': True,
                                'text': y_axis.title()
                            }
                        }
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create bar chart: {e}")
            return {}
    
    async def _create_pie_chart(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create pie chart data."""
        try:
            data_key = config.get('data_key')
            chart_data = data.get(data_key, {})
            
            # Convert dictionary to arrays
            labels = list(chart_data.keys())
            values = list(chart_data.values())
            
            return {
                'type': 'pie',
                'data': {
                    'labels': labels,
                    'datasets': [{
                        'data': values,
                        'backgroundColor': config.get('colors', [
                            '#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6',
                            '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1'
                        ]),
                        'borderWidth': 2,
                        'borderColor': '#FFFFFF'
                    }]
                },
                'options': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'position': 'right'
                        }
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create pie chart: {e}")
            return {}
    
    async def _create_scatter_chart(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create scatter chart data."""
        try:
            data_key = config.get('data_key')
            x_axis = config.get('x_axis', 'x')
            y_axis = config.get('y_axis', 'y')
            
            chart_data = data.get(data_key, {})
            
            # Convert to scatter format
            scatter_data = []
            x_values = chart_data.get(x_axis, [])
            y_values = chart_data.get(y_axis, [])
            
            for i in range(len(x_values)):
                scatter_data.append({
                    'x': x_values[i],
                    'y': y_values[i]
                })
            
            return {
                'type': 'scatter',
                'data': {
                    'datasets': [{
                        'label': config.get('title', 'Data'),
                        'data': scatter_data,
                        'backgroundColor': config.get('color', '#3B82F6'),
                        'borderColor': config.get('border_color', '#1D4ED8')
                    }]
                },
                'options': {
                    'responsive': True,
                    'scales': {
                        'x': {
                            'title': {
                                'display': True,
                                'text': x_axis.title()
                            }
                        },
                        'y': {
                            'title': {
                                'display': True,
                                'text': y_axis.title()
                            }
                        }
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create scatter chart: {e}")
            return {}
    
    async def _create_heatmap(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create heatmap data."""
        try:
            data_key = config.get('data_key')
            chart_data = data.get(data_key, {})
            
            # Convert correlation matrix to heatmap format
            labels = list(chart_data.keys())
            matrix_data = []
            
            for i, row_label in enumerate(labels):
                row_data = []
                for j, col_label in enumerate(labels):
                    if row_label in chart_data and col_label in chart_data[row_label]:
                        row_data.append(chart_data[row_label][col_label])
                    else:
                        row_data.append(0)
                matrix_data.append(row_data)
            
            return {
                'type': 'heatmap',
                'data': {
                    'labels': labels,
                    'datasets': [{
                        'label': config.get('title', 'Heatmap'),
                        'data': matrix_data,
                        'backgroundColor': config.get('color_scheme', 'Blues')
                    }]
                },
                'options': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'display': False
                        }
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create heatmap: {e}")
            return {}
    
    async def _create_candlestick_chart(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create candlestick chart data."""
        try:
            data_key = config.get('data_key')
            chart_data = data.get(data_key, {})
            
            # Convert to candlestick format
            candlestick_data = []
            dates = chart_data.get('dates', [])
            opens = chart_data.get('opens', [])
            highs = chart_data.get('highs', [])
            lows = chart_data.get('lows', [])
            closes = chart_data.get('closes', [])
            
            for i in range(len(dates)):
                candlestick_data.append({
                    'x': dates[i],
                    'o': opens[i],
                    'h': highs[i],
                    'l': lows[i],
                    'c': closes[i]
                })
            
            return {
                'type': 'candlestick',
                'data': {
                    'datasets': [{
                        'label': config.get('title', 'Price Data'),
                        'data': candlestick_data
                    }]
                },
                'options': {
                    'responsive': True,
                    'scales': {
                        'x': {
                            'type': 'time',
                            'time': {
                                'unit': 'day'
                            }
                        },
                        'y': {
                            'title': {
                                'display': True,
                                'text': 'Price'
                            }
                        }
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create candlestick chart: {e}")
            return {}
    
    async def create_dashboard_data(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive dashboard data."""
        try:
            dashboard = {
                'summary_cards': await self._create_summary_cards(portfolio_data),
                'performance_charts': await self.create_performance_charts(portfolio_data.get('performance', {})),
                'risk_charts': await self.create_risk_charts(portfolio_data.get('risk', {})),
                'allocation_charts': await self.create_allocation_charts(portfolio_data.get('allocation', {})),
                'tables': await self._create_data_tables(portfolio_data)
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Failed to create dashboard data: {e}")
            return {}
    
    async def _create_summary_cards(self, portfolio_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create summary cards for dashboard."""
        try:
            cards = []
            
            # Total value card
            total_value = portfolio_data.get('total_value', 0)
            cards.append({
                'title': 'Total Value',
                'value': f'${total_value:,.2f}',
                'change': portfolio_data.get('daily_change', 0),
                'change_percentage': portfolio_data.get('daily_change_percentage', 0),
                'icon': 'dollar-sign',
                'color': 'green'
            })
            
            # Total return card
            total_return = portfolio_data.get('total_return', 0)
            cards.append({
                'title': 'Total Return',
                'value': f'{total_return:.2f}%',
                'change': portfolio_data.get('return_change', 0),
                'change_percentage': portfolio_data.get('return_change_percentage', 0),
                'icon': 'trending-up',
                'color': 'blue'
            })
            
            # Risk metrics card
            var_95 = portfolio_data.get('var_95', 0)
            cards.append({
                'title': 'VaR (95%)',
                'value': f'{var_95:.2f}%',
                'change': 0,
                'change_percentage': 0,
                'icon': 'shield',
                'color': 'red'
            })
            
            # Sharpe ratio card
            sharpe_ratio = portfolio_data.get('sharpe_ratio', 0)
            cards.append({
                'title': 'Sharpe Ratio',
                'value': f'{sharpe_ratio:.2f}',
                'change': 0,
                'change_percentage': 0,
                'icon': 'target',
                'color': 'purple'
            })
            
            return cards
            
        except Exception as e:
            logger.error(f"Failed to create summary cards: {e}")
            return []
    
    async def _create_data_tables(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create data tables for dashboard."""
        try:
            tables = {}
            
            # Positions table
            positions = portfolio_data.get('positions', [])
            tables['positions'] = {
                'title': 'Portfolio Positions',
                'columns': ['Asset', 'Quantity', 'Price', 'Value', 'P&L', 'Weight'],
                'data': [
                    [
                        pos.get('asset_name', ''),
                        f"{pos.get('quantity', 0):,.2f}",
                        f"${pos.get('current_price', 0):,.2f}",
                        f"${pos.get('market_value', 0):,.2f}",
                        f"${pos.get('unrealized_pnl', 0):,.2f}",
                        f"{pos.get('weight_percentage', 0):.2f}%"
                    ]
                    for pos in positions
                ]
            }
            
            # Performance table
            performance_metrics = portfolio_data.get('performance_metrics', {})
            tables['performance'] = {
                'title': 'Performance Metrics',
                'columns': ['Metric', 'Value'],
                'data': [
                    ['Total Return', f"{performance_metrics.get('total_return', 0):.2f}%"],
                    ['Annualized Return', f"{performance_metrics.get('annualized_return', 0):.2f}%"],
                    ['Volatility', f"{performance_metrics.get('volatility', 0):.2f}%"],
                    ['Sharpe Ratio', f"{performance_metrics.get('sharpe_ratio', 0):.2f}"],
                    ['Max Drawdown', f"{performance_metrics.get('max_drawdown', 0):.2f}%"]
                ]
            }
            
            return tables
            
        except Exception as e:
            logger.error(f"Failed to create data tables: {e}")
            return {}
    
    def export_chart_data(self, charts: Dict[str, Any], format: str = 'json') -> str:
        """Export chart data in specified format."""
        try:
            if format.lower() == 'json':
                return json.dumps(charts, indent=2, default=str)
            elif format.lower() == 'csv':
                # Convert to CSV format (simplified)
                return self._convert_to_csv(charts)
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            logger.error(f"Failed to export chart data: {e}")
            return ""
    
    def _convert_to_csv(self, charts: Dict[str, Any]) -> str:
        """Convert chart data to CSV format."""
        # This would implement CSV conversion
        return ""
