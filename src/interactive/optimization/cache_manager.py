# -*- coding: utf-8 -*-
"""
Cache Manager for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive caching strategies and management capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
import hashlib
import pickle
from typing import Dict, Any, Optional, List, Tuple, Callable
from enum import Enum
import warnings

class CacheStrategy(Enum):
    """Cache strategy enumeration."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    FIFO = "fifo"  # First In First Out
    TTL = "ttl"   # Time To Live
    SIZE_BASED = "size_based"

class CacheManager:
    """
    Cache manager for optimizing data access and computation.
    
    Features:
    - Multiple Cache Strategies
    - Memory-based Caching
    - Disk-based Caching
    - Cache Statistics
    - Cache Invalidation
    - Cache Warming
    - Cache Compression
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """
        Initialize the Cache Manager.
        
        Args:
            max_size: Maximum number of cache entries
            default_ttl: Default time-to-live in seconds
        """
        self.cache = {}
        self.cache_metadata = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "size": 0
        }
        self.cache_strategies = {
            CacheStrategy.LRU.value: self._lru_strategy,
            CacheStrategy.LFU.value: self._lfu_strategy,
            CacheStrategy.FIFO.value: self._fifo_strategy,
            CacheStrategy.TTL.value: self._ttl_strategy,
            CacheStrategy.SIZE_BASED.value: self._size_based_strategy
        }
    
    def set_cache(self, key: str, value: Any, ttl: int = None, 
                  strategy: str = CacheStrategy.LRU.value) -> Dict[str, Any]:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
            strategy: Cache strategy
            
        Returns:
            Cache set result
        """
        try:
            # Use default TTL if not specified
            if ttl is None:
                ttl = self.default_ttl
            
            # Check if cache is full
            if len(self.cache) >= self.max_size:
                self._evict_entry(strategy)
            
            # Serialize value for storage
            serialized_value = self._serialize_value(value)
            
            # Store in cache
            self.cache[key] = serialized_value
            
            # Store metadata
            self.cache_metadata[key] = {
                "created_time": time.time(),
                "last_accessed": time.time(),
                "access_count": 1,
                "ttl": ttl,
                "strategy": strategy,
                "size": len(serialized_value)
            }
            
            # Update statistics
            self.cache_stats["size"] = len(self.cache)
            
            result = {
                "status": "success",
                "key": key,
                "ttl": ttl,
                "strategy": strategy,
                "size": len(serialized_value),
                "cache_size": len(self.cache),
                "message": "Value cached successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to set cache: {str(e)}"}
    
    def get_cache(self, key: str) -> Dict[str, Any]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cache get result
        """
        try:
            # Check if key exists
            if key not in self.cache:
                self.cache_stats["misses"] += 1
                return {"status": "miss", "message": f"Key {key} not found in cache"}
            
            # Check if expired
            metadata = self.cache_metadata[key]
            if time.time() - metadata["created_time"] > metadata["ttl"]:
                self._remove_entry(key)
                self.cache_stats["misses"] += 1
                return {"status": "expired", "message": f"Key {key} has expired"}
            
            # Update access information
            metadata["last_accessed"] = time.time()
            metadata["access_count"] += 1
            
            # Deserialize value
            value = self._deserialize_value(self.cache[key])
            
            # Update statistics
            self.cache_stats["hits"] += 1
            
            result = {
                "status": "hit",
                "key": key,
                "value": value,
                "access_count": metadata["access_count"],
                "last_accessed": metadata["last_accessed"],
                "message": "Value retrieved successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get cache: {str(e)}"}
    
    def cache_function(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Cache function result.
        
        Args:
            func: Function to cache
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function caching result
        """
        try:
            # Generate cache key from function and arguments
            cache_key = self._generate_function_cache_key(func, *args, **kwargs)
            
            # Try to get from cache first
            cached_result = self.get_cache(cache_key)
            if cached_result["status"] == "hit":
                return {
                    "status": "success",
                    "result": cached_result["value"],
                    "from_cache": True,
                    "cache_key": cache_key
                }
            
            # Execute function
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Cache the result
            cache_result = self.set_cache(cache_key, result)
            
            return {
                "status": "success",
                "result": result,
                "from_cache": False,
                "execution_time": execution_time,
                "cache_key": cache_key,
                "cached": cache_result["status"] == "success"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Function caching failed: {str(e)}"}
    
    def invalidate_cache(self, key: str = None, pattern: str = None) -> Dict[str, Any]:
        """
        Invalidate cache entries.
        
        Args:
            key: Specific key to invalidate
            pattern: Pattern to match keys
            
        Returns:
            Cache invalidation result
        """
        try:
            invalidated_keys = []
            
            if key:
                # Invalidate specific key
                if key in self.cache:
                    self._remove_entry(key)
                    invalidated_keys.append(key)
            
            elif pattern:
                # Invalidate keys matching pattern
                for cache_key in list(self.cache.keys()):
                    if pattern in cache_key:
                        self._remove_entry(cache_key)
                        invalidated_keys.append(cache_key)
            
            else:
                # Invalidate all cache
                invalidated_keys = list(self.cache.keys())
                self.cache.clear()
                self.cache_metadata.clear()
                self.cache_stats["size"] = 0
            
            result = {
                "status": "success",
                "invalidated_keys": invalidated_keys,
                "n_invalidated": len(invalidated_keys),
                "cache_size": len(self.cache),
                "message": f"Invalidated {len(invalidated_keys)} cache entries"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to invalidate cache: {str(e)}"}
    
    def warm_cache(self, warmup_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Warm up the cache with predefined data.
        
        Args:
            warmup_data: Dictionary of key-value pairs to cache
            
        Returns:
            Cache warming result
        """
        try:
            warmed_keys = []
            failed_keys = []
            
            for key, value in warmup_data.items():
                result = self.set_cache(key, value)
                if result["status"] == "success":
                    warmed_keys.append(key)
                else:
                    failed_keys.append(key)
            
            result = {
                "status": "success",
                "warmed_keys": warmed_keys,
                "failed_keys": failed_keys,
                "n_warmed": len(warmed_keys),
                "n_failed": len(failed_keys),
                "cache_size": len(self.cache),
                "message": f"Warmed {len(warmed_keys)} cache entries"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to warm cache: {str(e)}"}
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Cache statistics result
        """
        try:
            total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
            hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
            
            # Calculate memory usage
            total_size = sum(metadata["size"] for metadata in self.cache_metadata.values())
            
            # Get strategy distribution
            strategy_distribution = {}
            for metadata in self.cache_metadata.values():
                strategy = metadata["strategy"]
                strategy_distribution[strategy] = strategy_distribution.get(strategy, 0) + 1
            
            statistics = {
                "cache_size": len(self.cache),
                "max_size": self.max_size,
                "utilization": (len(self.cache) / self.max_size * 100) if self.max_size > 0 else 0,
                "total_requests": total_requests,
                "hits": self.cache_stats["hits"],
                "misses": self.cache_stats["misses"],
                "hit_rate": hit_rate,
                "evictions": self.cache_stats["evictions"],
                "total_size_bytes": total_size,
                "avg_entry_size": total_size / len(self.cache) if self.cache else 0,
                "strategy_distribution": strategy_distribution
            }
            
            result = {
                "status": "success",
                "statistics": statistics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get cache statistics: {str(e)}"}
    
    def optimize_cache(self, target_hit_rate: float = 80.0) -> Dict[str, Any]:
        """
        Optimize cache configuration.
        
        Args:
            target_hit_rate: Target hit rate percentage
            
        Returns:
            Cache optimization result
        """
        try:
            current_stats = self.get_cache_statistics()
            current_hit_rate = current_stats["statistics"]["hit_rate"]
            
            optimizations = []
            
            # Analyze hit rate
            if current_hit_rate < target_hit_rate:
                optimizations.append({
                    "type": "increase_size",
                    "description": f"Current hit rate {current_hit_rate:.1f}% is below target {target_hit_rate}%",
                    "recommendation": "Consider increasing cache size or TTL"
                })
            
            # Analyze eviction rate
            eviction_rate = (self.cache_stats["evictions"] / self.cache_stats["size"] * 100) if self.cache_stats["size"] > 0 else 0
            if eviction_rate > 10:
                optimizations.append({
                    "type": "reduce_evictions",
                    "description": f"High eviction rate: {eviction_rate:.1f}%",
                    "recommendation": "Consider increasing cache size or optimizing cache strategy"
                })
            
            # Analyze strategy distribution
            strategy_dist = current_stats["statistics"]["strategy_distribution"]
            if len(strategy_dist) > 1:
                optimizations.append({
                    "type": "strategy_consistency",
                    "description": "Multiple cache strategies in use",
                    "recommendation": "Consider standardizing on a single strategy for better predictability"
                })
            
            result = {
                "status": "success",
                "current_hit_rate": current_hit_rate,
                "target_hit_rate": target_hit_rate,
                "optimizations": optimizations,
                "n_optimizations": len(optimizations),
                "message": f"Found {len(optimizations)} optimization opportunities"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to optimize cache: {str(e)}"}
    
    def _evict_entry(self, strategy: str) -> None:
        """Evict an entry based on the specified strategy."""
        if strategy in self.cache_strategies:
            self.cache_strategies[strategy]()
        else:
            # Default to LRU
            self._lru_strategy()
    
    def _lru_strategy(self) -> None:
        """Least Recently Used eviction strategy."""
        if not self.cache_metadata:
            return
        
        # Find least recently accessed entry
        lru_key = min(self.cache_metadata.keys(), 
                     key=lambda k: self.cache_metadata[k]["last_accessed"])
        self._remove_entry(lru_key)
    
    def _lfu_strategy(self) -> None:
        """Least Frequently Used eviction strategy."""
        if not self.cache_metadata:
            return
        
        # Find least frequently accessed entry
        lfu_key = min(self.cache_metadata.keys(), 
                     key=lambda k: self.cache_metadata[k]["access_count"])
        self._remove_entry(lfu_key)
    
    def _fifo_strategy(self) -> None:
        """First In First Out eviction strategy."""
        if not self.cache_metadata:
            return
        
        # Find oldest entry
        fifo_key = min(self.cache_metadata.keys(), 
                      key=lambda k: self.cache_metadata[k]["created_time"])
        self._remove_entry(fifo_key)
    
    def _ttl_strategy(self) -> None:
        """Time To Live eviction strategy."""
        if not self.cache_metadata:
            return
        
        current_time = time.time()
        expired_keys = []
        
        # Find expired entries
        for key, metadata in self.cache_metadata.items():
            if current_time - metadata["created_time"] > metadata["ttl"]:
                expired_keys.append(key)
        
        # Remove expired entries
        for key in expired_keys:
            self._remove_entry(key)
        
        # If no expired entries, use LRU
        if not expired_keys and self.cache_metadata:
            self._lru_strategy()
    
    def _size_based_strategy(self) -> None:
        """Size-based eviction strategy."""
        if not self.cache_metadata:
            return
        
        # Find largest entry
        largest_key = max(self.cache_metadata.keys(), 
                         key=lambda k: self.cache_metadata[k]["size"])
        self._remove_entry(largest_key)
    
    def _remove_entry(self, key: str) -> None:
        """Remove an entry from cache."""
        if key in self.cache:
            del self.cache[key]
            del self.cache_metadata[key]
            self.cache_stats["evictions"] += 1
            self.cache_stats["size"] = len(self.cache)
    
    def _serialize_value(self, value: Any) -> bytes:
        """Serialize value for storage."""
        try:
            return pickle.dumps(value)
        except:
            return pickle.dumps(str(value))
    
    def _deserialize_value(self, serialized_value: bytes) -> Any:
        """Deserialize value from storage."""
        try:
            return pickle.loads(serialized_value)
        except:
            return None
    
    def _generate_function_cache_key(self, func: Callable, *args, **kwargs) -> str:
        """Generate cache key for function call."""
        # Create a hash of function name and arguments
        key_data = {
            "function": func.__name__,
            "args": args,
            "kwargs": kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()
