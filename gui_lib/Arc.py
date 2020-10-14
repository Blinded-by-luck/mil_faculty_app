"""
Класс для представления ребра
"""

class Arc:
    def __init__(self, node_from, node_to):
        self.node_from = node_from
        self.node_to = node_to

    def __getstate__(self):
        data = [self.node_from.id, self.node_to.id]
        return data
