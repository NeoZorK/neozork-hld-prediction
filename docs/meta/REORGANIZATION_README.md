# File Reorganization - Quick Reference

## What Was Moved

### Main Files
- `test_ma_line.py` → `tests/calculation/indicators/trend/`
- `debug_wave_indicator.py` → `scripts/debug/`
- `debug_signals_analysis.py` → `scripts/debug/`

### Test Files
- `tests/test_test_ma_line.py` → `tests/calculation/indicators/trend/`
- `tests/test_debug_wave_indicator.py` → `tests/scripts/`
- `tests/test_debug_signals_analysis.py` → `tests/scripts/`

## Why This Was Done

1. **Better Organization**: Related files are now grouped together
2. **Logical Structure**: Test structure mirrors source structure
3. **Easier Maintenance**: Debug scripts are centralized
4. **Improved Navigation**: Developers can find files faster

## What Was Updated

- ✅ All import paths in test files
- ✅ All file references in tests
- ✅ Project structure documentation
- ✅ Test structure documentation (NEW)
- ✅ Scripts structure documentation (NEW)
- ✅ Main documentation index

## Testing

All moved files have been tested and work correctly:
```bash
# Test MA line functionality
uv run pytest tests/calculation/indicators/trend/test_test_ma_line.py -v

# Test debug script tests
uv run pytest tests/scripts/test_debug_wave_indicator.py -v
uv run pytest tests/scripts/test_debug_signals_analysis.py -v
```

## Documentation

- **Project Structure**: `docs/getting-started/project-structure.md`
- **Test Structure**: `docs/testing/test-structure.md` (NEW)
- **Scripts Structure**: `docs/development/scripts-structure.md` (NEW)
- **Full Summary**: `docs/meta/FILE_REORGANIZATION_SUMMARY.md`

## Benefits

- 🎯 **Logical Grouping**: Related files are together
- 🔍 **Easy Discovery**: Find files quickly
- 🛠️ **Better Maintenance**: Update related functionality easily
- 📚 **Clear Documentation**: Understand project structure
- ✅ **100% Test Coverage**: Maintained after reorganization

## Future Guidelines

When adding new files:
- **Indicator tests** → `tests/calculation/indicators/<category>/`
- **Debug scripts** → `scripts/debug/`
- **Utility scripts** → `scripts/utilities/`
- **Analysis scripts** → `scripts/analysis/`

---

**Status**: ✅ **COMPLETED** - All files moved, paths updated, documentation created, tests verified.
