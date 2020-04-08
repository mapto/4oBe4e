#!/usr/bin/env python3
# coding: utf-8

"""The game logic"""

from typing import Tuple

from player import roll_dice


def do_move(player, move):
    """Check if the move is valid. If it is, perform it. Returns whether it is valid."""
    # TODO: Implement
    return True


def choose_first(players: int) -> int:
    """ score index is 0..3, i.e. player-1 (player are 1..4)
    0 means hasn't drawn, -1 means is already out of drawing
    """
    m = 0
    score = [0] * players
    need_more = True
    while need_more:
        for i in range(len(score)):
            if score[i] != -1:
                score[i] = roll_dice(i + 1)
        m = max(score)
        if len([v for v in score if v == m]) > 1:
            for i in range(len(score)):
                if score[i] == m:
                    score[i] = 0
                else:
                    score[i] = -1
        else:
            need_more = False
    first = score.index(m) + 1
    print("Player {} plays first".format(first))
    return first


def check_endgame():
    """Check if any of the players has ended the game."""
    # TODO: Implement
    return True


def coord_in_home(player: int, piece: int, progress: int) -> Tuple[int, int]:
    """Draw in home positions: each piece has its location. Progress is always same, thus irrelevant"""
    zones = {1: (5,2), 2: (2,12), 3: (12,15), 4: (15,5)}
    shift = {0: (0,0), 1: (0,1), 2:(1,0), 3: (1,1)}
    return (zones[player][0] + shift[piece][0], zones[player][1] + shift[piece][1])


def coord_on_path(player: int, piece: int, progress: int) -> Tuple[int, int]:
    """TODO: draw on path: if two or more pieces on same cell, instead of number,
    draw a placeholder, which does not need to show piece number
    possibly split this in 4 or 8 different cases.
    Parameter piece does't influence logic"""
    return (2, 8)


def coord_on_finish(player: int, piece: int, progress: int) -> Tuple[int, int]:
    """TODO: draw on path: if two or more pieces on same cell, instead of number,
    draw a placeholder, which does not need to show piece number.
    Parameter piece does't influence logic"""
    return (3, 9)


def coord_in_target(player: int, piece: int, progress: int) -> Tuple[int, int]:
    """Draw in target positions: each piece has its location. Progress is always same, thus irrelevant"""
    zones = {1: (7,6), 2: (6,10), 3: (10,11), 4: (11,7)}
    shift = {0: (0,0), 1: (0,1), 2:(1,0), 3: (1,1)}
    return (zones[player][0] + shift[piece][0], zones[player][1] + shift[piece][1])


def put_piece_on_board(player: int, piece: int, progress: int) -> Tuple[int, int]:
    """Currently player is in [1..4], piece is in [0..3]. Do we need to change this?
    TODO: Refactor to implement startegy pattern
    """
    coords = (0, 0)
    if progress == 0:
        coords = coord_in_home(player, piece, progress)
    elif 0 < progress <= 56:
        coords = coord_on_path(player, piece, progress)
    elif 56 < progress <= 61:
        coords = coord_on_finish(player, piece, progress)
    elif progress == 62:
        coords = coord_in_target(player, piece, progress)
    else:
        raise NotImplementedError()

    return coords
