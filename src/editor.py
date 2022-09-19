import curses


class Window:
    pass


class Cursor:
    def __init__(self, row=0, col=0):
        self.__row = row
        self.__col = col

    @property
    def position(self) -> tuple[int, int]:
        return self.__row, self.__col


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
    pass


if __name__ == "__main__":
    curses.wrapper(main)