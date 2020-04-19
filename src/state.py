from dataclasses import dataclass, field
from typing import List, Sequence, Set
from enum import Enum


@dataclass
class Piece:
    number: int
    player: int
    position: int = 0  # the absolute position on the board


ROLL_DICE = 1
MOVE_PIECE = 2
PIECE_OUT = 3


@dataclass
class GameMove:
    move_type: int
    player: int
    piece: int = -1
    dice: int = -1

    @staticmethod
    def roll_dice(player: int):
        return GameMove(ROLL_DICE, player)

    @staticmethod
    def move_piece(player: int, piece: int, dice: int):
        return GameMove(MOVE_PIECE, player, piece, dice)

    @staticmethod
    def piece_out(player: int, piece: int, dice: int):
        return GameMove(PIECE_OUT, player, piece, dice)


@dataclass
class Board:
    # number of the players playing the current game
    players: List[int] = field(default_factory=lambda: [1, 3])
    pieces_per_player: int = 4  # how many pieces each player has
    pieces: List[Piece] = field(default_factory=lambda: [])

    # board shape and constants with their defaults for a square board
    # with side 14 positions
    board_corners: int = 4  # rectangular = 4, triangular = 3, pentagon = 5
    board_side_length: int = 14  # side length of the board shape

    # the offset between two neighbor players start possitions on the board
    player_shift: int = (board_side_length + 1)

    # normal walk path length including connecting corners
    path_zone_length: int = (board_corners * board_side_length) + board_corners

    # the length of the finish zone (at the end of the path_zone)
    finish_zone_length: int = 5

    # the position on which the piece is out of the finish zone
    end_progress: int = (path_zone_length + finish_zone_length + 1)

    def __post_init__(self):
        assert len(self.players) > 1
        assert len(set(self.players)) == len(self.players)
        assert len(self.players) <= self.board_corners
        assert self.pieces_per_player > 0
        assert len(self.pieces) == len(self.players) * self.pieces_per_player
        assert self.board_corners > 2
        assert self.board_side_length > 5
        assert self.finish_zone_length > 2
        assert self.end_progress == (
            self.path_zone_length + self.finish_zone_length + 1
        )

    @staticmethod
    def create(
        players: List[int] = [0, 1, 2, 3],
        pieces_per_player: int = 4,
        board_corners: int = 4,
        board_side_length: int = 14,
        finish_zone_length: int = 5,
    ):
        pieces: List[Piece] = []
        player_shift: int = (board_side_length + 1)
        path_zone_length: int = (board_corners * board_side_length) + board_corners
        end_progress: int = (path_zone_length + finish_zone_length + 1)
        for player_index in range(0, len(players)):
            for piece_num in range(pieces_per_player):
                pieces.append(Piece(piece_num, players[player_index]))

        return Board(
            players=players,
            pieces_per_player=pieces_per_player,
            board_corners=board_corners,
            board_side_length=board_side_length,
            finish_zone_length=finish_zone_length,
            pieces=pieces,
            player_shift=player_shift,
            path_zone_length=path_zone_length,
            end_progress=end_progress,
        )

    def relative_position(self, piece: Piece) -> int:
        # Relative position is only relevant within the path_zone
        assert self.is_on_path(piece)
        relative_position = (piece.player * self.player_shift) + piece.position
        relative_position = (
            relative_position
            if relative_position <= self.path_zone_length
            else relative_position % self.path_zone_length
        )
        return relative_position

    def is_on_start(self, piece: Piece) -> bool:
        return True if piece.position == 0 else False

    def is_on_path(self, piece: Piece) -> bool:
        return True if 1 <= piece.position <= self.path_zone_length else False

    def is_on_finish(self, piece: Piece) -> bool:
        return (
            True
            if self.path_zone_length < piece.position < self.end_progress
            else False
        )

    def is_on_target(self, piece: Piece) -> bool:
        return (
            True
            if piece.position > (self.path_zone_length + self.finish_zone_length)
            else False
        )


@dataclass
class GameState:
    board: Board
    valid_actions: Sequence[GameMove]
    current_player: int
    number: int = 0  # unique ordinal number of the state
    dice: int = -1
    winners: List[int] = field(default_factory=lambda: [])

    @staticmethod
    def create(board: Board):
        current_player = board.players[0]
        valid_actions = [GameMove.roll_dice(player=current_player)]
        return GameState(
            board=board, current_player=current_player, valid_actions=valid_actions
        )
