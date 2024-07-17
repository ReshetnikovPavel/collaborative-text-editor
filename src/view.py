from typing import List


class View:
    def __init__(self):
        self.controller = None
        self.editor = None
        self.doc_name = ''

    def initialise(self, controller: 'Controller', editor: 'Editor'):
        self.controller = controller
        self.editor = editor
        # self.update(self.controller.model.get_document())

    def update(self, lines: str):
        # self.editor.screen.nodelay(True)
        self.editor.buffer.lines = lines.split('\n')
