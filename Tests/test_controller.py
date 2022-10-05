import pickle
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

    def to_string(self):
        return src.glyphs.to_string(self.document.glyphs)


class Base(unittest.TestCase):
    def setUp(self):
        self.initializer = Initializer()
        self.initializer.initialise()
        self.controller = self.initializer.controller
        self.controller.view = ViewPlaceholder()
        self.wait_time = 0.1

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
        pickled_crdt2 = crdt2.pickle()

        self.controller.update_crdt(pickled_crdt2)
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

    def test_connect_to(self):
        controller2 = self.prepare_another_controller('')
        host = controller2.node.host
        port = controller2.node.port

        self.controller.connect_to(host, port)
        controller2.node.stop()
        self.assertTrue(len(self.controller.node.all_nodes) == 1)

    def test_connect_to_have_same_text(self):
        controller2 = self.prepare_another_controller('Hello world')
        host = controller2.node.host
        port = controller2.node.port

        self.controller.connect_to(host, port)

        time.sleep(self.wait_time)

        actual = self.controller.view.to_string()
        self.assertEqual(actual, 'Hello world')
        controller2.node.stop()

    def test_send_crdt(self):
        string = ''
        glyphs = list(src.glyphs.get_from(string))
        self.controller.create_document(glyphs)

        string2 = 'Hello World'
        controller2 = self.prepare_another_controller(string2)
        host = controller2.node.host
        port = controller2.node.port

        self.controller.connect_to(host, port)

        time.sleep(self.wait_time)

        string_to_add = 'a'
        self.controller.model.get_document().insert(
            src.glyphs.Character(string_to_add), 0)
        self.controller.send_crdt(self.controller.model.get_document()._crdt)

        time.sleep(self.wait_time)

        actual = src.glyphs.to_string(controller2.view.document._glyphs)
        expected_possible_1 = string_to_add + string2
        expected_possible_2 = string2 + string_to_add
        self.assertTrue(expected_possible_1 == actual
                        or expected_possible_2 == actual,
                        f'actual: {actual}, expected:'
                        f' {expected_possible_1} or {expected_possible_2}')
        controller2.node.stop()

    @staticmethod
    def prepare_another_controller(string):
        glyphs2 = list(src.glyphs.get_from(string))
        initializer2 = Initializer()
        initializer2.initialise()
        controller2 = initializer2.controller
        controller2.view = ViewPlaceholder()
        controller2.create_document(glyphs2)

        return controller2

    def test_insert(self):
        string = 'Hello World'
        glyphs = list(src.glyphs.get_from(string))
        self.controller.create_document(glyphs)

        self.controller.insert(src.glyphs.Character('a'), 1)

        actual = src.glyphs.to_string(self.controller.view.document._glyphs)
        expected = 'Haello World'
        self.assertEqual(actual, expected)

    def test_insert_but_other_node_also_updated(self):
        controller2 = self.prepare_another_controller('Hello World')
        host = controller2.node.host
        port = controller2.node.port

        time.sleep(self.wait_time)
        self.controller.connect_to(host, port)

        time.sleep(self.wait_time)

        self.controller.insert(src.glyphs.Character('a'), 1)

        time.sleep(self.wait_time)

        actual = src.glyphs.to_string(controller2.view.document._glyphs)
        expected = 'Haello World'
        self.assertEqual(actual, expected)
        controller2.node.stop()

    def test_remove(self):
        controller2 = self.prepare_another_controller('Hello World')
        host = controller2.node.host
        port = controller2.node.port

        time.sleep(self.wait_time)
        self.controller.connect_to(host, port)

        time.sleep(self.wait_time)

        self.controller.remove(1)

        time.sleep(self.wait_time)

        actual = src.glyphs.to_string(controller2.view.document._glyphs)
        expected = 'Hllo World'
        self.assertEqual(actual, expected)
        controller2.node.stop()

    def test_initial_text_is_gone_if_connected_to_another(self):
        self.controller.insert(src.glyphs.Character('a'), 0)
        self.controller.insert(src.glyphs.Character('b'), 1)
        controller2 = self.prepare_another_controller('Hello World')
        host = controller2.node.host
        port = controller2.node.port

        time.sleep(self.wait_time)
        self.controller.connect_to(host, port)

        time.sleep(self.wait_time)

        actual = src.glyphs.to_string(self.controller.view.document._glyphs)
        expected = 'Hello World'
        self.assertEqual(actual, expected)
        controller2.node.stop()

    def test_crdts_are_the_same_after_multiple_iterations(self):
        controller2 = self.prepare_another_controller('Hello World')
        host = controller2.node.host
        port = controller2.node.port

        time.sleep(self.wait_time)
        self.controller.connect_to(host, port)

        time.sleep(self.wait_time)

        self.controller.insert(src.glyphs.Character('a'), 1)
        time.sleep(self.wait_time)
        controller2.insert(src.glyphs.Character('b'), 2)
        time.sleep(self.wait_time)
        self.controller.insert(src.glyphs.Character('c'), 3)
        self.controller.remove(1)
        self.controller.remove(1)
        time.sleep(self.wait_time)
        controller2.remove(1)

        time.sleep(3)

        print('controller1', self.controller.view.document.glyphs)
        print('controller2', controller2.view.document.glyphs)

        actual = src.glyphs.to_string(self.controller.view.document._glyphs)
        expected = 'Hello World'
        self.assertEqual(actual, expected)
        controller2.node.stop()
        time.sleep(4)

    def test_blame(self):
        self.controller.insert(src.glyphs.Character('a'), 0)
        controller2 = self.prepare_another_controller('')
        host = controller2.node.host
        port = controller2.node.port
        self.controller.connect_to(host, port)
        self.controller.insert(src.glyphs.Character('a'), 0)
        controller2.insert(src.glyphs.Character('b'), 0)
        time.sleep(self.wait_time)

        blame1by2 = controller2.blame(0)
        blame1by1 = self.controller.blame(0)

        self.assertTrue(
            str(blame1by1) == str(blame1by2) == str(controller2.get_uuid()),
            f'{blame1by1} {blame1by2} {controller2.get_uuid()}')

        blame2by2 = controller2.blame(1)
        blame2by1 = self.controller.blame(1)

        self.assertTrue(
            str(blame2by1) == str(blame2by2) == str(self.controller.get_uuid()),
            f'{blame2by1} {blame2by2} {self.controller.get_uuid()}')



