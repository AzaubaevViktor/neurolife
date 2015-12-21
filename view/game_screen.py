from tkinter import Frame, Button, BOTTOM, Canvas, TOP

from model import World, Creature


class GameScreen:
    def __init__(self, master, params):
        self.master = master

        self.graphic_init()

        self.model = World(params)

        self.is_run = False

    def draw(self):
        # Сделать 4 солнца
        x, y = self.model.sun_x, self.model.sun_y
        suns = [(x, y),
                (x - self.model.width, y),
                (x, y - self.model.height),
                (x - self.model.width, y - self.model.height)]
        for x, y in suns:
            self.canvas.create_rectangle(x, y,
                                         x + self.model.sun_size, y + self.model.sun_size,
                                         fill="yellow")

        for coord, creature in self.model.creatures.items():
            color = "#00{:0>2}00".format(
                    hex(int(creature.life * 255))[2:]
            )
            if len(color) > 7:
                print("FFFFFUUUUUU")

            if isinstance(creature, Creature):
                func = self.canvas.create_oval
            else:
                func = self.canvas.create_rectangle
            func(coord[0], coord[1], coord[0] + 6, coord[1] + 6, fill=color)

    def graphic_init(self):
        self.slave = Frame(self.master,
                           width=600,
                           height=480,
                           bd=2)

        self.start_stop_button = Button(self.slave,
                                        text="Start",
                                        command=self.start_stop_perssed)
        self.start_stop_button.pack(side=BOTTOM)

        self.canvas = Canvas(self.slave,
                             width=600,
                             height=400)
        self.canvas.pack(side=TOP)

        self.slave.pack()

    def start_stop_perssed(self):
        self.is_run = not self.is_run
        self.run()

    def run(self):
        if self.is_run:
            self.canvas.delete("all")
            self.model.step()
            self.draw()
            self.master.after(1, self.run)