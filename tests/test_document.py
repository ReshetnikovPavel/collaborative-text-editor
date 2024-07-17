import unittest
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

        self.assertEqual(document.lines, string)
        self.assertEqual(document._crdt.site_id, 0)
        self.assertTrue(len(document._crdt.positions) != 0)

    def test_insert(self):
        document = Document([], 0)

        document.insert('a', 0)

        self.assertEqual(document.lines, 'a')

    def test_insert_multiple(self):
        document = Document([], 0)

        document.insert('a', 0)
        document.insert('b', 1)

        self.assertEqual(document.lines, 'ab')

    def test_insert_inside(self):
        document = Document(list('abc'), 0)

        document.insert('d', 1)

        self.assertEqual(document.lines, 'adbc')

    def test_insert_first(self):
        document = Document(list('abc'), 0)

        document.insert('d', 0)

        self.assertEqual(document.lines, 'dabc')

    def test_insert_multiple_inside(self):
        document = Document(list('abc'), 0)

        document.insert('d', 1)
        document.insert('e', 2)

        self.assertEqual(document.lines, 'adebc')

    def test_insert_next(self):
        document = Document(list('abc'), 0)

        document.insert('d', 3)

        self.assertEqual(document.lines, 'abcd')

    def test_get_next_position_not_last(self):
        document = Document(list('abc'), 0)

        position = document._converter._get_next_position(0)

        self.assertEqual(position.ids,
                         Position([Identifier(0, 0), Identifier(2, 0)]).ids)

    def test_get_next_position_last(self):
        site = 0
        document = Document(list('abc'), site)

        position = document._converter._get_next_position(2)

        self.assertEqual(position.ids,
                         Position.get_max(site).ids)

    def test_get_next_position_before_first_one(self):
        document = Document(list('abc'), 0)

        position = document._converter._get_next_position(-1)

        self.assertEqual(position.ids,
                         Position([Identifier(0, 0), Identifier(1, 0)]).ids)

    def test_generate_position_after_first_one(self):
        document = Document(list('abc'), 0)
        converter = document._converter

        position = converter._generate_position_between_index_and_next_index(0)

        self.assertEqual(
            position.ids,
            Position([Identifier(0, 0), Identifier(1, 0), Identifier(1, 0)]).ids)

    def test_generate_position_after_last_one(self):
        document = Document(list('abc'), 0)
        converter = document._converter

        position = converter._generate_position_between_index_and_next_index(2)

        self.assertEqual(
            position.ids,
            Position([Identifier(0, 0), Identifier(4, 0)]).ids)

    def test_generate_position_after_middle_one(self):
        document = Document(list('abc'), 0)
        converter = document._converter

        position = converter._generate_position_between_index_and_next_index(1)

        self.assertEqual(
            position.ids,
            Position([Identifier(0, 0), Identifier(2, 0), Identifier(1, 0)]).ids)

    def test_generate_first_position(self):
        document = Document(list('abc'), 0)

        position = document._converter._generate_first_position()

        self.assertEqual(
            position.ids,
            Position([Identifier(0, 0), Identifier(0, 0), Identifier(1, 0)]).ids)

    def test_generate_first_position_with_existing(self):
        document = Document(list('abc'), 0)

        position = document._converter._generate_first_position()

        self.assertEqual(
            position.ids,
            Position([Identifier(0, 0), Identifier(0, 0), Identifier(1, 0)]).ids)

    def test_remove(self):
        document = Document(list('abc'), 0)

        document.remove(1)

        self.assertEqual(document.lines, 'ac')

    def test_remove_first(self):
        document = Document(list('abc'), 0)

        document.remove(0)

        self.assertEqual(document.lines, 'bc')

    def test_remove_last(self):
        document = Document(list('abc'), 0)

        document.remove(2)

        self.assertEqual(document.lines, 'ab')

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
        self.assertEqual(document.lines, 'abcab')
