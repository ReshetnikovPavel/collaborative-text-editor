import time
import unittest
from src.node import Node


class Base(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestNode(Base):
    def test_init(self):
        node = Node(None, 'localhost', 5000, 1)

        self.assertEqual(node.host, 'localhost')
        self.assertEqual(node.port, 5000)

    def test_connect_to(self):
        node_1 = Node(None, "127.0.0.1", 8768, 1)
        node_2 = Node(None, "127.0.0.1", 9765, 2)

        node_1.start()
        node_2.start()

        time.sleep(2)

        node_1.connect_with_node('127.0.0.1', 9765)

        time.sleep(2)

        node_1_connected_to = (str(node_1.all_nodes[0].host), str(node_1.all_nodes[0].port))
        node_2_connected_to = (str(node_2.all_nodes[0].host), str(node_2.all_nodes[0].port))
        self.assertEqual(node_1_connected_to, ('127.0.0.1', '9765'))
        self.assertEqual(node_2_connected_to, ('127.0.0.1', '8768'))

        node_1.stop()
        node_2.stop()
