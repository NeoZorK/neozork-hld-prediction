# Cursor MCP Server для Neozork HLD Prediction

🚀 **Специализированный MCP сервер для Cursor IDE, оптимизированный для работы с проектом финансового анализа и машинного обучения**

## 🎯 Что это такое?

Cursor MCP Server - это интеллектуальный помощник для Cursor IDE, который значительно ускоряет разработку в проекте Neozork HLD Prediction. Сервер предоставляет:

- **Умное автодополнение** с учетом контекста проекта
- **Финансовые данные** - автоматическое сканирование и индексация
- **Технические индикаторы** - специализированные подсказки
- **Code Snippets** - готовые шаблоны для типичных задач
- **Быстрый поиск** функций, классов и индикаторов
- **Анализ проекта** - статистика и метаданные

## 🚀 Быстрый старт

### 1. Установка

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd neozork-hld-prediction

# Установите зависимости
pip install -e .

# Запустите тесты
python scripts/run_cursor_mcp.py --test --report
```

### 2. Настройка Cursor IDE

1. Откройте настройки Cursor IDE
2. Найдите раздел **AI Assistant** или **MCP Servers**
3. Добавьте новый сервер:

```json
{
  "name": "Neozork MCP Server",
  "command": "python",
  "args": ["cursor_mcp_server.py"],
  "cwd": "/path/to/neozork-hld-prediction"
}
```

### 3. Запуск

```bash
# Запуск сервера
python cursor_mcp_server.py

# Или через скрипт
python scripts/run_cursor_mcp.py --mode stdio
```

## 📊 Возможности

### 🎯 Автодополнение

Сервер предоставляет контекстно-зависимые подсказки:

- **Функции проекта** - все функции из вашего кода
- **Финансовые символы** - BTCUSD, GBPUSD, EURUSD и др.
- **Временные фреймы** - D1, H1, M15, M5 и др.
- **Технические индикаторы** - SMA, EMA, RSI, MACD и др.

### 📈 Финансовые данные

Автоматическое сканирование и индексация:

- **CSV файлы** из директории `mql5_feed/`
- **Метаданные** - символы, временные фреймы, колонки
- **Примеры данных** для быстрого понимания структуры

### 🧩 Code Snippets

Готовые шаблоны для типичных задач:

```python
# Загрузка данных
load_financial_data  # Загрузка и подготовка финансовых данных

# Расчет индикаторов
calculate_indicators  # Расчет технических индикаторов

# Создание графиков
plot_analysis  # Создание комплексного анализа
```

### 🔍 Поиск кода

Быстрый поиск по проекту:

- **Функции** - поиск по имени функции
- **Классы** - поиск по имени класса
- **Индикаторы** - поиск технических индикаторов

## 🏗️ Архитектура

### Основные компоненты

```
CursorMCPServer
├── CodeIndexer          # Индексация кода
├── DataScanner          # Сканирование данных
├── CompletionProvider   # Автодополнение
├── SnippetProvider      # Code snippets
└── SearchProvider       # Поиск кода
```

### Структура данных

- **ProjectFile** - информация о файлах проекта
- **FinancialData** - метаданные финансовых данных
- **CompletionItem** - элементы автодополнения

## 🧪 Тестирование

### Запуск тестов

```bash
# Функциональные тесты
pytest tests/mcp/test_cursor_mcp_server.py -v

# Полное тестирование с отчетом
python scripts/run_cursor_mcp.py --test --performance --report
```

### Покрытие тестами

```bash
pytest tests/mcp/test_cursor_mcp_server.py --cov=cursor_mcp_server --cov-report=html
```

## 📈 Производительность

### Метрики

- **Время инициализации**: < 5 секунд
- **Время автодополнения**: < 100ms
- **Потребление памяти**: < 100MB
- **Индексация**: Поддержка проектов до 10,000 файлов

### Оптимизации

- **Кэширование** файлов и метаданных
- **Ленивая загрузка** данных
- **AST-парсинг** для быстрого поиска
- **Фильтрация** ненужных файлов

## 🔧 Конфигурация

### Основные настройки

```json
{
  "mcpServers": {
    "neozork-cursor-mcp": {
      "command": "python",
      "args": ["cursor_mcp_server.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src:${workspaceFolder}",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Логирование

```json
{
  "logging": {
    "level": "INFO",
    "file": "logs/cursor_mcp.log",
    "maxSize": "10MB",
    "maxFiles": 5
  }
}
```

## 🐛 Устранение неполадок

### Частые проблемы

#### Сервер не запускается
```bash
# Проверьте версию Python
python --version  # Должно быть 3.11+

# Проверьте зависимости
pip list | grep -E "(pandas|numpy|ast)"

# Проверьте права доступа
ls -la cursor_mcp_server.py
```

#### Нет автодополнений
1. Убедитесь, что сервер запущен
2. Проверьте логи в `logs/cursor_mcp_*.log`
3. Перезапустите Cursor IDE

#### Медленная работа
1. Проверьте размер проекта
2. Убедитесь, что исключены ненужные директории
3. Проверьте доступность диска

### Отладка

```python
# Включение отладочного режима
import logging
logging.getLogger('cursor_mcp_server').setLevel(logging.DEBUG)

# Проверка состояния сервера
result = server._handle_project_info(None, {})
print(json.dumps(result, indent=2))
```

## 📚 Документация

### Подробная документация

- [Полная документация](docs/cursor-mcp-server.md)
- [API Reference](docs/cursor-mcp-server.md#api)
- [Примеры использования](docs/cursor-mcp-server.md#code-snippets)

### Примеры

#### Автодополнение
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "textDocument/completion",
  "params": {
    "textDocument": {"uri": "file:///path/to/file.py"},
    "position": {"line": 10, "character": 15}
  }
}
```

#### Поиск кода
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "cursor/codeSearch",
  "params": {"query": "calculate_sma"}
}
```

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта:

1. **Fork** репозитория
2. Создайте **feature branch**
3. Внесите изменения
4. Напишите **тесты**
5. Создайте **Pull Request**

### Руководство по разработке

- Следуйте **PEP 8** для стиля кода
- Добавляйте **типы** для всех функций
- Пишите **документацию** для новых функций
- Обновляйте **тесты** при изменении функциональности

## 📄 Лицензия

Проект распространяется под лицензией **MIT**.

## 🆘 Поддержка

### Получение помощи

1. **GitHub Issues** - создайте issue с подробным описанием
2. **Логи** - приложите логи из `logs/cursor_mcp_*.log`
3. **Примеры** - предоставьте примеры кода
4. **Версии** - укажите версии Python и Cursor IDE

### Полезные команды

```bash
# Запуск с отладкой
LOG_LEVEL=DEBUG python cursor_mcp_server.py

# Тестирование функциональности
python scripts/run_cursor_mcp.py --test

# Проверка производительности
python scripts/run_cursor_mcp.py --performance

# Генерация отчета
python scripts/run_cursor_mcp.py --test --performance --report
```

## 🎉 Changelog

### v2.0.0 (Текущая версия)
- ✅ Полная переработка архитектуры
- ✅ Улучшенное автодополнение
- ✅ Поддержка финансовых данных
- ✅ Code snippets
- ✅ Расширенное логирование
- ✅ Полное покрытие тестами

### v1.0.0
- ✅ Базовая функциональность MCP сервера
- ✅ Поддержка автодополнения
- ✅ Индексация кода

---

**Создано с ❤️ для сообщества Cursor IDE и финансового анализа** 