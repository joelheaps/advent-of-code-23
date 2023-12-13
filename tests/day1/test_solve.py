import pytest
from src.day1.solve import word_to_digit, get_digits, sum_all


def test_word_to_digit():
    assert (
        word_to_digit("one three five") == "1 3 5"
    ), "Failed to convert words to digits"
    assert (
        word_to_digit("hello world") == "hello world"
    ), "Incorrect conversion when no words present"


def test_get_digits():
    assert get_digits("a1b2c3") == "13", "Failed to extract first and last digits"
    assert get_digits("abc") == "", "Failed to return empty string when no digits"


def test_sum_all():
    assert sum_all(["12", "34", "56"]) == 102, "Failed to sum digit strings"


# Additional tests can be added as needed
