# -*- coding: utf-8 -*-
# src/cli/core/argument_groups/indicator_groups.py

"""
Indicator argument groups for the argument parser.
"""

import argparse

from .config import ArgumentParserConfig


class IndicatorArgumentGroups:
    """Builder class for creating indicator argument groups."""
    
    @staticmethod
    def add_indicator_options(parser: argparse.ArgumentParser) -> None:
        """Add indicator options group."""
        indicator_group = parser.add_argument_group('Indicator Options')
        
        all_rule_choices = ArgumentParserConfig.get_all_rule_choices()
        default_rule_name = 'OHLCV'
        
        indicator_group.add_argument(
            '--rule',
            default=default_rule_name,
            help=f"Trading rule to apply. Default: {default_rule_name}. Aliases: PHLD=Predict_High_Low_Direction, PV=Pressure_Vector, SR=Support_Resistants, BB=Bollinger_Bands."
        )
        
        indicator_group.add_argument(
            '--strategy',
            metavar='LOT,RISK_REWARD,FEE',
            help="Strategy parameters: lot_size,risk_reward_ratio,fee_per_trade. Example: --strategy 1,2,0.07 means lot=1.0, risk:reward=2:1, fee=0.07%%. Default: 1.0,2.0,0.07"
        )
        
        indicator_group.add_argument(
            '--price-type', 
            metavar='TYPE',
            choices=ArgumentParserConfig.PRICE_TYPE_CHOICES,
            default='close',
            help="Price type for indicator calculation: 'open' or 'close' (default: close). Supported by all indicators with price_type parameter"
        )
