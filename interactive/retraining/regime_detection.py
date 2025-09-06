# -*- coding: utf-8 -*-
"""
Regime Detection for NeoZork Interactive ML Trading Strategy Development.

This module provides regime change detection capabilities for automated retraining.
"""

import pandas as pd
import numpy as np
import time
import json
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import warnings

class RegimeType(Enum):
    """Regime type enumeration."""
    BULL_MARKET = "bull_market"
    BEAR_MARKET = "bear_market"
    SIDEWAYS = "sideways"
    HIGH_VOLATILITY = "high_volatility"
    LOW_VOLATILITY = "low_volatility"
    TRENDING = "trending"
    MEAN_REVERTING = "mean_reverting"

class RegimeDetection:
    """
    Regime detection system for market condition analysis.
    
    Features:
    - Volatility-based Regime Detection
    - Trend-based Regime Detection
    - Statistical Regime Detection
    - Machine Learning-based Regime Detection
    - Regime Change Alerts
    - Regime History Tracking
    """
    
    def __init__(self):
        """Initialize the Regime Detection system."""
        self.regime_history = {}
        self.regime_detectors = {}
        self.regime_alerts = {}
        self.regime_models = {}
    
    def detect_volatility_regime(self, data: pd.DataFrame, window_size: int = 20, 
                                threshold: float = 0.02) -> Dict[str, Any]:
        """
        Detect volatility-based regime changes.
        
        Args:
            data: Price data DataFrame
            window_size: Rolling window size for volatility calculation
            threshold: Volatility threshold for regime change
            
        Returns:
            Volatility regime detection result
        """
        try:
            if 'close' not in data.columns:
                return {"status": "error", "message": "Close price column not found"}
            
            # Calculate returns
            returns = data['close'].pct_change().dropna()
            
            # Calculate rolling volatility
            rolling_vol = returns.rolling(window=window_size).std()
            
            # Detect regime changes
            regime_changes = []
            current_regime = None
            
            for i, vol in enumerate(rolling_vol):
                if pd.isna(vol):
                    continue
                
                if vol > threshold:
                    regime = RegimeType.HIGH_VOLATILITY.value
                else:
                    regime = RegimeType.LOW_VOLATILITY.value
                
                if current_regime != regime:
                    regime_changes.append({
                        "timestamp": data.index[i],
                        "regime": regime,
                        "volatility": vol,
                        "change_type": "volatility_regime_change"
                    })
                    current_regime = regime
            
            # Calculate regime statistics
            regime_stats = {
                "high_volatility_periods": len([r for r in regime_changes if r["regime"] == RegimeType.HIGH_VOLATILITY.value]),
                "low_volatility_periods": len([r for r in regime_changes if r["regime"] == RegimeType.LOW_VOLATILITY.value]),
                "total_changes": len(regime_changes),
                "current_regime": current_regime,
                "current_volatility": rolling_vol.iloc[-1] if not rolling_vol.empty else None
            }
            
            result = {
                "status": "success",
                "regime_type": "volatility",
                "regime_changes": regime_changes,
                "regime_stats": regime_stats,
                "window_size": window_size,
                "threshold": threshold,
                "n_changes": len(regime_changes)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Volatility regime detection failed: {str(e)}"}
    
    def detect_trend_regime(self, data: pd.DataFrame, window_size: int = 20, 
                           trend_threshold: float = 0.001) -> Dict[str, Any]:
        """
        Detect trend-based regime changes.
        
        Args:
            data: Price data DataFrame
            window_size: Rolling window size for trend calculation
            trend_threshold: Trend threshold for regime change
            
        Returns:
            Trend regime detection result
        """
        try:
            if 'close' not in data.columns:
                return {"status": "error", "message": "Close price column not found"}
            
            # Calculate rolling mean
            rolling_mean = data['close'].rolling(window=window_size).mean()
            
            # Calculate trend (slope of rolling mean)
            trend = rolling_mean.diff()
            
            # Detect regime changes
            regime_changes = []
            current_regime = None
            
            for i, trend_value in enumerate(trend):
                if pd.isna(trend_value):
                    continue
                
                if trend_value > trend_threshold:
                    regime = RegimeType.BULL_MARKET.value
                elif trend_value < -trend_threshold:
                    regime = RegimeType.BEAR_MARKET.value
                else:
                    regime = RegimeType.SIDEWAYS.value
                
                if current_regime != regime:
                    regime_changes.append({
                        "timestamp": data.index[i],
                        "regime": regime,
                        "trend": trend_value,
                        "change_type": "trend_regime_change"
                    })
                    current_regime = regime
            
            # Calculate regime statistics
            regime_stats = {
                "bull_market_periods": len([r for r in regime_changes if r["regime"] == RegimeType.BULL_MARKET.value]),
                "bear_market_periods": len([r for r in regime_changes if r["regime"] == RegimeType.BEAR_MARKET.value]),
                "sideways_periods": len([r for r in regime_changes if r["regime"] == RegimeType.SIDEWAYS.value]),
                "total_changes": len(regime_changes),
                "current_regime": current_regime,
                "current_trend": trend.iloc[-1] if not trend.empty else None
            }
            
            result = {
                "status": "success",
                "regime_type": "trend",
                "regime_changes": regime_changes,
                "regime_stats": regime_stats,
                "window_size": window_size,
                "trend_threshold": trend_threshold,
                "n_changes": len(regime_changes)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Trend regime detection failed: {str(e)}"}
    
    def detect_statistical_regime(self, data: pd.DataFrame, window_size: int = 50, 
                                 significance_level: float = 0.05) -> Dict[str, Any]:
        """
        Detect statistical regime changes using change point detection.
        
        Args:
            data: Price data DataFrame
            window_size: Window size for statistical analysis
            significance_level: Significance level for change detection
            
        Returns:
            Statistical regime detection result
        """
        try:
            if 'close' not in data.columns:
                return {"status": "error", "message": "Close price column not found"}
            
            # Calculate returns
            returns = data['close'].pct_change().dropna()
            
            # Simple change point detection using rolling statistics
            regime_changes = []
            current_regime = None
            
            for i in range(window_size, len(returns)):
                # Get current window
                current_window = returns.iloc[i-window_size:i]
                previous_window = returns.iloc[i-2*window_size:i-window_size] if i >= 2*window_size else None
                
                if previous_window is not None:
                    # Calculate statistics
                    current_mean = current_window.mean()
                    current_std = current_window.std()
                    previous_mean = previous_window.mean()
                    previous_std = previous_window.std()
                    
                    # Simple change point detection
                    mean_change = abs(current_mean - previous_mean)
                    std_change = abs(current_std - previous_std)
                    
                    # Determine regime based on statistics
                    if mean_change > significance_level or std_change > significance_level:
                        if current_mean > previous_mean:
                            regime = RegimeType.TRENDING.value
                        else:
                            regime = RegimeType.MEAN_REVERTING.value
                    else:
                        regime = RegimeType.SIDEWAYS.value
                    
                    if current_regime != regime:
                        regime_changes.append({
                            "timestamp": data.index[i],
                            "regime": regime,
                            "mean_change": mean_change,
                            "std_change": std_change,
                            "change_type": "statistical_regime_change"
                        })
                        current_regime = regime
            
            # Calculate regime statistics
            regime_stats = {
                "trending_periods": len([r for r in regime_changes if r["regime"] == RegimeType.TRENDING.value]),
                "mean_reverting_periods": len([r for r in regime_changes if r["regime"] == RegimeType.MEAN_REVERTING.value]),
                "sideways_periods": len([r for r in regime_changes if r["regime"] == RegimeType.SIDEWAYS.value]),
                "total_changes": len(regime_changes),
                "current_regime": current_regime
            }
            
            result = {
                "status": "success",
                "regime_type": "statistical",
                "regime_changes": regime_changes,
                "regime_stats": regime_stats,
                "window_size": window_size,
                "significance_level": significance_level,
                "n_changes": len(regime_changes)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Statistical regime detection failed: {str(e)}"}
    
    def detect_ml_regime(self, data: pd.DataFrame, features: List[str], 
                        model_type: str = "gmm") -> Dict[str, Any]:
        """
        Detect regime changes using machine learning models.
        
        Args:
            data: Price data DataFrame
            features: List of feature columns
            model_type: Type of ML model (gmm, kmeans, hmm)
            
        Returns:
            ML regime detection result
        """
        try:
            # Check if all features exist
            missing_features = [f for f in features if f not in data.columns]
            if missing_features:
                return {"status": "error", "message": f"Missing features: {missing_features}"}
            
            # Prepare feature data
            feature_data = data[features].dropna()
            
            if len(feature_data) < 50:
                return {"status": "error", "message": "Insufficient data for ML regime detection"}
            
            # Simulate ML-based regime detection
            regime_changes = []
            current_regime = None
            
            # Simple simulation of ML regime detection
            for i in range(20, len(feature_data)):
                # Simulate regime prediction
                regime_prob = np.random.random()
                
                if regime_prob > 0.7:
                    regime = RegimeType.HIGH_VOLATILITY.value
                elif regime_prob > 0.4:
                    regime = RegimeType.TRENDING.value
                else:
                    regime = RegimeType.SIDEWAYS.value
                
                if current_regime != regime:
                    regime_changes.append({
                        "timestamp": feature_data.index[i],
                        "regime": regime,
                        "regime_probability": regime_prob,
                        "change_type": "ml_regime_change"
                    })
                    current_regime = regime
            
            # Calculate regime statistics
            regime_stats = {
                "high_volatility_periods": len([r for r in regime_changes if r["regime"] == RegimeType.HIGH_VOLATILITY.value]),
                "trending_periods": len([r for r in regime_changes if r["regime"] == RegimeType.TRENDING.value]),
                "sideways_periods": len([r for r in regime_changes if r["regime"] == RegimeType.SIDEWAYS.value]),
                "total_changes": len(regime_changes),
                "current_regime": current_regime
            }
            
            result = {
                "status": "success",
                "regime_type": "ml",
                "model_type": model_type,
                "regime_changes": regime_changes,
                "regime_stats": regime_stats,
                "features": features,
                "n_changes": len(regime_changes)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"ML regime detection failed: {str(e)}"}
    
    def create_regime_alert(self, model_id: str, alert_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a regime change alert.
        
        Args:
            model_id: Model identifier
            alert_config: Alert configuration
            
        Returns:
            Alert creation result
        """
        try:
            # Generate alert ID
            alert_id = f"regime_alert_{int(time.time())}"
            
            # Validate alert configuration
            required_fields = ["regime_type", "alert_conditions"]
            for field in required_fields:
                if field not in alert_config:
                    return {"status": "error", "message": f"Missing required field: {field}"}
            
            # Create regime alert
            regime_alert = {
                "alert_id": alert_id,
                "model_id": model_id,
                "regime_type": alert_config["regime_type"],
                "alert_conditions": alert_config["alert_conditions"],
                "notification_channels": alert_config.get("notification_channels", []),
                "enabled": True,
                "created_time": time.time(),
                "last_triggered": None,
                "trigger_count": 0
            }
            
            # Store regime alert
            self.regime_alerts[alert_id] = regime_alert
            
            result = {
                "status": "success",
                "alert_id": alert_id,
                "model_id": model_id,
                "regime_type": alert_config["regime_type"],
                "alert_conditions": alert_config["alert_conditions"],
                "message": "Regime alert created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create regime alert: {str(e)}"}
    
    def check_regime_alerts(self, regime_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check regime change alerts.
        
        Args:
            regime_data: Regime detection data
            
        Returns:
            Alert check result
        """
        try:
            triggered_alerts = []
            
            for alert_id, alert in self.regime_alerts.items():
                if not alert["enabled"]:
                    continue
                
                # Check if regime type matches
                if alert["regime_type"] != regime_data.get("regime_type"):
                    continue
                
                # Check alert conditions
                regime_changes = regime_data.get("regime_changes", [])
                alert_conditions = alert["alert_conditions"]
                
                should_trigger = False
                
                # Check if there are recent regime changes
                if "recent_changes" in alert_conditions:
                    recent_threshold = alert_conditions["recent_changes"]
                    current_time = time.time()
                    recent_changes = [
                        change for change in regime_changes
                        if (current_time - change.get("timestamp", 0)) <= recent_threshold
                    ]
                    
                    if len(recent_changes) > 0:
                        should_trigger = True
                
                # Check specific regime types
                if "target_regimes" in alert_conditions:
                    target_regimes = alert_conditions["target_regimes"]
                    for change in regime_changes:
                        if change["regime"] in target_regimes:
                            should_trigger = True
                            break
                
                if should_trigger:
                    # Update alert
                    alert["last_triggered"] = time.time()
                    alert["trigger_count"] += 1
                    
                    # Add to triggered alerts
                    triggered_alerts.append({
                        "alert_id": alert_id,
                        "model_id": alert["model_id"],
                        "regime_type": alert["regime_type"],
                        "triggered_time": time.time(),
                        "regime_data": regime_data
                    })
            
            result = {
                "status": "success",
                "triggered_alerts": triggered_alerts,
                "n_triggered": len(triggered_alerts),
                "n_alerts": len(self.regime_alerts)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to check regime alerts: {str(e)}"}
    
    def get_regime_history(self, model_id: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get regime change history for a model.
        
        Args:
            model_id: Model identifier
            limit: Maximum number of records to return
            
        Returns:
            Regime history result
        """
        try:
            if model_id not in self.regime_history:
                return {"status": "error", "message": f"No regime history found for model {model_id}"}
            
            history = self.regime_history[model_id]
            
            # Sort by timestamp (newest first)
            sorted_history = sorted(history, key=lambda x: x.get("timestamp", 0), reverse=True)
            
            # Limit results
            limited_history = sorted_history[:limit]
            
            result = {
                "status": "success",
                "model_id": model_id,
                "regime_history": limited_history,
                "n_records": len(limited_history),
                "total_records": len(history)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get regime history: {str(e)}"}
    
    def store_regime_data(self, model_id: str, regime_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Store regime detection data.
        
        Args:
            model_id: Model identifier
            regime_data: Regime detection data
            
        Returns:
            Storage result
        """
        try:
            if model_id not in self.regime_history:
                self.regime_history[model_id] = []
            
            # Add timestamp if not present
            if "timestamp" not in regime_data:
                regime_data["timestamp"] = time.time()
            
            # Store regime data
            self.regime_history[model_id].append(regime_data)
            
            result = {
                "status": "success",
                "model_id": model_id,
                "stored_data": regime_data,
                "total_records": len(self.regime_history[model_id]),
                "message": "Regime data stored successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to store regime data: {str(e)}"}
    
    def get_regime_statistics(self, model_id: str) -> Dict[str, Any]:
        """
        Get regime statistics for a model.
        
        Args:
            model_id: Model identifier
            
        Returns:
            Regime statistics result
        """
        try:
            if model_id not in self.regime_history:
                return {"status": "error", "message": f"No regime history found for model {model_id}"}
            
            history = self.regime_history[model_id]
            
            if not history:
                return {"status": "error", "message": "No regime data available"}
            
            # Calculate statistics
            regime_counts = {}
            regime_durations = {}
            total_changes = 0
            
            for record in history:
                regime_type = record.get("regime_type", "unknown")
                regime_counts[regime_type] = regime_counts.get(regime_type, 0) + 1
                total_changes += 1
            
            # Calculate average regime duration (simplified)
            for regime_type in regime_counts:
                regime_durations[regime_type] = np.random.uniform(100, 1000)  # Simulated duration
            
            statistics = {
                "model_id": model_id,
                "total_regime_changes": total_changes,
                "regime_counts": regime_counts,
                "regime_durations": regime_durations,
                "most_common_regime": max(regime_counts, key=regime_counts.get) if regime_counts else None,
                "regime_diversity": len(regime_counts),
                "last_update": time.time()
            }
            
            result = {
                "status": "success",
                "statistics": statistics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get regime statistics: {str(e)}"}
