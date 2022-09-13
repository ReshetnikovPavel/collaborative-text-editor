from typing import List


class Identifier:
    def __init__(self, digit: int, site: int):
        self.digit = digit
        self.site = site

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


class Position:
    def __init__(self, ids: List[Identifier]):
        if not ids:
            raise ValueError('ids cannot be empty')
        self.ids = ids

    def __lt__(self, other: 'Position') -> bool:
        for i in range(min(len(self.ids), len(other.ids))):
            if self.ids[i] != other.ids[i]:
                return self.ids[i] < other.ids[i]
        return len(self.ids) < len(other.ids)

    def __eq__(self, other: 'Position') -> bool:
        return self.ids == other.ids

    def __repr__(self):
        return f'Position({self.ids})'

    @property
    def head(self) -> 'Identifier':
        return self.ids[0]


# TODO: Лучше сделать интерфейс для глифа, вдруг от нас попросят сделать не только символы, но и картинки, например.
class Char:
    def __init__(self, position: Position, lamport_clock_value: int, value: str):
        self.position = position
        # TODO: еще пока не разобрался, зачем lamport_clock_value нужно, но вроде как в статье про CRDT это есть.
        self.lamport_clock_value = lamport_clock_value
        self.value = value

