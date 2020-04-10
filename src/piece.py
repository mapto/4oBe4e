from typing import Any

# TODO: Extract to board
PLAYER_SHIFT = 15
END_PROGRESS = 62


class Piece:
    def __init__(
        self, player_number: int, piece_number: int, absolutePosition: int = 0
    ):
        self.piece_number: int = piece_number
        self._player_num: int = player_number
        self._position: int = absolutePosition

    def id(self) -> int:
        return self.piece_number

    def player(self) -> int:
        return self._player_num

    def progress(self) -> int:
        return self._position

    def is_finished(self) -> bool:
        return self.progress() == END_PROGRESS

    def position(self) -> int:
        return self._player_num * PLAYER_SHIFT + self._position

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__
            and self.piece_number == other.piece_number
            and self.player == other.player
        )

    def __str__(self):
        return str(self.id())

    def __repr__(self):
        return str(self.id())

