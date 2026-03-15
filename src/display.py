from rich.live import Live
from rich.table import Table

def display_system_data_table(cpu_data, memory_data, discs_usage, interval):
    """
    Display table in command line with metrics and values about system usage.


    :param cpu_data: list of the load on each processor core
    :param memory_data: dictionary stores data about memory with keys: "used", "total", "percent".
    :param discs_usage: dictionary stores data about discs usage with keys: "C:", "D:"... Values of these keys is the usage of each disc.
    :param interval: get the interval time between refreshes
    :return: null.
    """
    with Live(refresh_per_second=1) as live:
            table = Table(title="System Metrics")

            table.add_column("Metric")
            table.add_column("Value")

            # CPU Data show
            average_core_usage = sum(cpu_data) / len(cpu_data)
            table.add_row("CPU Usage", f"{average_core_usage} %")
            for core_number, core_usage in enumerate(cpu_data):
                table.add_row(f"Core {core_number} usage", f"{core_usage} %")

            live.update(table)

