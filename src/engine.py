from state import Piece, Board, GameAction, RollDice, MovePiece, PieceOut, GameState
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

    def __on_roll_dice(self, player: int) -> GameState:
        dice = self.dice.roll()
        self.state.dice = dice
        player = self.state.current_player
        valid_actions: List[GameAction] = []

        def calc_valid_actions(piece: Piece) -> None:
            if piece.position == 0 and dice == 6:
                valid_actions.append(PieceOut(player, piece, dice))

        for piece in self.state.board.pieces:
            if piece.player == player:
                calc_valid_actions(piece)
        if len(valid_actions) == 0:
            valid_action.append(RollDice())

        self.state.valid_actions = valid_actions
        return self.state

    def __on_piece_out(self, player: int, piece: Piece, dice: int) -> GameState:
        pass

    def __on_move_piece(self, player: int, piece: Piece, dice: int) -> GameState:
        pass

    def play(self, action: GameAction) -> GameState:
        if action not in self.state.valid_actions:
            raise ValueError(
                f"Illegal action {action} is not one of {self.state.valid_actions}"
            )

        if isinstance(action, RollDice):
            self.__on_roll_dice(action.player)

        return self.state
