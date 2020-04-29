#!/usr/bin/env python3
# coding: utf-8

"""Various utility functions without internal dependencies for the project.
Extracted as a way to reuse in different modules"""

import random

from const import PLAYER_SHIFT, LAST_ON_PATH


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


def progress_to_position(
    player: int,
    position: int,
    player_shift: int = PLAYER_SHIFT,
    last_on_path: int = LAST_ON_PATH,
) -> int:
    """Position of player on board. Shared by all players.
    Used to determine colisions when on common path.
    Return 0 when not in a position where could clash with others
    
    >>> progress_to_position(0, 0)
    0
            
    >>> progress_to_position(3, 57)
    0

    >>> progress_to_position(0, 55)
    55

    >>> progress_to_position(1, 41)
    55

    >>> progress_to_position(2, 27)
    55
            
    >>> progress_to_position(3, 13)
    55
    """
    if position < 1 or position > last_on_path:
        return 0
    progress = player * player_shift + position
    return (progress - 1) % last_on_path + 1
