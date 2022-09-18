import crdt
import glyphs
import position_generator
from typing import Generator


class Document:
    def __init__(self, string: str, site_id: int):
        self.crdt = crdt.CRDT(site_id)
        self.string = string

    def assign_positions(self):
        positions = position_generator.generate(len(self.string),
                                                self.crdt.site_id)
        self.crdt.insert_many(glyphs.get_from(self.string), positions)

