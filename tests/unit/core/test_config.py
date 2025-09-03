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
        assert config.get("data.batch_size") == 1000
    
    def test_config_initialization_with_dict(self):
        """Test Config initialization with custom dictionary."""
        custom_config = {
            "logging": {"level": "DEBUG"},
            "custom": {"value": 42}
        }
        config = Config(custom_config)
        assert config.get("logging.level") == "DEBUG"
        assert config.get("custom.value") == 42
    
    def test_config_get_nested_value(self):
        """Test getting nested configuration values."""
        config = Config()
        # Test existing nested value
        assert config.get("data.validation.check_duplicates") is True
        
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
            config = Config()
            config.load_from_file(temp_file)
            assert config.get("test_section.test_key") == "test_value"
        finally:
            os.unlink(temp_file)
    
    def test_config_load_from_nonexistent_file(self):
        """Test loading from non-existent file raises error."""
        config = Config()
        with pytest.raises(ConfigurationError):
            config.load_from_file("nonexistent.json")
    
    def test_config_save_to_file(self):
        """Test saving configuration to file."""
        config = Config()
        config.set("test.save", "save_value")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            config.save_to_file(temp_file)
            
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
        
        config.update_from_dict(update_dict)
        
        assert config.get("logging.level") == "ERROR"
        assert config.get("new_section.new_key") == "new_value"
        # Other values should remain unchanged
        assert config.get("data.batch_size") == 1000


__all__ = ["TestConfig"]
