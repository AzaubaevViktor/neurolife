from enum import Enum
from .neuro import Neuro

x = [[-1, 1], [0, 1], [1, 1],
     [-1, 0], [0, 0], [1, 0],
     [-1, -1], [0, -1], [1, -1]]


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

    @classmethod
    def coord(cls, value):
        return x[value]

    def get_coord(self):
        return x[self.value]


class Creature:
    """
    Создание
    """
    def __init__(self, in_layers: list = None,
                 genome: Neuro = None,
                 life: float = 1,
                 burn_threshold = 0.8,
                 mutate_param=None):
        """

        :param in_layers: Слои нейросети
        :param genome: Геном, который будет там
        :return: instance создания
        """

        self.burn_threshold = burn_threshold
        in_layers = [11, 11] if in_layers is None else in_layers
        self.genome = Neuro([9] + in_layers + [11]) if genome is None else genome.copy()
        self.memory = 0
        self._life = life
        self.mutate_param = (0.2, 0.3) if mutate_param is None else mutate_param
        self.next_stalk = 10
        self.in_world = True

    @classmethod
    def load_from_file(cls, filename):
        pass

    @property
    def life(self):
        """
        Кол-во здоровья
        :return: float
        """
        return self._life

    @life.setter
    def life(self, val):
        """
        Устанавливает кол-во здоровья
        :param val: float
        :return:
        """
        self._life = val
        if self._life > 1:
            self._life = 1
        elif self._life < 0:
            self._life = 0

    @property
    def alive(self):
        """
        Проверка на то, что создание живо
        :return: bool
        """
        return self.life > 0

    def step(self, vision: list) -> (Direction, int, object):
        """
        Делает один шаг симуляции
        :param vision: list
        :return: (Direction, int, object)
        """
        *directs, self.memory, create_stalk = self._calc(vision)
        self.next_stalk -= 1
        stalk = None

        av = sum(directs)/len(directs)

        if create_stalk > av and self.next_stalk < 0 and self.life > self.burn_threshold:
            stalk = self.create_stalk()
            self.next_stalk = 10
        return Direction(directs.index(max(directs))), max(directs), stalk

    def create_stalk(self):
        """
        Создаёт потомка
        :return: Creature
        """
        stalk_life = min(self.life, 0.3)
        self.life -= stalk_life
        return Creature(genome=self.genome, life=stalk_life, mutate_param=self.mutate_param,
                        burn_threshold=self.burn_threshold)

    def _calc(self, vision: list) -> (list, bool):
        """
        :param vision: list с описанием, видно ли что-то вокруг
        :return: набор выходящих значений для направлений, выбрасывать ли stalk
        """
        self.life -= 0.00
        return self.genome.calc(vision + [self.life, self.memory])
