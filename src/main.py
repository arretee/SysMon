import threading
import time

from display import display_table

def main():
    # ----- Variables declaration -----
    interval = 2


    # ----- Create threads stop event -----
    stop_event = threading.Event()


    # ----- Create threads for Display and Logger -----
    thread_display = threading.Thread(target=display_table, args=(interval, stop_event))



    try:
        # ----- Display Data in the terminal -----
        thread_display.start()



        # Keep the main thread running until KeyboardInterrupt ( CTRL + C)
        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        stop_event.set()
        thread_display.join()

        print("\nThanks For Using SysMon\n")



























if __name__ == '__main__':
    main()