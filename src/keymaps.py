from abc import ABC, abstractmethod

from cursor import Cursor
from window import Window
from buffer import Buffer


class Command(ABC):
    @abstractmethod
    def do(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class UpCommand(Command):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        self.__cursor = cursor
        self.__window = window
        self.__buffer = buffer

    def do(self):
        self.__cursor.up(self.__buffer)
        self.__window.up(self.__cursor)
        self.__window.horizontal_scroll(self.__cursor)

    def undo(self):
        pass


class DownCommand(Command):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        self.__cursor = cursor
        self.__window = window
        self.__buffer = buffer

    def do(self):
        self.__cursor.down(self.__buffer)
        self.__window.down(self.__buffer, self.__cursor)
        self.__window.horizontal_scroll(self.__cursor)

    def undo(self):
        raise NotImplementedError()


class LeftCommand(Command):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        self.__cursor = cursor
        self.__window = window
        self.__buffer = buffer

    def do(self):
        self.__cursor.left(self.__buffer)
        self.__window.up(self.__cursor)
        self.__window.horizontal_scroll(self.__cursor)

    def undo(self):
        raise NotImplementedError()


class RightCommand(Command):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        self.__cursor = cursor
        self.__window = window
        self.__buffer = buffer

    def do(self):
        self.__cursor.right(self.__buffer)
        self.__window.down(self.__buffer, self.__cursor)
        self.__window.horizontal_scroll(self.__cursor)

    def undo(self):
        raise NotImplementedError()


class DeleteCommand(Command):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        self.last_symbol = None
        self.last_position = None
        self.__cursor = cursor
        self.__window = window
        self.__buffer = buffer

    def do(self):
        self.last_symbol = self.__buffer[self.__cursor.row][self.__cursor.col]
        self.last_position = self.__cursor.position
        self.__buffer.delete(self.__cursor.position, count=1)

    def undo(self):
        self.__buffer.insert(self.last_position, self.last_symbol)


class EnterCommand(Command):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        self.last_position = None
        self.__cursor = cursor
        self.__window = window
        self.__buffer = buffer

    def do(self):
        self.last_position = self.__cursor.position
        self.__buffer.split(self.__cursor.position)

    def undo(self):
        self.__buffer.join(self.    last_position)


class InsertCommand:
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        self.last_position = None
        self.__cursor = cursor
        self.__window = window
        self.__buffer = buffer

    def do(self, text: str):
        self.last_position = self.__cursor.position
        self.__buffer.insert(self.__cursor.position, text)

    def undo(self):
        self.__buffer.delete(self.last_position, count=1)