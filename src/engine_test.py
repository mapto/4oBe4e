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

def test_knock_out_single_piece(monkeypatch):
    # Given we have started the game and player 0 piece 0 is on the path
    board = Board.create(players=[0, 2], pieces_per_player=1)
    state = GameState.create(board)
    dice = Dice()
    monkeypatch.setattr(dice, "roll", lambda: 5)
    game = GameEngine(board, dice)

    state.board.pieces[0].position = 5
    state.board.pieces[1].position = 30
    state.current_player = 2

    # When player 2 rolls the dice with 5 which is exactly how much he
    # needs to hit player's 0 0 piece
    new_state = game.play(GameMove.roll_dice(player=2))

    # Then the piece should not go to the goal and it should be the
    # next player turn
    assert new_state == game.get_state()
    assert new_state.number == 1
    assert new_state.dice == 5
    assert new_state.valid_actions == [
        GameMove.move_piece(player=2, piece=0, dice=5),
    ]

    # When player 2 plays it's only possible move
    new_state = game.play(GameMove.move_piece(player=2, piece=0, dice=5))

    # Then hist piece should go to the new possition
    # And should knock out plaers 0 piece 0
    assert new_state.board.pieces == [
        Piece(number=0, player=0, position=0),
        Piece(number=0, player=2, position=35),
    ]
    # And it should be players 0 turn to roll the dice
    assert new_state.valid_actions == [
        GameMove.roll_dice(player=0),
    ]
    assert new_state.winners == []