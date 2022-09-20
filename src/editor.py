from utils import parse_args
import curses
import sys


class Window:
    def __init__(self, num_rows, num_cols, row=0, col=0):
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.row = row
        self.col = col

    @property
    def num_rows(self):
        return self.__num_rows

    @property
    def num_cols(self):
        return self.__num_cols

    @property
    def bottom(self):
        return self.__num_rows + self.row - 1

    def up(self, cursor):
        if cursor.row == self.row - 1 and self.row > 0:
            self.row -= 1

    def down(self, buffer, cursor):
        if cursor.row == self.bottom + 1 and self.bottom < len(buffer) - 1:
            self.row += 1

    def horizontal_scroll(self, cursor, left_margin=5, right_margin=2):
        num_pages = cursor.col // (self.__num_cols - right_margin)
        self.col = max(num_pages * self.__num_cols - right_margin - left_margin, 0)

    def get_translated_cursor_coordinates(self, cursor) -> tuple[int, int]:
        return cursor.row - self.row, cursor.col - self.col


class Cursor:
    def __init__(self, row=0, col=0):
        self.__row = row
        self.__col = col

    @property
    def position(self) -> tuple[int, int]:
        return self.__row, self.__col

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col

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
        if new_line == "":
            self.join(cursor)
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

    window = Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor()

    while True:
        stdscr.erase()
        for row, line in enumerate(
                buffer[window.row:window.row + window.num_rows]):
            if row == cursor.row - window.row and window.col > 0:
                line = "«" + line[window.col + 1:]
            if len(line) > window.num_cols:
                line = line[:window.num_cols - 1] + "»"
            stdscr.addstr(row, 0, line)

        stdscr.move(*window.get_translated_cursor_coordinates(cursor))

        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
        elif k == "KEY_UP":
            cursor.up(buffer)
            window.up(cursor)
            window.horizontal_scroll(cursor)
        elif k == "KEY_DOWN":
            cursor.down(buffer)
            window.down(buffer, cursor)
            window.horizontal_scroll(cursor)
        elif k == "KEY_LEFT":
            cursor.left(buffer)
            window.up(cursor)
            window.horizontal_scroll(cursor)
        elif k == "KEY_RIGHT":
            cursor.right(buffer)
            window.down(buffer, cursor)
            window.horizontal_scroll(cursor)
        elif k == "KEY_BACKSPACE":
            cursor.left(buffer)
            buffer.delete(cursor)
        elif k == "\n":
            buffer.split(cursor)
            cursor.right(buffer)
        else:
            buffer.insert(cursor, k)
            for _ in k:
                cursor.right(buffer)


if __name__ == "__main__":
    curses.wrapper(main)
