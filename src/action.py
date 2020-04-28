#!/usr/bin/env python3
# coding: utf-8

"""The player text-based interactions.
This is specific to standalone text-based application.
Web application will use another implementation of this logic."""

from typing import List

from colorama import Fore

from const import PLAYER_COLOURS
from piece import Piece
from player import Player
from util import roll


def roll_dice(player_num: int) -> int:
    """Asks player to roll dice"""
    sides = 6
    player_colour = eval(f"Fore.{PLAYER_COLOURS[player_num]}")
    input(f"{player_colour}{Player.get(player_num)}: Press ENTER to roll your dice")
    num_rolled = roll(sides)
    print("You rolled {}.".format(num_rolled))
    return num_rolled


def ask_move(movable_pieces: List[Piece]) -> int:
    """Ask the player which pawn to move. Returns the index of the piece to move."""
    assert movable_pieces

    player_num: int = movable_pieces[0].player()
    valid_moves = [str(p) for p in movable_pieces]

    while True:
        try:
            player_colour = eval(f"Fore.{PLAYER_COLOURS[player_num]}")
            pawn_symbol = input(
                f"{player_colour}{Player.get(player_num)}: Choose a piece to move [{', '.join(valid_moves)}]: "
            )
        except ValueError:
            continue
        else:
            if pawn_symbol.upper() in valid_moves:
                return ord(pawn_symbol.upper()) - ord("A")
            if not pawn_symbol and len(valid_moves) == 1:
                return ord(valid_moves[0]) - ord("A")


if __name__ == "__main__":
    pass
