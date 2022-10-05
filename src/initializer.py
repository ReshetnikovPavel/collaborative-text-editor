import uuid

from src.model import Model
from src.view import View
from src.controller import Controller

class Initializer:
    def __init__(self):
        self.site_id = _generate_unique_id()
        self.model = Model(self.site_id)
        self.view = View()
        self.controller = Controller(self.site_id)

    def initialise(self):
        self.controller.initialise(self.model, self.view)
        self.model.initialise(self.controller)
        self.view.initialise(self.controller)

def _generate_unique_id() -> uuid.UUID:
    return uuid.uuid4()