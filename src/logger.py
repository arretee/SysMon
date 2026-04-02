import pathlib
import threading
import time
import os
import csv

import collector

# ----------------------------------- Files And Folders Checks and Creation -----------------------------------
def check_folder_exist(path):
    """
    Function checks if folder exists on a pc

    :param path: path of a folder
    :return: True or False value
    """
    return pathlib.Path(path).is_dir()

def file_exist(path):
    """
    Function checks if file exist

    :param path: full path of file to check
    :return: True of False value
    """
    return os.path.isfile(path)

def create_log_file(file_path, params_names):
    """
    Function creates a file for logs. creates a csv file. also create a first line with param titles -> params_names[0], params_names[1], params_names[2], .....

    :param params_names: List of params names that logger had to log, for example -> ["CPU AVG", "CORE 0", "CORE 2", "USED MEMORY", "TOTAL MEMORY", "DISC C: USAGE", "DISC D: USAGE", "Ethernet Download Speed", "Ethernet Upload Speed"]
    :param file_path: full path of file, example -> "../logs/23-3-2000.csv"
    :return: None
    """
    try:
        with open(file_path, mode='w', newline='') as log_file:
            writer = csv.writer(log_file)
            writer.writerow(params_names)
    except FileNotFoundError:
        raise FileNotFoundError("Unknown Folder to create a File")



# ----------------------------------- Log data functions -----------------------------------
def get_params_titles(cores_number, discs_list, network_connections_names):
    """
    Function creates list with all params titles for log file

    :param cores_number: number of cpu cores.
    :param discs_list: list of all discs on PC.
    :param network_connections_names: list of all network connections names
    :return:  list with all params titles for log file, example -> ["Time", "CPU AVG Usage", "Core 0", "Memory Used", "Memory Total", "Memory Usage Percent", "Disc C: Usage Percent", "Ethernet Download Speed", "Ethernet Upload Speed"]
    """
    params_list = ["Time"]

    # CPU params
    params_list.append("CPU AVG Usage")   # Cpu Average title
    for core_num in range(cores_number):
        params_list.append(f"Core {core_num}")

    # Ram params
    params_list.append("Memory Used")
    params_list.append("Memory Total")
    params_list.append("Memory Usage Percent")

    # Discs params
    for disc in discs_list:
        params_list.append(f"Disc {disc} Usage Percent")

    # Network Connections
    for connection in network_connections_names:
        params_list.append(f"{connection} Download Speed")
        params_list.append(f"{connection} Upload Speed")

    return params_list

def get_log_line(cores_number, discs_list, network_connections):
    """
    Function collect data to a list for one log file
    Data collected and returned in this order -> ["Time", "CPU AVG Usage", "Core 0", "Core 1", ..., "Core X", "Memory Used", "Memory Total", "Memory Usage Percent", "Disc C: Usage Percent", "Disc D: Usage Percent", .... , "Disc X: Usage Percent", "Ethernet Download Speed", "Ethernet Upload Speed", ...]

    :param cores_number: number of cpu cores.
    :param discs_list: list of all discs on PC.
    :param network_connections: Dict of all network connections data in auto refreshes deque's, example -> {"Ethernet": deque(), "WiFi": deque()}
    :return: list with data for one log line. all the numbers will be converted to string and get units of measurement.
    """

    # ----- Variables Init -----
    cur_time = ''

    cpu_cores = []
    cpu_avg = 0
    memory_data = {}
    discs_usage_percents = {}

    params = []

    # ----- Collect Data -----
    # Time
    params.append(collector.get_time_string())  # Add current time

    # CPU Average
    cpu_cores = collector.get_cpu_percent()
    if cores_number == 0:
        raise ZeroDivisionError("Can't divide by zero, Number of cores can't be 0")
    cpu_avg = sum(cpu_cores) / cores_number  # Get Cpu Avg usage
    cpu_avg = str(round(cpu_avg, 1)) + " %"  # Round number after dot and convert to str with units
    params.append(cpu_avg)  # Add Cpu AVG

    # get all cpu cores stings
    for core in cpu_cores:
        params.append(str(core) + " %")

    # Memory
    memory_data = collector.get_memory_data()
    params.append(str(memory_data["used"]) + " MB")
    params.append(str(memory_data["total"]) + " MB")
    params.append(str(memory_data["percent"]) + " %")

    # Discs
    discs_usage_percents = collector.get_discs_usage_percent()
    for disc in discs_list:
        if disc in discs_usage_percents.keys():     # Check if disc is still in PC
            params.append(str(discs_usage_percents[disc]) + " %")
        else:
            params.append("Unknown Status")


    # Network Speeds
    for connection in network_connections.keys():
        try:
            # Create strings for params
            data = network_connections[connection][-1]
            dl_string = f"{round(data[0], 1)} kB/s"
            ul_string = f"{round(data[1], 1)} kB/s"

        except IndexError:
            # Create strings for params
            dl_string = "- kB/s"
            ul_string = "- kB/s"

        params.append(dl_string)
        params.append(ul_string)



    return params

