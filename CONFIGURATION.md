# Configuration Guide

## Overview

The Neozork HLD Prediction system uses a hierarchical configuration system that allows you to customize behavior at multiple levels.

## Configuration Sources

Configuration is loaded in the following order (later sources override earlier ones):

1. **Default Values** - Built-in sensible defaults
2. **Configuration Files** - JSON/YAML configuration files
3. **Environment Variables** - Override via environment
4. **Command Line** - Runtime configuration changes

## Configuration File

### Location
- **Default**: `config.json` in project root
- **Custom**: Specify with `--config` flag or `NEOZORK_CONFIG` environment variable

### Structure
```json
{
  "system": {
    "name": "Neozork HLD Prediction System",
    "version": "1.0.0",
    "environment": "development"
  },
  "data": {
    "cache_dir": "data/cache",
    "raw_dir": "data/raw",
    "processed_dir": "data/processed",
    "max_file_size_mb": 100,
    "supported_formats": ["csv", "json", "parquet", "xlsx"],
    "compression": {
      "enabled": true,
      "algorithm": "gzip",
      "level": 6
    }
  },
  "analysis": {
    "default_timeframe": "1H",
    "max_lookback_periods": 1000,
    "confidence_threshold": 0.8,
    "indicators": {
      "sma": {
        "default_period": 20,
        "min_period": 2,
        "max_period": 500
      },
      "rsi": {
        "default_period": 14,
        "min_period": 2,
        "max_period": 100,
        "overbought_threshold": 70,
        "oversold_threshold": 30
      }
    }
  },
  "ml": {
    "model_dir": "models",
    "default_algorithm": "random_forest",
    "cross_validation_folds": 5,
    "test_size": 0.2,
    "random_state": 42,
    "algorithms": {
      "random_forest": {
        "n_estimators": 100,
        "max_depth": 10,
        "min_samples_split": 2,
        "min_samples_leaf": 1
      }
    }
  },
  "export": {
    "default_format": "csv",
    "output_dir": "results",
    "supported_formats": ["csv", "json", "parquet", "xlsx", "html"],
    "compression": {
      "enabled": true,
      "algorithm": "gzip"
    }
  },
  "logging": {
    "level": "INFO",
    "file": "logs/system.log",
    "max_size_mb": 10,
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": {
      "console": {
        "enabled": true,
        "level": "INFO"
      },
      "file": {
        "enabled": true,
        "level": "DEBUG"
      }
    }
  },
  "cli": {
    "default_command": "help",
    "verbose": false,
    "colors": true,
    "progress_bars": true,
    "commands": {
      "analyze": {
        "default_indicators": ["sma", "rsi"],
        "max_indicators": 10
      }
    }
  },
  "performance": {
    "parallel_processing": {
      "enabled": true,
      "max_workers": "auto",
      "chunk_size": 1000
    },
    "caching": {
      "enabled": true,
      "max_size_mb": 100,
      "ttl_seconds": 3600
    },
    "memory": {
      "max_usage_mb": 1000,
      "cleanup_threshold": 0.8
    }
  },
  "security": {
    "input_validation": {
      "enabled": true,
      "strict_mode": false
    },
    "file_operations": {
      "allowed_extensions": [".csv", ".json", ".parquet", ".xlsx"],
      "max_file_size_mb": 100,
      "scan_for_malware": false
    },
    "api": {
      "rate_limiting": {
        "enabled": true,
        "requests_per_minute": 60
      },
      "authentication": {
        "required": false,
        "method": "api_key"
      }
    }
  },
  "monitoring": {
    "health_checks": {
      "enabled": true,
      "interval_seconds": 300
    },
    "metrics": {
      "enabled": true,
      "collection_interval": 60
    },
    "alerts": {
      "enabled": false,
      "email_notifications": false
    }
  },
  "development": {
    "debug_mode": true,
    "hot_reload": false,
    "test_coverage": {
      "enabled": true,
      "min_coverage": 80,
      "fail_under": true
    },
    "linting": {
      "enabled": true,
      "strict": false
    }
  }
}
```

## Environment Variables

### System Variables
```bash
# Basic configuration
export NEOZORK_ENV=production
export NEOZORK_LOG_LEVEL=WARNING
export NEOZORK_CONFIG_PATH=/path/to/config.json

# Data configuration
export NEOZORK_DATA_CACHE_DIR=/custom/cache/dir
export NEOZORK_DATA_RAW_DIR=/custom/raw/dir
export NEOZORK_DATA_MAX_FILE_SIZE_MB=500

# Analysis configuration
export NEOZORK_ANALYSIS_DEFAULT_TIMEFRAME=1D
export NEOZORK_ANALYSIS_MAX_LOOKBACK_PERIODS=2000
export NEOZORK_ANALYSIS_CONFIDENCE_THRESHOLD=0.9

# ML configuration
export NEOZORK_ML_MODEL_DIR=/custom/models/dir
export NEOZORK_ML_DEFAULT_ALGORITHM=xgboost
export NEOZORK_ML_CROSS_VALIDATION_FOLDS=10

# Performance configuration
export NEOZORK_PARALLEL_WORKERS=8
export NEOZORK_CACHE_MAX_SIZE_MB=200
export NEOZORK_MEMORY_MAX_USAGE_MB=2048

# Security configuration
export NEOZORK_SECURITY_STRICT_MODE=true
export NEOZORK_API_RATE_LIMIT=30
export NEOZORK_AUTH_REQUIRED=true
```

### Nested Configuration
```bash
# Access nested configuration
export NEOZORK_ANALYSIS_INDICATORS_SMA_DEFAULT_PERIOD=50
export NEOZORK_ANALYSIS_INDICATORS_RSI_OVERBOUGHT_THRESHOLD=80
export NEOZORK_ML_ALGORITHMS_RANDOM_FOREST_N_ESTIMATORS=200
```

