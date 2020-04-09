class Piece:
    def __init__(self, player: int, piece_number: int, absolutePosition: int = 0):
        self.piece_number: int = piece_number
        self._player: int = player
        self.absolutePosition: int = absolutePosition
        self.position: int = absolutePosition  # TODO?

    def id(self) -> int:
        return self.piece_number

    def player(self) -> int:
        return self._player

    def progress(self) -> int:
        return self.position
