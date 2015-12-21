from random import randint
from model.creature import Direction, Creature

to_list = lambda x: [int(x) for x in x.split(",") if x]

default_params = {
    "creatures": {
        'in_layers': ("10, 11", to_list),
        "count": ("500", int),
        "move_penalty": ("0.001", float),
        "fight_penalty_coef": ("0.2", float),
        "eat": ("0.4", float),
        "burn_threshold": (0.8, float)
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

    def _in_sun(self, x, y):
        coords = [(x, y),
                  (x + self.width, y),
                  (x, y + self.height),
                  (x + self.width, y + self.height)]

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

    def step(self):
        # Обрабатываем созданий
        new_creatures = {}
        for (x, y), cr in self.creatures.items():
            if isinstance(cr, Creature):
                if not cr.alive:
                    new_creatures[x, y] = cr
                    continue

                if self._in_sun(x, y):
                    cr.life += self.sun_power

                vision = [
                    0 if self.get_obj(x + Direction.coord(i)[0], y + Direction.coord(i)[1]) is None else 1 for i in
                    range(9)]
                vision = vision[:4] + vision[5:]
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
