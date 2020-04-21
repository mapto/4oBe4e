import pytest  # type: ignore

from piece import Piece


def test_invalid_position():
    p = Piece(0, 0)
    assert 0 == p.position()

    p = Piece(3, 0, 57)
    assert 0 == p.position()
