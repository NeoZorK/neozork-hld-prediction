# -*- coding: utf-8 -*-
# setup_mcp.py
"""
Setup script for MCP server configuration in PyCharm
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any


def create_pycharm_mcp_config() -> None:
    """Create PyCharm-specific MCP configuration"""

    # PyCharm external tools configuration
    pycharm_config = {
        "name": "Start MCP Server",
        "description": "Start MCP Server for GitHub Copilot integration",
        "program": "python",
        "arguments": "mcp_server.py",
        "workingDirectory": "$ProjectFileDir$",
        "environmentVariables": {
            "PYTHONPATH": "$ProjectFileDir$/src",
            "PROJECT_ROOT": "$ProjectFileDir$"
        }
    }

    # Create .idea directory if it doesn't exist
    idea_dir = Path(".idea")
    idea_dir.mkdir(exist_ok=True)

    # Create tools configuration
    tools_dir = idea_dir / "tools"
    tools_dir.mkdir(exist_ok=True)

    tools_config_file = tools_dir / "External Tools.xml"
    tools_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<toolSet name="External Tools">
  <tool name="Start MCP Server" description="Start MCP Server for GitHub Copilot integration" showInMainMenu="false" showInEditor="false" showInProject="false" showInSearchPopup="false" disabled="false" useConsole="true" showConsoleOnStdOut="false" showConsoleOnStdErr="false" synchronizeAfterRun="true">
    <exec>
      <option name="COMMAND" value="python" />
      <option name="PARAMETERS" value="mcp_server.py" />
      <option name="WORKING_DIRECTORY" value="$ProjectFileDir$" />
    </exec>
    <envs>
      <env name="PYTHONPATH" value="$ProjectFileDir$/src" />
      <env name="PROJECT_ROOT" value="$ProjectFileDir$" />
    </envs>
  </tool>
  <tool name="Test MCP Server" description="Test MCP Server configuration" showInMainMenu="false" showInEditor="false" showInProject="false" showInSearchPopup="false" disabled="false" useConsole="true" showConsoleOnStdOut="false" showConsoleOnStdErr="false" synchronizeAfterRun="true">
    <exec>
      <option name="COMMAND" value="python" />
      <option name="PARAMETERS" value="mcp_server.py --debug" />
      <option name="WORKING_DIRECTORY" value="$ProjectFileDir$" />
    </exec>
    <envs>
      <env name="PYTHONPATH" value="$ProjectFileDir$/src" />
      <env name="PROJECT_ROOT" value="$ProjectFileDir$" />
    </envs>
  </tool>
</toolSet>"""

    with open(tools_config_file, 'w', encoding='utf-8') as f:
        f.write(tools_xml)

    print(f"Created PyCharm external tools configuration: {tools_config_file}")


def create_copilot_workspace_config() -> None:
    """Create workspace configuration for GitHub Copilot"""

    copilot_config = {
        "github.copilot.enable": {
            "*": True,
            "yaml": True,
            "plaintext": True,
            "markdown": True,
            "python": True
        },
        "github.copilot.advanced": {
            "length": 500,
            "temperature": 0.1,
            "top_p": 1,
            "inlineSuggestEnable": True,
            "listCount": 10,
            "debug.overrideEngine": "codex",
            "debug.testOverrideProxyUrl": "",
            "debug.filterLogCategories": []
        }
    }

    # Create .vscode directory for workspace settings
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    settings_file = vscode_dir / "settings.json"
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(copilot_config, f, indent=2)

    print(f"Created Copilot workspace configuration: {settings_file}")


