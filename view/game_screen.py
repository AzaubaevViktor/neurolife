from tkinter import Frame, Button, BOTTOM, Canvas, TOP
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox

import pickle

from model import World

class GameScreen:
    def __init__(self, master, params, world=None):
        self.master = master

        self.model = World(params)

        self.graphic_init()

        self.is_run = True
        self.run()

    def draw(self):
        # Сделать 4 солнца
        x, y = self.model.sun_x, self.model.sun_y
        suns = [(x, y),
                (x - self.model.width, y),
                (x, y - self.model.height),
                (x - self.model.width, y - self.model.height)]
        for x, y in suns:
            self.canvas.create_rectangle(max(0, x), max(0, y),
                                         min(x + self.model.sun_size, self.model.width),
                                         min(y + self.model.sun_size, self.model.height),
                                         fill="yellow")

        for coord, creature in self.model.creatures.items():
            color = "#00{:0>2}00".format(
                    hex(int(creature.life * 255))[2:]
            )
            if len(color) > 7:
                print("FFFFFUUUUUU")

            if not creature.alive:
                color = "red"

            func = self.canvas.create_oval
            func(coord[0], coord[1], coord[0] + 6, coord[1] + 6, fill=color)

    def graphic_init(self):
        self.slave = Frame(self.master,
                           bd=2)

        self.start_stop_button = Button(self.slave,
                                        text="Пауза",
                                        command=self.start_stop_pressed)
        self.start_stop_button.pack(side=BOTTOM)

        self.save_button = Button(self.slave,
                                  text="Сохранить",
                                  command=self.save_pressed)
        self.save_button.pack(side=BOTTOM)

        self.canvas = Canvas(self.slave,
                             width=self.model.width,
                             height=self.model.height)
        self.canvas.pack(side=TOP)

        self.slave.pack()

    def start_stop_pressed(self):
        self.is_run = not self.is_run
        self.start_stop_button.config(
                text='Пауза' if self.is_run else 'Старт')
        self.run()

    def save_pressed(self):
        filename = asksaveasfilename(title="Сохранить мир")
        if filename:
            try:
                pickle.dump(self.model, open(filename, "wb"))
            except Exception as e:
                messagebox.showerror("Не удалось сохранить файл", str(e))

    def run(self):
        if self.is_run:
            self.canvas.delete("all")
            self.model.step()
            self.draw()
            self.master.after(1, self.run)
