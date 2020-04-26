import pytest  # type: ignore
from state import Board, Piece, GameState, GameMove
from engine import GameEngine, Dice


def test_initial_gate_state(monkeypatch):
    # Given
    board = Board.create(players=[1, 3])
    state = GameState.create(board)

    # When
    game = GameEngine(board)

    # Then
    assert game.state == state


def test_play_invalid_action_on_initial_state(monkeypatch):
    # Given
    board = Board.create(players=[1, 3])
    state = GameState.create(board)
    game = GameEngine(board)

    # When we try to play an invalid action PieceOut
    with pytest.raises(Exception):
        game.play(GameMove.piece_out(1, 1, 6))

    # When we try to play valid action for an invalid Player
    with pytest.raises(Exception):
        game.play(GameMove.roll_dice(player=3))


def test_play_roll_dice_6(monkeypatch):
    # Given
    board = Board.create(players=[1, 3])
    state = GameState.create(board)
    dice = Dice()
    monkeypatch.setattr(dice, "roll", lambda: 6)
    game = GameEngine(board, dice)

    # When
    new_state = game.play(GameMove.roll_dice(player=1))

    # Then
    # assert new_state == game.get_state()
    assert new_state.number == 1
    assert new_state.dice == 6
    assert new_state.valid_actions == [
        GameMove.piece_out(player=1, piece=0, dice=6),
        GameMove.piece_out(player=1, piece=1, dice=6),
        GameMove.piece_out(player=1, piece=2, dice=6),
        GameMove.piece_out(player=1, piece=3, dice=6),
    ]


def test_play_roll_dice_3(monkeypatch):
    # Given
    board = Board.create(players=[1, 3])
    state = GameState.create(board)
    dice = Dice()
    monkeypatch.setattr(dice, "roll", lambda: 3)
    game = GameEngine(board, dice)

    # When
    new_state = game.play(GameMove.roll_dice(player=1))

    # Then
    assert new_state == game.get_state()
    assert new_state.number == 1
    assert new_state.dice == 3
    assert new_state.valid_actions == [GameMove.roll_dice(player=3)]

    # And When
    new_state = game.play(GameMove.roll_dice(player=3))

    # Then
    assert new_state == game.get_state()
    assert new_state.number == 2
    assert new_state.dice == 3
    assert new_state.valid_actions == [GameMove.roll_dice(player=1)]


def test_play_until_the_end_two_players_once_piece(monkeypatch):
    # Given we have started the game
    board = Board.create(players=[0, 2], pieces_per_player=1)
    state = GameState.create(board)
    dice = Dice()
    monkeypatch.setattr(dice, "roll", lambda: 6)
    game = GameEngine(board, dice)

    # When we roll the dice
    new_state = game.play(GameMove.roll_dice(player=0))

    # Then the state should be as expected
    assert new_state == game.get_state()
    assert new_state.number == 1
    assert new_state.dice == 6
    assert new_state.valid_actions == [
        GameMove.piece_out(player=0, piece=0, dice=6),
    ]

    # And When we play getting out with the first peice
    new_state = game.play(GameMove.piece_out(player=0, piece=0, dice=6))
    # Then the first piece should be out
    assert new_state.current_player == 0
    assert new_state.number == 2
    assert new_state.dice == 6
    assert new_state.board.pieces == [
        Piece(number=0, player=0, position=1),
        Piece(number=0, player=2, position=0),
    ]
    assert new_state.valid_actions == [GameMove.roll_dice(player=0)]

    # And When we row the dice again with 6
    new_state = game.play(GameMove.roll_dice(player=0))
    # Then we should should be able to move the piece forward
    assert new_state.number == 3
    assert new_state.dice == 6
    assert new_state.valid_actions == [GameMove.move_piece(player=0, piece=0, dice=6)]

    # And When we move the piece
    new_state = game.play(GameMove.move_piece(player=0, piece=0, dice=6))
    # Then it should go forward and we should be able to roll the dice again
    assert new_state.number == 4
    assert new_state.winners == []
    assert new_state.board.pieces == [
        Piece(number=0, player=0, position=7),
        Piece(number=0, player=2, position=0),
    ]
    assert new_state.valid_actions == [GameMove.roll_dice(player=0)]

    # And When we roll the dice again with 6
    new_state = game.play(GameMove.roll_dice(player=0))
    # Then we should be able to move the piece forward
    assert new_state.dice == 6
    assert new_state.number == 5
    assert new_state.valid_actions == [GameMove.move_piece(player=0, piece=0, dice=6)]

    # And When we move the piece
    new_state = game.play(GameMove.move_piece(player=0, piece=0, dice=6))
    # Then the piece should go forward and we should be able to roll the dice again
    assert new_state.number == 6
    assert new_state.board.pieces == [
        Piece(number=0, player=0, position=13),
        Piece(number=0, player=2, position=0),
    ]
    assert new_state.winners == []
    assert new_state.valid_actions == [GameMove.roll_dice(player=0)]

    # And When we position the piece toward the end of the board
    new_state.board.pieces[0].position = board.end_progress - 6

    # And When we roll the dice again with 6
    new_state = game.play(GameMove.roll_dice(player=0))
    # Then we should be able to move the piece forward into the safe zone and to the goal
    assert new_state.dice == 6
    assert new_state.number == 7
    assert new_state.valid_actions == [GameMove.move_piece(player=0, piece=0, dice=6)]

    # And When we move the piece
    new_state = game.play(GameMove.move_piece(player=0, piece=0, dice=6))
    # Then the piece should go forward and we should be able to roll the dice again
    assert new_state.number == 8
    assert new_state.board.pieces == [
        Piece(number=0, player=0, position=board.end_progress),
        Piece(number=0, player=2, position=0),
    ]
    assert new_state.winners == [0]
    assert new_state.valid_actions == []


