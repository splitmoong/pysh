"""
disk monitor for pysh
displays disk usage in a boxed table with colors
"""

import psutil
import time
import os

RESET = "\033[0m"
HEADER_COLOR = "\033[1;37m"  # bright white
DISK_COLOR = "\033[1;36m"    # cyan
USAGE_COLOR = "\033[1;33m"   # yellow

def run(args=None):
    try:
        while True:
            if os.name == "nt":
                os.system("cls")
            else:
                print("\033[H\033[J", end="")

            partitions = psutil.disk_partitions()
            print("+" + "-"*20 + "+" + "-"*15 + "+" + "-"*15 + "+")
            print(f"|{HEADER_COLOR}{'Device':^20}{RESET}|{HEADER_COLOR}{'Used %':^15}{RESET}|{HEADER_COLOR}{'Mount':^15}{RESET}|")
            print("+" + "-"*20 + "+" + "-"*15 + "+" + "-"*15 + "+")

            for p in partitions:
                try:
                    usage = psutil.disk_usage(p.mountpoint)
                    used_percent = f"{usage.percent:.1f}%"
                    print(f"|{DISK_COLOR}{p.device:^20}{RESET}|{USAGE_COLOR}{used_percent:^15}{RESET}|{p.mountpoint:^15}|")
                except PermissionError:
                    continue

            print("+" + "-"*20 + "+" + "-"*15 + "+" + "-"*15 + "+")
            print("\nPress Ctrl+C to exit.")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nexiting disk monitor")
        return
