from gui_lib.Nodes import Node
from gui_lib.Nodes import Commutator
from gui_lib.Nodes import Computer
from gui_lib.Nodes import Router
from gui_lib.Arc import Arc

"""
Класс представляющий сеть. Хранит всю необходимую информацию о сети.
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
        if isinstance(node, Router):
            self.routers[node.id] = node
        if isinstance(node, Commutator):
            self.commutators[node.id] = node
        self.nodes[node.id] = node

    def __getstate__(self):
        self.computers.clear()
        self.routers.clear()
        self.commutators.clear()
        counter = 0
        for key_node in self.nodes:
            node = self.nodes[key_node]
            node.id = counter
            if isinstance(node, Computer):
                self.computers[node.id] = node
            else:
                if isinstance(node, Router):
                    self.routers[node.id] = node
                else:
                    self.commutators[node.id] = node
            counter += 1
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
        Node.Counter = counter # Проверить
        data = [self.computers, self.routers, self.commutators, self.arcs]
        return data

    def __setstate__(self, data):
        nodes = {}
        self.__init__(data[0], data[1], data[2])
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
        arcs = {}
        for key_arc in data[3]:
            arcs[Arc.Counter] = Arc(nodes[data[3][key_arc][0]], nodes[data[3][key_arc][1]])
            nodes[data[3][key_arc][0]].outgoing_arcs.append(arcs[Arc.Counter - 1])
            nodes[data[3][key_arc][1]].ingoing_arcs.append(arcs[Arc.Counter - 1])
        self.arcs = arcs














