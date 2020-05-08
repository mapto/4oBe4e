#!/usr/bin/env python3
# coding: utf-8

from state import GameState, GameMove
from typing import Optional
from bot import Bot


class FirstMoveBot(Bot):
    def onState(self, state: GameState) -> Optional[GameMove]:
        if self.player() == state.current_player and len(state.valid_actions) > 0:
            return state.valid_actions[0]
        return None
