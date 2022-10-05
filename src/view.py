from src.glyphs import to_list_of_lists


class View:
    def __init__(self):
        self.controller = None
        self.editor = None

    def initialise(self, controller: 'Controller', editor: 'Editor'):
        self.controller = controller
        self.editor = editor
        self.update(self.controller.model.get_document())

    def update(self, document: 'Document'):
        self.editor.buffer.list = to_list_of_lists(document.glyphs)

