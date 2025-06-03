# Migrating from pip to uv

## What is uv?

[uv](https://github.com/astral-sh/uv) is a new, fast Python package manager that can replace pip.

**Benefits of uv:**
- 10-100 times faster than pip when installing packages
- Parallel dependency installation
- Improved dependency resolution
- Smaller Docker container sizes
- Better package caching

## Installing uv

### Local installation

For local installation, you can use the provided script:

```bash
chmod +x uv_setup/setup_uv.sh
./uv_setup/setup_uv.sh
```

Or install manually:

```bash
# Create a temporary directory for the installer
mkdir -p /tmp/uv-installer
# Download the installer script
curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh -o /tmp/uv-installer/installer.sh
# Make it executable and run it
chmod +x /tmp/uv-installer/installer.sh
/tmp/uv-installer/installer.sh
# Clean up
rm -rf /tmp/uv-installer

# Add to PATH (add to your .bashrc or .zshrc)
export PATH="$HOME/.cargo/bin:$PATH"
```

### Verifying installation

```bash
uv --version
```

## uv commands (pip replacements)

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
    
    echo "$HOME/.cargo/bin" >> $GITHUB_PATH

- name: Install dependencies
  run: |
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
```
