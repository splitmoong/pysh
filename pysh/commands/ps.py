"""
Process monitor for Pysh
Displays top CPU-consuming processes in a table
"""

import psutil
import time
import os

RESET = "\033[0m"
HEADER_COLOR = "\033[1;37m"
PID_COLOR = "\033[1;36m"
NAME_COLOR = "\033[1;32m"
CPU_COLOR = "\033[1;33m"

def run(args=None):
    try:
        while True:
            if os.name == "nt":
                os.system("cls")
            else:
                print("\033[H\033[J", end="")

            procs = []
            for p in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    pid = p.pid
                    name = p.info['name'] or "?"
                    cpu = p.info['cpu_percent'] if p.info['cpu_percent'] is not None else 0.0
                    procs.append((pid, name, cpu))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            procs.sort(key=lambda x: x[2], reverse=True)
            top_procs = procs[:10]

            print("+" + "-"*8 + "+" + "-"*20 + "+" + "-"*8 + "+")
            print(f"|{HEADER_COLOR}{'PID':^8}{RESET}|{HEADER_COLOR}{'Process Name':^20}{RESET}|{HEADER_COLOR}{'CPU %':^8}{RESET}|")
            print("+" + "-"*8 + "+" + "-"*20 + "+" + "-"*8 + "+")

            for pid, name, cpu in top_procs:
                print(f"|{PID_COLOR}{pid:^8}{RESET}|{NAME_COLOR}{name[:20]:^20}{RESET}|{CPU_COLOR}{cpu:^8.1f}{RESET}|")

            print("+" + "-"*8 + "+" + "-"*20 + "+" + "-"*8 + "+")
            print("\nPress Ctrl+C to exit.")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting Process monitor.")
        return
