import time
import datetime

from rich.live import Live
from rich.table import Table

from collector import get_cpu_percent, get_disks_usage_percent, get_virtual_memory

def display_system_data_table(interval):
    """
    Function to draw a table with info about system usage

    :param interval: interval between refreshes.
    :return: null
    """
    with Live(refresh_per_second=interval) as live:
        while True:
            table = Table(title="System Metrics")

            table.add_column("Metric")
            table.add_column("Value")

            # CPU Data show
            cpu_data = get_cpu_percent()
            average_core_usage = round(sum(cpu_data) / len(cpu_data), 1)
            table.add_row("CPU Usage", f"{average_core_usage} %")
            for core_number, core_usage in enumerate(cpu_data):
                table.add_row(f"Core {core_number} usage", f"{core_usage} %")

            live.update(table)
            print(datetime.datetime.now())

