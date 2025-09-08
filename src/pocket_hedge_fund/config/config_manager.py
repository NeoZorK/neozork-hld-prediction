"""Configuration Manager - Centralized configuration management system"""

import logging
import asyncio
import os
import json
import yaml
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)


class ConfigEnvironment(Enum):
    """Configuration environment enumeration."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class ConfigSource(Enum):
    """Configuration source enumeration."""
    FILE = "file"
    ENVIRONMENT = "environment"
    DATABASE = "database"
    API = "api"
    DEFAULT = "default"


@dataclass
class ConfigValue:
    """Configuration value data class."""
    key: str
    value: Any
    source: ConfigSource
    environment: ConfigEnvironment
    last_updated: datetime
    is_sensitive: bool = False
    description: str = ""
    validation_rules: Dict[str, Any] = None


@dataclass
class ConfigSection:
    """Configuration section data class."""
    section_name: str
    values: Dict[str, ConfigValue]
    last_updated: datetime
    is_active: bool = True


class ConfigManager:
    """Centralized configuration management system."""
    
    def __init__(self, environment: ConfigEnvironment = ConfigEnvironment.DEVELOPMENT):
        self.environment = environment
        self.config_sections: Dict[str, ConfigSection] = {}
        self.config_files: List[str] = []
        self.watchers: List[callable] = []
        self.validation_rules: Dict[str, Dict[str, Any]] = {}
        
        # Initialize default configurations
        self._initialize_default_configs()
        
    def _initialize_default_configs(self):
        """Initialize default configuration values."""
        try:
            # Database configuration
            self._add_config_section("database", {
                "host": ConfigValue(
                    key="host",
                    value="localhost",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Database host address"
                ),
                "port": ConfigValue(
                    key="port",
                    value=5432,
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Database port"
                ),
                "name": ConfigValue(
                    key="name",
                    value="neozork_fund",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Database name"
                ),
                "username": ConfigValue(
                    key="username",
                    value="postgres",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    is_sensitive=True,
                    description="Database username"
                ),
                "password": ConfigValue(
                    key="password",
                    value="",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    is_sensitive=True,
                    description="Database password"
                )
            })
            
            # API configuration
            self._add_config_section("api", {
                "host": ConfigValue(
                    key="host",
                    value="0.0.0.0",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="API server host"
                ),
                "port": ConfigValue(
                    key="port",
                    value=8000,
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="API server port"
                ),
                "debug": ConfigValue(
                    key="debug",
                    value=True if self.environment == ConfigEnvironment.DEVELOPMENT else False,
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Enable debug mode"
                ),
                "cors_origins": ConfigValue(
                    key="cors_origins",
                    value=["*"] if self.environment == ConfigEnvironment.DEVELOPMENT else [],
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="CORS allowed origins"
                )
            })
            
            # Trading configuration
            self._add_config_section("trading", {
                "max_position_size": ConfigValue(
                    key="max_position_size",
                    value=0.1,
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Maximum position size as percentage of portfolio"
                ),
                "risk_limit": ConfigValue(
                    key="risk_limit",
                    value=0.02,
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Maximum risk per trade"
                ),
                "stop_loss_percentage": ConfigValue(
                    key="stop_loss_percentage",
                    value=0.05,
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Default stop loss percentage"
                ),
                "take_profit_percentage": ConfigValue(
                    key="take_profit_percentage",
                    value=0.15,
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Default take profit percentage"
                )
            })
            
            # Blockchain configuration
            self._add_config_section("blockchain", {
                "ethereum_rpc": ConfigValue(
                    key="ethereum_rpc",
                    value="https://mainnet.infura.io/v3/your-key",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Ethereum RPC endpoint"
                ),
                "bsc_rpc": ConfigValue(
                    key="bsc_rpc",
                    value="https://bsc-dataseed.binance.org",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="BSC RPC endpoint"
                ),
                "private_key": ConfigValue(
                    key="private_key",
                    value="",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    is_sensitive=True,
                    description="Blockchain private key"
                )
            })
            
            # Logging configuration
            self._add_config_section("logging", {
                "level": ConfigValue(
                    key="level",
                    value="INFO" if self.environment == ConfigEnvironment.PRODUCTION else "DEBUG",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Logging level"
                ),
                "format": ConfigValue(
                    key="format",
                    value="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Logging format"
                ),
                "file_path": ConfigValue(
                    key="file_path",
                    value="logs/neozork_fund.log",
                    source=ConfigSource.DEFAULT,
                    environment=self.environment,
                    last_updated=datetime.now(),
                    description="Log file path"
                )
            })
            
        except Exception as e:
            logger.error(f"Failed to initialize default configs: {e}")
    
    async def load_config_from_file(self, file_path: str, config_format: str = "json") -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            if not os.path.exists(file_path):
                return {'error': f'Configuration file not found: {file_path}'}
            
            with open(file_path, 'r') as file:
                if config_format.lower() == "json":
                    config_data = json.load(file)
                elif config_format.lower() == "yaml" or config_format.lower() == "yml":
                    config_data = yaml.safe_load(file)
                else:
                    return {'error': f'Unsupported configuration format: {config_format}'}
            
            # Process configuration data
            for section_name, section_data in config_data.items():
                if isinstance(section_data, dict):
                    await self._update_config_section(section_name, section_data, ConfigSource.FILE)
            
            # Track loaded file
            self.config_files.append(file_path)
            
            logger.info(f"Loaded configuration from file: {file_path}")
            return {
                'status': 'success',
                'file_path': file_path,
                'sections_loaded': len(config_data),
                'config_data': config_data
            }
            
        except Exception as e:
            logger.error(f"Failed to load config from file: {e}")
            return {'error': str(e)}
    
    async def load_config_from_environment(self, prefix: str = "NEZORK_") -> Dict[str, Any]:
        """Load configuration from environment variables."""
        try:
            env_configs = {}
            
            for key, value in os.environ.items():
                if key.startswith(prefix):
                    # Remove prefix and convert to lowercase
                    config_key = key[len(prefix):].lower()
                    
                    # Parse nested keys (e.g., DATABASE_HOST -> database.host)
                    if '_' in config_key:
                        section, key_name = config_key.split('_', 1)
                        if section not in env_configs:
                            env_configs[section] = {}
                        env_configs[section][key_name] = value
                    else:
                        if 'general' not in env_configs:
                            env_configs['general'] = {}
                        env_configs['general'][config_key] = value
            
            # Update configuration sections
            for section_name, section_data in env_configs.items():
                await self._update_config_section(section_name, section_data, ConfigSource.ENVIRONMENT)
            
            logger.info(f"Loaded {len(env_configs)} configuration sections from environment")
            return {
                'status': 'success',
                'sections_loaded': len(env_configs),
                'env_configs': env_configs
            }
            
        except Exception as e:
            logger.error(f"Failed to load config from environment: {e}")
            return {'error': str(e)}
    
    async def get_config_value(self, section: str, key: str) -> Dict[str, Any]:
        """Get a configuration value."""
        try:
            if section not in self.config_sections:
                return {'error': f'Configuration section not found: {section}'}
            
            section_config = self.config_sections[section]
            if key not in section_config.values:
                return {'error': f'Configuration key not found: {section}.{key}'}
            
            config_value = section_config.values[key]
            
            # Return value (mask sensitive values)
            return_value = config_value.value
            if config_value.is_sensitive and self.environment == ConfigEnvironment.PRODUCTION:
                return_value = "***MASKED***"
            
            return {
                'status': 'success',
                'section': section,
                'key': key,
                'value': return_value,
                'source': config_value.source.value,
                'last_updated': config_value.last_updated,
                'is_sensitive': config_value.is_sensitive,
                'description': config_value.description
            }
            
        except Exception as e:
            logger.error(f"Failed to get config value: {e}")
            return {'error': str(e)}
    
    async def set_config_value(self, section: str, key: str, value: Any, 
                              source: ConfigSource = ConfigSource.API,
                              description: str = "", is_sensitive: bool = False) -> Dict[str, Any]:
        """Set a configuration value."""
        try:
            # Validate value
            validation_result = await self._validate_config_value(section, key, value)
            if not validation_result['valid']:
                return {'error': f'Invalid configuration value: {validation_result["error"]}'}
            
            # Create or update configuration section
            if section not in self.config_sections:
                self.config_sections[section] = ConfigSection(
                    section_name=section,
                    values={},
                    last_updated=datetime.now()
                )
            
            # Create or update configuration value
            config_value = ConfigValue(
                key=key,
                value=value,
                source=source,
                environment=self.environment,
                last_updated=datetime.now(),
                is_sensitive=is_sensitive,
                description=description
            )
            
            self.config_sections[section].values[key] = config_value
            self.config_sections[section].last_updated = datetime.now()
            
            # Notify watchers
            await self._notify_watchers(section, key, value, source)
            
            logger.info(f"Set configuration value: {section}.{key} = {value}")
            return {
                'status': 'success',
                'section': section,
                'key': key,
                'value': value,
                'source': source.value,
                'last_updated': config_value.last_updated
            }
            
        except Exception as e:
            logger.error(f"Failed to set config value: {e}")
            return {'error': str(e)}
    
    async def get_config_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section."""
        try:
            if section not in self.config_sections:
                return {'error': f'Configuration section not found: {section}'}
            
            section_config = self.config_sections[section]
            
            # Build section data
            section_data = {}
            for key, config_value in section_config.values.items():
                return_value = config_value.value
                if config_value.is_sensitive and self.environment == ConfigEnvironment.PRODUCTION:
                    return_value = "***MASKED***"
                
                section_data[key] = {
                    'value': return_value,
                    'source': config_value.source.value,
                    'last_updated': config_value.last_updated,
                    'is_sensitive': config_value.is_sensitive,
                    'description': config_value.description
                }
            
            return {
                'status': 'success',
                'section': section,
                'data': section_data,
                'last_updated': section_config.last_updated,
                'is_active': section_config.is_active
            }
            
        except Exception as e:
            logger.error(f"Failed to get config section: {e}")
            return {'error': str(e)}
    
    async def save_config_to_file(self, file_path: str, config_format: str = "json") -> Dict[str, Any]:
        """Save configuration to file."""
        try:
            # Build configuration data
            config_data = {}
            for section_name, section_config in self.config_sections.items():
                if section_config.is_active:
                    section_data = {}
                    for key, config_value in section_config.values.items():
                        # Don't save sensitive values in production
                        if config_value.is_sensitive and self.environment == ConfigEnvironment.PRODUCTION:
                            continue
                        section_data[key] = config_value.value
                    config_data[section_name] = section_data
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write to file
            with open(file_path, 'w') as file:
                if config_format.lower() == "json":
                    json.dump(config_data, file, indent=2, default=str)
                elif config_format.lower() == "yaml" or config_format.lower() == "yml":
                    yaml.dump(config_data, file, default_flow_style=False)
                else:
                    return {'error': f'Unsupported configuration format: {config_format}'}
            
            logger.info(f"Saved configuration to file: {file_path}")
            return {
                'status': 'success',
                'file_path': file_path,
                'sections_saved': len(config_data),
                'format': config_format
            }
            
        except Exception as e:
            logger.error(f"Failed to save config to file: {e}")
            return {'error': str(e)}
    
    async def add_config_watcher(self, watcher: callable) -> Dict[str, Any]:
        """Add configuration change watcher."""
        try:
            self.watchers.append(watcher)
            
            logger.info(f"Added configuration watcher: {watcher.__name__}")
            return {
                'status': 'success',
                'watcher_count': len(self.watchers)
            }
            
        except Exception as e:
            logger.error(f"Failed to add config watcher: {e}")
            return {'error': str(e)}
    
    async def reload_configuration(self) -> Dict[str, Any]:
        """Reload configuration from all sources."""
        try:
            # Reload from files
            for file_path in self.config_files:
                if os.path.exists(file_path):
                    file_ext = Path(file_path).suffix.lower()
                    config_format = "json" if file_ext == ".json" else "yaml"
                    await self.load_config_from_file(file_path, config_format)
            
            # Reload from environment
            await self.load_config_from_environment()
            
            logger.info("Reloaded configuration from all sources")
            return {
                'status': 'success',
                'sections_loaded': len(self.config_sections),
                'files_loaded': len(self.config_files)
            }
            
        except Exception as e:
            logger.error(f"Failed to reload configuration: {e}")
            return {'error': str(e)}
    
    def _add_config_section(self, section_name: str, values: Dict[str, ConfigValue]) -> None:
        """Add configuration section."""
        try:
            section = ConfigSection(
                section_name=section_name,
                values=values,
                last_updated=datetime.now()
            )
            self.config_sections[section_name] = section
            
        except Exception as e:
            logger.error(f"Failed to add config section: {e}")
    
    async def _update_config_section(self, section_name: str, section_data: Dict[str, Any], 
                                   source: ConfigSource) -> None:
        """Update configuration section with new data."""
        try:
            if section_name not in self.config_sections:
                self.config_sections[section_name] = ConfigSection(
                    section_name=section_name,
                    values={},
                    last_updated=datetime.now()
                )
            
            section = self.config_sections[section_name]
            
            for key, value in section_data.items():
                # Check if value already exists
                if key in section.values:
                    # Update existing value
                    section.values[key].value = value
                    section.values[key].source = source
                    section.values[key].last_updated = datetime.now()
                else:
                    # Create new value
                    section.values[key] = ConfigValue(
                        key=key,
                        value=value,
                        source=source,
                        environment=self.environment,
                        last_updated=datetime.now()
                    )
            
            section.last_updated = datetime.now()
            
        except Exception as e:
            logger.error(f"Failed to update config section: {e}")
    
    async def _validate_config_value(self, section: str, key: str, value: Any) -> Dict[str, Any]:
        """Validate configuration value."""
        try:
            # Get validation rules for this key
            validation_key = f"{section}.{key}"
            rules = self.validation_rules.get(validation_key, {})
            
            # Type validation
            expected_type = rules.get('type')
            if expected_type and not isinstance(value, expected_type):
                return {'valid': False, 'error': f'Expected type {expected_type}, got {type(value)}'}
            
            # Range validation
            if 'min' in rules and value < rules['min']:
                return {'valid': False, 'error': f'Value {value} is below minimum {rules["min"]}'}
            if 'max' in rules and value > rules['max']:
                return {'valid': False, 'error': f'Value {value} is above maximum {rules["max"]}'}
            
            # Enum validation
            if 'enum' in rules and value not in rules['enum']:
                return {'valid': False, 'error': f'Value {value} not in allowed values {rules["enum"]}'}
            
            # Custom validation
            if 'validator' in rules:
                validator_result = rules['validator'](value)
                if not validator_result:
                    return {'valid': False, 'error': f'Custom validation failed for value {value}'}
            
            return {'valid': True, 'error': None}
            
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    async def _notify_watchers(self, section: str, key: str, value: Any, source: ConfigSource) -> None:
        """Notify configuration watchers of changes."""
        try:
            for watcher in self.watchers:
                try:
                    if asyncio.iscoroutinefunction(watcher):
                        await watcher(section, key, value, source)
                    else:
                        watcher(section, key, value, source)
                except Exception as e:
                    logger.error(f"Configuration watcher error: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to notify watchers: {e}")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration system summary."""
        total_sections = len(self.config_sections)
        total_values = sum(len(section.values) for section in self.config_sections.values())
        sensitive_values = sum(
            len([v for v in section.values.values() if v.is_sensitive])
            for section in self.config_sections.values()
        )
        
        return {
            'environment': self.environment.value,
            'total_sections': total_sections,
            'total_values': total_values,
            'sensitive_values': sensitive_values,
            'config_files': len(self.config_files),
            'watchers': len(self.watchers),
            'validation_rules': len(self.validation_rules)
        }
