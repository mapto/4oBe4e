import pytest  # type: ignore
from state import Board, Piece


def test_default_board_init(monkeypatch):
    board = Board.create()
    assert board.players_count == 4
    assert board.pieces_per_player == 4
    assert board.shape_angles == 4
    assert board.shape_side_length == 14
    assert board.player_shift == 15
    assert board.finish_zone_length == 5
    assert board.end_progress == 62
    assert len(board.pieces) == 16
    assert list(
        map(
            lambda p: (p.number, p.position),
            filter(lambda p: p.player == 0, board.pieces),
        )
    ) == [(0, 0), (1, 0), (2, 0), (3, 0)]

    assert list(
        map(
            lambda p: (p.number, p.position),
            filter(lambda p: p.player == 1, board.pieces),
        )
    ) == [(0, 0), (1, 0), (2, 0), (3, 0)]

    assert list(
        map(
            lambda p: (p.number, p.position),
            filter(lambda p: p.player == 2, board.pieces),
        )
    ) == [(0, 0), (1, 0), (2, 0), (3, 0)]

    assert list(
        map(
            lambda p: (p.number, p.position),
            filter(lambda p: p.player == 3, board.pieces),
        )
    ) == [(0, 0), (1, 0), (2, 0), (3, 0)]


def test_sutom_board_init(monkeypatch):
    board = Board.create(
        players_count=2,
        pieces_per_player=1,
        shape_angles=5,
        shape_side_length=13,
        finish_zone_length=3,
    )
    assert board.players_count == 2
    assert board.pieces_per_player == 1
    assert board.shape_angles == 5
    assert board.shape_side_length == 13
    assert board.player_shift == 14
    assert board.finish_zone_length == 3
    assert board.end_progress == 13 * 5 + 1 + 3
    assert board.pieces == [Piece(0, 0, 0), Piece(0, 1, 0)]
