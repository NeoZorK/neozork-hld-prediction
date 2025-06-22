#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для запуска и тестирования Cursor MCP Server
"""

import sys
import json
import time
import subprocess
import signal
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Добавляем корневую директорию проекта в путь
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cursor_mcp_server import CursorMCPServer

class CursorMCPServerRunner:
    """Класс для запуска и тестирования MCP сервера"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.server_process: Optional[subprocess.Popen] = None
        self.server: Optional[CursorMCPServer] = None
        
    def start_server(self, mode: str = "test") -> bool:
        """Запуск сервера в указанном режиме"""
        try:
            if mode == "test":
                # Запуск в тестовом режиме (без STDIO)
                self.server = CursorMCPServer(project_root=self.project_root)
                print("✅ MCP сервер запущен в тестовом режиме")
                return True
            elif mode == "stdio":
                # Запуск в STDIO режиме для Cursor IDE
                cmd = [sys.executable, "cursor_mcp_server.py"]
                self.server_process = subprocess.Popen(
                    cmd,
                    cwd=self.project_root,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                print("✅ MCP сервер запущен в STDIO режиме")
                return True
            else:
                print(f"❌ Неизвестный режим: {mode}")
                return False
        except Exception as e:
            print(f"❌ Ошибка запуска сервера: {e}")
            return False
    
    def stop_server(self):
        """Остановка сервера"""
        try:
            if self.server_process:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                print("✅ Сервер остановлен")
            elif self.server:
                self.server.running = False
                print("✅ Сервер остановлен")
        except Exception as e:
            print(f"❌ Ошибка остановки сервера: {e}")
    
    def test_server_functionality(self) -> Dict[str, Any]:
        """Тестирование функциональности сервера"""
        if not self.server:
            return {"error": "Сервер не запущен"}
        
        results = {}
        
        try:
            # Тест инициализации
            print("🧪 Тестирование инициализации...")
            init_result = self.server._handle_initialize(None, {})
            results["initialize"] = {
                "success": True,
                "capabilities": init_result.get("capabilities", {}),
                "serverInfo": init_result.get("serverInfo", {})
            }
            
            # Тест информации о проекте
            print("🧪 Тестирование информации о проекте...")
            project_info = self.server._handle_project_info(None, {})
            results["project_info"] = {
                "success": True,
                "data": project_info
            }
            
            # Тест финансовых данных
            print("🧪 Тестирование финансовых данных...")
            financial_data = self.server._handle_financial_data(None, {})
            results["financial_data"] = {
                "success": True,
                "data": financial_data
            }
            
            # Тест индикаторов
            print("🧪 Тестирование индикаторов...")
            indicators = self.server._handle_indicators(None, {})
            results["indicators"] = {
                "success": True,
                "data": indicators
            }
            
            # Тест автодополнения
            print("🧪 Тестирование автодополнения...")
            completion_params = {
                "textDocument": {"uri": "file://test.py"},
                "position": {"line": 0, "character": 0}
            }
            completion_result = self.server._handle_completion(None, completion_params)
            results["completion"] = {
                "success": True,
                "items_count": len(completion_result.get("items", [])),
                "is_incomplete": completion_result.get("isIncomplete", False)
            }
            
            # Тест поиска кода
            print("🧪 Тестирование поиска кода...")
            search_result = self.server._handle_code_search(None, {"query": "calculate"})
            results["code_search"] = {
                "success": True,
                "data": search_result
            }
            
            # Тест сниппетов
            print("🧪 Тестирование сниппетов...")
            snippets = self.server._handle_snippets(None, {})
            results["snippets"] = {
                "success": True,
                "count": len(snippets)
            }
            
            # Тест анализа проекта
            print("🧪 Тестирование анализа проекта...")
            analysis = self.server._handle_analysis(None, {})
            results["analysis"] = {
                "success": True,
                "data": analysis
            }
            
        except Exception as e:
            results["error"] = str(e)
            print(f"❌ Ошибка тестирования: {e}")
        
        return results
    
    def send_test_message(self, method: str, params: Dict = None) -> Dict[str, Any]:
        """Отправка тестового сообщения серверу"""
        if not self.server_process:
            return {"error": "Сервер не запущен в STDIO режиме"}
        
        try:
            message = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params or {}
            }
            
            message_str = json.dumps(message)
            content_length = len(message_str)
            
            # Формируем сообщение в формате LSP
            lsp_message = f"Content-Length: {content_length}\r\n\r\n{message_str}"
            
            # Отправляем сообщение
            self.server_process.stdin.write(lsp_message)
            self.server_process.stdin.flush()
            
            # Читаем ответ
            response = self.server_process.stdout.readline()
            if response.startswith("Content-Length:"):
                content_length = int(response.split(":")[1].strip())
                self.server_process.stdout.readline()  # Пустая строка
                response_body = self.server_process.stdout.read(content_length)
                return json.loads(response_body)
            else:
                return {"error": "Неверный формат ответа"}
                
        except Exception as e:
            return {"error": f"Ошибка отправки сообщения: {e}"}
    
    def run_performance_test(self) -> Dict[str, Any]:
        """Запуск теста производительности"""
        if not self.server:
            return {"error": "Сервер не запущен"}
        
        results = {}
        
        try:
            # Тест времени инициализации
            start_time = time.time()
            self.server._handle_initialize(None, {})
            init_time = time.time() - start_time
            results["initialization_time"] = init_time
            
            # Тест времени автодополнения
            start_time = time.time()
            for _ in range(10):
                self.server._handle_completion(None, {
                    "textDocument": {"uri": "file://test.py"},
                    "position": {"line": 0, "character": 0}
                })
            completion_time = (time.time() - start_time) / 10
            results["completion_time"] = completion_time
            
            # Тест времени поиска
            start_time = time.time()
            for _ in range(10):
                self.server._handle_code_search(None, {"query": "calculate"})
            search_time = (time.time() - start_time) / 10
            results["search_time"] = search_time
            
            # Статистика проекта
            project_stats = self.server._handle_analysis(None, {})
            results["project_stats"] = project_stats
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def generate_report(self, test_results: Dict[str, Any], performance_results: Dict[str, Any]) -> str:
        """Генерация отчета о тестировании"""
        report = []
        report.append("# Отчет о тестировании Cursor MCP Server")
        report.append("")
        
        # Результаты функционального тестирования
        report.append("## Функциональное тестирование")
        report.append("")
        
        for test_name, result in test_results.items():
            if test_name == "error":
                report.append(f"❌ **Ошибка**: {result}")
            else:
                status = "✅" if result.get("success", False) else "❌"
                report.append(f"{status} **{test_name}**: {'Успешно' if result.get('success', False) else 'Ошибка'}")
        
        report.append("")
        
        # Результаты производительности
        report.append("## Тест производительности")
        report.append("")
        
        if "error" in performance_results:
            report.append(f"❌ **Ошибка**: {performance_results['error']}")
        else:
            report.append(f"⏱️ **Время инициализации**: {performance_results.get('initialization_time', 0):.3f}с")
            report.append(f"⚡ **Время автодополнения**: {performance_results.get('completion_time', 0):.3f}с")
            report.append(f"🔍 **Время поиска**: {performance_results.get('search_time', 0):.3f}с")
            
            if "project_stats" in performance_results:
                stats = performance_results["project_stats"]
                report.append("")
                report.append("### Статистика проекта")
                report.append(f"- **Всего файлов**: {stats.get('project_stats', {}).get('total_files', 0)}")
                report.append(f"- **Python файлов**: {stats.get('project_stats', {}).get('python_files', 0)}")
                report.append(f"- **Функций**: {stats.get('code_analysis', {}).get('functions', 0)}")
                report.append(f"- **Классов**: {stats.get('code_analysis', {}).get('classes', 0)}")
                report.append(f"- **Индикаторов**: {stats.get('code_analysis', {}).get('indicators', 0)}")
        
        return "\n".join(report)

