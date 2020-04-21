from dataclasses import dataclass
from typing import List

from piece import Piece


class Board:
    def __init__(self, number_players: int = 4, number_of_pieces: int = 4):
        self._pieces: List[Piece] = []
        for player in range(number_players):
            for piece in range(number_of_pieces):
                self._pieces.append(Piece(player, piece))

    def moveForward(self, piece: Piece, positions: int) -> List[int]:
        """
          return the winners after 
        """
        # TODO redundancy/duplicate with game.do_move.
        # @mapto proposes that this class is kept only as a model and logic is external to it
        return []

    def winners(self) -> List[int]:
        return []

    def pieces(self) -> List[Piece]:
        return self._pieces

    def knocks_out(self, moving: Piece, static: Piece) -> bool:
        return True
