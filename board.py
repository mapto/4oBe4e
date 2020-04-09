from typing import List

from piece import Piece


class Board:
    def __init__(self, number_players: int = 4, numberOfPieces: int = 4):
        self._pieces: List[Piece] = []
        for player in range(1, number_players + 1):
            for piece in range(numberOfPieces):
                self._pieces.append(Piece(player, piece))
        self._winners: List[int] = []

    def moveForward(self, p: Piece, positions: int) -> List[int]:
        # TODO redundancy/duplicate with game.do_move.
        # @mapto proposes that this class is kept only as a model and logic is external to it
        return []

    def winners(self) -> List[int]:
        return self._winners

    def pieces(self) -> List[Piece]:
        return self._pieces
