# -*- coding: utf-8 -*-
# src/data/acquisition/cache.py

"""
Data acquisition caching functionality.
Handles caching of acquired data for performance optimization.
All comments are in English.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import pandas as pd
import pickle
import hashlib
import json
from datetime import datetime, timedelta


class DataAcquisitionCache:
    """Handles caching of acquired data."""
    
    def __init__(self, cache_dir: str = 'data/cache'):
        """
        Initialize the cache module.
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_metadata_file = self.cache_dir / 'cache_metadata.json'
        self.cache_metadata = self._load_cache_metadata()
    
    def get_cached_data(self, instrument: str, start_date: Optional[str] = None, 
                       end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        Get cached data for an instrument.
        
        Args:
            instrument: Name of the instrument
            start_date: Start date for data range
            end_date: End date for data range
            
        Returns:
            Cached DataFrame or None if not found/expired
        """
        cache_key = self._generate_cache_key(instrument, start_date, end_date)
        
        if cache_key not in self.cache_metadata:
            return None
        
        cache_info = self.cache_metadata[cache_key]
        
        # Check if cache is expired
        if self._is_cache_expired(cache_info):
            self._remove_cache_entry(cache_key)
            return None
        
        # Load cached data
        cache_file = self.cache_dir / f"{cache_key}.parquet"
        if not cache_file.exists():
            self._remove_cache_entry(cache_key)
            return None
        
        try:
            cached_data = pd.read_parquet(cache_file)
            print(f"✅ Retrieved cached data for {instrument}: {len(cached_data)} rows")
            return cached_data
        except Exception as e:
            print(f"❌ Error loading cached data: {e}")
            self._remove_cache_entry(cache_key)
            return None
    
    def cache_data(self, instrument: str, data: pd.DataFrame, 
                  start_date: Optional[str] = None, end_date: Optional[str] = None,
                  ttl_hours: int = 24) -> bool:
        """
        Cache data for an instrument.
        
        Args:
            instrument: Name of the instrument
            data: DataFrame to cache
            start_date: Start date for data range
            end_date: End date for data range
            ttl_hours: Time to live in hours
            
        Returns:
            True if caching successful, False otherwise
        """
        try:
            cache_key = self._generate_cache_key(instrument, start_date, end_date)
            
            # Save data to parquet file
            cache_file = self.cache_dir / f"{cache_key}.parquet"
            data.to_parquet(cache_file, index=False)
            
            # Update metadata
            self.cache_metadata[cache_key] = {
                'instrument': instrument,
                'start_date': start_date,
                'end_date': end_date,
                'rows': len(data),
                'columns': list(data.columns),
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(hours=ttl_hours)).isoformat(),
                'file_size': cache_file.stat().st_size
            }
            
            # Save metadata
            self._save_cache_metadata()
            
            print(f"✅ Cached data for {instrument}: {len(data)} rows")
            return True
            
        except Exception as e:
            print(f"❌ Error caching data for {instrument}: {e}")
            return False
    
    def clear_cache(self, instrument: Optional[str] = None) -> bool:
        """
        Clear cache for a specific instrument or all instruments.
        
        Args:
            instrument: Name of the instrument to clear, or None for all
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if instrument is None:
                # Clear all cache
                for cache_file in self.cache_dir.glob('*.parquet'):
                    cache_file.unlink()
                self.cache_metadata.clear()
                print("✅ Cleared all cache")
            else:
                # Clear cache for specific instrument
                keys_to_remove = []
                for key, info in self.cache_metadata.items():
                    if info['instrument'] == instrument:
                        keys_to_remove.append(key)
                
                for key in keys_to_remove:
                    self._remove_cache_entry(key)
                
                print(f"✅ Cleared cache for {instrument}")
            
            self._save_cache_metadata()
            return True
            
        except Exception as e:
            print(f"❌ Error clearing cache: {e}")
            return False
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about the cache.
        
        Returns:
            Dictionary with cache information
        """
        total_size = sum(info.get('file_size', 0) for info in self.cache_metadata.values())
        total_files = len(self.cache_metadata)
        
        instruments = list(set(info['instrument'] for info in self.cache_metadata.values()))
        
        return {
            'total_files': total_files,
            'total_size_bytes': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'instruments': instruments,
            'cache_directory': str(self.cache_dir)
        }
    
    def _generate_cache_key(self, instrument: str, start_date: Optional[str], 
                           end_date: Optional[str]) -> str:
        """Generate a unique cache key."""
        key_string = f"{instrument}_{start_date or 'all'}_{end_date or 'all'}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_cache_expired(self, cache_info: Dict[str, Any]) -> bool:
        """Check if cache entry is expired."""
        expires_at = cache_info.get('expires_at')
        if not expires_at:
            return True
        
        try:
            expiry_time = datetime.fromisoformat(expires_at)
            return datetime.now() > expiry_time
        except:
            return True
    
    def _remove_cache_entry(self, cache_key: str):
        """Remove a cache entry."""
        if cache_key in self.cache_metadata:
            # Remove data file
            cache_file = self.cache_dir / f"{cache_key}.parquet"
            if cache_file.exists():
                cache_file.unlink()
            
            # Remove from metadata
            del self.cache_metadata[cache_key]
    
    def _load_cache_metadata(self) -> Dict[str, Any]:
        """Load cache metadata from file."""
        if not self.cache_metadata_file.exists():
            return {}
        
        try:
            with open(self.cache_metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading cache metadata: {e}")
            return {}
    
    def _save_cache_metadata(self):
        """Save cache metadata to file."""
        try:
            with open(self.cache_metadata_file, 'w') as f:
                json.dump(self.cache_metadata, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving cache metadata: {e}")
