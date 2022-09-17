import curses
import sys

FILEPATH = 'example.py'


class Window:
    def __init__(self, row_num, col_num):
        self.row_count = row_num
        self.col_count = col_num


class Cursor:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def left(self):
        if self.col > 0:
            self.col -= 1

    def right(self, buffer):
        if self.col < len(buffer[self.row]):
            self.col += 1

    def up(self, buffer):
        if self.row > 0:
            self.row -= 1
            self._clamp_col(buffer)

    def down(self, buffer):
        if self.row < len(buffer) - 1:
            self.row += 1
            self._clamp_col(buffer)

    def _clamp_col(self, buffer):
        self.col = min(self.col, len(buffer[self.row]))


def main(stdscr):
    window = Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor()

    with open(FILEPATH, 'r') as f:
        buffer = f.readlines()

    while True:
        stdscr.erase()
        for row, line in enumerate(buffer[:window.row_count]):
            stdscr.addstr(row, 0, line[:window.col_count])
        stdscr.move(cursor.row, cursor.col)

        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
        elif k == "KEY_UP":
            cursor.up(buffer)
        elif k == "KEY_DOWN":
            cursor.down(buffer)
        elif k == "KEY_LEFT":
            cursor.left()
        elif k == "KEY_RIGHT":
            cursor.right(buffer)


if __name__ == '__main__':
    curses.wrapper(main)