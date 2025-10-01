#!/usr/bin/env python3
"""
Создание PDF с помощью Python библиотек
Альтернативный способ создания PDF

Автор: NeoZorK (Shcherbyna Rostyslav)
Дата: 2025
"""

import os
import subprocess
import sys
from pathlib import Path

def install_pdfkit():
    """Установка pdfkit если не установлен"""
    try:
        import pdfkit
        return True
    except ImportError:
        print("📦 Устанавливаем pdfkit...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pdfkit'], check=True)
        try:
            import pdfkit
            return True
        except ImportError:
            print("✗ Не удалось установить pdfkit")
            return False

def create_pdf_with_pdfkit():
    """Создание PDF с помощью pdfkit"""
    
    print("=== Создание PDF с pdfkit ===")
    
    if not install_pdfkit():
        return False
    
    import pdfkit
    
    # Определение путей
    project_root = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    html_file = docs_dir / "AutoML_Gluon_Complete_Manual_Enhanced.html"
    pdf_file = docs_dir / "AutoML_Gluon_Complete_Manual.pdf"
    
    print(f"HTML файл: {html_file}")
    print(f"PDF файл: {pdf_file}")
    
    if not html_file.exists():
        print(f"✗ HTML файл не найден: {html_file}")
        return False
    
    # Настройки для PDF
    options = {
        'page-size': 'A4',
        'margin-top': '1in',
        'margin-right': '1in',
        'margin-bottom': '1in',
        'margin-left': '1in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,
        'print-media-type': None,
        'disable-smart-shrinking': None
    }
    
    try:
        print("🔄 Создание PDF...")
        pdfkit.from_file(str(html_file), str(pdf_file), options=options)
        print("✅ PDF создан успешно!")
        print(f"📄 Файл: {pdf_file}")
        return True
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False

def create_pdf_with_reportlab():
    """Создание PDF с помощью ReportLab"""
    
    print("\n=== Создание PDF с ReportLab ===")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
    except ImportError:
        print("📦 Устанавливаем ReportLab...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'reportlab'], check=True)
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
        except ImportError:
            print("✗ Не удалось установить ReportLab")
            return False
    
    # Определение путей
    project_root = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    pdf_file = docs_dir / "AutoML_Gluon_Complete_Manual_ReportLab.pdf"
    
    print(f"PDF файл: {pdf_file}")
    
    try:
        # Создаем простой PDF
        doc = SimpleDocTemplate(str(pdf_file), pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Заголовок
        title = Paragraph("AutoML Gluon - Полное руководство пользователя", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Информация об авторе
        author_info = Paragraph(
            "<b>Автор:</b> NeoZorK (Shcherbyna Rostyslav)<br/>"
            "<b>Дата:</b> 2025<br/>"
            "<b>Местоположение:</b> Ukraine, Zaporizhzhya<br/>"
            "<b>Версия:</b> 1.0",
            styles['Normal']
        )
        story.append(author_info)
        story.append(Spacer(1, 20))
        
        # Содержание
        toc = Paragraph(
            "<b>Содержание:</b><br/>"
            "1. Введение и установка<br/>"
            "2. Базовое использование<br/>"
            "3. Продвинутая конфигурация<br/>"
            "4. Метрики и оценка качества<br/>"
            "5. Валидация моделей<br/>"
            "6. Продакшен и деплой<br/>"
            "7. Переобучение моделей<br/>"
            "8. Лучшие практики<br/>"
            "9. Примеры использования<br/>"
            "10. Troubleshooting<br/>"
            "11. Оптимизация для Apple Silicon<br/>"
            "12. Простой пример продакшена<br/>"
            "13. Сложный пример продакшена<br/>"
            "14. Теория и основы AutoML<br/>"
            "15. Интерпретируемость и объяснимость<br/>"
            "16. Продвинутые темы<br/>"
            "17. Этика и ответственный AI<br/>"
            "18. Кейс-стади<br/>"
            "19. WAVE2 Индикатор - Полный анализ<br/>"
            "20. SCHR Levels - Анализ и ML-модель<br/>"
            "21. SCHR SHORT3 - Краткосрочная торговля<br/>"
            "22. Супер-система: Объединение всех индикаторов<br/>"
            "23. Руководство по изучению учебника<br/>"
            "24. Правильное использование вероятностей<br/>"
            "25. Мониторинг торгового бота - Лучшие практики",
            styles['Normal']
        )
        story.append(toc)
        
        # Создаем PDF
        doc.build(story)
        print("✅ PDF создан с ReportLab!")
        print(f"📄 Файл: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False

def main():
    """Основная функция"""
    
    print("🚀 Создание PDF руководства AutoML Gluon")
    print("Автор: NeoZorK (Shcherbyna Rostyslav)")
    print("Дата: 2025")
    print("Местоположение: Ukraine, Zaporizhzhya")
    
    # Пробуем разные способы
    success = False
    
    # Способ 1: pdfkit
    if create_pdf_with_pdfkit():
        success = True
    
    # Способ 2: ReportLab (простой PDF)
    if create_pdf_with_reportlab():
        success = True
    
    if success:
        print("\n🎉 PDF создан успешно!")
        print("📄 Проверьте папку docs/automl/gluon/")
    else:
        print("\n⚠️  Автоматическое создание PDF не удалось")
        print("📋 Используйте ручной способ через браузер:")
        print("1. Откройте AutoML_Gluon_Complete_Manual_Enhanced.html в браузере")
        print("2. Нажмите Cmd+P (Mac) или Ctrl+P (Windows/Linux)")
        print("3. Выберите 'Сохранить как PDF'")
        print("4. Настройте параметры и сохраните")

if __name__ == "__main__":
    main()
