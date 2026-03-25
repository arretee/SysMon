import threading

import pytest

import sys
sys.path.append("../src")

import os

from logger import *
# ----------------------------------- Test -> Files And Folders Checks and Creation -----------------------------------

# ----- check_folder_exist -----
def test_check_folder_exist():
    assert check_folder_exist("..") == True, "Check for previous folder in dir"
    assert check_folder_exist("C:/") == True, "Check for absolute path Disc C:/"
    assert check_folder_exist("../uncreated_folder_1/uncreated_folder_2") == False, "Check for unknown path"

# ----- folder_can_be_created -----
def test_folder_can_be_created():
    assert folder_can_be_created("uncreated_folder_1") == True, "Check for option to create folder inside the current folder"
    assert folder_can_be_created("../uncreated_folder_1") == True, "Check for valid path 1"
    assert folder_can_be_created("../uncreated_folder_1/uncreated_folder_2") == False, "Check for invalid path, because uncreated_folder_1 is not exists"

# ----- folder_can_be_created -----
def test_file_exist():
    assert file_exist("../src/main.py") == True, "Check for file that is exists"
    assert file_exist("../src/funny_main.py") == False, "Check for file that not exists"
    assert file_exist("../src/uncreated_folder_1/uncreated_folder_2") == False, "Check for invalid path without file"


# ----- create_log_file -----
# Test with correct file name
def test_create_log_file1(tmp_path):
    file_path = tmp_path / "../test_create_log_file1_logs/25-4-1970.csv"
    params_names = ["Time", "CPU AVG", "CORE 0", "TEST 3"]

    os.mkdir(tmp_path / "../test_create_log_file1_logs") # create temp folder
    create_log_file(file_path, params_names) # create file

    # Check if file created
    assert os.path.exists(file_path) == True, "Check if file created successfully"

    # Check the content of created file
    with open(file_path, 'r') as f:
        file_content = f.read()

    assert file_content == ",".join(params_names) + "\n", "Check if file content is as expected"

# Test with incorrect file name
def test_create_log_file2(tmp_path):
    file_path = tmp_path / "../test_create_log_file2_logs/25-4-1970"
    params_names = ["Time", "CPU AVG", "CORE 0", "TEST 3"]

    os.mkdir(tmp_path / "../test_create_log_file2_logs") # create temp folder
    create_log_file(file_path, params_names) # create file

    # Check if file created
    assert os.path.exists(file_path) == True, "Check if file created successfully"

    # Check the content of created file
    with open(file_path, 'r') as f:
        file_content = f.read()

    assert file_content == ",".join(params_names) + "\n", "Check if file content is as expected"

# Test with incorrect file name
def test_create_log_file3(tmp_path):
    file_path = tmp_path / "../unknown_folder/25-4-1970"
    params_names = ["Time", "CPU AVG", "CORE 0", "TEST 3"]

    with pytest.raises(FileNotFoundError, match="Unknown Folder to create a File"):
            create_log_file(file_path, params_names)

# ----------------------------------- Test -> Log data functions -----------------------------------
# ----- get_params_titles -----
def test_get_params_titles(mocker):
    # Mock inside function get functions.
    mock_collector_get_cpu_percent = mocker.patch("collector.get_cpu_percent")
    mock_collector_get_cpu_percent.return_value = [0, 0, 0, 0, 0, 0]

    mock_collector_get_discs_list = mocker.patch("collector.get_discs_list")
    mock_collector_get_discs_list.return_value = ["C:", "D:"]


    result = get_params_titles()
    assert result == ["Time", "CPU AVG Usage", "Core 0", "Core 1", "Core 2", "Core 3", "Core 4", "Core 5", "Memory Used", "Memory Total", "Memory Usage Percent", "Disc C: Usage Percent", "Disc D: Usage Percent"]


# ----- get_log_line -----
# Test with valid input
def test_get_log_line1(mocker):
    # Mock Functions
    # time info
    mock_collector_get_time_string = mocker.patch("collector.get_time_string")
    mock_collector_get_time_string.return_value = "10:30:00"
    # cpu info
    mock_collector_get_memory_data = mocker.patch("collector.get_memory_data")
    mock_collector_get_memory_data.return_value = {"used": 213134000, 'total': 213134324, 'percent': 99.8}
    # memory info
    mock_collector_get_cpu_percent = mocker.patch("collector.get_cpu_percent")
    mock_collector_get_cpu_percent.return_value = [0, 0, 0, 0, 0, 0]
    # discs info
    mock_collector_get_discs_usage_percent = mocker.patch("collector.get_discs_usage_percent")
    mock_collector_get_discs_usage_percent.return_value = {"C:" : 50, "D:": 50}

    expected_list = ["10:30:00", "0.0 %", "0 %", "0 %", "0 %", "0 %", "0 %", "0 %", "213134000 MB", "213134324 MB", "99.8 %", "50 %", "50 %"]
    assert get_log_line(6, ["C:", "D:"]) == expected_list

# Test with input of -> number of cores = 0
def test_get_log_line2(mocker):
    # Mock Functions
    # time info
    mock_collector_get_time_string = mocker.patch("collector.get_time_string")
    mock_collector_get_time_string.return_value = "10:30:00"
    # cpu info
    mock_collector_get_memory_data = mocker.patch("collector.get_memory_data")
    mock_collector_get_memory_data.return_value = {"used": 213134000, 'total': 213134324, 'percent': 99.8}
    # memory info
    mock_collector_get_cpu_percent = mocker.patch("collector.get_cpu_percent")
    mock_collector_get_cpu_percent.return_value = [0]
    # discs info
    mock_collector_get_discs_usage_percent = mocker.patch("collector.get_discs_usage_percent")
    mock_collector_get_discs_usage_percent.return_value = {"C:" : 50, "D:": 50}

    # Assert
    with pytest.raises(ZeroDivisionError, match="Can't divide by zero, Number of cores can't be 0"):
        get_log_line(0, ["C:", "D:"])

