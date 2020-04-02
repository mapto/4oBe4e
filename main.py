#!/usr/bin/python3

"""The main standalone application for github.com/mapto/4oBe4e"""

players = 4

status = {1:[0]*4, 2:[0]*4, 3:[0]*4, 4:[0]*4}


def redraw_board():
    """Draws the board with the current pieces. Do with ASCII for now.
    @vkantsev can do this
    """
    pass

def roll_dice():    
    """Rolls a dice: randomly generate a value between 1 and 6. Use `import random`.
    @lankata can do this
    """
    pass

def ask_move(player):
    """Asks player which of his four pieces they want to move. Returns the piece index between 0 and 3.
    @lankata can do this
    """
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
    while not win:
        redraw_board()
        dice = roll_dice()
        
        valid = False
        while not valid: 
            move = ask_move(player)
            valid = do_move(player, move)

        win = check_endgame()
        if not win and dice != 6:
            player = (player + 1) % players
    end_game(player)

if __name__ == "__main__":
    start()