def create_project_metadata() -> None:
    """Create project metadata file for MCP server"""

    metadata = {
        "project": {
            "name": "NeoZorK HLD Prediction",
            "version": "1.0.0",
            "description": "High Low Prediction for Time Series Financial rates",
            "type": "financial_ml_project",
            "language": "python",
            "coding_style": "snake_case",
            "documentation_language": "english"
        },
        "structure": {
            "src_directory": "src",
            "test_directory": "tests",
            "script_directory": "scripts",
            "main_entry_point": "run_analysis.py"
        },
        "modules": {
            "calculation": "Financial calculations and prediction algorithms",
            "cli": "Command line interface components",
            "common": "Shared utilities and constants",
            "data": "Data processing and feature engineering",
            "eda": "Exploratory data analysis",
            "plotting": "Visualization and charting",
            "utils": "General utility functions",
            "workflow": "Pipeline and workflow management"
        },
        "technologies": [
            "tensorflow", "keras", "lightgbm", "xgboost",
            "pandas", "numpy", "matplotlib", "plotly",
            "yfinance", "python-binance", "backtrader",
            "scikit-learn", "scipy", "statsmodels"
        ],
        "mcp_server": {
            "enabled": True,
            "config_file": "mcp-config.json",
            "server_script": "mcp_server.py"
        }
    }

    metadata_file = Path("mcp/project_metadata.json")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    print(f"Created project metadata: {metadata_file}")


def create_startup_script() -> None:
    """Create startup script for MCP server"""

    startup_script = """#!/bin/bash
# -*- coding: utf-8 -*-
# start_mcp_server.sh

echo "Starting NeoZorK HLD Prediction MCP Server..."

# Set environment variables
export PYTHONPATH="./src:$PYTHONPATH"
export PROJECT_ROOT="."

# Activate virtual environment if exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Activated virtual environment"
elif [ -f "env/bin/activate" ]; then
    source env/bin/activate
    echo "Activated virtual environment"
fi

# Install dependencies if needed
if [ ! -f ".mcp_setup_complete" ]; then
    echo "Installing MCP server dependencies..."
    pip install -r requirements.txt
fi

# Start MCP server
python mcp/mcp_server.py

echo "MCP Server stopped"
"""

    scripts_dir = Path("scripts")
    scripts_dir.mkdir(exist_ok=True)

    script_file = scripts_dir / "start_mcp_server.sh"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(startup_script)

    # Make executable on Unix systems
    try:
        os.chmod(script_file, 0o755)
        print(f"Created startup script with execution permissions: {script_file}")
    except OSError:
        print(f"Created startup script (without execution permissions): {script_file}")


def create_test_connection_script() -> None:
    """Create script to test MCP server connection"""

    test_script = """#!/bin/bash
# Test the MCP server connection for GitHub Copilot

echo "=== Testing MCP Server Connection ==="
echo "Checking if MCP server is running correctly..."

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Define the test request
TEST_REQUEST='{"method":"initialize","params":{}}'

# Run the MCP server with a test input
echo "$TEST_REQUEST" | python3 "$PROJECT_ROOT/mcp/mcp_server.py"

echo ""
echo "=== Detailed Debug Information ==="
echo "Running MCP server in debug mode to check project context..."
python3 "$PROJECT_ROOT/mcp/mcp_server.py" --debug | head -n 20

echo ""
echo "If you see a valid JSON response above, the MCP server is working correctly."
echo "For troubleshooting:"
echo "1. Check that paths in mcp-config.json are correct"
echo "2. Check that PYTHONPATH includes your project root"
echo "3. Examine IntelliJ logs in Help > Show Log in Explorer"
echo "=== End of Test ==="
"""

    scripts_dir = Path("scripts")
    scripts_dir.mkdir(exist_ok=True)

    script_file = scripts_dir / "test_mcp_connection.sh"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(test_script)

    # Make executable on Unix systems
    try:
        os.chmod(script_file, 0o755)
        print(f"Created test connection script with execution permissions: {script_file}")
    except OSError:
        print(f"Created test connection script (without execution permissions): {script_file}")


def main():
    """Main setup function"""
    print("Setting up MCP Server for NeoZorK HLD Prediction project...")

    # Create all configuration files
    create_pycharm_mcp_config()
    create_copilot_workspace_config()
    create_project_metadata()
    create_startup_script()
    create_test_connection_script()

    print("\nMCP Server setup completed!")
    print("\nNext steps:")
    print("1. Open project in PyCharm")
    print("2. Go to Tools -> External Tools -> Start MCP Server")
    print("3. Or run: python mcp/mcp_server.py")
    print("4. Test with: python mcp/mcp_server.py --debug")
    print("\nGitHub Copilot will now have full context about your project!")


if __name__ == "__main__":
    main()

