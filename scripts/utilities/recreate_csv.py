#!/usr/bin/env python3
"""
Script to recreate CSV files from JSON indicator files.
"""

import pandas as pd
import json
from pathlib import Path

def convert_json_to_csv(json_file_path, csv_file_path):
    """Convert a JSON indicator file to CSV format."""
    try:
        # Read JSON file
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Convert index column to proper format if it exists
        if 'index' in df.columns:
            df['index'] = pd.to_datetime(df['index']).dt.strftime('%Y-%m-%d')
        
        # Save as CSV
        df.to_csv(csv_file_path, index=False)
        print(f"✅ Created: {csv_file_path}")
        print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {json_file_path}: {e}")
        return False

def main():
    """Main function to convert JSON files to CSV."""
    json_dir = Path("data/indicators/json")
    csv_dir = Path("data/indicators/csv")
    
    # Ensure CSV directory exists
    csv_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all JSON files
    json_files = list(json_dir.glob("*UNKNOWN*.json"))
    print(f"Found {len(json_files)} JSON files to convert:")
    
    for json_file in json_files:
        print(f"\n📄 Processing: {json_file.name}")
        
        # Create corresponding CSV filename
        csv_filename = json_file.stem + ".csv"
        csv_file = csv_dir / csv_filename
        
        # Convert
        convert_json_to_csv(json_file, csv_file)
    
    print(f"\n🎉 Conversion complete!")
    print(f"📁 Check the CSV files in: {csv_dir}")

if __name__ == "__main__":
    main()
