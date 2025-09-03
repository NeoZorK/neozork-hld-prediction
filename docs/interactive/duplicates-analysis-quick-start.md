# Duplicates Analysis - Quick Start Guide

## 🚀 Quick Start

### Step 1: Load Data
```bash
./interactive_system.py
```
Select: `1. 📁 Load Data`

### Step 2: Navigate to EDA
Select: `2. 🔍 EDA Analysis`

### Step 3: Run Duplicates Analysis
Select: `7. 🔄 Duplicates Analysis`

## 📊 What You'll See

### Main Dataset Analysis
```
📊 MAIN TIMEFRAME DATASET ANALYSIS
----------------------------------------
   🔄 Found 5 exact duplicate rows (4.76%)
   📋 Sample duplicate rows:
      Row 0: {'timestamp': '2024-01-01 10:00:00', 'open': 1000.0}
```

### Multi-Timeframe Analysis (if available)
```
🔄 MULTI-TIMEFRAME DATASETS ANALYSIS
--------------------------------------------------
📊 Found 2 additional timeframes to analyze

⏱️  Analyzing M5 timeframe:
   📊 Shape: 53 rows × 6 columns
   🔄 Duplicates found: 3 (5.66%)
```

### Overall Summary
```
📋 OVERALL DUPLICATES ANALYSIS SUMMARY
--------------------------------------------------
   📊 Total rows analyzed: 177
   🔄 Total duplicates found: 8
   📈 Overall duplicate percentage: 4.52%

💡 RECOMMENDATIONS:
   • Consider using 'Fix Data Issues' option to remove duplicates
```

## 🔍 Types of Duplicates Detected

1. **Exact Duplicates** - Completely identical rows
2. **Timestamp Duplicates** - Same timestamp, different data
3. **OHLCV Duplicates** - Same price/volume values
4. **Business Logic Duplicates** - Same timestamp + same price

## 🛠️ Next Steps

### Option 1: Fix Data Issues
- Go back to EDA menu
- Select: `15. 🧹 Fix Data Issues`
- System will automatically remove duplicates

### Option 2: Generate Report
- Select: `13. 📋 Generate HTML Report`
- Get comprehensive analysis report

### Option 3: Continue Analysis
- Select other EDA options for complete data quality assessment

## 💡 Tips

- **Load multiple timeframes** for comprehensive analysis
- **Check sample data** to understand duplicate patterns
- **Use recommendations** to improve data quality
- **Combine with other EDA tools** for complete picture

## 🔧 Troubleshooting

### No Data Loaded
```
❌ No data loaded. Please load data first.
```
**Solution**: Go back to main menu and load data first

### No Additional Timeframes
```
💡 No additional timeframes found for analysis
   Only main dataset was analyzed
```
**Solution**: This is normal if you only loaded one timeframe

### Memory Issues
**Solution**: The system automatically optimizes for large datasets
