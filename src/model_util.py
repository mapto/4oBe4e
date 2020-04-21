#!/usr/bin/env python3
# coding: utf-8

"""Various utility functions depending only on model.
Extracted as a way to reuse in different modules"""

from typing import List

from piece import Piece
from const import LAST_ON_PATH


def __pieces_on_path_position(pieces: List[Piece], path_pos: int) -> List[Piece]:
    """
    >>> __pieces_on_path_position([Piece(1, 0, 1)], 15)
    [0]

    >>> __pieces_on_path_position([Piece(2, 0, 1)], 29)
    [0]

    >>> __pieces_on_path_position([Piece(0, 0, 15), Piece(0, 1, 15)], 15)
    [0, 1]
    """
    return [p for p in pieces if path_pos == p.position()]


def __other_player_pieces(pieces: List[Piece], player_num: int) -> List[Piece]:
    return [p for p in pieces if p.player() != player_num]


def others_on_position(pieces: List[Piece], player: int, pos: int) -> List[Piece]:
    """Do other players block the position by having more than one piece on it.
    Position argument is board position, not piece progress."""
    assert 0 < pos <= LAST_ON_PATH
    at_dest = __pieces_on_path_position(pieces, pos)
    others = __other_player_pieces(at_dest, player)
    return others
