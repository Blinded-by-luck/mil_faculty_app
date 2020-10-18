from PyQt5.QtGui import QPixmap

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
        self.pixmap_item = None

    def __getstate__(self):
        data = [self.x, self.y]
        return data

    def __setstate__(self, data):
        self.__init__(x=data[0], y=data[1])


"""
Класс для представления компьютера
"""
class Computer(Node):

    def __init__(self, x=0, y=0, ingoing_arcs=None, outgoing_arcs=None, pixmap_item=None):
        super().__init__(x=x, y=y, ingoing_arcs=ingoing_arcs, outgoing_arcs=outgoing_arcs)
        self.pixmap_item = pixmap_item


"""
Класс для представления роутера
"""
class Router(Node):
    def __init__(self, x=0, y=0, ingoing_arcs=None, outgoing_arcs=None, pixmap_item=None):
        super().__init__(x=x, y=y, ingoing_arcs=ingoing_arcs, outgoing_arcs=outgoing_arcs)
        self.pixmap_item = pixmap_item


"""
Класс для представления коммутатора
"""
class Commutator(Node):
    def __init__(self, x=0, y=0, ingoing_arcs=None, outgoing_arcs=None, pixmap_item=None):
        super().__init__(x=x, y=y, ingoing_arcs=ingoing_arcs, outgoing_arcs=outgoing_arcs)
        self.pixmap_item = pixmap_item


def get_appropriate_pixmap(node):
    if isinstance(node, Computer):
        return QPixmap('Models\\Computer.png')
    else:
        if isinstance(node, Router):
            return QPixmap('Models\\Router.png')
        else:
            if isinstance(node, Commutator):
                return QPixmap('Models\\Commutator.png')
    return None
