# -*- coding: utf-8 -*-
# src/cli/core/argument_groups/__init__.py

"""
Argument groups for the CLI argument parser.

This module provides organized argument groups for different
functionalities of the CLI.
"""

from .config import ArgumentParserConfig
from .basic_groups import BasicArgumentGroups
from .data_source_groups import DataSourceArgumentGroups
from .indicator_groups import IndicatorArgumentGroups
from .show_mode_groups import ShowModeArgumentGroups
from .output_groups import OutputArgumentGroups

__all__ = [
    'ArgumentParserConfig',
    'BasicArgumentGroups',
    'DataSourceArgumentGroups', 
    'IndicatorArgumentGroups',
    'ShowModeArgumentGroups',
    'OutputArgumentGroups'
]
