from tkinter import Frame, Button, Canvas, TOP, DISABLED, ACTIVE
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename

from controller import GameScreenController
from .info_window import InfoWindow


class GameScreen:
    def __init__(self, master, params, model=None):
        self.master = master

        self.controller = GameScreenController(params, model=model)

        self.width = self.controller.model.width
        self.height = self.controller.model.height

        self.graphic_init()

        self.is_run = True
        self.run()

    def draw(self):
        # Сделать 4 солнца
        model = self.controller.model
        x, y = model.sun_x, model.sun_y
        suns = [(x, y),
                (x - self.width, y),
                (x, y - self.height),
                (x - self.width, y - self.height)]
        for x, y in suns:
            self.canvas.create_rectangle(max(0, x), max(0, y),
                                         min(x + model.sun_size, self.width + 1),
                                         min(y + model.sun_size, self.height + 1),
                                         fill="yellow")

        for coord, creature in model.creatures.items():
            color = "#00{:0>2}00".format(
                    hex(int(creature.life * 255))[2:]
            )

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
                   width=self.width,
                   height=self.height)
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
                self.controller.save_pressed(filename)
            except Exception as e:
                messagebox.showerror("Не удалось сохранить файл", str(e))

    def info_pressed(self):
        InfoWindow(self.controller.model)

    def add_pressed(self):
        self.controller.add_pressed()

    def run(self):
        if self.is_run:
            self.canvas.delete("all")
            self.controller.run()
            self.draw()
            self.master.after(1, self.run)
