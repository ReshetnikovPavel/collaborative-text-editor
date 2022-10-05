import curses


from src.initializer import Initializer
# from src.editor import Editor
from src.utils import *


def main(stdscr):
    args = parse_args("filename")
    with open(args.filename) as f:
        text = f.read()
    glyph_list = to_glyph_list(text)

    initializer = Initializer()
    initializer.initialise(glyph_list, stdscr)
    initializer.model.create_document(glyph_list)
    initializer.view.editor.run()



if __name__ == "__main__":
    curses.wrapper(main)