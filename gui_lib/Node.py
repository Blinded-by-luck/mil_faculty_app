
"""
Абстрактный класс вершина для представления узлов в сети
"""

class Node:
    Counter = 0

    def __init__(self, x=0, y=0, ingoing_arcs=None, outgoing_arcs=None):
        if ingoing_arcs is None:
            ingoing_arcs = []
        if outgoing_arcs is None:
            outgoing_arcs = []
        self.id = Node.Counter
        Node.Counter += 1
        self.x = x
        self.y = y
        self.ingoing_arcs = ingoing_arcs
        self.outgoing_arcs = outgoing_arcs

    def __getstate__(self):
        data = [self.x, self.y]
        return data

    def __setstate__(self, data):
        self.__init__(x=data[0], y=data[1])
