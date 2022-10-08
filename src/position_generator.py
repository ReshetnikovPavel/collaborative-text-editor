from typing import List, Generator


def generate(amount: int, site: int) -> Generator['Position', None, None]:
    start = Position.get_min(site)
    end = Position.get_max(site)

    current = generate_between(start, end, site)
    yield current

    for i in range(amount - 1):
        current = generate_between(current, end, site)
        yield current


def generate_between(start: 'Position',
                     end: 'Position',
                     site: int) -> 'Position':
    head_start = start.head if start.has_head else Identifier.get_min(site)
    head_end = end.head if end.has_head else Identifier.get_max(site)

    if head_start.digit != head_end.digit:
        return _generate_between_arithmetically(start, end, site)

    if head_start.site < head_end.site:
        without_head = generate_between(start.without_head, Position([]), site)
        return Position([head_start]) + without_head

    if head_start.site == head_end.site:
        without_head = generate_between(start.without_head,
                                        end.without_head, site)
        return Position([head_start]) + without_head

    raise ValueError('Invalid site ordering')


def _generate_between_arithmetically(start: 'Position',
                                     end: 'Position',
                                     site: int) -> 'Position':
    start_number = start.convert_to_custom_decimal()
    end_number = end.convert_to_custom_decimal()

    delta = end_number - start_number
    next_number = start_number.plus_number_less_than(delta)

    return next_number.convert_to_position_between(start, end, site)


class Position:
    def __init__(self, ids: List['Identifier']):
        self.ids = ids

    def __lt__(self, other: 'Position') -> bool:
        for i in range(min(len(self.ids), len(other.ids))):
            if self.ids[i] != other.ids[i]:
                return self.ids[i] < other.ids[i]
        return len(self.ids) < len(other.ids)

    def __eq__(self, other: 'Position') -> bool:
        return self.ids == other.ids

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.ids + other.ids)

    def __hash__(self):
        return hash(tuple(self.ids))

    def __repr__(self):
        return f'Position({self.ids})'

    @property
    def head(self) -> 'Identifier':
        return self.ids[0]

    @property
    def without_head(self) -> 'Position':
        return Position(self.ids[1:])

    @property
    def has_head(self):
        return len(self.ids) > 0

    def convert_to_custom_decimal(self) -> 'Decimal':
        return Decimal(list(map(lambda x: x.digit, self.ids)))

    @staticmethod
    def get_min(site: int) -> 'Position':
        return Position([Identifier.get_min(site)])

    @staticmethod
    def get_max(site: int) -> 'Position':
        return Position([Identifier.get_max(site)])


class Identifier:
    def __init__(self, digit: int, site: int):
        self._check_digit(digit)
        self.digit = digit
        self.site = site

    @staticmethod
    def _check_digit(digit: int):
        if digit > Decimal.Base:
            raise ValueError(f'Digit cannot be greater than'
                             f' Decimal.Base = {Decimal.Base}')
        if digit < 0:
            raise ValueError('Digit cannot be negative')

    def __lt__(self, other: 'Identifier') -> bool:
        if self.digit < other.digit:
            return True
        if self.digit == other.digit:
            return self.site < other.site
        return False

    def __eq__(self, other: 'Identifier') -> bool:
        return self.digit == other.digit and self.site == other.site

    def __repr__(self):
        return f'Identifier({self.digit}, {self.site})'

    def __hash__(self):
        return hash((self.digit, self.site))

    @staticmethod
    def get_min(site: int) -> 'Identifier':
        return Identifier(0, site)

    @staticmethod
    def get_max(site: int) -> 'Identifier':
        return Identifier(Decimal.Base, site)


class Decimal:
    Base = 256

    def __init__(self, digits: List[int]):
        self.digits = digits

    def __add__(self, other: 'Decimal') -> 'Decimal':
        max_number_of_digits = max(len(self.digits), len(other.digits))
        result = [0] * max_number_of_digits
        carry = 0
        for i in reversed(range(max_number_of_digits)):
            a = self.digits[i] if i < len(self.digits) else 0
            b = other.digits[i] if i < len(other.digits) else 0
            c = a + b + carry
            carry = c // Decimal.Base
            result[i] = c % Decimal.Base
        if carry:
            raise ValueError(
                f'Overflow: sum must be less than 1 in base {self.Base}')
        return Decimal(result)

    def __sub__(self, other: 'Decimal') -> 'Decimal':
        if self < other:
            raise ValueError(f'Cannot subtract {other} from {self}:'
                             f' result must be positive')
        max_number_of_digits = max(len(self.digits), len(other.digits))
        result = [0] * max_number_of_digits
        carry = 0
        for i in reversed(range(max_number_of_digits)):
            a = self.digits[i] if i < len(self.digits) else 0
            b = other.digits[i] if i < len(other.digits) else 0
            c = a - b - carry
            carry = 0 if c >= 0 else 1
            result[i] = c + Decimal.Base if c < 0 else c
        return Decimal(result)

    def __lt__(self, other):
        for i in range(max(len(self.digits), len(other.digits))):
            a = self.digits[i] if i < len(self.digits) else 0
            b = other.digits[i] if i < len(other.digits) else 0
            if a != b:
                return a < b
        return False

    def __eq__(self, other):
        return self.digits == other.digits

    def __repr__(self):
        return f'Decimal({self.digits})'

    def plus_number_less_than(self, other: 'Decimal') -> 'Decimal':
        small_number = other._get_slightly_smaller_number()
        result = self + small_number
        return result if result.digits[-1] != 0 else result + small_number

    def _get_slightly_smaller_number(self) -> 'Decimal':
        first_nonzero_digit_index = self._get_first_nonzero()
        return Decimal(self.digits[:first_nonzero_digit_index] + [0, 1])

    def _get_first_nonzero(self) -> int:
        return next((i for i, x in enumerate(self.digits) if x != 0), None)

    def convert_to_position_between(self,
                                    before: Position,
                                    after: Position,
                                    creation_site: int) -> Position:
        ids = []
        for index, digit in enumerate(self.digits):
            if index == len(self.digits) - 1:
                ids.append(Identifier(digit, creation_site))
            elif index < len(before.ids) and digit == before.ids[index].digit:
                ids.append(before.ids[index])
            elif index < len(after.ids) and digit == after.ids[index].digit:
                ids.append(after.ids[index])
            else:
                ids.append(Identifier(digit, creation_site))
        return Position(ids)
