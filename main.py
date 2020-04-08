#!/usr/bin/env python3
# coding: utf-8

"""The main standalone application for github.com/mapto/4oBe4e"""

# standard
from typing import Any, List, Tuple, Dict

# external
from colorama import Back, Fore, Style  # type: ignore


# local
from game import check_endgame, choose_first, do_move, put_piece_on_board
from action import ask_move, roll_dice

players = 4

status = {1: [0] * 4, 2: [0] * 4, 3: [0] * 4, 4: [0] * 4}


def draw_board() -> List[List[Any]]:
    """ Draw an ASCII board with the current pieces.
    """

    # TODO (@vkantsev): Discuss how to add the pieces with their current positions

    ROWS = 19
    COLS = 19
    HOME_SHAPE = "[ ]"
    TARGET_SHAPE = "{ }"
    FOOTPATH_SHAPE = "( )"
    FINISH_SHAPE = " @ "

    # Init board
    board = [[Style.RESET_ALL + "   "] * COLS for row in range(ROWS)]

    # Define players' board attributes
    players: List[Dict[str, Any]] = [
        {
            "colour": "RED",
            "home": [[5, [2, 3]], [6, [2, 3]]],
            "target": [[7, [6, 7]], [8, [6, 7]]],
            "finish": [[9, [*range(3, 8)]], None],
        },
        {
            "colour": "BLUE",
            "home": [[2, [12, 13]], [3, [12, 13]]],
            "target": [[6, [10, 11]], [7, [10, 11]]],
            "finish": [[3, [9]], [4, [9]], [5, [9]], [6, [9]], [7, [9]]],
        },
        {
            "colour": "GREEN",
            "home": [[12, [15, 16]], [13, [15, 16]]],
            "target": [[10, [11, 12]], [11, [11, 12]]],
            "finish": [[9, [*range(11, 16)]], None],
        },
        {
            "colour": "YELLOW",
            "home": [[15, [5, 6]], [16, [5, 6]]],
            "target": [[11, [7, 8]], [12, [7, 8]]],
            "finish": [[11, [9]], [12, [9]], [13, [9]], [14, [9]], [15, [9]]],
        },
    ]

    # Fill board frame
    for i in range(len(board)):
        board[i][:: len(board[i]) - 1] = [Fore.MAGENTA + " . ", Fore.MAGENTA + " . "]

    for i in 0, -1:
        board[i][:] = (Fore.CYAN + " . ") * len(board[i])

    # Fill player areas
    for p in players:
        for h in p["home"]:
            for c in h[1]:
                board[h[0]][c] = eval(f"Fore.{p['colour']}") + HOME_SHAPE
        for t in p["target"]:
            for c in t[1]:
                board[t[0]][c] = eval(f"Fore.{p['colour']}") + TARGET_SHAPE
        for f in p["finish"]:
            if f:
                for c in f[1]:
                    board[f[0]][c] = eval(f"Fore.{p['colour']}") + FINISH_SHAPE

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


def draw_pieces_on_board(
    board: List[List[Any]], status: Dict[int, List[int]]
) -> List[List[Any]]:
    """ It is not part of a job of this method to resolve game logic,
    such as collision of pieces of different players on the path"""
    for player in range(1, 5):
        for piece in range(4):
            (x, y) = put_piece_on_board(player, piece, status[player][piece])
            # TODO: Draw the piece on the board properly
            # If there's already another piece, indicate this with another symbol for collision
            board[x][y] = "." + str(piece) + "."

    return board


def redraw() -> None:
    """The screen update function. Do not modify this for now."""

    board = draw_board()
    draw_pieces_on_board(board, status)

    print()
    for row in board:
        print("".join(row))


def end_game(winner: int) -> None:
    """Celebrate the winning player."""

    redraw()
    print("Player {:d} has won!".format(winner))


def start(players: int, board: List[List[Any]]) -> None:
    """The main game loop"""

    player = choose_first(players)
    print()
    print("Player {} plays first!".format(player))

    win = False
    while not win:
        redraw()
        dice = roll_dice(player)

        valid = False
        while not valid:
            move = ask_move(player)
            valid = do_move(player, move)

        win = check_endgame()
        if not win and dice != 6:
            player = ((player + 1) % players) + 1

    end_game(player)


if __name__ == "__main__":
    start(players, draw_board())
