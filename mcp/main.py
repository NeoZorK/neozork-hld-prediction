#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Точка входа для запуска MCP сервера.
Запускается при интеграции с PyCharm и GitHub Copilot.
"""

import sys
from pathlib import Path
import traceback

# Добавляем родительскую директорию в PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from mcp.logger import setup_logging
from mcp.server import MCPServer
from mcp.handlers import MCPHandlers
from mcp.utils import get_file_context, get_python_completions, get_financial_completions, get_workspace_completions


def main():
    """Основная функция запуска сервера"""
    try:
        # Настройка логирования
        logger = setup_logging()
        logger.info("Запуск MCP сервера")

        # Создание экземпляра сервера
        server = MCPServer(logger)

        # Добавляем методы из utils.py в сервер
        server.get_file_context = lambda uri, line, character: get_file_context(server, uri, line, character)
        server.get_python_completions = lambda prefix, file_context: get_python_completions(server, prefix, file_context)
        server.get_financial_completions = lambda prefix: get_financial_completions(server, prefix)
        server.get_workspace_completions = lambda prefix: get_workspace_completions(server, prefix)

        # Устанавливаем обработчики запросов
        for method, handler in {
            "initialize": MCPHandlers.handle_initialize,
            "shutdown": MCPHandlers.handle_shutdown,
            "exit": MCPHandlers.handle_exit,
            "textDocument/completion": MCPHandlers.handle_completion,
            "workspace/symbols": MCPHandlers.handle_workspace_symbols,
            "workspace/files": MCPHandlers.handle_workspace_files,
            "textDocument/context": MCPHandlers.handle_document_context,
            "financialData/symbols": MCPHandlers.handle_financial_symbols,
            "financialData/timeframes": MCPHandlers.handle_financial_timeframes,
            "financialData/info": MCPHandlers.handle_financial_data_info,
            "financialData/summary": MCPHandlers.handle_financial_data_summary,
            "codeSearch/byName": MCPHandlers.handle_code_search_by_name,
            "codeSearch/references": MCPHandlers.handle_code_search_references,
            "codeSearch/definition": MCPHandlers.handle_code_search_definition,
        }.items():
            server.handlers[method] = lambda request_id, params, method=method, handler=handler: handler(server, request_id, params)

        # Запуск сервера
        server.start()

    except Exception as e:
        if 'logger' in locals():
            logger.error(f"Критическая ошибка при запуске сервера: {str(e)}")
            logger.error(traceback.format_exc())
        else:
            print(f"Критическая ошибка при запуске сервера: {str(e)}")
            print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
