import psutil
import os

# -------------------------------- CPU Data Functions --------------------------------
def get_cpu_percent():
    return psutil.cpu_percent(interval=2, percpu=True)

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

    :return: list of all names of discs on a pc.
    """
    discs = []

    discs_data_temp = psutil.disk_partitions()
    for disc in discs_data_temp:
        # Get disc path ('C:', 'D:',...)
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