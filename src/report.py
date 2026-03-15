from rich.live import Live
from rich.table import Table
import time


def f():
    with Live(refresh_per_second=1) as live:
        value = 130
        while True:
            table = Table(title="System Metrics")
            table.add_column("Metric")
            table.add_column("Value")
            # ... populate with data from collector ...
            value += 1

            for i in range(value):
                table.add_row(str(value), str(value))

            live.update(table)
            time.sleep(2)


f()