# Test with zero discs in discs list input
def test_get_log_line3(mocker):
    # Mock Functions
    # time info
    mock_collector_get_time_string = mocker.patch("collector.get_time_string")
    mock_collector_get_time_string.return_value = "10:30:00"
    # cpu info
    mock_collector_get_memory_data = mocker.patch("collector.get_memory_data")
    mock_collector_get_memory_data.return_value = {"used": 213134000, 'total': 213134324, 'percent': 99.8}
    # memory info
    mock_collector_get_cpu_percent = mocker.patch("collector.get_cpu_percent")
    mock_collector_get_cpu_percent.return_value = [0, 0, 0, 0, 0, 0]
    # discs info
    mock_collector_get_discs_usage_percent = mocker.patch("collector.get_discs_usage_percent")
    mock_collector_get_discs_usage_percent.return_value = {"C:" : 50, "D:": 50}

    expected_list = ["10:30:00", "0.0 %", "0 %", "0 %", "0 %", "0 %", "0 %", "0 %", "213134000 MB", "213134324 MB", "99.8 %"]
    assert get_log_line(6, []) == expected_list



# ----------------------------------- Test -> Main Log Loop Function -----------------------------------
# ----- logger -----
# Test that log file is created
def test_logger1(mocker, tmp_path):
    # *In this function I am not creating files and folders for logger function, function will call functions: write_log_line, file_exist, create_log_file.
    # *The reason for this, There is a test for all this functions, this test if for testing logic of logger, that need this functions for test.

    path = "../test_logger1_logs"
    date = "1-1-1970"
    interval = 1
    stop_event = threading.Event()
    params_frame =  ["10:30:00", "0.0 %", "0 %", "0 %", "0 %", "0 %", "0 %", "0 %", "213134000 MB", "213134324 MB", "99.8 %", "50 %", "50 %"]
    param_titles = ["Time", "CPU AVG Usage", "Core 0", "Core 1", "Core 2", "Core 3", "Core 4", "Core 5", "Memory Used", "Memory Total", "Memory Usage Percent", "Disc C: Usage Percent", "Disc D: Usage Percent"]


    # mock functions
    mock_collector_get_date_string = mocker.patch("collector.get_date_string")
    mock_collector_get_date_string.return_value = date

    mock_collector_get_cpu_percent = mocker.patch("collector.get_cpu_percent")
    mock_collector_get_cpu_percent.return_value = [0, 0, 0, 0, 0, 0]

    mock_collector_get_discs_list = mocker.patch("collector.get_discs_list")
    mock_collector_get_discs_list.return_value = ["C:", "D:"]

    mock_get_log_line = mocker.patch("logger.get_log_line")
    mock_get_log_line.return_value = params_frame

    # call the function
    logger(interval, path, stop_event = stop_event, durations = 0)

    # Check if file created
    file_path = path + "/" + date + ".csv"

    try:
        assert os.path.isfile(file_path) == True, "Check if file created successfully"
    finally:
        os.remove(file_path)
        os.rmdir(path)

# Test for file content
def test_logger2(mocker, tmp_path):
    # *In this function I am not creating files and folders for logger function, function will call functions: write_log_line, file_exist, create_log_file.
    # *The reason for this, There is a test for all this functions, this test if for testing logic of logger, that need this functions for test.

    path = "../test_logger1_logs"
    date = "1-1-1970"
    interval = 1
    stop_event = threading.Event()
    params_frame = ["10:30:00", "0.0 %", "0 %", "0 %", "0 %", "0 %", "0 %", "0 %", "213134000 MB", "213134324 MB",
                    "99.8 %", "50 %", "50 %"]
    param_titles = ["Time", "CPU AVG Usage", "Core 0", "Core 1", "Core 2", "Core 3", "Core 4", "Core 5", "Memory Used",
                    "Memory Total", "Memory Usage Percent", "Disc C: Usage Percent", "Disc D: Usage Percent"]

    # mock functions
    mock_collector_get_date_string = mocker.patch("collector.get_date_string")
    mock_collector_get_date_string.return_value = date

    mock_collector_get_cpu_percent = mocker.patch("collector.get_cpu_percent")
    mock_collector_get_cpu_percent.return_value = [0, 0, 0, 0, 0, 0]

    mock_collector_get_discs_list = mocker.patch("collector.get_discs_list")
    mock_collector_get_discs_list.return_value = ["C:", "D:"]

    mock_get_log_line = mocker.patch("logger.get_log_line")
    mock_get_log_line.return_value = params_frame

    # call the function
    logger(interval, path, stop_event=stop_event, durations=2)

    # Check if file created
    file_path = path + "/" + date + ".csv"

    # Create expected output
    titles_str = ','.join(param_titles)
    log_line_str = ','.join(params_frame)

    output = titles_str + '\n'
    for i in range(3):  # number of logs lines is durations + 1
        output = output + log_line_str
        output = output + '\n'

    # Check the content of created file
    with open(file_path, 'r') as f:
        file_content = f.read()

    print(output)
    print('\n\n\n\n\n')
    print(file_content)

    try:
        assert file_content == output, "Check if file content fit expectation"
    finally:
        # delete file and folder after test
        os.remove(file_path)
        os.rmdir(path)


