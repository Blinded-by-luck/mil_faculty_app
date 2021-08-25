"""
Класс для представления ребра
Включает в себя бекенд и фронтенд.
"""
class Arc:
    Counter = 1

    @classmethod
    def reset_counter(cls):
        cls.Counter = 1

    # mode=0 означает создание не при загрузке
    def __init__(self, node_from=None, node_to=None, mode=0):
        self.node_from = node_from
        self.node_to = node_to
        self.id = -Arc.Counter
        """Фронтенд ребра"""
        self.custom_line = None
        if mode == 0:
            self.node_from.outgoing_arcs.append(self)
            self.node_to.ingoing_arcs.append(self)
        print("Arc init: Arc.Counter =", Arc.Counter)
        print("Arc id=", self.id)
        Arc.Counter += 1

    """Удаляет ребро со сцены и из модели"""
    def delete(self):
        self.delete_from_scene()
        self.delete_from_model()

    """Удаляет ребро со сцены"""
    def delete_from_scene(self):
        pass

    """Удаляет ребро из модели"""
    def delete_from_model(self):
        pass

    def __getstate__(self):
        data = [self.node_from.id, self.node_to.id]
        return data

    def __setstate__(self, data):
        self.__init__(data[0], data[1], mode=1)
