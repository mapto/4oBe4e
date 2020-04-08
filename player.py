#!/usr/bin/env python3
# coding: utf-8

"""The player interactions"""

import random


def roll_dice(player):
    """Asks player to roll dice"""
    sides = 6
    num_rolled = random.randint(1, sides)
    roll_again = input("Играч {}: Хвърли зара = ENTER ".format(player))
    if roll_again.lower() != "q":
        num_rolled = roll(sides)
        print("Ти хвърли ", num_rolled)

    print("Играй твоя зар!")
    return num_rolled


def roll(sides: int = 6) -> int:
    """Rolls a dice: randomly generate a value between 1 and 6.

    >>> result = roll(); 1 <= result <= 6
    True
    """
    num_rolled = random.randint(1, sides)
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
