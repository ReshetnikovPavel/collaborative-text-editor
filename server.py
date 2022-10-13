import sys

from src.controller_server import ControllerServer
from src.model import Model
from src.utils import *
from src.document import Document

if __name__ == "__main__":
    args = parse_args("filename")
    with open(args.filename) as f:
        text = f.read()
    site_id = 12345
    model = Model(site_id)
    controller = ControllerServer(site_id)

    model.initialise(controller)
    controller.initialise(model, None)

    model.create_document(text)
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
            elif command == 'r_all':
                for (host, port) in controller.rights:
                    controller.set_rights(host, port, True)

            elif command == 'q':
                sys.exit()
        except Exception:
            pass
