#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Обработчики различных типов запросов MCP сервера
"""

from pathlib import Path


class MCPHandlers:
    """Обработчики различных типов запросов MCP сервера"""

    @staticmethod
    def handle_initialize(server, request_id, params):
        """Обработка запроса initialize"""
        server.logger.info("Обработка запроса initialize")

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

        server.send_response(request_id, result)

    @staticmethod
    def handle_shutdown(server, request_id, params):
        """Обработка запроса shutdown"""
        server.logger.info("Обработка запроса shutdown")

        # Отправляем пустой результат как указано в спецификации LSP
        server.send_response(request_id, None)

        # Фактическое завершение работы происходит при получении запроса exit
        # Но мы должны подготовиться к завершению

    @staticmethod
    def handle_exit(server, request_id, params):
        """Обработка запроса exit"""
        server.logger.info("Получен запрос exit, завершение работы сервера")
        server.running = False

        # Exit не требует ответа

    @staticmethod
    def handle_completion(server, request_id, params):
        """Обработка запроса на автодополнение"""
        server.logger.info("Обработка запроса на автодополнение")

        try:
            # Получаем информацию о текущем документе и позиции курсора
            text_document = params.get("textDocument", {})
            position = params.get("position", {})

            if not text_document or not position:
                server.send_error_response(request_id, -32602, "Не указан документ или позиция курсора")
                return

            uri = text_document.get("uri", "")
            line = position.get("line", 0)
            character = position.get("character", 0)

            # Получаем контекст файла и строки
            file_context = server.get_file_context(uri, line, character)
            if not file_context:
                # Если не удалось получить контекст, возвращаем пустой список
                result = {
                    "isIncomplete": False,
                    "items": []
                }
                server.send_response(request_id, result)
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
                completion_items.extend(server.get_python_completions(prefix, file_context))

            # Если в тексте есть упоминания о финансовых символах или таймфреймах
            if any(symbol in prefix for symbol in server.available_symbols) or \
               any(timeframe in prefix for timeframe in server.available_timeframes):
                completion_items.extend(server.get_financial_completions(prefix))

            # Добавляем общие символы рабочего пространства
            completion_items.extend(server.get_workspace_completions(prefix))

            # Возвращаем результат с найденными элементами автодополнения
            result = {
                "isIncomplete": False,
                "items": completion_items
            }

            server.send_response(request_id, result)

        except Exception as e:
            server.logger.error(f"Ошибка при обработке запроса на автодополнение: {str(e)}")
            import traceback
            server.logger.error(traceback.format_exc())
            server.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

    @staticmethod
    def handle_workspace_symbols(server, request_id, params):
        """Обработка запроса символов рабочего пространства"""
        server.logger.info("Обработка запроса workspace/symbols")

        # Здесь должна быть логика поиска символов в рабочем пространстве
        # В качестве заглушки возвращаем пустой список
        result = []

        server.send_response(request_id, result)

    @staticmethod
    def handle_workspace_files(server, request_id, params):
        """Обработка запроса файлов рабочего пространства"""
        server.logger.info("Обработка запроса workspace/files")
        result = list(server.project_files.keys())
        server.send_response(request_id, result)

    @staticmethod
    def handle_document_context(server, request_id, params):
        """Обработка запроса контекста документа"""
        server.logger.info("Обработка запроса textDocument/context")
        try:
            file_path = params.get("textDocument", {}).get("uri")
            if not file_path:
                server.send_error_response(request_id, -32602, "Не указан путь к файлу")
                return

            relative_path = Path(file_path).relative_to(server.project_root)
            content = server.file_content_cache.get(str(relative_path))
            if content is None:
                server.send_error_response(request_id, -32602, f"Файл {file_path} не найден")
                return

            result = {
                "content": content
            }
            server.send_response(request_id, result)
        except Exception as e:
            server.logger.error(f"Ошибка при обработке контекста документа: {str(e)}")
            import traceback
            server.logger.error(traceback.format_exc())
            server.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

    @staticmethod
    def handle_financial_symbols(server, request_id, params):
        """Обработка запроса financialData/symbols"""
        server.logger.info("Обработка запроса financialData/symbols")
        result = list(server.available_symbols)
        server.send_response(request_id, result)

    @staticmethod
    def handle_financial_timeframes(server, request_id, params):
        """Обработка запроса financialData/timeframes"""
        server.logger.info("Обработка запроса financialData/timeframes")
        result = list(server.available_timeframes)
        server.send_response(request_id, result)

    @staticmethod
    def handle_financial_data_info(server, request_id, params):
        """Обработка запроса financialData/info"""
        server.logger.info("Обработка запроса financialData/info")
        try:
            symbol = params.get("symbol")
            timeframe = params.get("timeframe")
            key = f"{symbol}_{timeframe}"
            data_info = server.financial_data_summary.get(key)
            if not data_info:
                server.send_error_response(request_id, -32602, f"Данные для {symbol} и {timeframe} не найдены")
                return
            server.send_response(request_id, data_info)
        except Exception as e:
            server.logger.error(f"Ошибка при обработке financialData/info: {str(e)}")
            import traceback
            server.logger.error(traceback.format_exc())
            server.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

    @staticmethod
    def handle_financial_data_summary(server, request_id, params):
        """Обработка запроса financialData/summary"""
        server.logger.info("Обработка запроса financialData/summary")
        result = server.financial_data_summary
        server.send_response(request_id, result)

    @staticmethod
    def handle_code_search_by_name(server, request_id, params):
        """Обработка запроса codeSearch/byName"""
        server.logger.info("Обработка запроса codeSearch/byName")
        try:
            name = params.get("name")
            if not name:
                server.send_error_response(request_id, -32602, "Не указано имя для поиска")
                return

            result = {
                "functions": server.code_indexer.code_index['functions'].get(name, []),
                "classes": server.code_indexer.code_index['classes'].get(name, []),
                "variables": server.code_indexer.code_index['variables'].get(name, []),
                "imports": server.code_indexer.code_index['imports'].get(name, [])
            }
            server.send_response(request_id, result)
        except Exception as e:
            server.logger.error(f"Ошибка при обработке codeSearch/byName: {str(e)}")
            import traceback
            server.logger.error(traceback.format_exc())
            server.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

    @staticmethod
    def handle_code_search_references(server, request_id, params):
        """Обработка запроса codeSearch/references"""
        server.logger.info("Обработка запроса codeSearch/references")
        try:
            name = params.get("name")
            if not name:
                server.send_error_response(request_id, -32602, "Не указано имя для поиска ссылок")
                return

            result = {
                "references": server.code_indexer.get_references(name)
            }
            server.send_response(request_id, result)
        except Exception as e:
            server.logger.error(f"Ошибка при обработке codeSearch/references: {str(e)}")
            import traceback
            server.logger.error(traceback.format_exc())
            server.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")

    @staticmethod
    def handle_code_search_definition(server, request_id, params):
        """Обработка запроса codeSearch/definition"""
        server.logger.info("Обработка запроса codeSearch/definition")
        try:
            name = params.get("name")
            if not name:
                server.send_error_response(request_id, -32602, "Не указано имя для поиска определения")
                return

            result = {
                "definition": server.code_indexer.get_definitions(name)
            }
            server.send_response(request_id, result)
        except Exception as e:
            server.logger.error(f"Ошибка при обработке codeSearch/definition: {str(e)}")
            import traceback
            server.logger.error(traceback.format_exc())
            server.send_error_response(request_id, -32603, "Внутренняя ошибка сервера")
