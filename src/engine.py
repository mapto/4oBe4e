from state import GameAction, RollDice, MovePiece, GameState

from piece import Piece
from board import Board
from player import Player


class GameEngine:
    def __init__(self, _board: Board):
        self.state = GameState(board)

    def get_state(self) -> GameState:
        return self.state

    def apply(self, action: GameAction) -> GameEngine:
        if actioin not in self.state.valid_actions:
            raise ValueError(f'Illegal action {action} is not one of {self.valid_actions}')
        self.valid_action
        return self
