import pytest  # type: ignore
from state import Board, Piece, GameState, GameMove
import dataclasses, json


def test_default_board_init(monkeypatch):
    board = Board.create()
    assert board.players == [0, 1, 2, 3]
    assert board.pieces_per_player == 4
    assert board.board_corners == 4
    assert board.board_side_length == 14
    assert board.player_shift == 15
    assert board.finish_zone_length == 5
    assert board.end_progress == 66
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
    """Make sure if we have just two players in a 4 corner board for them
      to be at the opposite corners instead of next to each other.
    """
    board = Board.create(players=[1, 3])
    assert board.players == [1, 3]
    assert board.pieces_per_player == 4
    assert board.board_corners == 4
    assert board.board_side_length == 14
    assert board.player_shift == 15
    assert board.finish_zone_length == 5
    assert board.end_progress == 66

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


def test_3_players_5_corner_board_init(monkeypatch):
    """Make sure if we have just 3 players in a 5 corner board for them
      to be at the opposite corners instead of next to each other.
    """
    board = Board.create(players=[0, 2, 3], board_corners=5)
    assert board.players == [0, 2, 3]
    assert board.pieces_per_player == 4
    assert board.board_corners == 5
    assert board.board_side_length == 14
    assert board.player_shift == 15
    assert board.path_zone_length == 5 * 14 + 5
    assert board.finish_zone_length == 5
    assert board.end_progress == 5 * 14 + 5 + 5 + 1
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
        board_corners=5,
        board_side_length=13,
        finish_zone_length=3,
    )
    assert board.players == [0, 1]
    assert board.pieces_per_player == 1
    assert board.board_corners == 5
    assert board.board_side_length == 13
    assert board.player_shift == 14
    assert board.path_zone_length == 5 * 13 + 5
    assert board.finish_zone_length == 3
    assert board.end_progress == 5 * 13 + 5 + 3 + 1
    assert board.pieces == [Piece(0, 0, 0), Piece(0, 1, 0)]


def test_negative_create_wrong_players_board(monkeypatch):
    # player index bigger then the board
    # with pytest.raises(Exception):
    #    board = Board.create(players=[6, 1], board_corners=5)
    # board with no players
    with pytest.raises(Exception):
        Board.create(players=[])
    # board with duplicate players
    with pytest.raises(Exception):
        Board.create(players=[1, 1])
    # board with too many players
    with pytest.raises(Exception):
        Board.create(players=[0, 1, 2], board_corners=2)


def test_state_next_player(monkeypatch):
    board = Board.create(players=[0, 1, 3, 5])
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
    rel_pos_p0 = board.relative_position(piece=Piece(number=0, player=0, position=20))
    assert rel_pos_p0 == 20

    rel_pos_p1 = board.relative_position(piece=Piece(number=0, player=1, position=20))
    assert rel_pos_p1 == 35

    rel_pos_p2 = board.relative_position(piece=Piece(number=0, player=2, position=20))
    assert rel_pos_p2 == 50

    rel_pos_p3 = board.relative_position(piece=Piece(number=0, player=3, position=20))
    assert rel_pos_p3 == 5

    # Test a position outside of path_zone
    with pytest.raises(Exception):
        board.relative_position(piece=Piece(number=0, player=0, position=61))


def test_board_is_on_start():
    board = Board.create()

    p0_on_start = board.is_on_start(piece=Piece(number=0, player=0, position=0))
    assert not p0_on_start

    p0_on_start = board.is_on_start(piece=Piece(number=0, player=0, position=1))
    assert p0_on_start

    p0_on_start = board.is_on_start(piece=Piece(number=0, player=0, position=2))
    assert not p0_on_start


def test_board_is_on_path():
    board = Board.create()

    p0_on_path = board.is_on_path(piece=Piece(number=0, player=0, position=0))
    assert not p0_on_path

    p0_on_path = board.is_on_path(piece=Piece(number=0, player=0, position=10))
    assert p0_on_path

    p0_on_path = board.is_on_path(piece=Piece(number=0, player=0, position=61))
    assert not p0_on_path


def test_board_is_on_finish():
    board = Board.create()

    p0_on_finish = board.is_on_finish(piece=Piece(number=0, player=0, position=60))
    assert not p0_on_finish

    p0_on_finish = board.is_on_finish(piece=Piece(number=0, player=0, position=61))
    assert p0_on_finish

    p0_on_finish = board.is_on_finish(piece=Piece(number=0, player=0, position=66))
    assert not p0_on_finish


def test_board_is_on_target():
    board = Board.create()

    p0_on_target = board.is_on_target(piece=Piece(number=0, player=0, position=60))
    assert not p0_on_target

    p0_on_target = board.is_on_target(piece=Piece(number=0, player=0, position=66))
    assert p0_on_target
