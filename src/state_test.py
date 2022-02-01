#!/usr/bin/env python3
# coding: utf-8

import pytest  # type: ignore
from state import Board, Piece, GameState, GameMove
import dataclasses, json


def test_default_board_init(monkeypatch):
    board = Board.create()

    # Defaults asserts
    assert board.players == [0, 1, 2, 3]
    assert board.pieces_per_player == 4
    assert board.board_sides == 4
    assert board.board_side_length == 14
    assert board.finish_zone_length == 5

    # Consistency asserts
    assert board.player_shift == 14
    assert (
        board.end_progress
        == board.player_shift * len(board.players) + board.finish_zone_length + 1
    )
    assert len(board.pieces) == len(board.players) * board.pieces_per_player

    # Explicit asserts
    assert list(filter(lambda p: p.player == 0, board.pieces)) == [
        Piece(0, 0, 0),
        Piece(1, 0, 0),
        Piece(2, 0, 0),
        Piece(3, 0, 0),
    ]
    assert list(filter(lambda p: p.player == 1, board.pieces)) == [
        Piece(0, 1, 0),
        Piece(1, 1, 0),
        Piece(2, 1, 0),
        Piece(3, 1, 0),
    ]
    assert list(filter(lambda p: p.player == 2, board.pieces)) == [
        Piece(0, 2, 0),
        Piece(1, 2, 0),
        Piece(2, 2, 0),
        Piece(3, 2, 0),
    ]
    assert list(filter(lambda p: p.player == 3, board.pieces)) == [
        Piece(0, 3, 0),
        Piece(1, 3, 0),
        Piece(2, 3, 0),
        Piece(3, 3, 0),
    ]


def test_2_players_board_init(monkeypatch):
    """Make sure if we have just two players in a 4 corner board for them
    to be at the opposite corners instead of next to each other.
    """
    board = Board.create([1, 3])

    # Redundant asserts
    assert board.players == [1, 3]

    # Defaults asserts
    assert board.pieces_per_player == 4
    assert board.board_sides == 4
    assert board.board_side_length == 14
    assert board.finish_zone_length == 5

    # Consistency asserts
    assert board.player_shift == board.board_side_length * board.board_sides // len(
        board.players
    )
    assert board.path_zone_length == len(board.players) * board.player_shift
    assert (
        board.end_progress
        == board.player_shift * len(board.players) + board.finish_zone_length + 1
    )
    assert len(board.pieces) == len(board.players) * board.pieces_per_player

    # Explicit asserts
    assert board.pieces == [
        Piece(0, 1, 0),
        Piece(1, 1, 0),
        Piece(2, 1, 0),
        Piece(3, 1, 0),
        Piece(0, 3, 0),
        Piece(1, 3, 0),
        Piece(2, 3, 0),
        Piece(3, 3, 0),
    ]


def test_3_players_6_corner_board_init(monkeypatch):
    """Make sure if we have just 3 players in a 5 corner board for them
    to be at the opposite corners instead of next to each other.
    """
    board = Board.create([0, 2, 3], board_sides=6, board_side_length=9)

    # Redundant asserts
    assert board.players == [0, 2, 3]
    assert board.board_sides == 6
    assert board.board_side_length == 9

    # Defaults asserts
    assert board.finish_zone_length == 5
    assert board.pieces_per_player == 4

    # Consistency asserts
    assert board.player_shift == board.board_side_length * board.board_sides // len(
        board.players
    )
    assert board.path_zone_length == len(board.players) * board.player_shift
    # end_progress == path_zone_length + finish_zone_length + 1 THAT IS
    # end_progress == (board_sides * board_side_length) + finish_zone_length + 1
    assert (
        board.end_progress
        == board.player_shift * len(board.players) + board.finish_zone_length + 1
    )
    assert len(board.pieces) == len(board.players) * board.pieces_per_player

    # Explicit asserts
    assert board.pieces == [
        Piece(0, 0, 0),
        Piece(1, 0, 0),
        Piece(2, 0, 0),
        Piece(3, 0, 0),
        Piece(0, 2, 0),
        Piece(1, 2, 0),
        Piece(2, 2, 0),
        Piece(3, 2, 0),
        Piece(0, 3, 0),
        Piece(1, 3, 0),
        Piece(2, 3, 0),
        Piece(3, 3, 0),
    ]


