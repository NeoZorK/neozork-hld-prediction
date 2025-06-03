#!/bin/bash
# Script for installing uv in the local development environment

echo "Installing uv - a fast Python package manager..."

# Check if curl is available
if ! command -v curl &> /dev/null; then
    echo "curl not found, please install it"
    exit 1
fi

# Install uv safely
mkdir -p /tmp/uv-installer
curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh -o /tmp/uv-installer/installer.sh
chmod +x /tmp/uv-installer/installer.sh
/tmp/uv-installer/installer.sh
rm -rf /tmp/uv-installer

# Check if installation was successful
if command -v uv &> /dev/null; then
    echo "uv successfully installed!"
    echo "To activate, add the following line to your ~/.bashrc or ~/.zshrc:"
    echo 'export PATH="$HOME/.cargo/bin:$PATH"'

    # Create a virtual environment using uv if it doesn't exist yet
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment using uv..."
        ~/.cargo/bin/uv venv
        echo "Virtual environment created in .venv directory"
        echo "Activate it with: source .venv/bin/activate"
    fi

    echo "Installing dependencies from requirements.txt..."
    if [ -f "requirements.txt" ]; then
        if [ -d ".venv" ]; then
            source .venv/bin/activate
            ~/.cargo/bin/uv pip install -r requirements.txt
            echo "Dependencies successfully installed in the virtual environment!"
        else
            echo "Error: virtual environment not found"
        fi
    else
        echo "Error: requirements.txt file not found"
    fi
else
    echo "Error: failed to install uv"
    exit 1
fi

echo "Done! You can now use uv instead of pip."
