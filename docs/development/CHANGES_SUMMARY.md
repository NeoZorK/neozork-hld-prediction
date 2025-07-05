# Changes Summary

## Dual Chart Fast Refactoring (2025-07-05)

### Overview
Successfully refactored `src/plotting/dual_chart_fast.py` by extracting indicator plotting logic into separate functions for each indicator type, while maintaining 100% backward compatibility.

### Key Improvements
- **21 Individual Indicator Functions**: Created dedicated functions for each indicator type (RSI, MACD, EMA, BB, ATR, CCI, VWAP, Pivot, HMA, TSF, Monte Carlo, Kelly, Donchian Channel, Fibonacci, OBV, StdDev, ADX, SAR, RSI Momentum, RSI Divergence, Stochastic)
- **Enhanced Code Organization**: Reduced main function from ~760 to ~200 lines
- **Improved Maintainability**: Each indicator can be modified independently
- **Better Testability**: Created comprehensive test suite with 31 new test cases

### Helper Functions Added
- `_get_indicator_hover_tool()` - Generates appropriate hover tools for different indicators
- `_plot_indicator_by_type()` - Main dispatcher function that calls the appropriate indicator function

### Testing Results
- ✅ All 31 new tests pass
- ✅ All 10 existing tests continue to pass
- ✅ Total: 41 tests pass, 0 failures
- ✅ 100% backward compatibility maintained

### Benefits
- **Modular Structure**: Easier to add new indicators or modify existing ones
- **Independent Testing**: Each indicator function can be tested separately
- **Code Reusability**: Functions can be imported and used independently
- **Future Scalability**: Simplified structure for future enhancements

### Files Modified
- `src/plotting/dual_chart_fast.py` - Refactored with modular indicator functions
- `tests/plotting/test_dual_chart_fast_refactored.py` - New comprehensive test suite
- `docs/development/REFACTORING_SUMMARY.md` - Detailed refactoring documentation

## Native Container Test Fixes (2025-06-30)

### Проблема
При запуске `uv run pytest tests/native-container/ -n auto` вне контейнера падали 2 теста:
- `test_entrypoint_script_interactive_shell`
- `test_entrypoint_script_welcome_message`

### Решение
1. **Исправлена логика определения окружения** - добавлены функции `is_running_in_native_container()` и `should_skip_native_container_tests()`
2. **Исправлены проверки в тестах** - обновлены ожидаемые строки в соответствии с реальным содержимым `container-entrypoint.sh`
3. **Обновлены все тесты** - теперь используют правильную логику пропуска

### Результат
- ✅ Все тесты проходят успешно
- ✅ Тесты правильно пропускаются вне контейнера
- ✅ Сохранена существующая логика и код

### Файлы изменены
- `tests/native-container/test_native_container_features.py`
- `docs/development/native-container-test-fixes.md` (новая документация)

## Fibonacci Retracements Improvements (2025-07-03)

### Enhanced Signal Generation
- **Balanced Buy/Sell Signals**: Improved algorithm now generates equal opportunities for buy and sell signals
- **Momentum Detection**: Added signals based on price momentum near Fibonacci levels
- **Multiple Level Support**: Enhanced support for all standard Fibonacci levels (0.236, 0.382, 0.5, 0.618, 0.786)

### New Parameter Support
- **`--rule fibo:all`**: Automatically uses all standard Fibonacci levels
- **Custom Levels**: Support for any combination of Fibonacci levels
- **Improved Parsing**: Better error handling for invalid level parameters

### Signal Logic Improvements
```python
# Buy signals: Price crosses above support levels
buy_condition_618 = (price > fib_618) & (price.shift(1) <= fib_618.shift(1))
buy_condition_382 = (price > fib_382) & (price.shift(1) <= fib_382.shift(1))
buy_condition_236 = (price > fib_236) & (price.shift(1) <= fib_236.shift(1))

# Additional buy conditions: price near support with momentum
buy_near_618 = (price >= fib_618 * 0.995) & (price <= fib_618 * 1.005) & (price > price.shift(1))
```

### Usage Examples
```bash
# Use all standard levels
uv run run_analysis.py show csv mn1 -d fastest --rule fibo:all

# Custom levels
uv run run_analysis.py show csv mn1 -d fastest --rule fibo:0.236,0.5,0.786

# Default levels
uv run run_analysis.py show csv mn1 -d fastest --rule fibo
```

### Performance Results
- **Signal Balance**: Now generates balanced buy/sell signals (74 buy vs 66 sell with `all` parameter)
- **Improved Accuracy**: Better signal timing with momentum detection
- **Enhanced Flexibility**: Support for any Fibonacci level combination

### Documentation Updates
- Updated comprehensive documentation with new parameter options
- Added signal generation logic explanation
- Included best practices and trading strategies
- Enhanced CLI interface documentation 