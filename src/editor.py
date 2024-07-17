import curses
import pyperclip
from curses import panel
from cansi import Cansi

from src.buffer import Buffer
from src.pdf_convertor import to_pdf
from src.cursor import Cursor
from src.window import Window
from src.popup import Popup
from src.formatter import highlight_code
from src.utils import parse_args, to_one_dimensional_index


class Editor:
    def __init__(self, stdscr, text: str, controller) -> None:
        self.screen = stdscr
        self.__set_up_screen_options()
        self.controller = controller
        self.buffer = Buffer(text)
        self.cursor = Cursor(0, 0)
        self.window = Window(curses.LINES - 2, curses.COLS - 1)
        self.__cansi = Cansi(self.screen)
        self.history = Popup("History",
                             curses.LINES//2,
                             curses.COLS//2,
                             curses.LINES//4,
                             curses.COLS//4)
        self.history.hide()
        self.blame = Popup("Blame",
                             curses.LINES // 8,
                             curses.COLS // 8,
                             curses.LINES // 2 - curses.LINES // 16,
                             curses.COLS // 2 - curses.COLS // 16)
        self.blame.hide()
        self.screen_panel = panel.new_panel(self.screen)
        self.visual_mode = False

    def __set_up_screen_options(self) -> None:
        self.screen.timeout(500)

    def __draw_text(self) -> None:
        for row, line in enumerate(
                self.buffer[self.window.row: self.window.row + self.window.num_rows-1]):
            self.__cansi.addstr(row+1, 3, highlight_code(line))

    def __draw_lower_status_bar(self) -> None:
        height, width = self.screen.getmaxyx()
        mode = f"Mode: {'VISUAL' if self.visual_mode else 'INSERT'}"
        position = f"{self.cursor.row} {self.cursor.col}"
        space_count = width - len(mode) - len(position) - 1
        status_bar = f"\033[7m{mode}{' '*space_count}{position}\033[0m"

        self.__cansi.addstr(curses.LINES-1, 0, status_bar)

    def __draw_upper_status_bar(self) -> None:
        height, width = self.screen.getmaxyx()
        filename = self.controller.view.doc_name
        host, port = self.controller.get_host_port()
        instruction = f"<F1> Change Mode | <F2> History | <F3> Blame | <F4> Save PDF | <F5> Save"
        address = f"[{host}:{port}]"
        # body = f"{instruction}".center(width)
        space_count = width - len(instruction) - len(address) - len(filename) - 1
        status_bar = f"\033[7m{instruction}{' '*space_count}{filename} {address}\033[0m"

        self.__cansi.addstr(0, 0, status_bar)

    def __draw_line_numbers(self) -> None:
        for i in range(self.buffer.bottom+1):
            num = abs(self.cursor.row-i) % max(1, self.buffer.bottom)
            body = f"{abs(self.cursor.row-i)}".center(3)
            self.__cansi.addstr(min(i+1, curses.LINES-2), 0, f"\033[7m{body}\033[0m")

    def __draw_screen(self) -> None:
        self.screen.clear()
        self.__draw_text()
        self.__draw_upper_status_bar()
        self.__draw_lower_status_bar()
        self.__draw_line_numbers()
        self.screen.move(
            *self.window.get_translated_cursor_coordinates(self.cursor))
        self.screen.refresh()

    def __handle_keypress(self, key: int) -> None:
        if key == curses.KEY_UP and not self.history.is_active:
            self.cursor.up(self.buffer)
            self.window.up(self.cursor)
            self.window.horizontal_scroll(self.cursor)
        elif key == curses.KEY_DOWN and not self.history.is_active:
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
            if self.cursor.position == (0, 0):
                return
            self.cursor.left(self.buffer)
            self.controller.remove(
                to_one_dimensional_index(self.cursor.position,
                                         self.buffer.lines))
        elif key == curses.KEY_DC:
            try:
                if self.cursor.position < (self.buffer.bottom, len(self.buffer.lines[-1])):
                    return
                self.controller.remove(
                    to_one_dimensional_index(
                        self.cursor.position, self.buffer.lines))
            except Exception as e:
                pass
        elif key == curses.KEY_ENTER or key == 10:
            self.controller.insert("\n",
                                   to_one_dimensional_index(
                                       self.cursor.position,
                                       self.buffer.lines))
            self.cursor.push_cursor_to_start_of_line(self.buffer)
        elif key == curses.KEY_RESIZE:
            self.window = Window(curses.LINES - 1, curses.COLS - 1)
        elif key == curses.KEY_F2:
            self.history.is_active = not self.history.is_active
            while self.history.is_active:
                self.history.activate(open("server_history.txt").read().splitlines())
                key = self.screen.getch()
                self.history.handle_keypress(key)
                self.__handle_keypress(key)
        elif key == curses.KEY_F3:
            self.blame.is_active = not self.blame.is_active
            while self.blame.is_active:
                blame_port = self.controller.blame(
                    to_one_dimensional_index(self.cursor.position,
                                             self.buffer.lines))
                self.blame.activate([f"User PORT: {blame_port}"])
                key = self.screen.getch()
                self.blame.handle_keypress(key)
                self.__handle_keypress(key)
        elif key == curses.KEY_F4:
            to_pdf(self.buffer.lines, self.controller.view.doc_name)
        elif key == curses.KEY_F1:
            self.visual_mode = not self.visual_mode
            self.__draw_lower_status_bar()
            first_iter = True
            while self.visual_mode:
                if first_iter:
                    first_iter = False
                    self.start_pos = self.cursor.position
                key = self.screen.getch()
                self.__handle_keypress(key)
                self.screen.chgat(self.cursor.row+1, self.cursor.col+3, 1, curses.A_REVERSE)

        elif self.visual_mode and key == ord('c'):
            self.visual_mode = False
            start = to_one_dimensional_index(self.start_pos, self.buffer.lines)
            curr_pos = to_one_dimensional_index(
                self.cursor.position, self.buffer.lines)
            pyperclip.copy("".join(
                self.controller.model.get_document().lines[start:curr_pos]))
        elif ord(" ") <= key <= ord("~"):
            self.controller.insert(chr(key),
                                   to_one_dimensional_index(
                                       self.cursor.position,
                                       self.buffer.lines))
            self.cursor.right(self.buffer)
            self.window.down(self.buffer, self.cursor)
            self.window.horizontal_scroll(self.cursor)

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
