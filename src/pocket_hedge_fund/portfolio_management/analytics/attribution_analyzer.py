"""
Attribution Analyzer - Performance Attribution Analysis

This module provides performance attribution analysis including asset allocation
effects, security selection effects, and interaction effects.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, date, timedelta
from decimal import Decimal
import numpy as np
import pandas as pd

from ..models.portfolio_models import Portfolio, Position, AssetType
from ..models.performance_models import AttributionMetrics

logger = logging.getLogger(__name__)


class AttributionAnalyzer:
    """Performance attribution analysis functionality."""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        
    async def calculate_attribution_metrics(
        self, 
        portfolio: Portfolio, 
        benchmark_returns: Dict[str, float],
        period: str = "1Y"
    ) -> AttributionMetrics:
        """Calculate comprehensive attribution metrics."""
        try:
            # Get historical data
            portfolio_data = await self._get_portfolio_historical_data(portfolio.id, period)
            benchmark_data = await self._get_benchmark_historical_data(period)
            
            if not portfolio_data or not benchmark_data:
                return self._get_default_attribution_metrics()
            
            # Calculate attribution effects
            asset_allocation_effect = self._calculate_asset_allocation_effect(
                portfolio, portfolio_data, benchmark_data
            )
            
            security_selection_effect = self._calculate_security_selection_effect(
                portfolio, portfolio_data, benchmark_data
            )
            
            interaction_effect = self._calculate_interaction_effect(
                portfolio, portfolio_data, benchmark_data
            )
            
            total_attribution = asset_allocation_effect + security_selection_effect + interaction_effect
            
            # Get top and bottom contributors
            top_contributors = self._get_top_contributors(portfolio, portfolio_data, benchmark_data)
            bottom_contributors = self._get_bottom_contributors(portfolio, portfolio_data, benchmark_data)
            
            # Calculate sector and asset class attribution
            sector_attribution = self._calculate_sector_attribution(portfolio, portfolio_data, benchmark_data)
            asset_class_attribution = self._calculate_asset_class_attribution(portfolio, portfolio_data, benchmark_data)
            
            return AttributionMetrics(
                asset_allocation_effect=asset_allocation_effect,
                security_selection_effect=security_selection_effect,
                interaction_effect=interaction_effect,
                total_attribution=total_attribution,
                top_contributors=top_contributors,
                bottom_contributors=bottom_contributors,
                sector_attribution=sector_attribution,
                asset_class_attribution=asset_class_attribution,
                period_start=portfolio_data[0]['date'] if portfolio_data else date.today(),
                period_end=portfolio_data[-1]['date'] if portfolio_data else date.today()
            )
            
        except Exception as e:
            logger.error(f"Failed to calculate attribution metrics: {e}")
            return self._get_default_attribution_metrics()
    
    async def get_detailed_attribution(
        self, 
        portfolio: Portfolio, 
        benchmark_returns: Dict[str, float],
        period: str = "1Y"
    ) -> Dict[str, Any]:
        """Get detailed attribution analysis."""
        try:
            # Get historical data
            portfolio_data = await self._get_portfolio_historical_data(portfolio.id, period)
            benchmark_data = await self._get_benchmark_historical_data(period)
            
            if not portfolio_data or not benchmark_data:
                return {}
            
            # Position-level attribution
            position_attribution = self._calculate_position_level_attribution(
                portfolio, portfolio_data, benchmark_data
            )
            
            # Sector-level attribution
            sector_attribution = self._calculate_sector_level_attribution(
                portfolio, portfolio_data, benchmark_data
            )
            
            # Asset class attribution
            asset_class_attribution = self._calculate_asset_class_level_attribution(
                portfolio, portfolio_data, benchmark_data
            )
            
            # Time-based attribution
            time_attribution = self._calculate_time_based_attribution(
                portfolio, portfolio_data, benchmark_data
            )
            
            return {
                'position_attribution': position_attribution,
                'sector_attribution': sector_attribution,
                'asset_class_attribution': asset_class_attribution,
                'time_attribution': time_attribution,
                'summary': {
                    'total_attribution': sum(pos['contribution'] for pos in position_attribution.values()),
                    'top_contributor': max(position_attribution.values(), key=lambda x: x['contribution']) if position_attribution else None,
                    'bottom_contributor': min(position_attribution.values(), key=lambda x: x['contribution']) if position_attribution else None
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get detailed attribution: {e}")
            return {}
    
    async def get_rolling_attribution(
        self, 
        portfolio: Portfolio, 
        benchmark_returns: Dict[str, float],
        window: int = 30,
        period: str = "1Y"
    ) -> Dict[str, List[float]]:
        """Get rolling attribution analysis."""
        try:
            # Get historical data
            portfolio_data = await self._get_portfolio_historical_data(portfolio.id, period)
            benchmark_data = await self._get_benchmark_historical_data(period)
            
            if not portfolio_data or not benchmark_data:
                return {}
            
            # Calculate rolling attribution
            rolling_attribution = []
            dates = []
            
            for i in range(window, len(portfolio_data)):
                window_portfolio_data = portfolio_data[i-window:i]
                window_benchmark_data = benchmark_data[i-window:i]
                
                # Calculate attribution for this window
                attribution = self._calculate_window_attribution(
                    portfolio, window_portfolio_data, window_benchmark_data
                )
                
                rolling_attribution.append(attribution)
                dates.append(portfolio_data[i]['date'])
            
            return {
                'rolling_attribution': rolling_attribution,
                'dates': dates,
                'window_size': window
            }
            
        except Exception as e:
            logger.error(f"Failed to get rolling attribution: {e}")
            return {}
    
    def _calculate_asset_allocation_effect(
        self, 
        portfolio: Portfolio, 
        portfolio_data: List[Dict[str, Any]], 
        benchmark_data: List[Dict[str, Any]]
    ) -> float:
        """Calculate asset allocation effect."""
        try:
            # This is a simplified calculation
            # In practice, this would compare portfolio weights to benchmark weights
            # and calculate the effect of overweighting/underweighting asset classes
            
            total_effect = 0.0
            
            # Get current asset allocation
            asset_allocation = portfolio.get_asset_allocation()
            
            # Compare with benchmark allocation (simplified)
            benchmark_allocation = self._get_benchmark_asset_allocation()
            
            for asset_type, portfolio_weight in asset_allocation.items():
                benchmark_weight = benchmark_allocation.get(asset_type, 0)
                weight_diff = portfolio_weight - benchmark_weight
                
                # Get asset class return from benchmark
                asset_return = self._get_asset_class_return(asset_type, benchmark_data)
                
                # Allocation effect = (Portfolio Weight - Benchmark Weight) * Benchmark Return
                allocation_effect = (weight_diff / 100) * (asset_return / 100)
                total_effect += allocation_effect
            
            return total_effect * 100  # Convert to percentage
            
        except Exception as e:
            logger.error(f"Failed to calculate asset allocation effect: {e}")
            return 0.0
    
    def _calculate_security_selection_effect(
        self, 
        portfolio: Portfolio, 
        portfolio_data: List[Dict[str, Any]], 
        benchmark_data: List[Dict[str, Any]]
    ) -> float:
        """Calculate security selection effect."""
        try:
            # This is a simplified calculation
            # In practice, this would compare individual security returns
            # to their respective benchmark returns
            
            total_effect = 0.0
            
            for position in portfolio.get_active_positions():
                # Get position return
                position_return = self._get_position_return(position, portfolio_data)
                
                # Get benchmark return for this asset
                benchmark_return = self._get_asset_benchmark_return(position.asset_id, benchmark_data)
                
                # Selection effect = Portfolio Weight * (Portfolio Return - Benchmark Return)
                selection_effect = (position.weight_percentage / 100) * (position_return - benchmark_return)
                total_effect += selection_effect
            
            return total_effect
            
        except Exception as e:
            logger.error(f"Failed to calculate security selection effect: {e}")
            return 0.0
    
    def _calculate_interaction_effect(
        self, 
        portfolio: Portfolio, 
        portfolio_data: List[Dict[str, Any]], 
        benchmark_data: List[Dict[str, Any]]
    ) -> float:
        """Calculate interaction effect."""
        try:
            # Interaction effect = (Portfolio Weight - Benchmark Weight) * (Portfolio Return - Benchmark Return)
            # This captures the effect of both allocation and selection decisions
            
            total_effect = 0.0
            
            for position in portfolio.get_active_positions():
                # Get weights and returns
                portfolio_weight = position.weight_percentage / 100
                benchmark_weight = self._get_benchmark_weight(position.asset_id)
                
                portfolio_return = self._get_position_return(position, portfolio_data)
                benchmark_return = self._get_asset_benchmark_return(position.asset_id, benchmark_data)
                
                # Interaction effect
                weight_diff = portfolio_weight - benchmark_weight
                return_diff = portfolio_return - benchmark_return
                interaction_effect = weight_diff * return_diff
                
                total_effect += interaction_effect
            
            return total_effect * 100  # Convert to percentage
            
        except Exception as e:
            logger.error(f"Failed to calculate interaction effect: {e}")
            return 0.0
    
    def _calculate_position_level_attribution(
        self, 
        portfolio: Portfolio, 
        portfolio_data: List[Dict[str, Any]], 
        benchmark_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate position-level attribution."""
        try:
            attribution = {}
            
            for position in portfolio.get_active_positions():
                # Calculate individual effects
                allocation_effect = self._calculate_position_allocation_effect(position, benchmark_data)
                selection_effect = self._calculate_position_selection_effect(position, portfolio_data, benchmark_data)
                interaction_effect = self._calculate_position_interaction_effect(position, portfolio_data, benchmark_data)
                
                total_contribution = allocation_effect + selection_effect + interaction_effect
                
                attribution[position.asset_id] = {
                    'asset_id': position.asset_id,
                    'asset_name': position.asset.name,
                    'weight': position.weight_percentage,
                    'allocation_effect': allocation_effect,
                    'selection_effect': selection_effect,
                    'interaction_effect': interaction_effect,
                    'contribution': total_contribution
                }
            
            return attribution
            
        except Exception as e:
            logger.error(f"Failed to calculate position-level attribution: {e}")
            return {}
    
    def _calculate_sector_level_attribution(
        self, 
        portfolio: Portfolio, 
        portfolio_data: List[Dict[str, Any]], 
        benchmark_data: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate sector-level attribution."""
        try:
            sector_attribution = {}
            
            # Group positions by sector
            sector_positions = {}
            for position in portfolio.get_active_positions():
                sector = position.asset.sector or "Unknown"
                if sector not in sector_positions:
                    sector_positions[sector] = []
                sector_positions[sector].append(position)
            
            # Calculate attribution for each sector
            for sector, positions in sector_positions.items():
                sector_contribution = 0.0
                
                for position in positions:
                    # Calculate position contribution
                    allocation_effect = self._calculate_position_allocation_effect(position, benchmark_data)
                    selection_effect = self._calculate_position_selection_effect(position, portfolio_data, benchmark_data)
                    interaction_effect = self._calculate_position_interaction_effect(position, portfolio_data, benchmark_data)
                    
                    sector_contribution += allocation_effect + selection_effect + interaction_effect
                
                sector_attribution[sector] = sector_contribution
            
            return sector_attribution
            
        except Exception as e:
            logger.error(f"Failed to calculate sector-level attribution: {e}")
            return {}
    
    def _calculate_asset_class_level_attribution(
        self, 
        portfolio: Portfolio, 
        portfolio_data: List[Dict[str, Any]], 
        benchmark_data: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate asset class-level attribution."""
        try:
            asset_class_attribution = {}
            
            # Group positions by asset class
            asset_class_positions = {}
            for position in portfolio.get_active_positions():
                asset_class = position.asset.asset_type.value
                if asset_class not in asset_class_positions:
                    asset_class_positions[asset_class] = []
                asset_class_positions[asset_class].append(position)
            
            # Calculate attribution for each asset class
            for asset_class, positions in asset_class_positions.items():
                asset_class_contribution = 0.0
                
                for position in positions:
                    # Calculate position contribution
                    allocation_effect = self._calculate_position_allocation_effect(position, benchmark_data)
                    selection_effect = self._calculate_position_selection_effect(position, portfolio_data, benchmark_data)
                    interaction_effect = self._calculate_position_interaction_effect(position, portfolio_data, benchmark_data)
                    
                    asset_class_contribution += allocation_effect + selection_effect + interaction_effect
                
                asset_class_attribution[asset_class] = asset_class_contribution
            
            return asset_class_attribution
            
        except Exception as e:
            logger.error(f"Failed to calculate asset class-level attribution: {e}")
            return {}
    
    def _calculate_time_based_attribution(
        self, 
        portfolio: Portfolio, 
        portfolio_data: List[Dict[str, Any]], 
        benchmark_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate time-based attribution."""
        try:
            # This would analyze attribution over different time periods
            # (daily, weekly, monthly, quarterly)
            
            return {
                'daily_attribution': [],
                'weekly_attribution': [],
                'monthly_attribution': [],
                'quarterly_attribution': []
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate time-based attribution: {e}")
            return {}
    
    def _calculate_window_attribution(
        self, 
        portfolio: Portfolio, 
        portfolio_data: List[Dict[str, Any]], 
        benchmark_data: List[Dict[str, Any]]
    ) -> float:
        """Calculate attribution for a specific time window."""
        try:
            allocation_effect = self._calculate_asset_allocation_effect(portfolio, portfolio_data, benchmark_data)
            selection_effect = self._calculate_security_selection_effect(portfolio, portfolio_data, benchmark_data)
            interaction_effect = self._calculate_interaction_effect(portfolio, portfolio_data, benchmark_data)
            
            return allocation_effect + selection_effect + interaction_effect
            
        except Exception as e:
            logger.error(f"Failed to calculate window attribution: {e}")
            return 0.0
    
    # Helper methods
    def _get_default_attribution_metrics(self) -> AttributionMetrics:
        """Get default attribution metrics."""
        return AttributionMetrics(
            asset_allocation_effect=0.0,
            security_selection_effect=0.0,
            interaction_effect=0.0,
            total_attribution=0.0,
            top_contributors=[],
            bottom_contributors=[],
            sector_attribution={},
            asset_class_attribution={},
            period_start=date.today(),
            period_end=date.today()
        )
    
    async def _get_portfolio_historical_data(self, portfolio_id: str, period: str) -> List[Dict[str, Any]]:
        """Get historical portfolio data."""
        # This would query the database for historical portfolio values
        return []
    
    async def _get_benchmark_historical_data(self, period: str) -> List[Dict[str, Any]]:
        """Get historical benchmark data."""
        # This would query the database for historical benchmark values
        return []
    
    def _get_benchmark_asset_allocation(self) -> Dict[AssetType, float]:
        """Get benchmark asset allocation."""
        # This would return the benchmark's asset allocation
        return {}
    
    def _get_asset_class_return(self, asset_type: AssetType, benchmark_data: List[Dict[str, Any]]) -> float:
        """Get asset class return from benchmark data."""
        # This would calculate the return for the specific asset class
        return 0.0
    
    def _get_position_return(self, position: Position, portfolio_data: List[Dict[str, Any]]) -> float:
        """Get position return."""
        # This would calculate the return for the specific position
        return 0.0
    
    def _get_asset_benchmark_return(self, asset_id: str, benchmark_data: List[Dict[str, Any]]) -> float:
        """Get benchmark return for specific asset."""
        # This would get the benchmark return for the specific asset
        return 0.0
    
    def _get_benchmark_weight(self, asset_id: str) -> float:
        """Get benchmark weight for specific asset."""
        # This would get the benchmark weight for the specific asset
        return 0.0
    
    def _calculate_position_allocation_effect(self, position: Position, benchmark_data: List[Dict[str, Any]]) -> float:
        """Calculate allocation effect for a specific position."""
        return 0.0
    
    def _calculate_position_selection_effect(self, position: Position, portfolio_data: List[Dict[str, Any]], benchmark_data: List[Dict[str, Any]]) -> float:
        """Calculate selection effect for a specific position."""
        return 0.0
    
    def _calculate_position_interaction_effect(self, position: Position, portfolio_data: List[Dict[str, Any]], benchmark_data: List[Dict[str, Any]]) -> float:
        """Calculate interaction effect for a specific position."""
        return 0.0
    
    def _get_top_contributors(self, portfolio: Portfolio, portfolio_data: List[Dict[str, Any]], benchmark_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get top contributors to performance."""
        return []
    
    def _get_bottom_contributors(self, portfolio: Portfolio, portfolio_data: List[Dict[str, Any]], benchmark_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get bottom contributors to performance."""
        return []
    
    def _calculate_sector_attribution(self, portfolio: Portfolio, portfolio_data: List[Dict[str, Any]], benchmark_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate sector attribution."""
        return {}
    
    def _calculate_asset_class_attribution(self, portfolio: Portfolio, portfolio_data: List[Dict[str, Any]], benchmark_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate asset class attribution."""
        return {}
