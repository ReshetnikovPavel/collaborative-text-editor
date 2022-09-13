import unittest
from index_generator import Identifier, Position, Char


class Base(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestIdentifier(Base):
    def test_init(self):
        digit = 1
        site = 0

        identifier = Identifier(digit, site)

        self.assertEqual(identifier.digit, digit)
        self.assertEqual(identifier.site, site)

    def test_different_digits_same_site_less(self):
        digit1 = 1
        digit2 = 2
        site = 0

        identifier1 = Identifier(digit1, site)
        identifier2 = Identifier(digit2, site)

        self.assertTrue(identifier1 < identifier2)

    def test_different_digits_same_site_greater(self):
        digit1 = 2
        digit2 = 1
        site = 0

        identifier1 = Identifier(digit1, site)
        identifier2 = Identifier(digit2, site)

        self.assertTrue(identifier1 > identifier2)

    def test_compare_same_digits_different_site(self):
        digit = 1
        site1 = 0
        site2 = 1

        identifier1 = Identifier(digit, site1)
        identifier2 = Identifier(digit, site2)

        self.assertTrue(identifier1 < identifier2)

    def test_compare_same_digits_different_site_greater(self):
        digit = 1
        site1 = 1
        site2 = 0

        identifier1 = Identifier(digit, site1)
        identifier2 = Identifier(digit, site2)

        self.assertTrue(identifier1 > identifier2)

    def test_compare_different_digits_different_site_less(self):
        digit1 = 1
        digit2 = 2
        site1 = 1
        site2 = 0

        identifier1 = Identifier(digit1, site1)
        identifier2 = Identifier(digit2, site2)

        self.assertTrue(identifier1 < identifier2)

    def test_equal(self):
        digit = 1
        site = 0

        identifier1 = Identifier(digit, site)
        identifier2 = Identifier(digit, site)

        self.assertTrue(identifier1 == identifier2)


class TestPosition(Base):
    def test_init(self):
        ids = [Identifier(1, 0), Identifier(2, 1)]

        position = Position(ids)

        self.assertEqual(position.ids, ids)

    def test_init_with_no_ids(self):
        with self.assertRaises(ValueError):
            Position([])

    def test_get_head(self):
        position = Position([Identifier(1, 0), Identifier(2, 1)])

        self.assertEqual(position.head, Identifier(1, 0))

    def test_compare(self):
        position1 = Position([Identifier(1, 0), Identifier(2, 1)])
        position2 = Position([Identifier(1, 0), Identifier(2, 1)])

        self.assertTrue(position1 == position2)

    def test_compare_different_length(self):
        position1 = Position([Identifier(1, 0), Identifier(2, 1)])
        position2 = Position([Identifier(1, 0)])

        self.assertTrue(position1 > position2)

    def test_compare_different_length2(self):
        position1 = Position([Identifier(2, 0)])
        position2 = Position([Identifier(1, 0), Identifier(2, 1)])

        self.assertTrue(position1 > position2)

    def test_compare_different_sites(self):
        position1 = Position([Identifier(1, 0), Identifier(2, 1)])
        position2 = Position([Identifier(1, 0), Identifier(2, 2)])

        self.assertTrue(position1 < position2)

    def test_compare_different_sites2(self):
        position1 = Position([Identifier(1, 1), Identifier(2, 1)])
        position2 = Position([Identifier(1, 0), Identifier(2, 2)])

        self.assertTrue(position1 > position2)


class TestChar(Base):
    def test_init(self):
        position = Position([Identifier(1, 0), Identifier(2, 1)])
        lamport_clock_value = 0
        value = 'a'

        char = Char(position, lamport_clock_value, value)

        self.assertEqual(char.position, position)
        self.assertEqual(char.lamport_clock_value, lamport_clock_value)
        self.assertEqual(char.value, value)
