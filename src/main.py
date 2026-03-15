import threading

from collector import get_cpu_percent, get_disc_usage, get_virtual_memory
from display import display_system_data_table

def main():
    # ----- Variables declaration -----
    interval = 2


    # ----- Display Data in the terminal -----
    display_system_data_table(interval)




























if __name__ == '__main__':
    main()