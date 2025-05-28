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

def read_message(timeout=5.0):
    """Читает сообщение из stdin в формате LSP с таймаутом"""
    # Чтение заголовков
    content_length = None
    start_time = time.time()
    buffer = b""

    # Неблокирующее чтение заголовков с таймаутом
    while True:
        if time.time() - start_time > timeout:
            logger.warning(f"Timeout reached while reading headers after {timeout} seconds")
            return None

        if os.name == 'nt':  # Windows использует блокирующее чтение
            line = sys.stdin.buffer.readline()
        else:
            # Проверка доступности данных
            import select
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)
            if not ready:
                time.sleep(0.1)  # Маленькая пауза, чтобы не загружать CPU
                continue
            line = sys.stdin.buffer.readline()

        if not line:
            logger.warning("No data received from stdin")
            time.sleep(0.1)
            continue

        # Добавляем в буфер и ищем маркер конца заголовков
        buffer += line

        # Поддержка как стандартного разделителя \r\n\r\n, так и PyCharm-стиля \n\n
        if b'\r\n\r\n' in buffer:
            headers, buffer = buffer.split(b'\r\n\r\n', 1)
            break
        elif b'\n\n' in buffer:
            headers, buffer = buffer.split(b'\n\n', 1)
            break

        # Проверяем заголовок Content-Length в текущей строке
        try:
            header = line.decode('utf-8').strip()
            if header.lower().startswith('content-length:'):
                content_length = int(header.split(':', 1)[1].strip())
                logger.debug(f"Found Content-Length: {content_length}")
        except Exception as e:
            logger.warning(f"Error parsing header: {e}")

    # Если после разделителя заголовков уже есть данные, считаем их началом тела
    body = buffer

    # Если Content-Length не найден, возвращаем ошибку
    if content_length is None:
        logger.error("Content-Length header not found")
        return None

    # Дочитываем оставшуюся часть тела
    remaining = content_length - len(body)
    if remaining > 0:
        logger.debug(f"Reading remaining {remaining} bytes of message body")

        # Чтение оставшихся данных с таймаутом
        start_body_time = time.time()
        while len(body) < content_length:
            if time.time() - start_body_time > timeout:
                logger.warning(f"Timeout reached while reading message body after {timeout} seconds")
                return None

            if os.name == 'nt':  # Windows использует блокирующее чтение
                chunk = sys.stdin.buffer.read(min(1024, content_length - len(body)))
            else:
                # Проверка доступности данных
                import select
                ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                if not ready:
                    time.sleep(0.1)  # Маленькая пауза, чтобы не загружать CPU
                    continue
                chunk = sys.stdin.buffer.read(min(1024, content_length - len(body)))

            if not chunk:
                time.sleep(0.1)
                continue

            body += chunk
            logger.debug(f"Read {len(chunk)} bytes, total {len(body)}/{content_length}")

    if len(body) != content_length:
        logger.warning(f"Incomplete message: got {len(body)} bytes, expected {content_length}")
        return None

    try:
        message = json.loads(body.decode('utf-8'))
        logger.debug(f"Received message: {json.dumps(message)}")
        return message
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON: {e}")
        logger.debug(f"Raw content: {body}")
        return None

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

def test_mcp_connection_direct(server_process):
    """Тестирует соединение с MCP сервером через прямое соединение потоков ввода/вывода"""
    logger.info("Starting MCP direct connection test")

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
    _send_message_to_server(server_process, initialize_request)

    # 2. Ожидаем ответ на initialize
    initialize_response = _read_message_from_server(server_process)
    if not initialize_response:
        logger.error("Failed to receive initialize response")
        return False

    logger.info(f"Received initialize response: {json.dumps(initialize_response)}")

    # 3. Отправляем уведомление initialized
    initialized_notification = {
        "jsonrpc": "2.0",
        "method": "initialized",
        "params": {}
    }

    logger.info("Sending initialized notification")
    _send_message_to_server(server_process, initialized_notification)

    # 4. Ожидаем любое уведомление от сервера (опционально)
    try:
        notification = _read_message_from_server(server_process, timeout=1.0)
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
    _send_message_to_server(server_process, shutdown_request)

    # 6. Ожидаем ответ на shutdown
    shutdown_response = _read_message_from_server(server_process)
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
    _send_message_to_server(server_process, exit_notification)

    logger.info("MCP connection test completed successfully")
    return True

