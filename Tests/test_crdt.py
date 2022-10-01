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

        self.assertEqual(crdt.get_elements(), [])

    def test_positions_empty(self):
        crdt = CRDT(0)

        self.assertEqual(crdt.get_positions(), [])

    def test_elements(self):
        crdt = CRDT(0)
        char = Character('a')
        crdt.insert(char, Position([Identifier(0, 0)]))

        self.assertEqual(crdt.get_elements(), [char])

    def test_positions(self):
        crdt = CRDT(0)
        char = Character('a')
        position = Position([Identifier(0, 0)])
        crdt.insert(char, position)

        self.assertEqual(crdt.get_positions(), [position])

    def test_insert(self):
        crdt = CRDT(0)
        char = Character('a')
        position = Position([Identifier(0, 0)])

        crdt.insert(char, position)

        self.assertEqual(crdt.get_elements(), [char])
        self.assertEqual(crdt.get_positions(), [position])

    def test_remove(self):
        crdt = CRDT(0)
        char = Character('a')
        position = Position([Identifier(0, 0)])
        crdt.insert(char, position)

        crdt.remove(position)

        self.assertEqual(crdt.get_elements(), [])
        self.assertEqual(crdt.get_positions(), [])

    def test_merge(self):
        crdt1 = CRDT(0)
        crdt2 = CRDT(1)
        char = Character('a')
        position1 = Position([Identifier(0, 0)])
        position2 = Position([Identifier(1, 0)])
        crdt1.insert(char, position1)
        crdt2.insert(char, position2)

        pickled_crdt2 = crdt2.pickle()
        crdt1.merge(pickled_crdt2)

        self.assertEqual(crdt1.get_elements(), [char, char])
        self.assertEqual(crdt1.get_positions(), [position1, position2])

        self.assertEqual(crdt2.get_elements(), [char])
        self.assertEqual(crdt2.get_positions(), [position2])

    def test_insert_already_exists(self):
        crdt = CRDT(0)
        char = Character('a')
        position = Position([Identifier(0, 0)])
        crdt.insert(char, position)

        with self.assertRaises(KeyError):
            crdt.insert(char, position)

    def test_remove_do_not_exist(self):
        crdt = CRDT(0)
        position = Position([Identifier(0, 0)])

        with self.assertRaises(KeyError):
            crdt.remove(position)

    def test_delete_positions_suppressing_key_errors(self):
        crdt = CRDT(0)
        char = Character('a')
        position = Position([Identifier(0, 0)])
        char2 = Character('b')
        position2 = Position([Identifier(0, 0), Identifier(0, 1)])
        crdt.insert(char, position)
        crdt.insert(char2, position2)

        crdt._delete_positions_suppressing_key_errors(
            {position2, Position([Identifier(0, 1)])})

        self.assertEqual(crdt.get_elements(), [char])
