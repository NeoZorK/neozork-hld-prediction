# Third Wave Hover Feature

## Overview

A new third hover trace named "wave" has been added to the Wave indicator in fastest mode. This trace provides a simplified hover experience that shows values only for red and blue Wave segments (buy/sell signals).

## Feature Details

### Purpose
The third wave hover trace serves as a clean, simplified way to view Wave values without the additional color information that appears on the main Wave segments.

### Behavior
- **Name**: "wave"
- **Visibility**: Invisible markers (transparent)
- **Data Filtering**: Only shows hover information for red (BUY) and blue (SELL) segments
- **No Legend Entry**: Does not appear in the chart legend
- **Hover Template**: Simple format showing "wave Value: X.XXXXXX"

### Technical Implementation

```python
# Add third hover trace named "wave" that shows values only for red/blue segments
red_blue_mask = red_mask | blue_mask
if red_blue_mask.any():
    red_blue_data = display_df[red_blue_mask]
    fig.add_trace(
        go.Scatter(
            x=red_blue_data.index,
            y=red_blue_data[plot_wave_col],
            mode='markers',  # Use markers to show only at specific points
            name='wave',
            marker=dict(
                size=0,  # Invisible markers
                color='rgba(0,0,0,0)'  # Transparent
            ),
            showlegend=False,  # Don't show in legend
            hoverinfo='y+name',  # Show value and name
            hovertemplate='<b>wave</b><br>Value: %{y:.6f}<extra></extra>'  # Custom hover template
        ),
        row=2, col=1
    )
```

## Usage

### Command
```bash
uv run run_analysis.py show csv mn1 -d fastest --rule wave:339,10,2,fast,22,11,4,fast,prime,55,open
```

### Expected Behavior
1. **Lower Chart**: Shows Wave indicator with colored segments
2. **Hover Effects**:
   - **Main Wave segments**: Show "Wave Value: X.XXXXXX Color: Red (BUY)" or "Blue (SELL)"
   - **Third wave trace**: Shows "wave Value: X.XXXXXX" (only on red/blue segments)
   - **Fast Line**: Shows "Fast Line Value: X.XXXXXX Color: Red (Signal)"
   - **MA Line**: Shows "MA Line Value: X.XXXXXX Color: Light Blue (MA)"

## Benefits

1. **Clean Hover Experience**: Provides a simple way to view Wave values without color information
2. **Selective Display**: Only shows hover information where there are meaningful signals
3. **Non-Intrusive**: Invisible markers don't interfere with the visual display
4. **Consistent Naming**: Uses lowercase "wave" to distinguish from main "Wave" segments

## Testing

The feature is fully tested with:
- ✅ Third wave hover trace creation
- ✅ Data filtering (only red/blue segments)
- ✅ Invisible marker properties
- ✅ Hover template correctness

### Running Tests
```bash
uv run pytest tests/plotting/test_wave_hover_enhancement.py -v
```

## Technical Notes

- Uses `mode='markers'` with invisible markers to create hover points
- Filters data using `red_mask | blue_mask` to include only buy/sell signals
- Maintains backward compatibility with existing Wave indicator functionality
- Follows the same pattern as other hover enhancements in the codebase
