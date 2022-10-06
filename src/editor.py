import curses

from cansi import Cansi

from src.buffer import Buffer
from src.cursor import Cursor
from src.window import Window
from src.formatter import highlight_code
from src.utils import parse_args, to_one_dimensional_index


class Editor:
    def __init__(self, stdscr, glyph_list: list, controller) -> None:
        self.controller = controller
        self.screen = stdscr
        self.screen.timeout(500)
        self.__cansi = Cansi(self.screen)
        self.buffer = Buffer(glyph_list)
        self.__cursor = Cursor()
        self.__window = Window(curses.LINES - 1, curses.COLS - 1)

    def __draw_text(self) -> None:
        for row, line in enumerate(
                self.buffer[self.__window.row: self.__window.row + self.__window.num_rows]):
            self.__cansi.addstr(row, 0, highlight_code(line))

    def __draw_screen(self) -> None:
        self.screen.clear()
        self.__draw_text()
        self.__cansi.addstr(curses.LINES-1, 0, f"Host and Port: {self.controller.get_host_port()}")
        self.screen.move(
            *self.__window.get_translated_cursor_coordinates(self.__cursor))
        self.screen.refresh()
        # self.screen.nodelay(False)

    def __handle_keypress(self, key: int) -> None:
        if key == curses.KEY_UP:
            self.__cursor.up(self.buffer)
            self.__window.up(self.__cursor)
            self.__window.horizontal_scroll(self.__cursor)
        elif key == curses.KEY_DOWN:
            self.__cursor.down(self.buffer)
            self.__window.down(self.buffer, self.__cursor)
            self.__window.horizontal_scroll(self.__cursor)
        elif key == curses.KEY_LEFT:
            self.__cursor.left(self.buffer)
            self.__window.up(self.__cursor)
            self.__window.horizontal_scroll(self.__cursor)
        elif key == curses.KEY_RIGHT:
            self.__cursor.right(self.buffer)
            self.__window.down(self.buffer, self.__cursor)
            self.__window.horizontal_scroll(self.__cursor)
        elif key == curses.KEY_BACKSPACE:
            self.__cursor.left(self.buffer)
            try:
                self.controller.remove(
                    to_one_dimensional_index(
                        self.__cursor.position, self.buffer.lines))
            except Exception as e:
                pass
        elif key == curses.KEY_DC:
            try:
                self.controller.remove(
                    to_one_dimensional_index(
                        self.__cursor.position, self.buffer.lines))
            except Exception as e:
                pass
        elif key == curses.KEY_ENTER or key == 10:
            try:
                self.controller.insert("\n", to_one_dimensional_index(self.__cursor.position, self.buffer.lines))
                self.__cursor.push_cursor_to_start_of_line(self.buffer)
            except Exception as e:
                pass

            # self.buffer.split(self.__cursor.position)
        elif key == curses.KEY_RESIZE:
            self.__window = Window(curses.LINES - 1, curses.COLS - 1)
        else:
            try:
                self.controller.insert(chr(key), to_one_dimensional_index(self.__cursor.position, self.buffer.lines))
                self.__cursor.right(self.buffer)
                self.__window.down(self.buffer, self.__cursor)
                self.__window.horizontal_scroll(self.__cursor)
            except Exception as e:
                pass
            # self.screen.touchwin()
            # self.buffer.insert(self.__cursor.position, chr(key))


    def run(self) -> None:
        self.__draw_screen()
        while True:
            key = self.screen.getch()
            self.__handle_keypress(key)
            self.__draw_screen()


# def run(stdscr):
#     args = parse_args("filename")
#     with open(args.filename) as f:
#         text = f.read()
#     editor = Editor(stdscr, text)
#     editor.run()


# if __name__ == "__main__":
#     curses.wrapper(run)
