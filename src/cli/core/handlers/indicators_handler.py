# -*- coding: utf-8 -*-
# src/cli/core/handlers/indicators_handler.py

"""
Indicators search handler for CLI.
"""

from colorama import Fore, Style

from src.cli.indicators.indicators_search import IndicatorSearcher


class IndicatorsSearchHandler:
    """Handles indicators search functionality."""
    
    @staticmethod
    def handle_indicators_search(args_list: list) -> None:
        """Handle indicators search with different argument patterns."""
        searcher = IndicatorSearcher()
        
        if not args_list:
            IndicatorsSearchHandler._display_all_categories(searcher)
        elif len(args_list) == 1:
            IndicatorsSearchHandler._handle_single_query(args_list[0], searcher)
        else:
            IndicatorsSearchHandler._handle_category_query(args_list, searcher)
    
    @staticmethod
    def _display_all_categories(searcher: IndicatorSearcher) -> None:
        """Display all available categories."""
        searcher.display_categories()
    
    @staticmethod
    def _handle_single_query(query: str, searcher: IndicatorSearcher) -> None:
        """Handle single query search."""
        if query in searcher.indicators:
            searcher.display_category(query, detailed=True)
        else:
            IndicatorsSearchHandler._search_across_categories(query, searcher)
    
    @staticmethod
    def _search_across_categories(query: str, searcher: IndicatorSearcher) -> None:
        """Search for indicators across all categories."""
        results = searcher.search_indicators(query)
        if results:
            print(f"\n{Fore.YELLOW}Search results for '{query}' across all categories:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
            for ind in results:
                print(ind.display(detailed=True))
        else:
            IndicatorsSearchHandler._display_no_results_message(query, searcher)
    
    @staticmethod
    def _display_no_results_message(query: str, searcher: IndicatorSearcher) -> None:
        """Display message when no results are found."""
        print(f"{Fore.RED}No indicators found matching: {query}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Available categories: {', '.join(searcher.list_categories())}{Style.RESET_ALL}")
    
    @staticmethod
    def _handle_category_query(args_list: list, searcher: IndicatorSearcher) -> None:
        """Handle category-specific query search."""
        category = args_list[0]
        name = ' '.join(args_list[1:])
        print(f"\n{Fore.YELLOW}Search in category '{category}' for '{name}':{Style.RESET_ALL}")
        
        results = searcher.search_indicators(name)
        filtered = [ind for ind in results if ind.category == category]
        
        if filtered:
            for ind in filtered:
                print(ind.display(detailed=True))
        else:
            print(f"No indicators found in category '{category}' matching '{name}'")
