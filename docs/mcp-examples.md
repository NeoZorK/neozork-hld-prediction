# MCP Server Examples

Примеры использования MCP (Model Context Protocol) серверов для интеграции с GitHub Copilot.

## 🚀 Быстрый старт MCP серверов

### Автозапуск MCP серверов
```bash
# Запуск автозапуска
python scripts/auto_start_mcp.py

# Запуск с конфигурацией
python scripts/auto_start_mcp.py --config mcp_auto_config.json

# Запуск в режиме отладки
python scripts/auto_start_mcp.py --debug

# Запуск с кастомным путем проекта
python scripts/auto_start_mcp.py --project-path /path/to/project
```

### Ручное управление MCP серверами
```bash
# Запуск PyCharm GitHub Copilot MCP сервера
python pycharm_github_copilot_mcp.py

# Запуск с конфигурацией
python pycharm_github_copilot_mcp.py --config mcp_auto_config.json

# Запуск в stdio режиме для тестирования
python pycharm_github_copilot_mcp.py --stdio

# Запуск с отладочным логированием
python pycharm_github_copilot_mcp.py --debug
```

## 🔧 Управление серверами

### Статус и мониторинг
```bash
# Показать статус серверов
python scripts/auto_start_mcp.py --status

# Показать логи серверов
python scripts/auto_start_mcp.py --logs

# Показать конфигурацию
python scripts/auto_start_mcp.py --config-show
```

### Остановка серверов
```bash
# Остановить все серверы
python scripts/auto_start_mcp.py --stop

# Остановить конкретный сервер
python scripts/auto_start_mcp.py --stop-server pycharm_copilot

# Принудительная остановка
python scripts/auto_start_mcp.py --force-stop
```

### Перезапуск серверов
```bash
# Перезапустить все серверы
python scripts/auto_start_mcp.py --restart

# Перезапустить конкретный сервер
python scripts/auto_start_mcp.py --restart-server pycharm_copilot
```

## 🧪 Тестирование MCP серверов

### Тест stdio режима
```bash
# Тест stdio режима
python tests/test_stdio.py

# Тест с подробным выводом
python tests/test_stdio.py -v

# Тест с отладкой
python tests/test_stdio.py --debug
```

### Тест MCP функциональности
```bash
# Тест автозапуска MCP
python -m pytest tests/mcp/test_auto_start_mcp.py -v

# Тест PyCharm MCP сервера
python -m pytest tests/mcp/test_pycharm_github_copilot_mcp.py -v

# Тест всех MCP компонентов
python -m pytest tests/mcp/ -v
```

### Тест интеграции
```bash
# Тест интеграции MCP серверов
python scripts/run_cursor_mcp.py --test

# Тест с отчетом
python scripts/run_cursor_mcp.py --test --report

# Тест производительности
python scripts/run_cursor_mcp.py --test --benchmark
```

## 📊 Примеры использования в коде

### Автодополнение финансовых символов
```python
# GitHub Copilot предложит доступные символы
def analyze_market_data():
    symbol = "BTCUSD"  # Доступные: BTCUSD, GBPUSD, EURUSD, USDJPY
    timeframe = "D1"   # Доступные: D1, H1, M15, M5, M1
    
    # Загрузка данных с автодополнением
    data = load_financial_data(symbol, timeframe)
    
    # Расчет индикаторов с автодополнением
    sma_20 = calculate_sma(data, period=20)
    ema_50 = calculate_ema(data, period=50)
    rsi_14 = calculate_rsi(data, period=14)
    
    return data, sma_20, ema_50, rsi_14
```

### Технические индикаторы
```python
# GitHub Copilot предложит на основе контекста проекта
def calculate_technical_indicators(data):
    """
    Расчет комплексных технических индикаторов
    Copilot предложит: SMA, EMA, RSI, MACD, Bollinger Bands, ATR
    """
    indicators = {}
    
    # Простые скользящие средние
    indicators['sma_20'] = data['close'].rolling(window=20).mean()
    indicators['sma_50'] = data['close'].rolling(window=50).mean()
    
    # Экспоненциальные скользящие средние
    indicators['ema_12'] = data['close'].ewm(span=12, adjust=False).mean()
    indicators['ema_26'] = data['close'].ewm(span=26, adjust=False).mean()
    
    # RSI
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    indicators['rsi'] = 100 - (100 / (1 + rs))
    
    # MACD
    indicators['macd'] = indicators['ema_12'] - indicators['ema_26']
    indicators['macd_signal'] = indicators['macd'].ewm(span=9, adjust=False).mean()
    indicators['macd_histogram'] = indicators['macd'] - indicators['macd_signal']
    
    return indicators
```

