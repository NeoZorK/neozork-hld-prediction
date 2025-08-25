#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script for interactive system data loading functionality

This script demonstrates the new data loading features:
- P1: Load single file from data folder
- P2: Load all files from folder with optional mask
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.ml.interactive_system import InteractiveSystem


def demo_data_folder_scanning():
    """Demonstrate data folder scanning functionality."""
    print("🔍 DEMO: Data Folder Scanning")
    print("=" * 50)
    
    system = InteractiveSystem()
    data_folder = Path("data")
    
    print(f"📁 Scanning folder: {data_folder.absolute()}")
    
    # Find all data files
    data_files = []
    for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
        data_files.extend(data_folder.rglob(f"*{ext}"))
    
    print(f"✅ Found {len(data_files)} data files")
    
    # Show files by category
    categories = {}
    for file in data_files:
        category = file.parent.relative_to(data_folder)
        if category not in categories:
            categories[category] = []
        categories[category].append(file.name)
    
    print("\n📂 Files by category:")
    for category, files in categories.items():
        print(f"   {category}: {len(files)} files")
        for file in files[:3]:  # Show first 3 files
            print(f"     - {file}")
        if len(files) > 3:
            print(f"     ... and {len(files) - 3} more")
    
    print()


def demo_single_file_loading():
    """Demonstrate single file loading functionality."""
    print("📄 DEMO: Single File Loading")
    print("=" * 50)
    
    system = InteractiveSystem()
    
    # Find a sample file to demonstrate
    data_folder = Path("data")
    sample_files = list(data_folder.glob("sample_ohlcv_*.csv"))
    
    if not sample_files:
        print("⚠️  No sample files found for demonstration")
        return
    
    sample_file = sample_files[0]
    print(f"📄 Loading file: {sample_file.relative_to(data_folder)}")
    
    try:
        # Simulate the loading process
        data = system.load_data_from_file(str(sample_file))
        print(f"✅ Successfully loaded!")
        print(f"   Shape: {data.shape[0]} rows × {data.shape[1]} columns")
        print(f"   Columns: {list(data.columns)}")
        
        # Show data preview
        print(f"\n📋 Data preview:")
        print(data.head())
        
    except Exception as e:
        print(f"❌ Error loading file: {e}")
    
    print()


def demo_folder_loading_with_mask():
    """Demonstrate folder loading with mask functionality."""
    print("📁 DEMO: Folder Loading with Mask")
    print("=" * 50)
    
    system = InteractiveSystem()
    data_folder = Path("data")
    
    # Demo different mask patterns
    demo_cases = [
        ("data", None, "All files from data folder"),
        ("data", "sample", "Files with 'sample' in name"),
        ("data", "parquet", "All .parquet files"),
        ("data/raw_parquet", None, "All files from raw_parquet subfolder"),
    ]
    
    for folder, mask, description in demo_cases:
        print(f"🔍 {description}")
        print(f"   Input: '{folder}{' ' + mask if mask else ''}'")
        
        folder_path = Path(folder)
        if not folder_path.exists():
            print(f"   ⚠️  Folder not found: {folder_path}")
            continue
        
        # Find matching files
        data_files = []
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            if mask:
                pattern = f"*{mask}*{ext}"
                data_files.extend(folder_path.glob(pattern))
                # Also try case-insensitive search
                pattern = f"*{mask.upper()}*{ext}"
                data_files.extend(folder_path.glob(pattern))
                pattern = f"*{mask.lower()}*{ext}"
                data_files.extend(folder_path.glob(pattern))
            else:
                data_files.extend(folder_path.glob(f"*{ext}"))
        
        # Remove duplicates
        data_files = list(set(data_files))
        
        print(f"   Found {len(data_files)} files")
        if data_files:
            for file in data_files[:3]:  # Show first 3 files
                rel_path = file.relative_to(data_folder)
                print(f"     - {rel_path}")
            if len(data_files) > 3:
                print(f"     ... and {len(data_files) - 3} more")
        else:
            print(f"     No files found")
        
        print()


def demo_usage_examples():
    """Show usage examples for the new functionality."""
    print("💡 DEMO: Usage Examples")
    print("=" * 50)
    
    examples = [
        {
            "scenario": "Load a specific sample file",
            "menu_choice": "1",
            "input": "sample_ohlcv_1000.csv",
            "description": "Loads the specific CSV file from data folder"
        },
        {
            "scenario": "Load all GBPUSD files",
            "menu_choice": "2", 
            "input": "data gbpusd",
            "description": "Loads all files with 'gbpusd' in the filename"
        },
        {
            "scenario": "Load all parquet files",
            "menu_choice": "2",
            "input": "data parquet", 
            "description": "Loads all .parquet files from data folder"
        },
        {
            "scenario": "Load all files from indicators folder",
            "menu_choice": "2",
            "input": "data/indicators",
            "description": "Loads all files from data/indicators subfolder"
        },
        {
            "scenario": "Load CSV files from indicators",
            "menu_choice": "2",
            "input": "data/indicators csv",
            "description": "Loads all CSV files from data/indicators folder"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['scenario']}")
        print(f"   Menu: {example['menu_choice']}")
        print(f"   Input: '{example['input']}'")
        print(f"   Result: {example['description']}")
        print()


def main():
    """Run all demonstrations."""
    print("🚀 Interactive System Data Loading Demo")
    print("=" * 60)
    print("This demo shows the new data loading functionality")
    print("=" * 60)
    
    demos = [
        demo_data_folder_scanning,
        demo_single_file_loading,
        demo_folder_loading_with_mask,
        demo_usage_examples,
    ]
    
    for demo in demos:
        demo()
        print("-" * 60)
    
    print("🎉 Demo completed!")
    print("\n💡 To try the interactive system:")
    print("   uv run python scripts/ml/interactive_system.py")
    print("\n🧪 To run tests:")
    print("   uv run python tests/scripts/test_interactive_system_data_loading.py")


if __name__ == "__main__":
    main()
