#!/usr/bin/env python3
"""
Markdown to HTML Converter with Python Code Highlighting
Converts .md files to HTML with beautiful formatting and syntax highlighting
"""

import os
import re
import markdown
from pathlib import Path
from typing import List, Dict, Optional
import argparse
from datetime import datetime


class MarkdownToHTMLConverter:
 """Converts markdown files to HTML with custom styling and syntax highlighting"""

 def __init__(self, input_dir: str, output_dir: str):
 self.input_dir = Path(input_dir)
 self.output_dir = Path(output_dir)
 self.output_dir.mkdir(exist_ok=True)

 # Configure markdown with extensions
 self.md = markdown.Markdown(
 extensions=[
 'codehilite',
 'fenced_code',
 'tables',
 'toc',
 'attr_List',
 'def_List',
 'footnotes',
 'md_in_html'
 ],
 extension_configs={
 'codehilite': {
 'css_class': 'highlight',
 'Use_pygments': False,
 'guess_lang': True
 }
 }
 )

 def get_html_template(self, title: str, content: str) -> str:
 """Generate HTML template with styling from Python_Formatting_Example.html"""
 return f"""<!DOCTYPE html>
<html lang="ru">
<head>
 <meta charset="UTF-8">
 <meta name="Viewport" content="width=device-width, initial-scale=1.0">
 <title>{title}</title>
 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
 <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
 <style>
 body {{
 font-family: -apple-system, BlinkMacsystemFont, 'Segoe UI', Roboto, sans-serif;
 line-height: 1.6;
 color: #333;
 max-width: 1000px;
 margin: 0 auto;
 padding: 20px;
 background-color: #f8f9fa;
 }}

 .container {{
 background: white;
 padding: 40px;
 border-radius: 10px;
 box-shadow: 0 2px 10px rgba(0,0,0,0.1);
 }}

 h1 {{
 color: #2c3e50;
 border-bottom: 3px solid #3498db;
 padding-bottom: 10px;
 }}

 h2 {{
 color: #34495e;
 margin-top: 30px;
 border-left: 4px solid #3498db;
 padding-left: 15px;
 }}

 h3 {{
 color: #34495e;
 margin-top: 25px;
 border-left: 3px solid #3498db;
 padding-left: 12px;
 }}

 h4 {{
 color: #34495e;
 margin-top: 20px;
 border-left: 2px solid #3498db;
 padding-left: 10px;
 }}

 /* Enhanced code block styling */
 pre {{
 background: #1e1e1e;
 color: #d4d4d4;
 padding: 20px;
 border-radius: 8px;
 overflow-x: auto;
 border-left: 4px solid #3776ab;
 box-shadow: 0 4px 12px rgba(0,0,0,0.15);
 margin: 20px 0;
 position: relative;
 font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
 font-size: 14px;
 line-height: 1.5;
 }}

 pre::before {{
 content: attr(data-language);
 position: absolute;
 top: 10px;
 right: 15px;
 background: #3776ab;
 color: white;
 padding: 4px 8px;
 border-radius: 4px;
 font-size: 12px;
 font-weight: 600;
 text-transform: uppercase;
 }}

 code {{
 background: #f1f3f4;
 color: #d73a49;
 padding: 2px 6px;
 border-radius: 3px;
 font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
 font-size: 0.9em;
 }}

 pre code {{
 background: transparent;
 color: inherit;
 padding: 0;
 }}

 /* Prism.js color scheme for Python */
 .token.comment {{
 color: #6a9955;
 font-style: italic;
 }}

 .token.keyword {{
 color: #569cd6;
 font-weight: bold;
 }}

 .token.string {{
 color: #ce9178;
 }}

 .token.number {{
 color: #b5cea8;
 }}

 .token.function {{
 color: #dcdcaa;
 }}

 .token.class-name {{
 color: #4ec9b0;
 }}

 .token.operator {{
 color: #d4d4d4;
 }}

 .token.punctuation {{
 color: #d4d4d4;
 }}

 .token.variable {{
 color: #9cdcfe;
 }}

 .token.constant {{
 color: #4fc1ff;
 }}

 .token.builtin {{
 color: #dcdcaa;
 }}

 .token.boolean {{
 color: #569cd6;
 }}

 .token.parameter {{
 color: #9cdcfe;
 }}

 .token.property {{
 color: #9cdcfe;
 }}

 .token.attribute {{
 color: #9cdcfe;
 }}

 .token.tag {{
 color: #569cd6;
 }}

 .token.attr-name {{
 color: #92c5f8;
 }}

 .token.attr-value {{
 color: #ce9178;
 }}

 /* Table styling */
 table {{
 border-collapse: collapse;
 width: 100%;
 margin: 20px 0;
 background: white;
 box-shadow: 0 2px 8px rgba(0,0,0,0.1);
 border-radius: 8px;
 overflow: hidden;
 }}

 th, td {{
 padding: 12px 15px;
 text-align: left;
 border-bottom: 1px solid #e0e0e0;
 }}

 th {{
 background: #f8f9fa;
 font-weight: 600;
 color: #2c3e50;
 }}

 tr:hover {{
 background: #f8f9fa;
 }}

 /* Blockquote styling */
 blockquote {{
 border-left: 4px solid #17a2b8;
 background: #f8f9fa;
 padding: 15px 20px;
 margin: 20px 0;
 border-radius: 0 5px 5px 0;
 font-style: italic;
 }}

 /* List styling */
 ul, ol {{
 padding-left: 20px;
 }}

 li {{
 margin: 8px 0;
 }}

 /* Link styling */
 a {{
 color: #3498db;
 text-decoration: none;
 }}

 a:hover {{
 text-decoration: underline;
 }}

 /* Navigation */
 .nav-links {{
 background: #f8f9fa;
 padding: 20px;
 border-radius: 8px;
 margin: 20px 0;
 }}

 .nav-links a {{
 display: inline-block;
 margin: 5px 10px 5px 0;
 padding: 8px 12px;
 background: #3498db;
 color: white;
 border-radius: 4px;
 text-decoration: none;
 }}

 .nav-links a:hover {{
 background: #2980b9;
 text-decoration: none;
 }}

 /* Footer */
 .footer {{
 margin-top: 40px;
 padding-top: 20px;
 border-top: 1px solid #e0e0e0;
 color: #666;
 font-size: 0.9em;
 text-align: center;
 }}
 </style>
</head>
<body>
 <div class="container">
 {content}

 <div class="footer">
 <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
 <a href="index.html">← Back to index</a></p>
 </div>
 </div>

 <script>
 // Initialize Prism.js for syntax highlighting
 if (typeof Prism !== 'undefined') {{
 Prism.highlightall();
 }}

 // Add language labels to code blocks
 document.addEventListener('DOMContentLoaded', function() {{
 const codeBlocks = document.querySelectorall('pre code');
 codeBlocks.forEach(block => {{
 const pre = block.parentElement;
 const className = block.className;
 const language = className.replace('language-', '') || 'text';
 pre.setAttribute('data-language', language);
 }});
 }});
 </script>
</body>
</html>"""

 def process_markdown_file(self, md_file: Path) -> str:
 """Process a single markdown file and return HTML content"""
 with open(md_file, 'r', encoding='utf-8') as f:
 content = f.read()

 # Convert markdown to HTML
 html_content = self.md.convert(content)

 # Reset markdown instance for next file
 self.md.reset()

 return html_content

 def extract_title_from_content(self, content: str) -> str:
 """Extract title from markdown content (first h1)"""
 lines = content.split('\n')
 for line in lines:
 if line.startswith('# '):
 return line[2:].strip()
 return "Documentation"

 def convert_file(self, md_file: Path) -> Path:
 """Convert a single markdown file to HTML"""
 print(f"Converting: {md_file.name}")

 # Read markdown content
 with open(md_file, 'r', encoding='utf-8') as f:
 md_content = f.read()

 # Extract title
 title = self.extract_title_from_content(md_content)

 # Convert to HTML
 html_content = self.process_markdown_file(md_file)

 # Generate full HTML
 full_html = self.get_html_template(title, html_content)

 # Save HTML file
 html_file = self.output_dir / f"{md_file.stem}.html"
 with open(html_file, 'w', encoding='utf-8') as f:
 f.write(full_html)

 return html_file

 def convert_all_files(self) -> List[Path]:
 """Convert all markdown files in input directory"""
 md_files = List(self.input_dir.glob("*.md"))
 html_files = []

 print(f"found {len(md_files)} markdown files to convert")

 for md_file in md_files:
 try:
 html_file = self.convert_file(md_file)
 html_files.append(html_file)
 except Exception as e:
 print(f"Error converting {md_file.name}: {e}")

 return html_files

 def create_index_file(self, html_files: List[Path]) -> Path:
 """Create index.html with links to all converted files"""
 index_content = """
 <h1>Neozork AutoML Documentation</h1>

 <div class="exPlanation">
 <strong>📚 Complete guide on Neozork AutoML:</strong><br>
 Комплексная documentation on созданию робастных ML-систем with использованием AutoML технологий.
 </div>

 <h2>Содержание</h2>
 <div class="nav-links">
 """

 # Sort files by name to maintain order
 html_files.sort(key=lambda x: x.name)

 for html_file in html_files:
 # Extract title from filename or content
 title = html_file.stem.replace('_', ' ').replace('-', ' ').title()
 if title.startswith('01 '):
 title = title[3:] # Remove leading number
 elif title.startswith('02 '):
 title = title[3:]
 elif title.startswith('03 '):
 title = title[3:]
 elif title.startswith('04 '):
 title = title[3:]
 elif title.startswith('05 '):
 title = title[3:]
 elif title.startswith('06 '):
 title = title[3:]
 elif title.startswith('07 '):
 title = title[3:]
 elif title.startswith('08 '):
 title = title[3:]
 elif title.startswith('09 '):
 title = title[3:]
 elif title.startswith('10 '):
 title = title[3:]
 elif title.startswith('11 '):
 title = title[3:]
 elif title.startswith('12 '):
 title = title[3:]
 elif title.startswith('13 '):
 title = title[3:]
 elif title.startswith('14 '):
 title = title[3:]
 elif title.startswith('15 '):
 title = title[3:]
 elif title.startswith('16 '):
 title = title[3:]
 elif title.startswith('17 '):
 title = title[3:]
 elif title.startswith('18 '):
 title = title[3:]

 index_content += f'<a href="{html_file.name}">{title}</a>\n'

 index_content += """
 </div>

 <h2>О проекте</h2>
 <p>Neozork AutoML - это комплексная система for создания робастных машинного обучения решений with использованием современных AutoML технологий. documentation охватывает все аспекты from installation окружения to развертывания in production.</p>

 <h2>Основные разделы</h2>
 <ul>
 <li><strong>installation and configuration:</strong> Полная configuration окружения for разработки</li>
 <li><strong>Подготовка данных:</strong> Методы очистки and подготовки данных</li>
 <li><strong>Обучение моделей:</strong> AutoML подходы and best practices</li>
 <li><strong>Тестирование:</strong> Backtesting and валидация моделей</li>
 <li><strong>Риск-менеджмент:</strong> Management рисками in ML системах</li>
 <li><strong>Развертывание:</strong> Production deployment and Monitoring</li>
 </ul>

 <div class="exPlanation">
 <strong>💡 Совет:</strong> Начните with раздела "installation окружения" and следуйте документации on порядку for лучшего понимания материала.
 </div>
 """

 # Generate full index HTML
 full_index = self.get_html_template("Neozork AutoML Documentation", index_content)

 # Save index file
 index_file = self.output_dir / "index.html"
 with open(index_file, 'w', encoding='utf-8') as f:
 f.write(full_index)

 return index_file


def main():
 """main function to run the converter"""
 parser = argparse.ArgumentParser(description='Convert Markdown files to HTML with beautiful formatting')
 parser.add_argument('--input-dir', '-i',
 default='/users/rostsh/Documents/DIS/REPO/neozork-hld-Prediction/docs/automl/neozork',
 help='Input directory containing .md files')
 parser.add_argument('--output-dir', '-o',
 default='/users/rostsh/Documents/DIS/REPO/neozork-hld-Prediction/docs/automl/neozork/html',
 help='Output directory for HTML files')

 args = parser.parse_args()

 # Create converter
 converter = MarkdownToHTMLConverter(args.input_dir, args.output_dir)

 # Convert all files
 print("starting conversion process...")
 html_files = converter.convert_all_files()

 # Create index file
 print("Creating index file...")
 index_file = converter.create_index_file(html_files)

 print(f"\n✅ Conversion COMPLETED!")
 print(f"📁 Input directory: {args.input_dir}")
 print(f"📁 Output directory: {args.output_dir}")
 print(f"📄 Converted {len(html_files)} files")
 print(f"📄 index file: {index_file.name}")
 print(f"\n🌐 Open {index_file} in your browser to View the documentation!")


if __name__ == "__main__":
 main()
