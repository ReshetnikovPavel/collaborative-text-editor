import curses


from src.initializer import Initializer
# from src.editor import Editor
from src.utils import *


def main(stdscr):
    args = parse_args("filename")
    with open(args.filename) as f:
        text = f.read()

    initializer = Initializer()
    initializer.initialise(text, stdscr)
    initializer.model.create_document(text)
    initializer.view.editor.run()


if __name__ == "__main__":
    curses.wrapper(main)