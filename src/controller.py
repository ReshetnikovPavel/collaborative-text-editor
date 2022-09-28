from typing import List

from node import Node
from src.glyphs import Glyph


class Controller:
    def __init__(self):
        self.node = None
        self.model = None
        self.view = None

    def initialise(self, model: 'Model', view: 'View'):
        self.model = model
        self.view = view
        self.node = Node(self, 'localhost', 0)

    def update_crdt(self, crdt):
        self.model.update_crdt(crdt)
        document = self.model.get_document(crdt.id)
        self.view.update(document)

    def send_crdt(self, crdt):
        self.node.send_to_nodes(crdt)

    def create_document(self, glyphs: List[Glyph]):
        document = self.model.create_document(glyphs)
        self.view.update(document)
