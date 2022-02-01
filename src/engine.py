#!/usr/bin/env python3
# coding: utf-8

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

    def __on_next_player(self) -> GameMove:
        """Update engine state for next player's turn and return corresponding dice roll"""
        current_player_index = self.state.board.players.index(self.state.current_player)
        next_index = (current_player_index + 1) % len(self.state.board.players)
        next_player = self.state.board.players[next_index]
        self.state.current_player = next_player
        return GameMove.roll_dice(next_player)

    def __on_end_move(self) -> GameMove:
        if self.state.dice == 6:
            return GameMove.roll_dice(self.state.current_player)
        return self.__on_next_player()

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
            """Converts representation from state/engine representation to game/main representation to reuse logic"""
            from game import is_valid_move
            from piece import Piece as GamePiece

            b = self.state.board
            pl = b.players
            # in game terms players are 0..n, in state terms they are (not necessarily ordered unique identifiers)
            game_piece = GamePiece(pl.index(piece.player), piece.number, piece.progress)
            status = [
                GamePiece(pl.index(p.player), p.number, p.progress) for p in b.pieces
            ]
            if is_valid_move(
                game_piece,
                dice,
                status,
                b.player_shift,
                b.path_zone_length,
                b.end_progress,
            ):
                if piece.progress == 0:
                    valid_actions.append(GameMove.piece_out(player, piece.number, dice))
                else:
                    valid_actions.append(
                        GameMove.move_piece(player, piece.number, dice)
                    )

        for piece in self.state.board.pieces:
            if piece.player == player:
                calc_valid_actions(piece)
        if not valid_actions:
            valid_actions = [self.__on_end_move()]
        self.state.valid_actions = valid_actions
        self.state.number = self.state.number + 1
        return self.state

    def __knock_out_other_players(self, piece: Piece) -> None:
        b = self.state.board
        assert b.is_on_path(piece)
        contested = b.relative_position(piece)
        at_position = [
            p
            for p in b.pieces
            if b.is_on_path(p)
            and b.relative_position(p) == contested
            and p.player != piece.player
        ]
        for p in at_position:
            if p.player != piece.player:
                p.progress = 0
                assert len(at_position) == 1
                return  # only one piece can be knocked out

    def __on_piece_out(self, piece: Piece, dice: int) -> GameState:
        assert self.state.board.is_on_start(piece)
        assert dice == 6
        piece.progress = 1
        self.__knock_out_other_players(piece)
        self.state.valid_actions = [GameMove.roll_dice(piece.player)]
        self.state.number = self.state.number + 1
        return self.state

    def __on_move_piece(self, piece: Piece, dice: int) -> GameState:
        def __is_winning(piece: Piece) -> bool:
            winner = True
            for _piece in self.state.board.pieces:
                if _piece.player == piece.player:
                    winner = winner and _piece.progress == self.state.board.end_progress
            return winner

        b = self.state.board
        if piece.progress + dice < b.end_progress + 1:
            piece.progress = piece.progress + dice
            if b.is_on_path(piece):
                self.__knock_out_other_players(piece)

        if __is_winning(piece):
            self.state.winners.append(piece.player)
            if len(self.state.winners) >= len(b.players) - 1:
                self.state.valid_actions = []
        else:
            self.state.valid_actions = [self.__on_end_move()]

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
