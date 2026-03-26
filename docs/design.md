# Project architecture:

## Main function
Main function can get 4 flags, one for interval of scans (Number of seconds between frames of logs and frames of table, by default = 2) and one for log_path where logs file will save (by default = None).
And 2 flags -> --mem-warn, --cpu-warn. this flags activate colored indication for cpu and memory stat, if stat above 60 percent -> yellow, if stat above 85 percent -> red.
The main function in main.py is starting 2 threads, for display function and logger function each.
The logger is activated only of -l or --log  flag is activated and correct path is given.
After main function called the threads, main thread keep running inside While loop until CTRL + C is pressed.
After CTRL + C is pressed, main function call the stop statement for both threads and stops the program with exit message for user.

## Display function
The Display function is using rich package to display the data in cmd.
Display function get info from collector.py, with all data collector functions for PC information and time.
Network data is saved and refreshes inside variable named "network_connections" inside the display function.

## Collector
For all pc spec except one, there is a function you call every time you need a pc stat.
Only one data collector is uniq, Network data -> for each network card in a pc created deque and thread that run endlessly and stores data in the deque.
That why you do not call collector function every time you need a network stat, you call it once for each interface and after that you can get info from deque that you got.
example -> after you call a function get_network_speed_deque_for_every_pc_connection from collector. you got a dict with all connections and their deque's.
To get that for one specific connection use: `connections_speed["Connection_name"][-1] -> (Download_speed, Upload_speed)`

## Logger function
The logger function is creating file in path that user gave.
Each file have name by date it was created on, example of file name "1970-1-1.csv"
Logger function also create new file if day is over during the program run. 
Logger function do not crush if it can't access to log file during the run, it waits and saves logs in memory until it can access.
Logger get info from Collector function also, not from display function. 
Network data is saved and refreshes inside variable named "network_connections" inside the logger function.
Logger create last log into a file after program stopped by CTRL + C.

### Logs file folder
Logger can create a folder, but only one folder for logs files. 
Example -> if path given is "../existed_folder/unexisted_folder", logger function will create unexisted_folder into existed_folder for logs file,
But if path is "../unexisted_folder1/unexisted_folder2", main function will throw an ValueError("Path is invalid, Give path of existing folder or path to create one folder.")
This checked on start of program inside main function in main.py.

