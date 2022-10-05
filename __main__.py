import curses


from src.initializer import Initializer
# from src.editor import Editor
from src.utils import *


def main(stdscr):
    args = parse_args("filename", "server", "host", "port")
    with open(args.filename) as f:
        text = f.read()
    host = args.host
    port = args.port
    server = args.server
    initializer = Initializer()
    initializer.initialise(text, stdscr)
    initializer.model.create_document(text)
    if server != "0":
        initializer.controller.connect_to(host, int(port))
    initializer.view.editor.run()
    # if host=="0" and port=="0":
    #     initializer.controller.connect_to(host, port)


if __name__ == "__main__":
    curses.wrapper(main)