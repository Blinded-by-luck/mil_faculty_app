
"""
Класс для представления ребра
"""
class Arc:
    Counter = 1
    @classmethod
    def reset_counter(cls):
        cls.Counter = 1

    def __init__(self, node_from=None, node_to=None, mode=0):
        self.node_from = node_from
        self.node_to = node_to
        self.id = -Arc.Counter
        if mode == 0:
            self.node_from.outgoing_arcs.append(self)
            self.node_to.ingoing_arcs.append(self)
        print("Arc init: Arc.Counter =", Arc.Counter)
        Arc.Counter += 1

    def __getstate__(self):
        data = [self.node_from.id, self.node_to.id]
        return data

    def __setstate__(self, data):
        self.__init__(data[0], data[1], mode=1)
