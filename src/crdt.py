import pickle
from typing import Generator, List
from uuid import UUID

from py3crdt.sequence import Sequence
from wrapt import synchronized

from src.position_generator import Position


class CRDT:
    def __init__(self, site_id: UUID):
        self._seq = Sequence(site_id)

    @property
    def site_id(self) -> int:
        return self._seq.id

    @synchronized
    def get_elements(self) -> List[chr]:
        return self._seq.elem_seq

    @synchronized
    def get_positions(self) -> List[Position]:
        return self._seq.id_seq

    @synchronized
    def insert(self, element: chr, position: Position):
        if self._seq.query(position):
            raise ValueError(f'Position already exists: {position}')
        self._seq.add(element, position)

    @synchronized
    def insert_many(self, elements: List[chr],
                    positions: Generator[Position, None, None]):
        for element, position in zip(elements, positions):
            self.insert(element, position)

    @synchronized
    def remove(self, position: Position):
        if not self._seq.query(position):
            raise ValueError(f'Position does not exist: {position}')
        self._seq.remove(position)

    @synchronized
    def merge(self, other: bytes):
        seq = pickle.loads(other)
        self._seq.merge(seq)

    def __repr__(self):
        return f'CRDT({self._seq})'

    @synchronized
    def pickle(self):
        return pickle.dumps(self._seq)


