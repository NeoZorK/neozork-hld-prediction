#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive System Script for NeoZorK HLD Prediction

This script provides an interactive interface for the entire system,
including EDA, Feature Engineering, and other capabilities.

Usage:
    python interactive_system.py
    ./interactive_system.py
"""

import argparse
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.interactive.core.interactive_system import InteractiveSystem
except ImportError as e:
    print(f"Error importing interactive system: {e}")
    print("Please ensure all dependencies are installed and the project structure is correct.")
    sys.exit(1)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="NeoZorK HLD Prediction Interactive System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--version', '-v', action='version', version='1.0.0')
    
    args = parser.parse_args()
    
    try:
        system = InteractiveSystem()
        system.run()
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠️  System interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ System failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
