from typing import Any

# TODO: Extract to board
PLAYER_SHIFT = 14
LAST_ON_PATH = PLAYER_SHIFT * 4
END_PROGRESS = LAST_ON_PATH + 6

OUT_OF_CLASH = -1


class Piece:
    def __init__(self, player_number: int, piece_number: int, position: int = 0):
        self.piece_number: int = piece_number
        self.__player_num: int = player_number
        self.__position: int = position

    def move(self, move: int) -> None:
        self.__position += move

    def send_home(self) -> None:
        self.__position = 0

    def index(self) -> int:
        return self.piece_number

    def player(self) -> int:
        return self.__player_num

    def progress(self) -> int:
        """Progress of player relative to start position. Unique for each player"""
        return self.__position

    def is_finished(self) -> bool:
        """
        >>> p = Piece(0, 0, 62); p.is_finished()
        True

        >>> p = Piece(1, 1, 61); p.is_finished()
        False

        >>> p = Piece(2, 2); p.is_finished()
        False
        """
        return self.progress() == END_PROGRESS

    def position(self) -> int:
        """Position of player on board. On path is common for all players
        
        >>> p = Piece(0, 0); p.position()
        -1
                
        >>> p = Piece(3, 0, 57); p.position()
        -1

        >>> p = Piece(0, 0, 55); p.position()
        55

        >>> p = Piece(1, 0, 41); p.position()
        55

        >>> p = Piece(2, 0, 27); p.position()
        55
                
        >>> p = Piece(3, 0, 13); p.position()
        55
        """
        if self.__position < 1 or self.__position > LAST_ON_PATH:
            return OUT_OF_CLASH
        return (
            self.__player_num * PLAYER_SHIFT + self.__position - 1
        ) % LAST_ON_PATH + 1

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Piece):
            return self.player() == other.player() and self.index() == other.index()
        return False

    def __str__(self):
        return str(chr(ord("A") + self.piece_number))

    def __int__(self):
        return self.index()

    def __repr__(self):
        return str(self.index())

    def __format__(self, format):
        if format == "s":
            return str(self)
        if format == "d":
            return int(self)
        return str(self.index())
