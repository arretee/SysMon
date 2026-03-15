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

            # Memory
            memory_data = get_virtual_memory()

            live.update(table)
            table.add_row("Used Memory", str(memory_data["used"]) + " MB")
            table.add_row("Total Memory", str(memory_data["total"]) + " MB")
            table.add_row("Usage Percent", str(memory_data["percent"]) + " MB")

            # discs
            discs_data = get_disks_usage_percent()
            for disc in discs_data.keys():
                table.add_row(f"{disc} usage precent", str(discs_data[disc]) + " %")
