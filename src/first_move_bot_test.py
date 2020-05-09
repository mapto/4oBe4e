#!/usr/bin/env python3
# coding: utf-8

import pytest  # type: ignore
from state import GameState, GameMove, Board
from typing import Optional
from first_move_bot import FirstMoveBot


def test_other_player_returns_none(monkeypatch):
    # When we have a state where the current player is 0
    board = Board.create([0, 1, 3, 5])
    state = GameState.create(board)
    state.current_player = 0

    # And a bot which's player number is not the curren tone
    bot = FirstMoveBot(3)

    # When we call onState it should return None
    assert bot.onState(state) == None


def test_empty_moves_returns_none(monkeypatch):
    # When we have a state where the current player is 0
    board = Board.create([0, 1, 3, 5])
    state = GameState.create(board)
    state.current_player = 0

    # And valida_actions is empty
    state.valid_actions = []

    # And we have a bot with the current player number
    bot = FirstMoveBot(0)

    # When we call onState it should return None
    assert bot.onState(state) == None


def test_return_the_fist_possible_move(monkeypatch):
    # When we have a state where the current player is 0
    board = Board.create([0, 1, 3, 5])
    state = GameState.create(board)
    state.current_player = 0

    # And valida_actions is empty
    m1 = GameMove.roll_dice(0)
    m2 = GameMove.move_piece(0, 0, 1)
    m3 = GameMove.piece_out(0, 1)
    state.valid_actions = [m1, m2, m3]

    # And we have a bot with the current player number
    bot = FirstMoveBot(0)

    # When we call onState it should return the first valid move
    assert bot.onState(state) == m1

    state.valid_actions = [m2, m3, m1]
    assert bot.onState(state) == m2

    state.valid_actions = [m3, m1, m2]
    assert bot.onState(state) == m3
