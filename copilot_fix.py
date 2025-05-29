#!/usr/bin/env python3
# copilot_fix.py - Простой скрипт для запуска исправленного MCP сервера на порту 9999

import sys
import os
import socket
import subprocess
import time
import signal

def check_port_available(port):
    """Проверяет, свободен ли указанный порт"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("127.0.0.1", port))
        result = True
    except:
        pass
    finally:
        sock.close()
    return result

def start_server(port):
    """Запускает сервер на указанном порту"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(script_dir, "mcp_server.py")

    # Проверяем наличие файла
    if not os.path.exists(server_path):
        print(f"Ошибка: файл {server_path} не найден!")
        return None

    # Запускаем сервер с указанием порта через переменную окружения
    env = os.environ.copy()
    env["MCP_PORT"] = str(port)

    try:
        # Запускаем процесс без перенаправления вывода, чтобы он не завершался
        process = subprocess.Popen(
            [sys.executable, server_path],
            env=env,
            # Без перенаправления stdout и stderr
            # Используем текущий терминал
        )
        print(f"Сервер запущен на порту {port}, PID: {process.pid}")
        return process
    except Exception as e:
        print(f"Ошибка при запуске сервера: {e}")
        return None

def main():
    # Порты, на которых GitHub Copilot может искать MCP сервер
    ports = [9999, 5000, 8765]

    processes = []

    print("Запуск MCP серверов для GitHub Copilot...")

    # Обработчик сигнала для корректного завершения
    def signal_handler(sig, frame):
        print("\nПолучен сигнал завершения. Останавливаем серверы...")
        for port, process in processes:
            try:
                process.terminate()
                print(f"Сервер на порту {port} успешно остановлен.")
            except:
                print(f"Не удалось корректно остановить сервер на порту {port}.")
        sys.exit(0)

    # Регистрируем обработчик сигнала
    signal.signal(signal.SIGINT, signal_handler)

    for port in ports:
        if check_port_available(port):
            process = start_server(port)
            if process:
                processes.append((port, process))
                # Даем серверу время на запуск
                time.sleep(2)
                print(f"Проверка сервера на порту {port}...")
                if process.poll() is not None:
                    print(f"Сервер на порту {port} завершился с кодом {process.returncode}")
                else:
                    print(f"Сервер на порту {port} успешно запущен и работает")
        else:
            print(f"Порт {port} уже используется!")

    if not processes:
        print("Не удалось запустить ни один сервер!")
        return

    print(f"Запущено {len(processes)} серверов.")
    print("Нажмите Ctrl+C для завершения.")

    # Ожидаем, пока все процессы не завершятся
    try:
        while True:
            # Проверяем статус процессов
            for i, (port, process) in enumerate(processes[:]):
                if process.poll() is not None:
                    print(f"Сервер на порту {port} завершил работу с кодом {process.returncode}")
                    # Удаляем завершившийся процесс из списка
                    processes.pop(i)
                    # Пытаемся перезапустить сервер
                    print(f"Попытка перезапуска сервера на порту {port}...")
                    if check_port_available(port):
                        new_process = start_server(port)
                        if new_process:
                            processes.append((port, new_process))
                            print(f"Сервер на порту {port} успешно перезапущен")

            # Если все серверы завершили работу, выходим из цикла
            if not processes:
                print("Все серверы завершили работу!")
                break

            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

    print("Работа завершена.")

if __name__ == "__main__":
    main()
