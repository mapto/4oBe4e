#!/usr/bin/env python3
# coding: utf-8

from io import StringIO

import pytest  # type: ignore

import action


def test_roll_dice(monkeypatch):

    user_input = StringIO("\n")
    monkeypatch.setattr("sys.stdin", user_input)
    assert 1 <= action.roll_dice(1) <= 6


def test_ask_move_invalid_input(monkeypatch):

    pawn_number = StringIO("\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(Exception):
        assert action.ask_move(1)

    pawn_number = StringIO("a_string\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(Exception):
        assert action.ask_move(1)

    pawn_number = StringIO("-1\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(Exception):
        assert action.ask_move(1)

    pawn_number = StringIO("1.3\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(Exception):
        assert action.ask_move(1)

    pawn_number = StringIO("4\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    with pytest.raises(Exception):
        assert action.ask_move(1)


def test_ask_move_valid_input(monkeypatch):

    pawn_number = StringIO("0\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(1) == 0

    pawn_number = StringIO("1\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(1) == 1

    pawn_number = StringIO("2\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(1) == 2

    pawn_number = StringIO("3\n")
    monkeypatch.setattr("sys.stdin", pawn_number)
    assert action.ask_move(1) == 3
