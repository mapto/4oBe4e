#!/usr/bin/env python3
# coding: utf-8

from typing import Any, List, Dict

from colorama import Back, Fore, Style  # type: ignore


from const import HOME_ZONE, LAST_ON_PATH, END_PROGRESS, PLAYER_COLOURS

from piece import Piece
from player import Player
from game import put_piece_on_board


# Define players' board attributes
players: List[Dict[str, Any]] = [
    {
        "colour": PLAYER_COLOURS[0],
        "home": [[5, [2, 3]], [6, [2, 3]]],
        "target": [[7, [6, 7]], [8, [6, 7]]],
        "finish": [[9, [*range(3, 8)]], None],
    },
    {
        "colour": PLAYER_COLOURS[1],
        "home": [[2, [12, 13]], [3, [12, 13]]],
        "target": [[6, [10, 11]], [7, [10, 11]]],
        "finish": [[3, [9]], [4, [9]], [5, [9]], [6, [9]], [7, [9]]],
    },
    {
        "colour": PLAYER_COLOURS[2],
        "home": [[12, [15, 16]], [13, [15, 16]]],
        "target": [[10, [11, 12]], [11, [11, 12]]],
        "finish": [[9, [*range(11, 16)]], None],
    },
    {
        "colour": PLAYER_COLOURS[3],
        "home": [[15, [5, 6]], [16, [5, 6]]],
        "target": [[11, [7, 8]], [12, [7, 8]]],
        "finish": [[11, [9]], [12, [9]], [13, [9]], [14, [9]], [15, [9]]],
    },
]


def _colour(name: str = "WHITE") -> str:
    return eval(f"Fore.{name}")


def draw_board() -> List[List[Any]]:
    """Draw an ASCII board with the current pieces."""

    ROWS = 19
    COLS = 19
    HOME_SHAPE = "[ ]"
    TARGET_SHAPE = "{ }"
    FOOTPATH_SHAPE = "( )"
    FINISH_SHAPE = " + "

    # Init board
    board = [[Style.RESET_ALL + "   "] * COLS for row in range(ROWS)]

    # Fill board frame
    for i in range(len(board)):
        board[i][:: len(board[i]) - 1] = [Fore.MAGENTA + " . ", Fore.MAGENTA + " . "]

    for i in 0, -1:
        board[i][:] = (Fore.CYAN + " . ") * len(board[i])

    # Fill player areas
    for p in players:
        for h in p["home"]:
            for c in h[1]:
                board[h[0]][c] = _colour(p["colour"]) + HOME_SHAPE
        for t in p["target"]:
            for c in t[1]:
                board[t[0]][c] = _colour(p["colour"]) + TARGET_SHAPE
        for f in p["finish"]:
            if f:
                for c in f[1]:
                    board[f[0]][c] = _colour(p["colour"]) + FINISH_SHAPE

    # Fill footpath
    footpath: List[List[List[int]]] = [
        [[2, 16], [8, 9, 10]],
        [[3, 4, 14, 15], [8, 10]],
        [[5, 13], [5, 6, 7, 8, 10, 11, 12, 13]],
        [[6, 7, 11, 12], [5, 13]],
        [[8, 10], [2, 3, 4, 5, 13, 14, 15, 16]],
        [[9], [2, 16]],
    ]

    for fp in footpath:
        for r in fp[0]:
            for c in fp[1]:
                board[r][c] = Fore.WHITE + FOOTPATH_SHAPE

    # Fill Trophies
    board[9][9] = ">|<"
    board[-1][-1] = Style.RESET_ALL + "🏳️‍🌈"

    return board


def _cant_overlap(piece: Piece) -> bool:
    """Even though this is piece-related logic, it has to do only with visualisation.
    Thus in view, rather than object logic"""
    return not (HOME_ZONE < piece.progress() < END_PROGRESS)


def draw_pieces_on_board(
    board: List[List[Any]], pieces: List[Piece]
) -> List[List[Any]]:
    """It is not part of a job of this method to resolve game logic,
    such as collision of pieces of different players on the path"""
    for piece in pieces:
        (x, y) = put_piece_on_board(piece)
        player_progress = [p.progress() for p in pieces if p.player() == piece.player()]
        count = player_progress.count(piece.progress())
        val = str(piece) if _cant_overlap(piece) or count == 1 else str(count)
        board[x][y] = f"{_colour(players[piece.player()]['colour'])}.{val}."

    return board


def end_game(status: List[Piece], winner: Player) -> None:
    """Celebrate the winning player."""
    redraw(status)
    print("{:s} has won!".format(winner))


def redraw(status: List[Piece]) -> None:
    """The screen update function. Do not modify this for now."""

    board = draw_board()
    draw_pieces_on_board(board, status)

    print()
    for row in board:
        print("".join(row))
