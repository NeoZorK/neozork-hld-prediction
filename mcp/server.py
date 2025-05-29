#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Основной класс MCP сервера
"""

import json
import logging
import sys
import traceback
from datetime import datetime
from pathlib import Path
import re
import csv
import pandas as pd

# Импорт из локальных модулей
from mcp.code_indexer import CodeIndexer


class MCPServer:
    """Класс для обработки сообщений по протоколу MCP"""

    def __init__(self, logger):
        self.logger = logger
        self.running = True
        self.request_id_to_handler = {}
        self.project_root = Path.cwd()  # Текущая директория проекта
        self.project_files = {}
        self.file_content_cache = {}
        self.available_symbols = set()
        self.available_timeframes = set()
        self.financial_data_summary = {}

        # Инициализация системы индексации кода
        self.code_indexer = CodeIndexer(logger)

        # Сканируем файлы проекта при инициализации
        self.scan_project_files()

        # Сканируем данные финансовых инструментов
        self.scan_mql5_feed_data()

        # Индексируем код проекта
        self.index_project_code()

        # Регистрация обработчиков разных типов запросов
        self.handlers = {
            "initialize": self.handle_initialize,
            "shutdown": self.handle_shutdown,
            "exit": self.handle_exit,
            "textDocument/completion": self.handle_completion,
            "workspace/symbols": self.handle_workspace_symbols,
            "workspace/files": self.handle_workspace_files,
            "textDocument/context": self.handle_document_context,
            "financialData/symbols": self.handle_financial_symbols,
            "financialData/timeframes": self.handle_financial_timeframes,
            "financialData/info": self.handle_financial_data_info,
            "financialData/summary": self.handle_financial_data_summary,
            "codeSearch/byName": self.handle_code_search_by_name,
            "codeSearch/references": self.handle_code_search_references,
            "codeSearch/definition": self.handle_code_search_definition,
        }

        self.logger.info("MCP Server инициализирован")

    def scan_project_files(self):
        """Сканирование файлов проекта"""
        self.logger.info("Сканирование файлов проекта")
        try:
            # Создаем словарь для хранения информации о файлах
            self.project_files = {}
            self.file_content_cache = {}

            # Список расширений файлов, которые мы хотим сканировать
            code_extensions = ['.py', '.json', '.md', '.csv', '.txt']

            # Игнорируемые директории
            ignore_dirs = ['__pycache__', '.git', '.idea', 'logs']

            # Рекурсивный обход директорий
            for file_path in self.project_root.rglob('*'):
                # Пропускаем директории из списка игнорируемых
                if any(ignore_dir in str(file_path) for ignore_dir in ignore_dirs):
                    continue

                # Проверяем, что это файл, а не директория
                if file_path.is_file():
                    # Проверяем расширение файла
                    if file_path.suffix in code_extensions or file_path.suffix == '':
                        # Получаем относительный путь к файлу
                        relative_path = file_path.relative_to(self.project_root)
                        self.project_files[str(relative_path)] = {
                            'path': file_path,
                            'extension': file_path.suffix,
                            'size': file_path.stat().st_size,
                            'modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                        }

                        # Кэшируем содержимое только текстовых файлов и не слишком больших
                        if file_path.suffix in ['.py', '.json', '.md', '.txt'] and file_path.stat().st_size < 1024 * 1024:  # Не более 1 МБ
                            try:
                                self.file_content_cache[str(relative_path)] = file_path.read_text(encoding='utf-8')
                            except UnicodeDecodeError:
                                # Если возникла ошибка декодирования, файл может быть бинарным
                                self.logger.warning(f"Не удалось прочитать файл {relative_path} как текстовый")

            self.logger.info(f"Найдено файлов: {len(self.project_files)}")
        except Exception as e:
            self.logger.error(f"Ошибка при сканировании файлов проекта: {str(e)}")
            self.logger.error(traceback.format_exc())

    def scan_mql5_feed_data(self):
        """Сканирование и анализ данных финансовых инструментов из директории mql5_feed"""
        self.logger.info("Сканирование данных MQL5 Feed")

        self.available_symbols = set()
        self.available_timeframes = set()
        self.financial_data_summary = {}

        mql5_feed_dir = self.project_root / "mql5_feed"

        if not mql5_feed_dir.exists() or not mql5_feed_dir.is_dir():
            self.logger.warning(f"Директория {mql5_feed_dir} не найдена")
            return

        # Регулярное выражение для извлечения символа и таймфрейма из имени файла
        pattern = re.compile(r'CSVExport_([A-Z0-9\.]+)_PERIOD_([A-Z0-9]+)\.csv')

        csv_files = list(mql5_feed_dir.glob("*.csv"))
        self.logger.info(f"Найдено {len(csv_files)} CSV файлов в директории mql5_feed")

        for file_path in csv_files:
            match = pattern.match(file_path.name)
            if match:
                symbol, timeframe = match.groups()
                self.available_symbols.add(symbol)
                self.available_timeframes.add(timeframe)

                # Анализируем структуру CSV файла
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        headers = next(reader)  # Первая строка с заголовками

                        # Читаем первые 5 строк для определения типов данных
                        sample_data = []
                        for _ in range(5):
                            try:
                                sample_data.append(next(reader))
                            except StopIteration:
                                break

                    # Сохраняем метаданные о файле
                    key = f"{symbol}_{timeframe}"
                    self.financial_data_summary[key] = {
                        'path': str(file_path),
                        'symbol': symbol,
                        'timeframe': timeframe,
                        'columns': headers,
                        'sample_data': sample_data,
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                    }

                except Exception as e:
                    self.logger.error(f"Ошибка при анализе файла {file_path.name}: {str(e)}")

        self.logger.info(f"Найдены символы: {', '.join(sorted(self.available_symbols))}")
        self.logger.info(f"Найдены таймфреймы: {', '.join(sorted(self.available_timeframes))}")

    def index_project_code(self):
        """Индексирует код проекта"""
        self.logger.info("Индексирование кода проекта")
        try:
            for file_path, file_info in self.project_files.items():
                if file_info['extension'] == '.py':
                    content = self.file_content_cache.get(file_path)
                    if content:
                        self.code_indexer.index_python_file(file_path, content)
        except Exception as e:
            self.logger.error(f"Ошибка при индексировании кода проекта: {str(e)}")
            self.logger.error(traceback.format_exc())

    def start(self):
        """Запуск сервера и обработка входящих сообщений"""
        self.logger.info("MCP Server запущен и ожидает сообщений")

        while self.running:
            try:
                # Чтение заголовков
                headers = {}
                while True:
                    line = sys.stdin.readline().strip()
                    if not line:
                        break
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()

                if not headers:
                    continue

                # Чтение тела сообщения
                content_length = int(headers.get('Content-Length', 0))
                if content_length > 0:
                    body = sys.stdin.read(content_length)
                    self.logger.debug(f"Получено сообщение: {body}")
                    self.process_message(body)
                else:
                    self.logger.warning("Получено сообщение с нулевой длиной")

            except Exception as e:
                self.logger.error(f"Ошибка при обработке сообщения: {str(e)}")
                self.logger.error(traceback.format_exc())

    def process_message(self, message_str):
        """Обработка входящего сообщения"""
        try:
            message = json.loads(message_str)
            self.logger.debug(f"Обработка сообщения: {message}")

            # Проверка является ли сообщение запросом или ответом
            if "method" in message:
                # Это запрос
                request_id = message.get("id")
                method = message.get("method")
                params = message.get("params", {})

                self.logger.info(f"Получен запрос {method} с ID: {request_id}")

                # Вызов соответствующего обработчика метода
                if method in self.handlers:
                    self.handlers[method](request_id, params)
                else:
                    self.logger.warning(f"Неизвестный метод: {method}")
                    self.send_error_response(request_id, -32601, f"Метод {method} не поддерживается")

        except json.JSONDecodeError:
            self.logger.error(f"Ошибка декодирования JSON: {message_str}")
        except Exception as e:
            self.logger.error(f"Ошибка при обработке сообщения: {str(e)}")
            self.logger.error(traceback.format_exc())

    def send_response(self, request_id, result):
        """Отправка ответа на запрос"""
        if request_id is None:
            return

        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }

        self.send_message(response)

    def send_error_response(self, request_id, code, message, data=None):
        """Отправка ответа с ошибкой"""
        if request_id is None:
            return

        error = {
            "code": code,
            "message": message
        }

        if data:
            error["data"] = data

        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": error
        }

        self.send_message(response)

    def send_message(self, message):
        """Отправка сообщения клиенту"""
        message_str = json.dumps(message)
        content_length = len(message_str)

        # Формирование и отправка сообщения
        response = f"Content-Length: {content_length}\r\n\r\n{message_str}"
        sys.stdout.write(response)
        sys.stdout.flush()

        self.logger.debug(f"Отправлено сообщение: {message_str}")
