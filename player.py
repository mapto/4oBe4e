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

    >>> result = roll(); 0 < result and result < 7
    True
    """
    num_rolled = random.randint(1, sides)
    return num_rolled


def ask_move(player: int) -> int:
    """Ask player which pawn to move."""

    while True:

        try:
            pawn_number = int(input(f"Player {player} choose a pawn to move (0-3): "))
        except ValueError:
            continue
        else:
            if not (0 <= pawn_number <= 3):
                continue
            else:
                break

    return pawn_number
