# -*- coding: utf-8 -*-
"""
Tests for Menu System of NeoZork Interactive ML Trading Strategy Development.

This module contains tests for the menu system components.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.interactive.menu_system import InteractiveMenuSystem, DataLoadingMenu, EDAMenu

class TestInteractiveMenuSystem:
    """Test cases for InteractiveMenuSystem."""
    
    def test_menu_system_initialization(self):
        """Test menu system initialization."""
        menu_system = InteractiveMenuSystem()
        assert menu_system is not None
        assert hasattr(menu_system, 'main_menu_items')
        assert hasattr(menu_system, 'running')
    
    def test_menu_items_structure(self):
        """Test menu items structure."""
        menu_system = InteractiveMenuSystem()
        assert isinstance(menu_system.main_menu_items, dict)
        assert len(menu_system.main_menu_items) > 0
        
        # Check that all menu items have required keys
        for key, item in menu_system.main_menu_items.items():
            assert 'title' in item
            assert 'handler' in item
            assert isinstance(item['title'], str)
            assert callable(item['handler']) or item['handler'] is None

class TestDataLoadingMenu:
    """Test cases for DataLoadingMenu."""
    
    def test_data_loading_menu_initialization(self):
        """Test data loading menu initialization."""
        menu = DataLoadingMenu()
        assert menu is not None
        assert hasattr(menu, 'menu_items')
        assert isinstance(menu.menu_items, dict)

class TestEDAMenu:
    """Test cases for EDAMenu."""
    
    def test_eda_menu_initialization(self):
        """Test EDA menu initialization."""
        menu = EDAMenu()
        assert menu is not None
        assert hasattr(menu, 'menu_items')
        assert isinstance(menu.menu_items, dict)

if __name__ == "__main__":
    pytest.main([__file__])
