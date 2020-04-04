#!/usr/bin/python3

"""The main standalone application for github.com/mapto/4oBe4e"""
import random

players = 4

status = {1: [0] * 4, 2: [0] * 4, 3: [0] * 4, 4: [0] * 4}


def redraw_board():
    """ Draw an ASCII board with the current pieces. 

    >>> result = redraw_board(); lines = result.split("\n"); len(lines) == 21 and len(result) = 22 * 21 
    True
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


def roll_dice():
    """Rolls a dice: randomly generate a value between 1 and 6. Use `import random`.
    @lankata can do this

    >>> result = roll_dice(); type(result) == int and 0 < result and result < 7
    True
    """
    sides = 6
    roll_again = input("Ready to roll? ENTER=Roll. Q=Quit.")
    if roll_again.lower() != "q":
        num_rolled = roll(sides)
        print("You rolled a", num_rolled)

    print("Play yopr number!")
    return num_rolled


def roll(sides=6):
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


def do_move(player, move):
    """Check if the move is valid. If it is, perform it. Returns whether it is valid."""
    # TODO: Implement
    return True


def check_endgame():
    """Check if any of the players has ended the game."""
    # TODO: Implement
    return True


def end_game(winner):
    """Celebrate the winning player."""
    print("Player {} has won!".format(winner))


def choose_first():
    """ score index is 0..3, i.e. player-1 (player are 1..4)
    0 means hasn't drawn, -1 means is already out of drawing
    """
    m = 0
    score = [0] * players
    need_more = True
    while need_more:
        for i in range(len(score)):
            if score[i] != -1:
                score[i] = roll_dice()
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


def start():
    """The main game loop"""
    win = False
    player = choose_first()
    redraw(player)
    while not win:
        dice = roll_dice()

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
    start()
