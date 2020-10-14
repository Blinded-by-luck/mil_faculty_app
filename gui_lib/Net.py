

"""
Класс представляющий сеть. Хранит всю необходимую информацию о сети.
"""
from gui_lib import Node
from gui_lib.Arc import Arc


class Net:
    def __init__(self, computers=None, routers=None, commutators=None, concentrators=None, arcs=None, nodes=None):
        self.computers = computers
        self.routers = routers
        self.commutators = commutators
        self.concentrators = concentrators
        self.arcs = arcs
        self.nodes = nodes

    def __getstate__(self):
        counter = 0
        for node in self.computers:
            node.id = counter
            counter += 1
        for node in self.routers:
            node.id = counter
            counter += 1
        for node in self.commutators:
            node.id = counter
            counter += 1
        for node in self.concentrators:
            node.id = counter
            counter += 1
        data = [self.computers, self.routers, self.commutators, self.concentrators, self.arcs]
        return data

    def __setstate__(self, data):
        self.__init__(data[0], data[1], data[2], data[3])
        nodes = {}
        for node in self.computers:
            nodes[node.id] = node
        for node in self.routers:
            nodes[node.id] = node
        for node in self.commutators:
            nodes[node.id] = node
        for node in self.concentrators:
            nodes[node.id] = node
        Node.Counter = len(data[3])
        self.nodes = nodes
        arcs = []
        for i in range(data[4]):
            arcs.append(Arc(nodes[data[4][i][0]], nodes[data[4][i][1]]))
            nodes[data[4][i][0]].outgoing_arcs.append(arcs[i])
            nodes[data[4][i][1]].ingoing_arcs.append(arcs[i])
        self.arcs = arcs
