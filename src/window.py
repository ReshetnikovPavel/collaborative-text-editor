from buffer import Buffer
from cursor import Cursor


class Window:
    def __init__(self, num_rows, num_cols, row=0, col=0):
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.row = row
        self.col = col

    @property
    def num_rows(self) -> int:
        return self.__num_rows

    @property
    def num_cols(self) -> int:
        return self.__num_cols

    @property
    def bottom(self) -> int:
        return self.__num_rows + self.row - 1

    def up(self, cursor: Cursor) -> None:
        if cursor.row == self.row - 1 and self.row > 0:
            self.row -= 1

    def down(self, buffer: Buffer, cursor: Cursor) -> None:
        if cursor.row == self.bottom + 1 and self.bottom < buffer.bottom:
            self.row += 1

    def horizontal_scroll(self, cursor, left_margin=5, right_margin=2) -> None:
        num_pages = cursor.col // (self.__num_cols - right_margin)
        self.col = max(
            num_pages * self.__num_cols - right_margin - left_margin, 0)

    def get_translated_cursor_coordinates(self, cursor: Cursor) -> tuple[int, int]:
        return cursor.row - self.row, cursor.col - self.col
