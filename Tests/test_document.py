import contextlib
import sys
import unittest
from io import StringIO

from document import Document, IndexPositionConverter
from glyphs import Character
from position_generator import Position, Identifier


@contextlib.contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class Base(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestDocument(Base):
    def test_init(self):
        string = 'Hello World'
        document = Document(string, 0)

        self.assertEqual(document.string, string)
        self.assertEqual(document.crdt.site_id, 0)
        self.assertTrue(len(document.crdt.positions) != 0)

    def test_insert(self):
        document = Document('', 0)

        document.insert(Character('a'), 0)

        self.assertEqual(document.string, 'a')

    def test_insert_multiple(self):
        document = Document('', 0)

        document.insert(Character('a'), 0)
        document.insert(Character('b'), 1)

        self.assertEqual(document.string, 'ab')

    def test_insert_inside(self):
        document = Document('abc', 0)

        document.insert(Character('d'), 1)

        self.assertEqual(document.string, 'adbc')

    def test_insert_first(self):
        document = Document('abc', 0)

        document.insert(Character('d'), 0)

        self.assertEqual(document.string, 'dabc')

    def test_insert_multiple_inside(self):
        document = Document('abc', 0)

        document.insert(Character('d'), 1)
        document.insert(Character('e'), 2)

        self.assertEqual(document.string, 'adebc')

    def test_insert_index_greater_than_length(self):
        document = Document('abc', 0)
        with self.assertRaises(IndexError):
            document.insert(Character('d'), 4)

    def test_insert_next(self):
        document = Document('abc', 0)

        document.insert(Character('d'), 3)

        self.assertEqual(document.string, 'abcd')

    def test_get_next_position_not_last(self):
        document = Document('abc', 0)

        position = document.converter._get_next_position(0)

        self.assertEqual(position,
                         Position([Identifier(0, 0), Identifier(2, 0)]))

    def test_get_next_position_last(self):
        site = 0
        document = Document('abc', site)

        position = document.converter._get_next_position(2)

        self.assertEqual(position,
                         Position.get_max(site))

    def test_get_next_position_before_first_one(self):
        document = Document('abc', 0)

        position = document.converter._get_next_position(-1)

        self.assertEqual(position,
                         Position([Identifier(0, 0), Identifier(1, 0)]))

    def test_generate_position_after_first_one(self):
        document = Document('abc', 0)
        converter = document.converter

        position = converter._generate_position_between_index_and_next_index(0)

        self.assertEqual(
            position,
            Position([Identifier(0, 0), Identifier(1, 0), Identifier(1, 0)]))

    def test_generate_position_after_last_one(self):
        document = Document('abc', 0)
        converter = document.converter

        position = converter._generate_position_between_index_and_next_index(2)

        self.assertEqual(
            position,
            Position([Identifier(0, 0), Identifier(4, 0)]))

    def test_generate_position_after_middle_one(self):
        document = Document('abc', 0)
        converter = document.converter

        position = converter._generate_position_between_index_and_next_index(1)

        self.assertEqual(
            position,
            Position([Identifier(0, 0), Identifier(2, 0), Identifier(1, 0)]))

    def test_generate_first_position(self):
        document = Document('', 0)

        position = document.converter._generate_first_position()

        self.assertEqual(
            position,
            Position([Identifier(0, 0), Identifier(1, 0)]))

    def test_generate_first_position_with_existing(self):
        document = Document('a', 0)

        position = document.converter._generate_first_position()

        self.assertEqual(
            position,
            Position([Identifier(0, 0), Identifier(0, 0), Identifier(1, 0)]))

    def test_remove(self):
        document = Document('abc', 0)

        document.remove(1)

        self.assertEqual(document.string, 'ac')

    def test_remove_first(self):
        document = Document('abc', 0)

        document.remove(0)

        self.assertEqual(document.string, 'bc')

    def test_remove_last(self):
        document = Document('abc', 0)

        document.remove(2)

        self.assertEqual(document.string, 'ab')

    def test_remove_out_of_bounds(self):
        document = Document('abc', 0)
        with self.assertRaises(IndexError):
            document.remove(3)
