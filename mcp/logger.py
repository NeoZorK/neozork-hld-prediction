#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging setup for MCP Server
"""

import logging
import sys
import os
import datetime

def setup_logger(project_root=None, console_output=False):
    """
    Set up and configure logger for the MCP server

    Args:
        project_root: Project root directory path
        console_output: Whether to output logs to console (default: False)
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
            if console_output:
                print(f"Created logs directory: {logs_dir}")
        except Exception as e:
            if console_output:
                print(f"Error creating logs directory: {str(e)}")

    # Use a single permanent log file instead of creating a new one with each launch
    log_file_path = os.path.join(logs_dir, "mcp_server.log")

    # Создаем форматтер, который будет использоваться для обработчиков
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Настраиваем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Устанавливаем базовый уровень логирования

    # Удаляем все существующие обработчики
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Добавляем файловый обработчик всегда
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Сохраняем уровень DEBUG для файла (подробные логи)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Добавляем консольный обработчик только если console_output=True
    if console_output:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.DEBUG)  # Устанавливаем уровень DEBUG для консоли
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # Создаем логгер для приложения
    logger = logging.getLogger("simple_mcp")
    logger.setLevel(logging.DEBUG)  # Убедимся, что уровень логирования установлен правильно

    # Log information about startup and path to log file
    logger.info(f"Logs are saved to file: {log_file_path}")

    # Add log entry about server startup
    logger.info("========================")
    logger.info("MCP Server starting up at %s", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("Working directory: %s", os.getcwd())
    logger.info("Project root directory: %s", project_root)
    logger.info("Script location: %s", os.path.abspath(__file__))
    logger.info("========================")

    return logger
