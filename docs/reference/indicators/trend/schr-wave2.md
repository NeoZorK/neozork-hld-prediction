# SCHR Wave2 Indicator

## Overview

SCHR Wave2 is an advanced dual-wave trend prediction indicator developed by Shcherbyna Rostyslav. It combines two independent wave calculations with multiple trading rules to generate comprehensive trading signals.

## Features

- **Dual-Wave Analysis**: Combines two independent wave calculations for enhanced signal accuracy
- **Multiple Trading Rules**: 10 different trading rule combinations for flexible signal generation
- **Global Rule Combinations**: 7 global trading rules to combine signals from both waves
- **Real-time Signal Generation**: Provides buy/sell signals based on wave crossovers and trend analysis
- **Multiple Timeframe Support**: Configurable periods for different market conditions

## Algorithm

### Core Components

1. **ECORE Calculation**: Exponential Change of Rate calculation for price momentum
2. **Wave Calculation**: Primary trend wave based on ECORE values
3. **FastLine Calculation**: Secondary trend line for signal generation
4. **Trading Rule Application**: Multiple rule sets for signal generation
5. **Global Rule Combination**: Final signal combination from both waves

### Mathematical Formulas

#### ECORE (Exponential Change of Rate)
```
ECORE[i] = ECORE[i-1] + (2.0/period) * (price_change_percent - ECORE[i-1])
```

#### Wave Calculation
```
Wave[i] = Wave[i-1] + (2.0/fast_period) * (ECORE[i] - Wave[i-1])
```

#### FastLine Calculation
```
FastLine[i] = FastLine[i-1] + (2.0/(trend_period + 1)) * (Wave[i] - FastLine[i-1])
```

## Parameters

### Wave 1 Parameters
- **long1** (int): First long period for ECORE calculation (default: 339)
- **fast1** (int): First fast period for Wave calculation (default: 10)
- **trend1** (int): First trend period for FastLine calculation (default: 2)
- **tr1** (string): First trading rule (default: Fast)

### Wave 2 Parameters
- **long2** (int): Second long period for ECORE calculation (default: 22)
- **fast2** (int): Second fast period for Wave calculation (default: 11)
- **trend2** (int): Second trend period for FastLine calculation (default: 4)
- **tr2** (string): Second trading rule (default: Fast)

### Global Parameters
- **global_tr** (string): Global trading rule (default: Prime)
- **sma_period** (int): SMA period for moving average calculation (default: 22)

## Trading Rules

### Individual Wave Rules (tr1, tr2)

| Rule | Description | Signal Logic |
|------|-------------|--------------|
| **Fast** | Standard crossover | BUY if Wave > FastLine, SELL if Wave < FastLine |
| **Zone** | Zone-based signals | BUY if Wave > 0, SELL if Wave < 0 |
| **StrongTrend** | Strong trend confirmation | BUY only in plus zone when Wave > FastLine, SELL only in minus zone when Wave < FastLine |
| **WeakTrend** | Weak trend confirmation | BUY only in plus zone when Wave < FastLine, SELL only in minus zone when Wave > FastLine |
| **FastZoneReverse** | Reverse zone signals | BUY in minus zone when Wave > FastLine, SELL in plus zone when Wave < FastLine |
| **BetterTrend** | Enhanced trend analysis | Enhanced trend confirmation logic |
| **BetterFast** | Enhanced fast signals | Enhanced crossover logic |
| **Rost** | Rost-specific logic | Custom signal generation |
| **TrendRost** | Trend-based Rost logic | Trend-enhanced Rost signals |
| **BetterTrendRost** | Enhanced trend Rost | Best of trend and Rost logic |

### Global Trading Rules (global_tr)

| Rule | Description | Signal Logic |
|------|-------------|--------------|
| **Prime** | Standard combination | Use signal when both waves agree |
| **Reverse** | Reverse signals | Reverse the signal when both waves agree |
| **PrimeZone** | Prime with zone filtering | Prime rule + zone-based filtering |
| **ReverseZone** | Reverse with zone filtering | Reverse rule + zone-based filtering |
| **NewZone** | New zone logic | Advanced zone-based combination |
| **LongZone** | Long zone analysis | Extended zone analysis |
| **LongZoneReverse** | Long zone reverse | Extended zone reverse logic |

