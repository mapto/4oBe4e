#!/usr/bin/python3

"""The main standalone application for github.com/mapto/4oBe4e"""

players = 4

status = {1:[0]*4, 2:[0]*4, 3:[0]*4, 4:[0]*4}

def redraw_board():
    """ Draw an ASCII board with the current pieces. """


    # TODO (@vkantsev): Discuss how to add the pieces with their current positions

    BOARD_WIDTH = 45  # width excluding border
    POS_SHAPE = '( )'  # unit position shape
    FILLER = ' * '  # filler
    BORDER_H = '-' # horizontal
    BORDER_V = '|' # vertical

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
        board += BORDER_V + (POS_SHAPE + FILLER + POS_SHAPE).center(BOARD_WIDTH) + BORDER_V + "\n"
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
    """
    pass

def ask_move(player):
    """Asks player which of his four pieces they want to move. Returns the piece index between 0 and 3.
    @lankata can do this
    """
    print(f"It is player {player}'s turn.")
    print()
    pass

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
    print(f"Player {winner} has won!")


def start():
    """The main game loop"""
    win = False
    player = 0
    redraw(player)
    while not win:
        dice = roll_dice()

        valid = False
        while not valid: 
            move = ask_move(player)
            valid = do_move(player, move)

        win = check_endgame()
        if not win and dice != 6:
            player = (player + 1) % players
        redraw(player)
    end_game(player)

if __name__ == "__main__":
    start()
