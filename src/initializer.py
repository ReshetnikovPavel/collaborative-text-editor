from model import Model
from view import View
from controller import Controller


class Initializer:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.controller = Controller()

    def initialise(self):
        self.controller.initialise(self.model, self.view)
        self.model.initialise(self.controller)
        self.view.initialise(self.controller)
