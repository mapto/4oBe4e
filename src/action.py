#!/usr/bin/env python3
# coding: utf-8

"""The player text-based interactions.
This is specific to standalone text-based application.
Web application will use another implementation of this logic."""

from typing import List

from util import roll

from piece import Piece


def roll_dice(player_num: int) -> int:
    """Asks player to roll dice"""
    sides = 6
    input("Player {}: Press ENTER to roll your dice...".format(player_num))
    num_rolled = roll(sides)
    print("You rolled {}.".format(num_rolled))
    return num_rolled


def ask_move(movable_pieces: List[Piece]) -> int:
    """Ask the player which pawn to move. Returns the index of the piece to move."""
    assert movable_pieces

    player_num: int = movable_pieces[0].player()
    valid_moves = [p.id() for p in movable_pieces]

    while True:

        try:
            pawn_number = int(
                input(
                    "Player {}: Choose a piece to move {}: ".format(
                        player_num, valid_moves
                    )
                )
            )
        except ValueError:
            continue
        else:
            if pawn_number in valid_moves:
                break

    return pawn_number


if __name__ == "__main__":
    pass
