#!/usr/bin/env python3
# Test terminal plotting directly

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.plotting.term_plot import plot_indicator_results_term
from src.common.constants import TradingRule

# Create sample data
dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
data = {
    'Open': np.random.random(len(dates)) * 10 + 100,
    'High': np.random.random(len(dates)) * 10 + 105,
    'Low': np.random.random(len(dates)) * 10 + 95,
    'Close': np.random.random(len(dates)) * 10 + 100,
    'Volume': np.random.randint(1000, 5000, len(dates))
}

df = pd.DataFrame(data, index=dates)

print("Testing terminal plotting directly...")
try:
    plot_indicator_results_term(df, TradingRule.OHLCV, "Test Terminal Plot")
    print("Terminal plotting test completed successfully!")
except Exception as e:
    print(f"Terminal plotting test failed: {e}")
    import traceback
    traceback.print_exc()
