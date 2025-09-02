# Cleaned Data for ML Models

This folder contains cleaned and preprocessed data files that are ready for machine learning model training and prediction.

## Purpose

The cleaned data files are created after running comprehensive data quality checks and gap fixing through the interactive system. These files are optimized for ML workflows and eliminate the need to re-process raw data each time.

## File Naming Convention

Files follow this naming pattern:
```
cleaned_{folder_name}_{mask}_{timeframe}_{timestamp}.parquet
```

Example:
- `cleaned_cache_eurusd_M1_20250101_143022.parquet`
- `cleaned_indicators_gbpusd_H1_20250101_143022.parquet`

## File Format

All cleaned data files are saved in **Parquet format** which provides:

- **Fast Loading**: Optimized for pandas/pyarrow with column-oriented storage
- **Efficient Memory Usage**: Built-in compression reduces file size
- **ML Compatibility**: Works seamlessly with all major ML libraries
- **Data Integrity**: Preserves data types and handles missing values properly

## Data Quality Standards

Each cleaned data file meets these quality standards:

✅ **No Missing Values**: All gaps in time series have been filled using appropriate algorithms
✅ **No Infinite Values**: All infinite values have been replaced with valid numbers
✅ **No Outliers**: Extreme values have been handled appropriately
✅ **Consistent Data Types**: All columns have proper data types for ML processing
✅ **Time Series Integrity**: Timestamps are properly formatted and sequential
✅ **Memory Optimized**: Data is stored efficiently for large-scale processing

## Metadata

Each cleaned data file has a corresponding `.json` metadata file containing:

- Original data source information
- Processing parameters used
- Data shape and column information
- Memory usage statistics
- Creation timestamp
- Quality check results

## Usage in ML Workflows

### Loading Data
```python
import pandas as pd

# Load cleaned data
df = pd.read_parquet('data/cleaned_data/cleaned_cache_eurusd_M1_20250101_143022.parquet')

# Data is immediately ready for ML processing
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Data types: {df.dtypes}")
```

### Feature Engineering
```python
# Data is already clean, focus on feature creation
from sklearn.preprocessing import StandardScaler

# Prepare features
feature_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
X = df[feature_columns]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### Model Training
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, df['target'], test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

## Benefits

1. **Time Savings**: No need to re-run data quality checks
2. **Consistency**: All ML models use the same cleaned dataset
3. **Performance**: Parquet format loads faster than CSV/JSON
4. **Memory Efficiency**: Optimized storage reduces memory usage
5. **Reproducibility**: Metadata tracks exactly how data was processed
6. **Scalability**: Efficient format for large datasets

## Maintenance

- Cleaned data files are automatically created when using the interactive system
- Old files can be safely deleted to save disk space
- Always check metadata to understand data processing history
- Re-run data cleaning if source data changes significantly

## Best Practices

1. **Version Control**: Keep metadata files to track data lineage
2. **Regular Updates**: Re-process data when source data changes
3. **Storage Management**: Archive old cleaned files to save space
4. **Quality Validation**: Verify cleaned data meets your ML requirements
5. **Documentation**: Update this README when adding new data types

## Support

For questions about cleaned data or data quality issues, refer to:
- Interactive System documentation
- Data quality check reports
- Gap fixing algorithm documentation
- ML model training guides
