# -*- coding: utf-8 -*-
# src/cli/indicators_search.py

"""
Indicator search and information module.
Provides functionality to search and display information about available indicators.
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class IndicatorInfo:
    """Container for indicator information."""
    
    def __init__(self, name: str, category: str, description: str, 
                 usage: str, parameters: str, pros: str, cons: str, file_path: str):
        self.name = name
        self.category = category
        self.description = description
        self.usage = usage
        self.parameters = parameters
        self.pros = pros
        self.cons = cons
        self.file_path = file_path
    
    def __str__(self) -> str:
        return f"{self.name} ({self.category})"
    
    def display(self, detailed: bool = False) -> str:
        """Display indicator information."""
        if not detailed:
            return f"  {self.name:<20} - {self.description}"
        
        output = []
        output.append(f"Indicator: {self.name}")
        output.append(f"Category: {self.category}")
        output.append(f"Description: {self.description}")
        output.append(f"Usage: {self.usage}")
        output.append(f"Parameters: {self.parameters}")
        output.append(f"Pros: {self.pros}")
        output.append(f"Cons: {self.cons}")
        output.append(f"File: {self.file_path}")
        output.append("-" * 50)
        
        return "\n".join(output)


class IndicatorSearcher:
    """Searches and displays information about indicators."""
    
    def __init__(self, base_path: str = "src/calculation/indicators"):
        self.base_path = Path(base_path)
        self.indicators: Dict[str, List[IndicatorInfo]] = {}
        self._load_indicators()
    
    def _load_indicators(self) -> None:
        """Load all indicators from the indicators directory."""
        if not self.base_path.exists():
            print(f"Warning: Indicators directory not found: {self.base_path}")
            return
        
        # Define categories and their subdirectories
        categories = {
            "trend": ["ema_ind.py", "adx_ind.py", "sar_ind.py", "supertrend_ind.py"],
            "momentum": ["rsi_ind.py", "macd_ind.py", "stochoscillator_ind.py"],
            "volatility": ["bb_ind.py", "atr_ind.py", "stdev_ind.py"],
            "volume": ["obv_ind.py", "vwap_ind.py"],
            "suportresist": ["pivot_ind.py", "fiboretr_ind.py", "donchain_ind.py"],
            "oscillators": ["rsi_ind.py", "stoch_ind.py", "cci_ind.py"],
            "sentiment": ["putcallratio_ind.py", "cot_ind.py", "feargreed_ind.py"],
            "predictive": ["hma_ind.py", "tsforecast_ind.py"],
            "probability": ["montecarlo_ind.py", "kelly_ind.py"]
        }
        
        for category, files in categories.items():
            self.indicators[category] = []
            category_path = self.base_path / category
            
            if not category_path.exists():
                continue
            
            for file_name in files:
                file_path = category_path / file_name
                if file_path.exists():
                    indicator_info = self._parse_indicator_file(file_path, category)
                    if indicator_info:
                        self.indicators[category].append(indicator_info)
    
    def _parse_indicator_file(self, file_path: Path, category: str) -> Optional[IndicatorInfo]:
        """Parse indicator information from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract indicator info from docstring
            info_match = re.search(r'INDICATOR INFO:(.*?)(?=\n\n|\n[A-Z]|$)', 
                                 content, re.DOTALL | re.IGNORECASE)
            
            if not info_match:
                # Create default info for empty files
                name = file_path.stem.replace('_ind', '').upper()
                return IndicatorInfo(
                    name=name,
                    category=category,
                    description="Indicator description not available",
                    usage=f"--rule {name.lower()}",
                    parameters="Not specified",
                    pros="Not specified",
                    cons="Not specified",
                    file_path=str(file_path)
                )
            
            info_text = info_match.group(1).strip()
            
            # Parse individual fields
            name = self._extract_field(info_text, "Name", "Unknown")
            description = self._extract_field(info_text, "Description", "No description available")
            usage = self._extract_field(info_text, "Usage", f"--rule {name.lower()}")
            parameters = self._extract_field(info_text, "Parameters", "Not specified")
            pros = self._extract_field(info_text, "Pros", "Not specified")
            cons = self._extract_field(info_text, "Cons", "Not specified")
            
            return IndicatorInfo(
                name=name,
                category=category,
                description=description,
                usage=usage,
                parameters=parameters,
                pros=pros,
                cons=cons,
                file_path=str(file_path)
            )
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def _extract_field(self, text: str, field_name: str, default: str) -> str:
        """Extract a field value from indicator info text."""
        pattern = rf"{field_name}:\s*(.*?)(?=\n[A-Z][a-z]+:|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else default
    
    def list_categories(self) -> List[str]:
        """List all available categories."""
        return list(self.indicators.keys())
    
    def list_indicators(self, category: Optional[str] = None) -> List[IndicatorInfo]:
        """List indicators, optionally filtered by category."""
        if category is None:
            all_indicators = []
            for indicators in self.indicators.values():
                all_indicators.extend(indicators)
            return all_indicators
        
        return self.indicators.get(category, [])
    
    def search_indicators(self, query: str) -> List[IndicatorInfo]:
        """Search indicators by name or description."""
        query = query.lower()
        results = []
        
        for indicators in self.indicators.values():
            for indicator in indicators:
                if (query in indicator.name.lower() or 
                    query in indicator.description.lower() or
                    query in indicator.category.lower()):
                    results.append(indicator)
        
        return results
    
    def display_categories(self) -> None:
        """Display all categories with indicator counts."""
        print("Available Indicator Categories:")
        print("=" * 40)
        
        for category in sorted(self.indicators.keys()):
            count = len(self.indicators[category])
            print(f"{category:<15} - {count} indicators")
    
    def display_category(self, category: str, detailed: bool = False) -> None:
        """Display indicators in a specific category."""
        indicators = self.indicators.get(category, [])
        
        if not indicators:
            print(f"No indicators found in category: {category}")
            return
        
        print(f"\nIndicators in category '{category}':")
        print("=" * 50)
        
        for indicator in indicators:
            print(indicator.display(detailed))
    
    def display_search_results(self, query: str, detailed: bool = False) -> None:
        """Display search results."""
        results = self.search_indicators(query)
        
        if not results:
            print(f"No indicators found matching: {query}")
            return
        
        print(f"\nSearch results for '{query}':")
        print("=" * 50)
        
        for indicator in results:
            print(indicator.display(detailed))


def main():
    """Main function for indicator search CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Search and display indicator information')
    parser.add_argument('--category', type=str, help='Show indicators in specific category')
    parser.add_argument('--search', type=str, help='Search indicators by name or description')
    parser.add_argument('--detailed', action='store_true', help='Show detailed information')
    parser.add_argument('--list-categories', action='store_true', help='List all categories')
    
    args = parser.parse_args()
    
    searcher = IndicatorSearcher()
    
    if args.list_categories:
        searcher.display_categories()
    elif args.category:
        searcher.display_category(args.category, args.detailed)
    elif args.search:
        searcher.display_search_results(args.search, args.detailed)
    else:
        # Default: show all categories
        searcher.display_categories()
        print("\nUse --category <name> to see indicators in a category")
        print("Use --search <query> to search indicators")
        print("Use --detailed for more information")


if __name__ == "__main__":
    main() 