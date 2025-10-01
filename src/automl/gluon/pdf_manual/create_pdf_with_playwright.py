#!/usr/bin/env python3
"""
Создание PDF с помощью Playwright
Современный и надежный способ создания PDF

Автор: NeoZorK (Shcherbyna Rostyslav)
Дата: 2025
"""

import os
import subprocess
import sys
from pathlib import Path

def install_playwright():
    """Установка Playwright если не установлен"""
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        print("📦 Устанавливаем Playwright...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'playwright'], check=True)
        subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'], check=True)
        try:
            from playwright.sync_api import sync_playwright
            return True
        except ImportError:
            print("✗ Не удалось установить Playwright")
            return False

def create_pdf_with_playwright():
    """Создание PDF с помощью Playwright"""
    
    print("=== Создание PDF с Playwright ===")
    
    if not install_playwright():
        return False
    
    from playwright.sync_api import sync_playwright
    
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
    
    try:
        with sync_playwright() as p:
            # Запускаем браузер
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Загружаем HTML
            print("🔄 Загружаем HTML...")
            page.goto(f"file://{html_file.absolute()}")
            
            # Ждем загрузки
            page.wait_for_load_state('networkidle')
            
            # Создаем PDF
            print("🔄 Создание PDF...")
            page.pdf(
                path=str(pdf_file),
                format='A4',
                margin={
                    'top': '1in',
                    'right': '1in',
                    'bottom': '1in',
                    'left': '1in'
                },
                print_background=True,
                prefer_css_page_size=True
            )
            
            browser.close()
            
        print("✅ PDF создан успешно!")
        print(f"📄 Файл: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False

def create_simple_pdf_with_playwright():
    """Создание простого PDF с Playwright"""
    
    print("\n=== Создание простого PDF с Playwright ===")
    
    if not install_playwright():
        return False
    
    from playwright.sync_api import sync_playwright
    
    # Определение путей
    project_root = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = project_root / "docs" / "automl" / "gluon"
    
    pdf_file = docs_dir / "AutoML_Gluon_Complete_Manual_Simple.pdf"
    
    print(f"PDF файл: {pdf_file}")
    
    try:
        with sync_playwright() as p:
            # Запускаем браузер
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Создаем простой HTML контент
            html_content = """
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>AutoML Gluon - Полное руководство</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    h1 { color: #2c3e50; border-bottom: 3px solid #3498db; }
                    h2 { color: #34495e; margin-top: 30px; }
                    .toc { background: #f8f9fa; padding: 20px; border-radius: 8px; }
                    .section { margin-bottom: 30px; }
                </style>
            </head>
            <body>
                <h1>AutoML Gluon - Полное руководство пользователя</h1>
                <p><strong>Автор:</strong> NeoZorK (Shcherbyna Rostyslav)</p>
                <p><strong>Дата:</strong> 2025</p>
                <p><strong>Местоположение:</strong> Ukraine, Zaporizhzhya</p>
                <p><strong>Версия:</strong> 1.0</p>
                
                <div class="toc">
                    <h2>Содержание</h2>
                    <ol>
                        <li>Введение и установка</li>
                        <li>Базовое использование</li>
                        <li>Продвинутая конфигурация</li>
                        <li>Метрики и оценка качества</li>
                        <li>Валидация моделей</li>
                        <li>Продакшен и деплой</li>
                        <li>Переобучение моделей</li>
                        <li>Лучшие практики</li>
                        <li>Примеры использования</li>
                        <li>Troubleshooting</li>
                        <li>Оптимизация для Apple Silicon</li>
                        <li>Простой пример продакшена</li>
                        <li>Сложный пример продакшена</li>
                        <li>Теория и основы AutoML</li>
                        <li>Интерпретируемость и объяснимость</li>
                        <li>Продвинутые темы</li>
                        <li>Этика и ответственный AI</li>
                        <li>Кейс-стади</li>
                        <li>WAVE2 Индикатор - Полный анализ</li>
                        <li>SCHR Levels - Анализ и ML-модель</li>
                        <li>SCHR SHORT3 - Краткосрочная торговля</li>
                        <li>Супер-система: Объединение всех индикаторов</li>
                        <li>Руководство по изучению учебника</li>
                        <li>Правильное использование вероятностей</li>
                        <li>Мониторинг торгового бота - Лучшие практики</li>
                    </ol>
                </div>
                
                <div class="section">
                    <h2>Введение</h2>
                    <p>Это полное руководство по AutoML Gluon - мощному инструменту для автоматического машинного обучения. Руководство содержит 25 разделов, охватывающих все аспекты работы с AutoML Gluon.</p>
                </div>
                
                <div class="section">
                    <h2>Основные возможности</h2>
                    <ul>
                        <li>Автоматическое обучение моделей</li>
                        <li>Поддержка различных типов данных</li>
                        <li>Встроенная валидация и метрики</li>
                        <li>Оптимизация гиперпараметров</li>
                        <li>Ансамбли моделей</li>
                        <li>Интерпретируемость результатов</li>
                    </ul>
                </div>
                
                <div class="section">
                    <h2>Заключение</h2>
                    <p>Это руководство поможет вам освоить AutoML Gluon и использовать его для решения реальных задач машинного обучения. Все примеры кода и инструкции проверены и готовы к использованию.</p>
                </div>
            </body>
            </html>
            """
            
            # Устанавливаем контент
            page.set_content(html_content)
            
            # Создаем PDF
            print("🔄 Создание простого PDF...")
            page.pdf(
                path=str(pdf_file),
                format='A4',
                margin={
                    'top': '1in',
                    'right': '1in',
                    'bottom': '1in',
                    'left': '1in'
                },
                print_background=True
            )
            
            browser.close()
            
        print("✅ Простой PDF создан успешно!")
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
    
    # Способ 1: Playwright с полным HTML
    if create_pdf_with_playwright():
        success = True
    
    # Способ 2: Playwright с простым HTML
    if create_simple_pdf_with_playwright():
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
