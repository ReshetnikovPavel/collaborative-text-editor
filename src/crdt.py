from typing import Generator, List

from py3crdt.sequence import Sequence

from glyphs import Glyph
from position_generator import Position


class CRDT:
    def __init__(self, site_id: int):
        self._seq = Sequence(site_id)

    @property
    def site_id(self) -> int:
        return self._seq.id

    @property
    def elements(self) -> List[Glyph]:
        return self._seq.elem_seq

    @property
    def positions(self) -> List[Position]:
        return self._seq.id_seq

    def insert(self, element: Glyph, position: Position):
        if self._seq.query(position):
            raise ValueError(f'Position already exists: {position}')
        self._seq.add(element, position)

    def insert_many(self, elements: List[Glyph],
                    positions: Generator[Position, None, None]):
        for element, position in zip(elements, positions):
            self.insert(element, position)

    def remove(self, position: Position):
        if not self._seq.query(position):
            raise ValueError(f'Position does not exist: {position}')
        self._seq.remove(position)

    def merge(self, other: 'CRDT'):
        self._seq.merge(other._seq)
