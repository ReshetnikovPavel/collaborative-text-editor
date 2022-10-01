from typing import List
from uuid import UUID

from src.crdt import CRDT
from src.glyphs import Glyph
from src.document import Document


class Model:
    def __init__(self, site_id: UUID):
        self.controller = None
        self.documents = []
        self.site_id = site_id
        self.current_document = Document([], self.site_id)

    def initialise(self, controller: 'Controller'):
        self.controller = controller

    def create_document(self, glyphs: List[Glyph]) -> Document:
        document = Document(glyphs, self.site_id)
        self.documents.append(document)
        self.current_document = document
        return document

    def get_document(self) -> Document:
        return self.current_document

    def update_crdt(self, pickled_crdt: bytes):
        self.current_document.update_crdt(pickled_crdt)
