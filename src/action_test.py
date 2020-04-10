#!/usr/bin/env python3
# coding: utf-8

from io import StringIO

import pytest  # type: ignore

from piece import Piece
import action


def test_ask_move_invalid_input(monkeypatch):

    pieces = [Piece(1, 0, 1), Piece(1, 1, 1), Piece(1, 2, 1), Piece(1, 3, 1)]

    pawn_number = StringIO(f"\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("a_string\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO(f"-1\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO(f"1.3\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO(f"4\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)


def test_ask_move_invalid_move(monkeypatch):
    with pytest.raises(AssertionError):
        action.ask_move([])

    pawn_number = StringIO(f"2\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move([Piece(1, 1, 1)])

    pawn_number = StringIO(f"2\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move([Piece(1, 0, 1)])


def test_ask_move_valid_input(monkeypatch):

    pieces = [Piece(1, 0, 1), Piece(1, 1, 1), Piece(1, 2, 1), Piece(1, 3, 1)]

    pawn_number = StringIO("0\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 0

    pawn_number = StringIO("1\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 1

    pawn_number = StringIO("2\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 2

    pawn_number = StringIO("3\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 3
