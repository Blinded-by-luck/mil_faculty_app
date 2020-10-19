
"""
Класс для представления ребра
"""
class Arc:
    Counter = 0
    @classmethod
    def reset_counter(cls):
        cls.Counter = 0

    def __init__(self, node_from, node_to):
        self.node_from = node_from
        self.node_to = node_to
        self.id = Arc.Counter
        print("Arc init: Arc.Counter =", Arc.Counter)
        Arc.Counter += 1

    def __getstate__(self):
        data = [self.node_from.id, self.node_to.id]
        return data
