import time
import unittest
from typing import List

from src.controller_client import ControllerClient
from src.controller_server import ControllerServer
from src.initializer import get_free_port
from src.model import Model


class ViewPlaceholder:
    def update(self, lines: List[str]):
        self.lines = lines


class TestCursor(unittest.TestCase):
    def setUp(self) -> None:
        site_id = 12345
        model = Model(site_id)
        controller = ControllerServer(site_id)

        model.initialise(controller)
        controller.initialise(model, None)

        model.create_document('')
        self.server = controller

        site_id = get_free_port()
        model = Model(site_id)
        view = ViewPlaceholder()
        controller = ControllerClient(site_id)

        model.initialise(controller)
        controller.initialise(model, view)

        controller.connect_to('127.0.0.1', 12345)

        self.client1 = controller

        site_id = get_free_port()
        model = Model(site_id)
        view = ViewPlaceholder()
        controller = ControllerClient(site_id)

        model.initialise(controller)
        controller.initialise(model, view)

        controller.connect_to('127.0.0.1', 12345)

        self.client2 = controller


    def test_works_with_rights(self):
        self.server.set_rights('127.0.0.1', self.client1.site_id, True)
        self.server.set_rights('127.0.0.1', self.client2.site_id, True)

        self.client1.insert('a', 0)

        time.sleep(1)

        self.assertEqual(self.client1.view.lines, ['a'])
        self.assertEqual(self.client2.view.lines, ['a'])
        self.assertEqual(self.server.model.get_document().lines, ['a'])
