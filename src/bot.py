#!/usr/bin/env python3
# coding: utf-8

from abc import ABC, abstractmethod
from typing import Optional
from state import GameState, GameMove
from engine import GameEngine


class Bot(ABC):
    def __init__(self, player: int) -> None:
        self.player_num = player

    def player(self) -> int:
        return self.player_num

    @abstractmethod
    def onState(self, state: GameState) -> Optional[GameMove]:
        pass
