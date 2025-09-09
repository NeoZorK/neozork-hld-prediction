"""
Chart Generator

Generates various types of charts for analytics visualization.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json
import base64
from io import BytesIO

from ..models.analytics_models import MarketData, PredictionResult, AnalyticsInsight

logger = logging.getLogger(__name__)


class ChartGenerator:
    """
    Generates various types of charts for analytics visualization.
    """
    
    def __init__(self):
        """Initialize chart generator."""
        self.chart_configs = self._setup_chart_configs()
        self.supported_formats = ['png', 'svg', 'html', 'json']
    
    def _setup_chart_configs(self) -> Dict[str, Any]:
        """Setup default chart configurations."""
        return {
            'price_chart': {
                'type': 'line',
                'width': 800,
                'height': 400,
                'colors': ['#1f77b4', '#ff7f0e', '#2ca02c'],
                'grid': True,
                'legend': True
            },
            'volume_chart': {
                'type': 'bar',
                'width': 800,
                'height': 200,
                'colors': ['#17a2b8'],
                'grid': True,
                'legend': False
            },
            'correlation_heatmap': {
                'type': 'heatmap',
                'width': 600,
                'height': 600,
                'colors': ['#ffffff', '#ff0000'],
                'grid': True,
                'legend': True
            },
            'prediction_chart': {
                'type': 'line',
                'width': 800,
                'height': 400,
                'colors': ['#1f77b4', '#ff7f0e', '#2ca02c'],
                'grid': True,
                'legend': True,
                'confidence_bands': True
            }
        }
    
    async def generate_price_chart(
        self,
        market_data: List[MarketData],
        indicators: Optional[Dict[str, List[float]]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate price chart with optional technical indicators.
        
        Args:
            market_data: Market data
            indicators: Technical indicators data
            config: Chart configuration
            
        Returns:
            Chart data in specified format
        """
        try:
            if not market_data:
                raise ValueError("Market data cannot be empty")
            
            chart_config = self._merge_config('price_chart', config)
            
            # Prepare data
            chart_data = self._prepare_price_data(market_data, indicators)
            
            # Generate chart
            chart = await self._create_line_chart(chart_data, chart_config)
            
            return {
                'type': 'price_chart',
                'data': chart_data,
                'config': chart_config,
                'chart': chart,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate price chart: {e}")
            raise
    
    async def generate_volume_chart(
        self,
        market_data: List[MarketData],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate volume chart."""
        try:
            if not market_data:
                raise ValueError("Market data cannot be empty")
            
            chart_config = self._merge_config('volume_chart', config)
            
            # Prepare data
            chart_data = self._prepare_volume_data(market_data)
            
            # Generate chart
            chart = await self._create_bar_chart(chart_data, chart_config)
            
            return {
                'type': 'volume_chart',
                'data': chart_data,
                'config': chart_config,
                'chart': chart,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate volume chart: {e}")
            raise
    
    async def generate_correlation_heatmap(
        self,
        correlation_matrix: Dict[str, Dict[str, float]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate correlation heatmap."""
        try:
            if not correlation_matrix:
                raise ValueError("Correlation matrix cannot be empty")
            
            chart_config = self._merge_config('correlation_heatmap', config)
            
            # Prepare data
            chart_data = self._prepare_correlation_data(correlation_matrix)
            
            # Generate chart
            chart = await self._create_heatmap_chart(chart_data, chart_config)
            
            return {
                'type': 'correlation_heatmap',
                'data': chart_data,
                'config': chart_config,
                'chart': chart,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate correlation heatmap: {e}")
            raise
    
    async def generate_prediction_chart(
        self,
        market_data: List[MarketData],
        predictions: List[PredictionResult],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate prediction chart with confidence bands."""
        try:
            if not market_data or not predictions:
                raise ValueError("Market data and predictions cannot be empty")
            
            chart_config = self._merge_config('prediction_chart', config)
            
            # Prepare data
            chart_data = self._prepare_prediction_data(market_data, predictions)
            
            # Generate chart
            chart = await self._create_prediction_chart(chart_data, chart_config)
            
            return {
                'type': 'prediction_chart',
                'data': chart_data,
                'config': chart_config,
                'chart': chart,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate prediction chart: {e}")
            raise
    
    async def generate_insights_chart(
        self,
        insights: List[AnalyticsInsight],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate insights visualization chart."""
        try:
            if not insights:
                raise ValueError("Insights cannot be empty")
            
            # Prepare data
            chart_data = self._prepare_insights_data(insights)
            
            # Generate chart
            chart = await self._create_insights_chart(chart_data, config)
            
            return {
                'type': 'insights_chart',
                'data': chart_data,
                'config': config or {},
                'chart': chart,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate insights chart: {e}")
            raise
    
    def _merge_config(self, chart_type: str, custom_config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge default config with custom config."""
        base_config = self.chart_configs.get(chart_type, {}).copy()
        if custom_config:
            base_config.update(custom_config)
        return base_config
    
    def _prepare_price_data(
        self,
        market_data: List[MarketData],
        indicators: Optional[Dict[str, List[float]]] = None
    ) -> Dict[str, Any]:
        """Prepare price chart data."""
        try:
            # Extract price data
            timestamps = [data.timestamp.isoformat() for data in market_data]
            prices = [float(data.close_price) for data in market_data]
            volumes = [float(data.volume) for data in market_data]
            
            chart_data = {
                'timestamps': timestamps,
                'prices': prices,
                'volumes': volumes,
                'indicators': indicators or {}
            }
            
            return chart_data
            
        except Exception as e:
            logger.error(f"Failed to prepare price data: {e}")
            raise
    
    def _prepare_volume_data(self, market_data: List[MarketData]) -> Dict[str, Any]:
        """Prepare volume chart data."""
        try:
            timestamps = [data.timestamp.isoformat() for data in market_data]
            volumes = [float(data.volume) for data in market_data]
            
            return {
                'timestamps': timestamps,
                'volumes': volumes
            }
            
        except Exception as e:
            logger.error(f"Failed to prepare volume data: {e}")
            raise
    
    def _prepare_correlation_data(self, correlation_matrix: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Prepare correlation heatmap data."""
        try:
            symbols = list(correlation_matrix.keys())
            correlations = []
            
            for symbol1 in symbols:
                row = []
                for symbol2 in symbols:
                    if symbol1 in correlation_matrix and symbol2 in correlation_matrix[symbol1]:
                        row.append(correlation_matrix[symbol1][symbol2])
                    else:
                        row.append(0.0)
                correlations.append(row)
            
            return {
                'symbols': symbols,
                'correlations': correlations
            }
            
        except Exception as e:
            logger.error(f"Failed to prepare correlation data: {e}")
            raise
    
    def _prepare_prediction_data(
        self,
        market_data: List[MarketData],
        predictions: List[PredictionResult]
    ) -> Dict[str, Any]:
        """Prepare prediction chart data."""
        try:
            # Historical data
            timestamps = [data.timestamp.isoformat() for data in market_data]
            prices = [float(data.close_price) for data in market_data]
            
            # Prediction data
            pred_timestamps = [pred.timestamp.isoformat() for pred in predictions]
            pred_values = [float(pred.predicted_value) for pred in predictions]
            confidences = [float(pred.confidence) for pred in predictions]
            
            # Calculate confidence bands
            confidence_bands = self._calculate_confidence_bands(pred_values, confidences)
            
            return {
                'historical': {
                    'timestamps': timestamps,
                    'prices': prices
                },
                'predictions': {
                    'timestamps': pred_timestamps,
                    'values': pred_values,
                    'confidences': confidences,
                    'confidence_bands': confidence_bands
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to prepare prediction data: {e}")
            raise
    
    def _prepare_insights_data(self, insights: List[AnalyticsInsight]) -> Dict[str, Any]:
        """Prepare insights chart data."""
        try:
            insight_types = {}
            confidence_levels = []
            impact_levels = []
            
            for insight in insights:
                # Group by type
                if insight.insight_type not in insight_types:
                    insight_types[insight.insight_type] = 0
                insight_types[insight.insight_type] += 1
                
                # Collect confidence and impact
                confidence_levels.append(float(insight.confidence))
                impact_levels.append(insight.impact)
            
            return {
                'insight_types': insight_types,
                'confidence_levels': confidence_levels,
                'impact_levels': impact_levels,
                'total_insights': len(insights)
            }
            
        except Exception as e:
            logger.error(f"Failed to prepare insights data: {e}")
            raise
    
    def _calculate_confidence_bands(
        self,
        values: List[float],
        confidences: List[float]
    ) -> Dict[str, List[float]]:
        """Calculate confidence bands for predictions."""
        try:
            upper_band = []
            lower_band = []
            
            for value, confidence in zip(values, confidences):
                # Calculate band width based on confidence
                band_width = value * (1 - confidence) * 0.1  # 10% of value
                upper_band.append(value + band_width)
                lower_band.append(value - band_width)
            
            return {
                'upper': upper_band,
                'lower': lower_band
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate confidence bands: {e}")
            return {'upper': values, 'lower': values}
    
    async def _create_line_chart(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create line chart (simplified implementation)."""
        try:
            # This is a simplified implementation
            # In practice, you would use libraries like Plotly, Matplotlib, or Chart.js
            
            chart_config = {
                'type': 'line',
                'data': data,
                'config': config,
                'rendered': True
            }
            
            # Convert to JSON string for now
            return json.dumps(chart_config)
            
        except Exception as e:
            logger.error(f"Failed to create line chart: {e}")
            raise
    
    async def _create_bar_chart(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create bar chart (simplified implementation)."""
        try:
            chart_config = {
                'type': 'bar',
                'data': data,
                'config': config,
                'rendered': True
            }
            
            return json.dumps(chart_config)
            
        except Exception as e:
            logger.error(f"Failed to create bar chart: {e}")
            raise
    
    async def _create_heatmap_chart(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create heatmap chart (simplified implementation)."""
        try:
            chart_config = {
                'type': 'heatmap',
                'data': data,
                'config': config,
                'rendered': True
            }
            
            return json.dumps(chart_config)
            
        except Exception as e:
            logger.error(f"Failed to create heatmap chart: {e}")
            raise
    
    async def _create_prediction_chart(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Create prediction chart (simplified implementation)."""
        try:
            chart_config = {
                'type': 'prediction',
                'data': data,
                'config': config,
                'rendered': True
            }
            
            return json.dumps(chart_config)
            
        except Exception as e:
            logger.error(f"Failed to create prediction chart: {e}")
            raise
    
    async def _create_insights_chart(self, data: Dict[str, Any], config: Optional[Dict[str, Any]]) -> str:
        """Create insights chart (simplified implementation)."""
        try:
            chart_config = {
                'type': 'insights',
                'data': data,
                'config': config or {},
                'rendered': True
            }
            
            return json.dumps(chart_config)
            
        except Exception as e:
            logger.error(f"Failed to create insights chart: {e}")
            raise
    
    async def export_chart(
        self,
        chart_data: Dict[str, Any],
        format: str = 'json',
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export chart in specified format.
        
        Args:
            chart_data: Chart data
            format: Export format
            filename: Optional filename
            
        Returns:
            Export result
        """
        try:
            if format not in self.supported_formats:
                raise ValueError(f"Unsupported format: {format}")
            
            if format == 'json':
                export_data = json.dumps(chart_data, indent=2)
            elif format == 'html':
                export_data = self._generate_html_chart(chart_data)
            else:
                # For PNG/SVG, you would use actual charting libraries
                export_data = f"Chart data in {format} format"
            
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"chart_{timestamp}.{format}"
            
            return {
                'format': format,
                'filename': filename,
                'data': export_data,
                'size': len(export_data) if isinstance(export_data, str) else 0,
                'exported_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to export chart: {e}")
            raise
    
    def _generate_html_chart(self, chart_data: Dict[str, Any]) -> str:
        """Generate HTML chart (simplified implementation)."""
        try:
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Analytics Chart</title>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            </head>
            <body>
                <div id="chart"></div>
                <script>
                    var chartData = {chart_data};
                    Plotly.newPlot('chart', chartData.data, chartData.config);
                </script>
            </body>
            </html>
            """
            
            return html_template.format(chart_data=json.dumps(chart_data))
            
        except Exception as e:
            logger.error(f"Failed to generate HTML chart: {e}")
            return "<html><body>Chart generation failed</body></html>"
