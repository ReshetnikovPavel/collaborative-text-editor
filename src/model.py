
class Model:
    def __init__(self):
        self.controller = None
        self.documents = []
        self.current_document = None

    def initialise(self, controller: 'Controller'):
        self.controller = controller

    def get_document(self) -> 'Document':
        return self.current_document
