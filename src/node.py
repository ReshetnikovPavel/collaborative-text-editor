from uuid import UUID

from p2pnetwork import node

from src.crdt import CRDT


class Node(node.Node):
    def __init__(self, controller: 'Controller',
                 host: str, port: int, id: UUID,
                 callback=None, max_connections=0):
        super(Node, self).__init__(host, port, id, callback, max_connections)
        self.controller = controller
        self.buffer = b''
        self.message_size = 0

    def outbound_node_connected(self, node):
        super().outbound_node_connected(node)
        print(f"{self.id}: Node {node.id} connected")

    def inbound_node_connected(self, node):
        super().inbound_node_connected(node)
        print(f"{self.id}: Node {node.id} connected")
        self.controller.on_someone_joined()

    def node_message(self, node, data):
        print(f"{self.id}: Node {node.id} sent: {data}")
        self.process_data(data)

    def process_data(self, data):
        if isinstance(data, int):
            self.message_size = data
        elif isinstance(data, bytes):
            self.controller.update_crdt(data)






