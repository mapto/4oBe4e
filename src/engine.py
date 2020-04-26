from state import Piece, Board, GameMove, GameState, ROLL_DICE, MOVE_PIECE, PIECE_OUT
from util import roll as roll_dice
from typing import List, Sequence


class Dice:
    def roll(self) -> int:
        return roll_dice()


class GameEngine:
    def __init__(self, board: Board, dice: Dice = Dice()):
        self.state = GameState.create(board)
        self.dice = dice

    def get_state(self) -> GameState:
        return self.state

    def __next_player(self) -> int:
        current_player_index = self.state.board.players.index(self.state.current_player)
        if current_player_index >= (len(self.state.board.players) - 1):
            current_player_index = 0
            return self.state.board.players[0]
        return self.state.board.players[current_player_index + 1]

    def __find_piece(self, move: GameMove) -> Piece:
        for i in range(len(self.state.board.pieces)):
            piece = self.state.board.pieces[i]
            if piece.number == move.piece and piece.player == move.player:
                return piece
        raise ValueError("Cannot find piece: ", move.piece)

    def __on_roll_dice(self, player: int) -> GameState:
        dice = self.dice.roll()
        self.state.dice = dice
        player = self.state.current_player
        valid_actions: List[GameMove] = []

        def calc_valid_actions(piece: Piece) -> None:
            """ Converts representation from state/engine representation to game/main representation to reuse logic """
            from game import is_valid_move
            from piece import Piece as GamePiece

            b = self.state.board
            pl = b.players
            # in game terms players are 0..n, in state terms they are (not necessarily ordered unique identifiers)
            game_piece = GamePiece(pl.index(piece.player), piece.number, piece.position)
            status = [
                GamePiece(pl.index(p.player), p.number, p.position) for p in b.pieces
            ]
            if is_valid_move(
                game_piece,
                dice,
                status,
                b.player_shift,
                b.path_zone_length,
                b.end_progress,
            ):
                creator = (
                    GameMove.piece_out if piece.position == 0 else GameMove.move_piece
                )
                valid_actions.append(creator(player, piece.number, dice))

        for piece in self.state.board.pieces:
            if piece.player == player:
                calc_valid_actions(piece)
        if len(valid_actions) == 0:
            next_player = self.__next_player()
            self.state.current_player = next_player
            valid_actions.append(GameMove.roll_dice(next_player))

        self.state.valid_actions = valid_actions
        self.state.number = self.state.number + 1
        return self.state

    def __on_piece_out(self, piece: Piece, dice: int) -> GameState:
        assert self.state.board.is_on_start(piece)
        assert dice == 6
        piece.position = 1
        self.state.valid_actions = [GameMove.roll_dice(piece.player)]
        self.state.number = self.state.number + 1
        return self.state

    def __on_move_piece(self, piece: Piece, dice: int) -> GameState:
        def __is_winning(piece: Piece):
            winner = True
            for _piece in self.state.board.pieces:
                if _piece.player == piece.player:
                    winner = winner and _piece.position == self.state.board.end_progress
            return winner

        if piece.position + dice < self.state.board.end_progress + 1:
            piece.position = piece.position + dice

        if __is_winning(piece):
            self.state.winners.append(piece.player)
            if len(self.state.winners) >= len(self.state.board.players) - 1:
                self.state.valid_actions = []
        else:
            if dice == 6:
                self.state.valid_actions = [GameMove.roll_dice(piece.player)]
            else:
                next_player = self.__next_player()
                self.state.valid_actions = [GameMove.roll_dice(next_player)]

        self.state.number = self.state.number + 1
        return self.state

    def play(self, move: GameMove) -> GameState:
        if move not in self.state.valid_actions:
            raise ValueError(
                f"Illegal action {move} is not one of {self.state.valid_actions}"
            )

        if move.move_type == ROLL_DICE:
            self.__on_roll_dice(move.player)
        elif move.move_type == PIECE_OUT:
            self.__on_piece_out(self.__find_piece(move), move.dice)
        elif move.move_type == MOVE_PIECE:
            self.__on_move_piece(self.__find_piece(move), move.dice)

        return self.state
