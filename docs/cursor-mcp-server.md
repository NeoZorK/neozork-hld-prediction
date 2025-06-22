# Cursor MCP Server для Neozork HLD Prediction

## Обзор

Cursor MCP Server - это специализированный сервер Model Context Protocol (MCP), оптимизированный для работы с проектом Neozork HLD Prediction в Cursor IDE. Сервер предоставляет расширенные возможности автодополнения, поиска кода и анализа проекта, специфичные для финансового анализа и машинного обучения.

## Особенности

### 🚀 Основные возможности

- **Умное автодополнение**: Контекстно-зависимые подсказки для функций, классов и переменных
- **Финансовые данные**: Автоматическое сканирование и индексация финансовых данных
- **Технические индикаторы**: Специализированные подсказки для индикаторов
- **Code Snippets**: Готовые шаблоны кода для типичных задач
- **Поиск кода**: Быстрый поиск функций, классов и индикаторов
- **Анализ проекта**: Статистика и метаданные проекта

### 📊 Поддерживаемые типы данных

- **Финансовые символы**: BTCUSD, GBPUSD, EURUSD и др.
- **Временные фреймы**: D1, H1, M15, M5 и др.
- **Технические индикаторы**: SMA, EMA, RSI, MACD и др.
- **Функции анализа**: Плоттинг, статистика, машинное обучение

## Установка и настройка

### Требования

- Python 3.11+
- Cursor IDE
- Зависимости проекта (см. `pyproject.toml`)

### Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd neozork-hld-prediction
```

2. Установите зависимости:
```bash
pip install -e .
```

3. Запустите сервер:
```bash
python cursor_mcp_server.py
```

### Настройка Cursor IDE

1. Откройте настройки Cursor IDE
2. Найдите раздел MCP или AI Assistant
3. Добавьте новый сервер:
   ```json
   {
     "name": "Neozork MCP Server",
     "command": "python",
     "args": ["cursor_mcp_server.py"],
     "cwd": "/path/to/neozork-hld-prediction"
   }
   ```

## Архитектура

### Основные компоненты

#### CursorMCPServer
Главный класс сервера, управляющий всеми операциями.

#### CodeIndexer
Индексирует код проекта для быстрого поиска и автодополнения.

#### DataScanner
Сканирует финансовые данные и создает метаданные.

### Структура данных

#### CompletionItem
```python
@dataclass
class CompletionItem:
    label: str                    # Отображаемое имя
    kind: CompletionItemKind      # Тип элемента
    detail: Optional[str]         # Дополнительная информация
    documentation: Optional[str]  # Документация
    insert_text: Optional[str]    # Текст для вставки
```

#### ProjectFile
```python
@dataclass
class ProjectFile:
    path: str                     # Путь к файлу
    extension: str                # Расширение файла
    size: int                     # Размер файла
    modified: datetime            # Время изменения
    content: Optional[str]        # Содержимое файла
```

#### FinancialData
```python
@dataclass
class FinancialData:
    symbol: str                   # Финансовый символ
    timeframe: str                # Временной фрейм
    path: str                     # Путь к файлу данных
    columns: List[str]            # Колонки данных
    sample_data: List[List[str]]  # Примеры данных
```

## API

### Основные методы

#### initialize
Инициализация сервера и получение возможностей.

#### textDocument/completion
Получение автодополнений для текущей позиции курсора.

#### cursor/projectInfo
Получение информации о проекте.

#### cursor/financialData
Получение информации о финансовых данных.

#### cursor/indicators
Получение списка доступных индикаторов.

#### cursor/codeSearch
Поиск кода по запросу.

#### cursor/snippets
Получение доступных сниппетов.

#### cursor/analysis
Получение анализа проекта.

### Примеры запросов

#### Автодополнение
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "textDocument/completion",
  "params": {
    "textDocument": {
      "uri": "file:///path/to/file.py"
    },
    "position": {
      "line": 10,
      "character": 15
    }
  }
}
```

#### Поиск кода
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "cursor/codeSearch",
  "params": {
    "query": "calculate_sma"
  }
}
```

## Code Snippets

### Загрузка финансовых данных
```python
# Load financial data
csv_path = 'mql5_feed/CSVExport_BTCUSD_PERIOD_D1.csv'
df = pd.read_csv(csv_path)
df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)
print(f"Loaded {len(df)} records for BTCUSD D1")
```

### Расчет индикаторов
```python
# Calculate technical indicators
df['sma_20'] = df['close'].rolling(window=20).mean()
df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
df['rsi'] = calculate_rsi(df['close'], period=14)
df['macd'], df['macd_signal'] = calculate_macd(df['close'])
```

### Создание графика анализа
```python
# Create analysis plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

