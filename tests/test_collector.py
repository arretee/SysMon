import sys
sys.path.insert(0, "../src")

import pytest

import collector

def test_get_disc_usage():
    assert collector.get_disc_usage(), "By default checks disc C:"
    assert collector.get_disc_usage("D:"), "Check for existing disc"

    with pytest.raises(NameError, match="Discs with name this name not found"):
        collector.get_disc_usage("J:")
