import curses
from curses import panel
from typing import List


class Popup():
    def __init__(self, title, num_rows, num_cols, row, col):
        self.title = title
        self.win = curses.newwin(num_rows, num_cols, row, col)
        self.panel = panel.new_panel(self.win)
        self.num_rows = num_rows
        self.curr_row = 0
        self.is_active = False

    def hide(self) -> None:
        self.panel.hide()

    def show(self) -> None:
        self.panel.show()

    def __draw_title(self) -> None:
        self.win.addstr(0, 2, self.title)

    def __draw_content(self, content: List[str]) -> None:
        for i, value in enumerate(content[self.curr_row: self.curr_row + self.num_rows-1]):
            self.win.addstr(min(i+1, self.num_rows-2), 1, value)

    def activate(self, content: List[str]) -> None:
        self.win.clear()
        self.win.border()
        self.__draw_title()
        self.__draw_content(content)
        self.win.refresh()

    def handle_keypress(self, key) -> None:
        if key == curses.KEY_UP:
            self.curr_row = max(0, self.curr_row-1)
        elif key == curses.KEY_DOWN:
            self.curr_row = min(self.num_rows, self.curr_row+1)
        else:
            pass


# class HistoryPopup(Popup):
#     def __init__(self, num_rows, num_cols, row, col):
#         super().__init__(num_rows, num_cols, row, col)
#
#     def handle_keypress(self) -> None:
#         key = self.win.getch()
#         if key == curses.KEY_DOWN:
#             pass