# Price and indicators
ax1.plot(df.index, df['close'], label='Close', alpha=0.7)
ax1.plot(df.index, df['sma_20'], label='SMA 20', alpha=0.7)
ax1.plot(df.index, df['ema_50'], label='EMA 50', alpha=0.7)
ax1.set_title('BTCUSD - D1 Analysis')
ax1.legend()
ax1.grid(True)

# RSI
ax2.plot(df.index, df['rsi'], label='RSI', color='purple')
ax2.axhline(y=70, color='r', linestyle='--', alpha=0.5)
ax2.axhline(y=30, color='g', linestyle='--', alpha=0.5)
ax2.set_ylabel('RSI')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
```

## Логирование

Сервер создает подробные логи в директории `logs/`:

- `cursor_mcp_YYYYMMDD.log` - Основной лог файл
- Формат: `[timestamp] [level] [CursorMCP] message`

### Уровни логирования

- **DEBUG**: Детальная отладочная информация
- **INFO**: Общая информация о работе сервера
- **WARNING**: Предупреждения
- **ERROR**: Ошибки

## Тестирование

### Запуск тестов
```bash
pytest tests/mcp/test_cursor_mcp_server.py -v
```

### Покрытие тестами
```bash
pytest tests/mcp/test_cursor_mcp_server.py --cov=cursor_mcp_server --cov-report=html
```

### Тестируемые компоненты

- Инициализация сервера
- Сканирование проекта
- Индексация кода
- Генерация автодополнений
- Обработка сообщений
- Обработка ошибок

## Производительность

### Оптимизации

- **Кэширование**: Файлы и метаданные кэшируются в памяти
- **Ленивая загрузка**: Данные загружаются по требованию
- **Индексация**: AST-парсинг для быстрого поиска
- **Фильтрация**: Игнорирование ненужных файлов и директорий

### Метрики

- Время инициализации: < 5 секунд
- Время ответа на автодополнение: < 100ms
- Потребление памяти: < 100MB для среднего проекта

## Устранение неполадок

### Частые проблемы

#### Сервер не запускается
1. Проверьте версию Python (требуется 3.11+)
2. Убедитесь, что все зависимости установлены
3. Проверьте права доступа к директориям

#### Нет автодополнений
1. Проверьте, что файлы проекта проиндексированы
2. Убедитесь, что Cursor IDE правильно настроен
3. Проверьте логи на наличие ошибок

#### Медленная работа
1. Проверьте размер проекта
2. Убедитесь, что исключены ненужные директории
3. Проверьте доступность диска

### Отладка

#### Включение отладочного режима
```python
import logging
logging.getLogger('cursor_mcp_server').setLevel(logging.DEBUG)
```

#### Проверка состояния сервера
```python
# Получение информации о проекте
result = server._handle_project_info(None, {})
print(json.dumps(result, indent=2))
```

## Разработка

### Добавление новых функций

1. Создайте новый обработчик в `handlers`
2. Добавьте соответствующий метод
3. Напишите тесты
4. Обновите документацию

### Расширение автодополнений

1. Добавьте новые типы в `CompletionItemKind`
2. Создайте новые методы генерации
3. Обновите `_handle_completion`

### Добавление сниппетов

1. Создайте новый `CompletionItem` в `_get_code_snippets`
2. Добавьте соответствующий шаблон
3. Протестируйте в Cursor IDE

## Лицензия

Проект распространяется под лицензией MIT.

## Поддержка

Для получения поддержки:

1. Создайте issue в GitHub
2. Опишите проблему подробно
3. Приложите логи и примеры кода
4. Укажите версии Python и Cursor IDE

## Вклад в проект

Мы приветствуем вклад в развитие проекта:

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Напишите тесты
5. Создайте Pull Request

## Changelog

### v2.0.0
- Полная переработка архитектуры
- Улучшенное автодополнение
- Поддержка финансовых данных
- Code snippets
- Расширенное логирование

### v1.0.0
- Базовая функциональность MCP сервера
- Поддержка автодополнения
- Индексация кода 