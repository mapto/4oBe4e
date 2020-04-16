import pytest  # type: ignore
from state import Board, Piece, PieceOut, GameState, RollDice
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
        game.play(PieceOut(1, 1, 6))

    # When we try to play valid action for an invalid Player
    with pytest.raises(Exception):
        game.play(RollDice(player=3))


def test_play_roll_dice_6(monkeypatch):
    # Given
    board = Board.create(players=[1, 3])
    state = GameState.create(board)
    dice = Dice()
    monkeypatch.setattr(dice, "roll", lambda: 6)
    game = GameEngine(board, dice)

    # When
    new_state = game.play(RollDice(player=1))

    # Then
    assert new_state == game.get_state()
    assert new_state.dice == 6
    assert new_state.valid_actions == [
      PieceOut(player=1, piece=Piece(0, 1, 0), dice=6),
      PieceOut(player=1, piece=Piece(1, 1, 0), dice=6),
      PieceOut(player=1, piece=Piece(2, 1, 0), dice=6),
      PieceOut(player=1, piece=Piece(3, 1, 0), dice=6),
    ]

def test_play_roll_dice_3(monkeypatch):
    # Given
    board = Board.create(players=[1, 3])
    state = GameState.create(board)
    dice = Dice()
    monkeypatch.setattr(dice, "roll", lambda: 3)
    game = GameEngine(board, dice)

    # When
    new_state = game.play(RollDice(player=1))

    # Then
    assert new_state == game.get_state()
    assert new_state.dice == 3
    assert new_state.valid_actions == [RollDice(player=3)]

# TODO write tests for playing the game to completion from 2 players without knock outs
