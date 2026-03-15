import psutil
import os


def get_cpu_percent():
    return psutil.cpu_percent(interval=2, percpu=True)

def get_virtual_memory():
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

def get_disc_usage(disc = 'C:'):
    """
    Returns named tuple with data about disc, if used without argument returns data about disc C.

    :param disc: gets string with name of the disc. example of string: 'C:'
    :return: Returns named tuple with data about disc, example of return: sdiskusage(total=999495213056, used=336265076736, free=663230136320, percent=33.6)
    """
    return psutil.disk_usage(disc)

def get_disks_usage_percent():
    """
    Function collect data about all discs on a pc and returns dict with names and usage percent of each.

    :return: dict with names and usage percent of each disc on a pc.
    """
    discs_data_temp = []
    disks_usage_percent = {}
    disc_path = ""

    discs_data_temp = psutil.disk_partitions()

    for disc in discs_data_temp:
        # Get disc path ('C:', 'D:',...)
        disc_path = disc[0][0:2]

        # Store data about usage percent into a dict
        disks_usage_percent[disc_path] = get_disc_usage(disc_path)[3]

    return disks_usage_percent