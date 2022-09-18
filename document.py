import glyphs
import position_generator
from crdt import CRDT
from position_generator import Position


class Document:
    def __init__(self, string: str, site_id: int):
        self.crdt = CRDT(site_id)
        self.string = string
        self.converter = IndexPositionConverter(self.crdt, self.site_id)
        if string != '':
            self._assign_positions()

    def _assign_positions(self):
        positions = position_generator.generate(len(self.string), self.site_id)
        self.crdt.insert_many(glyphs.get_from(self.string), positions)

    @property
    def site_id(self) -> int:
        return self.crdt.site_id

    def insert(self, element: glyphs.Glyph, index: int):
        position = self.converter.generate_new_position(index)
        self.crdt.insert(element, position)
        self._update_string_local()

    def remove(self, index: int):
        position = self.converter.convert_index_to_position(index)
        self.crdt.remove(position)
        self._update_string_local()

    def _update_string_local(self):
        self.string = ''.join([glyph.draw() for glyph in self.crdt.elements])


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