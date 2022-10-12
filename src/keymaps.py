from abc import ABC, abstractmethod

from src.cursor import Cursor
from src.window import Window
from src.buffer import Buffer


class Command(ABC):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        self.cursor = cursor
        self.window = window
        self.buffer = buffer

    @abstractmethod
    def do(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class UpCommand(Command):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        super().__init__(cursor, window, buffer)

    def do(self):
        self.cursor.up(self.buffer)
        self.window.up(self.cursor)
        self.window.horizontal_scroll(self.cursor)

    def undo(self):
        pass


class DownCommand(Command):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        super().__init__(cursor, window, buffer)

    def do(self):
        self.cursor.down(self.buffer)
        self.window.down(self.buffer, self.cursor)
        self.window.horizontal_scroll(self.cursor)

    def undo(self):
        raise NotImplementedError()


class LeftCommand(Command):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        super().__init__(cursor, window, buffer)

    def do(self):
        self.cursor.left(self.buffer)
        self.window.up(self.cursor)
        self.window.horizontal_scroll(self.cursor)

    def undo(self):
        raise NotImplementedError()


class RightCommand(Command):
    def __init__(self, cursor: Cursor, window: Window, buffer: Buffer):
        super().__init__(cursor, window, buffer)

    def do(self):
        self.cursor.right(self.buffer)
        self.window.down(self.buffer, self.cursor)
        self.window.horizontal_scroll(self.cursor)

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
        self.__buffer.join(self.last_position)


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