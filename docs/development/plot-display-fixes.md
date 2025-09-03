# Исправление проблемы с автоматическим закрытием графиков

## Проблема

При использовании команд `uv run run_analysis.py show csv mn1 gbp -d mpl --rule AUTO` и `uv run run_analysis.py show csv mn1 gbp -d sb --rule AUTO` графики создавались, но мгновенно закрывались после открытия.

## Причина

Проблема была в функции `smart_plot_display()` в модуле `src/plotting/plot_utils.py`. Эта функция автоматически определяла, нужно ли показывать графики или закрывать их, но по умолчанию закрывала их слишком быстро.

## Решение

### 1. Обновление функции `smart_plot_display()`

Добавлены новые параметры:
- `block` - контролирует, должен ли график блокировать выполнение
- `pause_time` - время паузы перед закрытием (если не блокирующий режим)

### 2. Настройка через переменные окружения

Добавлена возможность настройки поведения через переменные окружения:

```bash
# Блокирующий режим (график остается открытым)
export PLOT_BLOCK_MODE=true

# Неблокирующий режим с паузой
export PLOT_BLOCK_MODE=false
export PLOT_PAUSE_TIME=10.0  # пауза 10 секунд
```

### 3. Обновление функций построения графиков

Обновлены функции в:
- `src/plotting/mplfinance_auto_plot.py`
- `src/plotting/seaborn_auto_plot.py`

Теперь они используют `smart_plot_display(block=True)` для блокирующего режима.

## Результат

После исправления:
- Графики mplfinance (`-d mpl`) остаются открытыми до закрытия пользователем
- Графики seaborn (`-d sb`) остаются открытыми до закрытия пользователем
- Добавлена гибкость настройки поведения через переменные окружения

## Использование

### Базовое использование (графики остаются открытыми)
```bash
uv run run_analysis.py show csv mn1 gbp -d mpl --rule AUTO
uv run run_analysis.py show csv mn1 gbp -d sb --rule AUTO
```

### Настройка через переменные окружения
```bash
# Графики закрываются через 15 секунд
export PLOT_BLOCK_MODE=false
export PLOT_PAUSE_TIME=15.0
uv run run_analysis.py show csv mn1 gbp -d mpl --rule AUTO

# Графики остаются открытыми (по умолчанию)
export PLOT_BLOCK_MODE=true
uv run run_analysis.py show csv mn1 gbp -d sb --rule AUTO
```

## Технические детали

### Функция `smart_plot_display()`

```python
def smart_plot_display(show_plot=True, block=None, pause_time=None):
    """
    Smart plot display function that automatically determines whether to show or close plots.
    
    Args:
        show_plot (bool): Whether to show the plot (overrides automatic detection)
        block (bool): Whether to block execution while showing the plot. If None, uses PLOT_BLOCK_MODE env var
        pause_time (float): Time to pause before closing (in seconds) if not blocking. If None, uses PLOT_PAUSE_TIME env var
    """
```

### Логика работы

1. **Блокирующий режим** (`block=True`): `plt.show(block=True)` - график остается открытым
2. **Неблокирующий режим** (`block=False`): `plt.show(block=False)` + пауза + `plt.close()`
3. **Автоматическое определение**: через переменные окружения `PLOT_BLOCK_MODE` и `PLOT_PAUSE_TIME`

### Совместимость

- Обратная совместимость сохранена
- По умолчанию используется блокирующий режим
- Работает со всеми бэкендами matplotlib (mpl, seaborn, mplfinance)
