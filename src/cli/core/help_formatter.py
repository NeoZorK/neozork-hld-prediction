# -*- coding: utf-8 -*-
# src/cli/core/help_formatter.py

"""
Custom help formatter for CLI with colored output and improved formatting.
"""

import argparse
import textwrap
from colorama import Fore, Style


class ColoredHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """Custom help formatter that adds color to the help output and improves text alignment."""

    def __init__(self, prog):
        # Set consistent width and max_help_position for better alignment with larger indent
        super().__init__(prog, width=200, max_help_position=50, indent_increment=4)

    def _format_action_invocation(self, action):
        """Format the action invocation (e.g. -h, --help) with color."""
        if action.option_strings:
            parts = []
            for option_string in action.option_strings:
                parts.append(f"{Fore.GREEN}{option_string}{Style.RESET_ALL}")
            return ', '.join(parts)
        else:
            return super()._format_action_invocation(action)

    def _format_usage(self, usage, actions, groups, prefix):
        """Format usage with colors."""
        if prefix is None:
            prefix = f"{Fore.YELLOW}usage: {Style.RESET_ALL}"
        return super()._format_usage(usage, actions, groups, prefix)

    def _format_args(self, action, default_metavar):
        """Format args with colors."""
        result = super()._format_args(action, default_metavar)
        return f"{Fore.CYAN}{result}{Style.RESET_ALL}"

    def _get_help_string(self, action):
        """Format help string with colors and better text wrapping."""
        help_text = super()._get_help_string(action)
        if action.default != argparse.SUPPRESS and action.default is not None:
            defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
            if action.option_strings or action.nargs in defaulting_nargs:
                help_text = help_text.replace(f"(default: {action.default})",
                                           f"({Fore.MAGENTA}default: {action.default}{Style.RESET_ALL})")
        return help_text

    def _split_lines(self, text, width):
        """Override to improve text wrapping with consistent indentation."""
        if len(text) <= width:
            return [text]
        
        # Split long lines more intelligently with larger indent
        lines = []
        for line in text.splitlines():
            if len(line) <= width:
                lines.append(line)
            else:
                wrapped = textwrap.fill(line, width, 
                                      break_long_words=False, 
                                      break_on_hyphens=False,
                                      subsequent_indent='                            ')
                lines.extend(wrapped.splitlines())
        return lines

    def _format_action(self, action):
        """Override to add larger consistent indentation for all help items."""
        # Get the original formatted action
        help_text = super()._format_action(action)
        
        # Add extra indentation to all lines (4 more spaces)
        lines = help_text.split('\n')
        indented_lines = []
        for i, line in enumerate(lines):
            if line.strip():  # Only indent non-empty lines
                if i == 0 or line.startswith('  '):  # First line or already indented
                    indented_lines.append('    ' + line)
                else:
                    indented_lines.append(line)
            else:
                indented_lines.append(line)
        
        return '\n'.join(indented_lines)

    def start_section(self, heading):
        """Format section headings with colors."""
        heading = f"{Fore.YELLOW}{Style.BRIGHT}{heading}{Style.RESET_ALL}"
        super().start_section(heading)
