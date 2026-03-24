import threading
from time import sleep

from rich.live import Live
from rich.table import Table

from collector import get_cpu_percent, get_discs_usage_percent, get_memory_data

def display_table(interval, stop_event = threading.Event()):
    """
    Function to draw a table with info about system usage
    * if not stop_event is used -> function will use "While True:"

    :param interval: interval between refreshes.
    :param stop_event: A statement in while loop (while not stop_event), default value is threading.Event().
    :return: null
    """

    with Live(refresh_per_second=4) as live:
        while not stop_event.is_set():
            table = Table(title="System Metrics")
            table.add_column("Metric")
            table.add_column("Value")

            # CPU Data show
            cpu_data = get_cpu_percent()
            average_core_usage = round(sum(cpu_data) / len(cpu_data), 1) # get average core usage rounded to 1 digit after dot.
            table.add_row("CPU Usage", f"{average_core_usage} %")
            # Create row for every core
            for core_number, core_usage in enumerate(cpu_data):
                table.add_row(f"CPU Core {core_number} usage", f"{core_usage} %")

            # Memory
            memory_data = get_memory_data()

            table.add_row("Used Memory", str(memory_data["used"]) + " MB")
            table.add_row("Total Memory", str(memory_data["total"]) + " MB")
            table.add_row("Memory Usage Percent", str(memory_data["percent"]) + "%")

            # Discs
            discs_data = get_discs_usage_percent()
            for disc in discs_data.keys():
                table.add_row(f"{disc} usage precent", str(discs_data[disc]) + " %")

            # Update the table
            live.update(table)

            sleep(interval)
