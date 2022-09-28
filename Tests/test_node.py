import time
import unittest
from src.node import Node, Client


class Base(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestNode(Base):
    def test_init(self):
        node = Node(Client(), 'localhost', 5000)

        self.assertEqual(node.host, 'localhost')
        self.assertEqual(node.port, 5000)

    def test_connect_to(self):
        node_1 = Node(Client(),"127.0.0.1", 8001, 1)
        node_2 = Node(Client(),"127.0.0.1", 8002, 2)

        node_1.start()
        node_2.start()

        time.sleep(2)

        node_1.connect_with_node('127.0.0.1', 8002)

        time.sleep(2)

        node_1_connected_to = (str(node_1.all_nodes[0].host), str(node_1.all_nodes[0].port))
        node_2_connected_to = (str(node_2.all_nodes[0].host), str(node_2.all_nodes[0].port))
        self.assertEqual(node_1_connected_to, ('127.0.0.1', '8002'))
        self.assertEqual(node_2_connected_to, ('127.0.0.1', '8001'))

        node_1.stop()
        node_2.stop()

    def test_send_message(self):
        node_1 = Node(Client(),"127.0.0.1", 8001, 1)
        node_2 = Node(Client(),"127.0.0.1", 8002, 2)

        node_1.start()
        node_2.start()

        time.sleep(2)

        node_1.connect_with_node('127.0.0.1', 8002)

        time.sleep(2)

        node_1.send_to_nodes('Hello World')

        #print(node_2.buffer)
        #self.assertTrue('Hello World' in node_2.buffer)

    def test_send_crdt(self):
        client_1 = Client()
        client_2 = Client()

        client_1.node.connect_with_node(client_2.node.host, client_2.node.port)

        time.sleep(2)

        client_1.document.insert('Hello World')

