import psutil


def get_cpu_percent():
    return psutil.cpu_percent(interval=2, percpu=True)

def get_virtual_memory():
    return psutil.virtual_memory()

def get_disc_usage():
    return psutil.disk_usage('/')

def get_disk_partitions():
    return psutil.disk_partitions()