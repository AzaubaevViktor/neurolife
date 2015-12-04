import copy
from random import random

import math


class Neuro:
    def __init__(self, layers):
        self.inp_size, *layers_sizes, self.out_size = layers
        self.layers = []
        for i in range(1, len(layers)):
            self.layers.append(Layer(layers[i-1], layers[i]))

    def calc(self, inp):
        out = inp
        for layer in self.layers:
            out = layer.calc(out)
        return out

    def mutate(self, probability, coef):
        for layer in self.layers:
            layer.mutate(probability, coef)

    def crossing(self, neuro):
        for i in range(len(self.layers)):
            self.layers[i].crossing(neuro.layers[i])

    def copy(self):
        return copy.deepcopy(self)


def sigmoid(x):
    return 1./(1 + math.e ** (-x))


class Layer:
    def __init__(self, size_left, size_right, parent=None):
        self.size_left = size_left
        self.size_right = size_right
        self.weights = [[random() for x in range(size_left)] for y in range(size_right)] if parent is None else parent

    def mutate(self, probability, coef):
        for x in range(self.size_left):
            for y in range(self.size_right):
                if random() < probability:
                    self.weights[y][x] += (random() - 0.5) * coef

    def crossing(self, layer):
        for x in range(self.size_left):
            for y in range(self.size_right):
                if random() < 0.5:
                    self.weights[y][x] = layer.weights[y][x]

    def calc(self, inp):
        out = [0 for x in range(self.size_right)]

        for y in range(self.size_right):
            s = 0
            for x in range(self.size_left):
                s += self.weights[y][x] * inp[x]

            out[y] += sigmoid(s)

        return out