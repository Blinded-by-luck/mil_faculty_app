from PyQt5.QtGui import QPixmap

"""
Абстрактный класс вершина для представления узлов в сети
"""
class Node:
    Counter = 1

    @classmethod
    def reset_counter(cls):
        cls.Counter = 1
    """Конструктор для создание вершины. Не должен вызываться обособленно"""
    def __init__(self, x=0, y=0, id=None, ingoing_arcs=None, outgoing_arcs=None):
        if ingoing_arcs is None:
            ingoing_arcs = []
        if outgoing_arcs is None:
            outgoing_arcs = []
        if id is None:
            self.id = Node.Counter
        else:
            self.id = id
        print("Node init: Node.Counter =", Node.Counter)
        Node.Counter += 1
        self.x = x
        self.y = y
        self.ingoing_arcs = ingoing_arcs
        self.outgoing_arcs = outgoing_arcs
        self.custom_widget = None

        self.is_under_attack = False
        # Вершина прекращает быть активной после ее защиты (или не защиты),
        # т.е. повторные атаки и защиты запрещены
        self.is_active = True
    """Удаляет вершину со сцены и из модели"""
    def delete(self):
        self.delete_from_scene()
        self.delete_from_model()

    """Удаляет вершину со сцены"""
    def delete_from_scene(self):
        pass

    """Удаляет вершину из модели"""
    def delete_from_model(self):
        pass

"""
Класс для представления компьютера
"""
class Computer(Node):
    """Конструтор для создания компьютера, не должен вызываться обособленно"""
    def __init__(self, x=0, y=0, id=None, ingoing_arcs=None, outgoing_arcs=None):
        super().__init__(x=x, y=y, id=id, ingoing_arcs=ingoing_arcs, outgoing_arcs=outgoing_arcs)
        print("Computer id=", self.id)

    def __getstate__(self):
        data = [self.x, self.y, self.id]
        return data

    def __setstate__(self, data):
        self.__init__(x=data[0], y=data[1], id=data[2])

"""
Класс для представления роутера
"""
class Router(Node):
    def __init__(self, x=0, y=0, id=None, ingoing_arcs=None, outgoing_arcs=None):
        super().__init__(x=x, y=y, id=id, ingoing_arcs=ingoing_arcs, outgoing_arcs=outgoing_arcs)
        print("Router id=", self.id)

    def __getstate__(self):
        data = [self.x, self.y, self.id]
        return data

    def __setstate__(self, data):
        self.__init__(x=data[0], y=data[1], id=data[2])


"""
Класс для представления коммутатора
"""
class Commutator(Node):
    def __init__(self, x=0, y=0, id=None, ingoing_arcs=None, outgoing_arcs=None):
        super().__init__(x=x, y=y, id=id, ingoing_arcs=ingoing_arcs, outgoing_arcs=outgoing_arcs)
        print("Commutator id=", self.id)

    def __getstate__(self):
        data = [self.x, self.y, self.id]
        return data

    def __setstate__(self, data):
        self.__init__(x=data[0], y=data[1], id=data[2])



