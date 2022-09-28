
class View:
    def __init__(self):
        self.controller = None

    def initialise(self, controller: 'Controller'):
        self.controller = controller
