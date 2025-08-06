# MCP Server Docker Issue Analysis

## Проблема

MCP сервер в Docker контейнере показывает противоречивые результаты:

- ✅ Сервер запускается и инициализируется
- ✅ Процесс работает (PID найден)
- ❌ Ping запросы таймаутят
- ❌ Сокет-соединения не работают

## Диагностика

### 1. Анализ логов

```
🚀 Starting Neozork Unified MCP Server...
📁 Project root: /app
🐍 Python version: 3.11.13
📅 Started at: 2025-08-06 19:58:50
🎯 Server mode: unified
📊 Scanning project files...
🔍 Indexing code...
✅ Neozork Unified MCP Server initialized successfully
📈 Server Statistics:
   - Project files: 7021
   - Financial symbols: 11
   - Timeframes: 9
   - Functions indexed: 102889
   - Classes indexed: 11004
🔄 Server is ready to accept connections...
🔄 Starting MCP server loop...
🐳 Running in Docker mode - using socket communication
🔌 MCP Socket Server listening on localhost:8080
```

### 2. Проблемы найдены

1. **Переменная окружения**: `DOCKER_CONTAINER=true` установлена правильно
2. **Docker режим**: Сервер определяет Docker среду корректно
3. **Сокет-сервер**: Запускается на localhost:8080
4. **Проблема**: Сокет не принимает соединения

### 3. Тестирование порта

```bash
# Проверка порта
python3 -c "import socket; s=socket.socket(); print('Port 8080:', s.connect_ex(('localhost', 8080))); s.close()"
# Результат: Port 8080: 111 (Connection refused)
```

## Корень проблемы

### Проблема 1: Блокирующий сокет

В методе `_start_docker_mode()` сокет-сервер блокируется на `accept()` и не может принимать соединения из-за:

1. **Таймаут**: Сокет имеет таймаут 1 секунду
2. **Блокировка**: Основной поток блокируется на `accept()`
3. **Отсутствие обработки ошибок**: Нет обработки исключений

### Проблема 2: Неправильная обработка сообщений

В методе `_handle_socket_client()` есть проблемы с:

1. **JSON парсинг**: Неправильная обработка JSON сообщений
2. **Обработка ошибок**: Нет обработки исключений
3. **Закрытие соединений**: Неправильное закрытие сокетов

## Решения

### 1. Исправление сокет-сервера

```python
def _start_docker_mode(self):
    """Start MCP server in Docker mode with socket communication"""
    import socket
    import threading
    
    # Create socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8080))  # Bind to all interfaces
    server_socket.listen(5)
    server_socket.settimeout(1.0)  # 1 second timeout
    
    print_to_stderr("🔌 MCP Socket Server listening on 0.0.0.0:8080")
    
    try:
        while self.running:
            try:
                client_socket, address = server_socket.accept()
                print_to_stderr(f"📡 New connection from {address}")
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self._handle_socket_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    self.logger.error(f"Error accepting connection: {e}")
                break
                
    except Exception as e:
        self.logger.error(f"Error starting socket server: {e}")
    finally:
        server_socket.close()
```

### 2. Исправление обработки клиентов

```python
def _handle_socket_client(self, client_socket, address):
    """Handle socket client communication"""
    try:
        while self.running:
            # Receive data
            data = client_socket.recv(4096)
            if not data:
                break
            
            try:
                message = json.loads(data.decode('utf-8'))
                self.logger.info(f"Received message from {address}: {message.get('method', 'unknown')}")
                
                # Process message using MCP server
                method = message.get("method")
                request_id = message.get("id")
                params = message.get("params", {})
                
                if hasattr(self, 'handlers') and method in self.handlers:
                    result = self.handlers[method](request_id, params)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}"
                        }
                    }
                
                # Send response
                client_socket.send(json.dumps(response).encode('utf-8'))
                
            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {e}"
                    }
                }
                client_socket.send(json.dumps(error_response).encode('utf-8'))
                
    except Exception as e:
        self.logger.error(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()
        print_to_stderr(f"📡 Connection from {address} closed")
```

### 3. Улучшение тестирования

```python
def test_mcp_socket_connection():
    """Test connection to MCP socket server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 8080))
        
        # Test ping request
        test_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "neozork/ping",
            "params": {}
        }
        
        sock.send(json.dumps(test_message).encode('utf-8'))
        response = sock.recv(4096)
        response_data = json.loads(response.decode('utf-8'))
        
        if response_data.get("result", {}).get("pong"):
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Socket test failed: {e}")
        return False
    finally:
        sock.close()
```

## Рекомендации

### 1. Немедленные исправления

1. **Изменить bind адрес**: `localhost` → `0.0.0.0`
2. **Улучшить обработку ошибок**: Добавить try-catch блоки
3. **Исправить JSON парсинг**: Правильная обработка сообщений
4. **Добавить логирование**: Подробные логи для диагностики

### 2. Долгосрочные улучшения

1. **Мониторинг**: Добавить health checks
2. **Метрики**: Сбор статистики соединений
3. **Конфигурация**: Настройка портов и адресов
4. **Безопасность**: Аутентификация и авторизация

### 3. Тестирование

1. **Unit тесты**: Тестирование отдельных компонентов
2. **Integration тесты**: Тестирование полного цикла
3. **Load тесты**: Тестирование под нагрузкой
4. **Docker тесты**: Тестирование в контейнере

## Заключение

Проблема в том, что MCP сервер запускается в Docker режиме, но сокет-сервер не может принимать соединения из-за неправильной конфигурации и обработки ошибок. Необходимо исправить bind адрес, улучшить обработку ошибок и добавить правильное логирование. 