### Фрагменты кода
```python
# Введите 'load_data' и получите автодополнение
load_financial_data  # Расширяется в: load_financial_data(symbol, timeframe)

# Введите 'calculate_indicators' и получите автодополнение
calculate_indicators  # Расширяется в: calculate_indicators(data)

# Введите 'plot_analysis' и получите автодополнение
plot_analysis  # Расширяется в: plot_analysis(data, indicators)

# Введите 'backtest_strategy' и получите автодополнение
backtest_strategy  # Расширяется в: backtest_strategy(data, strategy_params)
```

### Интеграция с GitHub Copilot
```python
# Copilot предложит на основе контекста проекта
def create_trading_strategy():
    """
    Создание полной торговой стратегии
    Copilot предложит: загрузка данных, расчет индикаторов, генерация сигналов
    """
    # Загрузка данных (Copilot предложит: BTCUSD, D1)
    data = load_financial_data("BTCUSD", "D1")
    
    # Расчет индикаторов (Copilot предложит: SMA, RSI, MACD)
    indicators = calculate_technical_indicators(data)
    
    # Генерация сигналов (Copilot предложит: логика пересечений)
    signals = generate_trading_signals(data, indicators)
    
    # Бэктестинг стратегии (Copilot предложит: метрики производительности)
    results = backtest_strategy(data, signals)
    
    return results
```

## 🔄 Паттерны использования

### Паттерн загрузки данных
```python
def load_and_prepare_data(symbol: str, timeframe: str):
    """
    Стандартный паттерн для загрузки и подготовки финансовых данных
    """
    # 1. Загрузка сырых данных
    raw_data = load_financial_data(symbol, timeframe)
    
    # 2. Проверка качества данных
    if not check_data_quality(raw_data):
        raise ValueError(f"Плохое качество данных для {symbol} {timeframe}")
    
    # 3. Предобработка данных
    processed_data = preprocess_data(raw_data)
    
    # 4. Инжиниринг признаков
    features = engineer_features(processed_data)
    
    return processed_data, features
```

### Паттерн расчета индикаторов
```python
def calculate_all_indicators(data):
    """
    Стандартный паттерн для расчета технических индикаторов
    """
    indicators = {}
    
    # Трендовые индикаторы
    indicators.update(calculate_trend_indicators(data))
    
    # Моментум индикаторы
    indicators.update(calculate_momentum_indicators(data))
    
    # Индикаторы волатильности
    indicators.update(calculate_volatility_indicators(data))
    
    # Объемные индикаторы
    indicators.update(calculate_volume_indicators(data))
    
    return indicators
```

### Паттерн визуализации
```python
def create_comprehensive_chart(data, indicators):
    """
    Стандартный паттерн для создания комплексных графиков
    """
    # Создание фигуры с подграфиками
    fig, axes = plt.subplots(3, 1, figsize=(15, 12))
    
    # График цены с индикаторами
    plot_price_chart(axes[0], data, indicators)
    
    # График объема
    plot_volume_chart(axes[1], data)
    
    # Графики индикаторов
    plot_indicator_charts(axes[2], indicators)
    
    plt.tight_layout()
    return fig
```

### Паттерн бэктестинга
```python
def backtest_trading_strategy(data, strategy_params):
    """
    Стандартный паттерн для бэктестинга торговых стратегий
    """
    # 1. Генерация сигналов
    signals = generate_signals(data, strategy_params)
    
    # 2. Расчет позиций
    positions = calculate_positions(signals)
    
    # 3. Расчет доходности
    returns = calculate_returns(data, positions)
    
    # 4. Расчет метрик производительности
    metrics = calculate_performance_metrics(returns)
    
    # 5. Генерация отчета
    report = generate_backtest_report(metrics, strategy_params)
    
    return report
```

## 🧪 Тестирование

### Модульные тесты
```python
class TestPyCharmMCPServer:
    def test_initialization(self):
        """Тест инициализации сервера"""
        server = PyCharmGitHubCopilotMCPServer()
        assert server.running == True
        assert len(server.handlers) > 0
    
    def test_completion(self):
        """Тест автодополнения кода"""
        server = PyCharmGitHubCopilotMCPServer()
        
        # Тест автодополнения финансовых данных
        completions = server._get_financial_completions()
        assert len(completions) > 0
        
        # Тест автодополнения индикаторов
        indicator_completions = server._get_indicator_completions()
        assert len(indicator_completions) > 0
    
    def test_github_copilot_integration(self):
        """Тест интеграции с GitHub Copilot"""
        server = PyCharmGitHubCopilotMCPServer()
        
        # Тест предложений Copilot
        context = "financial data analysis"
        suggestions = server._handle_copilot_suggestions(None, {"context": context})
        assert "suggestions" in suggestions
```