def test_custom_board_init(monkeypatch):
    board = Board.create([0, 1, 2, 3, 4], 1, 5, 10, 3)

    # Redundant asserts
    assert board.players == [0, 1, 2, 3, 4]
    assert board.pieces_per_player == 1
    assert board.board_sides == 5
    assert board.board_side_length == 10
    assert board.finish_zone_length == 3

    # Consistency asserts
    assert board.player_shift == board.board_side_length * board.board_sides // len(
        board.players
    )
    assert board.path_zone_length == len(board.players) * board.player_shift
    assert (
        board.end_progress
        == board.player_shift * len(board.players) + board.finish_zone_length + 1
    )
    assert len(board.pieces) == len(board.players) * board.pieces_per_player

    # Explicit asserts
    assert board.pieces == [
        Piece(0, 0, 0),
        Piece(0, 1, 0),
        Piece(0, 2, 0),
        Piece(0, 3, 0),
        Piece(0, 4, 0),
    ]


def test_negative_create_wrong_players_board(monkeypatch):
    # player index bigger then the board
    # with pytest.raises(Exception):
    #    board = Board.create(players=[6, 1], board_sides=5)
    # board with no players
    with pytest.raises(Exception):
        Board.create([])
    # board with duplicate players
    with pytest.raises(Exception):
        Board.create([1, 1])
    # board with too many players
    with pytest.raises(Exception):
        Board.create([0, 1, 2], board_sides=2)


def test_state_next_player(monkeypatch):
    board = Board.create([0, 1, 3, 5])
    state = GameState.create(board)

    assert state.current_player == 0
    # assert state.next_player() == 1

    state.current_player = 1
    # assert state.next_player() == 3

    state.current_player = 3
    # assert state.next_player() == 5

    state.current_player = 5
    # assert state.next_player() == 0


def test_game_state_defaults(monkeypatch):
    board = Board.create()
    state = GameState.create(board)

    assert state.board == board
    assert state.number == 0
    assert state.dice == -1
    assert state.winners == []
    assert state.current_player == 0
    assert state.valid_actions == [GameMove.roll_dice(player=0)]


def test_board_to_json(monkeypatch):
    board = Board.create()
    board_json = json.dumps(dataclasses.asdict(board))
    # print(board_json) TODO: compare expected output

    state = GameState.create(board)
    state_json = json.dumps(dataclasses.asdict(state))
    # print(state_json) TODO: compare expected output


def test_board_relative_position():
    board = Board.create()

    # Test relative position for each player
    rel_pos_p0 = board.relative_position(piece=Piece(number=0, player=0, progress=20))
    assert rel_pos_p0 == 20

    rel_pos_p1 = board.relative_position(piece=Piece(number=0, player=1, progress=20))
    assert rel_pos_p1 == 34

    rel_pos_p2 = board.relative_position(piece=Piece(number=0, player=2, progress=20))
    assert rel_pos_p2 == 48

    rel_pos_p3 = board.relative_position(piece=Piece(number=0, player=3, progress=20))
    assert rel_pos_p3 == 6

    # Test a position outside of path_zone
    with pytest.raises(Exception):
        board.relative_position(piece=Piece(number=0, player=0, progress=61))


def test_board_is_on_start():
    board = Board.create()

    p0_on_start = board.is_on_start(piece=Piece(number=0, player=0, progress=0))
    assert p0_on_start

    p0_on_start = board.is_on_start(piece=Piece(number=0, player=0, progress=1))
    assert not p0_on_start

    p0_on_start = board.is_on_start(piece=Piece(number=0, player=0, progress=2))
    assert not p0_on_start


def test_board_is_on_path():
    board = Board.create()

    p0_on_path = board.is_on_path(piece=Piece(number=0, player=0, progress=0))
    assert not p0_on_path

    p0_on_path = board.is_on_path(piece=Piece(number=0, player=0, progress=1))
    assert p0_on_path

    p0_on_path = board.is_on_path(piece=Piece(number=0, player=0, progress=10))
    assert p0_on_path

    p0_on_path = board.is_on_path(piece=Piece(number=0, player=0, progress=61))
    assert not p0_on_path


def test_board_is_on_finish():
    board = Board.create()

    p0_on_finish = board.is_on_finish(piece=Piece(number=0, player=0, progress=56))
    assert not p0_on_finish

    p0_on_finish = board.is_on_finish(piece=Piece(number=0, player=0, progress=61))
    assert p0_on_finish

    p0_on_finish = board.is_on_finish(piece=Piece(number=0, player=0, progress=62))
    assert not p0_on_finish


def test_board_is_on_target():
    board = Board.create()

    p0_on_target = board.is_on_target(piece=Piece(number=0, player=0, progress=61))
    assert not p0_on_target

    p0_on_target = board.is_on_target(piece=Piece(number=0, player=0, progress=62))
    assert p0_on_target

    p0_on_target = board.is_on_target(piece=Piece(number=0, player=0, progress=66))
    assert not p0_on_target
