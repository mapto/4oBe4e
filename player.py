#!/usr/bin/python3

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


def ask_move(player):
    """Asks player which of his four pieces they want to move. Returns the piece index between 0 and 3.
    @lankata can do this
    """
    x = int(input("Please choose a pawn: "))

    # Please enter an integer: 42
    if x <= 1:
        x = 1

        return "ONE"
    elif x == 2:
        return "TWO"
    elif x == 3:
        return "THREE"
    else:
        return "FOUR"
