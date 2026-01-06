#!/usr/bin/env python3
"""
Markdown in TML Manual for AutoML Gluon
Transforms 33 chapters from .md files into a single TML masterpiece in Python_Formatting_Example.html

Author: Shcherbyna Rostyslav
Date: 2024
"""

import os
import re
import glob
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import markdown
from markdown.extensions import codehilite, tables, toc

class AutoMLGluonHTMLConverter:
""Markdown Files in HTML Manual for AutoML Gluon""

 def __init__(self, source_dir: str = "docs/automl/gluon", output_dir: str = "docs/automl/gluon"):
 self.source_dir = Path(source_dir)
 self.output_dir = Path(output_dir)
 self.chapters = []
 self.toc_items = []

 # configuration Markdown
 self.md = markdown.Markdown(
 extensions=[
 'codehilite',
 'tables',
 'toc',
 'fenced_code',
 'attr_List',
 'def_List',
 'footnotes',
 'md_in_html'
 ],
 extension_configs={
 'codehilite': {
 'css_class': 'language-python',
 'Use_pygments': True,
 'noclasses': False
 },
 'toc': {
 'permalink': True,
'Permalink_tile': 'Reference on this section'
 }
 }
 )

 def get_chapter_order(self) -> List[str]:
"Gets the order of the chapters in the correct sequence."
 return [
 "01_installation.md",
 "02_basic_usage.md",
 "03_advanced_configuration.md",
 "04_risk_Analysis.md",
 "05_low_risk_systems.md",
 "06_metrics.md",
 "07_validation.md",
 "08_production.md",
 "09_retraining.md",
 "10_best_practices.md",
 "11_apple_silicon_optimization.md",
 "12_examples.md",
 "13_simple_production_example.md",
 "14_advanced_production_example.md",
 "15_theory_and_fundamentals.md",
 "16_Troubleshooting.md",
 "17_interpretability_and_explainability.md",
 "18_advanced_topics.md",
 "19_ethics_and_responsible_ai.md",
 "20_case_studies.md",
 "21_wave2_indicator_Analysis.md",
 "22_schr_levels_Analysis.md",
 "23_schr_short3_Analysis.md",
 "24_super_system_ultimate.md",
 "25_reading_guide.md",
 "26_probability_usage_guide.md",
 "27_trading_bot_Monitoring.md",
 "28_feature_generation_advanced.md",
 "29_backtesting_methods.md",
 "30_walk_forward_Analysis.md",
 "31_monte_carlo_simulations.md",
 "32_Portfolio_Management.md",
 "33_llm_parallel_computing_setup.md"
 ]

 def get_chapter_info(self, filename: str) -> Dict[str, str]:
""Strikes the information about the chapter from the file name."
 chapter_num = filename.split('_')[0]
 chapter_name = filename.replace('.md', '').replace(f"{chapter_num}_", "").replace('_', ' ').title()

# Special titles for certain chapters
 special_names = {
 "01_installation": "installation and configuration",
"02_Basic_use": "Base use",
"03_advanced_configration": "Advanced configration",
"04_risk_Anallysis": "Risk Analysis",
"05_low_risk_systems": Low-risk systems,
"06_metrics": "metrics and evaluation",
"07_validation": "validation of models",
"08_production": "Sold deployment",
"09_retraining": "retraining models",
"10_best_practices": "Best practices",
"11_apple_silicon_optimization": "Apple Silicon Optimization",
"12_examples": Practical examples,
"13_simple_production_example": "Simple sold example",
"14_advanced_production_example": "Proceeded sales",
"15_theory_and_fundamentals": "Theory and framework",
 "16_Troubleshooting": "Troubleshooting",
"17_interpretability_and_explainability": "Interpretability",
18_advanced_topics: advanced topics,
"19_ethics_and_responsible_ai": "Ethics and Responsible AI",
"20_case_studies": "case-studies",
"21_wave2_indicator_analysis": "Wave2 analysis indicator",
"22_shr_levels_Anallysis": "SCHR levels of analysis",
"23_shr_short3_Anallysis": "SCHR Short3 Analysis",
"24_super_system_optimate": "Super Ultimate",
"25_reading_guid": "Guide on reading",
"26_probability_use_guid": "Guide on Probabilities",
"27_trading_bot_Monitoring": "Monitoring commercial bota",
"28_feature_energy_advanced": advanced indicator generation,
"29_backtesting_methods": "methods bactering",
"30_walk_forward_analysis": "Walk-forward analysis",
"31_monte_carlo_simulations": "Monte-Carlo simulations",
"32_Porthfolio_Management": "Management portfolio",
"33_lm_parallel_computing_setup": "configration of parallel calculations"
 }

 return {
 'number': chapter_num,
 'name': special_names.get(filename.replace('.md', ''), chapter_name),
 'filename': filename
 }

 def process_markdown_file(self, filepath: Path) -> Dict[str, Any]:
