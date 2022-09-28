import unittest
from src.crdt import CRDT
from src.position_generator import Position, Identifier
from src.glyphs import Character


class Base(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestCRDT(Base):
    def test_site_id(self):
        crdt = CRDT(0)

        self.assertEqual(crdt.site_id, 0)

    def test_elements_empty(self):
        crdt = CRDT(0)

        self.assertEqual(crdt.elements, [])

    def test_positions_empty(self):
        crdt = CRDT(0)

        self.assertEqual(crdt.positions, [])

    def test_elements(self):
        crdt = CRDT(0)
        char = Character('a')
        crdt.insert(char, Position([Identifier(0, 0)]))

        self.assertEqual(crdt.elements, [char])

    def test_positions(self):
        crdt = CRDT(0)
        char = Character('a')
        position = Position([Identifier(0, 0)])
        crdt.insert(char, position)

        self.assertEqual(crdt.positions, [position])

    def test_insert(self):
        crdt = CRDT(0)
        char = Character('a')
        position = Position([Identifier(0, 0)])

        crdt.insert(char, position)

        self.assertEqual(crdt.elements, [char])
        self.assertEqual(crdt.positions, [position])

    def test_remove(self):
        crdt = CRDT(0)
        char = Character('a')
        position = Position([Identifier(0, 0)])
        crdt.insert(char, position)

        crdt.remove(position)

        self.assertEqual(crdt.elements, [])
        self.assertEqual(crdt.positions, [])

    def test_merge(self):
        crdt1 = CRDT(0)
        crdt2 = CRDT(1)
        char = Character('a')
        position1 = Position([Identifier(0, 0)])
        position2 = Position([Identifier(1, 0)])
        crdt1.insert(char, position1)
        crdt2.insert(char, position2)

        crdt1.merge(crdt2)

        self.assertEqual(crdt1.elements, [char, char])
        self.assertEqual(crdt1.positions, [position1, position2])

        self.assertEqual(crdt2.elements, [char])
        self.assertEqual(crdt2.positions, [position2])

    def test_insert_already_exists(self):
        crdt = CRDT(0)
        char = Character('a')
        position = Position([Identifier(0, 0)])
        crdt.insert(char, position)

        with self.assertRaises(ValueError):
            crdt.insert(char, position)

    def test_remove_do_not_exist(self):
        crdt = CRDT(0)
        position = Position([Identifier(0, 0)])

        with self.assertRaises(ValueError):
            crdt.remove(position)


