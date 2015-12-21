import copy
from random import random

import math


class Neuro:
    """
    Реализация нейросети
    """
    def __init__(self, layers):
        """

        :param layers: int, Кол-во слоёв
        :return:
        """
        self.layers = []
        for i in range(1, len(layers)):
            self.layers.append(Layer(layers[i-1], layers[i]))

    def calc(self, inp: list):
        """
        Рассчёт шага нейросети
        :param inp: list
        :return:
        """
        out = inp
        for layer in self.layers:
            out = layer.calc(out)
        return out

    def mutate(self, probability: float, coef: float):
        """
        Мутация нейросети
        :param probability: float, Вероятность мутации одной связи
        :param coef: float, Коэффициент мутации одной связи
        :return:
        """
        for layer in self.layers:
            layer.mutate(probability, coef)

    def copy(self):
        return copy.deepcopy(self)


def sigmoid(x):
    return 1./(1 + math.e ** (-x)) - 0.5


class Layer:
    """
    Слой для нейросети
    """
    def __init__(self, size_left, size_right, parent=None):
        """

        :param size_left: int, Кол-во входов
        :param size_right: int, Кол-во выходов
        :param parent: Layer, Родительский слой
        :return:
        """
        self.size_left = size_left
        self.size_right = size_right
        self.weights = [[(random() - 0.5) for x in range(size_left)] for y in range(size_right)] if parent is None else parent

    def mutate(self, probability, coef):
        """
        Воспроизводит процесс мутации
        :param probability: float, Вероятность мутации одной связи
        :param coef: float, Коэффициент мутации одной связи
        :return:
        """
        for x in range(self.size_left):
            for y in range(self.size_right):
                if random() < probability:
                    self.weights[y][x] += (random() - 0.5) * coef

    def calc(self, inp):
        """
        Рассчёт выходов
        :param inp: list
        :return: list
        """
        out = [0 for x in range(self.size_right)]

        for y in range(self.size_right):
            s = 0
            for x in range(self.size_left):
                s += self.weights[y][x] * inp[x]

            out[y] += sigmoid(s)

        return out