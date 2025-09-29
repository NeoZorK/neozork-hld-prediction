#!/usr/bin/env python3
"""
SCHR Levels AutoML - Main CLI Entry Point

Flexible command-line interface for SCHR Levels financial analysis.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from automl.gluon.cli.main import main

if __name__ == '__main__':
    main()
