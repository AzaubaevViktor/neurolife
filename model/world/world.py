from random import randint

import math

from model.creature import Direction, Creature

to_list = lambda x: [int(x) for x in x.split(",") if x]

default_params = {
    "creatures": {
        'in_layers': ("10, 11", to_list),
        "count": ("50", int),
        "move_penalty": ("0.001", float),
        "fight_penalty_coef": ("0.2", float),
        "eat": ("0.4", float),
        "burn_threshold": ("0.8", float),
        "vision_range": ("80", int)
    },
    "world": {
        "width": ("640", int),
        "height": ("400", int),
        "sun_size": ("200", int),
        "sun_power": ("0.002", float),
        "sun_speed": ("1", int)
    }
}

default_fields_count = sum([len(default_params[key]) for key in default_params])


class World:
    def __init__(self, params=None):
        """
        self.creatures: {(x,y): object, ...}
        :param params: dict с параметрами
        :return:
        """
        self.creatures = {}

        params = {} if params is None else params
        self.params = params

        creatures_params = params['creatures']
        self.creatures_in_layer = creatures_params['in_layers']
        self.creatures_count = creatures_params['count']
        self.move_penalty = creatures_params['move_penalty']
        self.fight_penalty_coef = creatures_params['fight_penalty_coef']
        self.eat = creatures_params['eat']
        self.burn_treshold = creatures_params['burn_threshold']
        self.vision_range = creatures_params['vision_range']

        world_param = params['world']
        self.width = world_param['width']
        self.height = world_param['height']
        self.sun_size = world_param['sun_size']
        self.sun_power = world_param['sun_power']
        self.sun_speed = world_param['sun_speed']
        self.sun_x = (self.width - self.sun_size) / 2
        self.sun_y = (self.height - self.sun_size) / 2

        for x in range(self.creatures_count):
            self.create_creature()
        pass

    def get_obj(self, x, y):
        """
        Получить объект по координате
        :param x: Координата по x
        :param y: Координата по y
        :return: Creature
        """
        return self.creatures.get((x % self.width, y % self.height), None)

    def del_obj(self, x, y):
        """
        Удаляет объект по координате
        :param x: Координата по x
        :param y: Координата по y
        :return:
        """
        try:
            del self.creatures[(x % self.width, y % self.height)]
        except KeyError:
            pass

    def _add_object(self, creature):
        x = 0
        y = 0
        while True:
            x = randint(0, self.width)
            y = randint(0, self.height)
            if (x, y) not in self.creatures.keys():
                break
        self.creatures[(x, y)] = creature

    def _get_four(self, coord):
        """
        Возвращает 4 координаты (ибо игровое поле -- тор)
        :param coord:
        :return:
        """
        x, y = coord
        return [(x, y),
                (x + self.width, y),
                (x, y + self.height),
                (x + self.width, y + self.height)]

    def _in_sun(self, source_coord):
        coords = self._get_four(source_coord)

        for coord in coords:
            if 0 < coord[0] - self.sun_x < self.sun_size and \
                                    0 < coord[1] - self.sun_y < self.sun_size:
                return True

        return False

    def create_creature(self):
        """
        Создаёт новое создание
        :return:
        """
        self._add_object(Creature(self.creatures_in_layer, burn_threshold=self.burn_treshold))

    def _vector(self, first, second):
        if first == second:
            return 0, 0
        _dist2dx = lambda dx, dy: dx*dx + dy*dy
        dist2 = lambda _x1, _y1, _x2, _y2: _dist2dx((_x2 - _x1), (_y2 - _y1))
        dist2c = lambda _first, _second: dist2(_first[0], _first[1], _second[0], _second[1])

        fs = self._get_four(first)
        ss = self._get_four(second)
        d_min = dist2c(first, second)
        phi_min = 0
        min_coords = (first, second)

        for f in fs:
            for s in ss:
                d = dist2c(f, s)
                if d_min > d:
                    min_coords = (f, s)
                    d_min = d

        #  Ищем угол
        (x1, y1), (x2, y2) = min_coords
        dx = x2 - x1
        dy = y2 - y1

        phi_min = math.atan2(dy, dx)

        return math.sqrt(d_min), phi_min

    def _create_vision(self, x, y):
        vision = [0 for x in range(8)]
        for coord, cr in self.creatures.items():
            if (x, y) == coord:
                continue

            x2, y2 = coord
            if min(abs(x2 - x), abs(y2 - y)) < self.vision_range:
                d, phi = self._vector((x, y), coord)
                if d > self.vision_range:
                    continue

                index = int(4 / math.pi * phi)
                vision[index] = max(vision[index], 1 - d / self.vision_range)
        return vision

    def step(self):
        # Обрабатываем созданий
        new_creatures = {}
        for (x, y), cr in self.creatures.items():
            if isinstance(cr, Creature):
                if not cr.alive:
                    new_creatures[x, y] = cr
                    continue

                if self._in_sun((x, y)):
                    cr.life += self.sun_power

                vision = self._create_vision(x, y)
                direct, power, stalk = cr.step(vision)

                if stalk:
                    while True:
                        dx, dy = Direction.coord(randint(0, 8))
                        dx, dy = dx * 3, dy * 3
                        if self.get_obj(x + dx, y + dy) is None:
                            new_creatures[((x + dx) % self.width, (y + dy) % self.height)] = stalk
                            break

                dx, dy = direct.get_coord()
                cell = self.get_obj(x + dx, y + dy)

                if isinstance(cell, Creature):
                    if self._attack(cr, cell, power):
                        new_creatures[((x + dx) % self.width, (y + dy) % self.height)] = cell
                else:
                    if cr.alive:
                        new_creatures[((x + dx) % self.width, (y + dy) % self.height)] = cr
                        cr.life -= self.move_penalty

        self.creatures = new_creatures

        # Двигаем солнце
        self.sun_y += self.sun_speed
        self.sun_x += self.sun_speed

        self.sun_x %= self.width
        self.sun_y %= self.height

    def _attack(self, first: Creature, second: Creature, power):
        if second.alive:
            second.life -= power * first.life
            first.life += power * first.life * (1 - self.fight_penalty_coef)
            return True
        else:
            first.life += self.eat
            return False

    def info(self):
        _info = {
            'cr_count': len(self.creatures),
            'cr_alive': len([None for x in self.creatures.values() if x.alive])
        }
        return _info
