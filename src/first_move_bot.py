#!/usr/bin/env python3
# coding: utf-8

from state import GameState, GameMove
from typing import Optional
from bot import Bot


class FirstMoveBot(Bot):
    def __init__(self, number: int):
        self.number = number

    def onState(self, state: GameState) -> Optional[GameMove]:
        if self.number == state.current_player and len(state.valid_actions) > 0:
            return state.valid_actions[0]
        return None
