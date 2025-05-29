#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple MCP Server runner script for GitHub Copilot connection
This script imports and runs the SimpleMCPServer from the mcp module
"""

import sys
import signal
import os
import logging

# Import logging setup module
from mcp.logger import setup_logger
# Import SimpleMCPServer class from mcp.server module
from mcp.server import SimpleMCPServer

# Define project root directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
project_root = script_dir

# Configure logging using our function
logger = setup_logger(project_root, console_output=False)

if __name__ == "__main__":
    # Display a noticeable message about server startup
    print("\n" + "=" * 60)
    print("🚀 SIMPLE MCP SERVER STARTED")
    print("=" * 60 + "\n")

    # Create MCP server instance
    server = SimpleMCPServer()

    # Note: We don't call display_start_message() to avoid duplicate startup messages

    # Register signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        # Note: We don't print shutdown message here to avoid duplicate messages
        # The shutdown_gracefully method will display the message
        logger.info(f"Received signal {sig}, shutting down gracefully...")
        server.shutdown_gracefully()
        sys.exit(0)

    # Register signal handlers for SIGINT and SIGTERM
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("Signal handlers registered for graceful shutdown (Ctrl+C/SIGTERM)")

    # Run the server
    server.run()

