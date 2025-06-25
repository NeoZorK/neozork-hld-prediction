# -*- coding: utf-8 -*-
# src/cli/interactive_mode.py

"""
Interactive mode for guided indicator selection and analysis.
Provides a user-friendly interface for selecting indicators and running analysis.
"""

import sys
import os
from typing import List, Dict, Optional, Tuple
from colorama import Fore, Style, init
from src.cli.indicators_search import IndicatorSearcher

# Initialize colorama
init(autoreset=True)


class InteractiveMode:
    """Interactive mode for guided indicator selection and analysis."""
    
    def __init__(self):
        self.searcher = IndicatorSearcher()
        self.categories = self.searcher.list_categories()
        self.current_selection = {
            'mode': None,
            'indicator': None,
            'data_source': None,
            'ticker': None,
            'interval': 'D1',
            'point': None,
            'period': None,
            'start_date': None,
            'end_date': None,
            'draw_method': 'fastest',
            'export_formats': []
        }
    
    def start(self):
        """Start the interactive mode."""
        self._print_welcome()
        
        while True:
            try:
                self._show_main_menu()
                choice = self._get_user_choice()
                
                if choice == '1':
                    self._select_mode()
                elif choice == '2':
                    self._select_indicator()
                elif choice == '3':
                    self._configure_data_source()
                elif choice == '4':
                    self._configure_plotting()
                elif choice == '5':
                    self._configure_export()
                elif choice == '6':
                    self._show_current_configuration()
                elif choice == '7':
                    self._run_analysis()
                elif choice == '8':
                    self._show_help()
                elif choice == '9':
                    self._list_indicators()
                elif choice == '10':
                    self._show_trading_metrics_encyclopedia()
                elif choice == '0':
                    print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                    break
                else:
                    print(f"\n{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Interactive mode interrupted. Exiting...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
    
    def _print_welcome(self):
        """Print welcome message."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Interactive Mode ==={Style.RESET_ALL}")
        print("Welcome to the Interactive Indicator Analysis Tool!")
        print("This mode will guide you through selecting indicators and configuring analysis.")
        print("Use the menu below to navigate through the options.\n")
    
    def _show_main_menu(self):
        """Show the main menu."""
        print(f"{Fore.YELLOW}{Style.BRIGHT}Main Menu:{Style.RESET_ALL}")
        print("1. Select Analysis Mode")
        print("2. Select Indicator")
        print("3. Configure Data Source")
        print("4. Configure Plotting")
        print("5. Configure Export")
        print("6. Show Current Configuration")
        print("7. Run Analysis")
        print("8. Help")
        print("9. List Available Indicators")
        print("10. Trading Metrics Encyclopedia")
        print("0. Exit")
        print()
    
    def _get_user_choice(self) -> str:
        """Get user choice from input."""
        return input(f"{Fore.GREEN}Enter your choice (0-10): {Style.RESET_ALL}").strip()
    
    def _select_mode(self):
        """Select analysis mode."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Select Analysis Mode:{Style.RESET_ALL}")
        modes = [
            ('demo', 'Demo data (for testing)'),
            ('csv', 'CSV file'),
            ('yfinance', 'Yahoo Finance'),
            ('polygon', 'Polygon.io'),
            ('binance', 'Binance'),
            ('exrate', 'Exchange Rate API'),
            ('show', 'Show cached data')
        ]
        
        for i, (mode, description) in enumerate(modes, 1):
            print(f"{i}. {mode} - {description}")
        
        choice = input(f"\n{Fore.GREEN}Select mode (1-{len(modes)}): {Style.RESET_ALL}").strip()
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(modes):
                self.current_selection['mode'] = modes[choice_idx][0]
                print(f"{Fore.GREEN}Selected mode: {self.current_selection['mode']}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    def _select_indicator(self):
        """Select indicator."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Select Indicator:{Style.RESET_ALL}")
        
        # Show categories
        print("Available categories:")
        for i, category in enumerate(self.categories, 1):
            indicators = self.searcher.list_indicators(category)
            print(f"{i}. {category} ({len(indicators)} indicators)")
        
        # Get category choice
        category_choice = input(f"\n{Fore.GREEN}Select category (1-{len(self.categories)}): {Style.RESET_ALL}").strip()
        
        try:
            category_idx = int(category_choice) - 1
            if 0 <= category_idx < len(self.categories):
                category = self.categories[category_idx]
                indicators = self.searcher.list_indicators(category)
                
                print(f"\nIndicators in {category}:")
                for i, indicator in enumerate(indicators, 1):
                    print(f"{i}. {indicator.name} - {indicator.description}")
                
                # Get indicator choice
                indicator_choice = input(f"\n{Fore.GREEN}Select indicator (1-{len(indicators)}): {Style.RESET_ALL}").strip()
                
                try:
                    indicator_idx = int(indicator_choice) - 1
                    if 0 <= indicator_idx < len(indicators):
                        self.current_selection['indicator'] = indicators[indicator_idx]
                        print(f"{Fore.GREEN}Selected indicator: {self.current_selection['indicator'].name}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    def _configure_data_source(self):
        """Configure data source parameters."""
        if not self.current_selection['mode']:
            print(f"{Fore.RED}Please select a mode first.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Configure Data Source:{Style.RESET_ALL}")
        
        # Configure based on mode
        if self.current_selection['mode'] == 'csv':
            self._configure_csv_source()
        elif self.current_selection['mode'] in ['yfinance', 'polygon', 'binance', 'exrate']:
            self._configure_api_source()
        elif self.current_selection['mode'] == 'show':
            self._configure_show_source()
        else:
            print(f"{Fore.GREEN}No additional configuration needed for {self.current_selection['mode']} mode.{Style.RESET_ALL}")
    
    def _configure_csv_source(self):
        """Configure CSV data source."""
        csv_file = input(f"{Fore.GREEN}Enter CSV file path: {Style.RESET_ALL}").strip()
        if csv_file:
            self.current_selection['data_source'] = csv_file
        
        point = input(f"{Fore.GREEN}Enter point size (e.g., 0.01): {Style.RESET_ALL}").strip()
        if point:
            try:
                self.current_selection['point'] = float(point)
            except ValueError:
                print(f"{Fore.RED}Invalid point size.{Style.RESET_ALL}")
    
    def _configure_api_source(self):
        """Configure API data source."""
        ticker = input(f"{Fore.GREEN}Enter ticker symbol: {Style.RESET_ALL}").strip()
        if ticker:
            self.current_selection['ticker'] = ticker
        
        interval = input(f"{Fore.GREEN}Enter interval (D1/H1/M1/W1/MN1) [D1]: {Style.RESET_ALL}").strip()
        if interval:
            self.current_selection['interval'] = interval
        
        point = input(f"{Fore.GREEN}Enter point size (e.g., 0.01): {Style.RESET_ALL}").strip()
        if point:
            try:
                self.current_selection['point'] = float(point)
            except ValueError:
                print(f"{Fore.RED}Invalid point size.{Style.RESET_ALL}")
        
        # Configure date range
        use_period = input(f"{Fore.GREEN}Use period instead of date range? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if use_period == 'y':
            period = input(f"{Fore.GREEN}Enter period (e.g., 1mo, 1y): {Style.RESET_ALL}").strip()
            if period:
                self.current_selection['period'] = period
        else:
            start_date = input(f"{Fore.GREEN}Enter start date (YYYY-MM-DD): {Style.RESET_ALL}").strip()
            if start_date:
                self.current_selection['start_date'] = start_date
            
            end_date = input(f"{Fore.GREEN}Enter end date (YYYY-MM-DD): {Style.RESET_ALL}").strip()
            if end_date:
                self.current_selection['end_date'] = end_date
    
    def _configure_show_source(self):
        """Configure show mode source."""
        sources = ['yfinance', 'csv', 'polygon', 'binance', 'exrate', 'ind']
        print("Available sources:")
        for i, source in enumerate(sources, 1):
            print(f"{i}. {source}")
        
        choice = input(f"\n{Fore.GREEN}Select source (1-{len(sources)}): {Style.RESET_ALL}").strip()
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(sources):
                self.current_selection['data_source'] = sources[choice_idx]
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    def _configure_plotting(self):
        """Configure plotting options."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Configure Plotting:{Style.RESET_ALL}")
        
        methods = [
            ('fastest', 'Fastest plotting (default)'),
            ('fast', 'Fast plotting'),
            ('plotly', 'Interactive Plotly'),
            ('mplfinance', 'Matplotlib Finance'),
            ('seaborn', 'Seaborn'),
            ('term', 'Terminal plotting')
        ]
        
        for i, (method, description) in enumerate(methods, 1):
            print(f"{i}. {method} - {description}")
        
        choice = input(f"\n{Fore.GREEN}Select plotting method (1-{len(methods)}): {Style.RESET_ALL}").strip()
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(methods):
                self.current_selection['draw_method'] = methods[choice_idx][0]
                print(f"{Fore.GREEN}Selected method: {self.current_selection['draw_method']}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    def _configure_export(self):
        """Configure export options."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Configure Export:{Style.RESET_ALL}")
        
        formats = ['parquet', 'csv', 'json', 'indicators_info']
        self.current_selection['export_formats'] = []
        
        for fmt in formats:
            choice = input(f"{Fore.GREEN}Export to {fmt}? (y/n): {Style.RESET_ALL}").strip().lower()
            if choice == 'y':
                self.current_selection['export_formats'].append(fmt)
        
        if self.current_selection['export_formats']:
            print(f"{Fore.GREEN}Selected formats: {', '.join(self.current_selection['export_formats'])}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No export formats selected.{Style.RESET_ALL}")
    
    def _show_current_configuration(self):
        """Show current configuration."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Current Configuration:{Style.RESET_ALL}")
        
        for key, value in self.current_selection.items():
            if key == 'indicator' and value:
                print(f"{key}: {value.name} ({value.category})")
            elif key == 'export_formats':
                print(f"{key}: {', '.join(value) if value else 'None'}")
            else:
                print(f"{key}: {value}")
    
    def _run_analysis(self):
        """Run the analysis with current configuration."""
        if not self.current_selection['mode']:
            print(f"{Fore.RED}Please select a mode first.{Style.RESET_ALL}")
            return
        
        if not self.current_selection['indicator']:
            print(f"{Fore.RED}Please select an indicator first.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Running Analysis...{Style.RESET_ALL}")
        
        # Build command arguments
        args = [self.current_selection['mode']]
        
        # Add indicator rule
        if self.current_selection['indicator']:
            args.extend(['--rule', self.current_selection['indicator'].name])
        
        # Add data source specific arguments
        if self.current_selection['mode'] == 'csv':
            if self.current_selection['data_source']:
                args.extend(['--csv-file', self.current_selection['data_source']])
            if self.current_selection['point']:
                args.extend(['--point', str(self.current_selection['point'])])
        elif self.current_selection['mode'] in ['yfinance', 'polygon', 'binance', 'exrate']:
            if self.current_selection['ticker']:
                args.extend(['--ticker', self.current_selection['ticker']])
            if self.current_selection['interval']:
                args.extend(['--interval', self.current_selection['interval']])
            if self.current_selection['point']:
                args.extend(['--point', str(self.current_selection['point'])])
            if self.current_selection['period']:
                args.extend(['--period', self.current_selection['period']])
            elif self.current_selection['start_date'] and self.current_selection['end_date']:
                args.extend(['--start', self.current_selection['start_date']])
                args.extend(['--end', self.current_selection['end_date']])
        elif self.current_selection['mode'] == 'show':
            if self.current_selection['data_source']:
                args.append(self.current_selection['data_source'])
        
        # Add plotting method
        if self.current_selection['draw_method']:
            args.extend(['--draw', self.current_selection['draw_method']])
        
        # Add export formats
        for fmt in self.current_selection['export_formats']:
            if fmt == 'indicators_info':
                args.append('--export-indicators-info')
            else:
                args.append(f'--export-{fmt}')
        
        print(f"Command: python run_analysis.py {' '.join(args)}")
        
        # Ask for confirmation
        confirm = input(f"\n{Fore.GREEN}Run this analysis? (y/n): {Style.RESET_ALL}").strip().lower()
        if confirm == 'y':
            try:
                # Import and run the main analysis function
                from run_analysis import main
                # Set sys.argv to our arguments
                original_argv = sys.argv
                sys.argv = ['run_analysis.py'] + args
                main()
                sys.argv = original_argv
                print(f"\n{Fore.GREEN}Analysis completed successfully!{Style.RESET_ALL}")
            except Exception as e:
                print(f"\n{Fore.RED}Error running analysis: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Analysis cancelled.{Style.RESET_ALL}")
    
    def _show_help(self):
        """Show help information."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Interactive Mode Help:{Style.RESET_ALL}")
        print("This interactive mode guides you through the analysis process:")
        print("1. Select Analysis Mode - Choose how to get your data")
        print("2. Select Indicator - Choose which indicator to calculate")
        print("3. Configure Data Source - Set up data source parameters")
        print("4. Configure Plotting - Choose how to visualize results")
        print("5. Configure Export - Choose export formats")
        print("6. Show Current Configuration - Review your settings")
        print("7. Run Analysis - Execute the analysis")
        print("8. Help - Show this help")
        print("9. List Available Indicators - Browse available indicators")
        print("10. Trading Metrics Encyclopedia - Explore trading metrics and strategy tips")
        print("0. Exit - Leave interactive mode")
        print()
        print("You can also use the regular CLI mode:")
        print("python run_analysis.py --help")
        print("python run_analysis.py --examples")
        print("python run_analysis.py --indicators")
        print("python run_analysis.py --metric")
    
    def _list_indicators(self):
        """List available indicators with detailed information."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Available Indicators:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        
        # Show categories with indicator counts
        print(f"{Fore.YELLOW}{Style.BRIGHT}🎯 Available Indicator Categories:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        
        for category in sorted(self.categories):
            indicators = self.searcher.list_indicators(category)
            count = len(indicators)
            emoji = self.searcher._get_category_emoji(category)
            print(f"{emoji} {Fore.GREEN}{category:<15}{Style.RESET_ALL} - {Fore.BLUE}{count} indicators{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}📋 Detailed Indicator List:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        
        # Show detailed list of indicators by category
        for category in sorted(self.categories):
            indicators = self.searcher.list_indicators(category)
            if indicators:
                emoji = self.searcher._get_category_emoji(category)
                print(f"\n{emoji} {Fore.YELLOW}{Style.BRIGHT}{category.title()} Indicators:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'─' * 40}{Style.RESET_ALL}")
                
                for i, indicator in enumerate(indicators, 1):
                    print(f"  {i:2d}. {Fore.CYAN}{indicator.name:<20}{Style.RESET_ALL} - {indicator.description}")
        
        print(f"\n{Fore.GREEN}💡 Tip: Use option 2 to select a specific indicator for analysis.{Style.RESET_ALL}")

    def _show_trading_metrics_encyclopedia(self):
        """Show trading metrics encyclopedia."""
        from src.cli.quant_encyclopedia import QuantEncyclopedia
        
        encyclopedia = QuantEncyclopedia()
        
        while True:
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}Trading Metrics Encyclopedia:{Style.RESET_ALL}")
            print("1. Show All Metrics")
            print("2. Show All Tips")
            print("3. Search Metrics")
            print("4. Search Tips")
            print("5. Back to Main Menu")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice (1-5): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
                encyclopedia.show_all_metrics()
                print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            elif choice == '2':
                print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
                encyclopedia.show_all_tips()
                print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            elif choice == '3':
                search_term = input(f"{Fore.GREEN}Enter search term for metrics: {Style.RESET_ALL}").strip()
                if search_term:
                    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
                    encyclopedia.show_all_metrics(search_term)
                    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            elif choice == '4':
                search_term = input(f"{Fore.GREEN}Enter search term for tips: {Style.RESET_ALL}").strip()
                if search_term:
                    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
                    encyclopedia.show_all_tips(search_term)
                    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            elif choice == '5':
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")


def start_interactive_mode():
    """Start the interactive mode."""
    interactive = InteractiveMode()
    interactive.start() 