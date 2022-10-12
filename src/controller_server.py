import contextlib
import pickle
from typing import List

from src.crdt import CRDT
from src.model import Model
from src.node import Node
from src.view import View


class ControllerServer:
    def __init__(self, site_id: int):
        self.node = None
        self.model = None
        self.site_id = site_id
        self.rights = {}

    def initialise(self, model: Model, view):
        self.model = model
        self.node = Node(self, '127.0.0.1', self.site_id, self.site_id)
        self.node.start()

    def update_crdt(self, pickled_crdt: bytes, node):
        if (node.host, node.port) in self.rights and self.rights[(node.host, node.port)]:
            self.model.update_crdt(pickled_crdt)
        document = self.model.get_document()
        self.send_crdt(document.crdt)

    def send_crdt(self, crdt: CRDT):
        pickled_crdt = crdt.pickle()
        self.node.send_to_nodes(str(len(pickled_crdt)))
        self.node.send_to_nodes(pickled_crdt, compression="zlib")

    def create_document(self, glyphs: List[chr]):
        document = self.model.create_document(glyphs)

    def connect_to(self, host: str, port: int):
        self.model.delete_current_document()
        self.node.connect_with_node(host, port)

    def on_someone_joined(self, node):
        self.send_crdt(self.model.get_document().crdt)
        self.rights[(node.host, node.port)] = False

    def insert(self, glyph: chr, index: int):
        with self.document_to_be_updated() as document:
            document.insert(glyph, index)

    def remove(self, index: int):
        with self.document_to_be_updated() as document:
            document.remove(index)

    def get_host_port(self):
        return self.node.host, self.node.port

    def get_uuid(self):
        return self.node.id

    def set_rights(self, host, port, can_write: bool):
        if (host, port) in self.rights:
            self.rights[(host, port)] = can_write
        self.node.send_to_nodes(pickle.dumps((host, port, can_write)), compression='zlib')
        self.send_crdt(self.model.get_document().crdt)

    def blame(self, index: int) -> int:
        document = self.model.get_document()
        position = document.crdt.positions[index]
        latest_person_edited = position.ids[-1].site
        return latest_person_edited

    @contextlib.contextmanager
    def document_to_be_updated(self):
        document = self.model.get_document()
        yield document
        self.send_crdt(document.crdt)
