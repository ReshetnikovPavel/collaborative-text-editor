import curses

from src.controller_server import ControllerServer
from src.initializer import Initializer
from src.model import Model
# from src.editor import Editor
from src.utils import *

if __name__ == "__main__":
    site_id = 12345
    model = Model(site_id)
    controller = ControllerServer(site_id)

    model.initialise(controller)
    controller.initialise(model, None)

    model.create_document([])
    while True:
        try:
            command = input(':::')
            if command == 'set_r':
                (host, port, right) = input('host port 0/1:::').split(' ')
                right = True if right == '1' else False
                controller.set_rights(host, port, right)
            elif command == 'r':
                print(controller.rights)
            elif command == 'txt':
                print(controller.model.get_document().lines)
            elif command == 'blame':
                index = input('index:::')
                print(controller.blame(int(index)))
        except:
            pass
