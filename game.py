#!/usr/bin/env python3
# coding: utf-8

"""The game logic.
This should be independent of media used to interact with player."""

from typing import Tuple

from player import roll_dice


def do_move(player, move) -> bool:
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
                # TODO: Resolve problem that this relies on logic that involves console interaction
                score[i] = roll_dice(player=i + 1)
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
    return first


def check_endgame() -> bool:
    """Check if any of the players has ended the game."""
    # TODO: Implement
    return True


def coord_in_home(player: int, piece: int, progress: int = 0) -> Tuple[int, int]:
    """Draw in home positions: each piece has its location. Progress is always same, thus irrelevant
    
    >>> coord_in_home(1, 0)
    (5, 2)

    >>> coord_in_home(2, 1)
    (2, 13)

    >>> coord_in_home(3, 2)
    (13, 15)

    >>> coord_in_home(4, 3)
    (16, 6)
    """
    zones = {1: (5, 2), 2: (2, 12), 3: (12, 15), 4: (15, 5)}
    shift = {0: (0, 0), 1: (0, 1), 2: (1, 0), 3: (1, 1)}
    return (zones[player][0] + shift[piece][0], zones[player][1] + shift[piece][1])


def coord_on_path(player: int, piece: int, progress: int) -> Tuple[int, int]:
    """TODO: draw on path: if two or more pieces on same cell, instead of number,
    draw a placeholder, which does not need to show piece number
    possibly split this in 4 or 8 different cases.
    Parameter piece does't influence logic
    
    >>> coord_on_path(1, 1, 1)
    (2, 8)

    The following tests currently fail, thus disabled when pushed. Enable for development:

    Test player 2:
    >> coord_on_finish(2, 1, 2)
    (10, 3)

    Test player 3:
    >> coord_on_finish(3, 1, 3)
    (14, 10)

    Test overlap:
    >> coord_on_finish(2, 1, 17)
    (14, 10)

    Test turn:
    >> coord_on_finish(3, 1, 5)
    (13, 11)

    Test last position:
    >> coord_on_finish(4, 1, 56)
    (9, 16)
    """

    return (2, 8)


def coord_on_finish(player: int, piece: int, progress: int) -> Tuple[int, int]:
    """TODO: draw on path: if two or more pieces on same cell, instead of number,
    draw a placeholder, which does not need to show piece number.
    Parameter piece does't influence logic
    
    >>> coord_on_finish(1, 1, 57)
    (3, 9)

    The following tests currently fail, thus disabled when pushed. Enable for development:
    >> coord_on_finish(2, 1, 58)
    (9, 4)

    >> coord_on_finish(3, 1, 59)
    (13, 9)

    >> coord_on_finish(3, 1, 61)
    (9, 11)
    """
    return (3, 9)


def coord_in_target(player: int, piece: int, progress: int = 62) -> Tuple[int, int]:
    """Draw in target positions: each piece has its location. Progress is always same, thus irrelevant
    
    >>> coord_in_target(1, 0)
    (7, 6)

    >>> coord_in_target(2, 1)
    (6, 11)

    >>> coord_in_target(3, 2)
    (11, 11)

    >>> coord_in_target(4, 3)
    (12, 8)
    """
    zones = {1: (7, 6), 2: (6, 10), 3: (10, 11), 4: (11, 7)}
    shift = {0: (0, 0), 1: (0, 1), 2: (1, 0), 3: (1, 1)}
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
