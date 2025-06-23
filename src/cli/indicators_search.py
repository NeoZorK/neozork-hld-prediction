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

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    # Fallback colors for terminals that support ANSI
    class Fore:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
    
    class Back:
        RED = '\033[101m'
        GREEN = '\033[102m'
        YELLOW = '\033[103m'
        BLUE = '\033[104m'
        MAGENTA = '\033[105m'
        CYAN = '\033[106m'
        WHITE = '\033[107m'
        RESET = '\033[0m'
    
    class Style:
        BRIGHT = '\033[1m'
        DIM = '\033[2m'
        NORMAL = '\033[22m'
        RESET_ALL = '\033[0m'
    
    COLORS_AVAILABLE = True


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
        """Display indicator information with colors."""
        if not detailed:
            return f"  {Fore.CYAN}{self.name:<20}{Style.RESET_ALL} - {self.description}"
        
        output = []
        # Header with indicator name
        output.append(f"{Fore.YELLOW}{Style.BRIGHT}📊 {self.name}{Style.RESET_ALL}")
        output.append(f"{Fore.CYAN}{'=' * (len(self.name) + 4)}{Style.RESET_ALL}")
        
        # Category
        output.append(f"{Fore.GREEN}🏷️  Category:{Style.RESET_ALL} {Fore.WHITE}{self.category.title()}{Style.RESET_ALL}")
        
        # Description
        output.append(f"{Fore.BLUE}📝 Description:{Style.RESET_ALL} {self.description}")
        
        # Usage
        output.append(f"{Fore.MAGENTA}💻 Usage:{Style.RESET_ALL} {Fore.YELLOW}{self.usage}{Style.RESET_ALL}")
        
        # Parameters
        output.append(f"{Fore.CYAN}⚙️  Parameters:{Style.RESET_ALL} {self.parameters}")
        
        # Pros
        pros_lines = self.pros.split(', ')
        pros_formatted = []
        for pro in pros_lines:
            if pro.startswith('+'):
                pros_formatted.append(f"{Fore.GREEN}✅ {pro[1:].strip()}{Style.RESET_ALL}")
            else:
                pros_formatted.append(f"{Fore.GREEN}✅ {pro.strip()}{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}👍 Pros:{Style.RESET_ALL} {', '.join(pros_formatted)}")
        
        # Cons
        cons_lines = self.cons.split(', ')
        cons_formatted = []
        for con in cons_lines:
            if con.startswith('-'):
                cons_formatted.append(f"{Fore.RED}❌ {con[1:].strip()}{Style.RESET_ALL}")
            else:
                cons_formatted.append(f"{Fore.RED}❌ {con.strip()}{Style.RESET_ALL}")
        output.append(f"{Fore.RED}👎 Cons:{Style.RESET_ALL} {', '.join(cons_formatted)}")
        
        # File path
        output.append(f"{Fore.WHITE}📁 File:{Style.RESET_ALL} {Style.DIM}{self.file_path}{Style.RESET_ALL}")
        
        # Separator
        output.append(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
        
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
            print(f"{Fore.RED}Warning: Indicators directory not found: {self.base_path}{Style.RESET_ALL}")
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

            # Extract docstring only
            docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            docstring = docstring_match.group(1) if docstring_match else ''

            # Extract indicator info from docstring
            info_match = re.search(r'INDICATOR INFO:(.*?)(?=\n\n|$)', docstring, re.DOTALL | re.IGNORECASE)

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
            name = self._extract_field(info_text, "Name", file_path.stem.replace('_ind', '').upper())
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
            print(f"{Fore.RED}Error parsing {file_path}: {e}{Style.RESET_ALL}")
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
        """Display all categories with indicator counts and names."""
        print(f"{Fore.YELLOW}{Style.BRIGHT}🎯 Available Indicator Categories:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        
        for category in sorted(self.indicators.keys()):
            indicators = self.indicators[category]
            count = len(indicators)
            emoji = self._get_category_emoji(category)
            print(f"{emoji} {Fore.GREEN}{category:<15}{Style.RESET_ALL} - {Fore.BLUE}{count} indicators{Style.RESET_ALL}")
            
            # Show indicator names in this category
            if indicators:
                indicator_names = [ind.name for ind in indicators]
                print(f"   {Fore.CYAN}└─ {', '.join(indicator_names)}{Style.RESET_ALL}")
            print()  # Add empty line for better readability
    
    def _get_category_emoji(self, category: str) -> str:
        """Get emoji for category."""
        emoji_map = {
            "trend": "📈",
            "momentum": "⚡",
            "oscillators": "🔄",
            "volatility": "📊",
            "volume": "📦",
            "suportresist": "🎯",
            "sentiment": "😊",
            "probability": "🎲",
            "predictive": "🔮"
        }
        return emoji_map.get(category, "📋")
    
    def display_category(self, category: str, detailed: bool = False) -> None:
        """Display indicators in a specific category."""
        indicators = self.indicators.get(category, [])
        
        if not indicators:
            print(f"{Fore.RED}❌ No indicators found in category: {category}{Style.RESET_ALL}")
            return
        
        emoji = self._get_category_emoji(category)
        print(f"\n{emoji} {Fore.YELLOW}{Style.BRIGHT}Indicators in category '{category}':{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        
        for indicator in indicators:
            print(indicator.display(detailed))
    
    def display_search_results(self, query: str, detailed: bool = False) -> None:
        """Display search results."""
        results = self.search_indicators(query)
        
        if not results:
            print(f"{Fore.RED}🔍 No indicators found matching: {query}{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}🔍 Search results for '{query}':{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        
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