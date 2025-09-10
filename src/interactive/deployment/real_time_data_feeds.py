# -*- coding: utf-8 -*-
"""
Real-time Data Feeds for NeoZork Interactive ML Trading Strategy Development.

This module provides real-time data feed capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
import threading
from typing import Dict, Any, Optional, List, Tuple, Callable
import warnings

class RealTimeDataFeeds:
    """
    Real-time data feeds system.
    
    Features:
    - WebSocket Data Feeds
    - REST API Data Feeds
    - Data Aggregation
    - Data Validation
    - Performance Monitoring
    """
    
    def __init__(self):
        """Initialize the Real-time Data Feeds system."""
        self.data_feeds = {}
        self.subscribers = {}
        self.data_cache = {}
        self.performance_metrics = {}
        self.feed_threads = {}
    
    def start_data_feed(self, symbols: List[str], interval: str = "1m") -> Dict[str, Any]:
        """
        Start real-time data feed.
        
        Args:
            symbols: List of trading symbols
            interval: Data interval
            
        Returns:
            Data feed result
        """
        try:
            # Validate symbols
            if not symbols:
                return {"status": "error", "message": "No symbols provided"}
            
            # Validate interval
            valid_intervals = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]
            if interval not in valid_intervals:
                return {"status": "error", "message": f"Invalid interval: {interval}"}
            
            # Start data feed for each symbol
            feed_results = {}
            
            for symbol in symbols:
                feed_id = f"feed_{symbol}_{interval}_{int(time.time())}"
                
                # Simulate data feed
                feed_config = {
                    "feed_id": feed_id,
                    "symbol": symbol,
                    "interval": interval,
                    "status": "running",
                    "start_time": time.time(),
                    "last_update": time.time(),
                    "data_points": 0
                }
                
                self.data_feeds[feed_id] = feed_config
                feed_results[symbol] = feed_config
            
            result = {
                "status": "success",
                "feeds": feed_results,
                "n_symbols": len(symbols),
                "interval": interval,
                "message": "Data feeds started successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to start data feed: {str(e)}"}
    
    def stop_data_feed(self, feed_id: str) -> Dict[str, Any]:
        """
        Stop data feed.
        
        Args:
            feed_id: Feed ID to stop
            
        Returns:
            Stop result
        """
        try:
            if feed_id not in self.data_feeds:
                return {"status": "error", "message": f"Feed {feed_id} not found"}
            
            # Update feed status
            self.data_feeds[feed_id]["status"] = "stopped"
            self.data_feeds[feed_id]["stop_time"] = time.time()
            
            result = {
                "status": "success",
                "feed_id": feed_id,
                "message": "Data feed stopped successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to stop data feed: {str(e)}"}
    
    def get_latest_data(self, symbol: str, interval: str = "1m") -> Dict[str, Any]:
        """
        Get latest data for symbol.
        
        Args:
            symbol: Trading symbol
            interval: Data interval
            
        Returns:
            Latest data
        """
        try:
            # Simulate latest data
            current_time = time.time()
            price = 100 + np.random.randn() * 5
            volume = np.random.lognormal(10, 1)
            
            latest_data = {
                "symbol": symbol,
                "interval": interval,
                "timestamp": current_time,
                "open": price,
                "high": price * (1 + np.random.uniform(0, 0.02)),
                "low": price * (1 - np.random.uniform(0, 0.02)),
                "close": price,
                "volume": volume
            }
            
            # Cache data
            cache_key = f"{symbol}_{interval}"
            self.data_cache[cache_key] = latest_data
            
            result = {
                "status": "success",
                "data": latest_data
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get latest data: {str(e)}"}
    
    def get_historical_data(self, symbol: str, interval: str = "1m", 
                           limit: int = 100) -> Dict[str, Any]:
        """
        Get historical data for symbol.
        
        Args:
            symbol: Trading symbol
            interval: Data interval
            limit: Number of data points
            
        Returns:
            Historical data
        """
        try:
            # Simulate historical data
            timestamps = pd.date_range(end=pd.Timestamp.now(), periods=limit, freq=interval)
            prices = 100 + np.random.randn(limit).cumsum()
            volumes = np.random.lognormal(10, 1, limit)
            
            historical_data = pd.DataFrame({
                'timestamp': timestamps,
                'open': prices,
                'high': prices * (1 + np.random.uniform(0, 0.02, limit)),
                'low': prices * (1 - np.random.uniform(0, 0.02, limit)),
                'close': prices,
                'volume': volumes
            })
            
            result = {
                "status": "success",
                "symbol": symbol,
                "interval": interval,
                "data": historical_data,
                "n_points": len(historical_data)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get historical data: {str(e)}"}
    
    def subscribe_to_data(self, symbol: str, callback: Callable, 
                         interval: str = "1m") -> Dict[str, Any]:
        """
        Subscribe to real-time data updates.
        
        Args:
            symbol: Trading symbol
            callback: Callback function
            interval: Data interval
            
        Returns:
            Subscription result
        """
        try:
            subscription_id = f"sub_{symbol}_{interval}_{int(time.time())}"
            
            subscription = {
                "subscription_id": subscription_id,
                "symbol": symbol,
                "interval": interval,
                "callback": callback,
                "active": True,
                "created_time": time.time()
            }
            
            self.subscribers[subscription_id] = subscription
            
            result = {
                "status": "success",
                "subscription_id": subscription_id,
                "symbol": symbol,
                "interval": interval,
                "message": "Subscription created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to subscribe to data: {str(e)}"}
    
    def unsubscribe_from_data(self, subscription_id: str) -> Dict[str, Any]:
        """
        Unsubscribe from data updates.
        
        Args:
            subscription_id: Subscription ID
            
        Returns:
            Unsubscription result
        """
        try:
            if subscription_id not in self.subscribers:
                return {"status": "error", "message": f"Subscription {subscription_id} not found"}
            
            # Deactivate subscription
            self.subscribers[subscription_id]["active"] = False
            self.subscribers[subscription_id]["end_time"] = time.time()
            
            result = {
                "status": "success",
                "subscription_id": subscription_id,
                "message": "Unsubscribed successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to unsubscribe: {str(e)}"}
    
    def get_feed_status(self, feed_id: str = None) -> Dict[str, Any]:
        """
        Get feed status.
        
        Args:
            feed_id: Specific feed ID (None for all feeds)
            
        Returns:
            Feed status
        """
        try:
            if feed_id:
                if feed_id not in self.data_feeds:
                    return {"status": "error", "message": f"Feed {feed_id} not found"}
                
                result = {
                    "status": "success",
                    "feed": self.data_feeds[feed_id]
                }
            else:
                result = {
                    "status": "success",
                    "feeds": self.data_feeds,
                    "n_feeds": len(self.data_feeds)
                }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get feed status: {str(e)}"}
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics.
        
        Returns:
            Performance metrics
        """
        try:
            # Calculate metrics
            total_feeds = len(self.data_feeds)
            active_feeds = len([f for f in self.data_feeds.values() if f["status"] == "running"])
            total_subscribers = len(self.subscribers)
            active_subscribers = len([s for s in self.subscribers.values() if s["active"]])
            
            # Calculate data points
            total_data_points = sum(f["data_points"] for f in self.data_feeds.values())
            
            metrics = {
                "total_feeds": total_feeds,
                "active_feeds": active_feeds,
                "total_subscribers": total_subscribers,
                "active_subscribers": active_subscribers,
                "total_data_points": total_data_points,
                "cache_size": len(self.data_cache),
                "timestamp": time.time()
            }
            
            self.performance_metrics = metrics
            
            result = {
                "status": "success",
                "metrics": metrics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get performance metrics: {str(e)}"}
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data quality.
        
        Args:
            data: Data to validate
            
        Returns:
            Validation result
        """
        try:
            # Check required fields
            required_fields = ["symbol", "timestamp", "open", "high", "low", "close", "volume"]
            for field in required_fields:
                if field not in data:
                    return {"status": "error", "message": f"Missing required field: {field}"}
            
            # Validate data types and ranges
            if not isinstance(data["timestamp"], (int, float)):
                return {"status": "error", "message": "Invalid timestamp type"}
            
            if not isinstance(data["open"], (int, float)) or data["open"] <= 0:
                return {"status": "error", "message": "Invalid open price"}
            
            if not isinstance(data["high"], (int, float)) or data["high"] <= 0:
                return {"status": "error", "message": "Invalid high price"}
            
            if not isinstance(data["low"], (int, float)) or data["low"] <= 0:
                return {"status": "error", "message": "Invalid low price"}
            
            if not isinstance(data["close"], (int, float)) or data["close"] <= 0:
                return {"status": "error", "message": "Invalid close price"}
            
            if not isinstance(data["volume"], (int, float)) or data["volume"] < 0:
                return {"status": "error", "message": "Invalid volume"}
            
            # Validate price relationships
            if data["high"] < data["low"]:
                return {"status": "error", "message": "High price cannot be less than low price"}
            
            if data["high"] < data["open"] or data["high"] < data["close"]:
                return {"status": "error", "message": "High price must be >= open and close"}
            
            if data["low"] > data["open"] or data["low"] > data["close"]:
                return {"status": "error", "message": "Low price must be <= open and close"}
            
            result = {
                "status": "success",
                "validation": "passed",
                "message": "Data validation successful"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Data validation failed: {str(e)}"}
    
    def aggregate_data(self, data: List[Dict[str, Any]], 
                      aggregation_type: str = "ohlc") -> Dict[str, Any]:
        """
        Aggregate data points.
        
        Args:
            data: List of data points
            aggregation_type: Type of aggregation (ohlc, volume, etc.)
            
        Returns:
            Aggregated data
        """
        try:
            if not data:
                return {"status": "error", "message": "No data provided"}
            
            if aggregation_type == "ohlc":
                # OHLC aggregation
                aggregated = {
                    "symbol": data[0]["symbol"],
                    "timestamp": data[0]["timestamp"],
                    "open": data[0]["open"],
                    "high": max(d["high"] for d in data),
                    "low": min(d["low"] for d in data),
                    "close": data[-1]["close"],
                    "volume": sum(d["volume"] for d in data)
                }
            elif aggregation_type == "volume":
                # Volume aggregation
                aggregated = {
                    "symbol": data[0]["symbol"],
                    "timestamp": data[0]["timestamp"],
                    "total_volume": sum(d["volume"] for d in data),
                    "avg_volume": np.mean([d["volume"] for d in data]),
                    "max_volume": max(d["volume"] for d in data),
                    "min_volume": min(d["volume"] for d in data)
                }
            else:
                return {"status": "error", "message": f"Unknown aggregation type: {aggregation_type}"}
            
            result = {
                "status": "success",
                "aggregated_data": aggregated,
                "n_points": len(data),
                "aggregation_type": aggregation_type
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to aggregate data: {str(e)}"}
    
    def clear_cache(self, symbol: str = None) -> Dict[str, Any]:
        """
        Clear data cache.
        
        Args:
            symbol: Specific symbol to clear (None for all)
            
        Returns:
            Cache clear result
        """
        try:
            if symbol:
                # Clear specific symbol
                keys_to_remove = [k for k in self.data_cache.keys() if k.startswith(symbol)]
                for key in keys_to_remove:
                    del self.data_cache[key]
                
                result = {
                    "status": "success",
                    "symbol": symbol,
                    "cleared_keys": len(keys_to_remove),
                    "message": f"Cache cleared for {symbol}"
                }
            else:
                # Clear all cache
                cache_size = len(self.data_cache)
                self.data_cache.clear()
                
                result = {
                    "status": "success",
                    "cleared_keys": cache_size,
                    "message": "All cache cleared"
                }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to clear cache: {str(e)}"}
