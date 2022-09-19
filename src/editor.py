from utils import parse_args
import curses
import sys


class Window:
    pass


class Cursor:
    def __init__(self, row=0, col=0):
        self.__row = row
        self.__col = col

    @property
    def position(self) -> tuple[int, int]:
        return self.__row, self.__col

    def up(self, buffer):
        if self.__row > 0:
            self.__row -= 1
            self.__push_cursor_to_end_of_line(buffer)

    def down(self, buffer):
        if self.__row < len(buffer) - 1:
            self.__row += 1
            self.__push_cursor_to_end_of_line(buffer)

    def left(self, buffer):
        if self.__col > 0:
            self.__col -= 1
        elif self.__row > 0:
            self.__row -= 1
            self.__col = len(buffer[self.__row])

    def right(self, buffer):
        if self.__col < len(buffer[self.__row]):
            self.__col += 1
        elif self.__row < len(buffer) - 1:
            self.__row += 1
            self.__col = 0

    def __push_cursor_to_end_of_line(self, buffer):
        self.__col = min(self.__col, len(buffer[self.__row]))


class Buffer:
    def __init__(self, text=""):
        self.__lines = text.split('\n')

    def __getitem__(self, index: int) -> str:
        return self.__lines[index]

    def __len__(self):
        return len(self.__lines)

    def insert(self, cursor: Cursor, text: str) -> None:
        row, col = cursor.position
        current = self.__lines.pop(row)
        new_line = current[:col] + text + current[col:]
        self.__lines.insert(row, new_line)

    def delete(self, cursor: Cursor, count: int = 1) -> None:
        row, col = cursor.position
        curr_line = self.__lines.pop(row)
        new_line = curr_line[:col] + curr_line[col + count:]
        self.__lines.insert(row, new_line)

    def split(self, cursor: Cursor) -> None:
        row, col = cursor.position
        curr_line = self.__lines.pop(row)
        self.__lines.insert(row, curr_line[:col])
        self.__lines.insert(row + 1, curr_line[col:])

    def join(self, cursor: Cursor) -> None:
        row, col = cursor.position
        current = self.__lines.pop(row)
        next_line = self.__lines.pop(row)
        self.__lines.insert(row, current + next_line)


def main(stdscr):
    args = parse_args("filename")

    with open(args.filename) as f:
        buffer = Buffer(f.read())

    cursor = Cursor()

    while True:
        stdscr.erase()
        for row, line in enumerate(buffer):
            stdscr.addstr(row, 0, line)

        stdscr.move(*cursor.position)

        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
        elif k == "KEY_UP":
            cursor.up(buffer)
        elif k == "KEY_DOWN":
            cursor.down(buffer)
        elif k == "KEY_LEFT":
            cursor.left(buffer)
        elif k == "KEY_RIGHT":
            cursor.right(buffer)


if __name__ == "__main__":
    curses.wrapper(main)
