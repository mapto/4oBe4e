from state import GameAction, RollDice, MovePiece, GameState

from piece import Piece
from board import Board
from player import Player


class GameEngine:
    def __init__(self, _board: Board):
        self.board = _board
