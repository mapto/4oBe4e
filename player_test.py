#!/usr/bin/env python3
# coding: utf-8

from io import StringIO
import pytest  # type: ignore

import player


def test_ask_move_invalid_input(monkeypatch):
    for test_input in ["a_string", "", " ", "\n", -1, 1.3, 4, None, False]:
        pawn_number = StringIO(f"{test_input}\n")
        monkeypatch.setattr("sys.stdin", pawn_number)

        with pytest.raises(Exception):
            assert player.ask_move(1)


def test_ask_move_valid_input(monkeypatch):
    for test_input in [0, 1, 2, 3]:
        pawn_number = StringIO(f"{test_input}\n")
        monkeypatch.setattr("sys.stdin", pawn_number)

        assert player.ask_move(1) == test_input
