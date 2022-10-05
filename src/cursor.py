from buffer import Buffer


class Cursor:
    def __init__(self, row=0, col=0):
        self.__row = row
        self.__col = col

    @property
    def position(self) -> tuple[int, int]:
        return self.__row, self.__col

    @property
    def row(self) -> int:
        return self.__row

    @property
    def col(self) -> int:
        return self.__col

    def up(self, buffer: Buffer) -> None:
        if self.__row > 0:
            self.__row -= 1
            self.__push_cursor_to_end_of_line(buffer)

    def down(self, buffer: Buffer) -> None:
        if self.__row < len(buffer) - 1:
            self.__row += 1
            self.__push_cursor_to_end_of_line(buffer)

    def left(self, buffer: Buffer) -> None:
        if self.__col > 0:
            self.__col -= 1
        elif self.__row > 0:
            self.__row -= 1
            self.__col = len(buffer[self.__row])

    def right(self, buffer: Buffer) -> None:
        if self.__col < len(buffer[self.__row]):
            self.__col += 1
        elif self.__row < len(buffer) - 1:
            self.__row += 1
            self.__col = 0

    def __push_cursor_to_end_of_line(self, buffer: Buffer) -> None:
        self.__col = min(self.__col, len(buffer[self.__row])) + 5
