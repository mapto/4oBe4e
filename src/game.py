#!/usr/bin/env python3
# coding: utf-8

"""The game logic.
This should be independent of media used to interact with player."""

from typing import Tuple, List, Set, Dict


from piece import Piece
from player import Player
from action import roll_dice

# TODO: Extract to board
LAST_ON_PATH = 14 * 4
END_PROGRESS = LAST_ON_PATH + 6


def do_move(status: List[Piece], player: Player, piece_to_move: int, dice: int) -> bool:
    """Check if the move is valid. If it is, perform it. Returns whether it is valid."""
    movable_piece_nums = [p.index() for p in get_valid_moves(player, dice, status)]
    if not (piece_to_move in movable_piece_nums):
        return False

    current = [
        p for p in status if p.player() == player.number and p.index() == piece_to_move
    ]
    assert len(current) == 1
    piece = current[0]
    if piece.progress() == 0:
        if dice == 6:
            piece.move(1)
        else:
            raise ValueError("Home can only be left with a full dice")
    else:
        piece.move(dice)
        if 0 < piece.progress() <= LAST_ON_PATH:
            others = [
                o
                for o in status
                if o.player() != player.number and piece.position() == o.position()
            ]
            for other in others:
                other.send_home()
    return True


def choose_first(players: Set[Player]) -> Player:
    """ score 0 means player hasn't drawn, -1 means is already out of drawing
    """
    m = 0
    score = [0] * len(players)
    need_more = True
    while need_more:
        for i in range(len(score)):
            if score[i] != -1:
                # TODO: Resolve problem that this relies on logic that involves console interaction
                score[i] = roll_dice(player_num=i)
        m = max(score)
        if len([v for v in score if v == m]) > 1:
            for i in range(len(score)):
                score[i] = 0 if score[i] == m else -1
        else:
            need_more = False
    return Player.get(score.index(m))


def check_endgame(status: List[Piece]) -> bool:
    """Check if any of the players has ended the game.
    
    >>> check_endgame([Piece(0, 0),Piece(0, 1),Piece(0, 2),Piece(0, 3),\
        Piece(1, 0),Piece(1, 1),Piece(1, 2),Piece(1, 3),\
        Piece(2, 0),Piece(2, 1),Piece(2, 2),Piece(2, 3),\
        Piece(3, 0),Piece(3, 1),Piece(3, 2),Piece(3, 3)])
    False
    
    >>> check_endgame([Piece(0, 0),Piece(0, 1),Piece(0, 2),Piece(0, 3),\
        Piece(1, 0),Piece(1, 1),Piece(1, 2),Piece(1, 3),\
        Piece(2, 0),Piece(2, 1),Piece(2, 2),Piece(2, 3),\
        Piece(3, 0, 62),Piece(3, 1, 62),Piece(3, 2, 62),Piece(3, 3, 62)])
    True
    
    >>> check_endgame([Piece(0, 0),Piece(0, 1),Piece(0, 2),Piece(0, 3),\
        Piece(1, 0, 62),Piece(1, 1, 62),Piece(1, 2, 62),Piece(1, 3, 61),\
        Piece(2, 0, 60),Piece(2, 1, 60),Piece(2, 2, 60),Piece(2, 3, 60),\
        Piece(3, 0, 10),Piece(3, 1, 20),Piece(3, 2, 30),Piece(3, 3, 40)])
    False
    """
    player_finished: Dict[int, bool] = {}
    for piece in status:
        player = piece.player()
        if player in player_finished:
            player_finished[player] = player_finished[player] and piece.is_finished()
        else:
            player_finished[player] = True

    return len([k for k, v in player_finished.items() if v]) > 0


