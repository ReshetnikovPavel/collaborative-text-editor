import time
import unittest

from src.crdt import CRDT
from src.initializer import Initializer
from src.document import Document
import src.glyphs
import src.initializer


class ViewPlaceholder:
    def update(self, document: Document):
        self.document = document


class Base(unittest.TestCase):
    def setUp(self):
        self.initializer = Initializer()
        self.initializer.initialise()
        self.controller = self.initializer.controller
        self.controller.view = ViewPlaceholder()

    def tearDown(self):
        self.controller.node.stop()


class TestController(Base):
    def test_create_document(self):
        string = 'The quick brown fox jumps over the lazy dog'
        glyphs = list(src.glyphs.get_from(string))

        self.controller.create_document(glyphs)

        actual = src.glyphs.to_string(self.controller.view.document._glyphs)
        expected = string
        self.assertEqual(actual, expected)

    def test_update_crdt(self):
        string = 'The quick brown fox jumps over the lazy dog'
        glyphs = list(src.glyphs.get_from(string))
        self.controller.create_document(glyphs)

        string2 = 'Hello World'
        crdt2 = self._create_another_crdt(string2)

        self.controller.update_crdt(crdt2)
        actual = src.glyphs.to_string(self.controller.view.document._glyphs)

        self.assertTrue(string in actual, actual)
        self.assertTrue(string2 in actual, actual)

    @staticmethod
    def _create_another_crdt(string):
        glyphs2 = list(src.glyphs.get_from(string))
        initializer2 = Initializer()
        initializer2.initialise()
        controller2 = initializer2.controller
        controller2.view = ViewPlaceholder()
        controller2.create_document(glyphs2)
        crdt2 = controller2.view.document._crdt
        controller2.node.stop()
        return crdt2

    # TODO я пока не придумал, как проверить, успешно ли соединение
    # Поэтому лучше чекнуть лог
    def test_connect_to(self):
        controller2 = self.prepare_another_controller('')
        host = controller2.node.host
        port = controller2.node.port

        self.controller.connect_to(host, port)
        controller2.node.stop()

    # TODO не могу проверить. Потоки. Нужна помощь
    def test_send_crdt(self):
        string = 'The quick brown fox jumps over the lazy dog'
        glyphs = list(src.glyphs.get_from(string))
        self.controller.create_document(glyphs)

        string2 = 'Hello World'
        controller2 = self.prepare_another_controller(string2)
        host = controller2.node.host
        port = controller2.node.port

        time.sleep(2)
        self.controller.connect_to(host, port)

        time.sleep(2)

        self.controller.model.get_document().insert(src.glyphs.Character('a'), 0)
        self.controller.send_crdt(self.controller.model.get_document()._crdt)

        time.sleep(2)

        print(controller2.view.document._glyphs)

    @staticmethod
    def minute_passed(oldepoch):
        return time.time() - oldepoch >= 60

    @staticmethod
    def prepare_another_controller(string):
        glyphs2 = list(src.glyphs.get_from(string))
        initializer2 = Initializer()
        initializer2.initialise()
        controller2 = initializer2.controller
        controller2.view = ViewPlaceholder()
        controller2.create_document(glyphs2)

        return controller2
