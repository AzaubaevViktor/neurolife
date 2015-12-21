import pickle
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from view.game_screen import GameScreen


class InitScreenController:
    def __init__(self, master):
        self.master = master
        self.model = None

    def start_button_press(self, params):
        if self.model:
            self.game_screen = GameScreen(self.master, params, world=self.model)
        else:
            self.game_screen = GameScreen(self.master, params)

    def load_button_press(self):
        filename = askopenfilename()
        if filename:
            try:
                self.model = pickle.load(open(filename, "rb"))
            except Exception as e:
                messagebox.showerror("Не удалось открыть файл", str(e))
                return False
        return self.model
