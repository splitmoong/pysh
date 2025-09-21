"""
memory monitor for pysh
displays RAM usage in a boxed table with colors
"""

import psutil
import time
import os

RESET = "\033[0m"
HEADER_COLOR = "\033[1;37m"
LABEL_COLOR = "\033[1;36m"
VALUE_COLOR = "\033[1;33m"

def run(args=None):
    try:
        while True:
            if os.name == "nt":
                os.system("cls")
            else:
                print("\033[H\033[J", end="")

            mem = psutil.virtual_memory()

            print("+" + "-"*20 + "+" + "-"*15 + "+")
            print(f"|{HEADER_COLOR}{'Metric':^20}{RESET}|{HEADER_COLOR}{'Value':^15}{RESET}|")
            print("+" + "-"*20 + "+" + "-"*15 + "+")
            print(f"|{LABEL_COLOR}{'Total':^20}{RESET}|{VALUE_COLOR}{mem.total / (1024**3):.2f} GB{RESET}|")
            print(f"|{LABEL_COLOR}{'Used':^20}{RESET}|{VALUE_COLOR}{mem.used / (1024**3):.2f} GB{RESET}|")
            print(f"|{LABEL_COLOR}{'Available':^20}{RESET}|{VALUE_COLOR}{mem.available / (1024**3):.2f} GB{RESET}|")
            print(f"|{LABEL_COLOR}{'Usage %':^20}{RESET}|{VALUE_COLOR}{mem.percent:.1f}%{RESET}|")
            print("+" + "-"*20 + "+" + "-"*15 + "+")
            print("\nPress Ctrl+C to exit.")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nexiting memory monitor")
        return