""""""""" "Checks one Markdown file."
 try:
 with open(filepath, 'r', encoding='utf-8') as f:
 content = f.read()

# We're extracting metadata
 title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
 author_match = re.search(r'\*\*Author:\*\* (.+)$', content, re.MULTILINE)
Data_match = re.search(r'\\\*Date:\\*(.+)$,content, re.MULTILINE)

# Processing images
 content = self.process_images(content)

# Converging in HTML
 html_content = self.md.convert(content)

# Let's drop the Markdown status for the next file
 self.md.reset()

 return {
 'title': title_match.group(1) if title_match else filepath.stem,
 'author': author_match.group(1) if author_match else 'Shcherbyna Rostyslav',
 'date': date_match.group(1) if date_match else '2024',
 'content': html_content,
 'filename': filepath.name
 }

 except Exception as e:
print(f) File processing error {filepath}: {e})
 return None

 def process_images(self, content: str) -> str:
"""""""""""""""""
# Replace the relative paths on absolute
 content = re.sub(
 r'<img src="images/',
 '<img src="images/',
 content
 )

# Adding styles for images
 content = re.sub(
 r'<img src="([^"]+)" alt="([^"]*)"',
 r'<img src="\1" alt="\2" style="max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"',
 content
 )

 return content

 def generate_toc(self) -> str:
"""""""" "Generate the content."
 toc_html = '<div class="toc">\n'
