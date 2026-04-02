import datetime
import threading
import time
from time import sleep
from collections import deque

import psutil

# -------------------------------- CPU Data Functions --------------------------------
def get_cpu_percent():
    """
    Function returns per core list of percent of usage for each core of CPU.
    WARNING: on first call, returns 0, 0, 0, 0, 0.

    :return:
    """
    return psutil.cpu_percent(interval=0, percpu=True)

# -------------------------------- Memory Data Functions --------------------------------
def get_memory_data():
    """
    Function that collect data about memory.

    :return: dict with keys: "used", "total, "percent".
    """
    memory_data_temp = ()
    memory_data = {
        "used": 0,
        "total": 0,
        "percent": 0.0,
    }

    memory_data_temp = psutil.virtual_memory()
    memory_data["used"] = memory_data_temp[3]
    memory_data["total"] = memory_data_temp[0]
    memory_data["percent"] = memory_data_temp[2]
    return memory_data

# -------------------------------- Discs Data Functions --------------------------------
def get_discs_list():
    """
    function that create list with the names of all discs on a pc

    :return: list of all names of discs on a pc. Example -> ["C:", "D:"]
    """
    discs = []

    discs_data_temp = psutil.disk_partitions()
    # Create list of discs
    for disc in discs_data_temp:
        discs.append(disc[0][0:2])

    return discs

def get_disc_usage(disc = 'C:'):
    """
    Returns named tuple with data about disc, if used without argument returns data about disc C.

    :param disc: gets string with name of the disc. example of string: 'C:'
    :return: Returns named tuple with data about disc, example of return: sdiskusage(total=999495213056, used=336265076736, free=663230136320, percent=33.6)
    """
    discs = get_discs_list()

    if disc not in discs:
        raise NameError("Discs with name this name not found")

    return psutil.disk_usage(disc)

def get_discs_usage_percent():
    """
    Function collect data about all discs on a pc and returns dict with names and usage percent of each.

    :return: dict with names and usage percent of each disc on a pc.
    """
    discs_list = []
    disks_usage_percent = {}

    discs_list = get_discs_list()

    for disc in discs_list:
        # Store data about usage percent into a dict
        disks_usage_percent[disc] = round(get_disc_usage(disc)[3], 1)

    return disks_usage_percent

# -------------------------------- NetWork Data functions --------------------------------
def get_network_speed_deque_for_every_pc_connection(interval):
    """
    Function that creates dict with all pc network connection keys, and refreshable deque's like values that shows network speed for that connection.
    you can access data like that -> connections_speed["Connection_name"][-1] -> (Download_speed, Upload_speed)

    :param interval: Number of seconds between every deque is refreshed the info.
    :return: example of dict: {"Ethernet": deque(), "WiFi": deque()}, each deque refresh every (interval) seconds by itself and store current speed of network on this connection.
    """
    # Get all network connections
    counter = psutil.net_io_counters(pernic=True)
    connections_list = []
    for key in counter.keys():
        connections_list.append(key)

    # Create final dict with deque's
    connections_speed = {}
    for connection in connections_list:
        connections_speed[connection] = get_network_connection_speed_deque(interval, connection)

    return connections_speed

def get_network_connection_speed_deque(interval, interface="Ethernet"):
    """
    Function creates deque that stores relevant network data in format like -> deque[-1] = (current dl, current ul).
    Function create thread that run endlessly, run this function carefully to save computer resources.

    :param interval: Interval that data refreshes inside the deque.
    :return: deque with data, data refresh every (Interval) of seconds.
    :param interface: PC interface to check speed on, for example -> "Ethernet" (By Default is "Ethernet")
    """

    # Create Deque for thread results
    dl_ul_speed_deque = deque(maxlen=1)
    dl_ul_speed_deque.append((0,0))

    # Create thread for collecting network data
    thread_network_calculation = threading.Thread(target=network_dl_ul_calculation, args=(dl_ul_speed_deque, interval, interface))
    thread_network_calculation.daemon = True

    thread_network_calculation.start()


    return dl_ul_speed_deque

def network_dl_ul_calculation(q, interval, interface="Ethernet"):
    """
    Function creates While loop that endlessly calculate network speed information and store it inside deque.
    Use function like a thread that will run endlessly.
    calculate speed in units of kB/s.

    :param q: deque to store info about networking, current data stored in last element like (dl, du)
    :param interval: interval between calculations
    :param interface: PC interface to check speed on, for example -> "Ethernet" (By Default is "Ethernet")
    :return: None
    """
    time_start = time.time()

    counter = psutil.net_io_counters(pernic=True)[interface]
    stats =  (counter.bytes_recv, counter.bytes_sent)

    while True:
        # Save current stats
        last_stats = stats

        # Sleep for interval
        time.sleep(interval)

        # Get new stats
        counter = psutil.net_io_counters(pernic=True)[interface]
        time_current = time.time()
        stats = (counter.bytes_recv, counter.bytes_sent)

        dl = (stats[0] - last_stats[0]) / (time_current - time_start) / 1000
        ul = (stats[1] - last_stats[1]) / (time_current - time_start) / 1000

        q.append((dl, ul))
        time_start = time.time()


# -------------------------------- Get Time Functions --------------------------------
def get_time_string():
    """
    Get Time Function

    :return: string with current time -> hh:mm:ss
    """
    return str(datetime.datetime.now().time())[0:8]

def get_date_string():
    """
    Get Date Function

    :return: string with current date -> year:month:day
    """
    cur_date = datetime.date.today()
    str_date = f"{cur_date.year}-{cur_date.month}-{cur_date.day}"

    return str_date
