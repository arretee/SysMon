import psutil
import os


def get_cpu_percent():
    return psutil.cpu_percent(interval=2, percpu=True)

def get_virtual_memory():
    return psutil.virtual_memory()

def get_disc_usage(disc = 'C:'):
    """
    Returns named tuple with data about disc, if used without argument returns data about disc C.

    :param disc: gets string with name of the disc. example of string: 'C:'
    :return: Returns named tuple with data about disc, example of return: sdiskusage(total=999495213056, used=336265076736, free=663230136320, percent=33.6)
    """
    return psutil.disk_usage(disc)

def get_disk_partitions():
    return psutil.disk_partitions()