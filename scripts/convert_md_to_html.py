#!/usr/bin/env python3
"""
Script to convert all .md files in docs/automl/neozork/ to HTML
with beautiful formatting and syntax highlighting
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.md_to_html_converter import MarkdownToHTMLConverter


def main():
    """Convert all markdown files to HTML"""
    # Define paths
    input_dir = Path(__file__).parent.parent / "docs" / "automl" / "neozork"
    output_dir = Path(__file__).parent.parent / "docs" / "automl" / "neozork" / "html"
    
    print("🚀 Starting Markdown to HTML conversion...")
    print(f"📁 Input directory: {input_dir}")
    print(f"📁 Output directory: {output_dir}")
    
    # Check if input directory exists
    if not input_dir.exists():
        print(f"❌ Error: Input directory {input_dir} does not exist!")
        return 1
    
    # Create converter
    converter = MarkdownToHTMLConverter(str(input_dir), str(output_dir))
    
    # Convert all files
    print("\n📄 Converting markdown files...")
    html_files = converter.convert_all_files()
    
    if not html_files:
        print("❌ No files were converted!")
        return 1
    
    # Create index file
    print("\n📚 Creating index file...")
    index_file = converter.create_index_file(html_files)
    
    print(f"\n✅ Conversion completed successfully!")
    print(f"📄 Converted {len(html_files)} files")
    print(f"📄 Index file: {index_file.name}")
    print(f"\n🌐 Open {index_file} in your browser to view the documentation!")
    
    # List converted files
    print("\n📋 Converted files:")
    for html_file in sorted(html_files):
        print(f"  • {html_file.name}")
    
    return 0


if __name__ == "__main__":
    exit(main())