def test_do_not_move_piece_to_end_on_bigger_dice(monkeypatch):
    # Given we have started the game and a piece is in the safe zone
    board = Board.create(players=[0, 2], pieces_per_player=1)
    state = GameState.create(board)
    dice = Dice()
    monkeypatch.setattr(dice, "roll", lambda: 5)
    game = GameEngine(board, dice)

    state.board.pieces[0].position = board.end_progress - 3

    # When we roll the dice with 5 which is bigger then we need to
    # get to the goal
    new_state = game.play(GameMove.roll_dice(player=0))

    # Then the piece should not go to the goal and it should be the
    # next player turn
    assert new_state == game.get_state()
    assert new_state.number == 1
    assert new_state.dice == 5
    assert new_state.valid_actions == [
        GameMove.roll_dice(player=2),
    ]
    assert new_state.board.pieces == [
        Piece(number=0, player=0, position=board.end_progress - 3),
        Piece(number=0, player=2, position=0),
    ]
    assert new_state.winners == []


def test_do_move_take_out_of_home(monkeypatch):
    dice4 = Dice()
    monkeypatch.setattr(dice4, "roll", lambda: 4)
    dice6 = Dice()
    monkeypatch.setattr(dice6, "roll", lambda: 6)

    b = Board.create(players=[0, 1], pieces_per_player=1)
    g = GameEngine(b)
    assert GameMove.roll_dice(0) in g.state.valid_actions

    g.dice = dice4
    s = g.play(GameMove.roll_dice(0))
    assert GameMove.roll_dice(1) in s.valid_actions

    g.dice = dice6
    s = g.play(GameMove.roll_dice(1))
    s = g.play(GameMove.piece_out(1, 0, 6))
    assert s.board.pieces == [Piece(0, 0, 0), Piece(0, 1, 1)]
    assert GameMove.roll_dice(1) in s.valid_actions

    s = g.play(GameMove.roll_dice(1))
    s = g.play(GameMove.move_piece(1, 0, 6))
    assert s.board.pieces == [Piece(0, 0, 0), Piece(0, 1, 7)]
    assert GameMove.roll_dice(1) in s.valid_actions

    s = g.play(GameMove.roll_dice(1))
    s = g.play(GameMove.move_piece(1, 0, 6))
    assert s.board.pieces == [Piece(0, 0, 0), Piece(0, 1, 13)]
    assert GameMove.roll_dice(1) in s.valid_actions

    s = g.play(GameMove.roll_dice(1))
    s = g.play(GameMove.move_piece(1, 0, 6))
    assert s.board.pieces == [Piece(0, 0, 0), Piece(0, 1, 19)]
    assert GameMove.roll_dice(1) in s.valid_actions

    s = g.play(GameMove.roll_dice(1))
    s = g.play(GameMove.move_piece(1, 0, 6))
    assert s.board.pieces == [Piece(0, 0, 0), Piece(0, 1, 25)]
    assert GameMove.roll_dice(1) in s.valid_actions

    g.dice = dice4
    s = g.play(GameMove.roll_dice(1))
    s = g.play(GameMove.move_piece(1, 0, 4))
    assert s.board.pieces == [Piece(0, 0, 0), Piece(0, 1, 29)]
    assert GameMove.roll_dice(0) in s.valid_actions

    g.dice = dice6
    s = g.play(GameMove.roll_dice(0))
    assert GameMove.piece_out(0, 0, 6) in s.valid_actions
    s = g.play(GameMove.piece_out(0, 0, 6))

    # TODO: Not yet implemented:
    # assert s.board.pieces == [Piece(0, 0, 1), Piece(0, 1, 0)]
    assert s.board.pieces == [Piece(0, 0, 1), Piece(0, 1, 29)]


""" TODO: Convert into state-syntax


def test_do_move_cant_out_of_home():
    p1 = Player.get(1)
    piece = Piece(1, 0, 0)
    status = [piece]

    assert not is_valid_move(piece, 5, status)

    success = do_move(status, p1, 0, 5)

    assert not success
    assert status[0].progress() == 0


def test_do_move_blocked_out_of_home():
    p1 = Player.get(1)
    piece = Piece(1, 0, 0)
    status = [piece, Piece(0, 0, 15), Piece(0, 1, 15)]

    assert not is_valid_move(piece, 6, status)

    success = do_move(status, p1, 0, 6)

    assert not success
    assert status[0].progress() == 0


def test_do_move_on_path():
    p1 = Player.get(1)
    piece = Piece(0, 0, 16)
    status = [piece, Piece(1, 0, 1)]

    assert is_valid_move(piece, 1, status)

    success = do_move(status, p1, 0, 1)

    assert success
    assert status[0].progress() == 0
    assert status[1].progress() == 2


def test_do_move_blocked_on_path():
    p2 = Player.get(2)
    piece = Piece(2, 0, 28)
    status = [piece, Piece(0, 0, 1), Piece(0, 1, 1)]

    assert not is_valid_move(piece, 1, status)


def test_do_move_on_target():
    p0 = Player.get(0)
    status = [Piece(0, 0, 56), Piece(1, 0, 33)]

    success = do_move(status, p0, 0, 1)

    assert success
    assert status[0].progress() == 57
    assert status[1].progress() == 33


def test_do_move_on_finish():
    p0 = Player.get(0)
    status = [Piece(0, 0, 56)]

    success = do_move(status, p0, 0, 6)

    assert success
    assert status[0].progress() == 62


def test_do_move_cant_finish():
    p0 = Player.get(0)
    status = [Piece(0, 0, 58)]

    success = do_move(status, p0, 0, 6)

    assert not success
    assert status[0].progress() == 58
"""
