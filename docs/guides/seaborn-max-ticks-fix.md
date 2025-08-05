# Seaborn MAXTICKS Fix

## Problem

The MAXTICKS error occurred when displaying large time series in seaborn mode. The chart would not display on screen and some indicators were not supported.

## Solution

- Adaptive tick interval logic was implemented
- Chart display was fixed
- Support for additional indicators was added

## Details

- The fixed interval `mdates.DayLocator(interval=7)` was replaced with adaptive logic
- Tick interval is now calculated based on the time range of the data
- Applied to both the main and indicator charts

### Interval selection logic:
- > 5 years: ticks every 2 years
- > 2 years: ticks every year
- > 1 year: ticks every 3 months
- > 3 months: ticks every month
- < 3 months: ticks with interval `max(1, days_range // 10)` days

### Chart display fix
- Added `plt.show()` call after saving the chart
- Chart now displays on screen

### Added indicator support
- `putcallratio` - put/call options ratio indicator
- `cot` - Commitments of Traders indicator
- `feargreed` - fear and greed indicator
- `supertrend` - SuperTrend indicator

## Result

All commands now work correctly:
```bash
# MACD indicator
uv run run_analysis.py show csv gbp -d sb --rule macd:12,26,9,close

# Put/Call Ratio indicator
uv run run_analysis.py show csv gbp -d sb --rule putcallratio:20,close,60,40

# COT indicator
uv run run_analysis.py show csv gbp -d sb --rule cot:20,close

# Fear & Greed indicator
uv run run_analysis.py show csv gbp -d sb --rule feargreed:14,close

# SuperTrend indicator
uv run run_analysis.py show csv gbp -d sb --rule supertrend:10,3
```

**Tests:** 25 tests passed successfully
- `test_dual_chart_seaborn_fix.py` - 5 tests
- `test_seaborn_plot_display.py` - 5 tests
- `test_seaborn_putcallratio.py` - 5 tests
- `test_seaborn_cot.py` - 5 tests
- `test_seaborn_feargreed.py` - 5 tests
- `test_seaborn_supertrend.py` - 5 tests

## Created files

**Tests:**
- `tests/plotting/test_dual_chart_seaborn_fix.py`
- `tests/plotting/test_seaborn_plot_display.py`
- `tests/plotting/test_seaborn_putcallratio.py`
- `tests/plotting/test_seaborn_cot.py`
- `tests/plotting/test_seaborn_feargreed.py`
- `tests/plotting/test_seaborn_supertrend.py`

**Documentation:**
- `docs/guides/seaborn-max-ticks-fix.md`
- `docs/guides/seaborn-max-ticks-fix-summary.md`

## Status

✅ Problem completely solved
- All indicators are supported in seaborn mode
- Charts display correctly
- Adaptive tick logic prevents MAXTICKS errors
- 100% test coverage for all fixes 