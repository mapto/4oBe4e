#!/usr/bin/env python3
# coding: utf-8

from typing import Any

from const import END_PROGRESS
from util import progress_to_position


class Piece:
    def __init__(self, player_number: int, piece_number: int, progress: int = 0):
        self.piece_number: int = piece_number
        self.__player_num: int = player_number
        self.__progress: int = progress

    def move(self, move: int) -> None:
        self.__progress += move

    def send_home(self) -> None:
        self.__progress = 0

    def index(self) -> int:
        return self.piece_number

    def player(self) -> int:
        return self.__player_num

    def progress(self) -> int:
        """Progress of player relative to start position. Unique for each player.
        Normally always incremental (see move()).
        Only exception is when hit by another player (see send_home())"""
        return self.__progress

    def is_finished(self) -> bool:
        """
        >>> p = Piece(0, 0, 62); p.is_finished()
        True

        >>> p = Piece(1, 1, 61); p.is_finished()
        False

        >>> p = Piece(2, 2); p.is_finished()
        False

        >>> p = Piece(1,0,28); p.is_finished()
        False
        """
        return self.progress() == END_PROGRESS

    def position(self) -> int:
        """Position of player on board. Shared by pieces of all players.
        Used to determine colisions when on common path.
        Return 0 when not in a position where could clash with others.
        
        >>> p = Piece(0, 0); p.position()
        0
                
        >>> p = Piece(3, 0, 57); p.position()
        0

        >>> p = Piece(0, 0, 55); p.position()
        55

        >>> p = Piece(1, 0, 41); p.position()
        55

        >>> p = Piece(2, 0, 27); p.position()
        55
                
        >>> p = Piece(3, 0, 13); p.position()
        55
        """
        return progress_to_position(self.__player_num, self.__progress)

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
