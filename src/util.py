#!/usr/bin/env python3
# coding: utf-8

"""Various utility functions without internal dependencies for the project.
Extracted as a way to reuse in different modules"""

import random


def roll(sides: int = 6) -> int:
    """Rolls a dice: randomly generate a value, based on a dice.
    Default dice has 6 sides, but other dice are also supported.

    >>> result = roll(); 1 <= result <= 6
    True

    >>> roll(1)
    1

    >>> result = roll(20); 1 <= result <= 20
    True
    """
    num_rolled = random.randint(1, sides)
    return num_rolled
