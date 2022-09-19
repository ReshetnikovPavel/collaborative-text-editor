from typing import List

import glyphs
import position_generator
from crdt import CRDT
from position_generator import Position


class Document:
    def __init__(self, glyphs: List[glyphs.Glyph], site_id: int):
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
    def site_id(self) -> int:
        return self._crdt.site_id

    def insert(self, element: glyphs.Glyph, index: int):
        position = self._converter.generate_new_position(index)
        self._crdt.insert(element, position)
        self._update_glyphs_local()

    def remove(self, index: int):
        position = self._converter.convert_index_to_position(index)
        self._crdt.remove(position)
        self._update_glyphs_local()

    def _update_glyphs_local(self):
        self._glyphs = self._crdt.elements


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
        return position_generator.generate_between(
            Position.get_min(self.site_id),
            self._get_next_position(-1),
            self.site_id)

    def _generate_position_between_index_and_next_index(self,
                                                        index) -> Position:
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
