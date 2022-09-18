from typing import Generator

from py3crdt.sequence import Sequence
from position_generator import Position
from glyphs import Glyph


class CRDT:
    def __init__(self, site_id: int):
        self._seq = Sequence(site_id)

    @property
    def site_id(self) -> int:
        return self._seq.id

    def insert(self, element: Glyph, position: Position):
        self._seq.add(element, position)

    def insert_many(self, elements: Generator[Glyph, None, None],
                    positions: Generator[Position, None, None]):
        for element, position in zip(elements, positions):
            self.insert(element, position)

    def remove(self, position: Position):
        self._seq.remove(position)

    def merge(self, other: 'CRDT'):
        self._seq.merge(other._seq)
