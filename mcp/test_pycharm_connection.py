#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование соединения MCP с PyCharm
Этот скрипт помогает проверить совместимость MCP сервера с PyCharm
"""

import sys
import os
import json
import subprocess
import time
import logging
from typing import Dict, Any

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pycharm_mcp_test.log", mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("pycharm_mcp_test")

def send_message(message: Dict[str, Any]) -> None:
    """Отправляет сообщение через stdout в формате LSP"""
    message_str = json.dumps(message)
    message_bytes = message_str.encode('utf-8')

    # Формируем сообщение с заголовками
    header = f"Content-Length: {len(message_bytes)}\r\n\r\n".encode('utf-8')

    sys.stdout.buffer.write(header)
    sys.stdout.buffer.write(message_bytes)
    sys.stdout.buffer.flush()

    logger.debug(f"Sent message: {message_str}")

def read_message():
    """Читает сообщение из stdin в формате LSP"""
    # Чтение заголовков
    content_length = None

    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None

        if line == b'\r\n':
            break

        header = line.decode('utf-8').strip()
        if header.lower().startswith('content-length:'):
            content_length = int(header.split(':', 1)[1].strip())

    if content_length is None:
        return None

    # Чтение тела сообщения
    body = sys.stdin.buffer.read(content_length)
    message = json.loads(body.decode('utf-8'))

    logger.debug(f"Received message: {json.dumps(message)}")
    return message

def test_mcp_connection():
    """Тестирует соединение с MCP сервером"""
    logger.info("Starting MCP connection test")

    # 1. Отправляем запрос initialize
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "processId": os.getpid(),
            "clientInfo": {
                "name": "PyCharm Test Client",
                "version": "1.0.0"
            },
            "rootUri": f"file://{os.getcwd()}",
            "capabilities": {},
            "trace": "verbose",
            "protocolVersion": "2025-03-26"
        }
    }

    logger.info("Sending initialize request")
    send_message(initialize_request)

    # 2. Ожидаем ответ на initialize
    initialize_response = read_message()
    if not initialize_response:
        logger.error("Failed to receive initialize response")
        return False

    logger.info("Received initialize response")

    # 3. Отправляем уведомление initialized
    initialized_notification = {
        "jsonrpc": "2.0",
        "method": "initialized",
        "params": {}
    }

    logger.info("Sending initialized notification")
    send_message(initialized_notification)

    # 4. Ожидаем любое уведомление от сервера (опционально)
    try:
        notification = read_message()
        if notification:
            logger.info(f"Received notification: {notification.get('method', 'unknown')}")
    except Exception as e:
        logger.warning(f"Error while waiting for notification: {str(e)}")

    # 5. Отправляем запрос shutdown
    shutdown_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "shutdown"
    }

    logger.info("Sending shutdown request")
    send_message(shutdown_request)

    # 6. Ожидаем ответ на shutdown
    shutdown_response = read_message()
    if not shutdown_response:
        logger.error("Failed to receive shutdown response")
        return False

    logger.info("Received shutdown response")

    # 7. Отправляем уведомление exit
    exit_notification = {
        "jsonrpc": "2.0",
        "method": "exit"
    }

    logger.info("Sending exit notification")
    send_message(exit_notification)

    logger.info("MCP connection test completed successfully")
    return True

if __name__ == "__main__":
    try:
        test_mcp_connection()
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        sys.exit(1)
