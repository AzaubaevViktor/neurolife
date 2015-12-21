import json
from copy import deepcopy
from tkinter import Frame, Button, DISABLED, Text, Label, LEFT, Entry
from tkinter.filedialog import askopenfilename, asksaveasfilename

from .game_screen import GameScreen

from model import default_params, default_fields_count


def _convert(text: str):
    norm = text.replace('_', ' ')
    return norm[0].upper() + norm[1:]


class InitScreen:
    def __init__(self, master):
        self.funcs = {}
        self.master = master
        self.master.title('parent')
        self.master.geometry('640x480+200+150')

        self.set_param_init()

        self.set_param_frame.pack()

        self.master.mainloop()

    def set_param_init(self):
        self.set_param_frame = Frame(width=400, height=300, bd=2)
        self.set_param_frame.grid_bbox(2, 3 + default_fields_count)

        self._buttons_init()

        self.texts = {}
        _vcmd = self.set_param_frame.register(self._validate)

        count = 0

        for block_name, block in default_params.items():
            Label(self.set_param_frame,
                  text=_convert(block_name),
                  background="#999",
                  justify=LEFT).grid(
                    row=count,
                    column=1
            )
            count += 1

            for name, _default in block.items():
                default, func = _default

                Label(self.set_param_frame,
                      text=_convert(name),
                      justify=LEFT).grid(
                        row=count,
                        column=1
                )
                self.texts[_convert(name)] = ""
                e = Entry(self.set_param_frame,
                          validate='key',
                          vcmd=(_vcmd, "%P", "%W"))
                e.grid(row=count,
                       column=2)

                self.texts[name] = e
                self.funcs[e] = func

                e.insert(0, default_params[block_name][name][0])

                count += 1

    def _buttons_init(self):
        self.load_button = Button(self.set_param_frame,
                                  text='Загрузить',
                                  state=DISABLED,
                                  command=self.load_button_press)
        self.load_button.grid(row=3 + default_fields_count,
                              column=1)

        self.start_button = Button(self.set_param_frame,
                                   text='Старт',
                                   command=self.start_button_press)
        self.start_button.grid(row=3 + default_fields_count,
                               column=2)

        self.master.protocol('WM_DELETE_WINDOW',
                             self.exit)

    def _validate(self, P, W):
        e = self.set_param_frame.nametowidget(W)
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
                block[key] = func(self.texts[key].get())

        return params

    def start_button_press(self):
        params = self._collect_params()

        self.game_screen = GameScreen(self.master, params)
        self.set_param_frame.forget()

    def load_button_press(self):
        pass

    def exit(self):
        exit()
