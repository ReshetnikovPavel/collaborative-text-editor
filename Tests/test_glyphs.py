import unittest

import glyphs


class Base(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestFunctions(Base):
    def test_get_from(self):
        string = 'Hello World'

        actual_glyphs = list(glyphs.get_from(string))
        values = [glyph.draw() for glyph in actual_glyphs]

        self.assertEqual(
            values, ['H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd'])
