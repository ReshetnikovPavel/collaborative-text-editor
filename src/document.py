from typing import List
from uuid import UUID

import src.position_generator as position_generator
from src.crdt import CRDT
from src.position_generator import Position


class Document:
    def __init__(self, glyphs: List[chr], site_id: UUID):
        self._crdt = CRDT(site_id)
        self._glyphs = glyphs
        self._converter = IndexPositionConverter(self._crdt, self.site_id)
        if glyphs:
            self._assign_positions()

    def _assign_positions(self):
        positions = position_generator.generate(len(self._glyphs),
                                                self.site_id)
        self._crdt.insert_many(self._glyphs, positions)

    @property
    def site_id(self) -> UUID:
        return self._crdt.site_id

    def insert(self, element: chr, index: int):
        position = self._converter.generate_new_position(index)
        self._crdt.insert(element, position)
        self._update_glyphs_local()

    def remove(self, index: int):
        position = self._converter.convert_index_to_position(index)
        self._crdt.remove(position)
        self._update_glyphs_local()

    def _update_glyphs_local(self):
        self._glyphs = self._crdt.get_elements()

    @property
    def glyphs(self) -> List[chr]:
        return self._glyphs

    @property
    def crdt(self) -> CRDT:
        return self._crdt

    def update_crdt(self, pickled_crdt: bytes):
        self._crdt.merge(pickled_crdt)
        self._update_glyphs_local()


class IndexPositionConverter:
    def __init__(self, crdt: CRDT, site_id: int):
        self.crdt = crdt
        self.site_id = site_id

    def convert_index_to_position(self, index: int) -> Position:
        return self.crdt.get_positions()[index]

    def convert_position_to_index(self, position: Position) -> int:
        return self.crdt.get_positions().index(position)

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
        positions = self.crdt.get_positions()
        if len(positions) > 0:
            other_id = positions[0].ids[0].site
        else:
            other_id = self.site_id
        return self.site_id if self.site_id < other_id else other_id


    def _generate_position_between_index_and_next_index(self,
                                                        index) -> Position:
        return position_generator.generate_between(
            self.crdt.get_positions()[index],
            self._get_next_position(index),
            self.site_id)

    def _get_next_position(self, index: int):
        if index != len(self.crdt.get_positions()) - 1:
            return self.crdt.get_positions()[index + 1]
        return Position.get_max(self.site_id)

    def _get_position(self, index: int):
        if index != 0:
            return self.crdt.get_positions()[index - 1]
        return Position.get_min(self.site_id)
