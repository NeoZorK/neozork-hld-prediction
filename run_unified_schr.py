#!/usr/bin/env python3
"""
Unified SCHR Levels AutoML Runner
Запуск единой системы SCHR Levels AutoML

Простой интерфейс для запуска robust profitable ML-model
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from automl.unified_schr_system import UnifiedSCHRSystem, main

if __name__ == '__main__':
    main()
