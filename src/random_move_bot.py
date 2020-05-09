#!/usr/bin/env python3
# coding: utf-8

from engine import GameEngine
from state import GameState, GameMove
from typing import Optional
from bot import Bot
import random


class RandomMoveBot(Bot):
    def onState(self, state: GameState) -> Optional[GameMove]:
        movesLen = len(state.valid_actions)
        if self.player() == state.current_player and movesLen > 0:
            return state.valid_actions[random.randint(0, movesLen - 1)]
        return None
