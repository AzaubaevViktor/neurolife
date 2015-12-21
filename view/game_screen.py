from tkinter import Frame, Button, BOTTOM, Canvas, TOP, LEFT, SE, NE, DISABLED, ACTIVE
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox

import pickle

from model import World
from view.info_window import InfoWindow


class GameScreen:
    def __init__(self, master, params, world=None):
        self.master = master

        self.model = world if world else World(params)

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
        self.frame = Frame(self.master,
                           bd=2)

        self.button_frame = Frame(self.frame,
                                  bd=2)
        self.button_frame.grid_bbox(row=1,
                                    column=4)

        self.start_stop_button = \
            Button(self.button_frame,
                   text="Пауза",
                   command=self.start_stop_pressed)
        self.start_stop_button.grid(row=1,
                                    column=2)

        self.save_button = \
            Button(self.button_frame,
                   text="Сохранить",
                   command=self.save_pressed)
        self.save_button.grid(row=1,
                              column=1)

        self.info_button = \
            Button(self.button_frame,
                   text="Инфо",
                   command=self.info_pressed,
                   state=DISABLED)
        self.info_button.grid(row=1,
                              column=4)

        self.add_button = \
            Button(self.button_frame,
                   text="Добавить существо",
                   command=self.add_pressed, )
        self.add_button.grid(row=1,
                             column=3)

        self.canvas = \
            Canvas(self.frame,
                   width=self.model.width,
                   height=self.model.height)
        self.canvas.pack(side=TOP)

        self.button_frame.pack()

        self.frame.pack()

    def start_stop_pressed(self):
        self.is_run = not self.is_run
        self.start_stop_button.config(
                text='Пауза' if self.is_run else 'Старт')
        self.info_button.config(
                state=DISABLED if self.is_run else ACTIVE
        )
        self.run()

    def save_pressed(self):
        filename = asksaveasfilename(title="Сохранить мир")
        if filename:
            try:
                pickle.dump(self.model, open(filename, "wb"))
            except Exception as e:
                messagebox.showerror("Не удалось сохранить файл", str(e))

    def info_pressed(self):
        top = InfoWindow(self.model)

    def add_pressed(self):
        self.model.create_creature()

    def run(self):
        if self.is_run:
            self.canvas.delete("all")
            self.model.step()
            self.draw()
            self.master.after(1, self.run)
