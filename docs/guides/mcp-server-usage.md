# MCP Server Usage Guide

## Overview

Neozork MCP Server - это универсальный сервер Model Context Protocol для финансового анализа с интеграцией в IDE.

## 🚀 Quick Start

### 1. Автоматический запуск (Рекомендуется)

MCP сервер запускается автоматически при открытии проекта в поддерживаемых IDE:

- **Cursor IDE** - автоматически
- **PyCharm** - автоматически  
- **VS Code** - автоматически

### 2. Ручной запуск

```bash
# Простой запуск
python3 start_mcp_server.py

# Прямой запуск сервера
python3 neozork_mcp_server.py

# Запуск с отладкой
python3 neozork_mcp_server.py --debug
```

### 3. Проверка статуса

```bash
# Проверить статус сервера
python3 scripts/check_mcp_status.py

# Показать запущенные процессы
ps aux | grep neozork_mcp_server
```

## 📁 File Structure

```
📁 MCP Server Files:
├── neozork_mcp_server.py          # Основной сервер
├── neozork_mcp_config.json        # Конфигурация сервера
├── start_mcp_server.py            # Скрипт запуска
├── cursor_mcp_config.json         # Конфигурация Cursor
├── pycharm_mcp_config.json        # Конфигурация PyCharm
├── mcp.json                       # Универсальная конфигурация
├── scripts/
│   ├── setup_ide_configs.py       # Настройка IDE
│   ├── neozork_mcp_manager.py     # Менеджер сервера
│   └── check_mcp_status.py        # Проверка статуса
└── logs/                          # Логи сервера
```

## ⚙️ Configuration

### Основная конфигурация (`neozork_mcp_config.json`)

```json
{
  "server_mode": "unified",
  "server_name": "Neozork Unified MCP Server",
  "version": "2.0.0",
  "features": {
    "financial_data": true,
    "technical_indicators": true,
    "github_copilot": true,
    "code_completion": true,
    "project_analysis": true,
    "ai_suggestions": true
  }
}
```

### IDE Конфигурации

#### Cursor IDE (`cursor_mcp_config.json`)
```json
{
  "mcpServers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "LOG_LEVEL": "INFO"
      },
      "cwd": "${workspaceFolder}"
    }
  }
}
```

#### PyCharm (`pycharm_mcp_config.json`)
```json
{
  "mcpServers": {
    "neozork": {
      "command": "python3",
      "args": ["neozork_mcp_server.py"],
      "env": {
        "PYTHONPATH": "${PROJECT_ROOT}",
        "LOG_LEVEL": "INFO"
      },
      "cwd": "${PROJECT_ROOT}"
    }
  }
}
```

## 🔧 Setup Commands

### Настройка IDE конфигураций

```bash
# Настроить все IDE
python3 scripts/setup_ide_configs.py

# Настроить конкретную IDE
python3 scripts/neozork_mcp_manager.py create-config cursor
python3 scripts/neozork_mcp_manager.py create-config pycharm
python3 scripts/neozork_mcp_manager.py create-config vscode
```

### Управление сервером

```bash
# Запустить менеджер
python3 scripts/neozork_mcp_manager.py start

# Показать статус
python3 scripts/neozork_mcp_manager.py status

# Остановить сервер
python3 scripts/neozork_mcp_manager.py stop

# Перезапустить сервер
python3 scripts/neozork_mcp_manager.py restart
```

## 🐛 Troubleshooting

### Проблемы с подключением

1. **Сервер не запускается**
```bash
# Проверить Python
python3 --version

# Проверить зависимости
uv pip list

# Проверить права доступа
ls -la neozork_mcp_server.py
```

2. **IDE не подключается**
```bash
# Перезапустить IDE
# Проверить конфигурацию
cat cursor_mcp_config.json

# Проверить логи
tail -f logs/neozork_mcp_*.log
```

3. **Множественные процессы**
```bash
# Остановить все процессы
pkill -f neozork_mcp_server.py

# Проверить процессы
ps aux | grep neozork_mcp_server
```

### Логи

- `logs/neozork_mcp_YYYYMMDD.log` - основные логи сервера
- `logs/mcp_status_check.log` - логи проверки статуса
- `logs/ide_setup.log` - логи настройки IDE

## 📊 Features

### Доступные возможности

- **Financial Data Integration** - интеграция финансовых данных
- **Technical Indicators** - технические индикаторы
- **Code Completion** - автодополнение кода
- **Project Analysis** - анализ проекта
- **AI Suggestions** - AI предложения
- **GitHub Copilot** - интеграция с Copilot

### Команды MCP

- `neozork/status` - статус сервера
- `neozork/health` - проверка здоровья
- `neozork/ping` - ping/pong тест
- `neozork/metrics` - метрики производительности
- `neozork/projectInfo` - информация о проекте
- `neozork/financialData` - финансовые данные
- `neozork/indicators` - технические индикаторы

## 🔄 Development

### Добавление новых функций

1. Добавить обработчик в `neozork_mcp_server.py`
2. Обновить конфигурацию
3. Добавить тесты
4. Обновить документацию

### Тестирование

```bash
# Запустить тесты
python -m pytest tests/mcp/ -v

# Тестировать сервер
python3 scripts/check_mcp_status.py
```

## 📝 Notes

- Сервер работает в stdio режиме для IDE интеграции
- Конфигурации автоматически обновляются при запуске `setup_ide_configs.py`
- Логи сохраняются в папку `logs/`
- Сервер поддерживает hot reload при изменении файлов 