#!/usr/bin/env python3
"""
Создание PDF с помощью WeasyPrint
Простой и надежный способ создания PDF из HTML

Автор: Shcherbyna Rostyslav
Дата: 2024
"""

import os
from pathlib import Path
from weasyprint import HTML, CSS

def create_pdf_with_weasyprint():
    """Создание PDF с помощью WeasyPrint"""
    
    # Пути к файлам
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    html_file = docs_dir / "AutoML_Gluon_Complete_Manual_Enhanced.html"
    css_file = script_dir / "style.css"
    output_pdf = docs_dir / "AutoML_Gluon_Complete_Manual.pdf"
    
    print("=== Создание PDF с WeasyPrint ===")
    print(f"HTML файл: {html_file}")
    print(f"CSS файл: {css_file}")
    print(f"Выходной PDF: {output_pdf}")
    
    if not html_file.exists():
        print(f"✗ HTML файл не найден: {html_file}")
        return False
    
    try:
        # Читаем HTML
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Читаем CSS если существует
        css_content = None
        if css_file.exists():
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
        
        # Создаем PDF
        print("Создание PDF...")
        html_doc = HTML(string=html_content)
        
        if css_content:
            css_doc = CSS(string=css_content)
            html_doc.write_pdf(str(output_pdf), stylesheets=[css_doc])
        else:
            html_doc.write_pdf(str(output_pdf))
        
        print(f"✓ PDF создан успешно: {output_pdf}")
        print(f"Размер файла: {output_pdf.stat().st_size / 1024 / 1024:.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"✗ Ошибка при создании PDF: {e}")
        return False

def main():
    print("=== Создание PDF учебника AutoML Gluon с WeasyPrint ===")
    print("Автор: Shcherbyna Rostyslav")
    print("Дата: 2024")
    
    success = create_pdf_with_weasyprint()
    
    if success:
        print("\n🎉 PDF учебник успешно создан!")
        print("Файл готов к использованию.")
    else:
        print("\n⚠️  Не удалось создать PDF автоматически.")
        print("Попробуйте открыть HTML файл в браузере и сохранить как PDF.")

if __name__ == "__main__":
    main()
