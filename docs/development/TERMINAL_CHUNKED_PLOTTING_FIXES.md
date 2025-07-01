# Terminal Chunked Plotting Fixes

## Overview
Fixed issues in terminal display mode (`-d term`) for the command `uv run run_analysis.py show csv mn1 -d term --rule rsi:14,30,70,open`.

## Issues Fixed

### 1. Removed Statistics Under Each Chart
- **Problem**: Statistics were displayed under each chart, cluttering the output
- **Solution**: Removed calls to `_show_chunk_statistics()` from all chunk display functions
- **Files Modified**: `src/plotting/term_chunked_plot.py`

### 2. Added Date/Time Range Display
- **Problem**: It was not clear which dates were displayed in each chunk
- **Solution**: Added display of start and end dates in the title of each chunk
- **Implementation**: 
  ```python
  start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
  end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
  plt.title(f"{title} - {rule_type.upper()} (Chunk {i+1}/{len(chunks)}) - {start_date} to {end_date}")
  ```

### 3. Proper Axis Labels
- **Problem**: Axes were labeled as "Time / Bar Index" and "Price"
- **Solution**: Changed to "Date/Time" and "Price/Value" for better understanding
- **Implementation**:
  ```python
  plt.xlabel("Date/Time")
  plt.ylabel("Price/Value")
  ```

### 4. Full Screen Chart Size
- **Problem**: Charts were too small
- **Solution**: Increased chart size from `(140, 35)` to `(200, 50)`
- **Implementation**:
  ```python
  plt.plot_size(200, 50)  # Much larger plot size
  ```

### 5. Candles Style
- **Problem**: "matrix" style was used by default
- **Solution**: Changed to "candles" style for all rules
- **Implementation**:
  ```python
  def plot_ohlcv_chunks(df: pd.DataFrame, title: str = "OHLCV Chunks", style: str = "candles") -> None:
  ```

## Additional Improvements

### Date Axis Ticks
- Added date display on X-axis with automatic step
- Shows approximately 10 date labels per chart for readability

### Enhanced Date Handling
- Support for both datetime indices and numeric indices
- Automatic date formatting in 'YYYY-MM-DD HH:MM' format

### Consistent Implementation
- All chunk display functions (OHLCV, AUTO, PV, SR, PHLD, RSI) updated with the same improvements
- Uniform style and size for all chart types

## Files Modified

1. **src/plotting/term_chunked_plot.py**
   - Updated all chunk display functions
   - Added X-axis date support
   - Increased chart sizes
   - Changed default style to "candles"

2. **src/cli/cli_show_mode.py**
   - Updated calls to use "candles" style

3. **src/plotting/plotting_generation.py**
   - Updated `plot_chunked_terminal` call to use "candles" style

4. **tests/plotting/test_term_chunked_plot.py**
   - Updated tests to verify new "candles" style

## Testing

All changes tested:
- ✅ Unit tests pass (23/23)
- ✅ Real command execution successful
- ✅ Charts display correctly with dates and proper sizing
- ✅ No statistics clutter under charts
- ✅ Full screen utilization

## Usage Example

```bash
uv run run_analysis.py show csv mn1 -d term --rule rsi:14,30,70,open
```

**Result**: 
- 8 chunks with ~50 candles each
- Each chunk shows date range in the title
- Charts occupy almost the full screen
- Axes labeled as "Date/Time" and "Price/Value"
- "candles" style for better visualization
- No statistics under charts

## Benefits

1. **Better Readability**: Large charts with clear dates
2. **Cleaner Output**: Removed unnecessary statistics
3. **Professional Look**: Candlestick style for financial data
4. **User-Friendly**: Clear axis labels and dates
5. **Consistent Experience**: Uniform style for all rules 