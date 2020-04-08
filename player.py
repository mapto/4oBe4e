#!/usr/bin/env python3
# coding: utf-8

"""The player text-based interactions.
This is specific to standalone text-based application.
Web application will use another implementation of this logic."""

from util import roll


def roll_dice(player: int) -> int:
    """Asks player to roll dice"""
    sides = 6
    roll_again = input("Играч {}: Хвърли зара = ENTER ".format(player))
    num_rolled = roll(sides)
    print("Ти хвърли ", num_rolled)
    return num_rolled


def ask_move(player: int) -> int:
    """Ask the player which pawn to move. Returns an integer between 0 and 3."""

    while True:

        try:
            pawn_number = int(input(f"Player {player} choose a pawn to move (0-3): "))
        except ValueError:
            continue
        else:
            if 0 <= pawn_number <= 3:
                break

    return pawn_number


if __name__ == "__main__":
    pass
