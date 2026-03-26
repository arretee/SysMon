import collections
import threading

import pytest
from pytest_mock import mocker

import sys
sys.path.append("../src")

from collector import get_cpu_percent # CPU Functions
from collector import get_memory_data # Memory functions
from collector import get_discs_usage_percent, get_discs_list, get_disc_usage # Disc Functions
from collector import get_network_speed_deque_for_every_pc_connection, get_network_connection_speed_deque, network_dl_ul_calculation # Network functions

# --------------------------------- get_cpu_percent Tests --------------------------------
#Default tester
def test_get_cpu_percent(mocker):
    cpu_percent_mock = mocker.patch("psutil.cpu_percent")
    cpu_percent_mock.return_value = [20, 30, 40, 50, 60, 70]

    result = get_cpu_percent()

    assert result == [20, 30, 40, 50, 60, 70]

# --------------------------------- get_memory_data Tests --------------------------------
# Test zero values
def test_get_memory_data1(mocker):
    mock_memory = mocker.patch("psutil.virtual_memory")

    mock_memory.return_value= (0, 0, 0, 0)

    result = get_memory_data()
    assert result == {"used": 0, 'total': 0, 'percent': 0}

# Test random values
def test_get_memory_data2(mocker):
    mock_memory = mocker.patch("psutil.virtual_memory")

    mock_memory.return_value = (213134324, 134214214, 99.8, 213134000)

    result = get_memory_data()
    assert result == {"used": 213134000, 'total': 213134324, 'percent': 99.8}

# --------------------------------- get_discs_list Tests ---------------------------------
def test_get_discs_list1(mocker):
    # Mock functions
    mock_psutil_disk_partitions = mocker.patch("psutil.disk_partitions")
    mock_psutil_disk_partitions.return_value = [["C:/", 0, 0], ["D:/", 0, 0], ["E:/", 0, 0]]


    assert get_discs_list() == ["C:", "D:", "E:"], "Check for valid discs name"


# --------------------------------- get_disc_usage Tests ---------------------------------
def test_get_disc_usage():
    assert get_disc_usage(), "By default checks disc C:"
    assert get_disc_usage("D:"), "Check for existing disc"

    with pytest.raises(NameError, match="Discs with name this name not found"):
        get_disc_usage("J:")

# --------------------------------- get_discs_usage_percent Test ---------------------------------
# Default number of discs
def test_get_discs_usage_percent1(mocker):
    # Mock data that collected from pc
    mock_discs_list =  mocker.patch("psutil.disk_partitions")
    mock_discs_list.return_value = [['C:'], ['D:'], ['E:']]

    mock_get_disc_usage = mocker.patch("psutil.disk_usage")
    mock_get_disc_usage.return_value = (0, 0, 0, 33.6)

    # Assertion
    result = get_discs_usage_percent()
    assert result == {'C:': 33.6, 'D:': 33.6, 'E:': 33.6}

# Check for long float numbers
def test_get_discs_usage_percent2(mocker):
    # Mock data that collected from pc
    mock_discs_list =  mocker.patch("psutil.disk_partitions")
    mock_discs_list.return_value = [['C:'], ['D:'], ['E:']]

    mock_get_disc_usage = mocker.patch("psutil.disk_usage")
    mock_get_disc_usage.return_value = (0, 0, 0, 33.613213123213123123)

    # Assertion
    result = get_discs_usage_percent()
    assert result == {'C:': 33.6, 'D:': 33.6, 'E:': 33.6}



# --------------------------------- get_network_speed_deque_for_every_pc_connection Test ---------------------------------
# --------------------------------- get_network_connection_speed_deque Test ---------------------------------
# --------------------------------- network_dl_ul_calculation Test ---------------------------------
# I tried to create test for network functions, but the problem is that they using time and threads to work,
# I do not know and do not find how to do such tests.


# --------------------------------- get_time_string ---------------------------------
# Nothing to test

# --------------------------------- get_date_string ---------------------------------
# Nothing to test