# SCHR Wave2 Quick Start Guide

## Quick Start

### Basic Command
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_wave2
```

### Advanced Command with Custom Parameters
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_wave2:339,10,2,Fast,22,11,4,Fast,Prime,22
```

## Parameter Explanation

```
schr_wave2:long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period
```

### Default Values
- **long1**: 339 (first long period)
- **fast1**: 10 (first fast period)
- **trend1**: 2 (first trend period)
- **tr1**: Fast (first trading rule)
- **long2**: 22 (second long period)
- **fast2**: 11 (second fast period)
- **trend2**: 4 (second trend period)
- **tr2**: Fast (second trading rule)
- **global_tr**: Prime (global trading rule)
- **sma_period**: 22 (SMA period)

## Trading Rules

### Individual Wave Rules
- **Fast**: Wave > FastLine = BUY, Wave < FastLine = SELL
- **Zone**: Wave > 0 = BUY, Wave < 0 = SELL
- **StrongTrend**: Trend confirmation with zone filtering
- **WeakTrend**: Counter-trend signals with zone filtering
- **FastZoneReverse**: Reverse logic for zone-based trading

### Global Trading Rules
- **Prime**: Use signal when both waves agree
- **Reverse**: Reverse the signal when both waves agree
- **PrimeZone**: Zone-filtered prime rule
- **ReverseZone**: Zone-filtered reverse rule

## Signal Interpretation

- **1 (BUY)**: Both waves indicate upward momentum
- **2 (SELL)**: Both waves indicate downward momentum
- **0 (NO SIGNAL)**: Waves disagree or no clear trend

## Quick Examples

### Conservative Settings (Long-term trends)
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_wave2:500,20,5,StrongTrend,50,15,8,Zone,Prime,30
```

### Aggressive Settings (Short-term signals)
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_wave2:100,5,2,Fast,15,8,3,Fast,Prime,10
```

### Balanced Settings (Medium-term analysis)
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_wave2:200,10,3,Fast,25,12,5,Zone,PrimeZone,20
```

## Market Conditions

### Trending Markets
- Use **Fast** + **StrongTrend** combinations
- Longer periods (200-500)
- **Prime** global rule

### Ranging Markets
- Use **Zone** + **WeakTrend** combinations
- Shorter periods (10-50)
- **PrimeZone** global rule

### Volatile Markets
- Use longer periods and **PrimeZone** rules
- Balance responsiveness with stability
- Consider **Reverse** rules for contrarian signals

## Tips for Success

1. **Start with Defaults**: Begin with default parameters
2. **Adjust Periods**: Modify based on your timeframe
3. **Test Rules**: Experiment with different trading rule combinations
4. **Monitor Performance**: Use trading metrics to evaluate results
5. **Optimize Gradually**: Make small changes and test thoroughly

## Common Issues

- **No Signals**: Periods too long for data length
- **Too Many Signals**: Increase periods or use restrictive rules
- **Late Signals**: Reduce periods for faster response
- **Poor Performance**: Review parameter combinations

## Next Steps

1. **Read Full Documentation**: See `docs/reference/indicators/trend/schr_wave2.md`
2. **Run Tests**: Execute test suite for validation
3. **Experiment**: Try different parameter combinations
4. **Optimize**: Fine-tune for your specific market and timeframe