def _send_message_to_server(server_process, message):
    """Отправляет сообщение серверу MCP через его stdin"""
    message_str = json.dumps(message)
    message_bytes = message_str.encode('utf-8')

    # Формируем сообщение с заголовками
    header = f"Content-Length: {len(message_bytes)}\r\n\r\n".encode('utf-8')

    try:
        server_process.stdin.write(header)
        server_process.stdin.write(message_bytes)
        server_process.stdin.flush()
        logger.debug(f"Sent message to server: {message_str}")
    except Exception as e:
        logger.error(f"Error sending message to server: {str(e)}")
        raise

def _read_message_from_server(server_process, timeout=5.0):
    """Читает сообщение от сервера MCP из его stdout с таймаутом"""
    # Чтение заголовков
    content_length = None
    start_time = time.time()
    buffer = b""

    # Неблокирующее чтение заголовков с таймаутом
    while True:
        if time.time() - start_time > timeout:
            logger.warning(f"Timeout reached while reading server headers after {timeout} seconds")
            return None

        # Проверка доступности данных
        import select
        ready, _, _ = select.select([server_process.stdout], [], [], 0.1)
        if not ready:
            time.sleep(0.1)  # Маленькая пауза, чтобы не загружать CPU
            continue

        # Читаем по одному байту, чтобы найти разделитель заголовков
        char = server_process.stdout.read(1)
        if not char:
            if server_process.poll() is not None:
                logger.error(f"Server process exited with code {server_process.returncode}")
                return None
            time.sleep(0.1)
            continue

        buffer += char

        # Ищем разделители заголовков
        if len(buffer) >= 4 and buffer[-4:] == b"\r\n\r\n":
            headers = buffer[:-4]
            buffer = b""
            break
        elif len(buffer) >= 2 and buffer[-2:] == b"\n\n":
            headers = buffer[:-2]
            buffer = b""
            break

        # Проверяем заголовок Content-Length
        if len(buffer) > 16 and b"Content-Length:" in buffer:
            # Ищем Content-Length в буфере
            try:
                header_text = buffer.decode('utf-8', errors='ignore')
                for line in header_text.split("\r\n"):
                    if line.lower().startswith("content-length:"):
                        content_length = int(line.split(":", 1)[1].strip())
                        logger.debug(f"Found Content-Length: {content_length}")
            except Exception as e:
                logger.warning(f"Error parsing header: {e}")

    # Если не нашли заголовок Content-Length в буфере, ищем его в headers
    if content_length is None:
        try:
            header_text = headers.decode('utf-8', errors='ignore')
            for line in header_text.split("\r\n"):
                if line.lower().startswith("content-length:"):
                    content_length = int(line.split(":", 1)[1].strip())
                    logger.debug(f"Found Content-Length in headers: {content_length}")
        except Exception as e:
            logger.warning(f"Error parsing headers: {e}")

    # Если Content-Length не найден, возвращаем ошибку
    if content_length is None:
        logger.error("Content-Length header not found")
        return None

    # Чтение тела сообщения
    start_body_time = time.time()
    while len(buffer) < content_length:
        if time.time() - start_body_time > timeout:
            logger.warning(f"Timeout reached while reading message body after {timeout} seconds")
            return None

        # Проверка доступности данных
        import select
        ready, _, _ = select.select([server_process.stdout], [], [], 0.1)
        if not ready:
            time.sleep(0.1)  # Маленькая пауза, чтобы не загружать CPU
            continue

        # Читаем данные порциями
        chunk = server_process.stdout.read(min(1024, content_length - len(buffer)))
        if not chunk:
            if server_process.poll() is not None:
                logger.error(f"Server process exited with code {server_process.returncode}")
                return None
            time.sleep(0.1)
            continue

        buffer += chunk
        logger.debug(f"Read {len(chunk)} bytes from server, total {len(buffer)}/{content_length}")

    if len(buffer) != content_length:
        logger.warning(f"Incomplete message from server: got {len(buffer)} bytes, expected {content_length}")
        return None

    try:
        message = json.loads(buffer.decode('utf-8'))
        logger.debug(f"Received message from server: {json.dumps(message)}")
        return message
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from server: {e}")
        logger.debug(f"Raw content: {buffer}")
        return None

