# Outlier Treatment Guide

## Overview

The NeoZorK HLD Prediction Interactive System now includes comprehensive outlier detection and treatment capabilities. This guide explains how to use the outlier treatment functionality that is automatically triggered after running Basic Statistics when outliers are detected.

## Automatic Outlier Detection

### When It Triggers

The outlier treatment interface automatically appears after running **Basic Statistics** when:
- Any column has more than 5% outliers (using IQR method)
- The system detects potentially problematic data distributions

### Detection Methods

The system uses multiple methods to detect outliers:

1. **IQR Method (Interquartile Range)**
   - Calculates Q1 (25th percentile) and Q3 (75th percentile)
   - Defines outliers as values outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
   - Most commonly used method

2. **Z-Score Method**
   - Calculates how many standard deviations a value is from the mean
   - Default threshold: 3.0 standard deviations
   - Good for normally distributed data

3. **Isolation Forest**
   - Machine learning-based outlier detection
   - Requires scikit-learn to be installed
   - Good for multivariate outlier detection

## Treatment Methods

### 1. Removal Method

**What it does:** Completely removes rows containing outliers.

**Pros:**
- Preserves data structure and relationships
- Eliminates extreme values that might skew analysis
- Simple and straightforward

**Cons:**
- Reduces dataset size
- May lose important information
- Can create gaps in time series data

**Best for:**
- When outliers are clearly errors
- When you have sufficient data to spare
- When outliers represent less than 10% of data

### 2. Capping Method

**What it does:** Caps outliers to reasonable bounds instead of removing them.

**Cap Methods:**
- **Percentile:** Caps to 1st and 99th percentiles
- **IQR:** Caps to IQR bounds (Q1 - 1.5×IQR, Q3 + 1.5×IQR)
- **Manual:** User-defined bounds

**Pros:**
- Preserves all data points
- Maintains dataset size
- Reduces impact of extreme values

**Cons:**
- May create artificial clustering at bounds
- Doesn't address underlying data quality issues

**Best for:**
- When you want to preserve all observations
- When outliers are legitimate but extreme
- When you need consistent dataset size

### 3. Winsorization Method

**What it does:** Replaces outliers with percentile values.

**How it works:**
- Replaces bottom 5% with 5th percentile value
- Replaces top 5% with 95th percentile value
- User can adjust these percentages

**Pros:**
- Preserves data distribution shape
- Maintains dataset size
- More sophisticated than simple capping

**Cons:**
- Creates artificial clustering
- May not be appropriate for all data types

**Best for:**
- When you want to preserve distribution characteristics
- When outliers are legitimate but need adjustment
- Statistical analysis requiring normal-like distributions

### 4. Custom Method

**What it does:** Allows different treatment methods for different columns.

**Use cases:**
- Some columns need removal, others need capping
- Different sensitivity to outliers for different variables
- Domain-specific requirements

## Safety Features

### Automatic Backup

Before any treatment, the system automatically creates a backup:
- **Location:** `data/backups/`
- **Format:** Parquet files with timestamps
- **Naming:** `outlier_backup_YYYYMMDD_HHMMSS_[suffix].parquet`

### Validation

After treatment, the system validates:
- **Data Integrity:** Ensures data is still valid
- **Shape Changes:** Reports if rows were removed
- **Missing Values:** Checks for new missing data
- **Infinite Values:** Detects computational issues

### Treatment History

The system tracks all treatments applied:
- Method used
- Columns affected
- Results summary
- Backup file locations

## Step-by-Step Usage

### 1. Run Basic Statistics

```bash
./interactive_system.py
# Navigate to: 2. EDA Analysis → 1. Basic Statistics
```

### 2. Review Outlier Analysis

The system will show:
- Columns with high outlier percentages
- Number of outliers per column
- Percentage of data affected

### 3. Choose Treatment Method

When prompted "Do you want to fix outliers? (Yes/No):", answer "Yes"

### 4. Select Treatment Approach

Choose from:
- **1. Removal** - Remove outlier rows
- **2. Capping** - Cap outliers to bounds
- **3. Winsorization** - Replace with percentile values
- **4. Custom** - Different method per column
- **5. Skip** - Continue without treatment

