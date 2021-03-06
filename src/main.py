#!/usr/bin/env python3
# coding: utf-8

"""The main standalone application for github.com/mapto/4oBe4e"""

# standard
from typing import Any, List

from colorama import Style  # type: ignore

# local
from const import NUMBER_OF_PLAYERS, NUMBER_OF_PIECES
from piece import Piece
from player import Player
from game import check_endgame, choose_first, do_move, get_valid_moves, set_board
from action import ask_move, roll_dice
from console_view import redraw, end_game


def play(num_players: int, num_pieces: int, first_player: Player) -> None:
    status = set_board(num_players, num_pieces)

    next = first_player.number
    win = False
    while not win:
        redraw(status)
        dice = roll_dice(next)
        player = Player.get(next)
        valid_moves = get_valid_moves(player, dice, status)
        valid = not valid_moves
        while not valid:
            piece_to_move = ask_move(valid_moves)
            valid = do_move(status, player, piece_to_move, dice)

        win = check_endgame(status)
        if not win and dice != 6:
            next = (next + 1) % num_players

    end_game(status, player)


def main(num_players: int, num_pieces: int) -> None:
    """The main game loop"""
    for _ in range(num_players):
        Player.create()

    player = choose_first(Player.players)
    print()
    print(f"{Style.RESET_ALL}{player:s} plays first!")

    play(num_players, num_pieces, player)


if __name__ == "__main__":
    main(NUMBER_OF_PLAYERS, NUMBER_OF_PIECES)
