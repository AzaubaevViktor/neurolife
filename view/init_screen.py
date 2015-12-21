from copy import deepcopy
from tkinter import Frame, Button, Label, LEFT, Entry, StringVar

from controller import InitScreenController
from model import default_params, default_fields_count
from .game_screen import GameScreen


def _convert(text: str):
    norm = text.replace('_', ' ')
    return norm[0].upper() + norm[1:]


class InitScreen:
    def __init__(self, master):
        self.funcs = {}
        self.master = master
        self.controller = InitScreenController(master)
        self.master.title('parent')
        self.master.geometry('640x480+200+150')

        self.set_param_init()

        self.frame.pack()

        self.master.mainloop()

    def set_param_init(self):
        self.frame = Frame(width=400, height=300, bd=2)
        self.frame.grid_bbox(2, 4 + default_fields_count)

        self._buttons_init()

        self.entrys = {}
        _vcmd = self.frame.register(self._validate)

        count = 0

        for block_name, block in default_params.items():
            Label(self.frame,
                  text=_convert(block_name),
                  background="#999",
                  justify=LEFT).grid(
                    row=count,
                    column=1
            )
            count += 1

            for name, _default in block.items():
                default, func = _default

                Label(self.frame,
                      text=_convert(name),
                      justify=LEFT).grid(
                        row=count,
                        column=1
                )
                # self.entrys[_convert(name)] = ""
                sv = StringVar(
                        value=default_params[block_name][name][0])
                e = Entry(self.frame)

                self.entrys[name] = sv
                self.funcs[e] = func

                e.config(validate='key',
                         vcmd=(_vcmd, "%P", "%W"),
                         textvariable=sv)
                e.grid(row=count,
                       column=2)

                count += 1

        Label(self.frame,
              text="Количество существ:",
              justify=LEFT).grid(
                row=count,
                column=1
        )

        self.creature_count = \
            Label(self.frame,
                  text='0',
                  justify=LEFT)
        self.creature_count.grid(
                row=count,
                column=2
        )

    def _buttons_init(self):
        self.load_button = Button(self.frame,
                                  text='Загрузить',
                                  command=self.load_button_press)
        self.load_button.grid(row=4 + default_fields_count,
                              column=1)

        self.start_button = Button(self.frame,
                                   text='Старт',
                                   command=self.start_button_press)
        self.start_button.grid(row=4 + default_fields_count,
                               column=2)

        self.master.protocol('WM_DELETE_WINDOW',
                             self.exit)

    def _validate(self, P, W):
        e = self.frame.nametowidget(W)
        func = self.funcs[e]

        try:
            func(P)
        except ValueError:
            return False
        else:
            return True

    def _collect_params(self):
        params = deepcopy(default_params)
        for block in params.values():
            for key in block:
                func = block[key][1]
                block[key] = func(self.entrys[key].get())

        return params

    def start_button_press(self):
        params = self._collect_params()

        if self.controller.model:
            self.game_screen = GameScreen(self.master, params, model=self.controller.model)
        else:
            self.game_screen = GameScreen(self.master, params)

        self.frame.forget()

    def load_button_press(self):

        self.controller.load_button_press()

        model = self.controller.model
        self.creature_count.config(text=str(len(model.creatures)))

        for block in model.params.values():
            for k, v in block.items():
                if k == "in_layers":
                    v = ", ".join([str(x) for x in v])
                self.entrys[k].set(v)

    def exit(self):
        exit()