## Usage

### Basic Usage
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_wave2
```

### With Custom Parameters
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_wave2:339,10,2,Fast,22,11,4,Fast,Prime,22
```

### Parameter Examples

#### Conservative Settings
```bash
schr_wave2:500,20,5,StrongTrend,50,25,10,Zone,PrimeZone,50
```

#### Aggressive Settings
```bash
schr_wave2:100,5,1,Fast,15,8,3,Fast,Prime,15
```

#### Balanced Settings
```bash
schr_wave2:200,15,3,BetterTrend,30,15,6,Fast,Prime,30
```

## Output Columns

### Main Indicator Values
- `schr_wave2_wave`: Main wave values
- `schr_wave2_fast_line`: Fast line values
- `schr_wave2_ma_line`: Moving average line values
- `schr_wave2_direction`: Trading direction (1=Up, 2=Down)
- `schr_wave2_signal`: Trading signals (0=No Signal, 1=Buy, 2=Sell)

### Wave Components
- `schr_wave2_wave1`: First wave values
- `schr_wave2_wave2`: Second wave values
- `schr_wave2_fast_line1`: First wave fast line
- `schr_wave2_fast_line2`: Second wave fast line
- `schr_wave2_color1`: First wave color signals
- `schr_wave2_color2`: Second wave color signals

### Parameters Reference
- `schr_wave2_long1`, `schr_wave2_fast1`, `schr_wave2_trend1`, `schr_wave2_tr1`
- `schr_wave2_long2`, `schr_wave2_fast2`, `schr_wave2_trend2`, `schr_wave2_tr2`
- `schr_wave2_global_tr`, `schr_wave2_sma_period`

## Signal Interpretation

### Buy Signals (1)
- **Strong Buy**: Both waves show buy signals with Prime rule
- **Trend Buy**: Wave in positive zone with trend confirmation
- **Crossover Buy**: Wave crosses above FastLine

### Sell Signals (2)
- **Strong Sell**: Both waves show sell signals with Prime rule
- **Trend Sell**: Wave in negative zone with trend confirmation
- **Crossover Sell**: Wave crosses below FastLine

### No Signal (0)
- **Conflicting Signals**: Waves show different directions
- **Weak Confirmation**: Insufficient signal strength
- **Sideways Market**: No clear trend direction

## Best Practices

### Parameter Selection
1. **Start with Defaults**: Use default parameters for initial testing
2. **Adjust for Timeframe**: Longer periods for higher timeframes, shorter for lower
3. **Market Conditions**: Use StrongTrend for trending markets, Fast for ranging markets
4. **Risk Management**: Combine with other indicators for confirmation

### Trading Strategy
1. **Signal Confirmation**: Wait for both waves to agree
2. **Trend Alignment**: Ensure signals align with overall market trend
3. **Risk Control**: Use stop losses based on wave levels
4. **Position Sizing**: Adjust based on signal strength and market volatility

## Performance Considerations

### Calculation Speed
- **Fast Mode**: Optimized for real-time trading
- **Standard Mode**: Balanced performance and accuracy
- **Precision Mode**: Maximum accuracy with slower performance

### Memory Usage
- **Minimal**: Efficient memory usage for large datasets
- **Scalable**: Handles multiple timeframes simultaneously
- **Optimized**: Reduced memory footprint for embedded systems

## Troubleshooting

### Common Issues
1. **No Signals Generated**: Check parameter ranges and data quality
2. **Inconsistent Signals**: Verify trading rule combinations
3. **Performance Issues**: Optimize parameter values for your timeframe

### Debug Information
- Enable debug logging for detailed calculation information
- Check parameter validation and data preprocessing
- Verify indicator column generation and plotting

## Related Indicators

- **SCHR Rost**: Single-wave trend indicator
- **SCHR Trend**: Direction-based trend indicator
- **SCHR Direction**: Growth-based direction indicator

## References

- **Original MQL5**: SCHR_Wave2.mq5 by Shcherbyna Rostyslav
- **Algorithm**: Based on exponential smoothing and wave analysis
- **Implementation**: Python port with 100% algorithm compatibility
