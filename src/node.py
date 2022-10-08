from p2pnetwork import node


class Node(node.Node):
    def __init__(self, controller: 'Controller',
                 host: str, port: int, id: int,
                 callback=None, max_connections=0):
        super(Node, self).__init__(host, port, id, callback, max_connections)
        self.controller = controller

    def outbound_node_connected(self, node):
        super().outbound_node_connected(node)
        self.controller.on_someone_joined()

    def inbound_node_connected(self, node):
        super().inbound_node_connected(node)
        self.controller.on_someone_joined()

    def node_message(self, node, data):
        self.process_data(data)

    def process_data(self, data):
        if isinstance(data, bytes):
            self.controller.update_crdt(data)

    def debug_print(self, message):
        with open("debug.txt", "a") as f:
            f.write(message + "\n")
