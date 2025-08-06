# Debug RSI Signals File Movement

## Overview
Файл `debug_rsi_signals.py` был успешно перемещен из корневой папки `scripts/` в соответствующую подпапку `scripts/debug/` для лучшей организации кода.

## Changes Made

### 1. File Movement
- **From**: `scripts/debug_rsi_signals.py`
- **To**: `scripts/debug/debug_rsi_signals.py`

### 2. Path Updates
Обновлен путь к данным в файле для корректной работы из новой локации:
```python
# Old path
df = pd.read_parquet('../data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet')

# New path (updated for debug subfolder)
df = pd.read_parquet('../../data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet')
```

### 3. Test Coverage
Создан полный набор тестов в `tests/scripts/test_debug_rsi_signals.py` с покрытием:
- ✅ Basic functionality testing
- ✅ Identical metrics warning testing
- ✅ No trading signals handling
- ✅ RSI analysis functionality
- ✅ File path verification

## Test Results
```
✅ Passed: 5
❌ Failed: 0
📈 Total: 5
```

## Benefits
1. **Better Organization**: Файл теперь находится в логически соответствующей папке `debug/`
2. **Consistent Structure**: Соответствует структуре других debug файлов
3. **Maintained Functionality**: Все функции работают корректно после перемещения
4. **Full Test Coverage**: 100% покрытие тестами новой функциональности

## File Structure
```
scripts/
├── debug/
│   ├── debug_rsi_signals.py          # ← Moved here
│   ├── debug_binance_connection.py
│   ├── debug_csv_reader.py
│   └── ...
├── analysis/
├── demos/
└── ...
```

## Verification
- ✅ File successfully moved to `scripts/debug/`
- ✅ Old file removed from `scripts/`
- ✅ Path updated for new location
- ✅ All tests passing
- ✅ No breaking changes to existing functionality 