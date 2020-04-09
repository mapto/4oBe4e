#!/usr/bin/env python3
# coding: utf-8

"""The main standalone application for github.com/mapto/4oBe4e"""

# standard
from typing import Any, List

# local
from piece import Piece
from board import Board
from game import check_endgame, choose_first, do_move
from action import ask_move, roll_dice
from console_view import redraw, draw_board

players = 4

board = Board()
status = board.pieces()


def end_game(winner: int) -> None:
    """Celebrate the winning player."""

    redraw(status)
    print("Player {:d} has won!".format(winner))


def start(players: int, board: List[List[Any]]) -> None:
    """The main game loop"""

    player = choose_first(players)
    print()
    print("Player {} plays first!".format(player))

    win = False
    while not win:
        redraw(status)
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
