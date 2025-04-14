# /run_analysis.py (root folder NeoZorK HLD)

import pandas as pd
# Use absolute imports to avoid issues with relative imports
from src.constants import TradingRule
from src.indicator import calculate_pressure_vector
from src.plotting import plot_indicator_results
from src import __version__ # Import version from __init__.py

print("Pressure Vector Calculation Module", __version__)

# Example data for testing
data = {
    'Open': [1.1, 1.11, 1.12, 1.115, 1.125, 1.13, 1.128, 1.135, 1.14, 1.138,
             1.142, 1.145, 1.140, 1.135, 1.130, 1.132, 1.138, 1.145, 1.148, 1.150],
    'High': [1.105, 1.115, 1.125, 1.12, 1.13, 1.135, 1.133, 1.14, 1.145, 1.142,
             1.146, 1.148, 1.143, 1.139, 1.136, 1.137, 1.142, 1.150, 1.152, 1.155],
    'Low': [1.095, 1.105, 1.115, 1.11, 1.12, 1.125, 1.125, 1.13, 1.135, 1.136,
            1.140, 1.142, 1.138, 1.133, 1.128, 1.130, 1.135, 1.143, 1.146, 1.148],
    'Close': [1.1, 1.11, 1.118, 1.118, 1.128, 1.128, 1.131, 1.138, 1.138, 1.14,
              1.145, 1.141, 1.136, 1.131, 1.131, 1.136, 1.144, 1.149, 1.151, 1.149],
    'TickVolume': [1000, 1200, 1100, 1300, 1500, 1400, 1600, 1700, 1550, 1650,
                   1750, 1800, 1600, 1900, 2000, 1850, 1950, 2100, 2050, 2200]
}

# Create a DataFrame with the example data
index = pd.date_range(start='2024-01-01', periods=len(data['Open']), freq='D')

# Create the DataFrame
ohlcv_df = pd.DataFrame(data, index=index)

# Set the instrument point size (for example, 0.00001 for Forex pairs)
instr_point = 0.00001



# --- Trading Rule 1 : PV_HighLow ---
print("--- Calculating Rule: PV_HighLow ---")
rule_to_test = TradingRule.PV_HighLow
result_df_1 = calculate_pressure_vector(
    df=ohlcv_df.copy(),
    point=instr_point,
    core_back=5, strength_back=3,
    tr_num=rule_to_test
)
print(result_df_1.tail())
plot_indicator_results(result_df_1, rule=rule_to_test, title="PV HighLow Rule Results")



# --- Trading Rule 2: Pressure_Vector ---
print("\n--- Calculating Rule: Pressure_Vector ---")
rule_to_test = TradingRule.Pressure_Vector
result_df_2 = calculate_pressure_vector(
    df=ohlcv_df.copy(),
    point=instr_point,
    core_back=5, strength_back=3,
    tr_num=rule_to_test
)
print(result_df_2.tail())
plot_indicator_results(result_df_2, rule=rule_to_test, title="Pressure Vector Rule Results")



# --- Trading Rule 3: CORE1 ---
print("\n--- Calculating Rule: CORE1 ---")
rule_to_test = TradingRule.CORE1
result_df_3 = calculate_pressure_vector(
    df=ohlcv_df.copy(),
    point=instr_point,
    core_back=14, strength_back=3,
    tr_num=rule_to_test
)
print(result_df_3.tail())
plot_indicator_results(result_df_3, rule=rule_to_test, title="CORE1 Rule Results")