import curses

from cansi import Cansi

from buffer import Buffer
from cursor import Cursor
from window import Window
from formatter import highlight_code
from utils import parse_args


class Editor:
    def __init__(self, stdscr, text: str) -> None:
        self.__screen = stdscr
        self.__cansi = Cansi(self.__screen)
        self.__buffer = Buffer(text)
        self.__cursor = Cursor()
        self.__window = Window(curses.LINES, curses.COLS - 1)

    def __draw_text(self) -> None:
        for row, line in enumerate(
                self.__buffer[self.__window.row: self.__window.row + self.__window.num_rows]):
            # self.__cansi.addstr(row, 0, f"{row:3} | ")
            self.__cansi.addstr(row, 0, highlight_code(line))

    def __draw_screen(self) -> None:
        self.__screen.clear()
        self.__draw_text()
        self.__screen.move(
            *self.__window.get_translated_cursor_coordinates(self.__cursor))
        self.__screen.refresh()

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
            self.__buffer.delete(self.__cursor.position)
        elif key == curses.KEY_DC:
            self.__buffer.delete(self.__cursor.position, count=1)
        elif key == curses.KEY_ENTER or key == 10:
            self.__buffer.split(self.__cursor.position)
        elif key == curses.KEY_RESIZE:
            self.__window = Window(curses.LINES - 1, curses.COLS - 1)
        else:
            self.__buffer.insert(self.__cursor.position, chr(key))

    def run(self) -> None:
        self.__draw_screen()
        while True:
            key = self.__screen.getch()
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
