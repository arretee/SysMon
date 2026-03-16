import threading

from collector import get_cpu_percent, get_disc_usage, get_memory_data
from display import display_system_data_table

def main():
    # ----- Variables declaration -----
    interval = 2


    try:
        # ----- Display Data in the terminal -----
        display_system_data_table(interval)

    except KeyboardInterrupt:
        print("\nThanks For Using SysMon\n")



























if __name__ == '__main__':
    main()