#!/bin/bash
# -*- coding: utf-8 -*-
"""
Simple test for Docker EOF issue in interactive system.

This script tests the basic functionality to identify the EOF issue.
"""

set -e

echo "🧪 Simple Docker EOF Test"
echo "========================"

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

# Test 1: Simple interactive system startup and exit
echo ""
echo "🔍 Test 1: Simple startup and exit"
echo "----------------------------------"
docker-compose exec neozork-hld bash -c 'echo "0" | python /app/interactive_system.py' || {
    echo "❌ Test 1 failed: Simple startup"
    exit 1
}
echo "✅ Test 1 passed: Simple startup"

# Test 2: Load data and exit
echo ""
echo "🔍 Test 2: Load data and exit"
echo "----------------------------"
docker-compose exec neozork-hld bash -c 'echo -e "1\n1\nsample_ohlcv_with_issues.csv\ny\n0" | python /app/interactive_system.py' || {
    echo "❌ Test 2 failed: Load data"
    exit 1
}
echo "✅ Test 2 passed: Load data"

# Test 3: Load data, go to EDA, and exit
echo ""
echo "🔍 Test 3: Load data, go to EDA, and exit"
echo "----------------------------------------"
docker-compose exec neozork-hld bash -c 'echo -e "1\n1\nsample_ohlcv_with_issues.csv\ny\n2\n0\n0" | python /app/interactive_system.py' || {
    echo "❌ Test 3 failed: EDA menu"
    exit 1
}
echo "✅ Test 3 passed: EDA menu"

# Test 4: Load data, go to EDA, run comprehensive check, and exit
echo ""
echo "🔍 Test 4: Load data, go to EDA, run comprehensive check, and exit"
echo "----------------------------------------------------------------"
docker-compose exec neozork-hld bash -c 'echo -e "1\n1\nsample_ohlcv_with_issues.csv\ny\n2\n1\nn\n0\n0" | python /app/interactive_system.py' || {
    echo "❌ Test 4 failed: Comprehensive check without fixing"
    exit 1
}
echo "✅ Test 4 passed: Comprehensive check without fixing"

# Test 5: Load data, go to EDA, run comprehensive check, fix issues, and exit
echo ""
echo "🔍 Test 5: Load data, go to EDA, run comprehensive check, fix issues, and exit"
echo "---------------------------------------------------------------------------"
docker-compose exec neozork-hld bash -c 'echo -e "1\n1\nsample_ohlcv_with_issues.csv\ny\n2\n1\ny\n0\n0" | python /app/interactive_system.py' || {
    echo "❌ Test 5 failed: Comprehensive check with fixing"
    exit 1
}
echo "✅ Test 5 passed: Comprehensive check with fixing"

echo ""
echo "🎉 All simple Docker tests passed!"
echo "================================="
echo ""
echo "📋 Summary:"
echo "   ✅ Simple startup and exit"
echo "   ✅ Load data and exit"
echo "   ✅ Load data, go to EDA, and exit"
echo "   ✅ Load data, go to EDA, run comprehensive check, and exit"
echo "   ✅ Load data, go to EDA, run comprehensive check, fix issues, and exit"
echo ""
echo "🔧 The Docker EOF fix is working correctly!"
