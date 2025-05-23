#!/usr/bin/env python3
"""
Test runner script for neozork-hld-prediction

Usage:
    python run_tests.py [test_module]

Examples:
    # Run all tests
    python run_tests.py

    # Run specific test module
    python run_tests.py tests.eda.test_feature_importance

    # Run specific test class
    python run_tests.py tests.eda.test_feature_importance.TestFeatureImportance

    # Run specific test method
    python run_tests.py tests.eda.test_feature_importance.TestFeatureImportance.test_compute_feature_importance_regression
"""
import sys
import unittest

if __name__ == "__main__":
    # If no arguments are provided, discover and run all tests
    if len(sys.argv) == 1:
        print("Running all tests...")
        test_suite = unittest.defaultTestLoader.discover('tests')
        unittest.TextTestRunner().run(test_suite)

    # If a test module is specified, run that specific test
    else:
        test_name = sys.argv[1]
        print(f"Running test: {test_name}")
        unittest.main(module=None, argv=[sys.argv[0], test_name])
