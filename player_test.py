#!/usr/bin/env python3
# coding: utf-8

from io import StringIO

import pytest  # type: ignore

import player


def test_ask_move_invalid_input(monkeypatch):

    pawn_number = StringIO(f"\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(Exception):
        assert player.ask_move(1)

    pawn_number = StringIO("a_string\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(Exception):
        assert player.ask_move(1)

    pawn_number = StringIO(f"-1\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(Exception):
        assert player.ask_move(1)

    pawn_number = StringIO(f"1.3\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(Exception):
        assert player.ask_move(1)

    pawn_number = StringIO(f"4\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(Exception):
        assert player.ask_move(1)


def test_ask_move_valid_input(monkeypatch):

    pawn_number = StringIO("0\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert player.ask_move(1) == 0

    pawn_number = StringIO("1\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert player.ask_move(1) == 1

    pawn_number = StringIO("2\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert player.ask_move(1) == 2

    pawn_number = StringIO("3\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert player.ask_move(1) == 3
