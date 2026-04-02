# SysMon
cmd tool for monitoring and logging PC stats.

<img width="331" height="890" alt="image" src="https://github.com/user-attachments/assets/2c270888-b6f0-4a4b-9a05-9767575ff1e5" />



## Desctiption
Simple cmd tool that help to user monitor and log pc stats in real time, pc stats that program monitor: CPU AVG and per core usage, memory used/total/usage percent, disc usage per disc, Donwload and upload speed per network interface.

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

### Memory warn flag
* use flag --mem-warn for turning on memory colored indication
* when memory usage percent above 85 the stat is colored red
* when memory usage percent above 60 the stat is colored yellow
* Example of using --mem-warn -> `python main.py --mem-warn`
  
### CPU warn flag
* use flag --cpu-warn for turning on cpu colored indication
* when cpu core or avg usage percent above 85 the stat is colored red
* when cpu core or avg usage percent above 60 the stat is colored yellow
* Example of using --cpu-warn -> `python main.py --cpu-warn`
