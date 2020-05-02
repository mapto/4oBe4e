#!/usr/bin/env python3
# coding: utf-8

from io import StringIO

import pytest  # type: ignore

from piece import Piece
from player import Player
import action


def test_roll_dice(monkeypatch):

    user_input = StringIO("\n")
    monkeypatch.setattr("sys.stdin", user_input)
    Player.create()  # needed because action.roll_dice asks for player name
    assert 1 <= action.roll_dice(0) <= 6


def test_ask_move_invalid_input(monkeypatch):

    Player.create()
    pieces = [Piece(0, 0, 1), Piece(0, 1, 1), Piece(0, 2, 1), Piece(0, 3, 1)]

    pawn_number = StringIO("\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("long_string\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("F\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("g\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("0\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("-1\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("1.3\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("4\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)


def test_ask_move_invalid_move(monkeypatch):
    with pytest.raises(AssertionError):
        action.ask_move([])

    pawn_number = StringIO(f"a\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move([Piece(1, 1, 1)])

    pawn_number = StringIO(f"B\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move([Piece(1, 0, 1)])


def test_ask_move_valid_input(monkeypatch):

    Player.create()
    pieces = [Piece(0, 0, 1), Piece(0, 1, 1), Piece(0, 2, 1), Piece(0, 3, 1)]

    pawn_number = StringIO("A\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 0

    pawn_number = StringIO("B\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 1

    pawn_number = StringIO("C\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 2

    pawn_number = StringIO("D\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 3

    pawn_number = StringIO("a\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 0

    pawn_number = StringIO("b\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 1

    pawn_number = StringIO("c\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 2

    pawn_number = StringIO("d\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 3


def test_ask_limited_valid_input(monkeypatch):

    Player.create()
    pieces = [Piece(0, 1, 1)]

    pawn_number = StringIO("A\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("B\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 1

    pawn_number = StringIO("\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 1

    pawn_number = StringIO("C\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("D\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("a\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("b\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(pieces) == 1

    pawn_number = StringIO("c\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)

    pawn_number = StringIO("d\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(EOFError):
        action.ask_move(pieces)
