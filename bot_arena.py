#!/usr/bin/env python3
# coding: utf-8

from state import GameState, GameMove
from typing import Optional, List, Set
from bot import Bot
from random_move_bot import RandomMoveBot
from first_move_bot import FirstMoveBot
import random

def __random_board_position(angles: int, players: List[int]) -> int:
    result = random.randint(0, angles - 1)
    while result in players:
        result = random.randint(0, len(players) - 1)
    return result


def fight(bots: List[Bot]) -> List[int]:
    for i in range(len(bots)):
        print("i:", i)
        # assert bots[i].player == i

    board_sides = 4
    players = [-1 for p in players]

    # players[i] is the player number for bot bots[i]
    for b in bots:
       players[i] = __random_board_position(angles, players)

    print("players: ", players)

    board = Board.create(players=players, board_sides=board_sides)
    state = GameState.create(board)

    while len(game.state.valid_actions) > 0:
        for bot in bots:
           move = bot.onState(game.state)
           if move != None and move.player == bot.player:
               game.play(move)

    return game.state.winnersj

if __name__ == "__main__":
    bots = [
        RandomMoveBot(0),
        FirstMoveBot(1),
    ]
    [fight(bots) for i in range(10)]
