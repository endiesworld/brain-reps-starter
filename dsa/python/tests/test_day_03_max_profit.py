import pytest
from dsa.python.solutions.day_03_max_profit import max_profit



def test_max_profit_basic():
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5

def test_max_profit_no_profit():
    assert max_profit([7, 6, 4, 3, 1]) == 0

def test_max_profit_single_day():
    assert max_profit([5]) == 0

def test_max_profit_two_days_profit():
    assert max_profit([2, 4]) == 2

def test_max_profit_two_days_no_profit():
    assert max_profit([4, 2]) == 0

def test_max_profit_late_best_sell():
    assert max_profit([3, 2, 6, 1, 8]) == 7