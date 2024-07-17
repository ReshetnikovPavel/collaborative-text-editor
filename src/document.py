from typing import List

import src.position_generator as position_generator
from src.crdt import CRDT
from src.position_generator import Position


class Document:
    def __init__(self, elements: List[chr], site_id: int):
        self._crdt = CRDT(site_id)
        self._converter = IndexPositionConverter(self._crdt, self.site_id)
        if elements:
            self._assign_positions(elements)

    def _assign_positions(self, elements: List[chr]):
        positions = position_generator.generate(len(elements),
                                                self.site_id)
        self._crdt.insert_many(elements, positions)

    @property
    def site_id(self) -> int:
        return self._crdt.site_id

    def insert(self, element: chr, index: int):
        position = self._converter.generate_new_position(index)
        self._crdt.insert(element, position)

    def remove(self, index: int):
        position = self._converter.convert_index_to_position(index)
        self._crdt.remove(position)

    @property
    def lines(self) -> List[str]:
        return self._crdt.lines

    @property
    def crdt(self) -> CRDT:
        return self._crdt

    def update_crdt(self, pickled_crdt: bytes):
        self._crdt.merge(pickled_crdt)


class IndexPositionConverter:
    def __init__(self, crdt: CRDT, site_id: int):
        self.crdt = crdt
        self.site_id = site_id

    def convert_index_to_position(self, index: int) -> Position:
        return self.crdt.positions[index]

    def convert_position_to_index(self, position: Position) -> int:
        return self.crdt.positions.index(position)

    def generate_new_position(self, index: int) -> Position:
        if index == 0:
            return self._generate_first_position()
        return self._generate_position_between_index_and_next_index(index - 1)

    def _generate_first_position(self) -> Position:
        first_site_id = self._get_site_on_first_position()
        return position_generator.generate_between(
            Position.get_min(first_site_id),
            self._get_next_position(-1),
            self.site_id)

    def _get_site_on_first_position(self):
        positions = self.crdt.positions
        if len(positions) > 0:
            other_id = positions[0].ids[0].site
        else:
            other_id = self.site_id
        return self.site_id if self.site_id < other_id else other_id

    def _generate_position_between_index_and_next_index(self,
                                                        index) -> Position:
        if index >= len(self.crdt.positions):
            index = len(self.crdt.positions)-1
        return position_generator.generate_between(
            self.crdt.positions[index],
            self._get_next_position(index),
            self.site_id)

    def _get_next_position(self, index: int):
        if index != len(self.crdt.positions) - 1:
            return self.crdt.positions[index + 1]
        return Position.get_max(self.site_id)

    def _get_position(self, index: int):
        if index != 0:
            return self.crdt.positions[index - 1]
        return Position.get_min(self.site_id)
