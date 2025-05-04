import subprocess
import sys
import os
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PYTHON = sys.executable
SCRIPT = os.path.join(PROJECT_ROOT, 'run_analysis.py')
LOG_FILE = os.path.join(PROJECT_ROOT, 'test_cli_all_commands.log')

# Все режимы, правила, plot-режимы, edge-cases
rules = [
    'PHLD', 'PV', 'SR', 'Predict_High_Low_Direction', 'Pressure_Vector', 'Support_Resistants'
]
draw_modes = ['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl']

# Базовые команды
commands = [
    [PYTHON, SCRIPT, '-h'],
    [PYTHON, SCRIPT, '--version'],
    [PYTHON, SCRIPT, '--examples'],
    [PYTHON, SCRIPT, 'demo'],
]
# demo + все правила и plot
for rule in rules:
    commands.append([PYTHON, SCRIPT, 'demo', '--rule', rule])
    for draw in draw_modes:
        commands.append([PYTHON, SCRIPT, 'demo', '--rule', rule, '-d', draw])
# csv режимы
csv_file = 'data.csv'  # Можно заменить на существующий файл для реального теста
for rule in rules:
    for draw in draw_modes:
        commands.append([PYTHON, SCRIPT, 'csv', '--csv-file', csv_file, '--point', '0.01', '--rule', rule, '-d', draw])
# yfinance/yf режимы
for mode in ['yf', 'yfinance']:
    for rule in rules:
        for draw in draw_modes:
            commands.append([
                PYTHON, SCRIPT, mode, '--ticker', 'AAPL', '--period', '1mo', '--point', '0.01', '--rule', rule, '-d', draw
            ])
            commands.append([
                PYTHON, SCRIPT, mode, '--ticker', 'AAPL', '--start', '2024-01-01', '--end', '2024-04-01', '--point', '0.01', '--rule', rule, '-d', draw
            ])
# polygon режимы
for rule in rules:
    for draw in draw_modes:
        commands.append([
            PYTHON, SCRIPT, 'polygon', '--ticker', 'AAPL', '--interval', 'D1', '--start', '2024-01-01', '--end', '2024-04-01', '--point', '0.01', '--rule', rule, '-d', draw
        ])
# binance режимы
for rule in rules:
    for draw in draw_modes:
        commands.append([
            PYTHON, SCRIPT, 'binance', '--ticker', 'BTCUSDT', '--interval', 'H1', '--start', '2024-01-01', '--end', '2024-04-01', '--point', '0.01', '--rule', rule, '-d', draw
        ])
# show режимы
show_sources = ['yf', 'yfinance', 'csv', 'polygon', 'binance']
for source in show_sources:
    commands.append([PYTHON, SCRIPT, 'show', source])
    for rule in rules:
        commands.append([PYTHON, SCRIPT, 'show', source, '--show-rule', rule])
    for draw in draw_modes:
        commands.append([PYTHON, SCRIPT, 'show', source, '-d', draw])
    commands.append([PYTHON, SCRIPT, 'show', source, '--show-start', '2024-01-01', '--show-end', '2024-04-01'])
    commands.append([PYTHON, SCRIPT, 'show', source, 'AAPL', '2024'])

# Ошибочные кейсы (ожидаем код возврата != 0)
error_commands = [
    [PYTHON, SCRIPT, 'csv', '--csv-file', csv_file],  # нет --point
    [PYTHON, SCRIPT, 'csv', '--point', '0.01'],       # нет --csv-file
    [PYTHON, SCRIPT, 'yf', '--ticker', 'AAPL'],       # нет period/start/end
    [PYTHON, SCRIPT, 'binance', '--ticker', 'BTCUSDT', '--start', '2024-01-01', '--point', '0.01'], # нет end
    [PYTHON, SCRIPT, 'binance', '--ticker', 'BTCUSDT', '--end', '2024-04-01', '--point', '0.01'],   # нет start
    [PYTHON, SCRIPT, 'binance', '--start', '2024-01-01', '--end', '2024-04-01', '--point', '0.01'], # нет ticker
    [PYTHON, SCRIPT, 'demo', '--rule', 'INVALID_RULE'],
    [PYTHON, SCRIPT, 'invalid_mode'],
]

def run_command(cmd):
    env = os.environ.copy()
    env['MPLBACKEND'] = 'Agg'
    env['NEOZORK_TEST'] = '1'
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return {
        'cmd': cmd,
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    }

def run_all():
    total = len(commands) + len(error_commands)
    failed = 0
    start_time = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor, tqdm(total=total, desc='CLI Smoke Test') as pbar:
        futures = [executor.submit(run_command, cmd) for cmd in commands + error_commands]
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            pbar.update(1)
    # Сохраняем лог
    with open(LOG_FILE, 'w', encoding='utf-8') as log:
        for res in results:
            log.write(f"\n[TEST] {' '.join(str(x) for x in res['cmd'])}\n")
            log.write(f"Return code: {res['returncode']}\n")
            log.write(f"STDOUT: {res['stdout'][:500]}\n")
            log.write(f"STDERR: {res['stderr'][:500]}\n")
            if res['returncode'] != 0 and res['cmd'] not in error_commands:
                log.write(f"[FAIL] Non-zero exit code!\n")
            elif 'Traceback' in res['stdout'] or 'Traceback' in res['stderr']:
                log.write(f"[FAIL] Traceback detected!\n")
            elif res['cmd'] in error_commands and res['returncode'] == 0:
                log.write(f"[FAIL] Expected error, but got 0!\n")
            else:
                if res['cmd'] in error_commands:
                    log.write("[OK - error as expected]\n")
                else:
                    log.write("[OK]\n")
    # Анализ лога и summary
    total_ok = 0
    total_fail = 0
    tracebacks = 0
    failed_cmds = []
    for res in results:
        is_error_case = res['cmd'] in error_commands
        if is_error_case and res['returncode'] != 0:
            total_ok += 1
        elif not is_error_case and res['returncode'] == 0 and 'Traceback' not in res['stdout'] and 'Traceback' not in res['stderr']:
            total_ok += 1
        else:
            total_fail += 1
            failed_cmds.append(res)
        if 'Traceback' in res['stdout'] or 'Traceback' in res['stderr']:
            tracebacks += 1
    elapsed = time.time() - start_time
    print(f"\nTest log: {LOG_FILE}")
    print(f"Total OK: {total_ok}")
    print(f"Total FAIL: {total_fail}")
    print(f"Tracebacks: {tracebacks}")
    print(f"Total time: {elapsed:.1f} sec")
    if failed_cmds:
        print("\nFailed commands:")
        for res in failed_cmds:
            print(f"[FAIL] {' '.join(str(x) for x in res['cmd'])}")
            print(f"Return code: {res['returncode']}")
            print(f"STDERR: {res['stderr'][:200]}")
    if total_fail > 0:
        print(f"Some tests failed. See {LOG_FILE} for details.")
        sys.exit(1)
    else:
        print("All CLI tests passed!")

if __name__ == "__main__":
    run_all() 