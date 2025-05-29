#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для индексации и поиска элементов кода в проекте
"""

import ast
import traceback


class CodeIndexer:
    """Класс для индексации и поиска элементов кода в проекте"""

    def __init__(self, logger):
        self.logger = logger

        # Структура для хранения индексированного кода
        self.code_index = {
            'functions': {},  # имя_функции -> [файлы, где она определена]
            'classes': {},    # имя_класса -> [файлы, где он определен]
            'variables': {},  # имя_переменной -> [файлы, где она определена/используется]
            'imports': {},    # имя_импорта -> [файлы, где он используется]
            'docstrings': {}  # (имя, тип) -> docstring
        }

        self.logger.info("Инициализирован индексатор кода")

    def index_python_file(self, file_path, content):
        """Индексирует содержимое Python файла"""
        try:
            # Парсим содержимое файла в AST
            tree = ast.parse(content)

            # Извлекаем имена и типы элементов кода
            for node in ast.walk(tree):
                # Индексируем функции
                if isinstance(node, ast.FunctionDef):
                    self._index_function(node, file_path)

                # Индексируем классы
                elif isinstance(node, ast.ClassDef):
                    self._index_class(node, file_path)

                # Индексируем импорты
                elif isinstance(node, ast.Import):
                    self._index_import(node, file_path)

                # Индексируем from-импорты
                elif isinstance(node, ast.ImportFrom):
                    self._index_import_from(node, file_path)

                # Индексируем переменные
                elif isinstance(node, ast.Assign):
                    self._index_variable(node, file_path)

            self.logger.debug(f"Успешно проиндексирован файл {file_path}")

        except Exception as e:
            self.logger.error(f"Ошибка при индексации файла {file_path}: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _index_function(self, node, file_path):
        """Индексирует функцию"""
        func_name = node.name

        # Пропускаем "приватные" функции (начинающиеся с _)
        if func_name.startswith('_') and not func_name.startswith('__'):
            return

        # Добавляем информацию о функции в индекс
        if func_name not in self.code_index['functions']:
            self.code_index['functions'][func_name] = []

        if file_path not in self.code_index['functions'][func_name]:
            self.code_index['functions'][func_name].append(file_path)

        # Извлекаем и сохраняем docstring
        docstring = ast.get_docstring(node)
        if docstring:
            self.code_index['docstrings'][(func_name, 'function')] = docstring

    def _index_class(self, node, file_path):
        """Индексирует класс"""
        class_name = node.name

        # Пропускаем "приватные" классы (начинающиеся с _)
        if class_name.startswith('_') and not class_name.startswith('__'):
            return

        # Добавляем информацию о классе в индекс
        if class_name not in self.code_index['classes']:
            self.code_index['classes'][class_name] = []

        if file_path not in self.code_index['classes'][class_name]:
            self.code_index['classes'][class_name].append(file_path)

        # Извлекаем и сохраняем docstring
        docstring = ast.get_docstring(node)
        if docstring:
            self.code_index['docstrings'][(class_name, 'class')] = docstring

    def _index_import(self, node, file_path):
        """Индексирует импорт"""
        for name in node.names:
            import_name = name.name
            alias = name.asname if name.asname else import_name

            # Добавляем информацию об импорте в индекс
            if import_name not in self.code_index['imports']:
                self.code_index['imports'][import_name] = []

            if file_path not in self.code_index['imports'][import_name]:
                self.code_index['imports'][import_name].append(file_path)

            # Добавляем информацию об алиасе, если он есть
            if alias != import_name:
                if alias not in self.code_index['imports']:
                    self.code_index['imports'][alias] = []

                if file_path not in self.code_index['imports'][alias]:
                    self.code_index['imports'][alias].append(file_path)

    def _index_import_from(self, node, file_path):
        """Индексирует from-импорт"""
        module = node.module
        for name in node.names:
            import_name = f"{module}.{name.name}" if module else name.name
            alias = name.asname if name.asname else name.name

            # Добавляем информацию об импорте в индекс
            if import_name not in self.code_index['imports']:
                self.code_index['imports'][import_name] = []

            if file_path not in self.code_index['imports'][import_name]:
                self.code_index['imports'][import_name].append(file_path)

            # Добавляем информацию об алиасе
            if alias != name.name:
                if alias not in self.code_index['imports']:
                    self.code_index['imports'][alias] = []

                if file_path not in self.code_index['imports'][alias]:
                    self.code_index['imports'][alias].append(file_path)

    def _index_variable(self, node, file_path):
        """Индексирует переменную"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id

                # Пропускаем "приватные" переменные (начинающиеся с _)
                if var_name.startswith('_') and not var_name.startswith('__'):
                    continue

                # Добавляем информацию о переменной в индекс
                if var_name not in self.code_index['variables']:
                    self.code_index['variables'][var_name] = []

                if file_path not in self.code_index['variables'][var_name]:
                    self.code_index['variables'][var_name].append(file_path)

    def get_references(self, name):
        """Получает все ссылки на имя в коде"""
        references = []

        # Ищем ссылки в функциях
        if name in self.code_index['functions']:
            for file_path in self.code_index['functions'][name]:
                references.append({
                    'file': file_path,
                    'type': 'function',
                    'name': name
                })

        # Ищем ссылки в классах
        if name in self.code_index['classes']:
            for file_path in self.code_index['classes'][name]:
                references.append({
                    'file': file_path,
                    'type': 'class',
                    'name': name
                })

        # Ищем ссылки в переменных
        if name in self.code_index['variables']:
            for file_path in self.code_index['variables'][name]:
                references.append({
                    'file': file_path,
                    'type': 'variable',
                    'name': name
                })

        # Ищем ссылки в импортах
        if name in self.code_index['imports']:
            for file_path in self.code_index['imports'][name]:
                references.append({
                    'file': file_path,
                    'type': 'import',
                    'name': name
                })

        return references

    def get_definitions(self, name):
        """Получает определения имени в коде"""
        definitions = []

        # Ищем определения в функциях
        if name in self.code_index['functions']:
            for file_path in self.code_index['functions'][name]:
                definition = {
                    'file': file_path,
                    'type': 'function',
                    'name': name
                }
                # Добавляем docstring, если есть
                if (name, 'function') in self.code_index['docstrings']:
                    definition['docstring'] = self.code_index['docstrings'][(name, 'function')]
                definitions.append(definition)

        # Ищем определения в классах
        if name in self.code_index['classes']:
            for file_path in self.code_index['classes'][name]:
                definition = {
                    'file': file_path,
                    'type': 'class',
                    'name': name
                }
                # Добавляем docstring, если есть
                if (name, 'class') in self.code_index['docstrings']:
                    definition['docstring'] = self.code_index['docstrings'][(name, 'class')]
                definitions.append(definition)

        return definitions
