#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging setup for MCP Server
"""

import logging
import sys
import os
import datetime

def setup_logger(project_root=None):
    """
    Set up and configure logger for the MCP server
    """
    if not project_root:
        # Determine project root if not provided
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        # If script is run from the mcp directory, use parent directory as root
        if os.path.basename(script_dir) == "mcp":
            project_root = os.path.dirname(script_dir)
        else:
            project_root = script_dir

    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(project_root, "logs")
    if not os.path.exists(logs_dir):
        try:
            os.makedirs(logs_dir)
            print(f"Created logs directory: {logs_dir}")
        except Exception as e:
            print(f"Error creating logs directory: {str(e)}")

    # Use a single permanent log file instead of creating a new one with each launch
    log_file_path = os.path.join(logs_dir, "mcp_server.log")

    # Unified logging setup for the entire application
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),      # Output logs to stdout for console display
            logging.FileHandler(log_file_path, encoding='utf-8')  # Output logs to file
        ]
    )
    logger = logging.getLogger("simple_mcp")

    # Log information about startup and path to log file
    logger.info(f"Logs are saved to file: {log_file_path}")

    # Configure logging to output ALL information to console and file
    # Make sure no logs are filtered
    for handler in logging.root.handlers:
        handler.setLevel(logging.DEBUG)

    # Set DEBUG level for all loggers
    logging.getLogger().setLevel(logging.DEBUG)

    # Add log entry about server startup
    logger.info("========================")
    logger.info("MCP Server starting up at %s", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("Working directory: %s", os.getcwd())
    logger.info("Project root directory: %s", project_root)
    logger.info("Script location: %s", os.path.abspath(__file__))
    logger.info("========================")

    return logger
