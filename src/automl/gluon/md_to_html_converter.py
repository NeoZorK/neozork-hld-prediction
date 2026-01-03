#!/usr/bin/env python3
"""
Конвертер Markdown in HTML Manual for AutoML Gluon
Преобразует 33 главы из .md files in единый HTML мануал in стиле Python_Formatting_Example.html

Author: Shcherbyna Rostyslav
Дата: 2024
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
 """Конвертер Markdown files in HTML мануал for AutoML Gluon"""

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
 'permalink_title': 'Ссылка on этот раздел'
 }
 }
 )

 def get_chapter_order(self) -> List[str]:
 """Получает порядок глав in правильной последовательности"""
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
 """Извлекает информацию о главе из имени файла"""
 chapter_num = filename.split('_')[0]
 chapter_name = filename.replace('.md', '').replace(f"{chapter_num}_", "").replace('_', ' ').title()

 # Специальные названия for некоторых глав
 special_names = {
 "01_installation": "installation and configuration",
 "02_basic_usage": "Базовое использование",
 "03_advanced_configuration": "Продвинутая configuration",
 "04_risk_Analysis": "Анализ рисков",
 "05_low_risk_systems": "Низкорисковые системы",
 "06_metrics": "Метрики and оценка",
 "07_validation": "Валидация моделей",
 "08_production": "Продакшен развертывание",
 "09_retraining": "Переобучение моделей",
 "10_best_practices": "Лучшие практики",
 "11_apple_silicon_optimization": "Apple Silicon оптимизация",
 "12_examples": "Практические examples",
 "13_simple_production_example": "Простой продакшен example",
 "14_advanced_production_example": "Продвинутый продакшен",
 "15_theory_and_fundamentals": "Теория and основы",
 "16_Troubleshooting": "Troubleshooting",
 "17_interpretability_and_explainability": "Интерпретируемость",
 "18_advanced_topics": "Продвинутые темы",
 "19_ethics_and_responsible_ai": "Этика and ответственный AI",
 "20_case_studies": "Кейс-стади",
 "21_wave2_indicator_Analysis": "Wave2 индикатор анализ",
 "22_schr_levels_Analysis": "SCHR уровни анализ",
 "23_schr_short3_Analysis": "SCHR short3 анализ",
 "24_super_system_ultimate": "Супер система Ultimate",
 "25_reading_guide": "guide on чтению",
 "26_probability_usage_guide": "guide on вероятностям",
 "27_trading_bot_Monitoring": "Monitoring торгового бота",
 "28_feature_generation_advanced": "Продвинутая генерация признаков",
 "29_backtesting_methods": "Методы бэктестинга",
 "30_walk_forward_Analysis": "Walk-forward анализ",
 "31_monte_carlo_simulations": "Монте-Карло симуляции",
 "32_Portfolio_Management": "Management портфелем",
 "33_llm_parallel_computing_setup": "configuration параллельных вычислений"
 }

 return {
 'number': chapter_num,
 'name': special_names.get(filename.replace('.md', ''), chapter_name),
 'filename': filename
 }

 def process_markdown_file(self, filepath: Path) -> Dict[str, Any]:
 """Обрабатывает один Markdown файл"""
 try:
 with open(filepath, 'r', encoding='utf-8') as f:
 content = f.read()

 # Извлекаем метаdata
 title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
 author_match = re.search(r'\*\*Author:\*\* (.+)$', content, re.MULTILINE)
 date_match = re.search(r'\*\*Дата:\*\* (.+)$', content, re.MULTILINE)

 # Обрабатываем изображения
 content = self.process_images(content)

 # Конвертируем in HTML
 html_content = self.md.convert(content)

 # Сбрасываем состояние markdown for следующего файла
 self.md.reset()

 return {
 'title': title_match.group(1) if title_match else filepath.stem,
 'author': author_match.group(1) if author_match else 'Shcherbyna Rostyslav',
 'date': date_match.group(1) if date_match else '2024',
 'content': html_content,
 'filename': filepath.name
 }

 except Exception as e:
 print(f"Ошибка обработки файла {filepath}: {e}")
 return None

 def process_images(self, content: str) -> str:
 """Обрабатывает изображения in контенте"""
 # Заменяем относительные пути on абсолютные
 content = re.sub(
 r'<img src="images/',
 '<img src="images/',
 content
 )

 # Добавляем стили for изображений
 content = re.sub(
 r'<img src="([^"]+)" alt="([^"]*)"',
 r'<img src="\1" alt="\2" style="max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"',
 content
 )

 return content

 def generate_toc(self) -> str:
 """Генерирует оглавление"""
 toc_html = '<div class="toc">\n'
 toc_html += '<h2>📚 Содержание (33 главы)</h2>\n'
 toc_html += '<div class="toc-grid">\n'

 for i, chapter in enumerate(self.chapters, 1):
 if chapter:
 chapter_info = self.get_chapter_info(chapter['filename'])
 toc_html += f'''
 <div class="toc-item">
 <h3>{i}. {chapter_info['name']}</h3>
 <p>{self.get_chapter_description(chapter_info['name'])}</p>
 </div>
 '''

 toc_html += '</div>\n</div>\n'
 return toc_html

 def get_chapter_description(self, chapter_name: str) -> str:
 """Возвращает description главы"""
 descriptions = {
 "installation and configuration": "Пошаговая installation, системные требования, configuration",
 "Базовое использование": "Основы работы with TabularPredictor, обучение моделей",
 "Продвинутая configuration": "Гиперпараметры, ансамбли, валидация, feature engineering",
 "Анализ рисков": "Technical, бизнес and операционные риски ML-систем",
 "Низкорисковые системы": "create надежных and устойчивых ML-систем",
 "Метрики and оценка": "Классификация, регрессия, временные ряды, финансовые метрики",
 "Валидация моделей": "Cross-validation, временные ряды, walk-forward анализ",
 "Продакшен развертывание": "API серверы, Docker, Kubernetes, Monitoring",
 "Переобучение моделей": "Автоматическое переобучение, Monitoring дрейфа",
 "Лучшие практики": "Подготовка данных, выбор метрик, оптимизация",
 "Apple Silicon оптимизация": "M1/M2/M3, MLX, Metal Performance Shaders",
 "Практические examples": "Банк, недвижимость, временные ряды, классификация",
 "Простой продакшен example": "from идеи to продакшен деплоя за 8 шагов",
 "Продвинутый продакшен": "МикроServices, масштабирование, Monitoring",
 "Теория and основы": "Математические основы, алгоритмы, принципы",
 "Troubleshooting": "Решение проблем, отладка, оптимизация",
 "Интерпретируемость": "Объяснимость моделей, SHAP, LIME",
 "Продвинутые темы": "Ансамбли, feature engineering, оптимизация",
 "Этика and ответственный AI": "Справедливость, прозрачность, безопасность",
 "Кейс-стади": "Реальные проекты and их решения",
 "Wave2 индикатор анализ": "Технический анализ and индикаторы",
 "SCHR уровни анализ": "Анализ уровней поддержки and сопротивления",
 "SCHR short3 анализ": "Краткосрочный анализ торговых сигналов",
 "Супер система Ultimate": "Комплексная торговая система",
 "guide on чтению": "Как эффективно изучать материал",
 "guide on вероятностям": "Working with вероятностями in ML",
 "Monitoring торгового бота": "Отслеживание and Management ботом",
 "Продвинутая генерация признаков": "Feature engineering for сложных задач",
 "Методы бэктестинга": "Тестирование стратегий on исторических данных",
 "Walk-forward анализ": "Скользящее тестирование стратегий",
 "Монте-Карло симуляции": "Стохастическое моделирование рисков",
 "Management портфелем": "Оптимизация and диверсификация портфеля",
 "configuration параллельных вычислений": "LLM and параллельные вычисления"
 }
 return descriptions.get(chapter_name, "Detailed description темы")

 def generate_html_template(self) -> str:
 """Генерирует HTML шаблон in стиле Python_Formatting_Example.html"""
 return '''<!DOCTYPE html>
<html lang="ru">
<head>
 <meta charset="UTF-8">
 <meta name="Viewport" content="width=device-width, initial-scale=1.0">
 <title>AutoML Gluon - Complete guide (33 главы)</title>
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

 /* Улучшенные стили for Python кода */
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

 /* Цветовое выделение for Python синтаксиса */
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
 <p>Complete guide on автоматизированному машинному обучению</p>
 <p><strong>33 главы</strong> | <strong>Author:</strong> Shcherbyna Rostyslav | <strong>Дата:</strong> 2024</p>
 </div>

 {toc}

 {content}
 </div>

 <a href="#" class="back-to-top">↑ Наверх</a>

 <script>
 // Инициализация Prism.js for синтаксического выделения
 if (typeof Prism !== 'undefined') {
 Prism.highlightall();
 }

 // Плавная прокрутка к якорям
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

 // Кнопка "Наверх"
 const backToTop = document.querySelector('.back-to-top');
 backToTop.addEventListener('click', function(e) {
 e.preventDefault();
 window.scrollTo({
 top: 0,
 behavior: 'smooth'
 });
 });

 // Показ/скрытие кнопки "Наверх"
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
 """Конвертирует все главы"""
 print("🔄 Начинаем конвертацию глав...")

 chapter_order = self.get_chapter_order()

 for filename in chapter_order:
 filepath = self.source_dir / filename
 if filepath.exists():
 print(f"📖 Обрабатываем: {filename}")
 chapter_data = self.process_markdown_file(filepath)
 if chapter_data:
 self.chapters.append(chapter_data)
 else:
 print(f"⚠️ File not found: {filename}")

 print(f"✅ ОбWorkingно {len(self.chapters)} глав")

 def generate_html(self) -> str:
 """Генерирует полный HTML мануал"""
 print("🔨 Генерируем HTML мануал...")

 # Генерируем оглавление
 toc_html = self.generate_toc()

 # Генерируем контент глав
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

 # Собираем полный HTML
 html_template = self.generate_html_template()
 full_html = html_template.format(
 toc=toc_html,
 content=content_html
 )

 return full_html

 def save_html(self, html_content: str) -> None:
 """Сохраняет HTML in файл"""
 output_file = self.output_dir / "AutoML_Gluon_Complete_Manual.html"

 with open(output_file, 'w', encoding='utf-8') as f:
 f.write(html_content)

 print(f"💾 HTML мануал сохранен: {output_file}")

 def run(self) -> None:
 """Launchает полный процесс конвертации"""
 print("🚀 Launch конвертера Markdown → HTML")
 print(f"📁 Исходная директория: {self.source_dir}")
 print(f"📁 Выходная директория: {self.output_dir}")

 # Конвертируем главы
 self.convert_chapters()

 # Генерируем HTML
 html_content = self.generate_html()

 # Сохраняем HTML
 self.save_html(html_content)

 print("🎉 Конвертация завершена успешно!")

def main():
 """Главная function"""
 converter = AutoMLGluonHTMLConverter()
 converter.run()

if __name__ == "__main__":
 main()