def coord_in_home(piece: Piece) -> Tuple[int, int]:
    """Draw in home positions: each piece has its location. Progress is always same, thus irrelevant
    
    >>> coord_in_home(Piece(0, 0))
    (5, 2)

    >>> coord_in_home(Piece(1, 1))
    (2, 13)

    >>> coord_in_home(Piece(2, 2))
    (13, 15)

    >>> coord_in_home(Piece(3, 3))
    (16, 6)
    """
    assert piece.progress() == 0

    zones = [(5, 2), (2, 12), (12, 15), (15, 5)]
    shift = [(0, 0), (0, 1), (1, 0), (1, 1)]

    return (
        zones[piece.player()][0] + shift[piece.index()][0],
        zones[piece.player()][1] + shift[piece.index()][1],
    )


def coord_on_path(piece: Piece) -> Tuple[int, int]:
    """Draws on path: if two or more pieces on same cell, instead of number,
    draws a placeholder, which does not need to show piece number
    Logic split this in 4 different cases, determined by player offset.
    Parameter piece does't influence logic.

    Player (absolute) Progress to (relative) Position conversion:
        P0     1..56: (pos)
        P1     1..42: (p_num * shift + pos)
              43..56: (p_num * shift + pos) % end_progress
        P2     1..28: (p_num * shift + pos)
              29..56: (p_num * shift + pos) % end_progress
        P3     1..14: (p_num * shift + pos)
              15..56: (p_num * shift + pos) % end_progress


    Test player 1:
    >>> coord_on_path(Piece(0, 1, 1))
    (8, 2)

    Test player 2:
    >>> coord_on_path(Piece(1, 1, 1))
    (2, 10)

    Test player 3:
    >>> coord_on_path(Piece(2, 1, 1))
    (10, 16)

    Test player 4:
    >>> coord_on_path(Piece(3, 1, 1))
    (16, 8)

    Test path wrap:
    >>> coord_on_path(Piece(3, 1, 56))
    (16, 9)

    Test overlap:
    >> coord_on_path(Piece(2, 1, 17))
    (10, 14)
    """

    assert 1 <= piece.progress() <= LAST_ON_PATH and 0 <= piece.player() <= 3

    POSITION_TO_ROWCOL: Tuple[Tuple[int, int], ...] = (
        (0, 0),
        (8, 2),
        (8, 3),
        (8, 4),
        (8, 5),
        (7, 5),
        (6, 5),
        (5, 5),
        (5, 6),
        (5, 7),
        (5, 8),
        (4, 8),
        (3, 8),
        (2, 8),
        (2, 9),
        (2, 10),
        (3, 10),
        (4, 10),
        (5, 10),
        (5, 11),
        (5, 12),
        (5, 13),
        (6, 13),
        (7, 13),
        (8, 13),
        (8, 14),
        (8, 15),
        (8, 16),
        (9, 16),
        (10, 16),
        (10, 15),
        (10, 14),
        (10, 13),
        (11, 13),
        (12, 13),
        (13, 13),
        (13, 12),
        (13, 11),
        (13, 10),
        (14, 10),
        (15, 10),
        (16, 10),
        (16, 9),
        (16, 8),
        (15, 8),
        (14, 8),
        (13, 8),
        (13, 7),
        (13, 6),
        (13, 5),
        (12, 5),
        (11, 5),
        (10, 5),
        (10, 4),
        (10, 3),
        (10, 2),
        (9, 2),
    )

    return POSITION_TO_ROWCOL[piece.position()]


def coord_on_finish(piece: Piece) -> Tuple[int, int]:
    """TODO: draw on path: if two or more pieces on same cell, instead of number,
    draw a placeholder, which does not need to show piece number.
    Parameter piece does't influence logic
    
    >>> coord_on_finish(Piece(1, 1, 57))
    (9, 3)

    The following tests currently fail, thus disabled when pushed. Enable for development:
    >>> coord_on_finish(Piece(2, 1, 58))
    (4, 9)

    >>> coord_on_finish(Piece(3, 1, 59))
    (9, 13)

    >>> coord_on_finish(Piece(3, 1, 61))
    (9, 11)

    >>> coord_on_finish(Piece(4, 1, 57))
    (15, 9)

    >>> coord_on_finish(Piece(4, 1, 61))
    (11, 9)
    """
    pos = piece.progress() - LAST_ON_PATH
    assert 0 < pos < 6

    player = piece.player()
    (x, y) = (0, 0)

    if player in [1, 3]:
        x = 9
        y = pos + 2 if player == 1 else 15 - (pos - 1)
    elif player in [2, 4]:
        x = pos + 2 if player == 2 else 15 - (pos - 1)
        y = 9
    else:
        raise NotImplementedError()

    return (x, y)


