from typing import List

from src.document import Document


class Model:
    def __init__(self, site_id: int):
        self.controller = None
        self.site_id = site_id
        self.current_document = Document([], self.site_id)
        self.documents = [self.current_document]

    def initialise(self, controller: 'Controller'):
        self.controller = controller

    def create_document(self, glyphs: List[chr]) -> Document:
        document = Document(glyphs, self.site_id)
        self.documents.append(document)
        self.current_document = document
        return document

    def get_document(self) -> Document:
        return self.current_document

    def update_crdt(self, pickled_crdt: bytes):
        self.current_document.update_crdt(pickled_crdt)

    def delete_current_document(self):
        self.documents.remove(self.current_document)
        self.current_document = Document([], self.site_id)
