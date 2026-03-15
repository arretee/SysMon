import time

from collector import get_cpu_percent, get_disc_usage, get_virtual_memory, get_disk_partitions
from display import display_system_data_table


def main():
    # ----- Variables declaration -----
    interval = 2

    #cpu variables
    cpu_per_core_percentage = []

    #memory variables
    memory_data_temp = ()
    memory_data = {
        "used": 0,
        "total": 0,
        "percent": 0.0,
    }

    #discs variables
    discs_data_temp = []
    discs_usage_data = {}
    disc_path = ""


    # ----- Program Main Loop -----
    while True:
        # ----- Get and sort the data ----

        #cpu
        cpu_per_core_percentage = get_cpu_percent()

        #memory
        memory_data_temp = get_virtual_memory()
        memory_data["used"] = memory_data_temp[3]
        memory_data["total"] = memory_data_temp[0]
        memory_data["percent"] = memory_data_temp[2]

        #discs
        discs_data_temp = get_disk_partitions()

        for disc in discs_data_temp:
            #Get disc path ('C:', 'D:',...)
            disc_path = disc[0][0:2]

            #Store data about usage percent into a dict
            discs_usage_data[disc_path] = get_disc_usage(disc_path)[3]


        # ----- Display Data in the terminal -----
        display_system_data_table(cpu_per_core_percentage, memory_data, discs_usage_data, interval)
        time.sleep(2)




























if __name__ == '__main__':
    main()