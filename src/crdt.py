import pickle
from typing import Generator, List
from uuid import UUID

from wrapt import synchronized

from src.position_generator import Position
from src.sequence import Sequence


class CRDT:
    def __init__(self, site_id: int):
        self._seq = Sequence(site_id)

    @property
    def site_id(self) -> int:
        return self._seq.site_id


    @property
    @synchronized
    def lines(self) -> List[str]:
        return self._seq.to_string().splitlines()

    @property
    @synchronized
    def positions(self) -> List[Position]:
        return list(self._seq.ids)

    @synchronized
    def insert(self, element: chr, position: Position):
        if self._seq.contains_id(position):
            raise ValueError(f'Position already exists: {position}')
        self._seq.add(element, position)

    @synchronized
    def insert_many(self, elements: List[chr],
                    positions: Generator[Position, None, None]):
        for element, position in zip(elements, positions):
            self.insert(element, position)

    @synchronized
    def remove(self, position: Position):
        if not self._seq.contains_id(position):
            raise ValueError(f'Position does not exist: {position}')
        self._seq.remove(position)

    @synchronized
    def merge(self, other: bytes):
        seq = pickle.loads(other)
        self._seq.merge(seq)

    @synchronized
    def replace(self, other: bytes):
        seq = pickle.loads(other)
        self._seq = seq

    def __repr__(self):
        return f'CRDT({self._seq})'

    def pickle(self):
        return pickle.dumps(self._seq)
