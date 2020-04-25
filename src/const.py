"""Board constants - extracted to avoid circular dependency between models of board and piece"""

NUMBER_OF_PLAYERS = 4
NUMBER_OF_PIECES = 4

HOME_ZONE = 0
PLAYER_SHIFT = 14
LAST_ON_PATH = PLAYER_SHIFT * NUMBER_OF_PLAYERS
END_PROGRESS = LAST_ON_PATH + 6
