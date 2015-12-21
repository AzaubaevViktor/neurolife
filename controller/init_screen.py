import pickle
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


class InitScreenController:
    def __init__(self, master):
        self.master = master
        self.model = None

    def load_button_press(self):
        filename = askopenfilename()
        if filename:
            try:
                self.model = pickle.load(open(filename, "rb"))
            except Exception as e:
                messagebox.showerror("Не удалось открыть файл", str(e))
                return False
        return self.model