def main():
    """Главная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Запуск и тестирование Cursor MCP Server")
    parser.add_argument("--mode", choices=["test", "stdio", "both"], default="test",
                       help="Режим запуска сервера")
    parser.add_argument("--test", action="store_true", help="Запустить тесты")
    parser.add_argument("--performance", action="store_true", help="Запустить тест производительности")
    parser.add_argument("--report", action="store_true", help="Сгенерировать отчет")
    parser.add_argument("--config", type=str, help="Путь к конфигурационному файлу")
    
    args = parser.parse_args()
    
    runner = CursorMCPServerRunner()
    
    try:
        # Запуск сервера
        if args.mode in ["test", "both"]:
            if not runner.start_server("test"):
                sys.exit(1)
        
        if args.mode in ["stdio", "both"]:
            if not runner.start_server("stdio"):
                sys.exit(1)
        
        # Выполнение тестов
        if args.test:
            print("🧪 Запуск функциональных тестов...")
            test_results = runner.test_server_functionality()
            
            if args.performance:
                print("⚡ Запуск теста производительности...")
                performance_results = runner.run_performance_test()
            else:
                performance_results = {}
            
            if args.report:
                report = runner.generate_report(test_results, performance_results)
                print("\n" + "="*50)
                print(report)
                print("="*50)
                
                # Сохранение отчета в файл
                report_file = Path("logs/mcp_test_report.md")
                report_file.parent.mkdir(exist_ok=True)
                report_file.write_text(report, encoding='utf-8')
                print(f"📄 Отчет сохранен в {report_file}")
            else:
                # Вывод кратких результатов
                print("\n📊 Краткие результаты:")
                for test_name, result in test_results.items():
                    if test_name != "error":
                        status = "✅" if result.get("success", False) else "❌"
                        print(f"  {status} {test_name}")
        
        # Интерактивный режим
        if not args.test and args.mode == "test":
            print("\n🎯 Сервер запущен в тестовом режиме")
            print("Нажмите Ctrl+C для остановки...")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
    
    except KeyboardInterrupt:
        print("\n⏹️ Получен сигнал остановки...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        runner.stop_server()

if __name__ == "__main__":
    main() 