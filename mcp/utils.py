#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Утилиты для работы с MCP сервером
"""

import keyword
import re
from pathlib import Path


def get_file_context(server, uri, line, character):
    """Получает контекст файла для автодополнения"""
    try:
        file_path = Path(uri)
        if not file_path.exists():
            # Пробуем получить файл из нашего кэша
            relative_path = file_path.relative_to(server.project_root)
            content = server.file_content_cache.get(str(relative_path))
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
        server.logger.error(f"Ошибка при получении контекста файла: {str(e)}")
        return None


def get_python_completions(server, prefix, file_context):
    """Генерирует предложения автодополнения для Python файлов"""
    completion_items = []

    # Основные ключевые слова Python
    python_keywords = keyword.kwlist

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


def get_financial_completions(server, prefix):
    """Генерирует предложения автодополнения для финансовых данных"""
    completion_items = []

    # Добавляем доступные символы
    for symbol in sorted(server.available_symbols):
        completion_items.append({
            "label": symbol,
            "kind": 14,  # Constant
            "detail": f"Финансовый символ",
            "documentation": f"Символ {symbol} доступен в таймфреймах: {', '.join(sorted(server.available_timeframes))}",
            "insertText": symbol
        })

    # Добавляем доступные таймфреймы
    for timeframe in sorted(server.available_timeframes):
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


def get_workspace_completions(server, prefix):
    """Генерирует предложения автодополнения на основе файлов рабочего пространства"""
    completion_items = []

    # Анализируем Python файлы в проекте для поиска классов и функций
    python_files = [path for path in server.project_files.keys() if path.endswith('.py')]

    for file_path in python_files:
        try:
            content = server.file_content_cache.get(file_path)
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
            server.logger.error(f"Ошибка при анализе файла {file_path}: {str(e)}")

    return completion_items