def coord_in_target(piece: Piece) -> Tuple[int, int]:
    """Draw in target positions: each piece has its location. Progress is always same, thus irrelevant
    
    >>> coord_in_target(Piece(0, 0, 62))
    (7, 6)

    >>> coord_in_target(Piece(1, 1, 62))
    (6, 11)

    >>> coord_in_target(Piece(2, 2, 62))
    (11, 11)

    >>> coord_in_target(Piece(3, 3, 62))
    (12, 8)
    """
    assert piece.progress() == 62

    zones = [(7, 6), (6, 10), (10, 11), (11, 7)]
    shift = [(0, 0), (0, 1), (1, 0), (1, 1)]

    return (
        zones[piece.player()][0] + shift[piece.index()][0],
        zones[piece.player()][1] + shift[piece.index()][1],
    )


def put_piece_on_board(piece: Piece) -> Tuple[int, int]:
    """Currently player is in [1..4], piece is in [0..3]. Do we need to change this?
    TODO: Refactor to implement startegy pattern
    """
    coords = (0, 0)
    progress = piece.progress()
    if progress == 0:
        coords = coord_in_home(piece)
    elif 0 < progress <= LAST_ON_PATH:
        coords = coord_on_path(piece)
    elif LAST_ON_PATH < progress < END_PROGRESS:
        coords = coord_on_finish(piece)
    elif progress == END_PROGRESS:
        coords = coord_in_target(piece)
    else:
        raise NotImplementedError()

    return coords


def is_valid_move(piece: Piece, dice: int, status: List[Piece]) -> bool:
    """
    >>> p = Piece(1, 1); is_valid_move(p, 6, [p])
    True

    >>> p = Piece(1, 1); is_valid_move(p, 1, [p])
    False

    >>> p = Piece(1, 1, 1); is_valid_move(p, 1, [p])
    True

    >>> p = Piece(1, 1, 1); is_valid_move(p, 6, [p])
    True

    """
    if 0 == dice:
        raise ValueError("Invalid dice: {}".format(dice))

    pos = piece.progress()
    if pos == 0:
        return dice == 6
    if 0 < pos <= LAST_ON_PATH:
        at_dest = [
            p
            for p in status
            if piece.position() == p.position() and piece.player() != p.player()
        ]
        return 2 > len(at_dest)
    if LAST_ON_PATH < pos < END_PROGRESS:
        return pos + dice <= END_PROGRESS

    assert pos == END_PROGRESS
    return False


def get_valid_moves(player: Player, dice: int, status: List[Piece]) -> List[Piece]:
    """
    >>> p = Player.create(); p2 = Player.create(); p = Player.get(0)
    >>> get_valid_moves(p, 6, [Piece(0, 0), Piece(0, 1), Piece(1, 0), Piece(1, 1)])
    [0, 1]

    >>> get_valid_moves(p, 1, [Piece(0, 0), Piece(0, 1), Piece(0, 2), Piece(1, 0)])
    []

    >>> get_valid_moves(p, 1, [Piece(0, 0, 1), Piece(0, 1), Piece(0, 2), Piece(1, 0)])
    [0]

    >>> get_valid_moves(p, 1, [Piece(0, 0, 1), Piece(0, 1, 57), Piece(0, 2), Piece(1, 0)])
    [0, 1]

    >>> get_valid_moves(p, 6, [Piece(0, 0, 1), Piece(0, 1, 60), Piece(0, 2), Piece(0, 3, 0)])
    [0, 2, 3]
    """
    own = [p for p in status if p.player() == player.number]
    return [p for p in own if is_valid_move(p, dice, status)]
