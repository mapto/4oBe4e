#!/usr/bin/env python3
# coding: utf-8

from engine import GameEngine
from state import GameState, GameMove, Board
from typing import Optional, List, Set
from bot import Bot
from random_move_bot import RandomMoveBot
from first_move_bot import FirstMoveBot
import random


def __random_board_position(board_sides: int, players: List[int]) -> int:
    result = random.randint(0, board_sides - 1)
    while result in players:
        result = random.randint(0, board_sides - 1)
    return result


def fight(board_sides: int, bots: List[Bot]) -> List[int]:
    players = [b.player() for b in bots]
    print("players:", players)

    board = Board.create(players=players, board_sides=board_sides)
    game = GameEngine(board)

    while len(game.state.valid_actions) > 0:
        print("valid action:", game.state.valid_actions)
        for bot in bots:
            move = bot.onState(game.state)
            if isinstance(move, GameMove) and move.player == bot.player():
                print("player: " + str(bot.player()) + " move: " + str(move))
                game.play(move)
                if move.move_type == 1:
                    print("dice rolled:", game.state.dice)


    print("fight results:", game.state.winners)
    return game.state.winners


if __name__ == "__main__":
    board_sides = 4

    board_position1 = __random_board_position(board_sides, [])
    board_position2 = __random_board_position(board_sides, [board_position1])
    board_position3 = __random_board_position(
        board_sides, [board_position1, board_position2]
    )
    bots = [
        RandomMoveBot(board_position1),
        FirstMoveBot(board_position2),
        RandomMoveBot(board_position3),
    ]
    results = [fight(board_sides, bots) for i in range(1)]
    print(results)