## Command Line Configuration

### Global Options
```bash
# Specify configuration file
neozork --config /path/to/config.json analyze --data data.csv

# Override specific settings
neozork --config-override '{"data.cache_dir": "/tmp/cache"}' analyze --data data.csv
```

### Command-Specific Configuration
```bash
# Override analysis settings
neozork analyze --data data.csv --config-override '{"analysis.default_timeframe": "4H"}'

# Override ML settings
neozork train --model random_forest --data data.csv --config-override '{"ml.algorithms.random_forest.n_estimators": 500}'
```

## Configuration Management

### Loading Configuration
```python
from src.core.config import config

# Access configuration values
cache_dir = config.get("data.cache_dir")
timeframe = config.get("analysis.default_timeframe", "1H")
model_dir = config.get("ml.model_dir")

# Set configuration values
config.set("data.cache_dir", "/new/cache/dir")
config.set("analysis.default_timeframe", "4H")

# Save configuration
config.save()
```

### Configuration Validation
```python
from src.core.config import ConfigValidator

# Validate configuration
validator = ConfigValidator()
is_valid, errors = validator.validate(config)

if not is_valid:
    for error in errors:
        print(f"Configuration error: {error}")
```

### Configuration Templates
```python
# Create configuration template
template = {
    "development": {
        "debug_mode": True,
        "log_level": "DEBUG"
    },
    "production": {
        "debug_mode": False,
        "log_level": "WARNING"
    }
}

# Apply template based on environment
env = os.getenv("NEOZORK_ENV", "development")
config.update(template[env])
```

## Environment-Specific Configuration

### Development Environment
```json
{
  "system": {"environment": "development"},
  "development": {
    "debug_mode": true,
    "hot_reload": true,
    "test_coverage": {"enabled": true}
  },
  "logging": {"level": "DEBUG"},
  "performance": {"caching": {"enabled": false}}
}
```

### Production Environment
```json
{
  "system": {"environment": "production"},
  "development": {
    "debug_mode": false,
    "hot_reload": false,
    "test_coverage": {"enabled": false}
  },
  "logging": {"level": "WARNING"},
  "performance": {"caching": {"enabled": true}},
  "security": {"strict_mode": true}
}
```

### Testing Environment
```json
{
  "system": {"environment": "testing"},
  "development": {
    "debug_mode": false,
    "test_coverage": {"enabled": true, "fail_under": 90}
  },
  "logging": {"level": "INFO"},
  "data": {"cache_dir": "test_data/cache"}
}
```

## Dynamic Configuration

### Runtime Updates
```python
# Update configuration at runtime
config.set("analysis.default_timeframe", "1D")
config.set("ml.default_algorithm", "xgboost")

# Save changes
config.save()

# Reload configuration
config.reload()
```

### Configuration Watchers
```python
from src.core.config import ConfigWatcher

# Watch for configuration changes
watcher = ConfigWatcher(config_file_path)
watcher.on_change(lambda: config.reload())
watcher.start()
```

## Configuration Security

### Sensitive Data
```bash
# Store sensitive data in environment variables
export NEOZORK_API_KEY=your_secret_key
export NEOZORK_DB_PASSWORD=your_db_password

# Use .env file for local development
echo "NEOZORK_API_KEY=your_secret_key" > .env
echo ".env" >> .gitignore
```

### Access Control
```bash
# Restrict configuration file access
chmod 600 config.json
chown $USER:$USER config.json

# Use separate configuration for different users
cp config.json config_$USER.json
chmod 600 config_$USER.json
```

## Configuration Migration

### Version Upgrades
```python
# Migrate configuration between versions
from src.core.config import ConfigMigrator

migrator = ConfigMigrator()
migrated_config = migrator.migrate(old_config, target_version)
```

### Backup and Restore
```bash
# Backup configuration
cp config.json config.json.backup

# Restore configuration
cp config.json.backup config.json

# Compare configurations
diff config.json config.json.backup
```

## Troubleshooting

### Common Issues

#### 1. Configuration Not Loaded
```bash
# Check configuration file path
echo $NEOZORK_CONFIG_PATH

# Verify file exists and is readable
ls -la config.json
cat config.json | head -5
```

#### 2. Invalid Configuration
```bash
# Validate JSON syntax
python -m json.tool config.json

# Check for missing required fields
python -c "
import json
with open('config.json') as f:
    config = json.load(f)
print('Required fields:', list(config.keys()))
"
```

#### 3. Environment Variables Not Applied
```bash
# Check environment variables
env | grep NEOZORK

# Verify variable names
echo $NEOZORK_DATA_CACHE_DIR
echo $NEOZORK_ANALYSIS_DEFAULT_TIMEFRAME
```

### Debug Configuration
```bash
# Enable configuration debugging
export NEOZORK_CONFIG_DEBUG=true

# Run with verbose output
neozork --verbose --config-debug analyze --data data.csv

# Check configuration in Python
python -c "
from src.core.config import config
print('Current config:', config._config)
print('Config path:', config.config_path)
"
```

## Best Practices

### 1. Configuration Organization
- Group related settings together
- Use descriptive names for configuration keys
- Document all configuration options
- Provide sensible defaults

### 2. Security
- Never commit sensitive data to version control
- Use environment variables for secrets
- Restrict file permissions on configuration files
- Validate all configuration inputs

### 3. Performance
- Cache configuration values when possible
- Use lazy loading for large configuration sections
- Minimize configuration file size
- Use efficient configuration formats

### 4. Maintenance
- Version your configuration schema
- Provide migration tools for upgrades
- Document configuration changes
- Test configuration in all environments
