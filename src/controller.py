import contextlib
from random import randint
import socket
from typing import List
from uuid import UUID

from src.crdt import CRDT
from src.node import Node
from src.glyphs import Glyph
import pickle


def get_free_port():
    while True:
        port = randint(32768, 61000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not (sock.connect_ex(('127.0.0.1', port)) == 0):
            return port


class Controller:
    def __init__(self, site_id: UUID):
        self.node = None
        self.model = None
        self.view = None
        self.site_id = site_id

    def initialise(self, model: 'Model', view: 'View'):
        self.model = model
        self.view = view
        self.node = Node(self, 'localhost', get_free_port(), self.site_id)
        self.node.start()

    def update_crdt(self, pickled_crdt: bytes):
        self.model.update_crdt(pickled_crdt)
        document = self.model.get_document()
        self.view.update(document)

    def send_crdt(self, crdt: CRDT):
        pickled_crdt = crdt.pickle()
        self.node.send_to_nodes(str(len(pickled_crdt)))
        self.node.send_to_nodes(pickled_crdt, compression="zlib")

    def create_document(self, glyphs: List[Glyph]):
        document = self.model.create_document(glyphs)
        self.view.update(document)

    def connect_to(self, host: str, port: int):
        self.model.delete_current_document()
        self.node.connect_with_node(host, port)

    def on_someone_joined(self):
        self.send_crdt(self.model.get_document().crdt)

    def insert(self, glyph: Glyph, index: int):
        with self.document_to_be_updated() as document:
            document.insert(glyph, index)

    def remove(self, index: int):
        with self.document_to_be_updated() as document:
            document.remove(index)

    def get_host_port(self):
        return self.node.host, self.node.port

    def get_uuid(self):
        return self.node.id

    def blame(self, index: int):
        document = self.model.get_document()
        positions = document.crdt.get_positions()
        position = positions[index]
        latest_person_edited = position.ids[-1].site
        return latest_person_edited


    @contextlib.contextmanager
    def document_to_be_updated(self):
        document = self.model.get_document()
        yield document
        self.view.update(self.model.get_document())
        self.send_crdt(document.crdt)