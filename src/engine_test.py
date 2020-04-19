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
    # Given
    board = Board.create(players=[0, 2], pieces_per_player=1)
    state = GameState.create(board)
    dice = Dice()
    monkeypatch.setattr(dice, "roll", lambda: 6)
    game = GameEngine(board, dice)

    # When
    new_state = game.play(GameMove.roll_dice(player=0))

    # Then
    # assert new_state == game.get_state()
    assert new_state.number == 1
    assert new_state.dice == 6
    assert new_state.valid_actions == [
        GameMove.piece_out(player=0, piece=0, dice=6),
    ]

    new_state = game.play(GameMove.piece_out(player=0, piece=0, dice=6))

    assert new_state.current_player == 0
    assert new_state.dice == 6
    assert new_state.board.pieces == [
        Piece(number=0, player=0, position=1),
        Piece(number=0, player=2, position=0),
    ]
    assert new_state.valid_actions == [GameMove.roll_dice(player=0)]


# TODO write tests for playing the game to completion from 2 players without knock outs
