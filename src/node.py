from typing import List
from src.crdt import CRDT

from p2pnetwork import node
import uuid

from src.document import Document


def _generate_unique_id() -> uuid.UUID:
    return uuid.uuid4()


class Node(node.Node):
    def __init__(self, controller: 'Controller', host: str, port: int, id=None, callback=None, max_connections=0):
        super(Node, self).__init__(host, port, id, callback, max_connections)
        self.controller = controller
        self.buffer = []

    def outbound_node_connected(self, node):
        super().outbound_node_connected(node)
        print(f"{self.id}: Node {node.id} connected")

    def node_message(self, node, data):
        print(f"{self.id}: Node {node.id} sent: {data}")
        self.process_data(data)

    def process_data(self, data):
        if isinstance(data, CRDT):
            self.controller.update_crdt(data)
        else:
            self.buffer.append(data)


