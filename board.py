from piece import Piece
from typing import Any, List, Tuple, Dict


class Board:
    def __init__(self, number_of_players: int = 4, number_of_pieces: int = 4):
        self.number_of_players = number_of_players
        self.number_of_pieces = number_of_pieces
        # self.pieces: List[Piece] = [] # TODO generate the initial state of the pieces
        # self.winners: List[int] = []

    def moveForward(self, piece: Piece, positions: int) -> List[int]:
        """
          return the winners after 
        """
        return []

    def winners(self) -> List[int]:
        return []

    def pieces(self) -> List[Piece]:
        return []

    def knocks_out(self, moving: Piece, static: Piece) -> bool:
        return True