### Интеграционные тесты
```python
def test_full_workflow():
    """Тест полного рабочего процесса"""
    # 1. Запуск сервера
    server = PyCharmGitHubCopilotMCPServer()
    
    # 2. Загрузка данных
    data = load_financial_data("BTCUSD", "D1")
    assert data is not None
    
    # 3. Расчет индикаторов
    indicators = calculate_technical_indicators(data)
    assert len(indicators) > 0
    
    # 4. Генерация сигналов
    signals = generate_trading_signals(data, indicators)
    assert signals is not None
    
    # 5. Бэктестинг
    results = backtest_strategy(data, signals)
    assert results is not None
```

## 📊 Производительность

### Бенчмаркинг
```python
import time
import psutil

def benchmark_mcp_server():
    """Бенчмаркинг MCP сервера"""
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    # Запуск сервера
    server = PyCharmGitHubCopilotMCPServer()
    
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    startup_time = end_time - start_time
    memory_usage = end_memory - start_memory
    
    print(f"Время запуска: {startup_time:.2f}s")
    print(f"Использование памяти: {memory_usage:.2f}MB")
    
    return startup_time, memory_usage
```

## 🔍 Отладка

### Отладочные команды
```bash
# Включить отладочное логирование
export LOG_LEVEL=DEBUG
python pycharm_github_copilot_mcp.py

# Проверить зависимости
pip list | grep -E "(watchdog|psutil)"

# Проверить статус серверов
python scripts/auto_start_mcp.py --status --verbose

# Просмотр логов
tail -f logs/mcp_server.log
```

### Отладочные скрипты
```bash
# Отладка MCP серверов
python scripts/debug_scripts/debug_mcp_servers.py

# Проверка конфигурации
python scripts/debug_scripts/debug_mcp_config.py

# Тест соединений
python scripts/debug_scripts/debug_mcp_connections.py
```

## 🐳 Docker интеграция

### Запуск в контейнере
```bash
# Запуск MCP серверов в Docker
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py

# Запуск с отладкой
docker compose run --rm neozork-hld python pycharm_github_copilot_mcp.py --debug

# Тест в контейнере
docker compose run --rm neozork-hld python tests/test_stdio.py
```

## 🔧 Настройка IDE

### PyCharm
1. Установите MCP плагин из Settings → Plugins
2. Настройте MCP сервер в Settings → Languages & Frameworks → MCP Servers
3. Включите GitHub Copilot для расширенной AI помощи

### Cursor
1. Откройте Settings (Cmd/Ctrl + ,)
2. Добавьте конфигурацию MCP сервера в разделе AI Assistant
3. Перезапустите Cursor для применения изменений

### VS Code
1. Установите MCP Extension
2. Настройте в settings.json
3. Включите GitHub Copilot extension

## 📈 Мониторинг и метрики

### Метрики производительности
```python
# Мониторинг производительности MCP сервера
def monitor_mcp_performance():
    """Мониторинг производительности MCP сервера"""
    metrics = {
        'startup_time': measure_startup_time(),
        'response_time': measure_response_time(),
        'memory_usage': measure_memory_usage(),
        'cpu_usage': measure_cpu_usage(),
        'active_connections': count_active_connections()
    }
    
    return metrics
```

### Логирование
```python
import logging

# Настройка логирования для MCP серверов
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mcp_server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('mcp_server')
```

## 🚨 Устранение неполадок

### Общие проблемы
```bash
# Проблема: MCP сервер не запускается
python scripts/auto_start_mcp.py --stop
python scripts/auto_start_mcp.py --debug

# Проблема: Нет автодополнения
python tests/test_stdio.py
python -m pytest tests/mcp/ -v

# Проблема: Высокое потребление памяти
python scripts/auto_start_mcp.py --restart
```

### Проблемы с IDE
```bash
# PyCharm: Проверьте MCP плагин
# Cursor: Проверьте настройки AI Assistant
# VS Code: Проверьте MCP Extension
```

---

📚 **Дополнительные ресурсы:**
- **[Настройка MCP серверов](mcp-servers/SETUP.md)** - Подробная настройка
- **[Использование MCP серверов](mcp-servers/USAGE.md)** - API документация
- **[Изменения в MCP серверах](mcp-servers/CHANGES_SUMMARY.md)** - История изменений
- **[Полные примеры использования](usage-examples.md)** - Комплексные примеры 