def write_log_line(file_path, data):
    """
    Function that write a log line into a file.

    :param file_path: Full path of log file
    :param data: list of all elements to write inside file.
    :return: None
    """

    with open(file_path, mode="a", newline='') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(data)


# ----------------------------------- Main Log Loop Function -----------------------------------
def logger(interval, path: pathlib.Path, stop_event = threading.Event(), durations = -1):
    """
    Main Logger function logic. Creates file of logs, and saves logs in that file.

    :param interval: number of seconds between every log
    :param path: path of folder to create there a log file. pathling.Path obj
    :param stop_event: stop event of while loop inside the function -> threading.Event statement, by default loop is unstoppable.
    :param durations: Number of loop durations left to logger to do, created for testing.
    :return: None
    """

    # ----- Get file name from date -----
    str_date = collector.get_date_string()

    # ----- Get Full Path of a log file -----
    file_path = ''
    if str(path)[-1] == '/':
        file_path = str(path) + str_date + ".csv"
    else:
        file_path = str(path) + '/' + str_date + ".csv"

    # ----- Create Deque's dict for network logging -----
    network_connections = collector.get_network_speed_deque_for_every_pc_connection(interval)
    network_connections_names = network_connections.keys()

    # ----- Create variables -----
    cpu_cores_num = len(collector.get_cpu_percent())
    discs_list = collector.get_discs_list()

    params = []
    params_list_history = []

    # ----- Create folder if not exist -----
    if not check_folder_exist(path):
        path.mkdir(parents=True, exist_ok=True)

    # ----- Create file if not exist -----
    if not file_exist(file_path):
        create_log_file(file_path, get_params_titles(cpu_cores_num, discs_list, network_connections_names))


    # ----- Logger Loop -----
    # Main Logger While Loop
    while not stop_event.is_set() and durations != 0:
        # Get data list for log
        params = get_log_line(cpu_cores_num, discs_list, network_connections)

        # Get Current date
        temp_str_date = collector.get_date_string()

        # if the date do not equal the saved in memory date, change log file (Create new log file for new day) and update variables
        if temp_str_date != str_date:
            str_date = temp_str_date
            if str(path)[-1] == '/':
                file_path = str(path) + str_date + ".csv"
            else:
                file_path = str(path) + '/' + str_date + ".csv"

            if not file_exist(file_path):
                create_log_file(file_path, get_params_titles(cpu_cores_num, discs_list, network_connections_names))

        try:
            # If was a permission error, complete missed lines to log file
            if params_list_history != []:
                for line in params_list_history:
                    write_log_line(file_path, line)
                # clear the list
                params_list_history.clear()

            # Write log line
            write_log_line(file_path, params)

        # If access for file is denied, save lines to list.
        except PermissionError:
            params_list_history.append(params.copy())

        # Wait for interval
        time.sleep(interval)

        # Update number_of_duration
        if durations != -1:
            durations -= 1

    # ----- Create last log on exit of program -----
    # Create data list for log
    params = get_log_line(cpu_cores_num, discs_list, network_connections)

    # Write log line
    try:
        write_log_line(file_path, params)
    except PermissionError:
        pass