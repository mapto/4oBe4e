from state import Piece, Board, GameAction, RollDice, MovePiece, PieceOut, GameState

# from pampy import match, _


class GameEngine:
    def __init__(self, board: Board):
        self.state = GameState.create(board)

    def get_state(self) -> GameState:
        return self.state

    def on_roll_dice(self, player: int) -> GameState:
        pass

    def on_piece_out(self, player: int, piece: Piece, dice: int) -> GameState:
        pass

    def on_move_piece(self, player: int, piece: Piece, dice: int) -> GameState:
        pass

    def apply(self, action: GameAction) -> GameState:
        if action not in self.state.valid_actions:
            raise ValueError(
                f"Illegal action {action} is not one of {self.state.valid_actions}"
            )

        #        match(action, RollDice(_), self.on_roll_dice)
        #        match(action, PieceOut(_, _, _), self.on_piece_out)
        #        match(action, MovePiece(_, _, _), self.on_move_piece)
        return self.state
