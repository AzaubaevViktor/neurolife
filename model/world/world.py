from random import randint
from model.creature import Direction, Creature, Stalk


class World:
    def __init__(self, params):
        """
        self.creatures: {(x,y): object, ...}
        :param params: dict с параметрами
        :return:
        """
        self.creatures = {}

        creatures_params = params.get('creatures', {})
        self.creatures_in_layer = creatures_params.get('in_layers', [11, 11])
        self.creatures_count = creatures_params.get('count', 10)
        self.move_penalty = creatures_params.get('move_penalty', 0.002)
        self.fight_penalty_coef = creatures_params.get('fight_penalty_coef', 0.2)
        self.eat = creatures_params.get('eat', 0.4)
        self.layers_in = [int(x) for x in creatures_params.get('in_layers', "3,5").split(',')]

        world_param = params.get('world', {})
        self.width = world_param.get('width', 50)
        self.height = world_param.get('height', 20)
        self.sun_size = world_param.get('sun_size', 10)
        self.sun_power = world_param.get('sun_power', 0.02)
        self.sun_speed = world_param.get('sun_speed', 0.1)
        self.sun_x = (self.width - self.sun_size) / 2
        self.sun_y = (self.height - self.sun_size) / 2
        pass

    def get_obj(self, x, y):
        """
        Получить объект по координате
        :param x: Координата по x
        :param y: Координата по y
        :return: :class:
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
        self._add_object(Creature(self.creatures_in_layer))

    def step(self):
        # Обрабатываем созданий
        new_creatures = {}
        for (x, y), cr in self.creatures.items():
            if isinstance(cr, Stalk):
                pass
            if isinstance(cr, Creature):
                if self._in_sun(x, y):
                    cr.life += self.sun_power

                vision = [self.get_obj(x + Direction.coord(i)[0], y + Direction.coord(i)[1]) for i in range(9)]
                direct, power, stalk = cr.step(vision)

                if stalk:
                    while True:
                        dx, dy = Direction.coord(randint(0,9))
                        if self.get_obj(x + dx, y + dy) is None:
                            new_creatures[((x + dx) % self.width, (y + dy) % self.height)] = stalk

                dx, dy = direct.get_coord()
                cell = self.get_obj(x + dx, y + dy)

                if isinstance(cell, Creature):
                    if self._attack(cr, cell, power):
                        new_creatures[((x + dx) % self.width, (y + dy) % self.height)] = cell
                elif isinstance(cell, Stalk):
                    cr.fertilization(stalk)
                    new_creatures[((x + dx) % self.width, (y + dy) % self.height)] = cell.generate_creature()
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
            first.life -= power * self.fight_penalty_coef
            return True
        else:
            first.life += self.eat
            return False








