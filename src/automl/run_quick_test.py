#!/usr/bin/env python3
"""
Quick Test Runner for Unified SCHR System
Запуск быстрого теста единой системы
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from automl.quick_test import quick_test

if __name__ == "__main__":
    quick_test()
