from abc import ABC, abstractmethod
from typing import List, Generator


class Glyph(ABC):
    @abstractmethod
    def __init__(self, value):
        pass

    @abstractmethod
    def draw(self):
        pass


class Character(Glyph):
    def __init__(self, value: str):
        if len(value) != 1:
            raise ValueError(f'Character must be a single character: {value}')
        self.value = value

    def draw(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"Character('{self.value}')"


class CompositeGlyph(Glyph):
    def __init__(self, value: List[Glyph]):
        self.value = value

    @abstractmethod
    def draw(self):
        for glyph in self.value:
            glyph.draw()


def get_from(string: str) -> Generator[Glyph, None, None]:
    for char in string:
        yield Character(char)


def to_string(glyphs: List[Glyph]) -> str:
    return ''.join([glyph.draw() for glyph in glyphs])


def to_list_of_lists(glyphs: List[Glyph]) -> List[List[Glyph]]:
    lines = [[]]
    i = 0
    for glyph in glyphs:
        if glyph.draw() != "\n":
            lines[i].append(glyph)
        else:
            lines.append([])
            i += 1
    return lines
