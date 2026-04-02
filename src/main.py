import threading
import time
import argparse
import pathlib

from collector import get_cpu_percent
from display import display_table
from logger import check_folder_exist, logger

def main():
    """
    Main function of SysMon Project. This function starts threads for display and for logger, also waits for CTRL + C From user and finish the threads.
    :return: None
    """

    # ----- Get Flags -----
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", help = "Time between log and table updates (Seconds)", default = 2, type = float)
    parser.add_argument("-l", "--log", help = "Path for logs file folder, if not given logs are not created!", default=None, type = str)
    parser.add_argument("--cpu-warn", help="Use flag without value to get colored cpu indication.", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--mem-warn", help="Use flag without value to get colored memory indication.", default=False, action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    interval = args.interval
    log_path = args.log
    cpu_warn_flag =args.cpu_warn
    mem_warn_flag = args.mem_warn



    # ----- Check arguments from flags -----
    # Check if log_path is given and there is a need to log stats
    logging = False # Variable that stores status of logger, is it active on this program run or not
    if log_path is not None:
        logging = True
        log_path = pathlib.Path(log_path).resolve()  # Create abspath to log folder


    # ----- Create threads stop event -----
    stop_event = threading.Event()


    # ----- Create threads for Display and Logger -----
    thread_display = threading.Thread(target=display_table, args=(interval, stop_event, mem_warn_flag, cpu_warn_flag))

    if logging:
        thread_logger = threading.Thread(target=logger, args=(interval, log_path, stop_event))




    try:
        # Display Data in the terminal
        thread_display.start()

        # Start logger function if path is given
        if logging:
            thread_logger.start()


        # Keep the main thread running until KeyboardInterrupt (CTRL + C)
        while True:
            time.sleep(interval/4)

    # CTRL + C -  Program EXIT
    except KeyboardInterrupt:
        # Close threads
        stop_event.set()

        # Join threads
        thread_display.join()
        if logging:
            thread_logger.join()

        # Send Exit confirmation
        print("\tThanks For Using SysMon\n")







if __name__ == '__main__':
    main()