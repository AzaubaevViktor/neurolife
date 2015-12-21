import pickle

from model import World


class GameScreenController:
    def __init__(self, params, model=None):

        if model:
            model.init_param(params)

        self.model = model if model else World(params)

    def save_pressed(self, filename):
        pickle.dump(self.model, open(filename, "wb"))

    def add_pressed(self):
        self.model.create_creature()

    def run(self):
        self.model.step()
