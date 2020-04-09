class Piece:
    def __init__(self, player: int, piece_number: int, absolutePosition: int = 0):
        self.piece_number: int = piece_number
        self.player: int = player
        self.absolutePosition: int = absolutePosition
        self.position: int = 0
