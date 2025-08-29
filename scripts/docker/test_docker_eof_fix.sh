#!/bin/bash
# -*- coding: utf-8 -*-
"""
Test script for Docker EOF fix in interactive system.

This script tests that the interactive system handles EOF properly
in Docker environment and doesn't exit unexpectedly after fixing data issues.
"""

set -e

echo "🧪 Testing Docker EOF Fix for Interactive System"
echo "================================================"

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

# Test 1: Basic interactive system startup
echo ""
echo "🔍 Test 1: Basic interactive system startup"
echo "-------------------------------------------"
docker-compose exec neozork-hld bash -c 'echo "0" | python /app/interactive_system.py' || {
    echo "❌ Test 1 failed: Basic startup"
    exit 1
}
echo "✅ Test 1 passed: Basic startup"

# Test 2: Load data and run comprehensive data quality check
echo ""
echo "🔍 Test 2: Load data and run comprehensive data quality check"
echo "------------------------------------------------------------"
docker-compose exec neozork-hld bash -c 'echo -e "1\n1\nsample_ohlcv_with_issues.csv\ny\n2\n1\nn\n0" | python /app/interactive_system.py' || {
    echo "❌ Test 2 failed: Data quality check without fixing"
    exit 1
}
echo "✅ Test 2 passed: Data quality check without fixing"

# Test 3: Load data, run comprehensive data quality check, and fix issues
echo ""
echo "🔍 Test 3: Load data, run comprehensive data quality check, and fix issues"
echo "------------------------------------------------------------------------"
docker-compose exec neozork-hld bash -c 'echo -e "1\n1\nsample_ohlcv_with_issues.csv\ny\n2\n1\ny\n0" | python /app/interactive_system.py' || {
    echo "❌ Test 3 failed: Data quality check with fixing"
    exit 1
}
echo "✅ Test 3 passed: Data quality check with fixing"

# Test 4: Test EOF handling in EDA menu
echo ""
echo "🔍 Test 4: Test EOF handling in EDA menu"
echo "----------------------------------------"
docker-compose exec neozork-hld bash -c 'echo -e "1\n1\nsample_ohlcv_with_issues.csv\ny\n2\n1\ny" | python /app/interactive_system.py' || {
    echo "❌ Test 4 failed: EOF handling in EDA menu"
    exit 1
}
echo "✅ Test 4 passed: EOF handling in EDA menu"

# Test 5: Test complete workflow with EOF
echo ""
echo "🔍 Test 5: Test complete workflow with EOF"
echo "------------------------------------------"
docker-compose exec neozork-hld bash -c 'echo -e "1\n1\nsample_ohlcv_with_issues.csv\ny\n2\n1\ny" | timeout 30 python /app/interactive_system.py' || {
    echo "❌ Test 5 failed: Complete workflow with EOF"
    exit 1
}
echo "✅ Test 5 passed: Complete workflow with EOF"

echo ""
echo "🎉 All Docker EOF fix tests passed!"
echo "==================================="
echo ""
echo "📋 Summary:"
echo "   ✅ Basic interactive system startup"
echo "   ✅ Data quality check without fixing"
echo "   ✅ Data quality check with fixing"
echo "   ✅ EOF handling in EDA menu"
echo "   ✅ Complete workflow with EOF"
echo ""
echo "🔧 The Docker EOF fix is working correctly!"
echo "   The interactive system now handles EOF gracefully"
echo "   and doesn't exit unexpectedly after fixing data issues."
