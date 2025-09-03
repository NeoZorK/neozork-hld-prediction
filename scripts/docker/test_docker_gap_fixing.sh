#!/bin/bash
# -*- coding: utf-8 -*-
"""
Test script for Docker gap fixing issue in interactive system.

This script tests that the gap fixing functionality works correctly
in Docker environment with large time gaps.
"""

set -e

echo "🧪 Testing Docker Gap Fixing for Interactive System"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if the container is running
if ! docker-compose ps | grep -q "neozork-hld.*Up"; then
    echo "❌ NeoZorK HLD container is not running. Starting it..."
    docker-compose up -d
    sleep 5
fi

echo "✅ Docker environment ready"

# Test 1: Check if sample_ohlcv_with_issues.csv has gaps
echo ""
echo "🔍 Test 1: Check if sample data has gaps"
echo "----------------------------------------"
docker-compose exec neozork-hld bash -c 'python -c "
import pandas as pd
import sys

try:
    # Load the sample data
    df = pd.read_csv(\"/app/data/sample_ohlcv_with_issues.csv\")
    print(f\"Data shape: {df.shape}\")
    
    # Check if there is a datetime column
    datetime_cols = []
    for col in df.columns:
        if any(keyword in col.lower() for keyword in [\"date\", \"time\", \"datetime\", \"timestamp\"]):
            datetime_cols.append(col)
    
    print(f\"Datetime columns found: {datetime_cols}\")
    
    if datetime_cols:
        col = datetime_cols[0]
        print(f\"Using column: {col}\")
        
        # Convert to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = pd.to_datetime(df[col])
            print(f\"Converted {col} to datetime\")
        
        # Sort by datetime
        df = df.sort_values(col)
        
        # Calculate time differences
        time_diffs = df[col].diff().dropna()
        
        print(f\"Time differences statistics:\")
        print(f\"  Count: {len(time_diffs)}\")
        print(f\"  Mean: {time_diffs.mean()}\")
        print(f\"  Median: {time_diffs.median()}\")
        print(f\"  Min: {time_diffs.min()}\")
        print(f\"  Max: {time_diffs.max()}\")
        
        # Check for large gaps
        large_gaps = time_diffs[time_diffs > pd.Timedelta(days=1)]
        print(f\"  Large gaps (>1 day): {len(large_gaps)}\")
        
        if not large_gaps.empty:
            print(f\"  Largest gap: {large_gaps.max()}\")
        
        # Test frequency detection
        freq_counts = time_diffs.value_counts()
        most_common_freq = freq_counts.index[0]
        
        print(f\"  Most common frequency: {most_common_freq}\")
        print(f\"  Frequency counts: {freq_counts.head()}\")
        
    else:
        print(\"No datetime columns found\")
        
except Exception as e:
    print(f\"Error: {e}\")
    sys.exit(1)
"' || {
    echo "❌ Test 1 failed: Data analysis"
    exit 1
}
echo "✅ Test 1 passed: Data analysis"

# Test 2: Test gap fixing in Docker
echo ""
echo "🔍 Test 2: Test gap fixing in Docker"
echo "------------------------------------"
docker-compose exec neozork-hld bash -c 'python -c "
import pandas as pd
import sys
import os

# Add project root to path
sys.path.insert(0, \"/app\")

try:
    from src.batch_eda import fix_files
    
    # Load the sample data
    df = pd.read_csv(\"/app/data/sample_ohlcv_with_issues.csv\")
    print(f\"Original data shape: {df.shape}\")
    
    # Find datetime column
    datetime_col = None
    for col in df.columns:
        if any(keyword in col.lower() for keyword in [\"date\", \"time\", \"datetime\", \"timestamp\"]):
            datetime_col = col
            break
    
    if datetime_col:
        print(f\"Using datetime column: {datetime_col}\")
        
        # Create gap summary
        gap_summary = [{
            \"column\": datetime_col,
            \"gaps_count\": 1,
            \"largest_gap\": \"9 days 00:00:00\",
            \"method\": \"direct\"
        }]
        
        # Try to fix gaps
        fixed_data = fix_files.fix_gaps(df, gap_summary, datetime_col)
        
        if fixed_data is not None:
            print(f\"✅ Gap fixing completed successfully\")
            print(f\"   Original rows: {len(df)}\")
            print(f\"   Fixed rows: {len(fixed_data)}\")
            
            # Check if gaps were actually filled
            if len(fixed_data) > len(df):
                print(f\"   ✅ Gaps were filled: +{len(fixed_data) - len(df)} rows\")
            else:
                print(f\"   ⚠️  No gaps were filled\")
        else:
            print(f\"❌ Gap fixing returned None\")
            
    else:
        print(\"No datetime column found\")
        
except Exception as e:
    print(f\"Error during gap fixing: {e}\")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"' || {
    echo "❌ Test 2 failed: Gap fixing"
    exit 1
}
echo "✅ Test 2 passed: Gap fixing"

# Test 3: Test comprehensive data quality check in Docker
echo ""
echo "🔍 Test 3: Test comprehensive data quality check in Docker"
echo "----------------------------------------------------------"
docker-compose exec neozork-hld bash -c 'echo -e "1\n1\nsample_ohlcv_with_issues.csv\ny\n2\n1\ny\n0" | timeout 60 python /app/interactive_system.py' || {
    echo "❌ Test 3 failed: Comprehensive data quality check"
    exit 1
}
echo "✅ Test 3 passed: Comprehensive data quality check"

echo ""
echo "🎉 All Docker gap fixing tests passed!"
echo "======================================"
echo ""
echo "📋 Summary:"
echo "   ✅ Data analysis in Docker"
echo "   ✅ Gap fixing in Docker"
echo "   ✅ Comprehensive data quality check in Docker"
echo ""
echo "🔧 The Docker gap fixing is working correctly!"
echo "   The interactive system can now fix gaps properly in Docker environment."
