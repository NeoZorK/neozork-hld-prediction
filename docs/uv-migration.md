# UV Migration Legacy Documentation

⚠️ **Note:** This file has been superseded by the new documentation structure. Please refer to [docs/uv-setup.md](uv-setup.md) for current UV documentation.

## Quick Reference

For current UV setup and usage, see:
- [UV Setup Guide](uv-setup.md) - Complete UV package manager guide
- [Installation](installation.md) - UV integration in setup
- [Docker Guide](docker.md) - UV in Docker builds

## Migration Notice

This file is kept for reference but may be outdated. The new documentation provides:
- Enhanced UV setup instructions
- Performance comparisons and benefits
- Docker integration examples
- Troubleshooting and best practices

| pip                            | uv                        | Description                               |
|--------------------------------|---------------------------|-------------------------------------------|
| `pip install package`          | `uv pip install package`  | Install a package                         |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` | Install from requirements file |
| `pip uninstall package`        | `uv pip uninstall package` | Remove a package                         |
| `pip freeze > requirements.txt`| `uv pip freeze > requirements.txt` | Save current dependencies         |
| `python -m venv .venv`         | `uv venv`                 | Create a virtual environment              |
| -                              | `uv pip compile requirements.txt` | Compile requirements.txt to a lock file |

## Virtual environments with uv

```bash
# Create a virtual environment
uv venv

# Activate (same as with regular venv)
source .venv/bin/activate
```

## Docker

The Dockerfile is already configured to use uv for dependency installation.

## CI/CD

For GitHub Actions, you can use caching to speed up dependency installation:

```yaml
- name: Install uv
  run: |
    # Create a temporary directory for the installer
    mkdir -p /tmp/uv-installer
    # Download the installer script
    curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh -o /tmp/uv-installer/installer.sh
    # Make it executable and run it
    chmod +x /tmp/uv-installer/installer.sh
    /tmp/uv-installer/installer.sh
    # Clean up
    rm -rf /tmp/uv-installer
    
    # Add uv to PATH
    source $HOME/.local/bin/env
    echo "$HOME/.local/bin" >> $GITHUB_PATH

- name: Install dependencies
  run: |
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
```
