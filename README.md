# SysMon
cmd tool for monitoring and logging PC stats.

<img width="324" height="705" alt="image" src="https://github.com/user-attachments/assets/adb94833-befc-4d03-8a28-2affabdd0dc7" />


## Desctiption
Simple cmd tool that help to user monitor and log pc stats in real time, pc stats that program monitor: CPU AVG and per core usage, memory used/total/usage percent, disc usage per disc.

<img width="1703" height="598" alt="image" src="https://github.com/user-attachments/assets/dbcdfdf8-a703-4da5-8e66-dc79cb61c0cd" />

## Getting Started
### Dependencies
* Python : [Python WenSite](https://www.python.org/).
* Necessary Python packages: `pip install rich` , `pip install psutil`
* Windows 10 (Tested and created on Windows 10)

  
### Executing program
* Get Clone of project
* Open folder with projcet in the explorer
  
<img width="637" height="142" alt="image" src="https://github.com/user-attachments/assets/790cde8b-b8a2-4171-a9d1-efbaa5c1ca21" />

* Get into a `src` folder
* Type 'cmd' on the path line of explorer
  
<img width="759" height="34" alt="image" src="https://github.com/user-attachments/assets/7eef7674-3ded-41b5-a5e7-3dacffdcbd23" />'

* Type in command line the basic command to run - `python main.py`
  
<img width="280" height="22" alt="image" src="https://github.com/user-attachments/assets/4e811467-557c-4e5c-84e3-5b3bd6e47d5d" />

* To finish the program press CTRL + C in the cmd.

## Features 
### Interval flag
* Use flag -i or --interval to change interval between logs and table updates
* Default value of this flag is 2 seconds
* Example of using -i or --interval -> `python main.py -i 1`

### Path flag
* Use flag -l or --log to create logs and save them in your folder. 
* Example of using -l or --log -> `python main.py -l C:\My_Folder`
* As resault of this run, file with logs will created in `C:\My_Folder`
* Give paths of existing folders or path with only one last folder missing or you will get an error
