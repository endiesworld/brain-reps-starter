import pytest
from dsa.python.solutions.day_02_valid_parentheses import is_valid


def test_is_valid_basic_pair():
    assert is_valid("()") is True

def test_is_valid_multiple_types():
    assert is_valid("()[]{}") is True

def test_is_valid_wrong_match():
    assert is_valid("(]") is False

def test_is_valid_wrong_order():
    assert is_valid("([)]") is False

def test_is_valid_nested():
    assert is_valid("{[]}") is True

def test_is_valid_starts_with_closing():
    assert is_valid("]") is False

def test_is_valid_unclosed_opening():
    assert is_valid("[") is False

def test_is_valid_empty_string():
    assert is_valid("") is True