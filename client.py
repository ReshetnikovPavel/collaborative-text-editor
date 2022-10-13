import curses

from src.controller_client import ControllerClient
from src.editor import Editor
from src.initializer import Initializer, get_free_port
from src.model import Model
# from src.editor import Editor
from src.utils import *
from src.view import View


def main(stdscr):
    site_id = get_free_port()
    model = Model(site_id)
    view = View()
    controller = ControllerClient(site_id)

    model.initialise(controller)
    controller.initialise(model, view)
    view.initialise(controller, Editor(stdscr, '', controller))

    controller.connect_to('127.0.0.1', 12345)
    view.editor.run()


if __name__ == "__main__":
    curses.wrapper(main)