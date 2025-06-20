#!/usr/bin/env python3
"""
Script to create test parquet files from existing JSON indicator files.
"""

import pandas as pd
import json
from pathlib import Path

def convert_json_to_parquet(json_file_path, parquet_file_path):
    """Convert a JSON indicator file to parquet format."""
    try:
        # Read JSON file
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Convert index column to datetime if it exists
        if 'index' in df.columns:
            df['index'] = pd.to_datetime(df['index'])
            df.set_index('index', inplace=True)
        
        # Save as parquet
        df.to_parquet(parquet_file_path)
        print(f"✅ Created: {parquet_file_path}")
        print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {json_file_path}: {e}")
        return False

def main():
    """Main function to convert JSON files to parquet."""
    json_dir = Path("data/indicators/json")
    parquet_dir = Path("data/indicators/parquet")
    
    # Ensure parquet directory exists
    parquet_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all JSON files
    json_files = list(json_dir.glob("*.json"))
    print(f"Found {len(json_files)} JSON files to convert:")
    
    for json_file in json_files:
        print(f"\n📄 Processing: {json_file.name}")
        
        # Create corresponding parquet filename
        parquet_filename = json_file.stem + ".parquet"
        parquet_file = parquet_dir / parquet_filename
        
        # Convert
        convert_json_to_parquet(json_file, parquet_file)
    
    print(f"\n🎉 Conversion complete!")
    print(f"📁 Check the parquet files in: {parquet_dir}")

if __name__ == "__main__":
    main()
