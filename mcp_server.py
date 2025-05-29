#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP (Model Completion Protocol) Server для GitHub Copilot
Работает через стандартный ввод/вывод (STDIO)
"""

import json
import logging
import os
import sys
import traceback
from datetime import datetime
import uuid
from pathlib import Path
import glob
import re
import csv
import pandas as pd
import ast
import keyword

# Настройка логирования
def setup_logging():
    """Настройка системы логирования"""
    try:
        log_dir = Path(__file__).parent / "logs"
        print(f"Попытка создать директорию логов по пути: {log_dir.absolute()}")
        # Автоматически создаем директорию logs, если она не существует
        log_dir.mkdir(exist_ok=True)
        print(f"Директория логов создана или уже существует: {log_dir.exists()}")
        log_file = log_dir / "mcp_server.log"

        # Создание форматировщика для логов
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(name)s] [Session: %(session_id)s] %(message)s'
        )

        # Настройка обработчика файла
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)

        # Настройка логгера
        logger = logging.getLogger('mcp_server')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

        # Добавляем session_id в контекст логгера
        session_id = str(uuid.uuid4())
        extra = {'session_id': session_id}
        logger = logging.LoggerAdapter(logger, extra)

        # Добавим разделитель сессий в лог-файл
        logger.info("="*80)
        logger.info(f"Начало новой сессии MCP сервера: {session_id}")
        logger.info("="*80)

        return logger
    except Exception as e:
        print(f"Ошибка при настройке логирования: {str(e)}")
        print(traceback.format_exc())
        # Создаем базовый логгер без файлового обработчика
        logger = logging.getLogger('mcp_server')
        logger.setLevel(logging.DEBUG)
        session_id = str(uuid.uuid4())
        extra = {'session_id': session_id}
        return logging.LoggerAdapter(logger, extra)

# Класс для обработки сообщений по протоколу MCP
class MCPServer:
    def __init__(self, logger):
        self.logger = logger
        self.running = True
        self.request_id_to_handler = {}
        self.project_root = Path(__file__).parent
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
            # Добавьте другие обработчики по мере необходимости
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

            # Здесь можно добавить обработку ответов от клиента,
            # если таковые ожидаются

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

    # Обработчики различных методов MCP

    def handle_initialize(self, request_id, params):
        """Обработка запроса initialize"""
        self.logger.info("Обработка запроса initialize")

        # Версия протокола и возможности сервера
        capabilities = {
            "completionProvider": {
                "triggerCharacters": ["."]
            },
            "workspaceSymbolProvider": True,
            # Дополнительные возможности при необходимости
        }

        result = {
            "capabilities": capabilities,
            "serverInfo": {
                "name": "Neozork MCP Server",
                "version": "1.0.0"
            }
        }

        self.send_response(request_id, result)

    def handle_shutdown(self, request_id, params):
        """Обработка запроса shutdown"""
        self.logger.info("Обработка запроса shutdown")

        # Отправляем пустой результат как указано в спецификации LSP
        self.send_response(request_id, None)

        # Фактическое завершение работы происходит при получении запроса exit
        # Но мы должны подготовиться к завершению

    def handle_exit(self, request_id, params):
        """Обработка запроса exit"""
        self.logger.info("Получен запрос exit, завершение работы сервера")
        self.running = False

        # Exit не требует ответа

    def handle_completion(self, request_id, params):
        """Обработка запроса на автодополнение"""
        self.logger.info("Обработка запроса на автодополнение")

        try:
            # Получаем информацию о текущем документе и позиции курсора
            text_document = params.get("textDocument", {})
            position = params.get("position", {})

            if not text_document or not position:
                self.send_error_response(request_id, -32602, "Не указан документ или позиция курсора")
                return

            uri = text_document.get("uri", "")
            line = position.get("line", 0)
            character = position.get("character", 0)

            # Получаем контекст файла и строки
            file_context = self.get_file_context(uri, line, character)
            if not file_context:
                # Если не удалось получить контекст, возвращаем пустой список
                result = {
                    "isIncomplete": False,
                    "items": []
                }
                self.send_response(request_id, result)
                return

            # Определяем тип файла по расширению
            file_extension = Path(uri).suffix.lower()

            # Массив для элементов автодополнения
            completion_items = []

            # Анализируем текущую строку для определения контекста
            current_line = file_context.get("current_line", "")
            prefix = current_line[:character]

            # Если это Python файл
            if file_extension == '.py':
                completion_items.extend(self.get_python_completions(prefix, file_context))

            # Если в тексте есть упоминания о финансовых символах или таймфреймах
            if any(symbol in prefix for symbol in self.available_symbols) or \
               any(timeframe in prefix for timeframe in self.available_timeframes):
                completion_items.extend(self.get_financial_completions(prefix))

            # Добавляем общие символы рабочего пространства
            completion_items.extend(self.get_workspace_completions(prefix))

            # Возвращаем результат с найденными элементами автодополнения
            result = {
                "isIncomplete": False,
                "items": completion_items
            }

            self.send_response(request_id, result)

        except Exception as e:
            self.logger.error(f"Ошибка при обработке запроса на автодополнение: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

    def get_file_context(self, uri, line, character):
        """Получает контекст файла для автодополнения"""
        try:
            file_path = Path(uri)
            if not file_path.exists():
                # Пробуем получить файл из нашего кэша
                relative_path = file_path.relative_to(self.project_root)
                content = self.file_content_cache.get(str(relative_path))
                if not content:
                    return None

                lines = content.splitlines()
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

            # Проверяем валидность номера строки
            if line >= len(lines):
                return None

            # Получаем текущую строку
            current_line = lines[line].rstrip('\r\n')

            # Получаем предыдущие 5 строк для контекста
            start_line = max(0, line - 5)
            previous_lines = lines[start_line:line]

            # Получаем следующие 5 строк для контекста
            end_line = min(len(lines), line + 5)
            next_lines = lines[line+1:end_line]

            return {
                "current_line": current_line,
                "previous_lines": previous_lines,
                "next_lines": next_lines,
                "full_content": lines
            }

        except Exception as e:
            self.logger.error(f"Ошибка при получении контекста файла: {str(e)}")
            return None

    def get_python_completions(self, prefix, file_context):
        """Генерирует предложения автодополнения для Python файлов"""
        completion_items = []

        # Основные ключевые слова Python
        python_keywords = ["def", "class", "if", "else", "elif", "for", "while", "try", "except",
                          "finally", "with", "import", "from", "as", "return", "yield", "lambda",
                          "True", "False", "None", "and", "or", "not", "in", "is"]

        # Полезные методы для работы с финансовыми данными
        finance_methods = [
            {
                "label": "load_financial_data",
                "kind": 3,  # Function
                "detail": "Загрузка финансовых данных из CSV файла",
                "documentation": "load_financial_data(symbol, timeframe)\nЗагружает данные для указанного символа и таймфрейма",
                "insertText": "load_financial_data('${1:symbol}', '${2:timeframe}')"
            },
            {
                "label": "calculate_sma",
                "kind": 3,  # Function
                "detail": "Расчет простой скользящей средней (SMA)",
                "documentation": "calculate_sma(data, period)\nРассчитывает простую скользящую среднюю для указанных данных",
                "insertText": "calculate_sma(${1:data}, ${2:period})"
            },
            {
                "label": "calculate_ema",
                "kind": 3,  # Function
                "detail": "Расчет экспоненциальной скользящей средней (EMA)",
                "documentation": "calculate_ema(data, period)\nРассчитывает экспоненциальную скользящую среднюю для указанных данных",
                "insertText": "calculate_ema(${1:data}, ${2:period})"
            },
            {
                "label": "predict_trend",
                "kind": 3,  # Function
                "detail": "Предсказание тренда цены",
                "documentation": "predict_trend(data)\nПредсказывает направление движения цены на основе исторических данных",
                "insertText": "predict_trend(${1:data})"
            }
        ]

        # Если есть импорт pandas, добавляем методы pandas
        if "import pandas" in "\n".join(file_context.get("previous_lines", [])) or "from pandas" in "\n".join(file_context.get("previous_lines", [])):
            pandas_methods = [
                {
                    "label": "pd.read_csv",
                    "kind": 3,  # Function
                    "detail": "Загрузка данных из CSV файла",
                    "documentation": "pd.read_csv(filepath_or_buffer, sep=',', header='infer', ...)\nЧитает файл CSV в DataFrame",
                    "insertText": "pd.read_csv('${1:filepath}')"
                },
                {
                    "label": "pd.DataFrame",
                    "kind": 3,  # Function
                    "detail": "Создание DataFrame",
                    "documentation": "pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)\nСоздает двумерную структуру данных с метками строк и столбцов",
                    "insertText": "pd.DataFrame(${1:data})"
                },
                {
                    "label": "df.rolling",
                    "kind": 3,  # Method
                    "detail": "Скользящее окно для DataFrame",
                    "documentation": "df.rolling(window, min_periods=None, center=False, ...)\nСоздает объект скользящего окна для расчета статистики",
                    "insertText": "df.rolling(${1:window}).${2:mean}()"
                }
            ]
            completion_items.extend(pandas_methods)

        # Добавляем ключевые слова Python
        for keyword in python_keywords:
            if keyword.startswith(prefix.strip()):
                completion_items.append({
                    "label": keyword,
                    "kind": 14,  # Keyword
                    "detail": "Ключевое слово Python",
                    "insertText": keyword
                })

        # Добавляем методы для работы с финансовыми данными
        completion_items.extend(finance_methods)

        return completion_items

    def get_financial_completions(self, prefix):
        """Генерирует предложения автодополнения для финансовых данных"""
        completion_items = []

        # Добавляем доступные символы
        for symbol in sorted(self.available_symbols):
            completion_items.append({
                "label": symbol,
                "kind": 14,  # Constant
                "detail": f"Финансовый символ",
                "documentation": f"Символ {symbol} доступен в таймфреймах: {', '.join(sorted(self.available_timeframes))}",
                "insertText": symbol
            })

        # Добавляем доступные таймфреймы
        for timeframe in sorted(self.available_timeframes):
            completion_items.append({
                "label": timeframe,
                "kind": 14,  # Constant
                "detail": f"Таймфрейм",
                "documentation": f"Таймфрейм {timeframe} (период)",
                "insertText": timeframe
            })

        # Добавляем специальные функции для анализа финансовых данных
        data_analysis_snippets = [
            {
                "label": "load_and_analyze",
                "kind": 15,  # Snippet
                "detail": "Загрузка и анализ финансовых данных",
                "documentation": "Загружает данные для указанного символа и таймфрейма и выполняет базовый анализ",
                "insertText": "# Загрузка данных\ncsv_path = 'mql5_feed/CSVExport_${1:BTCUSD}_PERIOD_${2:D1}.csv'\ndf = pd.read_csv(csv_path)\n\n# Преобразование времени\ndf['time'] = pd.to_datetime(df['time'])\ndf.set_index('time', inplace=True)\n\n# Расчет индикаторов\ndf['sma_20'] = df['close'].rolling(window=20).mean()\ndf['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()\n\n# Визуализация\nplt.figure(figsize=(12, 6))\nplt.plot(df.index, df['close'], label='Close')\nplt.plot(df.index, df['sma_20'], label='SMA 20')\nplt.plot(df.index, df['ema_50'], label='EMA 50')\nplt.legend()\nplt.title('${1:BTCUSD} - ${2:D1}')\nplt.show()"
            },
            {
                "label": "predict_hld",
                "kind": 15,  # Snippet
                "detail": "Предсказание HLD (High, Low, Direction)",
                "documentation": "Создает модель для предсказания максимальных и минимальных значений, а также направления тренда",
                "insertText": "# Подготовка данных для предсказания HLD\ndef prepare_hld_data(df):\n    # Добавляем лаги цен\n    for i in range(1, 6):\n        df[f'close_lag_{i}'] = df['close'].shift(i)\n        df[f'high_lag_{i}'] = df['high'].shift(i)\n        df[f'low_lag_{i}'] = df['low'].shift(i)\n    \n    # Добавляем целевые переменные\n    df['next_high'] = df['high'].shift(-1)\n    df['next_low'] = df['low'].shift(-1)\n    df['next_direction'] = np.where(df['close'].shift(-1) > df['close'], 1, -1)\n    \n    # Удаляем строки с NaN\n    df.dropna(inplace=True)\n    \n    return df\n\n# Загрузка данных\ncsv_path = 'mql5_feed/CSVExport_${1:BTCUSD}_PERIOD_${2:D1}.csv'\ndf = pd.read_csv(csv_path)\ndf['time'] = pd.to_datetime(df['time'])\n\n# Подготовка данных\ndf_prepared = prepare_hld_data(df)\n\n# Обучение моделей\n# ... код для обучения моделей ...\n\n# Предсказание\n# ... код для предсказания ...\n"
            }
        ]

        completion_items.extend(data_analysis_snippets)

        return completion_items

    def get_workspace_completions(self, prefix):
        """Генерирует предложения автодополнения на основе файлов рабочего пространства"""
        completion_items = []

        # Анализируем Python файлы в проекте для поиска классов и функций
        python_files = [path for path in self.project_files.keys() if path.endswith('.py')]

        for file_path in python_files:
            try:
                content = self.file_content_cache.get(file_path)
                if not content:
                    continue

                # Ищем определения функций
                func_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):', re.MULTILINE)
                functions = func_pattern.findall(content)

                # Ищем определения классов
                class_pattern = re.compile(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(\(.*?\))?:', re.MULTILINE)
                classes = class_pattern.findall(content)

                # Добавляем найденные функции в автодополнение
                for func_name, params in functions:
                    if func_name.startswith(prefix.strip()) or prefix.strip() == "":
                        completion_items.append({
                            "label": func_name,
                            "kind": 3,  # Function
                            "detail": f"Функция из {file_path}",
                            "documentation": f"def {func_name}({params})",
                            "insertText": func_name
                        })

                # Добавляем найденные классы в автодополнение
                for class_name, _ in classes:
                    if class_name.startswith(prefix.strip()) or prefix.strip() == "":
                        completion_items.append({
                            "label": class_name,
                            "kind": 7,  # Class
                            "detail": f"Класс из {file_path}",
                            "documentation": f"class {class_name}",
                            "insertText": class_name
                        })

            except Exception as e:
                self.logger.error(f"Ошибка при анализе файла {file_path}: {str(e)}")

        return completion_items

    def handle_workspace_symbols(self, request_id, params):
        """Обработка запроса символов рабочего пространства"""
        self.logger.info("Обработка запроса workspace/symbols")

        # Здесь должна быть логика поиска символов в рабочем пространстве
        # В качестве заглушки возвращаем пустой список
        result = []

        self.send_response(request_id, result)

    def handle_workspace_files(self, request_id, params):
        """Обработка запроса файлов рабочего пространства"""
        self.logger.info("Обработка запроса workspace/files")
        result = list(self.project_files.keys())
        self.send_response(request_id, result)

    def handle_document_context(self, request_id, params):
        """Обработка запроса контекста документа"""
        self.logger.info("Обработка запроса textDocument/context")
        try:
            file_path = params.get("textDocument", {}).get("uri")
            if not file_path:
                self.send_error_response(request_id, -32602, "Не указан путь к файлу")
                return

            relative_path = Path(file_path).relative_to(self.project_root)
            content = self.file_content_cache.get(str(relative_path))
            if content is None:
                self.send_error_response(request_id, -32602, f"Файл {file_path} не найден")
                return

            result = {
                "content": content
            }
            self.send_response(request_id, result)
        except Exception as e:
            self.logger.error(f"Ошибка при обработке контекста документа: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

    def handle_financial_symbols(self, request_id, params):
        """Обработка запроса financialData/symbols"""
        self.logger.info("Обработка запроса financialData/symbols")
        result = list(self.available_symbols)
        self.send_response(request_id, result)

    def handle_financial_timeframes(self, request_id, params):
        """Обработка запроса financialData/timeframes"""
        self.logger.info("Обработка запроса financialData/timeframes")
        result = list(self.available_timeframes)
        self.send_response(request_id, result)

    def handle_financial_data_info(self, request_id, params):
        """Обработка запроса financialData/info"""
        self.logger.info("Обработка запроса financialData/info")
        try:
            symbol = params.get("symbol")
            timeframe = params.get("timeframe")
            key = f"{symbol}_{timeframe}"
            data_info = self.financial_data_summary.get(key)
            if not data_info:
                self.send_error_response(request_id, -32602, f"Данные для {symbol} и {timeframe} не найдены")
                return
            self.send_response(request_id, data_info)
        except Exception as e:
            self.logger.error(f"Ошибка при обработке financialData/info: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

    def handle_financial_data_summary(self, request_id, params):
        """Обработка запроса financialData/summary"""
        self.logger.info("Обработка запроса financialData/summary")
        result = self.financial_data_summary
        self.send_response(request_id, result)

    def handle_code_search_by_name(self, request_id, params):
        """Обработка запроса codeSearch/byName"""
        self.logger.info("Обработка запроса codeSearch/byName")
        try:
            name = params.get("name")
            if not name:
                self.send_error_response(request_id, -32602, "Не указано имя для поиска")
                return

            result = {
                "functions": self.code_indexer.code_index['functions'].get(name, []),
                "classes": self.code_indexer.code_index['classes'].get(name, []),
                "variables": self.code_indexer.code_index['variables'].get(name, []),
                "imports": self.code_indexer.code_index['imports'].get(name, [])
            }
            self.send_response(request_id, result)
        except Exception as e:
            self.logger.error(f"Ошибка при обработке codeSearch/byName: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

    def handle_code_search_references(self, request_id, params):
        """Обработка запроса codeSearch/references"""
        self.logger.info("Обработка запроса codeSearch/references")
        try:
            name = params.get("name")
            if not name:
                self.send_error_response(request_id, -32602, "Не указано имя для поиска ссылок")
                return

            result = {
                "references": self.code_indexer.get_references(name)
            }
            self.send_response(request_id, result)
        except Exception as e:
            self.logger.error(f"Ошибка при обработке codeSearch/references: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

    def handle_code_search_definition(self, request_id, params):
        """Обработка запроса codeSearch/definition"""
        self.logger.info("Обработка запроса codeSearch/definition")
        try:
            name = params.get("name")
            if not name:
                self.send_error_response(request_id, -32602, "Не указано имя для поиска определения")
                return

            result = {
                "definition": self.code_indexer.get_definitions(name)
            }
            self.send_response(request_id, result)
        except Exception as e:
            self.logger.error(f"Ошибка при обработке codeSearch/definition: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

class CodeIndexer:
    """Класс для индексации и поиска элементов кода в проекте"""

    def __init__(self, logger):
        self.logger = logger

        # Структура для хранения индексированного кода
        self.code_index = {
            'functions': {},  # имя_функции -> [файлы, где она определена]
            'classes': {},    # имя_класса -> [файлы, где он определен]
            'variables': {},  # имя_переменной -> [файлы, где она определена/используется]
            'imports': {},    # имя_импорта -> [файлы, где он используется]
            'docstrings': {}  # (имя, тип) -> docstring
        }

        self.logger.info("Инициализирован индексатор кода")

    def index_python_file(self, file_path, content):
        """Индексирует содержимое Python файла"""
        try:
            # Парсим содержимое файла в AST
            tree = ast.parse(content)

            # Извлекаем имена и типы элементов кода
            for node in ast.walk(tree):
                # Индексируем функции
                if isinstance(node, ast.FunctionDef):
                    self._index_function(node, file_path)

                # Индексируем классы
                elif isinstance(node, ast.ClassDef):
                    self._index_class(node, file_path)

                # Индексируем импорты
                elif isinstance(node, ast.Import):
                    self._index_import(node, file_path)

                # Индексируем from-импорты
                elif isinstance(node, ast.ImportFrom):
                    self._index_import_from(node, file_path)

                # Индексируем переменные
                elif isinstance(node, ast.Assign):
                    self._index_variable(node, file_path)

            self.logger.debug(f"Успешно проиндексирован файл {file_path}")

        except Exception as e:
            self.logger.error(f"Ошибка при индексации файла {file_path}: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _index_function(self, node, file_path):
        """Индексирует функцию"""
        func_name = node.name

        # Пропускаем "приватные" функции (начинающиеся с _)
        if func_name.startswith('_') and not func_name.startswith('__'):
            return

        # Добавляем информацию о функции в индекс
        if func_name not in self.code_index['functions']:
            self.code_index['functions'][func_name] = []

        if file_path not in self.code_index['functions'][func_name]:
            self.code_index['functions'][func_name].append(file_path)

        # Извлекаем и сохраняем docstring
        docstring = ast.get_docstring(node)
        if docstring:
            self.code_index['docstrings'][(func_name, 'function')] = docstring

    def _index_class(self, node, file_path):
        """Индексирует класс"""
        class_name = node.name

        # Пропускаем "приватные" классы (начинающиеся с _)
        if class_name.startswith('_') and not class_name.startswith('__'):
            return

        # Добавляем информацию о классе в индекс
        if class_name not in
