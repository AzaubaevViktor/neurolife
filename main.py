# импортирование модулей python
import random
from time import sleep
from tkinter import *

from model import World, Creature


class Main:
    def __init__(self, master):
        self.master = master
        self.master.title('parent')
        self.master.geometry('640x480+200+150')

        self.set_param_init()

        self.set_param_frame.pack()

        self.master.mainloop()

    def set_param_init(self):
        self.set_param_frame = Frame(width=400, height=300, bd=2)
        self.set_param_frame.grid_bbox(3, 3)

        self.load_button = Button(self.set_param_frame,
                                  text='Импорт',
                                  state=DISABLED,
                                  command=self.load_button_press)
        self.load_button.grid(row=1, column=2)

        self.start_button = Button(self.set_param_frame,
                                   text='Старт',
                                   command=self.start_button_press)
        self.start_button.grid(row=2, column=1)

        self.master.protocol('WM_DELETE_WINDOW',
                             self.exit)

    def start_button_press(self):
        self.game_screen = GameScreen(self.master)
        self.set_param_frame.forget()

    def load_button_press(self):
        pass

    def exit(self):
        exit()


class GameScreen:
    def __init__(self, master):
        self.master = master

        self.graphic_init()

        self.model = World()

        self.is_run = False

    def draw(self):
        # Сделать 4 солнца
        self.canvas.create_rectangle(self.model.sun_x, self.model.sun_y,
                                     self.model.sun_x + self.model.sun_size, self.model.sun_y + self.model.sun_size,
                                     fill="yellow")

        for coord, creature in self.model.creatures.items():
            color ="#00{:0>2}00".format(
                hex(int(creature.life * 255))[2:]
            )
            if isinstance(creature, Creature):
                func = self.canvas.create_oval
            else:
                func = self.canvas.create_rectangle
            func(coord[0], coord[1], coord[0]+6, coord[1]+6, fill=color)

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
        self.canvas.create_line(1, 1, 10, 20, 30, 40, 50, 60)
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

# создание окна
root = Tk()

# запуск окна
Main(root)
