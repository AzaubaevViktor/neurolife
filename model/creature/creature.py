import random
from enum import Enum


class Direction(Enum):
    LeftUp = 0
    Up = 1
    RightUp = 2
    Left = 3
    Center = 4
    Right = 5
    LeftDown = 6
    Down = 7
    RightDown = 8


class Creature:
    def __init__(self, params):
        """

        :param params: Параметры создания
        :return: instance создания
        """
        self.memory = 0
        self.genome = None
        self._life = 1
        pass

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, val):
        if self.life > 1:
            self._life = 1
        elif self.life < 0:
            self._life = 0

    @property
    def alive(self):
        return self.life > 0

    def step(self, vision: list) -> Direction:
        return Direction(self._calc(vision))

    def _calc(self, vision: list):
        self.life -= 0.001
        ret_value = self.memory = (random.randint(0, 9) + self.memory) % 9
        return ret_value