### 5. Configure Parameters

Depending on your choice:
- **Removal:** Confirm the action
- **Capping:** Choose cap method (percentile/iqr/manual)
- **Winsorization:** Set limits (e.g., 0.05,0.05)
- **Custom:** Choose method for each column

### 6. Review Results

The system will show:
- Treatment summary
- Validation results
- Option to check post-treatment outlier analysis

## Best Practices

### When to Treat Outliers

**Treat outliers when:**
- They represent more than 5% of data
- They are clearly errors or artifacts
- They significantly skew statistical measures
- They affect model performance

**Don't treat outliers when:**
- They represent legitimate extreme events
- They are important for your analysis
- They are part of the natural data distribution
- You have domain knowledge suggesting they're valid

### Method Selection Guidelines

| Scenario | Recommended Method | Reason |
|----------|-------------------|---------|
| Data errors | Removal | Eliminate incorrect data |
| Legitimate extremes | Capping | Preserve information |
| Statistical analysis | Winsorization | Maintain distribution |
| Mixed cases | Custom | Tailored approach |
| Time series | Capping/Winsorization | Preserve continuity |

### Validation Checklist

After treatment, verify:
- ✅ Data integrity maintained
- ✅ No unexpected missing values
- ✅ Outlier percentage reduced
- ✅ Statistical measures improved
- ✅ Backup files created

## Troubleshooting

### Common Issues

**"Error importing outlier handler"**
- Ensure the `src.eda.outlier_handler` module is available
- Check that all dependencies are installed

**"No outliers detected"**
- System only flags columns with >5% outliers
- Check individual column analysis in Basic Statistics

**"Treatment didn't work"**
- Try different treatment method
- Adjust parameters (e.g., different cap method)
- Check validation results for warnings

**"Lost too much data"**
- Use capping instead of removal
- Restore from backup and try different approach
- Consider custom treatment for specific columns

### Restoring from Backup

If you need to restore data:

```python
from src.batch_eda.outlier_handler import OutlierHandler

# Create handler with current data
handler = OutlierHandler(current_data)

# Restore from specific backup
success = handler.restore_from_backup("data/backups/outlier_backup_20240101_120000.parquet")

if success:
    current_data = handler.current_data
    print("Data restored successfully")
else:
    print("Failed to restore data")
```

## Advanced Features

### Custom Outlier Detection

You can modify detection parameters:

```python
# Custom IQR multiplier
outlier_mask, stats = handler.detect_outliers_iqr('column_name', multiplier=2.0)

# Custom Z-score threshold
outlier_mask, stats = handler.detect_outliers_zscore('column_name', threshold=2.5)
```

### Batch Processing

For multiple datasets:

```python
# Process multiple columns with same method
results = handler.treat_outliers_capping(['col1', 'col2', 'col3'], method='iqr')

# Apply different methods to different columns
handler.treat_outliers_removal(['col1'], method='iqr')
handler.treat_outliers_capping(['col2'], method='iqr', cap_method='percentile')
```

### Treatment History Analysis

Review all treatments applied:

```python
summary = handler.get_treatment_summary()
print(f"Total treatments: {summary['total_treatments']}")
print(f"Original shape: {summary['original_shape']}")
print(f"Current shape: {summary['current_shape']}")
```

## Integration with Workflow

### After Outlier Treatment

Once outliers are treated, you can:

1. **Run Basic Statistics again** to verify improvements
2. **Continue with Feature Engineering** using cleaned data
3. **Proceed to Model Development** with better data quality
4. **Export results** including treatment summary

### Data Export

Treatment results are automatically saved:

```python
# Access treatment summary
treatment_summary = current_results['outlier_treatment']

# Export treated data
current_data.to_parquet('data/cleaned_data.parquet')
```

## Conclusion

The outlier treatment functionality provides a comprehensive, safe, and user-friendly way to handle outliers in your data. With automatic backup creation, multiple treatment methods, and thorough validation, you can confidently improve your data quality while preserving important information.

Remember to always review the results and consider the context of your data before applying any treatment method.
