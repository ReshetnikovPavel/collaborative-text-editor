import unittest
import uuid
from typing import List

from src.crdt import CRDT
from src.document import Document
from src.position_generator import Position, Identifier


class Base(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestDocument(Base):
    def test_init(self):
        string = 'Hello World'
        document = Document(list(string), 0)

        self.assertEqual(''.join(document._glyphs), string)
        self.assertEqual(document._crdt.site_id, 0)
        self.assertTrue(len(document._crdt.get_positions()) != 0)

    def assert_glyphs_equal_to_string(self, glyphs_list: List[chr],
                                      string: str):
        self.assertEqual(''.join(glyphs_list), string)

    def test_insert(self):
        document = Document([], 0)

        document.insert('a', 0)

        self.assert_glyphs_equal_to_string(document._glyphs, 'a')

    def test_insert_multiple(self):
        document = Document([], 0)

        document.insert('a', 0)
        document.insert('b', 1)

        self.assert_glyphs_equal_to_string(document._glyphs, 'ab')

    def test_insert_inside(self):
        document = Document(list('abc'), 0)

        document.insert('d', 1)

        self.assert_glyphs_equal_to_string(document._glyphs, 'adbc')

    def test_insert_first(self):
        document = Document(list('abc'), 0)

        document.insert('d', 0)

        self.assert_glyphs_equal_to_string(document._glyphs, 'dabc')

    def test_insert_multiple_inside(self):
        document = Document(list('abc'), 0)

        document.insert('d', 1)
        document.insert('e', 2)

        self.assert_glyphs_equal_to_string(document._glyphs, 'adebc')

    def test_insert_index_greater_than_length(self):
        document = Document(list('abc'), 0)
        with self.assertRaises(IndexError):
            document.insert('d', 4)

    def test_insert_next(self):
        document = Document(list('abc'), 0)

        document.insert('d', 3)

        self.assert_glyphs_equal_to_string(document._glyphs, 'abcd')

    def test_get_next_position_not_last(self):
        document = Document(list('abc'), 0)

        position = document._converter._get_next_position(0)

        self.assertEqual(position,
                         Position([Identifier(0, 0), Identifier(2, 0)]))

    def test_get_next_position_last(self):
        site = 0
        document = Document(list('abc'), site)

        position = document._converter._get_next_position(2)

        self.assertEqual(position,
                         Position.get_max(site))

    def test_get_next_position_before_first_one(self):
        document = Document(list('abc'), 0)

        position = document._converter._get_next_position(-1)

        self.assertEqual(position,
                         Position([Identifier(0, 0), Identifier(1, 0)]))

    def test_generate_position_after_first_one(self):
        document = Document(list('abc'), 0)
        converter = document._converter

        position = converter._generate_position_between_index_and_next_index(0)

        self.assertEqual(
            position,
            Position([Identifier(0, 0), Identifier(1, 0), Identifier(1, 0)]))

    def test_generate_position_after_last_one(self):
        document = Document(list('abc'), 0)
        converter = document._converter

        position = converter._generate_position_between_index_and_next_index(2)

        self.assertEqual(
            position,
            Position([Identifier(0, 0), Identifier(4, 0)]))

    def test_generate_position_after_middle_one(self):
        document = Document(list('abc'), 0)
        converter = document._converter

        position = converter._generate_position_between_index_and_next_index(1)

        self.assertEqual(
            position,
            Position([Identifier(0, 0), Identifier(2, 0), Identifier(1, 0)]))

    def test_generate_first_position(self):
        document = Document(list('abc'), 0)

        position = document._converter._generate_first_position()

        self.assertEqual(
            position,
            Position([Identifier(0, 0), Identifier(0, 0), Identifier(1, 0)]))

    def test_generate_first_position_with_existing(self):
        document = Document(list('abc'), 0)

        position = document._converter._generate_first_position()

        self.assertEqual(
            position,
            Position([Identifier(0, 0), Identifier(0, 0), Identifier(1, 0)]))

    def test_remove(self):
        document = Document(list('abc'), 0)

        document.remove(1)

        self.assert_glyphs_equal_to_string(document._glyphs, 'ac')

    def test_remove_first(self):
        document = Document(list('abc'), 0)

        document.remove(0)

        self.assert_glyphs_equal_to_string(document._glyphs, 'bc')

    def test_remove_last(self):
        document = Document(list('abc'), 0)

        document.remove(2)

        self.assert_glyphs_equal_to_string(document._glyphs, 'ab')

    def test_remove_out_of_bounds(self):
        document = Document(list('abc'), 0)
        with self.assertRaises(IndexError):
            document.remove(3)

    def test_update_crdt(self):
        document = Document([], 1)
        crdt = CRDT(0)
        crdt.insert('a',
                    Position([Identifier(0, 0), Identifier(1, 0)]))
        crdt.insert('b',
                    Position([Identifier(0, 0), Identifier(2, 0)]))
        crdt.insert('c',
                    Position([Identifier(0, 0), Identifier(3, 0)]))
        document.insert('a', 0)
        document.insert('b', 1)
        pickled_crdt = crdt.pickle()
        document.update_crdt(pickled_crdt)
        self.assert_glyphs_equal_to_string(document._glyphs, 'abcab')
