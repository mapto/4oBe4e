#!/usr/bin/python3

"""The main standalone application for github.com/mapto/4oBe4e"""

from player import roll_dice, ask_move
from game import choose_first, do_move, check_endgame

players = 4

status = {1: [0] * 4, 2: [0] * 4, 3: [0] * 4, 4: [0] * 4}


def redraw_board():
    """ Draw an ASCII board with the current pieces. 
    """

    # TODO (@vkantsev): Discuss how to add the pieces with their current positions

    BOARD_WIDTH = 45  # width excluding border
    POS_SHAPE = "( )"  # unit position shape
    FILLER = " * "  # filler
    BORDER_H = "-"  # horizontal
    BORDER_V = "|"  # vertical

    # Header
    board = "/" + BORDER_H * BOARD_WIDTH + "\\" + "\n"

    # Top half
    board += BORDER_V + (POS_SHAPE * 3).center(BOARD_WIDTH) + BORDER_V + "\n"
    for i in range(5):
        board += BORDER_V + "( ) * ( )".center(BOARD_WIDTH) + BORDER_V + "\n"

    # Middle
    board += BORDER_V + POS_SHAPE * 7 + FILLER + POS_SHAPE * 7 + BORDER_V + "\n"
    board += BORDER_V + POS_SHAPE + FILLER * 13 + POS_SHAPE + BORDER_V + "\n"
    board += BORDER_V + POS_SHAPE * 7 + FILLER + POS_SHAPE * 7 + BORDER_V + "\n"

    # Lower half
    for i in range(5):
        board += (
            BORDER_V
            + (POS_SHAPE + FILLER + POS_SHAPE).center(BOARD_WIDTH)
            + BORDER_V
            + "\n"
        )
    board += BORDER_V + (POS_SHAPE * 3).center(BOARD_WIDTH) + BORDER_V + "\n"

    # Footer
    board += "\\" + BORDER_H * BOARD_WIDTH + "/" + "\n"

    return board


def redraw(player):
    """The screen update function. Do not modify this for now."""
    print("\n\n\n")
    print(redraw_board())
    print()


def end_game(winner):
    """Celebrate the winning player."""
    print("Player {} has won!".format(winner))


def start(players):
    """The main game loop"""
    win = False
    player = choose_first(players)
    redraw(player)
    while not win:
        dice = roll_dice(player)

        valid = False
        while not valid:
            move = ask_move(player)
            valid = do_move(player, move)

        win = check_endgame()
        if not win and dice != 6:
            player = ((player + 1) % players) + 1
        redraw(player)
    end_game(player)


if __name__ == "__main__":
    start(players)
