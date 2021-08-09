from gui_lib.Nodes import Node
from gui_lib.Nodes import Commutator
from gui_lib.Nodes import Computer
from gui_lib.Nodes import Router
from gui_lib.Arc import Arc

"""
Класс представляющий сеть. Хранит всю необходимую информацию о сети.
Составная часть бекенда канваса (Canvas).
"""
class Net:
    def __init__(self, computers=None, routers=None, commutators=None, arcs=None, nodes=None):
        self.computers = computers
        self.routers = routers
        self.commutators = commutators
        self.arcs = arcs
        self.nodes = nodes

    def add_node(self, node):
        if isinstance(node, Computer):
            self.computers[node.id] = node
        elif isinstance(node, Router):
            self.routers[node.id] = node
        elif isinstance(node, Commutator):
            self.commutators[node.id] = node
        else:
            raise ValueError("Unknown node type")
        self.nodes[node.id] = node

    def renumbering_nodes(self):
        self.computers.clear()
        self.routers.clear()
        self.commutators.clear()
        counter = 1
        for key_node in self.nodes:
            node = self.nodes[key_node]
            node.id = counter
            if isinstance(node, Computer):
                self.computers[node.id] = node
            elif isinstance(node, Router):
                self.routers[node.id] = node
            else:
                self.commutators[node.id] = node
            counter += 1
        Node.Counter = counter

    def updating_nodes_dict(self):
        self.nodes.clear()
        for key_node in self.computers:
            node = self.computers[key_node]
            self.nodes[node.id] = node
        for key_node in self.routers:
            node = self.routers[key_node]
            self.nodes[node.id] = node
        for key_node in self.commutators:
            node = self.commutators[key_node]
            self.nodes[node.id] = node

    def __getstate__(self):
        self.renumbering_nodes()
        self.updating_nodes_dict()
        data = [self.computers, self.routers, self.commutators, self.arcs]
        return data

    def __setstate__(self, data):
        nodes = {}
        self.__init__(data[0], data[1], data[2], data[3])
        for key_node in self.computers:
            node = self.computers[key_node]
            nodes[node.id] = node
        for key_node in self.routers:
            node = self.routers[key_node]
            nodes[node.id] = node
        for key_node in self.commutators:
            node = self.commutators[key_node]
            nodes[node.id] = node
        self.nodes = nodes
        for key_arc in self.arcs:
            arc = self.arcs[key_arc]
            # arc.node_from и arc.node_to сейчас содержат id узлов
            node_from_id = arc.node_from
            node_to_id = arc.node_to
            arc.node_from = nodes[node_from_id]
            arc.node_to = nodes[node_to_id]
            arc.node_from.outgoing_arcs.append(arc)
            arc.node_to.ingoing_arcs.append(arc)














