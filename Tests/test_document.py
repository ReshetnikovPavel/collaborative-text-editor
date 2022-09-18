import contextlib
import sys
import unittest
from io import StringIO

from glyphs import Character
import crdt
from document import Document
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

    # TODO: хз почему не работает
    # def test_assign_positions(self):
    #     string = 'Hello World'
    #     document = Document(string, 0)
    #
    #     expected_positions = [Position([Identifier(0, 0), Identifier(1, 0)]),
    #                           Position([Identifier(0, 0), Identifier(2, 0)]),
    #                           Position([Identifier(0, 0), Identifier(3, 0)]),
    #                           Position([Identifier(0, 0), Identifier(4, 0)]),
    #                           Position([Identifier(0, 0), Identifier(5, 0)]),
    #                           Position([Identifier(0, 0), Identifier(6, 0)]),
    #                           Position([Identifier(0, 0), Identifier(7, 0)]),
    #                           Position([Identifier(0, 0), Identifier(8, 0)]),
    #                           Position([Identifier(0, 0), Identifier(9, 0)]),
    #                           Position([Identifier(0, 0), Identifier(10, 0)]),
    #                           Position([Identifier(0, 0), Identifier(11, 0)])]
    #     expected_glyphs = [Character('H'), Character('e'), Character('l'),
    #                        Character('l'), Character('o'), Character(' '),
    #                        Character('W'), Character('o'), Character('r'),
    #                        Character('l'), Character('d')]
    #
    #     document.assign_positions()
    #
    #     with captured_output() as (out, err):
    #         document.crdt._seq.display()
    #         self.assertTrue(repr(expected_positions) in out)
    #         self.assertTrue(repr(expected_glyphs) in out)




