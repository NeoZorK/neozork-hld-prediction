#!/usr/bin/env python3
# copilot_fix.py - Простой скрипт для запуска исправленного MCP сервера на порту 9999

import sys
import os
import socket
import subprocess
import time

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
        process = subprocess.Popen(
            [sys.executable, server_path],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        print(f"Сервер запущен на порту {port}, PID: {process.pid}")
        return process
    except Exception as e:
        print(f"Ошибка при запуске сервера: {e}")
        return None

def main():
    # Порты, на которых GitHub Copilot может искать MCP сервер
    ports = [9999, 5000]

    processes = []

    print("Запуск MCP серверов для GitHub Copilot...")

    for port in ports:
        if check_port_available(port):
            process = start_server(port)
            if process:
                processes.append((port, process))
                # Даем серверу время на запуск
                time.sleep(1)
        else:
            print(f"Порт {port} уже используется!")

    if not processes:
        print("Не удалось запустить ни один сервер!")
        return

    print(f"Запущено {len(processes)} серверов.")
    print("Нажмите Ctrl+C для завершения.")

    try:
        # Обрабатываем вывод серверов в реальном времени
        while True:
            for port, process in processes:
                # Читаем stdout без блокировки
                output = process.stdout.readline()
                if output:
                    print(f"[Server:{port}] {output.strip()}")

                # Читаем stderr без блокировки
                error = process.stderr.readline()
                if error:
                    print(f"[Server:{port} ERROR] {error.strip()}")

                # Проверяем, не завершился ли процесс
                if process.poll() is not None:
                    print(f"Сервер на порту {port} завершил работу с кодом {process.returncode}")
                    # Удаляем процесс из списка
                    processes.remove((port, process))

            # Если все серверы завершили работу, выходим из цикла
            if not processes:
                print("Все серверы завершили работу!")
                break

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nПолучен сигнал завершения. Останавливаем серверы...")
        for port, process in processes:
            try:
                process.terminate()
                print(f"Сервер на порту {port} успешно остановлен.")
            except:
                print(f"Не удалось корректно остановить сервер на порту {port}.")

    print("Работа завершена.")

if __name__ == "__main__":
    main()
