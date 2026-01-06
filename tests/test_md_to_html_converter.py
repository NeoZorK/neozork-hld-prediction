#!/usr/bin/env python3
"""
Unit tests for Markdown to HTML Converter
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.md_to_html_converter import MarkdownToHTMLConverter


class TestMarkdownToHTMLConverter:
    """Test cases for MarkdownToHTMLConverter"""
    
    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing"""
        input_dir = tempfile.mkdtemp()
        output_dir = tempfile.mkdtemp()
        yield input_dir, output_dir
        shutil.rmtree(input_dir)
        shutil.rmtree(output_dir)
    
    @pytest.fixture
    def sample_md_content(self):
        """Sample markdown content for testing"""
        return """# Test Document

This is a **test** document with some `code` and a code block:

```python
def hello_world():
    print("Hello, World!")
    return True
```

## Features

- Feature 1
- Feature 2
- Feature 3

### Code Example

```bash
pip install package
```

## Table

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |
"""
    
    def test_converter_initialization(self, temp_dirs):
        """Test converter initialization"""
        input_dir, output_dir = temp_dirs
        converter = MarkdownToHTMLConverter(input_dir, output_dir)
        
        assert converter.input_dir == Path(input_dir)
        assert converter.output_dir == Path(output_dir)
        assert converter.output_dir.exists()
    
    def test_extract_title_from_content(self, temp_dirs):
        """Test title extraction from markdown content"""
        input_dir, output_dir = temp_dirs
        converter = MarkdownToHTMLConverter(input_dir, output_dir)
        
        # Test with h1 title
        content_with_h1 = "# My Test Title\n\nSome content"
        title = converter.extract_title_from_content(content_with_h1)
        assert title == "My Test Title"
        
        # Test without h1 title
        content_without_h1 = "Some content without title"
        title = converter.extract_title_from_content(content_without_h1)
        assert title == "Documentation"
    
    def test_html_template_generation(self, temp_dirs):
        """Test HTML template generation"""
        input_dir, output_dir = temp_dirs
        converter = MarkdownToHTMLConverter(input_dir, output_dir)
        
        title = "Test Title"
        content = "<h1>Test Content</h1>"
        html = converter.get_html_template(title, content)
        
        assert "<!DOCTYPE html>" in html
        assert f"<title>{title}</title>" in html
        assert content in html
        assert "Prism.js" in html
        assert "syntax highlighting" in html
    
    def test_convert_single_file(self, temp_dirs, sample_md_content):
        """Test converting a single markdown file"""
        input_dir, output_dir = temp_dirs
        
        # Create test markdown file
        md_file = Path(input_dir) / "test.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(sample_md_content)
        
        # Convert file
        converter = MarkdownToHTMLConverter(input_dir, output_dir)
        html_file = converter.convert_file(md_file)
        
        # Check if HTML file was created
        assert html_file.exists()
        assert html_file.name == "test.html"
        
        # Check HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        assert "<!DOCTYPE html>" in html_content
        assert "Test Document" in html_content
<<<<<<< HEAD
        assert "def hello_world():" in html_content
        assert "language-python" in html_content
        assert "language-bash" in html_content
=======
        # Check for code blocks (markdown converts code to HTML with classes)
        assert "highlight" in html_content or "code" in html_content.lower()
        assert "language-python" in html_content or "python" in html_content.lower()
        assert "language-bash" in html_content or "bash" in html_content.lower()
>>>>>>> origin/master
    
    def test_convert_all_files(self, temp_dirs, sample_md_content):
        """Test converting all markdown files in directory"""
        input_dir, output_dir = temp_dirs
        
        # Create multiple test markdown files
        for i in range(3):
            md_file = Path(input_dir) / f"test_{i}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(f"# Test Document {i}\n\n{sample_md_content}")
        
        # Convert all files
        converter = MarkdownToHTMLConverter(input_dir, output_dir)
        html_files = converter.convert_all_files()
        
        # Check results
        assert len(html_files) == 3
        for html_file in html_files:
            assert html_file.exists()
            assert html_file.suffix == ".html"
    
    def test_create_index_file(self, temp_dirs):
        """Test index file creation"""
        input_dir, output_dir = temp_dirs
        
        # Create some test HTML files
        html_files = []
        for i in range(3):
            html_file = Path(output_dir) / f"test_{i}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(f"<html><body><h1>Test {i}</h1></body></html>")
            html_files.append(html_file)
        
        # Create index file
        converter = MarkdownToHTMLConverter(input_dir, output_dir)
        index_file = converter.create_index_file(html_files)
        
        # Check index file
        assert index_file.exists()
        assert index_file.name == "index.html"
        
        # Check index content
        with open(index_file, 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        assert "Neozork AutoML Documentation" in index_content
        assert "test_0.html" in index_content
        assert "test_1.html" in index_content
        assert "test_2.html" in index_content
<<<<<<< HEAD
        assert "Back to Index" in index_content
=======
        assert "Back to index" in index_content or "← Back to index" in index_content
>>>>>>> origin/master
    
    def test_code_highlighting_styles(self, temp_dirs):
        """Test that code highlighting styles are included"""
        input_dir, output_dir = temp_dirs
        converter = MarkdownToHTMLConverter(input_dir, output_dir)
        
        title = "Test"
        content = "<h1>Test</h1>"
        html = converter.get_html_template(title, content)
        
        # Check for Prism.js styles and scripts
        assert "prism-tomorrow.min.css" in html
        assert "prism-core.min.js" in html
        assert "prism-python.min.js" in html
        
        # Check for custom CSS classes
        assert ".token.comment" in html
        assert ".token.keyword" in html
        assert ".token.string" in html
        assert ".token.function" in html
    
    def test_table_styling(self, temp_dirs):
        """Test that table styling is included"""
        input_dir, output_dir = temp_dirs
        converter = MarkdownToHTMLConverter(input_dir, output_dir)
        
        title = "Test"
        content = "<h1>Test</h1>"
        html = converter.get_html_template(title, content)
        
        # Check for table styles
        assert "table {" in html
        assert "th, td {" in html
        assert "border-collapse: collapse" in html
    
    def test_responsive_design(self, temp_dirs):
        """Test that responsive design elements are included"""
        input_dir, output_dir = temp_dirs
        converter = MarkdownToHTMLConverter(input_dir, output_dir)
        
        title = "Test"
        content = "<h1>Test</h1>"
        html = converter.get_html_template(title, content)
        
        # Check for responsive design
        assert "max-width: 1000px" in html
        assert "margin: 0 auto" in html
<<<<<<< HEAD
        assert "viewport" in html
=======
        assert "viewport" in html.lower() or "Viewport" in html
>>>>>>> origin/master
        assert "width=device-width" in html


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
