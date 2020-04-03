#!/usr/bin/python3

"""The main standalone application for github.com/mapto/4oBe4e"""

players = 4

status = {1:[0]*4, 2:[0]*4, 3:[0]*4, 4:[0]*4}


def redraw_board():
    """Draws the board with the current pieces. Do with ASCII for now.
    Return a 21x21 board, represented by 21 lines of 21 characters each.
    @vkantsev can do this
    """
    # TODO: Implement inside of board. As first step draw a blank board.
    # TODO: Then we'll discuss how to add the pieces with their current positions 
    result = "/" + "-" * 19 + "\\\n"
    for i in range(0, 19):
        result += "|" + " " * 19 + "|\n"
    result += "\\" + "-" * 19 + "/\n"
    return result

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
