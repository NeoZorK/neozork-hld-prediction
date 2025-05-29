#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль настройки логирования для MCP сервера
"""

import logging
import uuid
from pathlib import Path


def setup_logging():
    """Настройка системы логирования"""
    try:
        # Определяем путь к директории логов относительно текущего файла
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
        import traceback
        print(traceback.format_exc())
        # Создаем базовый логгер без файлового обработчика
        logger = logging.getLogger('mcp_server')
        logger.setLevel(logging.DEBUG)
        session_id = str(uuid.uuid4())
        extra = {'session_id': session_id}
        return logging.LoggerAdapter(logger, extra)
