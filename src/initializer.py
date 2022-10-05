import uuid
from random import randint
import socket

from src.model import Model
from src.view import View
from src.controller import Controller
from src.editor import Editor


def get_free_port():
    while True:
        port = randint(32768, 61000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not (sock.connect_ex(('127.0.0.1', port)) == 0):
            return port


class Initializer:
    def __init__(self):
        self.site_id = get_free_port()
        self.model = Model(self.site_id)
        self.view = View()
        self.controller = Controller(self.site_id)

    def initialise(self, text, stdscr):
        self.controller.initialise(self.model, self.view)
        self.model.initialise(self.controller)
        self.view.initialise(self.controller, Editor(stdscr, text, self.controller))


# def get_free_port():
#     while True:
#         port = randint(32768, 61000)
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         if not (sock.connect_ex(('127.0.0.1', port)) == 0):
#             return port