def launch_mcp_server(server_path=None, timeout=10):
    """Запускает MCP сервер и возвращает процесс"""
    if server_path is None:
        # Попробуем найти сервер автоматически
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        default_server_path = os.path.join(project_root, "simple-mcp-server.py")

        if os.path.exists(default_server_path):
            server_path = default_server_path
        else:
            # Ищем другие возможные пути
            candidates = [
                os.path.join(project_root, "mcp", "mcp_server.py"),
                os.path.join(project_root, "mcp_server.py")
            ]
            for path in candidates:
                if os.path.exists(path):
                    server_path = path
                    break

        if server_path is None:
            logger.error("MCP server script not found")
            raise FileNotFoundError("Не удалось найти скрипт MCP сервера")

    logger.info(f"Launching MCP server from: {server_path}")

    # Запускаем MCP сервер как отдельный процесс
    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.dirname(os.path.abspath(server_path))
    env['PROJECT_ROOT'] = os.path.dirname(os.path.abspath(server_path))

    # Создаем временный файл для логов, чтобы не перегружать основной вывод
    log_file = os.path.join(os.path.dirname(__file__), "mcp_server_test.log")

    with open(log_file, 'w') as f:
        f.write(f"MCP Server Test Log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Запускаем сервер с перенаправлением stderr в лог-файл
    with open(log_file, 'a') as stderr_file:
        process = subprocess.Popen(
            [sys.executable, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=stderr_file,
            env=env,
            bufsize=0
        )

    # Ждем некоторое время, чтобы сервер запустился
    logger.info(f"Waiting {timeout} seconds for MCP server to start...")
    start_time = time.time()

    # Проверяем лог-файл на наличие признаков успешного запуска
    while time.time() - start_time < timeout:
        if process.poll() is not None:
            # Сервер неожиданно завершился
            logger.error(f"MCP server process exited with code {process.returncode}")
            with open(log_file, 'r') as f:
                log_content = f.read()
                logger.error(f"Server log: {log_content}")
            raise RuntimeError(f"MCP server failed to start, exit code: {process.returncode}")

        # Проверяем лог на признаки успешного запуска
        try:
            with open(log_file, 'r') as f:
                log_content = f.read()
                if "MCP Server started" in log_content or "initialized" in log_content.lower():
                    logger.info("MCP server successfully started")
                    break
        except Exception as e:
            logger.warning(f"Error reading log file: {str(e)}")

        time.sleep(0.1)

    return process, log_file

def run_test_with_server():
    """Запускает тест с автоматическим запуском сервера"""
    import argparse

    parser = argparse.ArgumentParser(description="Test MCP connection with PyCharm")
    parser.add_argument("--server", help="Path to MCP server script", default=None)
    parser.add_argument("--no-server", action="store_true", help="Don't start the server, assume it's already running")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout for operations in seconds")
    args = parser.parse_args()

    server_process = None

    try:
        # Запускаем сервер, если нужно
        if not args.no_server:
            try:
                server_process, log_file = launch_mcp_server(args.server, timeout=10)
            except Exception as e:
                logger.error(f"Failed to start MCP server: {str(e)}")
                return False

        # Запускаем тест
        if server_process:
            result = test_mcp_connection_direct(server_process)
        else:
            result = test_mcp_connection()

        if result:
            logger.info("✅ Test completed successfully!")
        else:
            logger.error("❌ Test failed")

        return result

    finally:
        # Останавливаем сервер, если он был запущен
        if server_process is not None:
            try:
                logger.info("Terminating MCP server process")
                server_process.terminate()
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning("MCP server did not terminate gracefully, killing...")
                server_process.kill()
            except Exception as e:
                logger.error(f"Error stopping MCP server: {str(e)}")

if __name__ == "__main__":
    try:
        run_test_with_server()
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        sys.exit(1)
