import pytest


def test_to_fail():
    assert False


def test_to_be_ok():
    assert 2 + 2 == 4