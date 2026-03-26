Project architecture:

The main function in main.py is starting 2 threads, for display function and logger function each.
After main function called the threads, main thread keep running inside While loop until CTRL + C is pressed.
After CTRL + C is pressed, main function call the stop statement for both threads and stops the program with exit message for user.
Main function can get 2 flags, one for interval of scans (Number of seconds between frames of logs and frames of table, by default = 2) and one for path where logs file will save (by default = "../logs").

The Display function is using rich package to display the data in cmd.
Display function get info from collector.py, with all data collector functions for PC information and time.

The logger function is creating file in path that user gave (or in default path -> "../logs")
Each file have name by date it was created on, example of file name "1970-1-1.csv"
Logger function also create new file if day is over during the program run. 
Logger function do not crush if it can't access to log file during the run, it waits and saves logs in memory until it can access.
Logger get info from Collector function also, not from display function. 
Logger create last log into a file after program stopped by CTRL + C.

Logger can create a folder, but only one folder for logs files. 
Example -> if path given is "../existed_folder/unexisted_folder", logger function will create unexisted_folder into existed_folder for logs file,
But if path is "../unexisted_folder1/unexisted_folder2", main function will throw an ValueError("Path is invalid, Give path of existing folder or path to create one folder.")
This checked on start of program inside main function in main.py.

