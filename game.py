#!/usr/bin/python3

"""The game logic"""

from player import roll_dice


def do_move(player, move):
    """Check if the move is valid. If it is, perform it. Returns whether it is valid."""
    # TODO: Implement
    return True


def choose_first(players):
    """ score index is 0..3, i.e. player-1 (player are 1..4)
    0 means hasn't drawn, -1 means is already out of drawing
    """
    m = 0
    score = [0] * players
    need_more = True
    while need_more:
        for i in range(len(score)):
            if score[i] != -1:
                score[i] = roll_dice(i + 1)
        m = max(score)
        if len([v for v in score if v == m]) > 1:
            for i in range(len(score)):
                if score[i] == m:
                    score[i] = 0
                else:
                    score[i] = -1
        else:
            need_more = False
    first = score.index(m) + 1
    print("Player {} plays first".format(first))
    return first


def check_endgame():
    """Check if any of the players has ended the game."""
    # TODO: Implement
    return True
