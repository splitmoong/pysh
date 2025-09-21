"""
CPU monitor for Pysh
Displays CPU usage per core in a boxed table with colors
Updates continuously, Ctrl+C to exit
"""

import psutil
import time
import os

# ANSI colors
RESET = "\033[0m"
HEADER_COLOR = "\033[1;37m"  # bright white
CORE_COLOR = "\033[1;36m"    # cyan
USAGE_COLOR = "\033[1;33m"   # yellow

def run(args=None):
    try:
        while True:
            # Clear screen
            if os.name == "nt":
                os.system("cls")
            else:
                print("\033[H\033[J", end="")  # ANSI clear screen

            cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
            num_cores = len(cpu_percent)

            # Table layout
            col_width = 12
            row_count = (num_cores + 1) // 2

            # Print top border
            print("+" + ("-" * col_width + "+") * 4)

            # Print header
            header = (
                f"|{HEADER_COLOR}{'CPU Core':^{col_width}}{RESET}"
                f"|{HEADER_COLOR}{'Usage %':^{col_width}}{RESET}"
                f"|{HEADER_COLOR}{'CPU Core':^{col_width}}{RESET}"
                f"|{HEADER_COLOR}{'Usage %':^{col_width}}{RESET}|"
            )
            print(header)

            # Print separator
            print("+" + ("-" * col_width + "+") * 4)

            # Print each row
            for i in range(row_count):
                col1_idx = i
                col2_idx = i + row_count if i + row_count < num_cores else None

                core1 = f"{CORE_COLOR}Core {col1_idx}{RESET}"
                usage1 = f"{USAGE_COLOR}{cpu_percent[col1_idx]:.1f}%{RESET}"

                if col2_idx is not None:
                    core2 = f"{CORE_COLOR}Core {col2_idx}{RESET}"
                    usage2 = f"{USAGE_COLOR}{cpu_percent[col2_idx]:.1f}%{RESET}"
                else:
                    core2 = usage2 = ""

                print(
                    f"|{core1:^{col_width}}|{usage1:^{col_width}}|{core2:^{col_width}}|{usage2:^{col_width}}|"
                )

                # Print row separator
                print("+" + ("-" * col_width + "+") * 4)

            print("\nPress Ctrl+C to exit.")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nexiting cpu monitor")
        return
