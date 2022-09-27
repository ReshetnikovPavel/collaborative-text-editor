import curses
import sys

from utils import parse_args


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
        self.__lines = text.split("\n")

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


class Editor:
    def __init__(self, stdscr, text: str) -> None:
        self.__stdscr = stdscr
        self.__buffer = Buffer(text)
        self.__cursor = Cursor()
        self.__window = Window(curses.LINES, curses.COLS - 1)

    def __set_color_scheme(self) -> None:
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        self.__stdscr.bkgd(" ", curses.color_pair(1) | curses.A_BOLD | curses.A_REVERSE)

    def __draw_text(self) -> None:
        for row, line in enumerate(self.__buffer[self.__window.row: self.__window.row + self.__window.num_rows]):
            self.__stdscr.addstr(row, 0, line)

    def __draw_screen(self) -> None:
        self.__stdscr.clear()
        self.__draw_text()
        self.__stdscr.move(*self.__window.get_translated_cursor_coordinates(self.__cursor))
        self.__stdscr.refresh()

    def __handle_keypress(self, key: int) -> None:
        if key == curses.KEY_UP:
            self.__cursor.up(self.__buffer)
            self.__window.up(self.__cursor)
            self.__window.horizontal_scroll(self.__cursor)
        elif key == curses.KEY_DOWN:
            self.__cursor.down(self.__buffer)
            self.__window.down(self.__buffer, self.__cursor)
            self.__window.horizontal_scroll(self.__cursor)
        elif key == curses.KEY_LEFT:
            self.__cursor.left(self.__buffer)
            self.__window.up(self.__cursor)
            self.__window.horizontal_scroll(self.__cursor)
        elif key == curses.KEY_RIGHT:
            self.__cursor.right(self.__buffer)
            self.__window.down(self.__buffer, self.__cursor)
            self.__window.horizontal_scroll(self.__cursor)
        elif key == curses.KEY_BACKSPACE:
            self.__buffer.delete(self.__cursor)
        elif key == curses.KEY_DC:
            self.__buffer.delete(self.__cursor, count=1)
        elif key == curses.KEY_ENTER or key == 10:
            self.__buffer.split(self.__cursor)
        elif key == curses.KEY_RESIZE:
            self.__window = Window(curses.LINES - 1, curses.COLS - 1)
        else:
            self.__buffer.insert(self.__cursor, chr(key))

    def run(self) -> None:
        self.__set_color_scheme()
        self.__draw_screen()
        while True:
            key = self.__stdscr.getch()
            self.__handle_keypress(key)
            self.__draw_screen()


def main(stdscr):
    args = parse_args("filename")
    with open(args.filename) as f:
        text = f.read()
    editor = Editor(stdscr, text)
    editor.run()


if __name__ == "__main__":
    curses.wrapper(main)
