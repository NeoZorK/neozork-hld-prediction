# -*- coding: utf-8 -*-
"""
CLI Examples Module

This module provides CLI examples organized by indicator groups.
"""

from .oscillators import OscillatorExamples
from .trend import TrendExamples
from .momentum import MomentumExamples
from .main_examples import show_all_cli_examples, show_indicator_group_examples

__all__ = [
    'OscillatorExamples',
    'TrendExamples',
    'MomentumExamples',
    'show_all_cli_examples',
    'show_indicator_group_examples'
]
