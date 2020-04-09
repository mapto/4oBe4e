from typing import List

from piece import Piece


class Board:
    def __init__(self, number_players: int = 4, numberOfPieces: int = 4):
        self._pieces: List[Piece] = []
        for player in range(1, number_players + 1):
            for piece in range(numberOfPieces):
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
