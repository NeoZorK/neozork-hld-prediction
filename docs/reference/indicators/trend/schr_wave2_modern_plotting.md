# SCHR Wave2 Complete Plotting

## Overview

The SCHR Wave2 indicator provides comprehensive visualization with buy/sell signals on the upper OHLC chart and modern wave analysis lines on the lower subplot. This combines the best of both worlds: clear trading signals and professional wave analysis.

## Key Features

### Upper Chart Elements
- **Buy Signals**: Green upward triangles below price lows
- **Sell Signals**: Red downward triangles above price highs
- **Clean OHLC**: Professional candlestick display without clutter

### Lower Chart Elements
- **Wave Lines**: Color-changing lines based on positive/negative values
- **Fast Line**: Consistent orange line for momentum analysis
- **MA Line**: Yellow moving average for trend smoothing

## Visual Components

### Trading Signals (Upper Chart)

#### Buy Signals
- **Symbol**: Green upward triangles
- **Position**: Slightly below price lows
- **Color**: Green (#00ff00)
- **Purpose**: Entry points for long positions

#### Sell Signals
- **Symbol**: Red downward triangles
- **Position**: Slightly above price highs
- **Color**: Red (#ff0000)
- **Purpose**: Entry points for short positions

### Wave Lines (Lower Chart)

#### Main Wave Line
- **Positive Values**: Blue color (#0000ff)
- **Negative Values**: Red color (#ff0000)
- **Width**: 3px
- **Style**: Smooth spline curves
- **Purpose**: Primary trend indicator with color coding

#### Fast Line
- **Color**: Always Orange (#ffa500)
- **Width**: 2.5px
- **Style**: Smooth spline curves
- **Purpose**: Short-term momentum indicator

#### MA Line
- **Color**: Always Yellow (#ffff00)
- **Width**: 2px
- **Style**: Smooth spline curves
- **Purpose**: Long-term trend smoothing

### Chart Elements

#### Zero Line
- **Style**: Dotted line
- **Color**: Modern Gray (#636363)
- **Opacity**: 80%
- **Purpose**: Reference line for wave analysis

#### Y-Axis
- **Title**: "SCHR Wave2"
- **Range**: [-0.5, 0.5]
- **Grid**: Subtle gray (rgba(0,0,0,0.08))
- **Font**: Modern typography

#### Legend
- **Position**: Top-left (x=0.02, y=0.98)
- **Background**: Semi-transparent white
- **Border**: Subtle gray border
- **Font**: Clean, readable typography

## Usage

### Command
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_wave2:339,10,2,Fast,22,11,4,Fast,Prime,22
```

### What You'll See
1. **Upper Chart**: OHLC candlesticks with buy/sell triangles
2. **Lower Chart**: Three wave lines with dynamic coloring
3. **Legend**: Clear identification of each component
4. **Zero Line**: Reference line for wave analysis

## Benefits

### For Traders
- **Clear Entry Points**: Visual buy/sell signals on price chart
- **Wave Analysis**: Professional wave pattern visualization
- **Color Coding**: Intuitive positive/negative wave identification

### For Analysis
- **Signal Confirmation**: Combine price signals with wave analysis
- **Trend Visualization**: Clear wave relationships and patterns
- **Professional Appearance**: Suitable for presentations and analysis

## Technical Implementation

### Signal Generation
- **Buy Signal (1)**: Generated when both waves indicate upward momentum
- **Sell Signal (2)**: Generated when both waves indicate downward momentum
- **No Signal (0)**: Generated when waves disagree or no clear trend

### Wave Calculation
- **ECORE**: Exponential change rate analysis
- **Dual Smoothing**: Wave and fast line calculations
- **Global Rules**: Flexible trading rule combinations

### Color Logic
- **Wave Line**: Blue for positive values, red for negative values
- **Fast Line**: Always orange for consistency
- **MA Line**: Always yellow for clear identification

## Signal Interpretation

### Buy Signals
- **Strong Buy**: Both waves show buy signals with Prime rule
- **Trend Buy**: Wave in positive zone with trend confirmation
- **Crossover Buy**: Wave crosses above FastLine

### Sell Signals
- **Strong Sell**: Both waves show sell signals with Prime rule
- **Trend Sell**: Wave in negative zone with trend confirmation
- **Crossover Sell**: Wave crosses below FastLine

### No Signal
- **Conflicting Signals**: Waves show different directions
- **Weak Confirmation**: Insufficient signal strength

## Performance Characteristics

### Strengths
- **Dual Confirmation**: Reduces false signals through dual-wave analysis
- **Visual Clarity**: Clear signals and professional wave display
- **Flexible Rules**: Multiple trading rule combinations
- **Trend Following**: Excellent for trending markets

### Limitations
- **Complex Parameters**: Requires careful parameter optimization
- **Signal Lag**: May lag in fast-moving markets
- **Parameter Sensitivity**: Performance varies with parameter selection

## Future Enhancements

### Planned Features
- **Custom Color Schemes**: User-selectable color palettes
- **Signal Filtering**: Advanced signal filtering options
- **Wave Pattern Recognition**: Automated pattern identification
- **Export Options**: High-resolution chart export

### User Customization
- **Theme Selection**: Light/dark themes
- **Line Styles**: Solid, dashed, dotted options
- **Chart Layout**: Adjustable subplot arrangements

## Support

For questions or issues with the SCHR Wave2 plotting:

1. **Check Documentation**: Review this guide and related materials
2. **Run Tests**: Execute test suite to verify functionality
3. **Report Issues**: Use project issue tracking system
4. **Community Support**: Engage with user community

## Related Files

- `src/plotting/dual_chart_fastest.py` - Main plotting implementation
- `tests/plotting/test_schr_wave2_modern_plotting.py` - Test suite
- `src/calculation/indicators/trend/schr_wave2_ind.py` - Indicator calculation
- `docs/reference/indicators/trend/schr_wave2.md` - Technical documentation
