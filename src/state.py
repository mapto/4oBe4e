from dataclasses import dataclass, field
from typing import List


@dataclass
class Piece:
    number: int
    player: int
    position: int = 0  # the absolute position on the board


@dataclass
class GameAction:
    player: int


@dataclass
class RollDice(GameAction):
    pass


@dataclass
class MovePiece(GameAction):
    piece: Piece
    dice: int


@dataclass
class Board:
    players_count: int = 4  # number of the players playing the current game
    pieces_per_player: int = 4  # how many pieces each player has
    pieces: List[Piece] = field(default_factory=lambda: [])

    # board shape and constants with their defaults for a square board
    # with side 14 positions
    shape_angles: int = 4  # rectangular = 4, triangular = 3, pentagon = 5
    shape_side_length: int = 14  # side length of the board shape

    # the offset between two neighbor players start possitions on the board
    # calculated in __post_init__. Probably there is a better way
    player_shift: int = 0

    # the length in possitions on the board of the finish zoen
    finish_zone_length: int = 5

    # the position on which the piece is out of the finish zone
    # calculated in __post_init__. Probably there is a better way
    end_progress: int = 0

    @staticmethod
    def create(
        players_count: int = 4,
        pieces_per_player: int = 4,
        shape_angles: int = 4,
        shape_side_length: int = 14,
        finish_zone_length=5,
    ):
        pieces: List[Piece] = []
        player_shift: int = shape_side_length + 1
        end_progress: int = 1 + shape_angles * shape_side_length + finish_zone_length
        for player_num in range(0, players_count):
            for piece_num in range(pieces_per_player):
                pieces.append(Piece(piece_num, player_num))

        return Board(
            players_count=players_count,
            pieces_per_player=pieces_per_player,
            pieces=pieces,
            shape_angles=shape_angles,
            shape_side_length=shape_side_length,
            player_shift=player_shift,
            finish_zone_length=finish_zone_length,
            end_progress=end_progress,
        )


@dataclass
class GameState:
    number: int  # unique ordinal number of the state
    board: Board
    current_player: int = 0
    valid_actions = [RollDice(player=0)]
