# Vertical Scrollbar for AUTO Mode

## Overview

The AUTO mode with `-d fastest` option now includes a vertical scrollbar functionality that allows users to navigate through all charts without overlapping issues.

## Features

### Vertical Scrollbar Implementation
- **Fixed Height Container**: Charts are displayed in a container with a fixed height of 800px
- **Smooth Scrolling**: Custom CSS scrollbar with rounded corners and hover effects
- **Responsive Design**: Adapts to different screen sizes while maintaining usability

### CSS Styling
```css
.chart-container {
    height: 800px;
    overflow-y: auto;
    padding: 20px;
}

.chart-container::-webkit-scrollbar {
    width: 12px;
}

.chart-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 6px;
}

.chart-container::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 6px;
}

.chart-container::-webkit-scrollbar-thumb:hover {
    background: #555;
}
```

### Information Panel
The HTML output includes an information panel at the bottom showing:
- Total number of panels (Candlestick + indicators + Volume)
- Number of data points
- List of displayed columns
- Instructions for using the scrollbar

## Usage

### Command
```bash
uv run run_analysis.py show csv mn1 -d fastest --rule AUTO
```

### Output
- Generates an HTML file with vertical scrollbar functionality
- Automatically opens in the default browser
- File saved as: `results/plots/auto_fastest_CSVExport_GBPUSD_PERIOD_MN1.html`

## Technical Implementation

### File Location
- **Source**: `src/plotting/fastest_auto_plot.py`
- **Tests**: `tests/plotting/test_fastest_auto_plot.py`

### Key Functions
- `plot_auto_fastest_parquet()`: Main function that creates the scrollable HTML dashboard
- HTML wrapper with custom CSS for scrollbar styling
- Information panel generation with chart statistics

### Test Coverage
The implementation includes comprehensive test coverage:
- Basic functionality testing
- CSS scrollbar properties verification
- Information panel content validation
- Error handling for edge cases
- Different data format support

## Benefits

1. **Better User Experience**: No more overlapping charts
2. **Easy Navigation**: Smooth scrolling through all indicators
3. **Visual Clarity**: Each chart is clearly separated and readable
4. **Information Display**: Built-in statistics panel for context
5. **Responsive Design**: Works on different screen sizes

## Browser Compatibility

The vertical scrollbar implementation uses WebKit-specific CSS properties:
- **Chrome/Edge**: Full support
- **Safari**: Full support
- **Firefox**: Falls back to default scrollbar styling
- **Other browsers**: Default scrollbar behavior

## Future Enhancements

Potential improvements for future versions:
- Horizontal scrollbar for wide charts
- Zoom functionality for individual panels
- Collapsible panels for better space utilization
- Custom scrollbar themes
- Keyboard navigation support 