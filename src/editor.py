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
    pass


def main(stdscr):
    pass


if __name__ == "__main__":
    curses.wrapper(main)