import pytest  # type: ignore
from state import Board, Piece, GameState, RollDice


def test_default_board_init(monkeypatch):
    board = Board.create()
    assert board.players == [0, 1, 2, 3]
    assert board.pieces_per_player == 4
    assert board.shape_angles == 4
    assert board.shape_side_length == 14
    assert board.player_shift == 15
    assert board.finish_zone_length == 5
    assert board.end_progress == 62
    assert len(board.pieces) == 16
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
    """Make sure if we have just two players in a 4 angle board for them
      to be at the opposite corners instead of next to each other.
    """
    board = Board.create(players=[1, 3])
    assert board.players == [1, 3]
    assert board.pieces_per_player == 4
    assert board.shape_angles == 4
    assert board.shape_side_length == 14
    assert board.player_shift == 15
    assert board.finish_zone_length == 5
    assert board.end_progress == 62
    assert len(board.pieces) == 8
    assert board.pieces == [
        Piece(0, 0, 0),
        Piece(1, 0, 0),
        Piece(2, 0, 0),
        Piece(3, 0, 0),
        Piece(0, 1, 0),
        Piece(1, 1, 0),
        Piece(2, 1, 0),
        Piece(3, 1, 0),
    ]


def test_3_players_5_angle_board_init(monkeypatch):
    """Make sure if we have just 3 players in a 5 angle board for them
      to be at the opposite corners instead of next to each other.
    """
    board = Board.create(players=[0, 2, 3], shape_angles=5)
    assert board.players == [0, 2, 3]
    assert board.pieces_per_player == 4
    assert board.shape_angles == 5
    assert board.shape_side_length == 14
    assert board.player_shift == 15
    assert board.finish_zone_length == 5
    assert board.end_progress == 5 * 14 + 1 + 5
    assert len(board.pieces) == 3 * 4
    assert board.pieces == [
        Piece(0, 0, 0),
        Piece(1, 0, 0),
        Piece(2, 0, 0),
        Piece(3, 0, 0),
        Piece(0, 1, 0),
        Piece(1, 1, 0),
        Piece(2, 1, 0),
        Piece(3, 1, 0),
        Piece(0, 2, 0),
        Piece(1, 2, 0),
        Piece(2, 2, 0),
        Piece(3, 2, 0),
    ]


def test_custom_board_init(monkeypatch):
    board = Board.create(
        players=[0, 1],
        pieces_per_player=1,
        shape_angles=5,
        shape_side_length=13,
        finish_zone_length=3,
    )
    assert board.players == [0, 1]
    assert board.pieces_per_player == 1
    assert board.shape_angles == 5
    assert board.shape_side_length == 13
    assert board.player_shift == 14
    assert board.finish_zone_length == 3
    assert board.end_progress == 13 * 5 + 1 + 3
    assert board.pieces == [Piece(0, 0, 0), Piece(0, 1, 0)]


def test_negative_create_wrong_players_board(monkeypatch):
    # player index bigger then the board
    with pytest.raises(Exception):
        board = Board.create(players=[6, 1], shape_angles=5)
    # board with no players
    with pytest.raises(Exception):
        board = Board.create(players=[])
    # board with duplicate players
    with pytest.raises(Exception):
        board = Board.create(players=[1, 1])
    # board with too many players
    with pytest.raises(Exception):
        board = Board.create(players=[0, 1, 2], shape_angles=2)


def test_game_state_defaults(monkeypatch):
    board = Board.create()
    state = GameState.create(board)

    assert state.board == board
    assert state.number == 0
    assert state.dice == -1
    assert state.winners == []
    assert state.current_player == 0
    assert state.valid_actions == [RollDice(player=0)]
