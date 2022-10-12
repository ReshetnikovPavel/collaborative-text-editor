import curses
import pyperclip
from curses import panel
from cansi import Cansi

from src.buffer import Buffer
from src.cursor import Cursor
from src.window import Window
from src.formatter import highlight_code
from src.utils import parse_args, to_one_dimensional_index


class Editor:
    def __init__(self, stdscr, glyph_list: str, controller) -> None:
        self.screen = stdscr
        self.controller = controller
        self.buffer = Buffer(glyph_list)
        self.cursor = Cursor()
        self.window = Window(curses.LINES - 1, curses.COLS - 1)
        self.__cansi = Cansi(self.screen)
        self.visual_mode = False

    def __set_up_screen_options(self) -> None:
        self.screen.timeout(500)

    def __draw_text(self) -> None:
        for row, line in enumerate(
                self.buffer[self.window.row: self.window.row + self.window.num_rows]):
            self.__cansi.addstr(row, 0, highlight_code(line))

    def __draw_lower_status_bar(self) -> None:
        # address = f"[{self.controller.get_host_port()}]"
        height, width = self.screen.getmaxyx()
        mode = f"Mode: {'VISUAL' if self.visual_mode else 'INSERT'}"
        position = f"{self.cursor.row} {self.cursor.col}"
        space_count = width - len(mode) - len(position) - 1
        status_bar = f"\033[7m{mode}{' '*space_count}{position}\033[0m"

        self.__cansi.addstr(curses.LINES-1, 0, status_bar)

    def __draw_screen(self) -> None:
        self.screen.clear()
        self.__draw_text()
        self.__draw_lower_status_bar()
        self.screen.move(
            *self.window.get_translated_cursor_coordinates(self.cursor))
        self.screen.refresh()
        # self.screen.nodelay(False)

    def __handle_keypress(self, key: int) -> None:
        if key == curses.KEY_UP:
            self.cursor.up(self.buffer)
            self.window.up(self.cursor)
            self.window.horizontal_scroll(self.cursor)
        elif key == curses.KEY_DOWN:
            self.cursor.down(self.buffer)
            self.window.down(self.buffer, self.cursor)
            self.window.horizontal_scroll(self.cursor)
        elif key == curses.KEY_LEFT:
            self.cursor.left(self.buffer)
            self.window.up(self.cursor)
            self.window.horizontal_scroll(self.cursor)
        elif key == curses.KEY_RIGHT:
            self.cursor.right(self.buffer)
            self.window.down(self.buffer, self.cursor)
            self.window.horizontal_scroll(self.cursor)
        elif key == curses.KEY_BACKSPACE:
            if self.cursor.row > 0:
                self.cursor.left(self.buffer)
                try:
                    self.controller.remove(
                        to_one_dimensional_index(
                            self.cursor.position, self.buffer.lines))
                except Exception as e:
                    pass
        elif key == curses.KEY_DC:
            try:
                self.controller.remove(
                    to_one_dimensional_index(
                        self.cursor.position, self.buffer.lines))
            except Exception as e:
                pass
        elif key == curses.KEY_ENTER or key == 10:
            try:
                self.controller.insert("\n", to_one_dimensional_index(self.cursor.position, self.buffer.lines))
                self.cursor.push_cursor_to_start_of_line(self.buffer)
            except Exception as e:
                pass

            # self.buffer.split(self.__cursor.position)
        elif key == curses.KEY_RESIZE:
            self.window = Window(curses.LINES - 1, curses.COLS - 1)
        elif key == curses.KEY_F1:
            self.visual_mode = not self.visual_mode
            first_iter = True
            while self.visual_mode:
                if first_iter:
                    first_iter = False
                    self.start_pos = self.cursor.position
                key = self.screen.getch()
                self.__handle_keypress(key)
                self.screen.chgat(*self.cursor.position, 1, curses.A_REVERSE)

        elif self.visual_mode and key == ord('c'):
            self.visual_mode = False
            start = to_one_dimensional_index(self.start_pos, self.buffer.lines)
            curr_pos = to_one_dimensional_index(self.cursor.position, self.buffer.lines)
            pyperclip.copy("".join(self.controller.model.get_document().glyphs[start:curr_pos]))
        # elif self.select_mode and key == ord('v'):
        #     self.select_mode = False
        #     # start = to_one_dimensional_index(self.start_pos, self.buffer.lines)
        #     text = pyperclip.paste()
        #     # curr_pos = to_one_dimensional_index(self.__cursor.position, self.buffer.lines)
        #     for char in text:
        #         try:
        #             self.controller.insert(str(char), to_one_dimensional_index(self.__cursor.position, self.buffer.lines))
        #         except:
        #             pass
        #         self.__cursor.right(self.buffer)
        else:
            try:
                self.controller.insert(chr(key), to_one_dimensional_index(self.cursor.position, self.buffer.lines))
                self.cursor.right(self.buffer)
                self.window.down(self.buffer, self.cursor)
                self.window.horizontal_scroll(self.cursor)
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
