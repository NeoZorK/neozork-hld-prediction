# UV Setup and Management

This directory contains scripts and tools for managing the Python development environment using `uv`, a fast Python package manager.

## Overview

`uv` is a modern Python package manager that provides:
- Fast dependency resolution
- Lock file management
- Virtual environment management
- Integration with `pyproject.toml`
- Binary package optimization

## Scripts

### 1. `setup_uv.sh` - Initial Setup
**Purpose**: Installs `uv` and sets up the development environment

**Features**:
- Automatic `uv` installation for macOS and Linux
- Python version compatibility checking
- Virtual environment creation
- Dependency installation from `pyproject.toml`
- Pre-commit hooks setup
- Lock file generation

**Usage**:
```bash
./uv_setup/setup_uv.sh
```

**What it does**:
1. Checks Python version compatibility (3.8-3.12)
2. Installs `uv` if not present
3. Creates virtual environment in `.venv/`
4. Installs project dependencies with `[dev]` extras
5. Sets up pre-commit hooks
6. Generates initial `uv.lock` file

### 2. `update_deps.sh` - Dependency Updates
**Purpose**: Updates project dependencies and maintains lock file consistency

**Features**:
- Automatic lock file backup before updates
- Dependency conflict checking
- Security vulnerability scanning
- Test verification after updates
- Docker integration
- Backup management

**Usage**:
```bash
./uv_setup/update_deps.sh
```

**What it does**:
1. Creates backup of current `uv.lock`
2. Updates lock file with latest compatible versions
3. Installs updated dependencies
4. Runs tests to verify updates
5. Checks for security issues
6. Offers Docker rebuild option
7. Cleans up old backups

### 3. `clean_environment.sh` - Environment Cleanup
**Purpose**: Cleans up virtual environment, cache, and temporary files

**Features**:
- Interactive and non-interactive modes
- Comprehensive cache cleaning
- Build artifact removal
- Temporary file cleanup
- Disk usage reporting

**Usage**:
```bash
# Interactive cleanup
./uv_setup/clean_environment.sh

# Full cleanup without prompts
./uv_setup/clean_environment.sh --full

# Show help
./uv_setup/clean_environment.sh --help
```

**What it cleans**:
- Virtual environment (`.venv/`)
- Cache directories (`.pytest_cache/`, `__pycache__/`, etc.)
- Build artifacts (`build/`, `dist/`, `*.egg-info`)
- Temporary files (`*.tmp`, `*.log`, `*.bak`)
- UV cache

### 4. `manage_deps.sh` - Dependency Management
**Purpose**: Provides easy commands for managing project dependencies

**Features**:
- Add/remove packages
- Development dependency management
- Package information display
- Dependency tree visualization
- Requirements export in multiple formats

**Usage**:
```bash
# Add a package
./uv_setup/manage_deps.sh add pandas

# Add development package
./uv_setup/manage_deps.sh add-dev pytest

# Add package with extra
./uv_setup/manage_deps.sh add fastapi api

# Remove package
./uv_setup/manage_deps.sh remove unused-package

# List packages
./uv_setup/manage_deps.sh list

# Show package info
./uv_setup/manage_deps.sh show numpy

# Check outdated packages
./uv_setup/manage_deps.sh outdated

# Update specific package
./uv_setup/manage_deps.sh update numpy

# Sync dependencies
./uv_setup/manage_deps.sh sync

# Generate lock file
./uv_setup/manage_deps.sh lock

# Install from lock file
./uv_setup/manage_deps.sh install-lock

# Show dependency tree
./uv_setup/manage_deps.sh tree

# Check for conflicts
./uv_setup/manage_deps.sh check

# Export requirements
./uv_setup/manage_deps.sh export toml

# Show help
./uv_setup/manage_deps.sh help
```

## Best Practices

### 1. Lock File Management
- Always commit `uv.lock` to version control
- Use `uv lock --upgrade` to update dependencies
- Backup lock file before major updates
- Test thoroughly after lock file changes

### 2. Virtual Environment
- Use `in-project = true` in `uv.toml`
- Activate environment: `source .venv/bin/activate`
- Use `uv run` for commands in virtual environment

### 3. Dependency Management
- Use `uv add` instead of `pip install`
- Specify extras: `uv add --extra dev pytest`
- Use `uv sync` to install from lock file
- Use `uv remove` to remove packages

### 4. Development Workflow
1. **Setup**: Run `./uv_setup/setup_uv.sh` once
2. **Daily**: Use `uv run pytest` for testing
3. **Updates**: Use `./uv_setup/update_deps.sh` periodically
4. **Cleanup**: Use `./uv_setup/clean_environment.sh` when needed

## Configuration

### `uv.toml` (Project Root)
The main configuration file includes:
- Python version requirements
- Virtual environment settings
- Dependency optimization
- Cache configuration
- Lock file settings

### Environment Variables
```bash
# Add uv to PATH (if not already done)
export PATH="$HOME/.cargo/bin:$PATH"

# Activate virtual environment
source .venv/bin/activate
```

## Troubleshooting

### Common Issues

1. **uv command not found**
   ```bash
   ./uv_setup/setup_uv.sh
   ```

2. **Virtual environment issues**
   ```bash
   ./uv_setup/clean_environment.sh --full
   ./uv_setup/setup_uv.sh
   ```

3. **Dependency conflicts**
   ```bash
   ./uv_setup/manage_deps.sh check
   ./uv_setup/manage_deps.sh sync
   ```

4. **Lock file issues**
   ```bash
   ./uv_setup/manage_deps.sh lock
   ./uv_setup/manage_deps.sh install-lock
   ```

### Performance Tips

1. **Use binary packages**: Configure `only-binary` in `uv.toml`
2. **Enable caching**: Set appropriate `cache-dir`
3. **Use lock file**: Always use `uv sync` instead of `uv pip install`
4. **Clean regularly**: Run cleanup script periodically

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: Setup uv
  uses: astral-sh/setup-uv@v1
  with:
    version: "0.2.0"

- name: Install dependencies
  run: uv sync --frozen

- name: Run tests
  run: uv run pytest tests/ -n auto
```

### Docker Integration
```dockerfile
# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy lock file
COPY uv.lock .

# Install dependencies
RUN uv sync --frozen
```

## Security

- Regular security checks with `safety`
- Lock file pinning for reproducible builds
- Backup management for rollback capability
- Dependency conflict detection

## Monitoring

- Disk usage tracking
- Cache size monitoring
- Dependency update notifications
- Test result verification

## Support

For issues with these scripts:
1. Check the script help: `./script.sh --help`
2. Review logs in `logs/` directory
3. Check `uv` documentation: https://docs.astral.sh/uv/
4. Verify Python version compatibility

## Contributing

When modifying these scripts:
1. Follow the existing code style
2. Add proper error handling
3. Include help documentation
4. Test on both macOS and Linux
5. Update this README if adding new features
