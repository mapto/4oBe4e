#!/usr/bin/env python3
# coding: utf-8

from abc import ABC, abstractmethod
from typing import Optional
from state import GameState, GameMove
from engine import GameEngine


class Bot(ABC):
    @abstractmethod
    def onState(self, state: GameState) -> Optional[GameMove]:
        pass
