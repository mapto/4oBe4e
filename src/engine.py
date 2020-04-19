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
            if self.state.board.is_on_start(piece) and dice == 6:
                valid_actions.append(GameMove.piece_out(player, piece.number, dice))
            elif self.state.board.is_on_path(piece):
                valid_actions.append(GameMove.move_piece(player, piece.number, dice))

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
        if piece.position + dice < self.state.board.end_progress + 1:
            piece.position = piece.position + dice

        winner = True
        for _piece in self.state.board.pieces:
            if _piece.player == piece.player:
                winner = winner and _piece.position == self.state.board.end_progress
        if winner:
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
