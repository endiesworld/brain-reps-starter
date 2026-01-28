import pytest
from dsa.python.solutions.day_01_two_sum import two_sum

def test_two_sum_basic():
    assert set(two_sum([2, 7, 11, 15], 9)) == {0, 1}

def test_two_sum_with_duplicates():
    assert set(two_sum([3, 3], 6)) == {0, 1}
