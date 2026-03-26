import threading
from time import sleep

from rich.live import Live
from rich.table import Table

from collector import get_cpu_percent, get_discs_usage_percent, get_memory_data, get_network_speed_deque_for_every_pc_connection



def get_correct_color_indication(stat):
    """
    Function that returns color string for rich table segment by the stat.
    Above 60% is Yellow color, Above 85% is Red color.

    :param stat: stat to check and get color on.
    :return: "[red]" if stat above 85, "[yellow]" if stat above 60, "" otherwise.
    """
    YELLOW_COLOR_PERCENT = 60   # Percent where yellow color starts
    RED_COLOR_PERCENT = 85 # Percent where red color starts
    if stat >= RED_COLOR_PERCENT:
        return "[red]"
    elif stat >= YELLOW_COLOR_PERCENT:
        return "[yellow]"
    else:
        return ""





def display_table(interval, stop_event = threading.Event(), mem_warn_flag = False, cpu_warn_flag = False):
    """
    Function to draw a table with info about system usage
    * if not stop_event is used -> function will use "While True:"

    :param interval: interval between refreshes.
    :param stop_event: A statement in while loop (while not stop_event), default value is threading.Event().
    :param cpu_warn_flag: flag that add colored memory indication
    :param mem_warn_flag: flag that add colored cpu indication
    :return: null
    """

    # Create dict with auto refresh network data
    network_connections = get_network_speed_deque_for_every_pc_connection(interval)


    with Live(refresh_per_second=4) as live:
        while not stop_event.is_set():
            table = Table(title="System Metrics")
            table.add_column("Metric")
            table.add_column("Value")

            # CPU Data show
            cpu_data = get_cpu_percent()
            average_core_usage = round(sum(cpu_data) / len(cpu_data), 1) # get average core usage rounded to 1 digit after dot.

            # Get color for CPU AVG if --cpu-warn flag activated
            cpu_color = get_correct_color_indication(average_core_usage) if cpu_warn_flag else ""

            # Add CPU AVG to table
            table.add_row(f"CPU Usage", f"{cpu_color}{average_core_usage} %")

            # Create row for every core
            for core_number, core_usage in enumerate(cpu_data):
                # Get color for CPU AVG if --cpu-warn flag activated
                cpu_color = get_correct_color_indication(core_usage) if cpu_warn_flag else ""

                table.add_row(f"CPU Core {core_number} usage", f"{cpu_color}{core_usage} %")

            # Memory
            memory_data = get_memory_data()

            # Get color for Memory usage and percent if --mem-warn flag activated
            mem_color = get_correct_color_indication(memory_data["percent"]) if mem_warn_flag else ""

            table.add_row("Used Memory", mem_color + str(memory_data["used"]) + " MB")
            table.add_row("Total Memory", str(memory_data["total"]) + " MB")
            table.add_row("Memory Usage Percent", mem_color + str(memory_data["percent"]) + "%")

            # Discs
            discs_data = get_discs_usage_percent()
            for disc in discs_data.keys():
                table.add_row(f"{disc} usage precent", str(discs_data[disc]) + " %")\

            # Network Speed
            for connection in network_connections.keys():
                dl_name = f"{connection} \nDownload Speed"
                ul_name = f"{connection} \nUpload Speed"
                try:
                    # Create strings for table
                    data = network_connections[connection][-1]
                    dl_string = f"{round(data[0], 1)} kB/s"
                    ul_string = f"{round(data[1], 1)} kB/s"

                except IndexError:
                    # Create strings for table
                    dl_string = "- kB/s"
                    ul_string = "- kB/s"

                # Add rows to table
                table.add_row(dl_name, dl_string)
                table.add_row(ul_name, ul_string)



            # Update the table
            live.update(table)

            sleep(interval)
