#!/usr/bin/env python3
# coding: utf-8

"""The main standalone application for github.com/mapto/4oBe4e"""

# standard
from typing import Any, List

# local
from piece import Piece
from board import Board
from player import Player
from game import check_endgame, choose_first, do_move
from action import ask_move, roll_dice
from console_view import redraw, end_game


def play(players: int, first_player: Player) -> None:
    board = Board()
    status = board.pieces()

    next = first_player.number
    win = False
    while not win:
        redraw(status)
        dice = roll_dice(next)

        valid = False
        while not valid:
            move = ask_move(next)
            valid = do_move(status, next, move)

        win = check_endgame()
        if not win and dice != 6:
            next = ((next + 1) % players) + 1

    end_game(status, next)


def main(num_players: int) -> None:
    """The main game loop"""
    for i in range(num_players):
        Player.create()

    player = choose_first(Player.players)
    print()
    print("Player {} plays first!".format(player))

    play(num_players, player)


if __name__ == "__main__":
    main(num_players=4)