from typing import Any


class Piece:
    def __init__(self, pience_number: int, player: int, absolutePosition: int):
        self.piece_number: int = pience_number
        self.player: int = player
        self.absolutePosition: int = absolutePosition
        self.position: int = 0

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__
            and self.piece_number == other.piece_number
            and self.player == other.player
        )