toc_html += `<h2>>the content (33 chapters)</h2>\n'
 toc_html += '<div class="toc-grid">\n'

 for i, chapter in enumerate(self.chapters, 1):
 if chapter:
 chapter_info = self.get_chapter_info(chapter['filename'])
 toc_html += f'''
 <div class="toc-item">
 <h3>{i}. {chapter_info['name']}</h3>
 <p>{self.get_chapter_describe(chapter_info['name'])}</p>
 </div>
 '''

 toc_html += '</div>\n</div>\n'
 return toc_html

 def get_chapter_describe(self, chapter_name: str) -> str:
"Returns describe chapter."
 describes = {
"Installation and configuration": "Strolling installation, system requirements, configration",
"Base Use": "Fundamentals of work with TabularPredictor, model training",
"Proved configuration": "Hyperparameters, ensembles, validation, feature engineering",
Risk Analysis: "Technical, Business and Operational Risks of ML Systems",
Low-risk systems: "create reliable and sustainable ML systems",
"Metrics and valuation": Classifications, regressions, time series, financial metrics,
"Validation of models": "Cross-validation, time series, Walk-forward analysis",
"Sold deployment": "API servers, Docker, Kubernetes, Monitoring",
"Retraining Models": "Automatic Retraining, Monitoring Drift",
"Best practices": "Preparation, choice of metric, optimization",
"Apple Silicon Optimization": "M1/M2/M3, MLX, Metal Performance Shaders",
Practical examples: "Bank, real estate, time series, classification",
"Simple sold example": "from ideas to deeds sold in eight steps,"
"The advanced product": "Microservices, scale, Monitoring",
"Theory and framework": "Mathematical framework, algorithms, principles",
"Troubleshooting": "Troubleshooting, decoupling, optimization",
"Interpretability": "Explanatoryness of Models, SHAP, LIME",
"Advanced themes": "Ansambles, feature engineering, optimization",
Ethic and Responsible AI: Justice, Transparency, Security,
Case Studies: Real projects and their solutions,
"Wave2 Analysis Indicator": "Technical Analysis and Indicators",
"SCHR levels of analysis": "Analysis of support and resistance levels",
"SCHR Short3 Analysis": "Scratcosm analysis of trade signals",
Super System Ultimate: Integrated Trading System,
"Guide on reading": "How to study material effectively",
"Guide on probability": "Working with probability in ML",
"Monitoring Commercial Bot": "Tracing and Management Bot",
"Advanced indicator generation": "Feature engineering for complex problems",
"Methods Becketting": "Trying strategies on historical data",
"Walk-forward analysis": "The rolling testing of strategies",
"Monte-Carlo Simulations": "Stochastic Risk Modelling",
Management Portfolio: Optimization and Diversification of the Portfolio,
"configuration of parallel calculations": "LLM and parallel calculations"
 }
Return describes.get(chapter_name, "Detained describe topics")

 def generate_html_template(self) -> str:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 return '''<!DOCTYPE html>
<html lang="ru">
<head>
 <meta charset="UTF-8">
 <meta name="Viewport" content="width=device-width, initial-scale=1.0">
<title>AutuML Gluon - Complete guide (33 chapters)</title>
 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
 <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
 <style>
 body {{
 font-family: -apple-system, BlinkMacsystemFont, 'Segoe UI', Roboto, sans-serif;
 line-height: 1.6;
 color: #333;
 max-width: 1200px;
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

 .header {
 text-align: center;
 margin-bottom: 40px;
 padding: 30px;
 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
 color: white;
 border-radius: 10px;
 }

 .header h1 {
 font-size: 2.5em;
 margin-bottom: 10px;
 border: none;
 }

 .header p {
 font-size: 1.2em;
 opacity: 0.9;
 }

 .toc {
 background: #f8f9fa;
 padding: 30px;
 border-radius: 10px;
 margin-bottom: 40px;
 border-left: 4px solid #667eea;
 }

 .toc h2 {
 color: #667eea;
 margin-bottom: 20px;
 border: none;
 padding: 0;
 }

 .toc-grid {
 display: grid;
 grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
 gap: 15px;
 }

 .toc-item {
 background: white;
 padding: 15px;
 border-radius: 8px;
 border-left: 4px solid #667eea;
 transition: transform 0.3s ease;
 }

 .toc-item:hover {
 transform: translateX(5px);
 }

 .toc-item h3 {
 color: #495057;
 margin-bottom: 8px;
 font-size: 1.1em;
 }

 .toc-item p {
 color: #6c757d;
 font-size: 0.9em;
 margin: 0;
 }

 h1 {
 color: #2c3e50;
 border-bottom: 3px solid #3498db;
 padding-bottom: 10px;
 }

 h2 {
 color: #34495e;
 margin-top: 40px;
 border-left: 4px solid #3498db;
 padding-left: 15px;
 }

 h3 {
 color: #495057;
 margin-top: 30px;
 border-left: 3px solid #667eea;
 padding-left: 12px;
 }

 h4 {
 color: #6c757d;
 margin-top: 20px;
 }

* Improved styles for Python code*
 pre {
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
 }

 pre::before {
 content: "Python";
 position: absolute;
 top: 10px;
 right: 15px;
 background: #3776ab;
 color: white;
 padding: 4px 8px;
 border-radius: 4px;
 font-size: 12px;
 font-weight: 600;
 }

* Color Selection for Python syntax*/
 .token.comment {
 color: #6a9955;
 font-style: italic;
 }

 .token.keyword {
 color: #569cd6;
 font-weight: bold;
 }

 .token.string {
 color: #ce9178;
 }

 .token.number {
 color: #b5cea8;
 }

 .token.function {
 color: #dcdcaa;
 }

 .token.class-name {
 color: #4ec9b0;
 }

 .token.operator {
 color: #d4d4d4;
 }

 .token.punctuation {
 color: #d4d4d4;
 }

 .token.variable {
 color: #9cdcfe;
 }

 .token.constant {
 color: #4fc1ff;
 }

 .token.builtin {
 color: #dcdcaa;
 }

 .token.boolean {
 color: #569cd6;
 }

 .exPlanation {
 background: #f8f9fa;
 border-left: 4px solid #17a2b8;
 padding: 15px;
 margin: 20px 0;
 border-radius: 0 5px 5px 0;
 }

 .warning {
 background: #f8d7da;
 border-left: 4px solid #dc3545;
 padding: 15px;
 margin: 20px 0;
 border-radius: 0 5px 5px 0;
 }

 .info {
 background: #d1ecf1;
 border-left: 4px solid #0dcaf0;
 padding: 15px;
 margin: 20px 0;
 border-radius: 0 5px 5px 0;
 }

 .success {
 background: #d4edda;
 border-left: 4px solid #28a745;
 padding: 15px;
 margin: 20px 0;
 border-radius: 0 5px 5px 0;
 }

 .feature-grid {
 display: grid;
 grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
 gap: 20px;
 margin: 20px 0;
 }

 .feature-card {
 background: #f8f9fa;
 padding: 20px;
 border-radius: 8px;
 border-left: 4px solid #667eea;
 }

 .feature-card h4 {
 color: #667eea;
 margin-bottom: 10px;
 }

 .metrics-table {
 width: 100%;
 border-collapse: collapse;
 margin: 20px 0;
 }

 .metrics-table th,
 .metrics-table td {
 border: 1px solid #dee2e6;
 padding: 12px;
 text-align: left;
 }

 .metrics-table th {
 background-color: #667eea;
 color: white;
 }

 .metrics-table tr:nth-child(even) {
 background-color: #f8f9fa;
 }

 .chapter {
 margin-bottom: 60px;
 padding: 30px;
 background: #f8f9fa;
 border-radius: 10px;
 border-left: 5px solid #667eea;
 }

 .chapter h2 {
 color: #667eea;
 margin-top: 0;
 border: none;
 padding: 0;
 }

 .back-to-top {
 position: fixed;
 bottom: 20px;
 right: 20px;
 background: #667eea;
 color: white;
 padding: 10px 15px;
 border-radius: 50px;
 text-decoration: none;
 box-shadow: 0 4px 12px rgba(0,0,0,0.15);
 transition: all 0.3s ease;
 }

 .back-to-top:hover {
 background: #5a6fd8;
 transform: translateY(-2px);
 }

 @media (max-width: 768px) {
 .toc-grid {
 grid-template-columns: 1fr;
 }

 .feature-grid {
 grid-template-columns: 1fr;
 }

 .header h1 {
 font-size: 2em;
 }
 }
 </style>
</head>
<body>
 <div class="container">
 <div class="header">
 <h1>AutoML Gluon</h1>
<p>Complete guide on automated machine learning</p>
<p><strong>33 chapters</strong> ¡strong>Author:</strong> Schherbyna Rostyslav ¡strong> Date:</strong> 2024</p>
 </div>

 {toc}

 {content}
 </div>

<a href="#"class="back-to-top">

 <script>
// Initiating Prism.js for syntax Selection
 if (typeof Prism !== 'undefined') {
 Prism.highlightall();
 }

/ / / Floating to anchors
 document.addEventListener('DOMContentLoaded', function() {
 const links = document.querySelectorall('a[href^="#"]');
 links.forEach(link => {
 link.addEventListener('click', function(e) {
 e.preventDefault();
 const target = document.querySelector(this.getAttribute('href'));
 if (target) {
 target.scrollIntoView({
 behavior: 'smooth',
 block: 'start'
 });
 }
 });
 });

♪ Up ♪
 const backToTop = document.querySelector('.back-to-top');
 backToTop.addEventListener('click', function(e) {
 e.preventDefault();
 window.scrollTo({
 top: 0,
 behavior: 'smooth'
 });
 });

Show/open the "Upstairs" button
 window.addEventListener('scroll', function() {
 if (window.scrollY > 300) {
 backToTop.style.display = 'block';
 } else {
 backToTop.style.display = 'none';
 }
 });
 });
 </script>
</body>
</html>'''

 def convert_chapters(self) -> None:
""Covers all chapters."
"Prent("♪ ♪ Start converting chapters... ♪

 chapter_order = self.get_chapter_order()

 for filename in chapter_order:
 filepath = self.source_dir / filename
 if filepath.exists():
(pint(f) processing: {filename})
 chapter_data = self.process_markdown_file(filepath)
 if chapter_data:
 self.chapters.append(chapter_data)
 else:
 print(f"⚠️ File not found: {filename}")

(f) oOWorkingno {len(self.chapters)} chapters)

 def generate_html(self) -> str:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Print("♪ ♪ HTML's powered manual... ♪

# Generate the table of contents
 toc_html = self.generate_toc()

# Generate the content of chapters
 content_html = ""
 for i, chapter in enumerate(self.chapters, 1):
 if chapter:
 chapter_info = self.get_chapter_info(chapter['filename'])
 content_html += f'''
 <div class="chapter" id="chapter-{i}">
 <h2>{i}. {chapter_info['name']}</h2>
 {chapter['content']}
 </div>
 '''

# Pick up a full TML
 html_template = self.generate_html_template()
 full_html = html_template.format(
 toc=toc_html,
 content=content_html
 )

 return full_html

 def save_html(self, html_content: str) -> None:
""Saves XML in file""
 output_file = self.output_dir / "AutoML_Gluon_Complete_Manual.html"

 with open(output_file, 'w', encoding='utf-8') as f:
 f.write(html_content)

Print(f"\HTML Manual retained: {output_file})

 def run(self) -> None:
"Launch the complete process of conversion."
"Prent("♪ Launch Markdown ♪ HTML) converter"
prent(f"\end directory: {self.source_dir}})
(pint(f)(end directory: {self.output_dir}})

# Converting chapters
 self.convert_chapters()

# Generate HTML
 html_content = self.generate_html()

# Save the TML
 self.save_html(html_content)

Print("

def main():
""The Main Function""
 converter = AutoMLGluonHTMLConverter()
 converter.run()

if __name__ == "__main__":
 main()
