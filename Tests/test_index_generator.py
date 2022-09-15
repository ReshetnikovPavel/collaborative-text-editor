import unittest
from typing import List
from index_generator import Identifier, Position, Decimal


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

    def test_convert_to_custom_decimal(self):
        ids = Position([Identifier(1, 0), Identifier(2, 1)])

        actual = ids.convert_to_custom_decimal()

        self.assertTrue(actual.digits == [1, 2])

    def assert_generate_between(self, first: Position, second: Position):
        site_id = 1

        actual = Position.generate_between(first, second, site_id)

        self.assertTrue(first < actual < second)

    def test_generate_between(self):
        self.assert_generate_between(
            Position([Identifier(1, 0), Identifier(1, 2)]),
            Position([Identifier(1, 0), Identifier(2, 1)]))

    def test_generate_between2(self):
        self.assert_generate_between(
            Position([Identifier(1, 0)]),
            Position([Identifier(1, 1)]))

    def test_generate_between3(self):
        self.assert_generate_between(
            Position([Identifier(1, 0)]),
            Position([Identifier(1, 0), Identifier(2, 3)]))

    def test_generate_between4(self):
        with self.assertRaises(ValueError):
            self.assert_generate_between(
                Position([Identifier(2, 0)]),
                Position([Identifier(1, 0), Identifier(2, 3)]))


class TestCustomDecimal(Base):
    def test_init(self):
        digits = [1, 2, 3, 4, 5]

        decimal = Decimal(digits)

        self.assertTrue(decimal.digits == digits)

    def test_convert_to_position(self):
        previous_pos = Position([Identifier(1, 0), Identifier(2, 1)])
        next_pos = Position([Identifier(1, 2), Identifier(2, 2)])
        decimal = Decimal([1, 2, 3])

        actual = decimal.convert_to_position_between(previous_pos, next_pos, 2)

        self.assertEqual(
            actual.ids, [Identifier(1, 0), Identifier(2, 1), Identifier(3, 2)])

    def assert_add(self, first: List[int], second: List[int],
                   expected: List[int]):
        first = Decimal(first)
        second = Decimal(second)

        actual = (first + second).digits

        self.assertEqual(expected, actual)

    def test_add_zeros(self):
        self.assert_add([0, 0], [0, 0], [0, 0])

    def test_add_without_carry(self):
        self.assert_add([5, 5], [5, 6], [10, 11])

    def test_add_with_carry(self):
        base = Decimal.Base
        self.assert_add([base - 2, base // 2],
                        [0, (base // 2) + 1],
                        [base - 1, 1])

    def test_add_overflow(self):
        base = Decimal.Base
        with self.assertRaises(ValueError):
            self.assert_add([base - 1, base - 1], [0, 1], [base, 0])

    def test_add_different_length(self):
        self.assert_add([1, 2], [1, 2, 3, 4], [2, 4, 3, 4])

    def assert_plus_number_less_than(self, first: List[int],
                                     second: List[int]):
        decimal = Decimal(first)
        delta = Decimal(second)

        actual = decimal.plus_number_less_than(delta)

        self.assertTrue(actual < decimal + delta,
                        f"{actual} should have been less than {decimal}")
        self.assertTrue(actual > decimal,
                        f"{actual} should have been greater than {decimal}")

    def test_plus_number_less_than_the_same(self):
        self.assert_plus_number_less_than([1], [1])

    def test_plus_number_less_than(self):
        self.assert_plus_number_less_than([1, 0, 3, 4], [0, 0, 1])

    def assert_sub(self, first: List[int],
                   second: List[int],
                   expected: List[int]):
        first = Decimal(first)
        second = Decimal(second)

        actual = (first - second).digits

        self.assertTrue(actual == expected)

    def test_sub_zeros(self):
        self.assert_sub([0, 0], [0, 0], [0, 0])

    def test_sub_without_carry(self):
        self.assert_sub([11, 4], [3, 2], [11 - 3, 4 - 2])

    def test_sub_with_carry(self):
        base = Decimal.Base
        self.assert_sub([11, 2], [3, 4], [11 - 3 - 1, base - 2])

    def test_sub_different_length(self):
        base = Decimal.Base
        self.assert_sub([1], [0, 1], [0, base - 1])

    def test_sub_lesser_minus_greater(self):
        with self.assertRaises(ValueError):
            self.assert_sub([0, 1], [1, 0], [])
