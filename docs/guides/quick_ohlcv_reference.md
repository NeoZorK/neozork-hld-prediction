# Quick OHLCV Analysis Reference

## Status Icons Quick Guide

### Price Validation
- ✅ **Excellent** (95-100%): Perfect OHLC relationships
- ⚠️ **Good** (80-94%): Minor issues, generally reliable
- 🔶 **Fair** (50-79%): Some problems, use with caution
- ❌ **Poor** (0-49%): Major issues, needs cleaning

### Volume Analysis
- ✅ **Perfect** (0% zero): All periods have volume
- ✅ **Good** (1-5% zero): Very few missing volumes
- ⚠️ **Acceptable** (6-15% zero): Some missing volumes
- ❌ **Problematic** (>15% zero): Many missing volumes

### Data Quality
- ✅ **Excellent** (99-100%): Almost complete data
- ✅ **Very Good** (95-98%): Very few gaps
- ⚠️ **Good** (90-94%): Some gaps, generally complete
- 🔶 **Fair** (80-89%): Significant gaps
- ❌ **Poor** (<80%): Major gaps, unreliable

### Price-Volume Correlation
- ✅ **Strong** (≥0.7): Volume strongly confirms price
- ⚠️ **Strong Negative** (≤-0.7): Volume contradicts price
- ✅ **Moderate** (0.3-0.7): Some volume confirmation
- ⚠️ **Moderate Negative** (-0.3 to -0.7): Mixed signals
- 🔶 **Weak** (0.1-0.3): Limited correlation
- 🔶 **Negligible** (-0.1 to 0.1): No meaningful correlation

## Quick Decision Matrix

| Price Val | Volume | Data Quality | Action |
|-----------|--------|--------------|--------|
| ✅ Excellent | ✅ Perfect | ✅ Excellent | **Proceed with confidence** |
| ⚠️ Good | ✅ Good | ✅ Very Good | **Generally reliable** |
| 🔶 Fair | ⚠️ Acceptable | ⚠️ Good | **Use with caution** |
| ❌ Poor | ❌ Problematic | ❌ Poor | **Clean data first** |

## Common Patterns

### High-Quality Trading Data
```
✅ Excellent | ✅ Perfect | ✅ Excellent | ✅ Strong positive
```
**Use for**: All trading strategies, backtesting, live trading

### Indicator Data (RSI, MACD, etc.)
```
❌ Poor | ✅ Perfect | ✅ Excellent | 🔶 Negligible
```
**Use for**: Technical analysis, indicator-based strategies

### Problematic Data
```
❌ Poor | ❌ Problematic | ❌ Poor | 🔶 Negligible
```
**Action**: Clean data before any analysis

## Quick Fixes

### For Poor Price Validation
1. Check if data is actually OHLC (not indicators)
2. Verify data source
3. Look for transformation errors

### For Problematic Volume
1. Check for missing trading days
2. Verify volume data source
3. Consider data interpolation

### For Poor Data Quality
1. Identify missing data patterns
2. Check data source reliability
3. Use data cleaning tools

## Red Flags 🚩

- **Price Validation: ❌ Poor** + **Data Quality: ❌ Poor** = Major data issues
- **Volume Analysis: ❌ Problematic** = Unreliable volume-based analysis
- **All metrics: ❌ Poor** = Data not suitable for analysis
- **Correlation: Strong Negative** = Volume contradicts price (investigate)

## Green Flags ✅

- **All metrics: ✅ Excellent/Perfect** = High-quality data
- **Price Validation: ✅ Excellent** + **Data Quality: ✅ Excellent** = Reliable for trading
- **Correlation: Strong Positive** = Volume confirms price trends
