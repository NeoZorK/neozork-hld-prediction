# PDF Manual Creation System

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Описание

Система для создания PDF учебника AutoML Gluon с рабочими ссылками и навигацией.

## Файлы

### Скрипты
- `create_final_pdf.py` - Основной скрипт создания PDF
- `create_pdf_alternative.py` - Альтернативный подход
- `create_pdf_manual.py` - Базовый скрипт
- `generate_graphics.py` - Генерация графиков и диаграмм

### Ресурсы
- `style.css` - CSS стили для форматирования
- `PDF_CREATION_README.md` - Подробная документация

## Использование

### Создание PDF
```bash
python3 create_final_pdf.py
```

### Генерация графиков
```bash
python3 generate_graphics.py
```

## Структура

```
src/automl/gluon/pdf_manual/
├── README.md
├── create_final_pdf.py
├── create_pdf_alternative.py
├── create_pdf_manual.py
├── generate_graphics.py
├── style.css
└── PDF_CREATION_README.md
```

## Особенности

- Автоматическое создание объединенного Markdown
- Генерация графиков и диаграмм
- Поддержка LaTeX и HTML
- Рабочие ссылки в PDF
- Оптимизация для Apple Silicon
