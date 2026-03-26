import threading
import time
import argparse


from display import display_table

from logger import check_folder_exist, folder_can_be_created, logger

def main(interval, log_path):
    """
    Main function of SysMon Project. This function starts threads for display and for logger, also waits for CTRL + C From user and finish the threads.

    :param interval: Time between log and table updates (Seconds)
    :param log_path: Path for logs file folder.
    :return: None
    """
    # ----- Check arguments from flags -----
    # Check if log_path is given and there is a need to log stats
    logging = False # Variable that stores status of logger, is it active on this program run or not
    if logging is not None:
        logging = True

    # Check if log path is valid, if folder exists or can be created
    # If do not exist and cant be created, close program and throw error
    if logging:
        if not check_folder_exist(log_path) and not folder_can_be_created(log_path):
            raise ValueError("Path is invalid, Give path of existing folder or path to create one folder.")


    # ----- Create threads stop event -----
    stop_event = threading.Event()


    # ----- Create threads for Display and Logger -----
    thread_display = threading.Thread(target=display_table, args=(interval, stop_event))

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", help = "Time between log and table updates (Seconds)", default = 2, type = float)
    parser.add_argument("-l", "--log", help = "Path for logs file folder, if not given logs are not created!", default=None, type = str)


    args = parser.parse_args()

    main(args.interval, args.path)