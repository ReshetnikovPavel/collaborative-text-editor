import pickle
from typing import Generator, List, Set
from uuid import UUID

from sortedcontainers import SortedDict

from src.glyphs import Glyph
from src.position_generator import Position
from wrapt import synchronized


class CRDT:
    def __init__(self, site_id: UUID):
        self._sorted_dict = SortedDict()
        self._site_id = site_id
        self._deleted_positions = set()

    @property
    def site_id(self) -> UUID:
        return self._site_id

    @synchronized
    def get_elements(self) -> List[Glyph]:
        return list(self._sorted_dict.values())

    @synchronized
    def get_positions(self) -> List[Position]:
        return list(self._sorted_dict.keys())

    @synchronized
    def insert(self, element: Glyph, position: Position):
        if position in self._sorted_dict.keys():
            raise KeyError(f'Position already exists {position}')
        self._sorted_dict[position] = element

    @synchronized
    def insert_many(self, elements: List[Glyph],
                    positions: Generator[Position, None, None]):
        for element, position in zip(elements, positions):
            self.insert(element, position)

    @synchronized
    def remove(self, position: Position):
        self._deleted_positions.add(position)
        del self._sorted_dict[position]

    @synchronized
    def merge(self, pickled_crdt: bytes):
        sorted_dict, deleted_positions = pickle.loads(pickled_crdt)
        print(f'Merging {sorted_dict} and {deleted_positions}')
        self._delete_positions_suppressing_key_errors(deleted_positions)
        self._insert_positions_from(sorted_dict)

    def _insert_positions_from(self, sorted_dict: SortedDict):
        for position, glyph in sorted_dict.items():
            self._sorted_dict[position] = glyph

    def _delete_positions_suppressing_key_errors(
            self, positions_to_delete: Set[Glyph]):
        for position in positions_to_delete:
            try:
                del self._sorted_dict[position]
            except KeyError:
                pass

    @synchronized
    def pickle(self):
        return pickle.dumps((self._sorted_dict, self._deleted_positions))

    @synchronized
    def __repr__(self):
        return f'CRDT({self._sorted_dict.values()})'
