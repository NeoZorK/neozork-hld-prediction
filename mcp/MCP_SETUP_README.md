# MCP Server Setup for NeoZorK HLD Prediction

## Description

This set of files configures a local MCP (Model Context Protocol) server for your financial time series data project. The MCP server provides GitHub Copilot with full context about the project structure, modules, and code.

## Configuration Files

### 1. `mcp_server.py`
Main MCP server that:
- Analyzes project structure
- Provides context about modules (calculation, data, eda, plotting, etc.)
- Reads project files
- Responds to MCP requests from Copilot

### 2. `mcp-config.json`
MCP server configuration with settings for:
- Included and excluded files
- Environment variables
- Server capabilities

### 3. `setup_mcp.py`
Installation script that creates:
- External Tools configuration for PyCharm
- Workspace settings for Copilot
- Project metadata
- Startup script

### 4. `test_mcp_server.py`
Test script to verify MCP server functionality

### 5. `test_mcp_connection.sh`
Shell script to test connection to the MCP server

## Installation and Setup

### Step 1: Run Installation
```bash
python mcp/setup_mcp.py
```
### Step 2: PyCharm Configuration

- Open project in PyCharm
- Navigate to Tools → External Tools
- Find "Start MCP Server" and "Test MCP Server"
- Run "Test MCP Server" for verification

### Step 3: Start MCP Server

#### Option A: Through PyCharm
Tools → External Tools → Start MCP Server

#### Option B: Command Line
```bash
python mcp/mcp_server.py
```
#### Option C: Script
 Give Execution Permissions to the Script
```bash
chmod +x /scripts/start_mcp_server.sh
```
```bash
scripts/.start_mcp_server.sh
```
### Step 4: Verify Operation
```bash
python mcp/mcp_server.py --debug
```
### Step 5: Check Server Operation
```bash
python mcp/test_mcp_server.py
```
### Step 6: Test Connection
```bash
scripts/.test_mcp_connection.sh
```
### Step 7: Give Execution Permissions to the Script
```bash
chmod +x /scripts/test_mcp_connection.sh
```


## MCP Server Capabilities

### Project Structure Analysis

- Modules: calculation, cli, common, data, eda, plotting, utils, workflow
- Dependencies: TensorFlow, Keras, LightGBM, XGBoost, pandas, numpy, etc.
- Code Style: snake_case, English comments

### Context for Copilot
- Complete project structure
- Module descriptions and purposes
- File listings and contents
- Technology stack
- Coding patterns

### MCP Resources

- Project Context: Complete project context
- Module Information: Detailed module information
- File Content: Project file contents

## Usage with GitHub Copilot

After starting the MCP server, GitHub Copilot will have access to:

1) Project Structure - architecture understanding
2) Modules and their purposes - functionality context
3) Dependencies - libraries in use
4) Code Style - convention compliance
5) Existing Code - for better suggestions

## Example Questions for Copilot

With the configured MCP server, you can ask:

- "How to add a new indicator to the calculation module?"
- "Create a function for prediction visualization"
- "Optimize data loading in the data module"
- "Add a new analysis type to the eda module"
- "Fix logic in the prediction function"

## Project Structure for Copilot
```plaintext
neozork-hld-prediction/
├── src/
│   ├── calculation/                # Calculations and prediction algorithms
│   ├── cli/                        # Command line interface components
│   ├── common/                     # Common utilities and constants
│   ├── data/                       # Data processing and features
│   ├── eda/                        # Exploratory data analysis
│   ├── export/                     # Exporting results
│   ├── plotting/                   # Visualization and charts
│   ├── utils/                      # Helper functions
│   └── workflow/                   # Pipeline management
├── tests/                          # Tests
│   ├── calculation/                # Tests for calculation module
│   ├── cli/                        # Tests for CLI module
│   ├── common/                     # Tests for common utilities
│   ├── data/                       # Tests for data processing
│   ├── eda/                        # Tests for EDA module
│   ├── plotting/                   # Tests for plotting module
│   ├── scripts/                    # Tests for scripts
│   ├── utils/                      # Tests for utility functions
│   └── workflow/                   # Tests for workflow management
├── scripts/                        # Scripts
│   └── start_mcp_server.sh         # Script to start MCP server
├── mcp/                            # MCP server files
│   ├── mcp-config.json             # MCP server configuration
│   ├── mcp_server.py               # Main MCP server script
│   ├── setup_mcp.py                # Setup script
│   ├── test_mcp_server.py          # Test script for MCP server
│   └── MCP_SETUP_README.md         # MCP setup documentation
├── requirements.txt    # Dependencies
└── run_analysis.py     # Main file
```

### Server Logs

Logs are displayed in the console when starting the server

## Development Integration

The MCP server automatically:

- Tracks file changes
- Updates context for Copilot
- Provides current project information
- Supports all modules and dependencies

## Technical Requirements

- Python 3.8+
- Installed dependencies from requirements.txt
- PyCharm (optional, for External Tools)
- GitHub Copilot extension

Now GitHub Copilot will have complete understanding of your project and can provide more accurate and contextual suggestions!
