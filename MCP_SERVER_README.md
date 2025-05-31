# MCP Server for GitHub Copilot

Local MCP (Model Completion Protocol) server to extend GitHub Copilot capabilities in PyCharm CE.

## Features

- Works through standard input/output (STDIO)
- Processes requests from GitHub Copilot MCP client
- Has access to the local project
- Provides detailed session logging
- Works continuously without terminating

## Installation

1. Make sure you have Python 3.8 or higher installed
2. Clone the repository or copy the `mcp_server.py` file
3. Create a `logs` directory in the project root (if it doesn't exist yet):
   ```
   mkdir -p logs
   ```
4. Set execution permissions:
   ```
   chmod +x mcp_server.py
   ```

## Setting up PyCharm CE to work with GitHub Copilot MCP

1. Open PyCharm CE
2. Install the GitHub Copilot plugin from the JetBrains marketplace
3. Go to Settings/Preferences -> Tools -> GitHub Copilot
4. In the "Advanced" section, find the "MCP Configuration" setting
5. Add the path to the `mcp.json` file, which should contain the following:

```json
{
  "command": "python",
  "args": ["/full/path/to/mcp_server.py"],
  "stdio": true
}
```

Replace `/full/path/to/mcp_server.py` with the absolute path to the mcp_server.py file.

## Launch

You don't need to do anything special to launch the MCP server. When properly configured, PyCharm CE will automatically start the MCP server when using GitHub Copilot. Everything happens automatically when you open your project.

## Successful Connection Signs

When GitHub Copilot MCP client successfully connects to your local MCP server, you will notice:

1. In Agent mode, local folders appear as options after clicking "Add Context"
2. Code suggestions include references to your local project files (e.g., the mql5_feed folder appears in autocompletions)
3. The agent can access and understand your project structure

## Diagnostic Commands

You can verify the connection status by asking GitHub Copilot in chat mode:
```
MCP_DEBUG: diagnostic
```

This command will return a JSON response with the current connection status and server information, similar to the following:

```json
{
  "connectionState": "active",
  "serverInfo": {
    "name": "Neozork MCP Server",
    "version": "1.0.0"
  },
  "workspaceRoot": "/Users/rost/Documents/DIS/REPO/neozork-hld-prediction",
  "indexedFilesCount": 142,
  "availableSymbols": [
    "AAPL",
    "BTCUSD",
    "ETHUSD",
    "EURUSD",
    "GBPUSD",
    "GOOG",
    "MSFT"
  ],
  "availableTimeframes": [
    "D1",
    "H1",
    "H4",
    "M1",
    "M5",
    "M15",
    "W1",
    "MN1"
  ]
} 
```

This should return information about the connection status, including:
- Connection state (active/inactive)
- Server version
- Current workspace path
- Number of indexed files
- Available symbols and timeframes from financial data

## Testing Content Access

You can test if GitHub Copilot can access your project's content by adding this prompt:
```
# write function, use main classes of this project
```

If properly connected, Copilot will generate code using your actual project classes and functions.

## Offline Usage

You can use the MCP server and Copilot client completely offline. Once the initial GitHub Copilot authentication is complete, the local MCP server allows you to:

1. Generate code based on your local files without an internet connection
2. Analyze and understand your project structure offline
3. Work on air-gapped systems or in environments with restricted internet access

## Integration with Ollama LLM

You can configure an Ollama LLM client to access the local MCP server, which allows you to:

1. Use local LLMs for code generation while still having access to your project context
2. Reduce dependency on cloud-based services
3. Maintain privacy by keeping all code generation processes local

To configure Ollama with the MCP server, add the MCP server endpoint to your Ollama configuration.

## Logging

All logs are saved in the `logs/` directory in the `mcp_server.log` file. Each session is clearly separated in the log.

You can view the logs in real-time using the following command:
```bash
tail -f logs/mcp_server.log
```

## Troubleshooting

### Problem: MCP server doesn't start

- Check that the `mcp.json` file contains the correct path to the server
- Make sure the `mcp_server.py` file has execution permissions
- Check that the `logs` directory exists and is writable

### Problem: GitHub Copilot doesn't use the local MCP server

- Restart PyCharm CE
- Check logs for connection errors
- Make sure the GitHub Copilot plugin is activated

## Running Tests

To ensure the MCP server works correctly, you can run the unit tests provided in the `tests/mcp` directory. Make sure you have Python's `unittest` module available.

```bash
# Install required dependencies
pip install -r requirements.txt

# Run the tests
python -m unittest discover tests/mcp
```

## Running Tests with pytest

To run the same test suite using pytest, first install pytest:

```bash
pip install pytest
```

Then execute:

```bash
# Run pytest on the tests/mcp directory
pytest tests/mcp
```
