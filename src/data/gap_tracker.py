"""
Gap tracking system to prevent repeated downloads of known empty data periods.
This module tracks which data gaps have been checked and found to be empty,
preventing unnecessary API calls on subsequent runs.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set
import pandas as pd

from ..common.logger import print_debug, print_info


class GapTracker:
    """Tracks data gaps that have been checked and found to be empty."""
    
    def __init__(self, cache_dir: Path = None):
        """
        Initialize the gap tracker.
        
        Args:
            cache_dir: Directory to store the gap tracking file. Defaults to data/cache.
        """
        if cache_dir is None:
            cache_dir = Path("data/cache")
        
        self.cache_dir = cache_dir
        self.gap_tracker_file = cache_dir / "gap_tracker.json"
        self.checked_gaps: Dict[str, Set[Tuple[str, str]]] = {}
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing gap data
        self._load_gap_data()
    
    def _load_gap_data(self):
        """Load existing gap tracking data from file."""
        if self.gap_tracker_file.exists():
            try:
                with open(self.gap_tracker_file, 'r') as f:
                    data = json.load(f)
                    # Convert string tuples back to tuples
                    self.checked_gaps = {
                        key: {tuple(gap) for gap in gaps}
                        for key, gaps in data.items()
                    }
                print_debug(f"Loaded gap tracking data for {len(self.checked_gaps)} instruments")
            except Exception as e:
                print_debug(f"Failed to load gap tracking data: {e}")
                self.checked_gaps = {}
        else:
            self.checked_gaps = {}
    
    def _save_gap_data(self):
        """Save gap tracking data to file."""
        try:
            # Convert tuples to lists for JSON serialization
            data = {
                key: [list(gap) for gap in gaps]
                for key, gaps in self.checked_gaps.items()
            }
            
            with open(self.gap_tracker_file, 'w') as f:
                json.dump(data, f, indent=2)
            print_debug(f"Saved gap tracking data for {len(self.checked_gaps)} instruments")
        except Exception as e:
            print_debug(f"Failed to save gap tracking data: {e}")
    
    def _get_instrument_key(self, ticker: str, interval: str, source: str) -> str:
        """Generate a unique key for an instrument."""
        return f"{source}_{ticker}_{interval}"
    
    def is_gap_checked(self, ticker: str, interval: str, source: str, 
                      gap_start: pd.Timestamp, gap_end: pd.Timestamp) -> bool:
        """
        Check if a gap has already been checked and found to be empty.
        
        Args:
            ticker: Trading pair ticker
            interval: Data interval (e.g., 'M5', 'M15')
            source: Data source (e.g., 'binance', 'yfinance')
            gap_start: Start of the gap
            gap_end: End of the gap
            
        Returns:
            True if the gap has been checked and found empty, False otherwise
        """
        key = self._get_instrument_key(ticker, interval, source)
        gap_tuple = (gap_start.isoformat(), gap_end.isoformat())
        
        return gap_tuple in self.checked_gaps.get(key, set())
    
    def mark_gap_checked(self, ticker: str, interval: str, source: str,
                        gap_start: pd.Timestamp, gap_end: pd.Timestamp):
        """
        Mark a gap as checked and found to be empty.
        
        Args:
            ticker: Trading pair ticker
            interval: Data interval (e.g., 'M5', 'M15')
            source: Data source (e.g., 'binance', 'yfinance')
            gap_start: Start of the gap
            gap_end: End of the gap
        """
        key = self._get_instrument_key(ticker, interval, source)
        gap_tuple = (gap_start.isoformat(), gap_end.isoformat())
        
        if key not in self.checked_gaps:
            self.checked_gaps[key] = set()
        
        self.checked_gaps[key].add(gap_tuple)
        self._save_gap_data()
        
        print_debug(f"Marked gap as checked: {gap_start} to {gap_end} for {ticker} {interval}")
    
    def filter_checked_gaps(self, ticker: str, interval: str, source: str,
                           gaps: List[Tuple[pd.Timestamp, pd.Timestamp]]) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
        """
        Filter out gaps that have already been checked and found to be empty.
        
        Args:
            ticker: Trading pair ticker
            interval: Data interval (e.g., 'M5', 'M15')
            source: Data source (e.g., 'binance', 'yfinance')
            gaps: List of (gap_start, gap_end) tuples to filter
            
        Returns:
            List of gaps that haven't been checked yet
        """
        unchecked_gaps = []
        checked_count = 0
        
        for gap_start, gap_end in gaps:
            if self.is_gap_checked(ticker, interval, source, gap_start, gap_end):
                checked_count += 1
                print_debug(f"Skipping already checked gap: {gap_start} to {gap_end}")
            else:
                unchecked_gaps.append((gap_start, gap_end))
        
        if checked_count > 0:
            print_info(f"Skipped {checked_count} already checked gaps for {ticker} {interval}")
        
        return unchecked_gaps
    
    def mark_gaps_as_checked_from_failed_fetch(self, ticker: str, interval: str, source: str,
                                             gaps: List[Tuple[pd.Timestamp, pd.Timestamp]],
                                             fetch_results: List[bool]):
        """
        Mark gaps as checked if they failed to fetch data (indicating they're empty).
        
        Args:
            ticker: Trading pair ticker
            interval: Data interval (e.g., 'M5', 'M15')
            source: Data source (e.g., 'binance', 'yfinance')
            gaps: List of (gap_start, gap_end) tuples that were attempted
            fetch_results: List of boolean results indicating if data was fetched
        """
        print_debug(f"mark_gaps_as_checked_from_failed_fetch called with {len(gaps)} gaps and {len(fetch_results)} results")
        
        if len(gaps) != len(fetch_results):
            print_debug(f"Gap count ({len(gaps)}) doesn't match fetch results count ({len(fetch_results)}), skipping gap marking")
            return
        
        marked_count = 0
        for i, ((gap_start, gap_end), success) in enumerate(zip(gaps, fetch_results)):
            print_debug(f"Gap {i+1}: {gap_start} to {gap_end}, success: {success}")
            if not success:  # If fetch failed, mark as checked (empty)
                self.mark_gap_checked(ticker, interval, source, gap_start, gap_end)
                marked_count += 1
        
        if marked_count > 0:
            print_info(f"Marked {marked_count} failed gaps as checked for {ticker} {interval}")
        else:
            print_debug(f"No gaps marked as checked for {ticker} {interval} (all fetches succeeded)")
    
    def clear_instrument_gaps(self, ticker: str, interval: str, source: str):
        """
        Clear all checked gaps for a specific instrument.
        Useful when new data becomes available.
        
        Args:
            ticker: Trading pair ticker
            interval: Data interval (e.g., 'M5', 'M15')
            source: Data source (e.g., 'binance', 'yfinance')
        """
        key = self._get_instrument_key(ticker, interval, source)
        if key in self.checked_gaps:
            del self.checked_gaps[key]
            self._save_gap_data()
            print_info(f"Cleared checked gaps for {ticker} {interval} {source}")
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics about tracked gaps."""
        stats = {}
        for key, gaps in self.checked_gaps.items():
            stats[key] = len(gaps)
        return stats


# Global gap tracker instance
_gap_tracker = None

def get_gap_tracker(cache_dir: Path = None) -> GapTracker:
    """Get the global gap tracker instance."""
    global _gap_tracker
    if _gap_tracker is None:
        _gap_tracker = GapTracker(cache_dir)
    return _gap_tracker
