from py3crdt.sequence import Sequence
from index_generator import Position


class CRDT:
    def __init__(self, site_id: int):
        self._seq = Sequence(site_id)

    @property
    def site_id(self) -> int:
        return self._seq.id

    def insert(self, element, position: Position):
        self._seq.add(element, position)

    def remove(self, element):
        self._seq.remove(element)

    def merge(self, other: 'CRDT'):
        self._seq.merge(other._seq)
