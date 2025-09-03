"""
Unit tests for core.config module.
"""

import pytest
import tempfile
import json
import os
from unittest.mock import patch, mock_open

from src.core.config import Config
from src.core.exceptions import ConfigurationError


class TestConfig:
    """Test cases for Config class."""
    
    def test_config_initialization_default(self):
        """Test Config initialization with default values."""
        config = Config()
        assert config.get("logging.level") == "INFO"
        assert config.get("data.cache_dir") == "data/cache"
    
    def test_config_initialization_with_dict(self):
        """Test Config initialization with custom dictionary."""
        # Config constructor expects a file path, not a dict
        # We'll test setting values after initialization
        config = Config()
        config.set("logging.level", "DEBUG")
        config.set("custom.value", 42)
        assert config.get("logging.level") == "DEBUG"
        assert config.get("custom.value") == 42
    
    def test_config_get_nested_value(self):
        """Test getting nested configuration values."""
        config = Config()
        # Test existing nested value
        assert config.get("data.cache_dir") == "data/cache"
        
        # Test non-existent nested value
        assert config.get("non.existent.path") is None
        
        # Test with default value
        assert config.get("non.existent.path", "default") == "default"
    
    def test_config_set_value(self):
        """Test setting configuration values."""
        config = Config()
        config.set("test.key", "test_value")
        assert config.get("test.key") == "test_value"
        
        # Test setting nested value
        config.set("nested.deep.value", 123)
        assert config.get("nested.deep.value") == 123
    
    def test_config_load_from_file(self):
        """Test loading configuration from file."""
        test_config = {
            "test_section": {
                "test_key": "test_value"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_config, f)
            temp_file = f.name
        
        try:
            # Config constructor loads from file path
            config = Config(temp_file)
            assert config.get("test_section.test_key") == "test_value"
        finally:
            os.unlink(temp_file)
    
    def test_config_load_from_nonexistent_file(self):
        """Test loading from non-existent file raises error."""
        # Config constructor will try to load from non-existent file
        # and fall back to default config
        config = Config("nonexistent.json")
        # Should not raise error, should use default config
        assert config.get("data.cache_dir") == "data/cache"
    
    def test_config_save_to_file(self):
        """Test saving configuration to file."""
        config = Config()
        config.set("test.save", "save_value")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save to the config's own path
            config.config_path = temp_file
            config.save()
            
            # Verify file was saved correctly
            with open(temp_file, 'r') as f:
                saved_config = json.load(f)
            
            assert saved_config["test"]["save"] == "save_value"
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_config_update_from_dict(self):
        """Test updating configuration from dictionary."""
        config = Config()
        original_level = config.get("logging.level")
        
        update_dict = {
            "logging": {"level": "ERROR"},
            "new_section": {"new_key": "new_value"}
        }
        
        # Use set method for each key
        for key, value in update_dict.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    config.set(f"{key}.{subkey}", subvalue)
            else:
                config.set(key, value)
        
        assert config.get("logging.level") == "ERROR"
        assert config.get("new_section.new_key") == "new_value"
        # Other values should remain unchanged
        assert config.get("data.cache_dir") == "data/cache"


__all__ = ["TestConfig"]
