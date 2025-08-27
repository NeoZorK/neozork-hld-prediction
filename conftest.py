# -*- coding: utf-8 -*-
"""
Global pytest configuration for NeoZorK HLD Prediction project.

This file contains global pytest fixtures and configuration.
"""

import warnings
import pytest

# Suppress all warnings globally
warnings.filterwarnings("ignore")

# Configure pytest to ignore all warnings
def pytest_configure(config):
    """Configure pytest to ignore all warnings."""
    config.addinivalue_line(
        "filterwarnings",
        "ignore::DeprecationWarning"
    )
    config.addinivalue_line(
        "filterwarnings",
        "ignore::PendingDeprecationWarning"
    )
    config.addinivalue_line(
        "filterwarnings",
        "ignore::UserWarning"
    )
    config.addinivalue_line(
        "filterwarnings",
        "ignore::FutureWarning"
    )
    config.addinivalue_line(
        "filterwarnings",
        "ignore::RuntimeWarning"
    )
    # InterpolationWarning is not available in builtins, so we'll handle it differently
    pass
    # PerformanceWarning and SettingWithCopyWarning are not available in builtins
    pass

def pytest_collection_modifyitems(config, items):
    """Modify test collection to suppress warnings."""
    for item in items:
        # Add marker to suppress warnings for all tests
        item.add_marker(pytest.mark.filterwarnings("ignore"))
